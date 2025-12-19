import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

sample = {
  "event_type": "reservation.checkout",
  "property_id": 1,
  "reservation": {
    "id": "res_test_1",
    "guest_name": "Test Guest",
    "check_in": "2025-12-01",
    "check_out": "2025-12-02",
    "room_id": "room_101",
    "status": "checked_out"
  }
}

def test_webhook_listener():
    res = client.post('/api/v1/integrations/cloudbeds/webhook', json=sample)
    assert res.status_code == 200
    body = res.json()
    assert body.get('status') == 'ok'