# Pilot Plan — iPad Device Deployment (3-Property Pilot)

Objective
- Validate iPad-first workflow, device adoption, dock-based device-return flow, and operational impact of RelayPoint in real hotels.

Scope
- 3 mid-size hotels (50–150 rooms)
- 4 iPads per property (shared across shifts) — 12 active devices
- 2 spare devices total
- 2 docks per property (charging + presence sensor)
- Pilot length: 6 weeks per property (staggered starts across properties)

Key Features to Validate
- Frontline staff adoption of company-owned iPad (per-shift login)
- Dock event → device-return signal → timekeeping integration
- Single App Mode (RelayPoint only) and session logging
- Task resolution improvements and reduction in dropped tasks

Success Metrics (baseline vs pilot)
- Device return rate (docked before shift end) — target ≥85%
- Dropped/unassigned tasks per shift — target ≥50% reduction
- Average task resolution time — target ≥20% faster
- Room turnover time — target measurable improvement (site-specific)
- Staff satisfaction (short pre/post survey) — neutral or positive
- Manager willingness to continue after pilot (qualitative)

Pilot Steps
1. Procurement & Setup (week -2 to 0)
   - Purchase/enroll devices in Apple Business Manager (ABM)
   - Configure MDM (Supervised mode, Single App Mode, per-shift login)
   - Set up docks and webhook endpoint; test dock → backend event flow
   - Prepare device inventory, cases, and spares
2. Training & Onboarding (day 0)
   - 30–60 minute manager training session
   - Short 5–10 minute role cards for frontline staff
3. Pilot Execution (weeks 1–6)
   - Week 1: shadowing + high-touch support
   - Weeks 2–5: collect operational metrics and feedback
   - Week 6: wrap-up, post-pilot survey, and results review
4. Synthesis & Decision (week 7)
   - Compare baseline vs pilot metrics
   - Decide continue, expand, or pivot

Data & Integrations
- Timekeeping: submit dock-return flags to payroll/time API (or CSV for pilots)
- Task system: RelayPoint event logs (task assign/complete timestamps)
- MDM: device health & provisioning status

Risk & Mitigations
- Legal: avoid hard-blocking clock-out; use dock as a signal and manager override
- Lost/stolen devices: remote wipe via MDM + spare device replacement plan
- Dock failure: dock health monitoring and spare dock on standby

Notes
- Device policy must be signed by staff prior to pilot (policy provided separately)
- Counsel/HR review recommended if you plan to enforce device-return rules beyond soft enforcement

Contact
- Pilot lead: Demond J Balentine (Debalent)
- Email: demond.balentine@atlasstudents.com

