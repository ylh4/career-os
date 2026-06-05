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

The `id` follows the kernel convention `YYYY-MM-<company>-<role>`. The entry skeleton is
defined once in `_schema.make_entry()` and shared with `scan_ingest.py`.

## `scan_ingest.py` — ingest scraped postings  (`/scan`)
The deterministic half of `/scan`. The `/scan` command calls Apify Actors via MCP and writes
a normalized batch of postings to a JSON file; this script dedupes them against the existing
pipeline (by company+title+url), scaffolds new `pipeline/<id>.json` files in `discovered`, and
saves each raw posting to `pipeline/_raw/<id>.json` for provenance. It never scores. Idempotent
— re-running creates nothing new. `--dry-run` reports decisions without writing; `--cap` bounds
how many new opportunities are created.

```bash
python scripts/scan_ingest.py --input pipeline/_raw/_incoming.json --cap 25 --dry-run
python scripts/scan_ingest.py --input pipeline/_raw/_incoming.json --cap 25
```

## `report.py` — pipeline dashboard  (`/status`)
Reads all `pipeline/*.json`, prints a markdown dashboard (counts by state, the pipeline
grouped by state with each opportunity's score + next_action, top-scored active, and
overdue/due next-actions) and writes `reports/pipeline-<today>.md`.

```bash
python scripts/report.py
```

## `advance.py` — validated state transition  (`/advance`, `/submit`)
Transitions `pipeline/<id>.json` to a new state with the kernel rules enforced: forward one
step or to a terminal state (`rejected`/`ghosted`/`withdrawn`); no skipping, no backward, no
leaving a terminal. Appends `{state, date: today}` to `history[]` (append-only) and sets a
sensible `next_action` with a date from today (e.g. `applied` → +7-day follow-up). Idempotent
(advancing to the current state is a no-op). Advancing into `applied` requires `--confirm`
(the human gate; `/submit` passes it).

```bash
python scripts/advance.py <id> [target_state] [--confirm] [--action "…"] [--due YYYY-MM-DD]
```

## `followups.py` — due/overdue list  (`/followups`)
Lists every active opportunity whose `next_action.due` is today or earlier (excludes terminal
states, oldest-first, flagged OVERDUE/due today). Read-only.

```bash
python scripts/followups.py
```

## `save_session.py` — capture a login session  (`/prefill`)
You run this once, by hand, for sites that require a login. It opens a visible browser using
the persistent profile `.auth/pw-profile` (the same `--user-data-dir` the Playwright MCP uses),
you log in yourself, and the cookies persist there so `/prefill` finds you signed in. No
passwords are ever scripted or echoed; `.auth/` is gitignored. One-time setup:
`pip install playwright && playwright install chromium` (only needed for login-gated sites).

```bash
python scripts/save_session.py https://www.linkedin.com/login
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
