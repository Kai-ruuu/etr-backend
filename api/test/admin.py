from backend.enums.user import Role
from backend.services.sysad import *
from backend.database.config import get_session
from backend.services.admin import get_audit_logs_by_admin_id
from backend.utilities.authorization import allow_roles

from sqlmodel import Session
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form, status

router = APIRouter(prefix='/admin', tags=['Admin'])

@router.get('/audit-logs')
def route_get_audit_logs(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), user: dict = Depends(allow_roles(Role.admin_roles())), session: Session = Depends(get_session)):
   return get_audit_logs_by_admin_id(user.get('id'), page, page_size, session)