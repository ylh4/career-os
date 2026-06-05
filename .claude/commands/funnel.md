---
description: Compute funnel conversion, response rate by source, and time-in-state → reports/.
---

Show funnel analytics for the pipeline.

Run `python scripts/funnel.py` (add `--source sample-data` to analyze the demo set). It reads
every `pipeline/*.json` (using the append-only `history[]`), plus the corpus and contacts, and
writes two files:
- `reports/funnel-<today>.md` — **funnel reach & conversion**, **response rate by source**,
  **time-in-state**, and the **active-application count** (out vs. active overall).
- `reports/pipeline-data.js` — the data the dashboard reads.

Then open **`reports/dashboard.html`** in a browser: a self-contained (offline, read-only)
kanban-by-state with a clickable opportunity drawer (score breakdown, state history, raw-JSON
toggle) plus corpus/outreach/funnel charts.

After running, call out the leakiest stage (lowest conversion), the best- and worst-performing
sources, and any state where opportunities sit too long. Keep it operational.
