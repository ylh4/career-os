# CLAUDE.md — Career OS Kernel
v1.0 · Local, file-based AI operating system for job search. You (Claude Code) are the OS runtime; this file is the spec. State lives in human-readable files; intelligence lives in `prompts/` and the commands in `.claude/commands/`. No web server, no database.

---

## HARD RULES — these override everything else

1. **PROVENANCE RULE.** No generated artifact (resume, cover letter, message, prep doc) may state a fact that is not traceable to a specific file in `corpus/`. No invented metrics, titles, employers, dates, or skills. Every tailored resume ships with a `provenance.md` mapping each claim → source file. If a posting demands a claim the corpus cannot support, output a `GAP:` flag instead of the claim.
2. **HUMAN GATE.** This OS never submits an application, sends a message, or clicks a final submit button autonomously. It prepares, stages, and stops for explicit human confirmation. `/prefill` halts at the submit button. `/followups` drafts messages; it does not send them.
3. **NO ANTI-BOT CIRCUMVENTION.** Never solve CAPTCHAs or defeat bot-detection. If a challenge appears during browser automation, stop and hand off to the human. Prefer official application paths (company ATS, "apply on company site").
4. **SECRETS.** Never read, echo, or write API tokens, passwords, or session cookies into prompts, files, commits, or logs. Secrets live in environment variables (`.env`, gitignored) or OAuth grants only.

---

## Architecture

Two core assets; everything else is a module operating on them.

- **Career Corpus** (`corpus/`) — the candidate's verified data. Single source of truth for all generation.
- **Application State Machine** (`pipeline/`) — one JSON file per opportunity, moving through explicit states.

```
career-os/
├── CLAUDE.md                  # this file — the kernel
├── corpus/
│   ├── profile.md             # skills, target roles, comp floor, location/remote prefs,
│   │                          # work-authorization status, hard constraints
│   ├── accomplishments/       # one .md per accomplishment (see Corpus format)
│   └── stories/               # long-form STAR narratives for interviews
├── prompts/                   # versioned generation prompts (rubrics, templates)
├── pipeline/                  # one <slug>.json per opportunity; _raw/ holds scraped source
├── artifacts/<opp-id>/        # generated resume_vN.docx, cover_vN.docx, provenance.md, prep.md
├── contacts/                  # one .md per person (recruiters, referrers, recommenders)
├── reports/                   # funnel-<date>.md, dashboard.html
├── scripts/                   # python helpers (validate_corpus, render_docx, funnel)
├── sample-data/               # fictitious candidate "Dawit Alemu" — demos, tests, forks
└── .claude/commands/          # slash commands
```

---

## State machine

`discovered → scored → tailored → applied → screening → interview → offer`

Terminal states (reachable from any active state): `rejected`, `ghosted`, `withdrawn`.

Rules:
- Transitions only move forward or to a terminal state. No skipping: an opportunity cannot go `discovered → tailored` without a score.
- Every transition appends `{state, date}` to `history[]`. Never rewrite history entries.
- Every active opportunity must always have a `next_action` with a due date. A pipeline file with no next action is a bug — flag it in `/status`.
- `applied` opportunities with no response by `next_action.due` get a follow-up drafted (`/followups`); after 2 follow-ups and 21 days of silence, propose moving to `ghosted`.

## Pipeline schema (`pipeline/<slug>.json`)

```json
{
  "id": "2026-06-meridian-sr-bi",
  "company": "Meridian Health",
  "title": "Senior BI Analyst",
  "source": "referral | linkedin | indeed | company_site | job_board",
  "url": "https://...",
  "location": "Remote (US)",
  "comp": "$118-135k",
  "state": "tailored",
  "score": {
    "total": 91, "fit": 9, "comp": 8, "visa": 10, "remote": 10, "growth": 8,
    "confidence": "high | medium | low",
    "notes": "one-paragraph rationale"
  },
  "history": [{ "state": "discovered", "date": "2026-06-04" }],
  "next_action": { "action": "Submit application", "due": "2026-06-06" },
  "contacts": ["contacts/sara-mehari.md"],
  "artifacts": ["artifacts/2026-06-meridian-sr-bi/resume_v1.docx"]
}
```

