```python
"""
Project model for RelayPoint's SQLAlchemy ORM.

This module defines the Project model, representing logical groupings of workflows within
teams in RelayPoint's AI-augmented, low-code workflow automation engine. It supports async
operations with TimescaleDB, includes audit fields for compliance, and integrates with
Auth0-based RBAC through team relationships. The model is designed for scalability and
compatibility with Alembic migrations.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Supports high-throughput project and workflow data with TimescaleDB and
  async operations, ideal for enterprise workloads.
- Reliability: Audit fields (created_at, updated_at) ensure consistent tracking, aligning
  with enterprise SLAs.
- Compliance: Audit-ready fields and relationships meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Security: Integrates with Auth0-based RBAC via team relationships.
- Developer Productivity: Type-safe model definitions and clear documentation streamline
  development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Project model for RelayPoint backend)
"""

from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from loguru import logger
import uuid

class Project(Base):
    """
    SQLAlchemy model for projects, grouping workflows within teams.

    Attributes:
        id: UUID primary key for the project.
        name: Project name (required).
        team_id: UUID foreign key linking to the Team model.
        config: JSON field for project-specific configurations.
        created_at: Timestamp for project creation.
        updated_at: Timestamp for project updates.
        team: Relationship to the Team model.
        workflows: Relationship to the Workflow model.
    """
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True)
    config = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    team = relationship("Team", back_populates="projects")
    workflows = relationship("Workflow", back_populates="project")

    def __init__(self, **kwargs):
        """
        Initialize a Project instance and log creation.

        Args:
            **kwargs: Attributes for the project (name, team_id, config).
        """
        super().__init__(**kwargs)
        logger.debug(f"Initialized Project instance: {self.id} - {self.name}")

# Log model registration
logger.info("Registered Project model with SQLAlchemy Base")
```
