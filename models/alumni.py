from backend.enums.user import Role
from backend.utilities.date_time import utc_now

from uuid import uuid4
from typing import Optional
from pydantic import EmailStr
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class AlumniAccount(SQLModel, table=True):
   id: Optional[int]                             = Field(default=None, primary_key=True)
   first_name: str                               = Field(min_length=1, max_length=100)
   middle_name: Optional[str]                    = Field(default=None, max_length=100)
   last_name: str                                = Field(min_length=1, max_length=100)
   role: Role                                    = Field(default=Role.alumni)
   email: EmailStr                               = Field(min_length=5, max_length=256)
   pass_hash: str                                = Field(max_length=256)
   avatar_filename: Optional[str]                = Field(default=None)
   created_at: datetime                          = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime                          = Field(default_factory=utc_now, nullable=False)

   # for all accounts for determining if their accounts are activated or not
   activated: bool                               = Field(default=True)

   # relationship/s
   sessions: list['AlumniSession']                = Relationship(back_populates='user')
   password_resets: list['AlumniPasswordReset']   = Relationship(back_populates='user')
   password_changes: list['AlumniPasswordChange'] = Relationship(back_populates='user')

class AlumniSession(SQLModel, table=True):
   id: str              = Field(default_factory=lambda: str(uuid4()), primary_key=True)
   user_id: int         = Field(foreign_key='alumniaccount.id')
   created_at: datetime = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime = Field(default_factory=utc_now, nullable=False)
   expires_at: datetime = Field(nullable=False)

   # relationships
   user: 'AlumniAccount' = Relationship(back_populates='sessions')

class AlumniPasswordReset(SQLModel, table=True):
   id: Optional[int]       = Field(default=None, primary_key=True)
   token: str              = Field(nullable=False)
   user_id: int            = Field(foreign_key='alumniaccount.id')
   created_at: datetime    = Field(default_factory=utc_now, nullable=False)
   updated_at: datetime    = Field(default_factory=utc_now, nullable=False)
   expires_at: datetime    = Field(nullable=False)
   expired: bool           = Field(default=False)

   # relationship/s
   user: 'AlumniAccount'  = Relationship(back_populates='password_resets')

class AlumniPasswordChange(SQLModel, table=True):
   id: Optional[int]       = Field(default=None, primary_key=True)
   created_at: datetime    = Field(default_factory=utc_now, nullable=False)
   user_id: int           = Field(foreign_key='alumniaccount.id')

   # relationship/s
   user: 'AlumniAccount'  = Relationship(back_populates='password_changes')