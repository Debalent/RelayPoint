from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Shared secret (in real deployments load from env/secret store)
DOCK_SHARED_SECRET = os.getenv("DOCK_SHARED_SECRET", "super-secret-key")

class DockEvent(BaseModel):
    event: str
    dock_id: str
    device_serial: str
    timestamp: datetime
    signature: str = None
    idempotency_key: str = None


def validate_signature(payload_bytes: bytes, signature: str) -> bool:
    mac = hmac.new(DOCK_SHARED_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)


@router.post("/webhooks/dock")
async def dock_webhook(request: Request):
    body_bytes = await request.body()
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    signature = payload.get("signature")
    if not signature or not validate_signature(body_bytes, signature):
        raise HTTPException(status_code=401, detail="invalid signature")

    # Basic payload validation
    try:
        event = DockEvent(**payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"payload invalid: {e}")

    # Map device_serial -> active session / user
    # NOTE: In this example we stub the mapping. Replace with DB lookup.
    # Example: session = db.get_active_session_by_device(serial=event.device_serial)
    session = {
        "user_id": "user-123",
        "session_id": "sess-456",
        "device_serial": event.device_serial,
        "state": "active",
    }

    # Process events
    if event.event == "device_docked":
        # mark the session docked
        # e.g., db.mark_session_docked(session_id=session["session_id"], timestamp=event.timestamp)
        # Optionally call timekeeping API or flag for manager review
        print(f"Device {event.device_serial} docked at {event.dock_id} by user {session['user_id']}")
    elif event.event == "device_undocked":
        print(f"Device {event.device_serial} undocked at {event.dock_id}")
    else:
        raise HTTPException(status_code=400, detail="unknown event")

    return {"status": "ok"}


# To wire into main FastAPI app:
# from backend.webhooks.dock_webhook import router as dock_router
# app.include_router(dock_router)
