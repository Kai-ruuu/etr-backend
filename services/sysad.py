from backend.utilities.storage import dump_dir
from backend.utilities.environment import envs
from backend.services.admin import add_audit_log
from backend.schemas.sysad import SysadAddSchoolInput, SysadAddJobPostInput
from backend.models.sysad import SysadSchool, SysadCompany, SysadCompanyJob
from backend.utilities.storage import files_saved_if_all_allowed_and_required, file_update_from_dir

import subprocess
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, update
from fastapi import HTTPException, UploadFile, File, Form, status

def database_backup():
   backup_filename = dump_dir / 'exported' / f'exported_{datetime.now().strftime("%m-%d-%Y_%I-%M_%p")}.sql'
   command = [
      'mysqldump',
      '-h', envs('DB_HOST'),
      '-u', envs('DB_USER'),
      f"--password={envs('DB_PASS')}",
      envs('DB_NAME')
   ]
   
   try:
      with open(backup_filename, 'w', encoding='utf-8') as file:
         subprocess.run(
            command,
            stdout = file,
            stderr = subprocess.PIPE,
            check = True
         )
         
      return { 'detail': 'Backup success.' }
   except subprocess.CalledProcessError as e:
      raise HTTPException(500, f"Backup failed.")

def get_school_by_name(school_name: str, session: Session) -> SysadSchool | None:
   query = select(SysadSchool).where(SysadSchool.name == school_name)
   result = session.execute(query)
   school = result.scalars().one_or_none()
   return school

def get_school_by_id(school_id: str, session: Session) -> SysadSchool | None:
   return session.get(SysadSchool, school_id)

def get_schools(archived: bool, page: int, page_size: int, session: Session):
   offset = (page - 1) * page_size
   total = len(session.execute(select(SysadSchool).where(SysadSchool.archived == archived)).scalars().all())
   statement = select(SysadSchool).where(SysadSchool.archived == archived).offset(offset).limit(page_size)
   schools = session.execute(statement).scalars().all()
   total_pages = (total + page_size - 1) // page_size
   return {
      'detail': 'Fetched schools.',
      'data': {
         "page": page,
         "page_size": page_size,
         "total": total,
         "total_pages": total_pages,
         "schools": schools
      }
   }

def add_school(payload: SysadAddSchoolInput, sysad: dict, session: Session):
   # check if the school already exists, raise if yes
   existing_school = get_school_by_name(payload.name, session)
   if existing_school:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'School already exists.'
      )
      
   # create audit log
   add_audit_log(sysad.get('id'), f'Added a new school "{payload.name}".', session)
   
   # add school if not
   new_school = SysadSchool(name = payload.name)
   session.add(new_school)
   session.commit()
   session.refresh(new_school)

   return {
      'detail': 'School has been added.',
      'data': { 'school': new_school }
   }

def rename_school_by_id(school_id: int, payload: SysadAddSchoolInput, sysad: dict, session: Session):
   # check if the new school's name is the same as any other school, raise if yes
   school_query = select(SysadSchool).where(SysadSchool.name == payload.name)
   school_query_result = session.execute(school_query)
   existing_school_by_name = school_query_result.scalars().one_or_none()
   if existing_school_by_name:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'A school with the same name already exists.'
      )
   
   # check if the school already exists, raise if yes
   existing_school = get_school_by_id(school_id, session)
   if not existing_school:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Invalid school id.'
      )
      
   # create audit log
   add_audit_log(sysad.get('id'), f'Renamed a school "{existing_school.name}" to "{payload.name}".', session)
   
   existing_school.name = payload.name
   session.commit()
   session.refresh(existing_school)
   return {
      'detail': 'School has been renamed.',
      'data': { 'school': existing_school }
   }

def arc_res_school_by_id(school_id: int, archived: bool, sysad: dict, session: Session):
   """Archives or restores a school."""
   # check if the school already exists, raise if yes
   existing_school = get_school_by_id(school_id, session)
   if not existing_school:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Invalid school id.'
      )
   
   # create audit log
   add_audit_log(sysad.get('id'), f'{"Archived" if archived else "Restored"} a school "{existing_school.name}".', session)
   
   existing_school.archived = archived
   session.commit()
   session.refresh(existing_school)
   return {
      'detail': f'School has been {"archived" if archived else "Restored"}.',
      'data': { 'school': existing_school }
   }

