---
description: Use Playwright to fill the application form and attach the resume — stops at the submit button.
argument-hint: <opportunity-id>
---

Pre-fill the application form for `$ARGUMENTS`. **You must stop at the submit button**
(HARD RULE 2 — the human submits). Then they run `/submit`.

1. Read `pipeline/$ARGUMENTS.json` for the `url` and the staged `artifacts/$ARGUMENTS/`
   resume/cover deliverables.
2. Use the **Playwright** MCP (headed/visible browser). Load the pre-saved authenticated
   session from `scripts/save_session.py` — **never script a login** and never read or echo
   cookies/tokens (HARD RULE 4). If no session exists, stop and ask the human to log in once.
3. Navigate to the posting's apply page (prefer the official ATS / "apply on company site").
   Fill fields from `corpus/profile.md` and the staged resume; attach `resume_vN.docx`.
4. **Do not click submit.** Leave the completed form for the human to review and submit.

Stop conditions: if a CAPTCHA or bot-detection challenge appears, **halt and hand off** (do
not attempt to solve it — HARD RULE 3). If stuck on the same page after 3 attempts, halt and
report. State does not change here — after the human submits, they run `/submit $ARGUMENTS`.
