# app imports
from backend.enums.sysad import *
from backend.utilities.date_time import utc_now

# library imports
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Relationship, Field

class SysadCompany(SQLModel, table=True):
   id: Optional[int]                  = Field(default=None, primary_key=True)
   name: str                          = Field(min_length=1, max_length=256)
   logo_filename: Optional[str]       = Field(default=None)
   letter_of_intent_filename: str     = Field(nullable=False) # Letter of intent
   company_profile_filename: str      = Field(nullable=False) # Company Profile
   business_permit_filename: str      = Field(nullable=False) # Business Permit
   sec_filename: str                  = Field(nullable=False) # Securities and Excahnge Commission
   dti_cda_filename: str              = Field(nullable=False) # Department of Trade and Industry
   reg_of_est_filename: str           = Field(nullable=False) # Registry of Establishment fr. DOLE
   dole_cert_filename: str                     = Field(nullable=False) # Certification from DOLE Provincial Office
   no_pending_case_cert_filename: str = Field(nullable=False) # Certification of No Pending Case
   philjob_reg_filename: str          = Field(nullable=False) # Phil-JobNet Reg.
   status: CompanyStatus              = Field(default=CompanyStatus.pending)
   archived: bool                     = Field(default=False)

   # timestamps
   created_at: datetime               = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime               = Field(default_factory=utc_now, nullable=False)

   # the id of the sysad who created the company
   sysad_creator_id: int              = Field(foreign_key='adminaccount.id')
   # the id of the peso user who validated the company
   peso_validator_id: Optional[int]   = Field(default=None, nullable=True, foreign_key='adminaccount.id')

   # relationship/s
   sysad_creator: 'AdminAccount'      = Relationship( # type: ignore
      back_populates='companies_created',
      sa_relationship_kwargs={'foreign_keys': '[SysadCompany.sysad_creator_id]'}
   )
   peso_validator: Optional['AdminAccount']     = Relationship( # type: ignore
      back_populates='companies_validated',
      sa_relationship_kwargs={'foreign_keys': '[SysadCompany.peso_validator_id]'}
   )
   jobs: list['SysadCompanyJob'] = Relationship(back_populates='company')

class SysadCompanyJob(SQLModel, table=True):
   id: Optional[int]             = Field(default=None, primary_key=True)
   company_id: int               = Field(foreign_key='sysadcompany.id')
   created_at: datetime          = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime          = Field(default_factory=utc_now, nullable=False)
   archived: bool                = Field(default=False)
   
   location: str                 = Field(nullable=False)
   title: str                    = Field(min_length=2, max_length=512)
   work_setup: CompanyWorkSetup  = Field(default=CompanyWorkSetup.on_site)
   description: str              = Field(nullable=False)
   qualifications: str           = Field(nullable=False)
   roles_and_res: str            = Field(nullable=False)
   application_steps: str        = Field(nullable=False)
   monthly_pay: bool             = Field(default=False)
   total_vacancies: int          = Field(default=1)

   # the id of the sysad who created the job
   sysad_creator_id: int         = Field(foreign_key='adminaccount.id')

   # relationship/s
   sysad_creator: 'AdminAccount' = Relationship(back_populates='jobs_created') # type: ignore
   company: 'SysadCompany'       = Relationship(back_populates='jobs')

class SysadSchool(SQLModel, table=True):
   id: Optional[int]           = Field(default=None, primary_key=True)
   name: str                   = Field(nullable=False, max_length=256)
   created_at: datetime        = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime        = Field(default_factory=utc_now, nullable=False)
   deans: list['AdminAccount'] = Relationship(back_populates='school') # type: ignore
   archived: bool              = Field(default=False)