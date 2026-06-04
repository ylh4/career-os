---
description: Render the pipeline dashboard (counts by state, top-scored, due actions).
---

Show the pipeline status.

Run `python scripts/report.py`. It prints the dashboard and writes
`reports/pipeline-<today>.md` (counts by state, top-scored active opportunities, and
overdue/due `next_action`s).

After running, briefly highlight what needs attention: any ⚠️ OVERDUE actions first, then
the highest-scored opportunities that haven't advanced. If `$ARGUMENTS` names a specific
opportunity, also summarize that entry's state, score, and next action.
