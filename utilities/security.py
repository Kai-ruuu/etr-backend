import string
import secrets
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['argon2'], deprecated='auto')

def hash_password(password: str) -> str:
   return crypt_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
   return crypt_context.verify(password, hashed_password)

def generate_password(length: int = 6) -> str:
   chars = string.ascii_letters + string.digits
   password = ''.join(secrets.choice(chars) for i in range(length))
   return password

def exclude_fields(model_dict: dict, excluded_fields: list = ['pass_hash']) -> dict:
   for field in excluded_fields:
      if field in model_dict.keys():
         model_dict.pop(field)
   
   return model_dict