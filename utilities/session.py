# app imports
from datetime import timedelta
from backend.utilities.date_time import auth_login_utc_now_expires_at
from backend.models.admin import AdminSession, AdminAccount
from backend.models.alumni import AlumniSession, AlumniAccount

# library imports
from sqlmodel import Session, select
from datetime import datetime, timezone
from fastapi import HTTPException, status

def create_local_session(user_id: int, SessionModel: AdminSession | AlumniSession, remembered: bool, session: Session) -> AdminSession | AlumniSession:
   """Creates a session within a specific session model."""
   new_session = SessionModel(user_id = user_id, expires_at = auth_login_utc_now_expires_at(remembered))
   session.add(new_session)
   session.commit()
   session.refresh(new_session)
   return new_session

def get_local_session(session_id: str, SessionModel: AdminSession | AlumniSession, session: Session) -> AdminSession | AlumniSession:
   """Gets session from a specific session model."""
   query = select(SessionModel).where(SessionModel.id == session_id)
   result = session.execute(query)
   return result.scalars().one_or_none()

def verify_session(session_id: str, session: Session = None) -> dict:
   """Verifies the sessions existense and lifespan by session_id."""
   # immediately cut the process if session id wasn't found
   if not session_id:
      raise HTTPException(
         status_code = status.HTTP_401_UNAUTHORIZED,
         detail = 'You are unauthorized to access this resource.'
      )
   
   # get session from admin sessions
   AccountModel = AdminAccount
   SessionModel = AdminSession
   user_session = get_local_session(session_id, SessionModel, session)
   
   # get session from alumni sessions
   if not user_session:
      AccountModel = AlumniAccount
      SessionModel = AlumniSession
      user_session = get_local_session(session_id, SessionModel, session)
   
   # stop verification if no session was found
   if not user_session:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Invalid session token.'
      )
   
   # stop verification if the session has ended
   if user_session.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail = 'Your session has ended, please re-login to the system.'
      )
   
   # return the user that's associated with user_session
   return session.get(AccountModel, user_session.user_id).model_dump()