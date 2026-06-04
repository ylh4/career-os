---
description: Score an opportunity on fit/comp/visa/remote/growth and advance it to `scored`.
argument-hint: <opportunity-id>
---

Score the opportunity `$ARGUMENTS`.

Follow `prompts/score-job.md` exactly. Read `pipeline/$ARGUMENTS.json`, `corpus/profile.md`,
and `corpus/accomplishments/*.md`. Fill the `score{}` block — dimensions are ints 0–10 and
`total = round(fit*3 + comp*2 + visa*2 + remote*1.5 + growth*1.5)` on the 0–100 scale, with a
`confidence` of high|medium|low. Append `{state: "scored", date: <today>}` to `history[]`, set
`state` to `scored` if it was `discovered`, and update `next_action`.

PROVENANCE: any "has X experience" claim in `score.notes` must cite a specific accomplishment
file. VISA DEFAULT: unstated sponsorship → visa ≤ 5, confidence low. Be honest about poor
fits. Then report the score, its tier (≥80 priority · 60–79 standard · <60 backup), and the
top reason. After writing, run `python scripts/validate.py` to confirm the entry is valid.
