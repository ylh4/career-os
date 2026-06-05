---
description: Use Playwright to fill the application form and attach the resume — stops at the submit button.
argument-hint: <opportunity-id>  (or a file:// URL to the practice form for testing)
---

Pre-fill the application form for `$ARGUMENTS`. **You must stop at the submit button** (HARD
RULE 2 — the human submits). Then they run `/submit`.

1. **Resolve the target.** If `$ARGUMENTS` is a `file://`/`http(s)://` URL, use it directly
   (testing). Otherwise read `pipeline/$ARGUMENTS.json` for the `url` and confirm state is
   `tailored` (or later) and `artifacts/$ARGUMENTS/resume_vN.docx` exists (use the highest `vN`).
2. **Session.** The Playwright MCP runs with a persistent profile (`.auth/pw-profile`), so a
   previously captured login is reused automatically. Never script a login and never read or
   echo cookies/tokens (HARD RULE 4). If the page demands login and you're not signed in,
   **STOP** and tell the human to run `python scripts/save_session.py <login-url>` once.
3. **Open & read.** `browser_navigate` to the URL — prefer the official ATS / "Apply on company
   site" path over third-party sites whose terms prohibit automation. `browser_snapshot` to
   read the form's fields.
4. **Fill.** Map fields from `corpus/profile.md` (name, email, phone, location, LinkedIn/site,
   etc.) and fill via `browser_fill_form` (or `browser_type` per field). Attach the resume with
   `browser_file_upload` (the `resume_vN.docx`). Only fill fields you can populate truthfully
   from the corpus; leave unknowns blank for the human.
5. **Hand off.** `browser_take_screenshot`, then print a summary of **every field you filled +
   the file attached + anything left blank**. Leave the browser open for the human to review
   and submit.

**Hard constraints (do not violate):**
- **Never click the final submit/apply button** — `/prefill` always stops there (HUMAN GATE).
- **Never solve a CAPTCHA or defeat an anti-bot challenge.** If one appears, halt and hand off
  to the human (HARD RULE 3).
- **Anti-runaway stop:** if you're still on the same page after **3** fill/navigation attempts,
  stop and report exactly what you see on screen — do not loop.
- State does not change here. After the human submits, they run `/submit $ARGUMENTS`.

**Testing:** run against the local practice form first, not a live posting:
`/prefill file://<repo>/sample-data/practice-form.html` — it should fill the named fields,
attach a resume to the file input, and stop at "Submit application".