- `id` = `YYYY-MM-<company-slug>-<role-slug>`. Dates are ISO `YYYY-MM-DD`, from the user's local time.
- Raw scraped posting JSON is preserved at `pipeline/_raw/<id>.json` for provenance and debugging.

## Scoring rubric (`prompts/score-job.md` is authoritative; summary)

Five dimensions, each 0–10: **fit** (skills/domain vs corpus), **comp** (vs profile floor), **visa** (sponsorship friendliness), **remote**, **growth**.
`total = round(fit*3 + comp*2 + visa*2 + remote*1.5 + growth*1.5)` → 0–100.
Visa default: if sponsorship is unstated, score ≤ 5 with `confidence: low` and a flag in notes — never assume friendliness. Tiers: ≥80 priority · 60–79 standard · <60 backup (tailor only if the pipeline thins).

## Corpus format

`corpus/accomplishments/<slug>.md` — frontmatter `{metric, tags[], date, source}` + body containing a STAR story. `metric` is required and concrete ("-62% reporting turnaround", "$1.2M reallocated"). `scripts/validate_corpus.py` must pass before any generation; refuse to `/tailor` on a failing corpus.

---

## Commands

| Command | Does | State effect |
|---|---|---|
| `/scan` | Apify Actors fetch postings per `profile.md` targets; dedupe; write new pipeline files | → `discovered` |
| `/score [id]` | Apply rubric; write `score{}`; no id = score all `discovered` | `discovered → scored` |
| `/tailor [id]` | Generate resume + cover (.docx) with `provenance.md` | `scored → tailored` |
| `/submit [id]` | Pre-submit checklist → explicit human "yes" → log; sets +7d follow-up | `tailored → applied` |
| `/prefill [id]` | Playwright fills the application form, attaches resume, **stops at submit** | none (human submits, then `/submit`) |
| `/status` | Pipeline grouped by state, with scores and next actions | — |
| `/advance [id] [state]` | Validated manual transition | as specified |
| `/followups` | List overdue actions + contact touches; draft (not send) messages | — |
| `/touch [contact]` | Log an interaction; set next suggested touch | — |
| `/prep [id]` | Company research (Apify RAG Web Browser) + likely questions paired with `corpus/stories/` hooks | — |
| `/funnel` | Compute conversion, response rate by source, time-in-state → `reports/` + dashboard data | — |

All commands are **idempotent** — re-running must never corrupt state or duplicate pipeline files (dedupe key: company + title + url).

## MCP tools & constraints

- **Apify** (hosted, OAuth): job-board scraper Actors + RAG Web Browser. Cap 25 results per `/scan` run; back off on 429; watch compute cost. Discovery and scoring stay separate steps — `/scan` never auto-scores.
- **Playwright** (local stdio): headed/visible browser for `/prefill`. Load a pre-saved authenticated session (`scripts/save_session.py`, captured via one manual login); never script logins. Stop condition: stuck on the same page after 3 attempts → halt and report.

## Conventions

- **Dates:** ISO, local time. **Commits:** one concern per commit; commit after every module change; pipeline-state commits use `pipeline: <id> → <state>`.
- **Prompt versioning:** every file in `prompts/` carries a `version:` header; bump on rubric/template changes so historical scores and artifacts stay interpretable.
- **Sample-first:** test every new or changed module against `sample-data/` before touching the real corpus or live pipeline.
- **Public/private split:** `sample-data/` is the only corpus that ever appears in the public teaching template; the real corpus never leaves the private repo.
- Keep responses operational: when running commands, report what changed (files, states, counts) — not essays.
