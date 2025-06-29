import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Project(Base):
    __tablename__ = "project"
    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name     = Column(String, nullable=False)
    team_id  = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)
    team     = relationship("Team", back_populates="projects")
    workflows= relationship("Workflow", back_populates="project")
