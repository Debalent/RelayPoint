import uuid
from sqlalchemy import Column, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Step(Base):
    __tablename__ = "step"
    id          = Column(PUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(PUUID(as_uuid=True), ForeignKey("workflow.id"), nullable=False)
    index       = Column(Integer, nullable=False)
    type        = Column(Enum("trigger","action", name="step_type"), nullable=False)
    config      = Column(JSON, nullable=False)
    workflow    = relationship("Workflow", back_populates="steps")
  