def get_companies(page: int, page_size: int, session: Session):
   offset = (page - 1) * page_size
   total = len(session.execute(select(SysadCompany)).scalars().all())
   statement = select(SysadCompany).offset(offset).limit(page_size)
   companies = session.execute(statement).scalars().all()
   total_pages = (total + page_size - 1) // page_size
   return {
      'detail': 'Fetched companies.',
      'data': {
         "page": page,
         "page_size": page_size,
         "total": total,
         "total_pages": total_pages,
         "companies": companies
      }
   }

def get_company_by_id(company_id: int, session: Session) -> SysadCompany | None:
   return session.get(SysadCompany, company_id)

def get_company_by_name(company_name: str, session: Session) -> SysadCompany | None:
   query = select(SysadCompany).where(SysadCompany.name == company_name)
   result = session.execute(query)
   company = result.scalars().one_or_none()
   return company

def add_company(
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
   sysad: dict = None,
   session: Session = None
):
   existing_company = get_company_by_name(company_name, session)
   if existing_company:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Company already exists.'
      )
   
   file_names = files_saved_if_all_allowed_and_required(
      files = [
         (
            'company_logo',
            'Company Logo',
            companny_logo,
            False,
            ['.png', '.jpg', '.jpeg']
         ),
         (
            'letter_of_intent',
            'Letter of Intent',
            letter_of_intent,
            True,
            ['.pdf']),
         (
            'company_profile',
            'Company Profile',
            companny_profile,
            True,
            ['.pdf']),
         (
            'business_permit',
            'Business Permit',
            business_permit,
            True,
            ['.pdf']),
         (
            'securities_and_exchange_commission',
            'Securities and Excahnge Commission',
            sec,
            True,
            ['.pdf']),
         (
            'department_of_trade_and_industries',
            'DTI/CDA Registration',
            dti_cda,
            True,
            ['.pdf']),
         (
            'registry_of_establishment',
            'Registration of Establishment',
            reg_of_est,
            True,
            ['.pdf']),
         (
            'dole_certification',
            'DOLE Provincial Office Certification',
            dole_certification,
            True,
            ['.pdf']),
         (
            'pending_case_certification',
            'Certification of No Pending Case',
            pending_case_certification,
            True,
            ['.pdf']),
         (
            'philjobnet_registration',
            'Phil-JobNet Registration',
            philjobnet_registration,
            True,
            ['.pdf'])
      ]
   )
   
   add_audit_log(sysad.get('id'), f'Added a company "{company_name}".', session)
   
   new_company = SysadCompany(
      name = company_name,
      logo_filename = file_names[0],
      letter_of_intent_filename = file_names[1],
      company_profile_filename = file_names[2],
      business_permit_filename = file_names[3],
      sec_filename = file_names[4],
      dti_cda_filename = file_names[5],
      reg_of_est_filename = file_names[6],
      dole_cert_filename = file_names[7],
      no_pending_case_cert_filename = file_names[8],
      philjob_reg_filename = file_names[9],
      sysad_creator_id = sysad.get('id')
   )
   session.add(new_company)
   session.commit()
   session.refresh(new_company)

   return {
      'detail': 'Company has been added',
      'data': { 'company': new_company }
   }

