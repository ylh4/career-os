# Career OS — Kernel

Career OS is a **local, file-based AI operating system for running a job search.**
There is no web server and no database. **Intelligence lives in prompts and this file;
state lives in human-readable files** (markdown + JSON). Claude Code is the runtime:
slash commands invoke prompts that read the *corpus* and *pipeline* and write *artifacts*.

If you (the model) are reading this, treat it as the operating contract. Every command
and prompt in this repo inherits the rules below.

---

## The Two Core Assets

### 1. Career Corpus — the candidate's ground truth (`corpus/`)
The single source of truth about the candidate. Generated artifacts may only draw from here.

- `corpus/profile.md` — identity, work authorization / visa status, location & remote
  preferences, compensation targets, role targets, hard constraints.
- `corpus/accomplishments/*.md` — **one verifiable achievement per file**, each with a
  concrete metric, a date, and a provenance source. These are the atoms of every resume
  bullet and cover-letter claim.
- `corpus/stories/*.md` — STAR narratives (Situation, Task, Action, Result) for behavioral
  interviews.

`sample-data/` holds a complete *fictitious* candidate so the system runs on first clone.
To go live, copy `sample-data/` content into `corpus/` (and `pipeline/`) and edit.

### 2. Application State Machine — the pipeline (`pipeline/`)
Every opportunity is **one JSON file**: `pipeline/<id>.json`. It moves through states:

```
discovered → scored → tailored → applied → followed_up → screening → interview → offer
                                                                              │
                              ┌───────────────────────────────────────────────┤
                              ▼                                                ▼
                          rejected                                         ghosted
```

- **discovered** — captured, not yet evaluated.
- **scored** — fit/comp/visa/remote/growth scored (`/score`).
- **tailored** — resume/letter staged in `artifacts/<id>/` (`/tailor`, `/cover-letter`).
- **applied** — human reviewed and submitted (HUMAN GATE — see below).
- **followed_up** — follow-up sent (`/follow-up`).
- **screening** — recruiter / phone screen in progress.
- **interview** — interview loop in progress.
- **offer** — offer received.
- **rejected** / **ghosted** — terminal branches, reachable from any active state.

Every transition appends to `history[]`. Commands **never silently overwrite** state.

---

## Pipeline JSON Schema

One file per opportunity at `pipeline/<id>.json`:

```json
{
  "id": "acme-staff-eng-2026",
  "company": "Acme",
  "title": "Staff Software Engineer",
  "source": "Referral — LinkedIn (Jordan Patel)",
  "location": "Remote (US)",
  "comp": { "min": 230000, "max": 280000, "currency": "USD", "equity": "0.05%", "notes": "base+bonus est." },
  "state": "scored",
  "score": {
    "total": 0,
    "fit": 0,
    "comp": 0,
    "visa": 0,
    "remote": 0,
    "growth": 0,
    "notes": "string — rationale, must cite corpus for fit claims"
  },
  "history": [
    { "state": "discovered", "date": "2026-05-20" },
    { "state": "scored", "date": "2026-05-21" }
  ],
  "next_action": { "action": "Tailor resume", "due": "2026-05-25" },
  "contacts": [
    { "name": "Jordan Patel", "role": "Referrer", "email": "", "notes": "Eng manager, met at conf" }
  ],
  "artifacts": [ "artifacts/acme-staff-eng-2026/resume.md" ]
}
```

Field notes:
- `id` — kebab-case slug, unique, used as the filename and the `artifacts/<id>/` folder.
- `comp` — may be a plain string (`"~$250k"`) or the object form shown above.
- `score` — integers 0–10 per dimension; `total` is the weighted roll-up (see
  `prompts/score-job.md`); `notes` carries rationale.
- `history` — append-only, chronological, each entry `{state, date}` with ISO dates.
- `next_action` — the single next thing to do and its due date (drives `/status`).
- `artifacts` — repo-relative paths to staged files for this opportunity.

---

## TWO HARD RULES

These are non-negotiable. Every prompt and command restates them; they hold from any entry point.

### RULE 1 — PROVENANCE
**No generated artifact may state a fact that is not traceable to a
`corpus/accomplishments/` file (or `corpus/profile.md`).** No invented metrics, titles,
employers, dates, or scope. If a desired claim has no corpus source, the artifact must
either omit it or insert a visible `[NEEDS SOURCE]` marker for the human to resolve.
A resume bullet without a corpus atom behind it is a bug, not a flourish.

### RULE 2 — HUMAN GATE
**The OS never submits an application autonomously.** It prepares and *stages* artifacts
under `artifacts/<id>/`. A human reviews and triggers the final submit. State may advance
to `applied` **only after explicit human confirmation** that they submitted. The OS
drafts emails and forms; it does not send or click submit on the candidate's behalf.

---

## Slash Commands

Prompt-backed (the "intelligence"):

| Command | Backed by | Does |
|---|---|---|
| `/score <id>` | `prompts/score-job.md` | Scores fit/comp/visa/remote/growth, writes `score{}`, advances `discovered → scored`. |
| `/tailor <id>` | `prompts/tailor-resume.md` | Stages a corpus-only resume at `artifacts/<id>/resume.md`, advances `→ tailored`. |
| `/cover-letter <id>` | `prompts/cover-letter.md` | Stages a cover letter from corpus + research. |
| `/interview-prep <id>` | `prompts/interview-prep.md` | Builds a prep doc from `stories/` + the role + research. |
| `/research <id>` | `prompts/company-research.md` | Produces a cited company brief. |

Pipeline operations (the "plumbing", stdlib Python helpers in `scripts/`):

| Command | Backed by | Does |
|---|---|---|
| `/add-opp` | `scripts/new_opp.py` | Scaffolds a new `pipeline/<id>.json` in `discovered`. |
| `/status` | `scripts/report.py` | Renders the pipeline dashboard to `reports/` and stdout. |
| `/advance <id>` | (kernel logic) | Moves an opportunity to its next state; appends `history[]`; updates `next_action`. Enforces HUMAN GATE before `applied`. |
| `/follow-up <id>` | `prompts/` + kernel | Drafts a follow-up message and sets the next `next_action`. |

---

## Standard Workflow

```
discover → /score → /research → /tailor → /cover-letter → [HUMAN reviews & submits]
   → /advance (to applied) → /follow-up → screening → /interview-prep → interview → offer
```

1. Capture an opportunity with `/add-opp` (or by hand) → `discovered`.
2. `/score` it; low scores can be parked or marked `rejected`.
3. `/research` the company; `/tailor` the resume and `/cover-letter` — all corpus-only.
4. **Human reviews the staged artifacts and submits the application.**
5. `/advance` to `applied` (only after the human confirms submission).
6. `/follow-up` on the cadence; `/interview-prep` when a loop is scheduled.
7. Keep `next_action` current so `/status` always shows the true next move.

## Conventions
- Dates are ISO `YYYY-MM-DD`. Today is supplied by the environment; never guess.
- State mutations are append-only to `history[]`.
- Python helpers are pure standard library — no install step.
- Keep the corpus factual and the pipeline current; everything else is derived.
