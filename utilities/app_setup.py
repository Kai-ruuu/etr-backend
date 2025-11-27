# app imports
from backend.enums.user import Role
from backend.database.config import engine
from backend.models.admin import AdminAccount
from backend.utilities.environment import envs
from backend.services.user import get_local_by_email
from backend.utilities.security import hash_password
from backend.database.config import initialize_database
from backend.models.admin import AdminAccount

# library imports
from fastapi import FastAPI
from sqlmodel import Session
from contextlib import asynccontextmanager

def bootstrap_sysad_account():
   with Session(engine) as session:
      email = envs('SYSTEM_ADMIN_EMAIL')
      password = hash_password(envs('SYSTEM_ADMIN_PASSWORD'))
      existing_sysad = get_local_by_email(email, AdminAccount, session)

      if existing_sysad:
         print('[SYSTEM] Skipped System Admin account creation. (already exists)')
      else:
         new_sysad = AdminAccount(
            first_name = "System",
            last_name = "Administrator",
            role = Role.sysad,
            email = email,
            pass_hash = password,
         )
         session.add(new_sysad)
         session.commit()
         print('[SYSTEM] System Admin account created.')

@asynccontextmanager
async def lifespan(app: FastAPI):
   initialize_database()
   bootstrap_sysad_account()
   yield