def update_company_document(company_id: int, document_title: str = Form(...), document_file: Optional[UploadFile] = File(None), sysad: dict = None, session: Session = None) -> SysadCompany:
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

   existing_company_dict = existing_company.model_dump()
   
   document_title_specs = {
      'company_logo': ['logo_filename', ['.png', '.jpg', '.jpeg']],
      'business_permit': ['business_permit_filename', ['.pdf']],
      'company_profile': ['company_profile_filename', ['.pdf']],
      'letter_of_intent': ['letter_of_intent_filename', ['.pdf']],
      'dole_certification': ['dole_cert_filename', ['.pdf']],
      'philjobnet_registration': ['philjob_reg_filename', ['.pdf']],
      'registry_of_establishment': ['reg_of_est_filename', ['.pdf']],
      'pending_case_certification': ['no_pending_case_cert_filename', ['.pdf']],
      'securities_and_exchange_commission': ['sec_filename', ['.pdf']],
      'department_of_trade_and_industries': ['dti_cda_filename', ['.pdf']],
   }

   if document_title not in document_title_specs.keys():
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Invalid document title.'
      )
   
   document_model_attribute = document_title_specs[document_title][0]
   document_allowed_extensions = document_title_specs[document_title][1]
   old_filename = existing_company_dict[document_model_attribute]

   # update file
   new_filename = file_update_from_dir(document_title, old_filename, document_file, document_allowed_extensions)

   add_audit_log(sysad.get('id'), f'Updated a company document "{existing_company.name}".', session)

   # update record's filname
   query = update(SysadCompany).where(SysadCompany.id == company_id).values(**{ document_model_attribute: new_filename })
   session.execute(query)
   session.commit()
   session.refresh(existing_company)
   return {
      'detail': 'Document has been updated',
      'data': { 'company': existing_company }
   }

def arc_res_company_by_id(company_id: int, archived: bool, sysad: dict, session: Session):
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

   add_audit_log(sysad.get('id'), f'{"archived" if archived else "restored"} a company "{existing_company.name}".', session)

   existing_company.archived = archived
   session.commit()
   session.refresh(existing_company)
   return {
      'detail': f'Company has been {"archived" if archived else "restored"}.',
      'data': { 'company': existing_company }
   }

def get_job_post_by_title(job_post_title: str, session: Session) -> SysadCompanyJob | None:
   query = select(SysadCompanyJob).where(SysadCompanyJob.title == job_post_title).options(selectinload(SysadCompanyJob.company))
   result = session.execute(query)
   job_post = result.scalars().one_or_none()
   return job_post

def get_job_posts(page: int, page_size: int, session: Session):
   offset = (page - 1) * page_size
   total = len(session.execute(select(SysadCompanyJob)).scalars().all())
   statement = select(SysadCompanyJob).offset(offset).limit(page_size)
   job_posts = session.execute(statement).scalars().all()
   total_pages = (total + page_size - 1) // page_size
   return {
      'detail': 'Fetched job_posts.',
      'data': {
         "page": page,
         "page_size": page_size,
         "total": total,
         "total_pages": total_pages,
         "job_posts": job_posts
      }
   }

def get_job_post_by_id(job_post_id: int, session: Session) -> SysadCompanyJob | None:
   return session.get(SysadCompanyJob, job_post_id)

def add_job_post(payload: SysadAddJobPostInput, sysad: dict, session: Session):
   existing_job_post = get_job_post_by_title(payload.title, session)
   if existing_job_post and existing_job_post.company.id == payload.company_id:
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = 'Job post already exists on the company.'
      )
   
   add_audit_log(sysad.get('id'), f'Posted a new job "{payload.title}".', session)
   
   new_job_post_input = payload.model_dump()
   new_job_post_input['sysad_creator_id'] = sysad.get('id')
   new_job_post = SysadCompanyJob(**new_job_post_input)
   session.add(new_job_post)
   session.commit()
   session.refresh(new_job_post)
   return {
      'detail': 'Job has been posted.',
      'data': { 'job_post': new_job_post }
   }

def arc_res_job_post_by_id(job_post_id: int, archived: bool, sysad: dict, session: Session):
   if not job_post_id:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Missing job post id.'
      )
   
   existing_job_post = get_job_post_by_id(job_post_id, session)
   if not existing_job_post:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Job post not found.'
      )

   add_audit_log(sysad.get('id'), f'{"archived" if archived else "restored"} a job post "{existing_job_post.title}".', session)

   existing_job_post.archived = archived
   session.commit()
   session.refresh(existing_job_post)
   return {
      'detail': f'Job post has been {"archived" if archived else "restored"}.',
      'data': { 'job_post': existing_job_post }
   }
