Phase 1 MVP — Issues & Milestones (90 days)

Goal: Ship an end-to-end housekeeping workflow that can be piloted with 3 paying customers.

Milestone 1 (Weeks 0–2): Core infra & design partner onboarding
- Issue: Finalize Phase 1 acceptance criteria and success metrics (3 paying customers, X% reduction manager hours)
- Issue: Recruit 3 design partner hotels and sign pilot MOUs
- Issue: Create dev environment & CI for mobile and backend

Milestone 2 (Weeks 2–6): Core features
- Issue: Cloudbeds integration (room status sync, check-in/out triggers)
- Issue: Task model enhancements (photo, notes, priority, attachments)
- Issue: Mobile task assignment UI (assign, accept, complete)
- Issue: Basic offline & sync strategy (local queue + conflict resolution)
- Issue: Push notifications (APNS/FCM) wiring

Milestone 3 (Weeks 6–10): Manager dashboard and ops
- Issue: Real-time task board (web) with filters and quick assign
- Issue: Basic reports (completion rate, avg task time, overdue tasks)
- Issue: Booking/triage integration for pilots and deposit capture

Milestone 4 (Weeks 10–12): Pilot instrument and launch
- Issue: Instrument telemetry and analytics for pilot metrics
- Issue: Seed forecasting integration for staffing suggestions (display only)
- Issue: Prepare pilot runbook and support materials (one-pager, MOU, checklist)
- Issue: Launch pilots, collect data, and evaluate against success metrics

Notes on scoping
- Keep initial integrations minimal: Cloudbeds only for Phase 1 (others later)
- Prioritize offline-first UX for mobile due to WiFi limitations in hotels
- Keep the manager dashboard feature set intentionally small—focus on immediate visibility and actions

Owner: Product + Engineering

Next action: Create linked GitHub issues with assigned owners, estimate story points, and schedule sprint planning.