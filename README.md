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

## The workflow

```
/scan ─▶ /score ─▶ /tailor ─▶ /submit ─▶ /prefill ─▶ /advance ─▶ /prep
   discover   rank fit    resume+cover   human gate   fill form   move state   interview
   (Apify)    0–100       (.docx+prov)   → applied    (Playwright)             prep (Apify)

   /followups · /touch   keep applications + contacts on cadence
   /status · /funnel      see the pipeline (text) and the live dashboard
```

State machine: `discovered → scored → tailored → applied → screening → interview → offer`
(plus terminals `rejected` / `ghosted` / `withdrawn`). Every transition is append-only history.

## Quickstart

```bash
# Runs out of the box on the fictitious sample candidate (sample-data/).
python scripts/validate_corpus.py sample-data/accomplishments  # lint the demo corpus
python scripts/funnel.py --source sample-data                  # build the dashboard data
open reports/dashboard.html                                    # the visual dashboard

# Go live: copy the sample into your live dirs, then edit to be truthfully about you.
cp sample-data/profile.md corpus/profile.md
cp sample-data/accomplishments/*.md corpus/accomplishments/
cp sample-data/stories/*.md corpus/stories/
mkdir -p contacts && cp sample-data/contacts/*.md contacts/
# (start your pipeline with /scan or /add-opp, not by copying the sample opps)
```

In Claude Code, drive it with slash commands (full catalog in `CLAUDE.md`):

| Command | Does |
|---|---|
| `/scan` | Discover postings via Apify (LinkedIn + Indeed), dedupe, write `discovered` files |
| `/score [id]` | Score fit/comp/visa/remote/growth → 0–100, advance to `scored` |
| `/tailor [id]` | Stage a corpus-only resume + cover (.docx) with a `provenance.md` map |
| `/submit [id]` | Pre-submit checklist → **explicit human yes** → `applied` + follow-up |
| `/prefill [id]` | Playwright fills the ATS form and **stops at submit** |
| `/advance [id] [state]` | Validated, idempotent state transition |
| `/followups` | Overdue application follow-ups **and** contact touches (drafts only) |
| `/touch <slug>` | Log a contact interaction; set the next touch |
| `/prep [id]` | Company research (Apify RAG) + likely questions paired with story hooks |
| `/status` · `/funnel` | Pipeline dashboard (text) · funnel analytics + dashboard data |
| `/add-opp` | Add a posting by hand (manual companion to `/scan`) |

## Dashboard

`reports/dashboard.html` is a single, self-contained, **read-only** viewer (dark/monospace,
offline, no CDN). It renders `window.CAREER_OS` from a generated `pipeline-data.js`:

- **Kanban by state** with a clickable **opportunity drawer** — score breakdown, state-history
  timeline, contacts/artifacts, and a raw-JSON toggle.
- **Charts** for funnel reach/conversion, response-rate-by-source, time-in-state, corpus tag
  coverage, and outreach.
- A **"Live" toggle** (default on) reloads every 30s and preserves the open opportunity via the
  URL hash. A PostToolUse hook regenerates the data whenever the pipeline changes, so the page
  stays current hands-free. (`pipeline-data.sample.js` is committed for the on-clone demo; your
  live `pipeline-data.js` is gitignored.)

## Automation & guardrails

- **Weekly cadence** — `scripts/weekly.sh` runs `/scan` → `funnel.py` → a dated commit
  (commit-only; `WEEKLY_PUSH=1` to push). Wire it via local cron (`0 7 * * 1 …`) or a Claude
  Code Routine.
- **Corpus gate** — a PreToolUse hook (`scripts/guard_corpus.py`) blocks writing a tailored
  resume/cover when `validate_corpus.py` fails — never generate from a broken corpus.
- **Scoped permissions** (`.claude/settings.json`) — allow the Apify/Playwright MCP tools and
  the project scripts; ask before `git push`; writes outside the repo still prompt.

## MCP integrations

- **Apify** — job-board scrapers for `/scan` (LinkedIn + Indeed, capped, deduped) and the RAG
  Web Browser for `/prep` company research.
- **Playwright** — a visible browser for `/prefill`; loads a saved login via
  `scripts/save_session.py` (one-time, manual — no scripted logins, no stored passwords).

## Directory map

```
CLAUDE.md            The kernel: assets, state machine, schema, HARD RULES, commands.
corpus/              Your ground truth — profile.md, accomplishments/, stories/.
pipeline/            One JSON file per opportunity (the state machine); _raw/ = scraped source.
artifacts/<id>/      Generated, staged outputs (resume/cover .md+.docx, provenance, research, prep).
contacts/            One .md per person (recruiters, referrers, recommenders/references).
prompts/             The intelligence — one versioned prompt per capability.
reports/             dashboard.html + generated funnel/status reports + pipeline-data*.js.
scripts/             Python/stdlib helpers + weekly.sh (see scripts/README.md).
sample-data/         A complete fictitious candidate ("Dawit Alemu") for demos and forks.
.claude/             commands/ (slash commands) + settings.json (hooks + permissions).
```

## The two HARD RULES (short version)

1. **Provenance** — no generated fact without a corpus source. Gaps are flagged `GAP:` /
   `[NEEDS SOURCE]`, and every tailored resume ships with a `provenance.md`.
2. **Human Gate** — the OS stages applications; a human reviews and submits. It never sends.

See `CLAUDE.md` for the authoritative statements.
