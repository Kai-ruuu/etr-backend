# app imports
from backend.utilities.environment import *

# library imports
from sqlmodel import Session, SQLModel, create_engine

DB_URL = f'mysql+pymysql://{envs("DB_USER")}:{envs("DB_PASS")}@{envs("DB_HOST")}/{envs("DB_NAME")}'
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)

def initialize_database():
   SQLModel.metadata.create_all(engine)
   print('[DATABASE] Initialized.')

def get_session():
   with Session(engine) as session:
      yield session

