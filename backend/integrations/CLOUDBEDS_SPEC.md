Cloudbeds Integration Spec (Phase 1)

Objective
- Implement a Cloudbeds connector to sync room state and bookings, enabling automatic task creation for checkouts and accurate occupancy for forecasting.

Key features
- Sync nightly reservations, room status (occupied, vacant, dirty, clean), and check-in/out events.
- Webhook listener for Cloudbeds events (if supported) for real-time updates.
- Map Room IDs to property_room identifiers used in RelayPoint.
- Create tasks automatically on checkout: "Turnover / Room ready" task with room number, due_by, priority.
- Expose endpoint to query Cloudbeds guest stay info for pilot triage flow (optional).

Data model mapping
- cloudbeds.reservations -> reservations table (guest_name, check_in, check_out, room_id, status)
- cloudbeds.rooms -> property_rooms (room_number, room_type)
- cloudbeds.events -> webhook events (type: checkin, checkout, cancellation)

Security & auth
- OAuth2 client credentials or API key depending on Cloudbeds setup (use secure secrets, rotate keys)
- Validate webhook signatures

API endpoints
- POST /api/v1/integrations/cloudbeds/configure { property_id, client_id, client_secret, oauth_token }
- GET /api/v1/integrations/cloudbeds/sync?property_id={id}  (trigger manual sync)
- POST /webhooks/integrations/cloudbeds  (listener for events)

Retries & resilience
- Implement idempotency keys for events
- Use a job queue (Celery) for long-running sync tasks
- Backoff on API failures and alert on repeated failures

Testing & validation
- End-to-end test with a Cloudbeds sandbox account
- Mapping verification UI for room mapping
- Add monitoring for sync lag and error rates

Milestones
- Week 1: Auth + manual sync + mapping UI
- Week 2: Webhook handling + automated task creation
- Week 3: Tests + pilot verification

Notes
- Cloudbeds API is the first chosen PMS due to ease of integration for small/mid hotels. For enterprise hotels later, add Opera Cloud / Mews.
- This spec will be converted to a set of GitHub issues with tasks for backend, db migrations, UI mapping, tests, and infra.