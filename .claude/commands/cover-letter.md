---
description: Draft and stage a cover letter for an opportunity (corpus + research only).
argument-hint: <opportunity-id>
---

Draft a cover letter for the opportunity `$ARGUMENTS`.

Follow `prompts/cover-letter.md` exactly. Read `pipeline/$ARGUMENTS.json`,
`corpus/profile.md`, `corpus/accomplishments/*.md`, and `artifacts/$ARGUMENTS/research.md`
if it exists. Write `artifacts/$ARGUMENTS/cover-letter.md` (under ~250 words), add it to
`artifacts[]`, and update `next_action` if appropriate. State does not change here.

PROVENANCE: candidate claims trace to the corpus; company claims trace to the research
brief (or are omitted); mark gaps `[NEEDS SOURCE]`. HUMAN GATE: staged only — the human
reviews and sends.
