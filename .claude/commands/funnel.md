---
description: Compute funnel conversion, response rate by source, and time-in-state → reports/.
---

Show funnel analytics for the pipeline.

Run `python scripts/funnel.py`. It reads every `pipeline/*.json` (using the append-only
`history[]`) and writes `reports/funnel-<today>.md` with:
- **Funnel reach & conversion** — how many opportunities reached each linear state and the
  stage-to-stage conversion rate, plus terminal outcomes.
- **Response rate by source** — of opportunities that reached `applied`, the share that drew
  a real response (reached `screening`+), grouped by `source`.
- **Time-in-state** — average days between entering a state and the next transition.

After running, call out the leakiest stage (lowest conversion), the best- and worst-
performing sources, and any state where opportunities sit too long. Keep it operational.
