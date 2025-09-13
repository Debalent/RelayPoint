# backend/app/api/v1/endpoints/admin_users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["user-management"])

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns a list of all users for admin oversight.
    Includes email, role, and status metadata.

    Strategic Role:
    - Powers governance, compliance, and team configuration.
    - Scalable for multi-tenant orgs, role editing, and audit logging.
    - Extensible for invitations, tier management, and behavioral analytics.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    return db.query(User).all()
