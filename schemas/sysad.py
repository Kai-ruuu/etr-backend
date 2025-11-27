from backend.enums.user import Role
from backend.enums.sysad import CompanyWorkSetup

from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr

class SysadAddAdminInput(BaseModel):
   first_name: str            = Field(min_length=1, max_length=100)
   middle_name: Optional[str] = Field(None, max_length=100)
   last_name: str             = Field(min_length=1, max_length=100)
   email: EmailStr            = Field(min_length=5, max_length=256)
   school_id: Optional[int]   = Field(None)
   role: Literal[Role.peso, Role.dean] 

class SysadAddSchoolInput(BaseModel):
   name: str = Field(..., max_length=256)

class SysadAddJobPostInput(BaseModel):
   company_id: int  = Field(...)
   location: str    = Field(...)
   title: str       = Field(...)
   work_setup: Literal[CompanyWorkSetup.on_site, CompanyWorkSetup.hybrid, CompanyWorkSetup.remote]
   description: str = Field(...)
   qualifications: str = Field(...)
   roles_and_res: str = Field(...)
   application_steps: str = Field(...)
   monthly_pay: bool = Field(default=False)
   total_vacancies: int = Field(gt=0)