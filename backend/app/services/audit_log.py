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

def log_workflow_edit(db: Session, admin_id: int, workflow_id: int, field_changed: str, old_value: str, new_value: str):
    """
    Records a workflow edit event in the audit log.
    Captures what was changed, by whom, and when.

    Strategic Role:
    - Powers behavioral analytics and governance transparency.
    - Scalable for multi-tenant orgs, investor dashboards, and audit trails.
    - Extensible for step-level diffs, versioning, and rollback logic.
    """
    log = AuditLog(
        admin_id=admin_id,
        user_id=None,
        action="workflow_edit",
        old_value=f"{field_changed}: {old_value}",
        new_value=f"{field_changed}: {new_value}",
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
