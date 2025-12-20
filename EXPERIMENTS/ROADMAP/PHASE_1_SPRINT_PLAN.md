Phase 1 Sprint Plan — 90-day roadmap (Hotel Operations: Housekeeping focus)

Objective
Deliver an end-to-end Housekeeping workflow MVP for hotel operations: task assignment, mobile execution (photo upload, offline basics), manager dashboard, Cloudbeds PMS sync (room status), and push notifications. Goal: 3 paid pilot customers within 90 days.

Success Metrics
- 3 paying pilot customers within 90 days
- Pilot customers report >=20% reduction in manager touch-time for housekeeping tasks
- System uptime > 99% and mobile app crash-free for pilot devices
- Forecasting baseline MAE < 2 staff/day after 4 weeks of pilot data

Epics & Milestones (90 days)
1. Week 0 (Planning & Kickoff)
  - Confirm design partners and pilot properties (3 targets)
  - Finalize Phase 1 acceptance criteria and instrument tracking events
  - Setup dev environment and data access with pilot customers

2. Weeks 1–4 (Sprint 1)
  - Implement Cloudbeds PoC (room status sync, check-in/out events)
  - Mobile: task assignment, task list, photo upload, basic offline cache
  - Backend: task persistence and API endpoints, auth + RBAC (basic)
  - QA: smoke tests, onboarding playbook for pilot installs

3. Weeks 5–8 (Sprint 2)
  - Manager Dashboard: live task board, filter by shift/room, export
  - Push notifications & WebSocket real-time sync
  - Mobile: offline sync improvements, push integration, minor UX
  - Cloudbeds: finalize mapping, handle edge cases (cancellations, group bookings)

4. Weeks 9–12 (Sprint 3 & Pilot Launch)
  - Pilot onboarding documentation, device provisioning SOP
  - Start pilots for 3 properties, daily monitoring & hotfixes
  - Integrate forecasting into dashboard and begin collecting predictions vs actuals
  - Collect feedback, iterate on workflows & UI

Deliverables
- Cloudbeds integration (PoC + production-ready adapter)
- Mobile app (iOS/Android) with photo upload, offline sync, push notifications
- Manager dashboard with real-time task board and export
- Pilot onboarding kit: MOU, pre-call checklist, device SOP, tracking sheet
- Monitoring & alerting for pilot health

Owners & Roles
- Product Owner: Demond
- Backend Lead: (hire/assign)
- Mobile Lead: (hire/assign)
- Designer: (hire/assign)
- QA / DevOps: (hire/assign)

Risks & Mitigations
- PMS API access delays (mitigation: secure API access early, use Cloudbeds as initial integration)
- Pilot data quality (mitigation: pre-install data checks and short training for staff)
- Mobile device compatibility (mitigation: provide managed iPads or test devices)

Next steps
- Confirm pilot customers and Cloudbeds account access
- Create sprint tickets (Jira/GitHub issues) for each deliverable and schedule sprints
- Begin Cloudbeds PoC immediately and run parallel mobile dev

Notes
- All sprint progress will be tracked in `EXPERIMENTS/ROADMAP` and associated GitHub issues.  
- For each pilot, use `EXPERIMENTS/ANALYTICS/ASSUMPTION_3_ANALYTICS_TEMPLATE.csv` to store daily KPI rows.