---
description: Stage a corpus-only tailored resume + cover letter (.docx) with provenance, advance to `tailored`.
argument-hint: <opportunity-id>
---

Tailor a resume and cover letter for the opportunity `$ARGUMENTS`.

First run `python scripts/validate_corpus.py` — **refuse to tailor on a failing corpus.**

Follow `prompts/tailor-resume.md` exactly (it folds in `prompts/cover-letter.md`). Read
`pipeline/$ARGUMENTS.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`, the posting JD
(`pipeline/_raw/$ARGUMENTS.json` and/or `artifacts/$ARGUMENTS/research.md`), and the research
brief if present. Extract the JD's key terms and **mirror the posting's wording only where the
corpus supports it** (ATS-aware); anything unsupported becomes a `GAP:`, never invented. Pick
the next version `N`, then stage, all **only** from the corpus:
- `artifacts/$ARGUMENTS/resume_vN.md`
- `artifacts/$ARGUMENTS/cover_vN.md`
- `artifacts/$ARGUMENTS/provenance.md` (each claim → source file)

Render the deliverables: `python scripts/render_docx.py artifacts/$ARGUMENTS/resume_vN.md
artifacts/$ARGUMENTS/cover_vN.md`. Add the `resume_vN.docx`, `cover_vN.docx`, and
`provenance.md` paths to `artifacts[]`, append `{state: "tailored", date: <today>}` to
`history[]`, set `state` to `tailored`, and update `next_action` (→ `/submit`).

PROVENANCE: every bullet/claim traces to a corpus file; never invent or inflate; emit
`GAP:` for anything the corpus can't support. HUMAN GATE: this only stages — the human
reviews and submits. After writing, run `python scripts/validate.py`.
