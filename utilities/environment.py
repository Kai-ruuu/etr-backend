from os import getenv
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'

load_dotenv(dotenv_path=env_path)

def envs(key: str) -> str:
   return getenv(key)

def envi(key: str) -> int:
   int_val = int(getenv(key))
   return int_val

def envf(key: str) -> float:
   float_val = float(getenv(key))
   return float_val

def envb(key: str, true_vals=[]) -> bool:
   return getenv(key) in true_vals