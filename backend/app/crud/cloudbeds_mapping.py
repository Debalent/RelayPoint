from sqlalchemy.orm import Session
from app.models import cloudbeds_mapping as cbm


def create_mapping(db: Session, *, property_id: int, cloud_room_id: str, property_room_id: str):
    obj = cbm.CloudbedsRoomMapping(property_id=property_id, cloud_room_id=cloud_room_id, property_room_id=property_room_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_mapping(db: Session, property_id: int, cloud_room_id: str):
    return db.query(cbm.CloudbedsRoomMapping).filter_by(property_id=property_id, cloud_room_id=cloud_room_id).first()


def list_mappings(db: Session, property_id: int):
    return db.query(cbm.CloudbedsRoomMapping).filter_by(property_id=property_id).all()