from backend.enums.user import Role
from backend.database.config import get_session
from backend.schemas.sysad import SysadAddAdminInput
from backend.utilities.security import exclude_fields
from backend.utilities.authorization import allow_roles
from backend.services.user import add_admin, act_deact_admin_by_id

from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix='/user', tags=['User'])

@router.get('/')
def route_get_user(user: dict = Depends(allow_roles(Role.all_roles()))):
   return {
      'detail': 'Fetched user info.',
      'data': { 'user': exclude_fields(user) }
   }