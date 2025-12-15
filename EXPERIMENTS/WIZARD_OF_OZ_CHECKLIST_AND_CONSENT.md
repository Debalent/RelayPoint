Wizard-of-Oz Operator Checklist & Consent — RelayPoint Elite

Purpose

This document provides step-by-step operator instructions, manager consent text, staff notification copy, override reasons, micro-survey templates, and a short MOU clause for running the Wizard-of-Oz (WoZ) Auto-Action Simulation described in `EXPERIMENTS/ASSUMPTION_2_AI_TRUST_AND_AUTOMATION.md`.

Manager Consent (Email / Short Agreement)

Subject: Pilot consent — RelayPoint Auto-Action Simulation (2 weeks)

Hi [Manager Name],

Thanks for agreeing to participate in a two-week RelayPoint simulation. Summary:
- What we’ll do: RelayPoint will "auto-assign" a small set of routine, non-guest-facing tasks (e.g., housekeeping assignments, low-priority maintenance routing) during agreed shifts. Actions will be performed by our operator (human-in-the-loop) and show as "RelayPoint auto-assigned" in your staff UI.
- Controls: Any staff member can immediately undo/override an action with one tap. Every auto-action is logged and visible to managers.
- Data: We will capture acceptance/override, timestamps, and short reasons for overrides. We’ll also collect brief micro-survey feedback after actions and a weekly trust survey from managers.
- Safety: No guest-critical or payroll-affecting actions will be automated during this simulation.
- Commitment: We ask only for transparency and cooperation; there is no financial commitment. You can withdraw at any time.

If you approve, reply to this email: "I consent to RelayPoint's two-week WoZ simulation for [property name]."

Operator Checklist (Pre-run)

1. Confirm signed consent/reply from manager. Record manager name, property, number of rooms, and point of contact.
2. Confirm scope of allowed task categories and time windows (e.g., Housekeeping assignments only, days 9AM–5PM).
3. Set up a tracking sheet (CSV/Google Sheet) with logging columns (see Logging Schema below).
4. Configure calendar availability and operator shift schedule.
5. Ensure staff are briefed by manager about the pilot and know the override method.
6. Prepare micro-survey (short link) and weekly trust survey.
7. Confirm operator has access and knows how to mark `wizard_action=true` in logs.

Operator Checklist (Daily)

1. Review yesterday's overrides and reasons; flag patterns to product/ops.
2. Check inbound triggers that match the automated rule set; perform actions via the backend UI, marking as "auto-assigned".
3. Immediately log action in the sheet with required fields (timestamp, property, room, task_type, assigned_to, operator_id, auto_assigned=true).
4. If staff override occurs, log override and override reason (selected from list or free text).
5. Send optional short note to manager for any unusual overrides or repeated rejections.
6. At end of shift, export actions and micro-survey responses for secure storage and analysis.

Operator Script (What to show users)

- In-app notification: "RelayPoint auto-assigned this task — tap Accept or Override. If overriding, choose a reason: Wrong room, Priority changed, Guest need, Other (explain)."
- Push/SMS (optional): "RelayPoint assigned [Task] for [Room]. Tap [Open] to accept or override."
- If staff taps Override: present reason selector + optional free-text; record timestamp and user.

Override Reasons (predefined)

- Wrong room
- Priority changed (urgent guest need)
- Guest present / guest-facing issue
- Incorrect task type
- Staffing constraints
- Other (free text)

Logging Schema (minimum fields)

- action_id (unique)
- timestamp_assigned
- property_id
- property_name
- room_number
- task_type
- assigned_to (staff id/name)
- operator_id
- auto_assigned (bool)
- overridden (bool)
- override_timestamp
- override_reason
- started_at
- completed_at
- result_helpful (micro-survey response: yes/no)
- notes (free text)

Micro-survey (post-action)

Question (1-tap): "Was this automated assignment helpful?" [Yes] [No]
Optional follow-up (if No): "Why not?" (short text)

Weekly Manager Trust Survey (3 items)

1. Overall, how helpful were the automated assignments this week? (1–5)
2. How comfortable would you be expanding auto-assignments to more categories? (1–5)
3. Did you experience any safety or guest-impact issues? [Yes/No — if Yes, please explain]

Transparency & Undo

- All auto-actions must be visible in a manager-accessible activity log in near real-time.
- An obvious single-tap undo must be available to staff and managers for every action.
- Operator must notify manager immediately if an override indicates a safety or guest-affecting issue.

Manager FAQ (short)

Q: What if an auto-action affects a guest?  
A: We will not automate guest-facing tasks in this simulation. If any such event occurs, we notify the manager and stop that rule immediately.

Q: Will this affect payroll or hours?  
A: No—this simulation only assigns tasks. Timekeeping and payroll are not impacted.

Q: Can I withdraw?  
A: Yes. Reply "Withdraw" and we'll stop the simulation immediately and archive collected data.

Example MOU Clause (one-paragraph)

"Participant grants RelayPoint permission to run a two-week Wizard-of-Oz simulation limited to pre-defined, non-guest-facing operational tasks. RelayPoint will log actions, maintain an activity audit, and provide an opt-out. The participant may withdraw at any time and RelayPoint will not make permanent operational changes or impact payroll during the simulation."

Safety & Legal Notes

- Do not simulate or automate actions that affect security, legal compliance, or payroll without legal counsel.
- Keep explicit logs and manager consent to defend against any disputes.

Deliverables (I can create)

- Manager consent email template (finalized text for sending)
- Staff notification copy (in-app + SMS templates)
- Operator checklist (document and printable checklist)
- Google Sheet tracking template with columns pre-populated and sample rows
- Short micro-survey form (Typeform/Google Forms) and weekly trust survey

Next step: I can draft the manager consent email as a ready-to-send template, create the Google Sheet tracking template, and produce the micro-survey/form. Which deliverable do you want first?