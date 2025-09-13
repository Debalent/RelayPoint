# backend/app/services/collaboration_aggregator.py

from sqlalchemy.orm import Session
from app.models.usage import UsageLog

def get_collaboration_matrix(db: Session):
    """
    Aggregates collaboration events into a user-to-user matrix.
    Strategic Role:
    - Powers heatmaps, team analytics, and governance scorecards.
    - Scalable for multi-tenant orgs and role-based segmentation.
    - Extensible for visual rendering, anomaly detection, and upgrade nudges.
    """
    logs = db.query(UsageLog).filter(UsageLog.action == "collaboration").all()
    matrix = {}

    for log in logs:
        user_id = log.user_id
        if not log.metadata or "collaborator:" not in log.metadata:
            continue

        collaborator_id = int(log.metadata.split("collaborator:")[1])
        pair = tuple(sorted([user_id, collaborator_id]))

        if pair not in matrix:
            matrix[pair] = 0
        matrix[pair] += 1

    return matrix
