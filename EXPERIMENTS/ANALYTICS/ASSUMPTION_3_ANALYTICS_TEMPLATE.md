Assumption #3 Analytics Template — Staffing & Measurable Results

This file describes the analytics CSV template and KPIs for pilots measuring measurable results.

CSV columns (headers):
- date (YYYY-MM-DD)
- property_name
- pilot_id
- metric_occupancy
- metric_checkins
- metric_room_turns
- housekeeping_tasks
- maintenance_tasks
- avg_time_per_task_minutes
- staff_hours_scheduled
- staff_hours_actual
- tasks_completed
- tasks_overdue
- revenue_impact_estimate
- predicted_staff
- actual_staff
- forecast_error
- notes

Suggested use:
- Collect daily/shift-level data during the pilot and append a row per day or shift.
- Use `predicted_staff` to store forecast output and `actual_staff` to store ground truth.
- `forecast_error` = ABS(predicted_staff - actual_staff)

Example CSV header row (copy into a Google Sheet or CSV file):

"date,property_name,pilot_id,metric_occupancy,metric_checkins,metric_room_turns,housekeeping_tasks,maintenance_tasks,avg_time_per_task_minutes,staff_hours_scheduled,staff_hours_actual,tasks_completed,tasks_overdue,revenue_impact_estimate,predicted_staff,actual_staff,forecast_error,notes"

Next steps:
- Use the sheet to compute rolling MAE and MAPE for predicted staffing vs actual staffing.
- Create charts for predicted vs actual staff and for task volume vs forecast error.
- Use the `revenue_impact_estimate` field to model ROI (e.g., reduced overtime, improved occupancy).