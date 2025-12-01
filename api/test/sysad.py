from backend.enums.user import Role
from backend.services.sysad import *
from backend.database.config import get_session
from backend.utilities.authorization import allow_roles
from backend.services.user import add_admin, act_deact_admin_by_id
from backend.schemas.sysad import SysadAddAdminInput, SysadAddSchoolInput, SysadAddJobPostInput

from typing import Optional
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form

router = APIRouter(prefix='/sysad', tags=['Sysad'])

@router.get('/database/backup')
def route_database_backup(user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return database_backup()

@router.post('/admin')
def route_add_admin(payload: SysadAddAdminInput, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return add_admin(payload, user, session)

@router.patch('/admin/{admin_id}/activate')
def route_act_deact_admin_by_id(admin_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return act_deact_admin_by_id(admin_id, True, user, session)

@router.patch('/admin/{admin_id}/deactivate')
def route_act_deact_admin_by_id(admin_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return act_deact_admin_by_id(admin_id, False, user, session)

@router.get('/school')
def route_get_schools(archived: bool = False, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return get_schools(archived, page, page_size, session)

@router.post('/school')
def route_add_school(payload: SysadAddSchoolInput, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return add_school(payload, user, session)

@router.patch('/school/{school_id}/rename')
def route_rename_school(school_id: int, payload: SysadAddSchoolInput, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return rename_school_by_id(school_id, payload, user, session)

@router.patch('/school/{school_id}/archive')
def route_archive_school(school_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_school_by_id(school_id, True, user, session)

@router.patch('/school/{school_id}/restore')
def route_restore_school(school_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_school_by_id(school_id, False, user, session)

@router.get("/company", tags=['PESO'])
def route_get_companies(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), user: dict = Depends(allow_roles([Role.sysad, Role.peso])), session: Session = Depends(get_session)):
   return get_companies(page, page_size, session)

@router.post('/company')
def route_add_company(
   company_name: str = Form(...),
   companny_logo: Optional[UploadFile] = File(None),
   letter_of_intent: Optional[UploadFile] = File(None),
   companny_profile: Optional[UploadFile] = File(None),
   business_permit: Optional[UploadFile] = File(None),
   sec: Optional[UploadFile] = File(None),
   reg_of_est: Optional[UploadFile] = File(None),
   dole_certification: Optional[UploadFile] = File(None),
   dti_cda: Optional[UploadFile] = File(None),
   pending_case_certification: Optional[UploadFile] = File(None),
   philjobnet_registration: Optional[UploadFile] = File(None),
   user: dict = Depends(allow_roles([Role.sysad])),
   session: Session = Depends(get_session)
):
   return add_company(
      company_name,
      companny_logo,
      letter_of_intent,
      companny_profile,
      business_permit,
      sec,
      reg_of_est,
      dole_certification,
      dti_cda,
      pending_case_certification,
      philjobnet_registration,
      user,
      session
   )

@router.patch('/company/{company_id}/update-document')
def route_update_company_document(company_id: int, document_title: str = Form(...), document_file: Optional[UploadFile] = File(None), user: dict = Depends(allow_roles([Role.sysad, Role.peso])), session: Session = Depends(get_session)):
   return update_company_document(company_id, document_title, document_file, user, session)

@router.patch('/company/{company_id}/archive')
def route_archive_company(company_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_company_by_id(company_id, True, user, session)

@router.patch('/company/{company_id}/restore')
def route_restore_company(company_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_company_by_id(company_id, False, user, session)

@router.get('/job-post')
def route_get_job_posts(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), user: dict = Depends(allow_roles([Role.sysad, Role.peso])), session: Session = Depends(get_session)):
   return get_job_posts(page, page_size, session)

@router.post('/job-post')
def route_add_job_post(payload: SysadAddJobPostInput, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return add_job_post(payload, user, session)

@router.patch('/job-post/{job_post_id}/archive')
def route_archive_job_post(job_post_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_job_post_by_id(job_post_id, True, user, session)

@router.patch('/job-post/{job_post_id}/restore')
def route_restore_job_post(job_post_id: int, user: dict = Depends(allow_roles([Role.sysad])), session: Session = Depends(get_session)):
   return arc_res_job_post_by_id(job_post_id, False, user, session)