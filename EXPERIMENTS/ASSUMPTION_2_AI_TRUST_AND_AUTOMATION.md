Assumption #2: AI Trust & Automation Boundaries (Behavioral Risk)

Operations managers and frontline supervisors will trust an AI-powered system to automate (not just suggest) operational decisions affecting guest or staff experience, and will allow the system to act without manual pre-approval on routine tasks—with clear boundaries where human oversight is required for guest-facing or safety-critical decisions.

Overview

We want to validate whether staff and managers will accept automated actions from RelayPoint for routine operational tasks (housekeeping assignments, maintenance routing, shift handoffs) and under what conditions (explanations, confidence scores, undo, opt-in). These experiments are designed to be low-effort (Wizard-of-Oz), causal (A/B), and actionable (consent + gradual scope).

Experiment 1 — Wizard-of-Oz Auto-Action Simulation (recommended first)

- Goal: Observe real acceptance, override, and trust signals when an action appears to be taken automatically by the system but is executed by a human operator.
- Target tasks (start low-risk):
  - Housekeeping assignment (room ready/room turn)
  - Maintenance routing (low-priority non-safety fixes)
  - Supply restocking notifications
- Procedure:
  1. Identify 1–2 properties (pilot hotels) and get manager consent for a 2-week simulation.
  2. Define the automated rules (e.g., "When a checkout is marked and room passes inspection, assign housekeeping and target time = 25 min").
  3. A human operator (team member on the dev/pilot team) will perform the action in the backend and the device UI will show "RelayPoint auto-assigned Housekeeping — expected completion in 25m".
  4. Staff can override the action with one tap, providing a reason (predefined list + free text).
  5. After action completion (or override), trigger a 1-question micro-survey: "Was the auto-action helpful? (Yes / No)"; optional 3-question trust survey at week end.
- Metrics:
  - Acceptance Rate: % of auto-actions left as-is (target >= 60%)
  - Override Rate: % of actions explicitly undone (target < 20%)
  - Time-to-complete comparison (auto vs manual)
  - Qualitative reasons for overrides (categorize)
  - Manager trust score (1–5 Likert) pre/post pilot
- Success Criteria: Acceptance >= 60% and Override < 20% for low-risk tasks; managers report non-decreasing trust and willingness to expand scope.
- Safety & Controls: Start with non-guest-facing tasks only; logging + single-tap undo; notify manager via channel when an auto-action is taken; immediate manual revert allowed.

Playbook (Wizard-of-Oz)

- Consent wording for managers: "RelayPoint will run a two-week simulation where some routine task assignments may be auto-assigned by our system (human-curated) to observe impact on response time and coordination. You can revert any action instantly and will see a record of every automated action. We will capture metrics and short feedback questions."
- Staff notification copy (in-app): "RelayPoint auto-assigned this task — tap to accept or override. If overriding, choose a reason." (Options: Wrong room, Priority changed, Guest needs, Other)
- Operator script (what the human operator does):
  - Monitor triggers and execute action in the platform
  - Log action as `wizard_action=true` in the tracking sheet
  - If staff overrides, note reason and (if necessary) contact manager for clarity
- Logging fields: timestamp, property, room, task_type, action_id, auto_assigned (bool), overridden (bool), override_reason, assigned_to, started_at, completed_at, operator_id
- Post-action micro-survey example: "Was this automated assignment helpful?" {Yes / No} — optional comment box

Experiment 2 — A/B: Suggestion vs Auto-Execute

- Goal: Measure causal effect of auto-execution vs suggestion-only on task resolution time and overrides.
- Procedure:
  1. Randomly assign similar tasks (matching on property/shift/type) to either Suggestion cohort (AI suggests, requires accept) or Auto-execute cohort (system performs action and notifies).
  2. Run for 2–4 weeks, capture same logging fields and micro-survey responses.
- Metrics:
  - Mean time-to-complete (compare cohorts). Target: Auto-exec >=20% faster.
  - Override rate (target auto-exec <25%)
  - Post-action helpfulness score and satisfaction
- Success Criteria: Auto-exec cohort is faster by >=20%, with override <25% and similar or better satisfaction.

Experiment 3 — Explainability & Confidence UI Test

- Goal: Determine whether adding a brief explanation and confidence score increases acceptance and reduces overrides.
- Procedure:
  1. For auto-exec or suggestion actions, present either: (A) No explanation (control) or (B) Short explanation + confidence e.g. "Assigned because 3 guests checked out; estimated cleaning time 25m (confidence 82%)."
  2. Randomize across actions and measure acceptance and override.
- Metrics:
  - Acceptance lift vs control (target +10–15%)
  - Qualitative feedback on explanation usefulness
- Success Criteria: Explanation increases acceptance by >=10%.

Experiment 4 — Pilot Permission & Gradual Scope Increase

- Goal: Measure long-term behavioral commitment by asking managers to opt-in to auto-actions in defined categories and track their willingness to expand scope.
- Procedure:
  1. Offer opt-in configuration UI (or MOU) where managers enable categories: Low-risk only (housekeeping, restock), Medium-risk (maintenance routing), High-risk (guest-facing automation — default off).
  2. Run pilot for 4–8 weeks; gather opt-in rates, revocations, and expansion events.
- Metrics:
  - % of managers who opt in to at least one category (target >= 40%)
  - % who expand scope after 4 weeks (target >= 25%)
  - Revocation rate and rationale
- Success Criteria: At least 40% opt-in to low-risk; 25% expand scope post-positive results.

Implementation & Data Capture

- Tracking storage: simple CSV/Google Sheet or a short pilot database table with the logging fields above.
- Surveys: Short micro-survey after auto-actions; longer end-of-week trust survey (3 items: helpfulness, fairness, willingness to expand; 1–5 Likert).
- Notifications & Undo: Every auto-action must provide a clear, single-tap undo and a visible log for transparency.

Ethical & Legal Notes

- Inform managers and get consent before starting simulations or auto-execution tests. For pilot MOU and deposit offers, include a short clause about what categories are allowed and data retention.
- For any actions that affect payroll, legal, or safety-critical operations, consult legal counsel before automating or simulating automation.

Next steps I can do now:
- Draft the Wizard-of-Oz operator checklist and ready-to-copy manager & staff consent text.
- Create a tracking template (CSV/Google Sheets) and short micro-survey forms.
- Draft the opt-in UI copy and MOU addendum language for pilot permission.

Tell me which of the above you'd like me to prepare next and I'll implement it.