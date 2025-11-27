from backend.enums.user import Role
from backend.models.admin import AdminAccount
from backend.models.alumni import AlumniAccount
from backend.services.admin import add_audit_log
from backend.schemas.sysad import SysadAddAdminInput
from backend.utilities.mailing import mail_admin_welcome
from backend.utilities.security import generate_password, hash_password, exclude_fields

from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException, status

def get_local_by_id(id: int, AccountModel: AdminAccount | AlumniAccount, session: Session) -> AdminAccount | AlumniAccount | None:
   """Get user from either of the account models."""
   return session.get(AccountModel, id)

def get_local_by_email(email: EmailStr, AccountModel: AdminAccount | AlumniAccount, session: Session) -> AdminAccount | AlumniAccount | None:
   """Get user from a specific account model."""
   query = select(AccountModel).where(AccountModel.email == email)
   result = session.execute(query)
   return result.scalars().one_or_none()

def get_global_by_email(email: EmailStr, session: Session) -> AdminAccount | AlumniAccount | None:
   """Get user from either of the account models."""
   # try to get account info from admin accounts
   account = get_local_by_email(email, AdminAccount, session)
   
   # try to get account info from alumni accounts
   if not account:
      account = get_local_by_email(email, AlumniAccount, session)
   
   return account

def add_admin(payload: SysadAddAdminInput, sysad: dict, session: Session):
   """Creates an admin account if it doesn't exist yet, otherwise, raises an exception."""
   existing_admin = get_local_by_email(payload.email, AdminAccount, session)

   # cut process if admin exists already
   if existing_admin:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Admin already exists.'
      )
   
   # generate password for the new admin
   new_admin_password = generate_password()
   payload_dict = payload.model_dump()
   payload_dict['pass_hash'] = hash_password(new_admin_password)
   
   # create audit log
   add_audit_log(sysad.get('id'), f'Assigned {payload.email} as a new {Role.as_display(payload.role)}.', session)
   
   # create the new admin
   new_admin = AdminAccount(**payload_dict)
   session.add(new_admin)
   session.commit()
   session.refresh(new_admin)
   
   # mail the new admin
   mail_admin_welcome(new_admin.model_dump(), new_admin_password, sysad.get('email'))
   
   # return the newly created admin and exlude the password hash
   return {
      'detail': 'Admin account has been created.',
      'data': { 'user': exclude_fields(new_admin.model_dump()) }
   }

def act_deact_admin_by_id(admin_id, activated: bool, sysad: dict, session: Session):
   """Activates or deactivates an admin's account."""
   existing_admin = get_local_by_id(admin_id, AdminAccount, session)

   # cut process if admin was not found
   if not existing_admin:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Admin account not found.'
      )
   
   # create audit log
   add_audit_log(sysad.get('id'), f'{"Activated" if existing_admin.activated else "Deactivated"} {existing_admin.email}.', session)
   
   # activate or deactivate and return the admin
   existing_admin.activated = activated
   session.commit()
   session.refresh(existing_admin)
   return {
      'detail': f'Admin account has been {"activated" if existing_admin.activated else "deactivated"}.',
      'data': { 'user': exclude_fields(existing_admin.model_dump()) }
   }