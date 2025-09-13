# backend/app/services/audit_log.py

from datetime import datetime
from app.models.audit import AuditLog
from sqlalchemy.orm import Session

def log_role_change(db: Session, admin_id: int, user_id: int, old_role: str, new_role: str):
    """
    Records a role change event in the audit log.
    Strategic Role:
    - Powers compliance, transparency, and enterprise governance.
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
    Strategic Role:
    - Powers behavioral analytics and governance transparency.
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

def log_login_event(db: Session, user_id: int):
    """
    Records a login event in the audit log.
    Strategic Role:
    - Powers security audits, usage analytics, and compliance tracking.
    """
    log = AuditLog(
        admin_id=None,
        user_id=user_id,
        action="login",
        old_value=None,
        new_value="success",
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

def log_permission_change(db: Session, admin_id: int, target_user_id: int, resource: str, old_permission: str, new_permission: str):
    """
    Records a permission change event in the audit log.
    Strategic Role:
    - Powers access governance, compliance, and security audits.
    """
    log = AuditLog(
        admin_id=admin_id,
        user_id=target_user_id,
        action="permission_change",
        old_value=f"{resource}: {old_permission}",
        new_value=f"{resource}: {new_permission}",
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
