import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Workflow(Base):
    __tablename__ = "workflow"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name       = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    project    = relationship("Project", back_populates="workflows")
    steps      = relationship("Step", back_populates="workflow", order_by="Step.index")
