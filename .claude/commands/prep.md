---
description: Build an interview prep doc (company research + likely questions paired with story hooks).
argument-hint: <opportunity-id>
---

Prepare for the interview at the opportunity `$ARGUMENTS`.

Two steps, both following the prompts exactly:

1. **Company brief.** If `artifacts/$ARGUMENTS/research.md` is missing or stale, follow
   `prompts/company-research.md`: use the Apify RAG Web Browser (and web search/fetch) to
   gather current, **cited** facts and write `artifacts/$ARGUMENTS/research.md` with a
   `## Sources` list. Every non-obvious claim gets a dated source; unverifiable claims go
   under *Open questions*.
2. **Prep doc.** Follow `prompts/interview-prep.md`: read `pipeline/$ARGUMENTS.json`,
   `corpus/stories/*.md`, `corpus/accomplishments/*.md`, `corpus/profile.md`, and the brief.
   Write `artifacts/$ARGUMENTS/prep.md`: role/company snapshot (cited), likely questions
   mapped to `stories/` files, a STAR bank (metrics verbatim), questions to ask them, and an
   honest risks/gaps section.

Add `research.md` and `prep.md` to `artifacts[]` and update `next_action` (e.g. the
interview date). PROVENANCE: stories/metrics come from the corpus verbatim; company facts
from the brief or omitted. Don't coach claims the candidate can't back. State is set via
`/advance`, not here. Then run `python scripts/validate.py`.
