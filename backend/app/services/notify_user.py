# backend/app/services/notify_user.py

import requests

def notify_user(user_email: str, message: str):
    """
    Sends a notification to a user via email or third-party service.
    Can be triggered on workflow events, step completions, or system alerts.

    Strategic Role:
    - Drives engagement and responsiveness across collaborative workflows.
    - Scalable for email, SMS, push notifications, or in-app alerts.
    - Extensible for role-based messaging, branded templates, and analytics tracking.
    """
    # Placeholder: Replace with actual email service or webhook integration
    payload = {
        "to": user_email,
        "subject": "RelayPoint Notification",
        "body": message
    }

    # Example: Send to external notification service
    try:
        response = requests.post("https://api.notification-service.com/send", json=payload)
        response.raise_for_status()
        return {"status": "sent", "recipient": user_email}
    except requests.RequestException as e:
        return {"status": "error", "detail": str(e)}
