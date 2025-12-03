# app imports
from backend.models.admin import *
from backend.models.sysad import *
from backend.utilities.app_setup import *
from backend.utilities.environment import *
from backend.utilities.storage import init_dirs
from backend.utilities.storage import storage_dir, dump_dir

# app routers
from backend.api.test import user as user_router
from backend.api.test import peso as peso_router
from backend.api.test import sysad as sysad_router
from backend.api.test import admin as admin_router
from backend.api.test import authentication as auth_router

# library imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# create exported sql dumps folder
init_dirs(
   dir = dump_dir,
   dirs = [
      'exported',
      'restored'
   ]
)

# create app storage folders
init_dirs(
   dir = storage_dir,
   dirs = [
      'avatar',
      'company_logo',
      'business_permit',
      'company_profile',
      'letter_of_intent',
      'dole_certification',
      'philjobnet_registration',
      'registry_of_establishment',
      'pending_case_certification',
      'securities_and_exchange_commission',
      'department_of_trade_and_industries',
   ]
)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
   CORSMiddleware,
   allow_headers=["*"],
   allow_methods=["*"],
   allow_origins=[envs("FRONT_END_URL")],
   allow_credentials=True,
)
app.mount('/files/company-logo', StaticFiles(directory=str(storage_dir / 'company_logo')))
app.mount('/files/business-permit', StaticFiles(directory=str(storage_dir / 'business_permit')))
app.mount('/files/company-profile', StaticFiles(directory=str(storage_dir / 'company_profile')))
app.mount('/files/letter-of-intent', StaticFiles(directory=str(storage_dir / 'letter_of_intent')))
app.mount('/files/dole-certification', StaticFiles(directory=str(storage_dir / 'dole_certification')))
app.mount('/files/philjobnet-registration', StaticFiles(directory=str(storage_dir / 'philjobnet_registration')))
app.mount('/files/registry-of-establishment', StaticFiles(directory=str(storage_dir / 'registry_of_establishment')))
app.mount('/files/pending-case-certification', StaticFiles(directory=str(storage_dir / 'pending_case_certification')))
app.mount('/files/securities-and-exchange-commission', StaticFiles(directory=str(storage_dir / 'securities_and_exchange_commission')))
app.mount('/files/department-of-trade-and-industries', StaticFiles(directory=str(storage_dir / 'department_of_trade_and_industries')))

@app.get('/')
def index():
   return 'Server is running...'

app.include_router(auth_router.router, prefix='/test')
app.include_router(user_router.router, prefix='/test')
app.include_router(peso_router.router, prefix='/test')
app.include_router(admin_router.router, prefix='/test')
app.include_router(sysad_router.router, prefix='/test')