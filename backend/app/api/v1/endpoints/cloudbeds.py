from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import cloudbeds as crud

router = APIRouter()

class CloudbedsConfig(BaseModel):
    property_id: int
    client_id: str
    client_secret: str
    token: str = None

@router.post('/configure', summary='Configure Cloudbeds integration')
async def configure_cloudbeds(cfg: CloudbedsConfig = Body(...), db: Session = Depends(get_db)):
    # For PoC store in a simple config table or secret manager (placeholder)
    # In production, use encrypted secrets store
    # For now just acknowledge
    return {'status': 'ok', 'property_id': cfg.property_id}

@router.post('/sync', summary='Manual sync from Cloudbeds')
async def manual_sync(property_id: int, db: Session = Depends(get_db)):
    # Placeholder: call Cloudbeds API, fetch rooms and reservations and upsert
    # PoC: return mock counts
    return {'status': 'ok', 'rooms_synced': 0, 'reservations_synced': 0}

@router.post('/webhook', summary='Cloudbeds webhook listener')
async def cloudbeds_webhook(req: Request, db: Session = Depends(get_db)):
    payload = await req.json()
    # Expected example payload keys: event_type, reservation, room
    event_type = payload.get('event_type')
    property_id = payload.get('property_id')
    try:
        if event_type == 'reservation.created' or event_type == 'reservation.updated':
            res = payload.get('reservation', {})
            crud.upsert_reservation(db, property_id=property_id, reservation_id=str(res.get('id')), guest_name=res.get('guest_name'), check_in=res.get('check_in'), check_out=res.get('check_out'), room_id=res.get('room_id'), status=res.get('status'), raw=res)
        elif event_type == 'room.updated':
            room = payload.get('room', {})
            crud.upsert_room(db, property_id=property_id, room_id=str(room.get('id')), room_number=room.get('number'), room_type=room.get('type'), metadata=room)
        # On checkout event, create a turnover task (use existing task creation service)
        if event_type == 'reservation.checkout':
            # Minimal: emit a task creation event or call internal service
            pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'status': 'ok'}