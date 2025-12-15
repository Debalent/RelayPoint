Micro-survey (post-action)

Purpose: Capture immediate staff perception after an automated assignment.

Implementation notes:
- Trigger after task is completed or after an override.
- Keep it one tap + optional short text.
- Include hidden fields in the form: `action_id`, `property_id`, `staff_id`, `timestamp` (populate via URL params or form prefill).

Questions (Typeform/Google Forms copy):
1) Was this automated assignment helpful?  (Single-select)
   - Yes
   - No
2) If No: Why not? (Short text, optional)

Form settings:
- Required: Question 1
- Prefill `action_id` and `property_id` using the trigger
- Keep responses tied to action_id for analysis

Suggested success signals:
- ≥60% "Yes" responses for low-risk tasks
- Common themes in "Why not" responses -> categorize and address rule improvements
