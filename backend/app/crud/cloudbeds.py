from sqlalchemy.orm import Session
from app.models import cloudbeds as cb


def upsert_room(db: Session, *, property_id: int, room_id: str, room_number: str = None, room_type: str = None, metadata: dict = None):
    existing = db.query(cb.CloudbedsRoom).filter_by(property_id=property_id, room_id=room_id).first()
    if existing:
        existing.room_number = room_number or existing.room_number
        existing.room_type = room_type or existing.room_type
        existing.metadata = metadata or existing.metadata
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    obj = cb.CloudbedsRoom(property_id=property_id, room_id=room_id, room_number=room_number, room_type=room_type, metadata=metadata)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def upsert_reservation(db: Session, *, property_id: int, reservation_id: str, guest_name: str = None, check_in=None, check_out=None, room_id: str = None, status: str = None, raw: dict = None):
    existing = db.query(cb.CloudbedsReservation).filter_by(property_id=property_id, reservation_id=reservation_id).first()
    if existing:
        existing.guest_name = guest_name or existing.guest_name
        existing.check_in = check_in or existing.check_in
        existing.check_out = check_out or existing.check_out
        existing.room_id = room_id or existing.room_id
        existing.status = status or existing.status
        existing.raw = raw or existing.raw
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    obj = cb.CloudbedsReservation(property_id=property_id, reservation_id=reservation_id, guest_name=guest_name, check_in=check_in, check_out=check_out, room_id=room_id, status=status, raw=raw)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj