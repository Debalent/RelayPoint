# backend/app/services/workflow_suggester.py

from sqlalchemy.orm import Session
from app.models.usage import UsageLog
from app.models.workflow import Workflow

def suggest_workflows_for_user(db: Session, user_id: int):
    """
    Suggests workflows based on user behavior.
    Strategic Role:
    - Powers smart onboarding, template recommendations, and upgrade nudges.
    - Scalable for role-based suggestions, tier awareness, and media sync.
    - Extensible for AI scoring, persona routing, and collaboration triggers.
    """
    # Step 1: Analyze user's past workflow usage
    usage = db.query(UsageLog).filter(UsageLog.user_id == user_id).all()
    actions = [log.action for log in usage]
    created = sum(1 for a in actions if a == "workflow_created")
    edited = sum(1 for a in actions if a == "workflow_edited")
    collaborated = sum(1 for a in actions if a == "collaboration")

    # Step 2: Determine user persona
    persona = "creator" if created >= 3 else "collaborator" if collaborated >= 3 else "observer"

    # Step 3: Suggest workflows based on persona
    suggestions = db.query(Workflow).filter(Workflow.tags.contains([persona])).limit(5).all()

    return [
        {
            "id": wf.id,
            "name": wf.name,
            "description": wf.description,
            "steps": wf.steps[:3],  # preview first few steps
        }
        for wf in suggestions
    ]
