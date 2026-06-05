---
version: 1.0
---

# Prompt: Company Research

**Invoked by:** `/prep [id]` (the company brief is built as part of interview prep).
**Reads:** `pipeline/<id>.json` (company, title, source)
**Writes:** `artifacts/<id>/research.md`; registers it in `artifacts[]`.
**Research engine:** the **Apify RAG Web Browser** Actor — `apify/rag-web-browser` (call it via
the Apify MCP `apify--rag-web-browser` tool, or `call-actor` with `apify/rag-web-browser`).
Query it for the company + role (e.g. "<Company> careers / funding / product / recent news");
it returns page content you cite. Fall back to plain web search/fetch only if needed. Watch
compute cost; a couple of focused queries is plenty.

Produce a structured, **cited** research brief on the company and role. This brief becomes
the provenance source for company facts used by `/tailor` (cover letter) and `/prep`.

## Sections
1. **Overview** — what they do, stage/size, funding or public status, business model.
2. **Product & tech** — main products; known tech stack relevant to the role.
3. **Recent signals** — news, launches, leadership changes, layoffs, hiring trends (last
   ~12 months). Date each item.
4. **Role context** — how this role likely fits; the team, the probable mandate.
5. **Culture & comp signals** — values, on-call/work-style reputation, public comp data
   (Levels.fyi / Glassdoor ranges) — clearly labeled as third-party estimates.
6. **Talking points** — 3–5 specific, true hooks the candidate can use, each tied to a
   `profile.md` priority.
7. **Open questions / unknowns** — what could not be verified.

## Sourcing — the hard rule
- **Every non-obvious claim gets an inline source** (URL or tool result) with a date.
- Distinguish **verified facts** from **inferences** — label inferences as such.
- If a claim can't be sourced, put it under *Open questions*, not the factual sections.
- Do not pass speculation downstream as fact; `/tailor` (cover letter) and `/prep` will
  treat this brief as ground truth for company claims.

## Output
Write `artifacts/<id>/research.md` with a `## Sources` list at the bottom. Add the path to
`artifacts[]` and update `next_action`. State is unchanged by this command.
