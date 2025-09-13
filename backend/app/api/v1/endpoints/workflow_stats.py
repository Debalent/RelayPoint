# backend/app/api/v1/endpoints/workflow_stats.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.workflow import Workflow

router = APIRouter(prefix="/admin", tags=["analytics"])

@router.get("/workflow-stats")
def get_workflow_stats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Returns key workflow analytics for admin dashboard.
    Includes total workflows, completion rate, and active project count.

    Strategic Role:
    - Powers admin visibility into platform usage and team performance.
    - Scalable for multi-tenant orgs, tiered access, and monetization tracking.
    - Extensible for time-based filters, persona segmentation, and audit logs.
    """
    total = db.query(Workflow).count()
    completed = db.query(Workflow).filter(Workflow.is_complete == True).count()
    active = db.query(Workflow).filter(Workflow.is_complete == False).count()

    completion_rate = round((completed / total) * 100, 2) if total > 0 else 0

    return {
        "total": total,
        "completion_rate": completion_rate,
        "active_projects": active
    }
