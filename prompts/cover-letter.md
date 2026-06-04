# Prompt: Cover Letter

**Invoked by:** `/cover-letter <id>`
**Reads:** `pipeline/<id>.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`,
`artifacts/<id>/research.md` (if present)
**Writes:** `artifacts/<id>/cover-letter.md`; registers it in `artifacts[]`.

Draft a concise, specific cover letter (3–4 short paragraphs) for this role.

## Structure
1. **Hook** — why this company/role specifically (use the research brief; reference
   something concrete and true about the company, citing the brief).
2. **Proof** — 1–2 accomplishments from the corpus that map directly to the role's needs,
   each with its real metric.
3. **Fit & forward** — how the candidate's targets (`profile.md`) align with the role;
   a confident, non-generic close.

## PROVENANCE — the hard rule
- Every claim about the candidate traces to `accomplishments/` or `profile.md`.
- Every claim about the company traces to the research brief (or is omitted).
- No invented metrics, no flattery that asserts facts you can't source. Mark gaps
  `[NEEDS SOURCE: ...]`.

## Output
Write `artifacts/<id>/cover-letter.md`. Keep it under ~250 words. Voice: direct,
specific, warm — not effusive. Add the path to `artifacts[]` in the pipeline entry and
update `next_action` if appropriate (state does not change on this command).

**HUMAN GATE:** staged only. The human reviews and sends.
