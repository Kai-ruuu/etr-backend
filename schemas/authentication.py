from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class AuthLoginInput(BaseModel):
   email: EmailStr = Field(..., min_length=5, max_length=256)
   password: str   = Field(..., min_length=6, max_length=64)
   remember: bool  = Field(False)

class AuthForgotPassInput(BaseModel):
   email: EmailStr = Field(..., min_length=5, max_length=256)

class AuthResetPassInput(BaseModel):
   password: str    = Field(..., min_length=6, max_length=64)
   reset_token: str = Field(...)

class AuthChangePassInput(BaseModel):
   current_password: str = Field(..., min_length=6, max_length=64)
   new_password: str     = Field(..., min_length=6, max_length=64)