# backend/app/api/v1/endpoints/preferences.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notification import NotificationPreferences
from app.models.user import User
from app.db import get_db

router = APIRouter(prefix="/notifications", tags=["preferences"])

@router.post("/preferences")
def save_preferences(preferences: NotificationPreferences, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Saves or updates the current user's notification preferences.
    Enables personalized alert delivery and compliance with opt-in standards.

    Strategic Role:
    - Empowers users to control engagement and reduce alert fatigue.
    - Scalable for multi-channel delivery, role-based defaults, and monetization tiers.
    - Extensible for analytics, behavioral targeting, and enterprise compliance.
    """
    current_user.notification_preferences = preferences.dict()
    db.add(current_user)
    db.commit()
    return {"status": "preferences updated"}
