# Career OS

A **local, file-based AI operating system for running a job search.** No web server,
no database — just markdown and JSON, driven by Claude Code. The intelligence lives in
`prompts/` and `CLAUDE.md`; your job-search *state* lives in human-readable files you own
and can read, diff, and back up.

> Read [`CLAUDE.md`](./CLAUDE.md) first — it is the kernel and defines the rules every
> command obeys, including the two HARD RULES: **Provenance** and the **Human Gate**.

## Why

Job search generates a pile of tailored resumes, cover letters, research notes, and
pipeline status that usually ends up scattered across docs, spreadsheets, and email. Career
OS keeps all of it as flat files in one repo:

- **Career Corpus** (`corpus/`) — your ground-truth accomplishments, profile, and stories.
- **Pipeline** (`pipeline/`) — one JSON file per opportunity, moving through a state machine.
- **Artifacts** (`artifacts/`) — generated resumes/letters/prep, staged for *you* to submit.

Two rules keep it honest: nothing is generated that isn't traceable to your corpus
(**Provenance**), and the OS never submits anything for you (**Human Gate**).

## Quickstart

```bash
# 1. Clone / fork this repo. It runs out of the box on fictitious sample data.
# 2. Try the helpers (stdlib only, except render_docx which uses python-docx):
python scripts/report.py                 # pipeline dashboard
python scripts/funnel.py                  # funnel analytics
python scripts/new_opp.py --id 2026-06-acme-staff-eng --company "Acme" \
  --title "Staff Engineer" --source linkedin --url "https://..."
python scripts/validate.py               # validate all pipeline/*.json

# 3. Go live: replace the demo data with your own.
cp -r sample-data/profile.md corpus/profile.md
cp -r sample-data/accomplishments/* corpus/accomplishments/
cp -r sample-data/stories/* corpus/stories/
mkdir -p contacts && cp -r sample-data/contacts/* contacts/
cp -r sample-data/pipeline/* pipeline/        # optional: start from the examples
# then edit corpus/ to be truthfully about you.
```

In Claude Code, use the slash commands (see `CLAUDE.md` for the full catalog):
`/scan`, `/score`, `/tailor`, `/submit`, `/prefill`, `/status`, `/advance`, `/followups`,
`/touch`, `/prep`, `/funnel` (plus `/add-opp` to add a posting by hand).

## Directory map

```
CLAUDE.md            The kernel: assets, state machine, schema, HARD RULES, commands.
README.md            This file.
corpus/              Your ground truth.
  profile.md         Identity, visa, location/remote, comp + role targets, constraints.
  accomplishments/   One verifiable achievement per file (metric + date + source).
  stories/           STAR behavioral-interview narratives.
prompts/             The intelligence — one prompt per capability.
pipeline/            One JSON file per opportunity (the state machine).
artifacts/           Generated, staged outputs per opportunity (artifacts/<id>/...).
contacts/            One .md per person (recruiters, referrers), linked from pipeline files.
reports/             Pipeline dashboards + funnel reports written by scripts/.
sample-data/         A complete fictitious candidate for demos and forks.
scripts/             Python helpers (validate, report, funnel, new_opp, render_docx).
.claude/commands/    Slash-command definitions.
```

## The two HARD RULES (short version)

1. **Provenance** — no generated fact without a corpus source. Gaps are marked `[NEEDS SOURCE]`.
2. **Human Gate** — the OS stages applications; a human reviews and submits. It never sends.

See `CLAUDE.md` for the authoritative statements.
