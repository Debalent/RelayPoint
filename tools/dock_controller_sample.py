"""
Simple dock controller example (MicroPython / ESP32 pseudocode).
Sends a webhook to RelayPoint backend when a device is detected in the dock.
This is a prototype example — adapt for your hardware and provisioning.
"""

import urequests as requests
import machine
import ubinascii
import utime
import hmac
import uhashlib

# Config
BACKEND_URL = "https://relaypoint.example.com/webhooks/dock"
DOCK_ID = "dock-abc-001"
SHARED_SECRET = b"super-secret-key"
DEVICE_SERIAL = "PLACEHOLDER_SERIAL"

# Example: GPIO pin that detects presence (depends on dock hardware)
PRESENCE_PIN = 4
pin = machine.Pin(PRESENCE_PIN, machine.Pin.IN)


def hmac_signature(payload_bytes):
    # HMAC-SHA256
    hm = hmac.new(SHARED_SECRET, payload_bytes, uhashlib.sha256)
    return ubinascii.hexlify(hm.digest()).decode()


def send_event(event_type):
    payload = {
        "event": event_type,
        "dock_id": DOCK_ID,
        "device_serial": DEVICE_SERIAL,
        "timestamp": utime.strftime("%Y-%m-%dT%H:%M:%SZ", utime.localtime())
    }
    import ujson
    body = ujson.dumps(payload)
    sig = hmac_signature(body.encode())
    payload["signature"] = sig

    try:
        r = requests.post(BACKEND_URL, json=payload, headers={"Content-Type":"application/json"})
        r.close()
    except Exception as e:
        # implement retry/backoff in real code
        pass


last_state = pin.value()
while True:
    state = pin.value()
    if state != last_state:
        if state == 1:
            send_event("device_docked")
        else:
            send_event("device_undocked")
        last_state = state
    utime.sleep(0.5)
