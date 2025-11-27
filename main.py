# app imports
from backend.models.admin import *
from backend.models.sysad import *
from backend.utilities.app_setup import *
from backend.utilities.environment import *
from backend.utilities.storage import init_dirs

# app routers
from backend.api.test import user as user_router
from backend.api.test import peso as peso_router
from backend.api.test import sysad as sysad_router
from backend.api.test import admin as admin_router
from backend.api.test import authentication as auth_router

# library imports
from fastapi import FastAPI
from os.path import join as join_path
from fastapi.middleware.cors import CORSMiddleware

init_dirs([
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
])


app = FastAPI(lifespan=lifespan)
app.add_middleware(
   CORSMiddleware,
   allow_headers=["*"],
   allow_methods=["*"],
   allow_origins=['http://localhost:5173'],
   allow_credentials=True,
)

@app.get('/')
def index():
   return 'Server is running...'

app.include_router(auth_router.router, prefix='/test')
app.include_router(user_router.router, prefix='/test')
app.include_router(peso_router.router, prefix='/test')
app.include_router(admin_router.router, prefix='/test')
app.include_router(sysad_router.router, prefix='/test')