---
description: Log an interaction with a contact and set the next suggested touch.
argument-hint: "<contact-slug>  [note]"
---

Log a networking interaction with the contact `$ARGUMENTS`.

Run the deterministic helper (it creates `contacts/<slug>.md` if needed, appends a dated entry
to the append-only `## Interactions` log, and stamps `last_touch` = today + `next_touch` =
today + cadence):

```bash
python scripts/touch.py <slug> --note "<what happened>" \
  [--cadence N] [--name "…"] [--role "…"] [--company "…"] [--relationship referrer|recruiter|recommender|hiring-manager|peer]
```

- Default cadence is 28 days; use `--cadence` for a tighter loop (e.g. 7–14 after a screen).
- For a brand-new contact, pass `--name/--role/--company/--relationship` so the frontmatter is
  complete (the loader and `/followups` rely on it).
- The same record doubles as a **reference / recommendation-letter recommender** tracker — set
  `--relationship recommender` and log whether they've agreed and when you last nudged them.

PROVENANCE: log only what actually happened — never invent commitments. Then report the logged
interaction and the next-touch date.
