# backend/app/services/get_user_persona.py

from app.models.user import User

def get_user_persona(user: User) -> str:
    """
    Determines the user's persona based on metadata, role, or usage patterns.
    Used to personalize onboarding, dashboard views, and feature access.

    Strategic Role:
    - Powers adaptive UX and role-based routing.
    - Scalable for tiered pricing, feature gating, and branded experiences.
    - Extensible for analytics, onboarding flows, and behavioral targeting.
    """
    # Example logic — replace with actual role or usage-based checks
    if user.email.endswith("@label.com"):
        return "producer"
    elif user.email.endswith("@studio.io"):
        return "artist"
    elif user.is_admin:
        return "admin"
    else:
        return "collaborator"
