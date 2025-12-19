Staffing Forecasting — Feature Spec

Overview
--------
Add a staffing-forecasting tool that predicts required staff counts per shift/role using historical guest and task data. Provide auditable, explainable forecasts with confidence intervals and a manager override flow. Start with a baseline heuristic + LightGBM MVP.

Goals
-----
- Reduce understaffing and overtime by predicting required headcount per role/shift.
- Provide clear, actionable recommendations and explainability for manager trust.
- Rapidly validate with pilot properties in shadow mode.

Data Requirements
-----------------
- Guest check-ins/check-outs (timestamp, room_type, booking_id)
- Occupancy per day/shift
- Task logs (timestamp, task_type, role tag)
- Staff schedules and logged hours (shift id, staff count)
- Optional: local events calendar, weather, booking lead time

Schema Changes / Tables
-----------------------
- forecast_history (property_id, date, shift, occupancy, tasks_count, staff_count, features_json)
- staff_forecasts (property_id, date, shift, role, predicted_headcount, lower_ci, upper_ci, model_version, generated_at)
- staff_forecast_results (property_id, date, shift, role, predicted_headcount, actual_headcount, error)

API
---
- GET /v1/forecast?property_id=&date=&horizon=7&role=housekeeping
  - returns forecasted headcount per shift with confidence intervals and top features.

Backend
-------
- New service: `backend/app/services/forecasting.py` with methods:
  - generate_baseline_forecast(property_id, start_date, horizon, role)
  - train_model(property_id)
  - predict(property_id, date, role)
- Retraining job scheduled daily/weekly; inference endpoint synchronous for small horizons.

Frontend
--------
- Dashboard card showing upcoming 7-day forecast with per-shift bars, confidence bands, and manual adjustment controls.
- Accept manager feedback (accept/reject/override) to capture training labels.

MVP Plan
--------
1. Implement baseline heuristic using rolling averages and day-of-week adjustments.
2. Add LightGBM model trained on lag features and occupancy/task aggregates.
3. Run shadow mode for 2–4 weeks; measure MAE & MAPE; iterate.

Metrics
-------
- MAE / MAPE per shift
- % of shifts under-staffed (actual > predicted + buffer)
- Manager adoption rate of suggestions

Pilot
-----
- Identify 1–3 pilot properties with historical data access.
- Run shadow mode for 2–4 weeks; compare to actuals.

Security & Privacy
------------------
- PII: avoid using guest PII as raw inputs; use aggregated features and hashed IDs.
- Access control: only authorized property managers can view forecasts.

Next steps
----------
- Implement schema migration and forecasting service stub.
- Build ETL to generate `forecast_history` from existing logs.
- Create initial endpoint and small frontend placeholder.

Files to add
------------
- `backend/app/services/forecasting.py`
- Alembic migration for `forecast_history` and `staff_forecasts`
- `notebooks/forecasting_baseline.ipynb`
- Frontend components and storybook stories
- Tests: unit + integration + minimal E2E
