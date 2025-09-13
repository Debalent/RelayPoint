# backend/app/api/v1/endpoints/filtered_audit_logs.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from app.auth import get_current_user
from app.models.audit import AuditLog

router = APIRouter(prefix="/admin", tags=["audit"])

@router.get("/audit-logs")
def get_filtered_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    action: str = Query(None),
    user_id: int = Query(None)
):
    """
    Returns filtered audit logs for admin analysis.
    Supports date range, action type, and user-specific queries.

    Strategic Role:
    - Powers governance analytics and behavioral segmentation.
    - Scalable for multi-tenant orgs, investor dashboards, and compliance reviews.
    - Extensible for persona filters, export tools, and UI surfacing.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    query = db.query(AuditLog)

    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    logs = query.order_by(AuditLog.timestamp.desc()).all()
    return {"logs": logs}
