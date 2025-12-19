LinkedIn Poll — Monitoring Playbook

Objective: Ensure timely follow-up of hand-raisers and consistent logging for analysis.

Roles
- Owner: Demond (primary responder)
- Backup: [Name or role] (check replies if owner unavailable)

Check-in cadence
- T+2 hours: quick scan for comments and DMs (prioritize hand-raisers)
- T+24 hours: follow-up on any unanswered DMs/comments
- Daily thereafter: review DMs, book triage calls, send one-pager and MOU as needed

Logging steps
1. When a hand-raiser is found (comment or DM), copy their details to `EXPERIMENTS/OUTREACH/PROSPECT_TEMPLATE.csv` with: name, title, company, location, linkedin_url, email (if provided), source=LinkedIn Poll, contacted_date, response="hand-raised", next_action.
2. Send SHORT DM snippet (copy from `DM_SNIPPETS.md`).
3. Update POLL_MONITORING.csv with a hand_raiser_count increment and hand_raiser_details (brief note)
4. If a booking is made: add booked_date and booking_email; if deposit is taken, update deposit_status.

Prioritization (who to triage first)
- High priority: Director+ Operations roles at properties 75+ rooms OR multiple properties
- Medium: Manager-level roles at 50–75 rooms
- Low: roles < 50 rooms or vendors

Triage call script (15 min)
- Intro (1 min): confirm role & pain
- Diagnosis (6 min): ask about current process, volume, staffing, pain points
- Pilot pitch (4 min): explain 6-week pilot, turnkey setup, key outcomes, minimal manager time
- Next step (2–3 min): offer times and send the one-pager + MOU; if immediate deal, offer deposit link

Reporting
- At Day 8 compile a 1‑page summary: votes, hand‑raisers, booked triage calls, deposits, sample qualitative quotes, and recommended next steps.

Escalations
- If a reply is clearly a sales-qualified lead: add "priority outreach" and notify founder immediately.
- If a group admin flags the post or requests edits, remove or adapt variant for compliance and repost with admin note.

Optional automation notes
- An email parser can append bookings and replies to `PROSPECT_TEMPLATE.csv` automatically.
- If you want I can provide a small script or Zapier instructions to semi-automate this.