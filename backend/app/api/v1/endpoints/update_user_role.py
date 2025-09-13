# backend/app/api/v1/endpoints/update_user_role.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import RoleUpdate

router = APIRouter(prefix="/admin", tags=["user-management"])

@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Allows an admin to update a user's role.
    Supports persona routing, feature gating, and tiered access.

    Strategic Role:
    - Powers governance and team configuration.
    - Scalable for multi-tenant orgs, branded flows, and onboarding logic.
    - Extensible for audit logs, subscription tiers, and behavioral segmentation.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    db.commit()
    return {"status": "role updated", "user_id": user_id, "new_role": role_update.role}
