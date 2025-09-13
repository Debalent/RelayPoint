# backend/app/api/v1/endpoints/snapshot_export.py

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.audit import AuditLog
from app.models.usage import UsageLog
import csv
import io

router = APIRouter(prefix="/admin", tags=["investor-export"])

@router.get("/snapshot/export")
def export_investor_snapshot(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Exports governance, usage, and monetization metrics as CSV.
    Strategic Role:
    - Powers investor decks, due diligence, and operational transparency.
    - Scalable for org-level segmentation and tier analytics.
    - Extensible for churn risk, upgrade velocity, and behavioral scoring.
    """
    if not current_user.is_admin:
        return Response(status_code=403)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "Full Name", "Tier", "Role", "Total Logins", "Workflows Created", "Permission Changes"])

    users = db.query(User).all()
    for user in users:
        login_count = db.query(AuditLog).filter(AuditLog.user_id == user.id, AuditLog.action == "login").count()
        workflow_count = db.query(UsageLog).filter(UsageLog.user_id == user.id, UsageLog.action == "workflow_created").count()
        permission_changes = db.query(AuditLog).filter(AuditLog.user_id == user.id, AuditLog.action == "permission_change").count()

        writer.writerow([
            user.id,
            user.full_name,
            user.tier,
            user.role,
            login_count,
            workflow_count,
            permission_changes
        ])

    return Response(content=output.getvalue(), media_type="text/csv")
