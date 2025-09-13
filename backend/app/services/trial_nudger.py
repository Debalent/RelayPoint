# backend/app/services/trial_nudger.py

from sqlalchemy.orm import Session
from app.models.usage import UsageLog
from app.models.user import User

def check_upgrade_trigger(db: Session, user_id: int):
    """
    Detects if a Free-tier user has reached Pro-level behavior.
    Strategic Role:
    - Powers upgrade nudges and trial conversion prompts.
    - Scalable for tiered thresholds, persona segmentation, and upsell logic.
    - Extensible for UI badges, email triggers, and dashboard banners.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.tier != "free":
        return False

    usage = db.query(UsageLog).filter(UsageLog.user_id == user_id).all()
    workflow_count = sum(1 for log in usage if log.action == "workflow_created")
    collab_count = sum(1 for log in usage if log.action == "collaboration")

    # Thresholds for upgrade nudge
    if workflow_count >= 5 or collab_count >= 3:
        return True

    return False
