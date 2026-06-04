---
description: Stage a corpus-only tailored resume for an opportunity and advance to `tailored`.
argument-hint: <opportunity-id>
---

Tailor a resume for the opportunity `$ARGUMENTS`.

Follow `prompts/tailor-resume.md` exactly. Read `pipeline/$ARGUMENTS.json`,
`corpus/profile.md`, and `corpus/accomplishments/*.md`. Write
`artifacts/$ARGUMENTS/resume.md` built **only** from the corpus, including a
`## Provenance map`. Add the path to `artifacts[]`, append `{state: "tailored", date:
<today>}` to `history[]`, set `state` to `tailored`, and update `next_action`.

PROVENANCE: every bullet traces to a corpus file; never invent or inflate; mark gaps
`[NEEDS SOURCE]`. HUMAN GATE: this only stages the resume — the human reviews and submits.
After writing, run `python scripts/validate.py`.
