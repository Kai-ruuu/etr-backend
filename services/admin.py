from backend.models.admin import AdminAuditLog

from pydantic import EmailStr
from sqlmodel import Session, select, desc
from fastapi import HTTPException, status, Query

def get_audit_logs_by_admin_id(admin_id: int, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), session: Session = None):
   offset = (page - 1) * page_size
   total = len(session.execute(select(AdminAuditLog).where(AdminAuditLog.user_id == admin_id)).scalars().all())
   statement = select(AdminAuditLog).where(AdminAuditLog.user_id == admin_id).offset(offset).limit(page_size).order_by(desc(AdminAuditLog.created_at))
   audit_logs = session.execute(statement).scalars().all()
   total_pages = (total + page_size - 1) // page_size
   return {
      'detail': 'Fetched audit logs.',
      'data': {
         "page": page,
         "page_size": page_size,
         "total": total,
         "total_pages": total_pages,
         "audit_logs": audit_logs
      }
   }

def add_audit_log(user_id: int, action: str, session: Session):
   new_audit_log = AdminAuditLog(user_id = user_id, action = action)
   session.add(new_audit_log)
   session.commit()
   session.refresh(new_audit_log)
   return new_audit_log