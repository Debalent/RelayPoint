# backend/app/api/v1/endpoints/status.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.workflow import Workflow
from app.models.step import Step
from app.schemas.step import StepStatus
from app.db import get_db

router = APIRouter(prefix="/workflows", tags=["status"])

@router.get("/{workflow_id}/status", response_model=StepStatus)
def get_workflow_status(workflow_id: str, db: Session = Depends(get_db)):
    """
    Returns the current status of all steps in a workflow.
    Enables real-time visibility for dashboards, analytics, and collaboration.

    Strategic Role:
    - Powers frontend status views and user feedback loops.
    - Scalable for role-based insights, notifications, and audit logging.
    - Extensible for time tracking, completion rates, and monetization metrics.
    """
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    steps = db.query(Step).filter(Step.workflow_id == workflow_id).order_by(Step.order).all()
    return {"steps": steps}
