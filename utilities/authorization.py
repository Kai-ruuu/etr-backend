# app imports
from backend.utilities.environment import *
from backend.enums.user import Role
from backend.schemas.authentication import AuthLoginInput
from backend.database.config import get_session
from backend.utilities.session import verify_session

# library imports
from sqlmodel import Session
from fastapi import Cookie, Depends
from fastapi import HTTPException, status

def get_user(session_id: str | None = Cookie(None), session: Session = Depends(get_session)) -> dict:
   return verify_session(session_id, session)

def allow_roles(allowed_roles: list):
   def wrapper(user: dict = Depends(get_user)):
      user_role = user.get('role')
      
      # block resource access if unauthorized
      if not Role.is_valid(user_role) or user_role not in allowed_roles:
         raise HTTPException(
            detail = 'You are not authorized to access this resource.',
            status_code = status.HTTP_401_UNAUTHORIZED
         )
      
      return user
   
   return wrapper