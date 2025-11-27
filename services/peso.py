from backend.models.sysad import SysadCompany
from backend.services.admin import add_audit_log
from backend.services.sysad import get_company_by_id
from backend.schemas.sysad import SysadAddSchoolInput
from backend.utilities.mailing import mail_admin_welcome

from sqlmodel import Session, select
from fastapi import HTTPException, status

def verify_company_by_id(company_id: int, peso: dict, session: Session):
   if not company_id:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Missing company id.'
      )
   
   existing_company = get_company_by_id(company_id, session)
   if not existing_company:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Company not found.'
      )
   
   add_audit_log(peso.get('id'), f'Verified a company "{existing_company.name}".', session)
   
   existing_company.validated = True
   existing_company.peso_validator_id = peso.get('id')
   session.commit()
   session.refresh(existing_company)
   return existing_company