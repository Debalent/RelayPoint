Logging Script Notes — Lightweight CSV Logger (annotated)

Goal: Provide a simple Python script to append a hand-raiser row to `PROSPECT_TEMPLATE.csv` when a DM or comment is processed.

Concept (simple, reliable)
- Use a script `scripts/log_handraiser.py` that accepts CLI args: name, title, company, location, linkedin, email, source, contacted_date, response, next_action
- The script appends a single CSV row preserving existing headers
- Use with local manual invocation or wire to a Zapier/Make webhook that posts into a small Node/Python HTTP endpoint which runs this script

Example snippet (Python):

```python
import csv
import sys
from datetime import date

row = {
  'name': sys.argv[1],
  'title': sys.argv[2],
  'company': sys.argv[3],
  'company_size': sys.argv[4],
  'location': sys.argv[5],
  'linkedin_url': sys.argv[6],
  'email': sys.argv[7],
  'source': sys.argv[8],
  'contacted_date': date.today().isoformat(),
  'response': 'hand-raised',
  'booked_date': '',
  'deposit_status': '',
  'notes': sys.argv[9]
}

with open('EXPERIMENTS/OUTREACH/PROSPECT_TEMPLATE.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    writer.writerow(row)
```

Notes
- Validate no duplicate rows by matching linkedin_url or email before appending
- Use small wrapper or a GitHub Action if you want commits to be recorded automatically (but be cautious about concurrent writes to CSV in Git)
- For production: use a small DB-backed endpoint rather than committing CSVs

If you want, I can implement the `scripts/log_handraiser.py` script and a tiny HTTP wrapper to accept webhook calls (and optionally a Zapier instruction doc).