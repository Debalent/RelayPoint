# backend/app/api/v1/endpoints/export_template.py

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.workflow import Workflow
import json

router = APIRouter(prefix="/admin", tags=["modular-export"])

@router.get("/workflow/{workflow_id}/export")
def export_workflow_template(workflow_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Exports a workflow as a reusable JSON template.
    Strategic Role:
    - Powers modular reuse, onboarding acceleration, and team scaling.
    - Scalable for branded templates, tiered access, and investor demos.
    - Extensible for export presets, template libraries, and sharing logic.
    """
    if not current_user.is_admin:
        return Response(status_code=403)

    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        return Response(status_code=404)

    template = {
        "name": workflow.name,
        "steps": workflow.steps,
        "roles": workflow.roles,
        "metadata": workflow.metadata,
    }

    return Response(content=json.dumps(template, indent=2), media_type="application/json")
