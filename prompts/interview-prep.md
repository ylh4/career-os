# Prompt: Interview Prep

**Invoked by:** `/interview-prep <id>`
**Reads:** `pipeline/<id>.json`, `corpus/stories/*.md`, `corpus/accomplishments/*.md`,
`corpus/profile.md`, `artifacts/<id>/research.md` (if present)
**Writes:** `artifacts/<id>/interview-prep.md`.

Build a focused prep document for an upcoming interview at this company.

## Sections to produce
1. **Role & company snapshot** — 3–5 bullets from the research brief (cited). What they do,
   recent news, likely priorities for this role.
2. **Likely questions** — behavioral + technical, derived from the JD and domain. For each
   behavioral question, name the best-matching `stories/` file (by its themes).
3. **STAR bank** — pull the relevant stories into tight, deliverable form (Situation→Result),
   keeping metrics exactly as in the corpus.
4. **Questions to ask them** — thoughtful, specific to the company/role and the candidate's
   `profile.md` priorities (e.g. on-call, scope, growth).
5. **Risks & gaps** — honest list of where the candidate's corpus is thin for this role, so
   they can prepare a candid answer. Mark anything unsourced `[NEEDS SOURCE]`.

## PROVENANCE — the hard rule
Stories and metrics come from the corpus, verbatim on the numbers. Company facts come from
the research brief or are omitted. Don't coach the candidate to claim things they can't back.

## Output
Write `artifacts/<id>/interview-prep.md`, add it to `artifacts[]`, and update `next_action`
(e.g. the interview date). State typically is already `screening`/`interview` — set via
`/advance`, not here.
