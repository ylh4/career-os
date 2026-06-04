---
description: Produce a cited company-research brief for an opportunity.
argument-hint: <opportunity-id>
---

Research the company for the opportunity `$ARGUMENTS`.

Follow `prompts/company-research.md` exactly. Read `pipeline/$ARGUMENTS.json` for the
company/title, then use web search/fetch and MCP tools to gather current facts. Write
`artifacts/$ARGUMENTS/research.md` with the structured sections (overview, product & tech,
recent signals, role context, culture & comp signals, talking points, open questions) and a
`## Sources` list. Add the path to `artifacts[]` and update `next_action`.

SOURCING: every non-obvious claim gets an inline dated source; label inferences as
inferences; unverifiable claims go under *Open questions*, not the factual sections. This
brief is the provenance source for company facts used by `/cover-letter` and
`/interview-prep`.
