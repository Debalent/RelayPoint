# backend/app/services/usage_tracker.py

from datetime import datetime
from app.models.usage import UsageLog
from sqlalchemy.orm import Session

def log_workflow_created(db: Session, user_id: int, workflow_id: int):
    """
    Logs when a user creates a workflow.
    Strategic Role:
    - Powers usage-based billing, tier nudges, and adoption analytics.
    """
    log = UsageLog(
        user_id=user_id,
        action="workflow_created",
        resource_id=workflow_id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

def log_workflow_edited(db: Session, user_id: int, workflow_id: int):
    """
    Logs when a user edits a workflow.
    Strategic Role:
    - Powers engagement metrics and iteration velocity tracking.
    """
    log = UsageLog(
        user_id=user_id,
        action="workflow_edited",
        resource_id=workflow_id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

def log_collaboration_event(db: Session, user_id: int, workflow_id: int, collaborator_id: int):
    """
    Logs when a user collaborates with another user on a workflow.
    Strategic Role:
    - Powers team analytics, upgrade triggers, and network effects.
    """
    log = UsageLog(
        user_id=user_id,
        action="collaboration",
        resource_id=workflow_id,
        metadata=f"collaborator:{collaborator_id}",
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
