# backend/app/schemas/step.py

from pydantic import BaseModel
from typing import List

class StepItem(BaseModel):
    """
    Represents a single step's status within a workflow.
    Used for frontend rendering and progress tracking.

    Strategic Role:
    - Enables real-time feedback and UI updates.
    - Scalable for analytics, notifications, and role-based filtering.
    - Extensible for timestamps, assigned users, and monetization metadata.
    """
    id: str
    name: str
    is_complete: bool

class StepStatus(BaseModel):
    """
    Aggregates all step statuses for a given workflow.
    Returned by the /status endpoint to power dashboards and UX flows.

    Strategic Role:
    - Defines API contract for workflow progress tracking.
    - Scalable for multi-user views, mobile clients, and analytics engines.
    - Extensible for audit logs, completion rates, and execution metadata.
    """
    steps: List[StepItem]
