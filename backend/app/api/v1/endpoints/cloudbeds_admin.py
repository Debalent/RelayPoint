from fastapi import APIRouter, Query, Depends, Body
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import cloudbeds_mapping as mapping_crud
from app.crud import cloudbeds as cb_crud

router = APIRouter()

@router.get('/rooms', summary='List Cloudbeds rooms')
async def list_rooms(property_id: int = Query(...), db: Session = Depends(get_db)):
    # Return rooms and mapping status
    rooms = db.query(cb_crud).all() if False else []
    # For PoC, return CloudbedsRoom entries
    res = db.execute("SELECT room_id, room_number, room_type FROM cloudbeds_rooms WHERE property_id = :pid", {"pid": property_id})
    rows = [{"room_id": r["room_id"], "room_number": r["room_number"], "room_type": r["room_type"]} for r in res]
    # Add mapping info
    for r in rows:
        m = mapping_crud.get_mapping(db, property_id=property_id, cloud_room_id=r["room_id"])
        r["mapped_to"] = m.property_room_id if m else None
    return {"rooms": rows}

@router.post('/map', summary='Create room mapping')
async def create_map(payload: dict = Body(...), db: Session = Depends(get_db)):
    property_id = payload.get('property_id')
    cloud_room_id = payload.get('cloud_room_id')
    property_room_id = payload.get('property_room_id')
    obj = mapping_crud.create_mapping(db, property_id=property_id, cloud_room_id=cloud_room_id, property_room_id=property_room_id)
    return {"mapping": {"id": obj.id, "cloud_room_id": obj.cloud_room_id, "property_room_id": obj.property_room_id}}