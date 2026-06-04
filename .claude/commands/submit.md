---
description: Pre-submit checklist → explicit human confirmation → log the application (tailored → applied).
argument-hint: <opportunity-id>
---

Move the opportunity `$ARGUMENTS` to `applied` — **only** after the human confirms they
submitted it. This is the HUMAN GATE (HARD RULE 2): the OS never submits autonomously.

1. Read `pipeline/$ARGUMENTS.json`. Verify state is `tailored` and that the staged
   artifacts exist (`resume_vN.docx`/`.md`, `cover_vN.docx`/`.md`, `provenance.md`).
2. Print a **pre-submit checklist**: role + company, the resume/cover version, a quick
   provenance sanity check (no `GAP:`/`[NEEDS SOURCE]` left unresolved), comp vs floor, and
   the application URL. Flag anything missing.
3. **Ask the human to confirm they have reviewed and submitted the application.** Do not
   proceed on anything less than an explicit "yes". If they haven't submitted, stop here.
4. On confirmation: append `{state: "applied", date: <today>}` to `history[]`, set `state`
   to `applied`, and set `next_action` to a follow-up **+7 days** out
   (`{action: "Follow up on application", due: <today+7>}`).

Then run `python scripts/validate.py` and report the transition. (`/prefill` can fill the
form for the human, but it always stops at the submit button.)
