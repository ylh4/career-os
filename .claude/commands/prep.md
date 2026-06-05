---
description: Build an interview prep doc (company research + likely questions paired with story hooks).
argument-hint: <opportunity-id>
---

Prepare for the interview at the opportunity `$ARGUMENTS`.

Two steps, both following the prompts exactly:

1. **Company brief.** If `artifacts/$ARGUMENTS/research.md` is missing or stale, follow
   `prompts/company-research.md`: research the company with the **Apify RAG Web Browser**
   Actor (`apify/rag-web-browser`, via the Apify MCP `apify--rag-web-browser` tool or
   `call-actor`) — a couple of focused queries on the company + role — and write
   `artifacts/$ARGUMENTS/research.md` with a `## Sources` list. Every non-obvious claim gets a
   dated source; unverifiable claims go under *Open questions*.
2. **Prep doc.** Follow `prompts/interview-prep.md`: read `pipeline/$ARGUMENTS.json`,
   `corpus/stories/*.md`, `corpus/accomplishments/*.md`, `corpus/profile.md`, and the brief.
   Write `artifacts/$ARGUMENTS/prep.md`: a cited role/company snapshot; **likely questions,
   each paired with an answer hook** — behavioral questions matched to a `corpus/stories/` file
   by its `themes` (cite the story + its Result metric), technical/role questions hooked to a
   specific `accomplishments/` file; a tight STAR bank (metrics verbatim); strong questions to
   ask them; and an honest risks/gaps section (mark unsupported asks `GAP:`).

Add `research.md` and `prep.md` to `artifacts[]` and update `next_action` (e.g. the
interview date). PROVENANCE: stories/metrics come from the corpus verbatim; company facts
from the brief or omitted. Don't coach claims the candidate can't back. State is set via
`/advance`, not here. Then run `python scripts/validate.py`.
