# backend/app/schemas/notification.py

from pydantic import BaseModel
from typing import Optional

class NotificationPreferences(BaseModel):
    """
    Defines user-specific preferences for receiving notifications.
    Supports customization by channel, frequency, and event type.

    Strategic Role:
    - Empowers users to control their engagement experience.
    - Scalable for multi-channel delivery (email, SMS, in-app).
    - Extensible for role-based defaults, monetization tiers, and analytics.
    """
    email_enabled: bool = True
    sms_enabled: bool = False
    in_app_enabled: bool = True
    frequency: Optional[str] = "realtime"  # Options: realtime, daily_digest, weekly_summary
    notify_on_step_complete: bool = True
    notify_on_project_update: bool = True
