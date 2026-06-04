# Scripts

Python helpers for the plumbing of Career OS. The pipeline helpers (`new_opp`, `report`,
`funnel`, `validate`, `validate_corpus`) are pure standard library; only `render_docx.py`
needs a dependency (`python-docx`, installed in the project venv). Shared schema constants
live in `_schema.py` so the state machine is defined once.

Run them from the repo root.

## `new_opp.py` — scaffold an opportunity  (`/add-opp`, `/scan`)
Creates `pipeline/<id>.json` in the `discovered` state. Won't overwrite an existing file.

```bash
python scripts/new_opp.py --id 2026-06-acme-staff-eng --company "Acme" \
  --title "Staff Software Engineer" --source referral \
  --url "https://..." --location "Remote (US)" --comp "~$250k" --due 2026-06-15
```

The `id` follows the kernel convention `YYYY-MM-<company>-<role>`.

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
Validates every `pipeline/*.json`: required keys, valid state, score block (dimensions
ints 0–10, weighted `total` 0–100, `confidence` high|medium|low), chronological
`{state, date}` history whose last entry matches `state`, ISO dates. Exits non-zero on any
failure (handy in CI or a pre-commit hook).

```bash
python scripts/validate.py
```

## `render_docx.py` — markdown → .docx  (`/tailor`)
Renders a staged markdown artifact (resume/cover letter) to the `.docx` deliverable that
gets uploaded to an ATS. The `.md` sources and `provenance.md` are the tracked, reviewable
artifacts; `.docx` exports are gitignored and regenerated on demand. Needs `python-docx`.

```bash
python scripts/render_docx.py artifacts/<id>/resume_v1.md artifacts/<id>/cover_v1.md
```

## `funnel.py` — funnel analytics  (`/funnel`)
Reads every `pipeline/*.json` (via the append-only `history[]`) and writes
`reports/funnel-<today>.md`: funnel reach & stage conversion, response rate by source, and
average time-in-state.

```bash
python scripts/funnel.py
```

## `_schema.py`
Shared module — `STATES`, `REQUIRED_KEYS`, date helpers, `load_pipeline()`,
`next_state()`, etc. Not run directly. Edit here if the schema changes, and keep it in
sync with `CLAUDE.md`.
