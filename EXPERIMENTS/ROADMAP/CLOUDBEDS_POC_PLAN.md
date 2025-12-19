Cloudbeds PoC Plan — Objectives & Test Plan

Objective
- Validate Cloudbeds integration for: auth flow, room/reservation sync, webhook events, and auto-creation of turnover tasks on checkout.

Scope
- Auth: OAuth2/client credentials or API key for sandbox
- Manual sync: endpoint to fetch rooms & reservations and upsert into DB
- Webhook: listener for reservation.checkin, reservation.checkout, room.updated events
- Mapping UI: small admin page to map Cloudbeds room IDs to RelayPoint property rooms
- Task creation: on checkout, auto-create a 'Turnover' task with room reference

Success criteria
- PoC can sync at least 90% of rooms and upcoming reservations from a Cloudbeds sandbox account
- Webhook checkout event results in a created Turnover task associated with the room
- Mapping UI allows admin to map rooms and view sync status

Test plan
1. Manual sync: run /sync and verify rows in cloudbeds_rooms and cloudbeds_reservations
2. Webhook: POST sample payload to /webhook and assert reservation inserted and turnover task created
3. Mapping: verify mapping UI shows unmapped rooms and ability to assign property room

Deliverables
- DB migration and models
- Backend endpoints (/configure, /sync, /webhook)
- CRUD helpers & unit tests
- Mapping UI scaffold in frontend
- PoC runbook with sample webhook payloads and validation steps

Timeline
- Day 0–3: Implement migration, models, CRUD, and basic endpoints
- Day 3–7: Implement webhook handling, mapping UI stub, and create basic tests
- Day 7–10: Validate with Cloudbeds sandbox; prepare pilot checklist

Notes
- Use idempotency keys for webhook handling to avoid duplicate processing
- Store secrets securely (use env for PoC)
- For the PoC, create a fake sample webhook payload in `EXPERIMENTS/INTEGRATIONS/CLOUDBEDS_SAMPLE_PAYLOAD.json`
