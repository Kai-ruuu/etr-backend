# library imports
from enum import Enum

class Role(str, Enum):
   sysad = 'sysad'
   peso = 'peso'
   dean = 'dean'
   alumni = 'alumni'
   
   @classmethod
   def is_valid(_class, role: str) -> bool:
      return role in _class._value2member_map_
   
   @classmethod
   def is_admin(_class, role: str) -> bool:
      if not _class.is_valid(role):
         return False
      
      return role in { _class.sysad, _class.dean, _class.peso }
   
   @classmethod
   def admin_roles(_class) -> list:
      return [ _class.sysad, _class.dean, _class.peso ]
   
   @classmethod
   def all_roles(_class) -> list:
      return [ _class.sysad, _class.dean, _class.peso, _class.alumni ]

   @classmethod
   def as_display(_class, role: str) -> str:
      if not _class.is_valid(role):
         return None
      
      role_display_map = {
         _class.sysad: 'System Administrator',
         _class.peso: 'PESO',
         _class.dean: 'Dean',
         _class.alumni: 'Alumni'
      }
      
      return role_display_map[role]