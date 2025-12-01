from backend.enums.user import Role
from backend.database.config import get_session
from backend.services.sysad import get_companies
from backend.services.peso import verify_company_by_id
from backend.utilities.authorization import allow_roles
from backend.services.user import add_admin, act_deact_admin_by_id
from backend.schemas.sysad import SysadAddAdminInput, SysadAddSchoolInput

from typing import Optional
from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix='/peso', tags=['PESO'])

@router.patch('/company/{company_id}/verify')
def route_verify_company(company_id: int, user: dict = Depends(allow_roles([Role.peso])), session: Session = Depends(get_session)):
   return verify_company_by_id(company_id, user, session)