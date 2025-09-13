# backend/app/api/v1/endpoints/persona.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.get_user_persona import get_user_persona
from app.db import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["persona"])

@router.get("/persona")
def fetch_user_persona(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns the persona type for the current user.
    Used to personalize onboarding, dashboard views, and feature access.

    Strategic Role:
    - Powers adaptive UX and role-based routing.
    - Scalable for tiered pricing, branded flows, and feature gating.
    - Extensible for analytics, onboarding metrics, and behavioral targeting.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    persona = get_user_persona(current_user)
    return {"persona": persona}
