# Scripts

Pure-stdlib Python helpers for the plumbing of Career OS. **No dependencies, no install
step** — they run with any Python 3.9+ (`json`, `pathlib`, `datetime`, `argparse`).
Shared schema constants live in `_schema.py` so the state machine is defined once.

Run them from the repo root.

## `new_opp.py` — scaffold an opportunity  (`/add-opp`)
Creates `pipeline/<id>.json` in the `discovered` state. Won't overwrite an existing file.

```bash
python scripts/new_opp.py --id acme-staff-eng --company "Acme" \
  --title "Staff Software Engineer" --source "Referral — LinkedIn" \
  --location "Remote (US)" --comp "~$250k" --due 2026-06-15
```

## `report.py` — pipeline dashboard  (`/status`)
Reads all `pipeline/*.json`, prints a markdown dashboard (counts by state, top-scored
active opportunities, overdue/due next-actions) and writes `reports/pipeline-<today>.md`.

```bash
python scripts/report.py
```

## `validate_corpus.py` — corpus linter + health report
Lints accomplishment files (frontmatter `{metric, tags, date, source}` + a non-empty
STAR body) and prints a health report: per-file ✓/⚠/✗, totals, date range, and tag
coverage. Frontmatter is parsed by a small hand-rolled parser — no PyYAML. Exits non-zero
if any file is missing a required key or has an empty body. Takes an optional directory
(default `corpus/accomplishments/`).

```bash
python scripts/validate_corpus.py sample-data/accomplishments   # lint the demo set
python scripts/validate_corpus.py                               # lint corpus/accomplishments
```

## `validate.py` — schema check
Validates every `pipeline/*.json`: required keys, valid state, score ints 0–10,
chronological `{state, date}` history whose last entry matches `state`, ISO dates.
Exits non-zero on any failure (handy in CI or a pre-commit hook).

```bash
python scripts/validate.py
```

## `_schema.py`
Shared module — `STATES`, `REQUIRED_KEYS`, date helpers, `load_pipeline()`,
`next_state()`, etc. Not run directly. Edit here if the schema changes, and keep it in
sync with `CLAUDE.md`.
