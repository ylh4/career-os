---
description: Scaffold a new opportunity in the pipeline (state `discovered`).
argument-hint: <id> "<company>" "<title>" "<source>"
---

Add a new opportunity to the pipeline.

Run `scripts/new_opp.py` to create `pipeline/<id>.json` in the `discovered` state. Map the
user's input `$ARGUMENTS` to the flags:

```bash
python scripts/new_opp.py --id <id> --company "<company>" --title "<title>" \
  --source "<source>" [--location "<loc>"] [--comp "<comp>"] [--due YYYY-MM-DD]
```

If the user didn't supply all required fields (`id`, `company`, `title`, `source`), ask for
the missing ones first. The `id` must be a kebab-case slug. After creating it, confirm the
path and suggest `/score <id>` as the next step.
