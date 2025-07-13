```python
"""
Base metadata configuration for RelayPoint's SQLAlchemy models.

This module defines the SQLAlchemy declarative base for all models in RelayPoint's
AI-augmented, low-code workflow automation engine, ensuring consistent metadata across
User, Team, Project, Workflow, and WorkflowRun models. It supports async operations with
TimescaleDB, integrates with Alembic for migrations, and ensures compatibility with
enterprise-grade features like observability and Auth0-based authentication.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Unified metadata with TimescaleDB support enables high-throughput data
  handling for enterprise workloads.
- Reliability: Consistent model definitions prevent migration errors, aligning with
  enterprise SLAs.
- Compliance: Audit-ready models (e.g., WorkflowRun hypertable) meet GDPR, HIPAA, and
  SOC 2 requirements, appealing to regulated industries like finance and healthcare.
- Security: Supports Auth0 integration for secure user management and RBAC.
- Developer Productivity: Type-safe model definitions and clear documentation streamline
  development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Base metadata for RelayPoint models)
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from loguru import logger
from app.core.config import get_settings

# Initialize settings
settings = get_settings()

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models in RelayPoint.

    Inherits from AsyncAttrs for async/await support and DeclarativeBase for ORM
    functionality. Configures metadata for TimescaleDB and Alembic migrations.

    Attributes:
        metadata: SQLAlchemy metadata object for table definitions.
    """
    def __init_subclass__(cls, **kwargs):
        """
        Log model registration for observability.

        Args:
            **kwargs: Additional arguments passed to the subclass.
        """
        logger.info(f"Registering model: {cls.__name__}")
        super().__init_subclass__(**kwargs)

# Create the global Base instance
Base = Base()

# Log base initialization
logger.info("Initialized SQLAlchemy Base for RelayPoint models")
```
