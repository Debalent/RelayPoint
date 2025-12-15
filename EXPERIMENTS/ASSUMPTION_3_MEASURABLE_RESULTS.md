Assumption #3: Measurable Results (Value Risk)

RelayPoint Elite can deliver quantifiable operational improvements (reduced issue resolution time, improved task completion rates, better coordination) within 30–60 days of first real usage for adopting teams.

Purpose

Define scrappy, low-cost experiments and measurement templates to (1) establish clean baselines, (2) measure short-term impact from Wizard-of-Oz and early automation, (3) run randomized tests where feasible, and (4) produce a simple ROI model for pilot decisions.

Key Metrics (KPIs)
- Time-to-start: time from task creation to staff starting the task (minutes)
- Time-to-complete: time from assignment to completion (minutes)
- Task completion rate: % tasks completed within SLA (e.g., within target time)
- Override rate: % of automated actions reversed by staff
- Task reassignments per task
- Room turnover time (check-out to room-ready, minutes)
- Staff satisfaction / perceived helpfulness (micro-survey)
- Manager trust score (weekly Likert)

Experiment 1 — Baseline Measurement (Required)

Goal: Capture 2–4 weeks of current-state metrics for the tasks you intend to affect.

Plan:
- Select 1–3 properties and 2–3 task types (housekeeping start/completion, maintenance ticket resolution).
- Instrument: Use current PMS, task system logs, and the `wizard_tracking_template.csv` where needed.
- Collect: per-task timestamps, staff ID, task type, priority, and shift.

Deliverables:
- `baseline_data.csv` (sample rows and column names provided below)
- Summary: mean, median, 25/75 percentiles, and control charts for each KPI

Sample baseline CSV columns:
- task_id, task_type, created_at, assigned_at, started_at, completed_at, property_id, staff_id, priority

Experiment 2 — Paired Before/After Pilot (within-property)

Goal: Measure pilot impact by comparing the same KPIs in a pre/post window at the same property.

Plan:
- Run Baseline for 2–4 weeks. Run pilot (WoZ or light automation) for 30–60 days.
- Keep task definitions and data collection consistent.
- Use paired comparisons where possible (same shifts, weekdays) to reduce noise.

Analysis:
- Compute % change in mean time-to-complete and task completion rate.
- Use paired t-test or Wilcoxon signed-rank test for statistical significance (depending on distribution).
- Present percent change with 95% confidence intervals and run charts.

Success Criteria (example):
- Mean time-to-complete reduced by >=20% within 30–60 days OR task completion rate increased by >=10%.

Experiment 3 — A/B Task Cohort Test (randomized)

Goal: Causal test: randomly split similar tasks into Control (manual process) and Treatment (RelayPoint-assisted / auto-assigned).

Plan:
- Randomization: assign new tasks randomly into cohorts. Ensure balance on property, shift, and priority.
- Duration: 2–4 weeks or until N tasks per cohort (see sample size guidance).

Metrics & Analysis:
- Compare mean time-to-complete between cohorts with t-tests (or non-parametric) and compute effect size.
- Monitor override rates and satisfaction.

Sample Size Guidance (rule of thumb):
- For detecting ~20% difference in mean time-to-complete with moderate variance, target 200–400 tasks per condition. If fewer tasks available, run longer or pool across properties.

Experiment 4 — Wizard-of-Oz Impact Test (fast signal)

Goal: Quickly identify high-impact rules and get early behavioral signals using human-in-the-loop automation.

Plan:
- Implement WoZ for selected rules (housekeeping assignment, low-priority maintenance routing) for 1–2 weeks.
- Track the same KPIs and micro-survey responses.

Success: Identify 1–2 rules that produce >=15% reduction in time-to-complete (or large acceptance with low overrides) for prioritization.

Experiment 5 — ROI & Value Modeling

Goal: Translate observed time savings into dollar-savings and room-availability improvements to produce pilot ROI signals.

Inputs:
- Per-task time savings (minutes) from pilot
- Staff hourly labor rates (average)
- Average revenue per available room (RevPAR) and throughput gains from faster room turnovers

Simple ROI Model:
- Labor savings = (time_saved_per_task / 60) * hourly_rate * number_of_tasks_per_period
- Revenue signal = (reduction in room turnover minutes) * (rooms impacted per period) * (RevPAR / average occupancy window)
- Pilot ROI = (estimated annualized benefit) / (annualized cost of licensing + device + pilot operations)

Deliverables: a small Google Sheet (template) with input cells for labor rate, tasks per day, RevPAR, and formulas for labor and revenue signals.

Instrumentation & Data Quality
- Ensure consistent timestamping and timezone handling.
- Tag each task with: experiment_id, cohort, rule_id, staff_id, and task metadata.
- Automatically export raw task logs weekly and snapshot them for audit.

Analysis Templates & Example Formulas
- Acceptance rate: =COUNTIFS(auto_assigned_column,TRUE,overridden_column,FALSE) / COUNTIF(auto_assigned_column,TRUE)
- Mean time-to-complete: =AVERAGE(completed_at - assigned_at)
- Paired percent change: =(mean_baseline - mean_treatment) / mean_baseline

Reporting & Dashboard
- Weekly snapshot chart: time-to-complete run chart (by day)
- Cumulative percent improvement chart
- Table with: baseline mean, pilot mean, delta (%), p-value, sample N

Ethical & Practical Notes
- Keep managers informed and retain consent for measurement and anonymized reporting.
- For any metric tied to payroll or guest safety, ensure explicit written approval before measuring or automating.

Next steps I can do now:
- Draft the `ASSUMPTION_3_MEASURABLE_RESULTS.md` experiment doc (this file), and
- Create a Google Sheets analytics template with KPI calculations and a simple ROI model (recommended next action).

Tell me if you want me to proceed to build the analytics sheet template now.