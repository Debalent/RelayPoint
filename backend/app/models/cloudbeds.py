from sqlalchemy import Column, Integer, String, Date, JSON, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class CloudbedsRoom(Base):
    __tablename__ = "cloudbeds_rooms"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    room_id = Column(String, nullable=False)
    room_number = Column(String, nullable=True)
    room_type = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class CloudbedsReservation(Base):
    __tablename__ = "cloudbeds_reservations"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    reservation_id = Column(String, nullable=False)
    guest_name = Column(String, nullable=True)
    check_in = Column(Date)
    check_out = Column(Date)
    room_id = Column(String, nullable=True)
    status = Column(String, nullable=True)
    raw = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())