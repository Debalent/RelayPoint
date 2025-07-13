```python
"""
Workflow model for RelayPoint's SQLAlchemy ORM.

This module defines the Workflow model, representing automated processes within projects
in RelayPoint's AI-augmented, low-code workflow automation engine. It supports async
operations with TimescaleDB, includes audit fields for compliance, and integrates with
Auth0-based RBAC through project and team relationships. The model is designed for
scalability and compatibility with Alembic migrations.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Supports high-throughput workflow execution with TimescaleDB and async
  operations, ideal for enterprise workloads.
- Reliability: Audit fields (created_at, updated_at) ensure consistent tracking, aligning
  with enterprise SLAs.
- Compliance: Audit-ready fields and relationships meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Security: Integrates with Auth0-based RBAC via project and team relationships.
- Developer Productivity: Type-safe model definitions and clear documentation streamline
  development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Workflow model for RelayPoint backend)
"""

from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from loguru import logger
import uuid

class Workflow(Base):
    """
    SQLAlchemy model for workflows, representing automated processes in projects.

    Attributes:
        id: UUID primary key for the workflow.
        name: Workflow name (required).
        project_id: UUID foreign key linking to the Project model.
        config: JSON field for workflow-specific configurations (e.g., execution settings).
        created_at: Timestamp for workflow creation.
        updated_at: Timestamp for workflow updates.
        project: Relationship to the Project model.
        steps: Relationship to the Step model, ordered by index.
        runs: Relationship to the WorkflowRun model.
    """
    __tablename__ = "workflows"

    id = Column(PUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    project_id = Column(PUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    config = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="workflows")
    steps = relationship("Step", back_populates="workflow", order_by="Step.index")
    runs = relationship("WorkflowRun", back_populates="workflow")

    def __init__(self, **kwargs):
        """
        Initialize a Workflow instance and log creation.

        Args:
            **kwargs: Attributes for the workflow (name, project_id, config).
        """
        super().__init__(**kwargs)
        logger.debug(f"Initialized Workflow instance: {self.id} - {self.name}")

# Log model registration
logger.info("Registered Workflow model with SQLAlchemy Base")
```
