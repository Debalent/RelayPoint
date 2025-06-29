import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Team(Base):
    __tablename__ = "team"
    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name     = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    owner    = relationship("User", back_populates="owned_teams")
    members  = relationship("TeamMembership", back_populates="team")
