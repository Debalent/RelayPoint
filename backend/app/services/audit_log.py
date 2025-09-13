# backend/app/services/audit_log.py

from datetime import datetime
from app.models.audit import AuditLog
from sqlalchemy.orm import Session

def log_role_change(db: Session, admin_id: int, user_id: int, old_role: str, new_role: str):
    """
    Records a role change event in the audit log.
    Captures who made the change, what was changed, and when.

    Strategic Role:
    - Powers compliance, transparency, and enterprise governance.
    - Scalable for multi-tenant orgs, permission audits, and behavioral tracking.
    - Extensible for UI surfacing, export tools, and investor dashboards.
    """
    log = AuditLog(
        admin_id=admin_id,
        user_id=user_id,
        action="role_change",
        old_value=old_role,
        new_value=new_role,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
