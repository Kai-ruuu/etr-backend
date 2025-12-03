# library imports
from enum import Enum

class CompanyType(str, Enum):
   sole_proprietorship = "Sole Proprietorship"
   partnership = "Partnership"
   corporation = "Corporation"
   llc = "Limited Liability Company"
   cooperative = "Cooperative"
   non_profit = "Non-Profit"
   government = "Government-Owned"
   private = "Private Company"
   public = "Public Company"
   joint_venture = "Joint Venture"
   foreign = "Foreign Corporation"
   professional_corporation = "Professional Corporation"
   b_corp = "Benefit Corporation"

class CompanyWorkSetup(str, Enum):
   remote = 'remote'
   on_site = 'on_site'
   hybrid = 'hybrid'

class CompanyStatus(str, Enum):
   pending = 'pending',
   approved = 'approved'
   rejected = 'rejected'