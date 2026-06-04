---
description: Scaffold a new opportunity in the pipeline (state `discovered`).
argument-hint: <id> "<company>" "<title>" "<source>"
---

Add a single opportunity to the pipeline by hand — the manual companion to `/scan` (use
this when you have a posting Apify didn't surface, e.g. a referral).

Run `scripts/new_opp.py` to create `pipeline/<id>.json` in the `discovered` state. Map the
user's input `$ARGUMENTS` to the flags:

```bash
python scripts/new_opp.py --id <id> --company "<company>" --title "<title>" \
  --source "<source>" [--url "<url>"] [--location "<loc>"] [--comp "<comp>"] [--due YYYY-MM-DD]
```

If the user didn't supply all required fields (`id`, `company`, `title`, `source`), ask for
the missing ones first. The `id` follows the kernel convention `YYYY-MM-<company>-<role>`
(e.g. `2026-06-acme-staff-eng`). After creating it, confirm the path and suggest
`/score <id>` as the next step.
