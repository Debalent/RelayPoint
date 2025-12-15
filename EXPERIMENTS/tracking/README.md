Tracking sheet README

This folder contains templates for tracking Wizard-of-Oz experiments and surveys.

Files:
- `wizard_tracking_template.csv` — CSV template with example rows (action logs). Use as the base ingestion sheet or import into Google Sheets.
- `micro_survey.md` — Post-action micro-survey questions and implementation notes.
- `weekly_manager_trust_survey.md` — Weekly manager trust survey and suggested copy.

Quick analysis formulas (Google Sheets):
- Total auto-actions: =COUNTIF(C:C, "true")  // if column C is auto_assigned
- Acceptance rate: =COUNTIFS(C:C, "true", D:D, "false") / COUNTIF(C:C, "true")  // D is overridden
- Override rate: =COUNTIFS(C:C, "true", D:D, "true") / COUNTIF(C:C, "true")

Notes:
- Use a separate sheet/tab for raw responses, processed metrics, and charts.
- Tag rows with `wizard_run_id` and `cohort` if running A/B tests.
- Export weekly snapshots for audit and for sharing with managers.
