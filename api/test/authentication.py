from backend.database.config import get_session
from backend.utilities.authorization import get_user
from backend.utilities.authentication import signin, signout, forgot_password, reset_password, change_password
from backend.schemas.authentication import AuthLoginInput, AuthForgotPassInput, AuthResetPassInput, AuthChangePassInput

from sqlmodel import Session
from fastapi import APIRouter, Depends, Response

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/signin')
def route_signin(response: Response, payload: AuthLoginInput, session: Session = Depends(get_session)):
   return signin(response, payload, session)

@router.post('/signout')
def route_signout(response: Response, user: dict = Depends(get_user)):
   return signout(response)

@router.post('/forgot-password')
def route_forgot_password(payload: AuthForgotPassInput, session: Session = Depends(get_session)):
   return forgot_password(payload, session)

@router.patch('/reset-password')
def route_reset_password(payload: AuthResetPassInput, session: Session = Depends(get_session)):
   return reset_password(payload, session)

@router.patch('/change-password')
def router_change_password(payload: AuthChangePassInput, user: dict = Depends(get_user), session: Session = Depends(get_session)):
   return change_password(payload, user, session)