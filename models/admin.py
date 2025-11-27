# app imports
from backend.enums.user import Role
from backend.utilities.date_time import utc_now

# library imports
from uuid import uuid4
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Relationship, Field

class AdminAccount(SQLModel, table=True):
   id: Optional[int]                             = Field(default=None, primary_key=True)
   first_name: str                               = Field(min_length=1, max_length=100)
   middle_name: Optional[str]                    = Field(default=None, max_length=100)
   last_name: str                                = Field(min_length=1, max_length=100)
   role: Role                                    = Field(default=Role.dean)
   email: EmailStr                               = Field(min_length=5, max_length=256)
   pass_hash: str                                = Field(max_length=256)
   avatar_filename: Optional[str]                = Field(default=None)
   created_at: datetime                          = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime                          = Field(default_factory=utc_now, nullable=False)

   # for all accounts for determining if their accounts are activated or not
   activated: bool                               = Field(default=True)

   # for dean accounts only for determining which school do they belong
   school_id: Optional[int]                      = Field(foreign_key='sysadschool.id')
   school: Optional['SysadSchool']               = Relationship(back_populates='deans') # type: ignore

   # for sysad accounts only for getting the companies that are created by a specific sysad
   companies_created: list['SysadCompany']       = Relationship( # type: ignore
      back_populates = 'sysad_creator',
      sa_relationship_kwargs = {'foreign_keys': '[SysadCompany.sysad_creator_id]'}
   )

   # for sysad accounts only for getting the jobs that are created by a specific sysad
   companies_validated: list['SysadCompany']     = Relationship( # type: ignore
      back_populates = 'peso_validator',
      sa_relationship_kwargs = {'foreign_keys': '[SysadCompany.peso_validator_id]'}
   )

   # for peso accounts only for getting the companies that are created by a specific peso
   jobs_created: list['SysadCompanyJob']         = Relationship( # type: ignore
      back_populates = 'sysad_creator',
      sa_relationship_kwargs = {'foreign_keys': '[SysadCompanyJob.sysad_creator_id]'}
   )

   # relationship/s
   sessions: list['AdminSession']                = Relationship(back_populates='user')
   password_resets: list['AdminPasswordReset']   = Relationship(back_populates='user')
   password_changes: list['AdminPasswordChange'] = Relationship(back_populates='user')
   audit_logs: list['AdminAuditLog']             = Relationship(back_populates='user')

class AdminSession(SQLModel, table=True):
   id: str              = Field(default_factory=lambda: str(uuid4()), primary_key=True)
   user_id: int         = Field(foreign_key='adminaccount.id')
   created_at: datetime = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime = Field(default_factory=utc_now, nullable=False)
   expires_at: datetime = Field(nullable=False)

   # relationships
   user: 'AdminAccount' = Relationship(back_populates='sessions')

class AdminPasswordReset(SQLModel, table=True):
   id: Optional[int]    = Field(default=None, primary_key=True)
   token: str           = Field(nullable=False)
   user_id: int         = Field(foreign_key='adminaccount.id')
   created_at: datetime = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime = Field(default_factory=utc_now, nullable=False)
   expires_at: datetime = Field(nullable=False)
   expired: bool        = Field(default=False)

   # relationship/s
   user: 'AdminAccount'  = Relationship(back_populates='password_resets')

class AdminPasswordChange(SQLModel, table=True):
   id: Optional[int]    = Field(default=None, primary_key=True)
   created_at: datetime = Field(default_factory=utc_now, nullable=False)
   user_id: int         = Field(foreign_key='adminaccount.id')

   # relationship/s
   user: 'AdminAccount' = Relationship(back_populates='password_changes')

class AdminAuditLog(SQLModel, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   created_at: datetime = Field(default_factory=utc_now, nullable=False)
   
   action: str       = Field(nullable=False)
   user_id: int      = Field(foreign_key='adminaccount.id')
   user: 'AdminAccount' = Relationship(back_populates='audit_logs')