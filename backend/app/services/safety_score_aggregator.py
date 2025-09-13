# backend/app/services/safety_score_aggregator.py

from sqlalchemy.orm import Session
from app.models.feedback import SafetySignal

def get_safety_scores(db: Session, workflow_id: int):
    """
    Aggregates psychological safety scores for a workflow.
    Strategic Role:
    - Powers team health dashboards, onboarding refinement, and contributor coaching.
    - Scalable for org benchmarking, role segmentation, and alert triggers.
    - Extensible for scorecards, trend analysis, and feedback loops.
    """
    signals = db.query(SafetySignal).filter(SafetySignal.workflow_id == workflow_id).all()
    if not signals:
        return {
            "clarity": None,
            "trust": None,
            "collaboration": None,
            "count": 0
        }

    total = len(signals)
    clarity = sum(s.clarity for s in signals) / total
    trust = sum(s.trust for s in signals) / total
    collaboration = sum(s.collaboration for s in signals) / total

    return {
        "clarity": round(clarity, 2),
        "trust": round(trust, 2),
        "collaboration": round(collaboration, 2),
        "count": total
    }
