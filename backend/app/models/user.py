```python
"""
User model for RelayPoint's SQLAlchemy ORM.

This module defines the User model, representing individuals interacting with teams and
projects in RelayPoint's AI-augmented, low-code workflow automation engine. It supports
async operations with TimescaleDB, includes audit fields for compliance, and integrates
with Auth0-based authentication for secure user management. The model is designed for
scalability and compatibility with Alembic migrations.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Supports high-throughput user and workflow data with TimescaleDB and async
  operations, ideal for enterprise workloads.
- Reliability: Audit fields (created_at, updated_at) ensure consistent tracking, aligning
  with enterprise SLAs.
- Compliance: Audit-ready fields and Auth0 integration meet GDPR, HIPAA, and SOC 2
  requirements, appealing to regulated industries like finance and healthcare.
- Security: Auth0-based authentication eliminates local password storage, enhancing security.
- Developer Productivity: Type-safe model definitions and clear documentation streamline
  development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (User model for RelayPoint backend)
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.team import user_team
from loguru import logger
import uuid
import datetime
from typing import Optional

class User(Base):
    """
    SQLAlchemy model for users, representing individuals in teams and projects.

    Attributes:
        id: UUID primary key for the user.
        phone: Unique phone number (required).
        email: Unique email address (required).
        name: Full name of the user (required).
        is_manager: Boolean indicating manager status.
        auth0_user_id: Auth0 user ID for authentication.
        reset_token: One-time token for password reset.
        reset_token_expires: UTC timestamp when reset_token expires.
        created_at: Timestamp for user creation.
        updated_at: Timestamp for user updates.
        teams: Relationship to Team model via user_team join table.
        owned_teams: Relationship to Team model (owned teams).
    """
    __tablename__ = "users"

    id = Column(PUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_manager = Column(Boolean, default=False, nullable=False)
    auth0_user_id = Column(String(255), unique=True, nullable=True)
    reset_token = Column(String(36), index=True, nullable=True, comment="One-time token for resetting password")
    reset_token_expires = Column(DateTime, nullable=True, comment="UTC timestamp when reset_token expires")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    teams = relationship("Team", secondary=user_team, back_populates="members")
    owned_teams = relationship("Team", back_populates="owner")

    def __init__(self, **kwargs):
        """
        Initialize a User instance and log creation.

        Args:
            **kwargs: Attributes for the user (phone, email, name, is_manager, auth0_user_id).
        """
        super().__init__(**kwargs)
        logger.debug(f"Initialized User instance: {self.id} - {self.name}")

    def set_reset_token(self, token: str, expires_in: int = 3600) -> None:
        """
        Set a password reset token and expiry on the user instance.

        Args:
            token: One-time reset token.
            expires_in: Expiry duration in seconds (default: 1 hour).
        """
        self.reset_token = token
        self.reset_token_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        logger.debug(f"Set reset token for user {self.id}")

    def clear_reset_token(self) -> None:
        """
        Clear reset token fields after successful password change.
        """
        self.reset_token = None
        self.reset_token_expires = None
        logger.debug(f"Cleared reset token for user {self.id}")

# Log model registration
logger.info("Registered User model with SQLAlchemy Base")
```
