---
description: Score an opportunity on fit/comp/visa/remote/growth and advance it to `scored`.
argument-hint: <opportunity-id>
---

Score the opportunity `$ARGUMENTS`.

Follow `prompts/score-job.md` exactly. Read `pipeline/$ARGUMENTS.json`, `corpus/profile.md`,
and `corpus/accomplishments/*.md`. Fill the `score{}` block (ints 0–10, weighted `total`),
append `{state: "scored", date: <today>}` to `history[]`, set `state` to `scored` if it was
`discovered`, and update `next_action`.

PROVENANCE: any "has X experience" claim in `score.notes` must cite a specific
accomplishment file. Be honest about poor fits. Then report the score and the top reason.
After writing, run `python scripts/validate.py` to confirm the entry is still valid.
