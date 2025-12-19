Phase 1 — GitHub Issue Templates and Sprint Plan

Use these templates to create issues in GitHub (manually or via the provided script).

Sprint: 90 days (3 x 30-day sprints)
Owners: @demond (product lead), assign engineers as hired

---

ISSUE: Phase1-001: Finalize Phase 1 acceptance criteria and success metrics
- type: task
- estimate: 1d
- description: Agree on exact success metrics (e.g., 3 paying customers, reduce manager hours by 20%, SLA for task completion), deliverable: acceptance criteria doc.
- labels: roadmap, milestone-0, product
- assignee: demond

---

ISSUE: Phase1-101: Cloudbeds integration — Auth & manual sync
- type: epic/subtask
- estimate: 5d
- description: Implement OAuth flow, manual sync endpoint, DB tables for Cloudbeds reservations and rooms, mapping UI.
- labels: integration, cloudbeds, backend
- acceptance: manual sync returns parity counts for reservations and rooms in sandbox

ISSUE: Phase1-102: Cloudbeds integration — Webhook + automated task creation
- type: task
- estimate: 5d
- description: Implement webhook listener, idempotency, create 'Turnover' tasks on checkout.
- labels: integration, cloudbeds, backend
- acceptance: checkout webhook results in an auto-created task with correct room mapping

---

ISSUE: Phase1-201: Mobile - Task assignment flow (assign/accept/complete)
- type: feature
- estimate: 8d
- description: RN screens for task list, accept task, add notes/photo, complete; offline queueing for actions.
- labels: mobile, feature
- acceptance: tasks can be assigned and completed offline and sync when online

ISSUE: Phase1-202: Mobile - Photo upload + compression + retry
- estimate: 3d
- labels: mobile

ISSUE: Phase1-203: Mobile - Push notifications (APNS/FCM)
- estimate: 3d
- labels: mobile, notifications

---

ISSUE: Phase1-301: Manager Dashboard - Real-time task board
- estimate: 10d
- description: Web view to filter tasks by status, room, shift, assign quickly, basic analytics widgets.
- labels: frontend, dashboard

ISSUE: Phase1-302: Manager Dashboard - Reports & exports
- estimate: 4d

---

ISSUE: Phase1-401: Pilot instrument & runbook
- estimate: 3d
- description: Create pilot runbook (onboarding checklist, MOU, device provisioning), analytics sheet, and scheduled reporting cadence.
- labels: operations, pilot

---

ISSUE: Phase1-501: Telemetry & model instrumentation
- estimate: 5d
- description: Track predicted vs actual staff, tasks, booking/resolution times; export metrics; basic dashboard for MAE/MAPE.
- labels: analytics, forecasting

---

How to use the script:
- Run `bash scripts/create_github_issues.sh` with a GitHub token set in env (GITHUB_TOKEN) to create all issues with these titles and bodies.

Notes:
- Triage these issues during sprint planning, assign owners, and add story points as you prefer (we used day estimates here).
- If you want, I can create the issues directly (requires a token), or you can run the script locally.
