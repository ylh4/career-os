---
description: Pre-submit checklist → explicit human confirmation → log the application (tailored → applied).
argument-hint: <opportunity-id>
---

Move the opportunity `$ARGUMENTS` to `applied` — **only** after the human confirms they
submitted it. This is the HUMAN GATE (HARD RULE 2): the OS never submits autonomously.

1. Read `pipeline/$ARGUMENTS.json`. If state is already `applied`, say so and stop
   (idempotent — nothing to do). If state is not `tailored`, refuse and explain. Verify the
   staged artifacts exist (`resume_vN.docx`/`.md`, `cover_vN.docx`/`.md`, `provenance.md`).
2. Print a **pre-submit checklist**: role + company, the resume/cover version, a quick
   provenance sanity check (call out any `GAP:`/`[NEEDS SOURCE]` left unresolved), comp vs
   floor, and the application URL. Flag anything missing.
3. **Ask the human to confirm they have reviewed and submitted the application.** Do not
   proceed on anything less than an explicit "yes". If they haven't submitted, stop here.
4. On explicit confirmation only, make the transition deterministically (this is the one path
   allowed to enter `applied`; it appends history with today's date and sets the +7-day
   follow-up):
   ```bash
   python scripts/advance.py $ARGUMENTS applied --confirm
   ```

Then run `python scripts/validate.py` and report the transition. (`/prefill` can fill the
form for the human, but it always stops at the submit button.)
