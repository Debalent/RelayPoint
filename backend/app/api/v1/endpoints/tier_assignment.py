# backend/app/api/v1/endpoints/tier_assignment.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import TierUpdate
from app.services.audit_log import log_permission_change

router = APIRouter(prefix="/admin", tags=["tier-management"])

@router.put("/users/{user_id}/tier")
def update_user_tier(user_id: int, tier_update: TierUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Allows an admin to assign or update a user's pricing tier.
    Supports feature gating, billing logic, and monetization analytics.

    Strategic Role:
    - Powers monetization workflows and tiered access control.
    - Scalable for multi-tenant orgs, usage-based pricing, and upgrade flows.
    - Extensible for audit logging, billing hooks, and investor dashboards.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    old_tier = user.tier
    user.tier = tier_update.tier
    db.commit()

    # 🔐 Audit log for tier change
    log_permission_change(db, current_user.id, user_id, "tier", old_tier, tier_update.tier)

    return {"status": "tier updated", "user_id": user_id, "new_tier": tier_update.tier}
