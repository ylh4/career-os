---
description: Build an interview prep doc from stories, the role, and company research.
argument-hint: <opportunity-id>
---

Build interview prep for the opportunity `$ARGUMENTS`.

Follow `prompts/interview-prep.md` exactly. Read `pipeline/$ARGUMENTS.json`,
`corpus/stories/*.md`, `corpus/accomplishments/*.md`, `corpus/profile.md`, and
`artifacts/$ARGUMENTS/research.md` if present. Write `artifacts/$ARGUMENTS/interview-prep.md`
with: role/company snapshot (cited), likely questions mapped to story files, a STAR bank,
questions to ask them, and an honest risks/gaps section. Add it to `artifacts[]` and update
`next_action`.

PROVENANCE: stories and metrics come from the corpus verbatim; company facts from the
research brief or omitted. Don't coach claims the candidate can't back.
