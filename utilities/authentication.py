from backend.enums.user import Role
from backend.utilities.mailing import mail_reset_link
from backend.utilities.session import create_local_session
from backend.services.user import get_global_by_email, get_local_by_id
from backend.utilities.security import verify_password, hash_password, exclude_fields
from backend.models.admin import AdminAccount, AdminSession, AdminPasswordReset, AdminPasswordChange
from backend.models.alumni import AlumniAccount, AlumniSession, AlumniPasswordReset, AlumniPasswordChange
from backend.utilities.date_time import auth_reset_utc_now_expires_at, get_session_cookie_lifespan_seconds
from backend.schemas.authentication import AuthLoginInput, AuthForgotPassInput, AuthResetPassInput, AuthChangePassInput

from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import Session, select, update, and_
from fastapi import HTTPException, status, Response

def add_local_change_record(user_id: int, ChangeModel: AdminPasswordChange | AlumniPasswordChange, session: Session):
   """Add a change record to a specific change record model."""
   new_change_record = ChangeModel(user_id = user_id)
   session.add(new_change_record)
   session.commit()
   session.refresh(new_change_record)
   
def add_local_reset_record(user_id: int, ResetModel: AdminPasswordReset | AlumniPasswordReset, session: Session) -> str:
   """Add a reset record to a specific reset record model."""
   new_reset_record_token = str(uuid4())
   new_reset_record = ResetModel(
      user_id = user_id,
      token = new_reset_record_token,
      expires_at = auth_reset_utc_now_expires_at()
   )
   session.add(new_reset_record)
   session.commit()
   session.refresh(new_reset_record)
   return new_reset_record_token

def get_local_reset_record_by_token(reset_token: str, ResetModel: AdminPasswordReset | AlumniPasswordReset, session: Session) -> AdminPasswordReset | AlumniPasswordReset | None:
   """Get user from a specific reset record model by reset_token."""
   query = select(ResetModel).where(ResetModel.token == reset_token)
   result = session.execute(query)
   reset_record = result.scalars().one_or_none()
   return reset_record

def get_global_reset_record_by_token(reset_token: str, session: Session) -> AdminPasswordReset | AlumniPasswordReset | None:
   """Get reset record from either of the reset record models by reset_token."""

   # try to get reset record info from admin reset records
   reset_record = get_local_reset_record_by_token(reset_token, AdminPasswordReset, session)
   
   # try to get reset record info from alumni reset records
   if not reset_record:
      reset_record = get_local_reset_record_by_token(reset_token, AlumniPasswordReset, session)
   
   return reset_record

def expire_local_reset_records_by_user_id(user_id, ResetModel: AdminPasswordReset | AlumniPasswordReset, session: Session):
   query = (
      update(ResetModel)
      .where(and_(
         ResetModel.user_id == user_id,
         ResetModel.expired == False
      ))
      .values(**{ 'expired': True })
   )
   session.execute(query)
   session.commit()

def signin(response: Response, payload: AuthLoginInput, session: Session):
   """Handles the signin process with the provided authntication payload."""
   user = get_global_by_email(payload.email, session)
   
   # cut process if user was not found
   if not user:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Email or password must be incorrect.'
      )
   
   # cut if passwords don't match
   if not verify_password(payload.password, user.pass_hash):
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Email or password must be incorrect.'
      )
   
   # determine if the user is an admin or an alumni
   user_is_admin = Role.is_admin(user.role)
   UserAccountModel = AdminAccount if user_is_admin else AlumniAccount
   UserSessionModel = AdminSession if user_is_admin else AlumniSession
   
   # delete existing session id cookie
   response.delete_cookie('session_id')

   # create a new session
   user_session = create_local_session(user.id, UserSessionModel, payload.remember, session)

   # set a new session id cookie
   response.set_cookie(
      key = 'session_id',
      value = user_session.id,
      httponly = True,
      secure = False,
      samesite='lax',
      max_age = get_session_cookie_lifespan_seconds(payload.remember)
   )
   
   refreshed_user = session.get(UserAccountModel, user.id)
   
   return {
      'detail': 'Signed-in successfully.',
      'data': { 'user': exclude_fields(refreshed_user.model_dump()) }
   }

def forgot_password(payload: AuthForgotPassInput, session: Session):
   user = get_global_by_email(payload.email, session)
   
   # cut process if user was not found
   if not user:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Email or must be incorrect.'
      )

   # determine if the user is an admin or an alumni
   user_is_admin = Role.is_admin(user.role)
   UserResetModel = AdminPasswordReset if user_is_admin else AlumniPasswordReset
   
   # expire all the previous reset tokens
   expire_local_reset_records_by_user_id(user.id, UserResetModel, session)
   
   # create a reset record and get the token
   reset_record_token = add_local_reset_record(user.id, UserResetModel, session)
   
   # mail the reset link
   mail_reset_link(reset_record_token, payload.email)
   
   return { 'detail': 'A password reset link has been sent to your email address.' }

def reset_password(payload: AuthResetPassInput, session: Session):
   reset_record = get_global_reset_record_by_token(payload.reset_token, session)

   if not reset_record:
      raise HTTPException(
         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
         detail = 'Invalid reset token.'
      )
   
   # determine if reset record had expired
   if reset_record.expired or reset_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
      # set as expired first if not yet flagged as one
      if not reset_record.expired:
         reset_record.expired = True
         session.commit()
      
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Reset token has expired, please request for a new reset.'
      )
   
   # determine if the request is from an admin's account
   for_admin = isinstance(reset_record, AdminPasswordReset)
   AccountModel = AdminAccount if for_admin else AlumniAccount
   
   # get user's account
   user = get_local_by_id(reset_record.user_id, AccountModel, session)
   user.pass_hash = hash_password(payload.password)
   session.commit()
   
   return { 'detail': 'Your password has been reset successfully. You may now login using it.' }

def change_password(payload: AuthChangePassInput, user: dict, session: Session):
   """Changes the password of a user."""
   # check if current password matches the actual current password of the user
   if not verify_password(payload.current_password, user.get('pass_hash')):
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Incorrect password. Please try again.'
      )
   
   # update the password
   user = get_global_by_email(user.get('email'), session)
   user.pass_hash = hash_password(payload.new_password)
   session.commit()
   session.refresh(user)
   
   # add a change record
   for_admin = Role.is_admin(user.role)
   ChangeModel = AdminPasswordChange if for_admin else AlumniPasswordChange
   add_local_change_record(user.id, ChangeModel, session)
   
   return { 'detail': 'Your password has been changed successfully.' }

def signout(response: Response):
   response.delete_cookie('session_id')
   return { 'detail': 'Signed-out successfully.' }