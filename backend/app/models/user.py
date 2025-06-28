# backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    is_manager = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)

    # ─── Password reset fields ────────────────────────────────────────
    reset_token = Column(
        String, index=True, nullable=True,
        comment="One-time token for resetting password"
    )
    reset_token_expires = Column(
        DateTime, nullable=True,
        comment="UTC timestamp when reset_token expires"
    )

    def set_reset_token(self, token: str, expires_in: int = 3600):
        """Helper to generate a token + expiry on the model instance."""
        self.reset_token = token
        self.reset_token_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

    def clear_reset_token(self):
        """Helper to clear reset fields after successful password change."""
        self.reset_token = None
        self.reset_token_expires = None
