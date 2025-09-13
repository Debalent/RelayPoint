# backend/app/services/governance_scorecard.py

from sqlalchemy.orm import Session
from app.models.workflow import Workflow
from app.models.audit import AuditLog
from app.models.user import User

def calculate_governance_score(db: Session, org_id: int):
    """
    Calculates a governance score for an organization.
    Strategic Role:
    - Powers investor dashboards, admin coaching, and org benchmarking.
    - Scalable for multi-tenant platforms and role-based segmentation.
    - Extensible for score breakdowns, alerts, and export logic.
    """
    workflows = db.query(Workflow).filter(Workflow.org_id == org_id).all()
    audit_logs = db.query(AuditLog).filter(AuditLog.org_id == org_id).all()
    users = db.query(User).filter(User.org_id == org_id).all()

    score = 0
    breakdown = {}

    # Workflow coverage
    active_workflows = [wf for wf in workflows if wf.status == "active"]
    breakdown["workflowCoverage"] = len(active_workflows)
    score += min(len(active_workflows) * 2, 20)

    # Audit activity
    breakdown["auditEvents"] = len(audit_logs)
    score += min(len(audit_logs) // 10, 15)

    # Role clarity
    role_assigned = sum(1 for user in users if user.role is not None)
    breakdown["roleClarity"] = role_assigned
    score += min(role_assigned * 1.5, 15)

    # Collaboration density
    collab_events = [log for log in audit_logs if log.action == "collaboration"]
    breakdown["collaborationDensity"] = len(collab_events)
    score += min(len(collab_events) // 5, 20)

    # Governance hygiene
    hygiene_events = [log for log in audit_logs if log.action in ["permission_updated", "role_changed", "workflow_archived"]]
    breakdown["hygieneEvents"] = len(hygiene_events)
    score += min(len(hygiene_events) // 3, 15)

    return {
        "org_id": org_id,
        "score": min(score, 100),
        "breakdown": breakdown
    }
