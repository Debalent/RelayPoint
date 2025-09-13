# backend/app/api/v1/endpoints/export_audit_logs.py

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from io import StringIO
import csv
from app.db import get_db
from app.auth import get_current_user
from app.models.audit import AuditLog

router = APIRouter(prefix="/admin", tags=["audit"])

@router.get("/audit-logs/export")
def export_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Exports audit logs as a CSV file.
    Includes role change events with timestamps and attribution.

    Strategic Role:
    - Powers compliance, investor reporting, and enterprise transparency.
    - Scalable for multi-tenant orgs, export filters, and audit dashboards.
    - Extensible for time-based queries, persona segmentation, and external integrations.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Admin ID", "User ID", "Action", "Old Role", "New Role"])

    for log in logs:
        writer.writerow([
            log.timestamp.isoformat(),
            log.admin_id,
            log.user_id,
            log.action,
            log.old_value,
            log.new_value
        ])

    return Response(content=output.getvalue(), media_type="text/csv")
