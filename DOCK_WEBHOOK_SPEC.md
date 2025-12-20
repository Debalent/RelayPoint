# Dock Webhook Specification

Purpose
- Describe the webhook payload and security for dock -> RelayPoint backend events when a device is docked/undocked.

Event types
- `device_docked` — fired when a device is placed in a dock
- `device_undocked` — fired when a device is removed from a dock

Payload (JSON)
{
  "event": "device_docked",
  "dock_id": "dock-abc-001",
  "device_serial": "ABCDEFG12345",
  "device_udid": "<udid-or-serial>",
  "timestamp": "2025-12-10T14:32:00Z",
  "signature": "<HMAC-SHA256-signature>"
}

Security
- Each dock controller is provisioned with a shared secret or private key.
- Use HMAC-SHA256 over the payload (or a canonical string) and include `signature` header/value. Backend validates signature before accepting event.
- All webhooks must be sent over HTTPS with TLS (valid cert).

Delivery semantics
- Webhooks should be retried on failure with exponential backoff.
- Include an `idempotency_key` if events might be delivered multiple times.

Backend actions (example)
1. Validate signature and map `device_serial` to active session (last authenticated user on device).
2. Mark session as `docked` and record timestamp.
3. Optionally call timekeeping API to submit a clock-out request or set a `device_returned` flag for manager review.
4. Respond `200 OK` on success.

Example curl
```bash
curl -X POST https://relaypoint.example.com/webhooks/dock \
  -H "Content-Type: application/json" \
  -d '{"event":"device_docked","dock_id":"dock-abc-001","device_serial":"ABCDEFG12345","timestamp":"2025-12-10T14:32:00Z","signature":"..."}'
```

