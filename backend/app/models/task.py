from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    role = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    status = Column(String, nullable=True, default="pending")
    department = Column(String, nullable=True)
    guest_room = Column(String, nullable=True)
    guest_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    due_at = Column(DateTime, nullable=True)
    shift = Column(String, nullable=True)
    guest_impact = Column(Boolean, default=False)
    raw = Column(JSON, nullable=True)