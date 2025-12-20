from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class CloudbedsRoomMapping(Base):
    __tablename__ = "cloudbeds_room_mappings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    cloud_room_id = Column(String, nullable=False)
    property_room_id = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())