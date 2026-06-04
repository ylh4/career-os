---
description: Draft a follow-up message for an opportunity and set the next next_action.
argument-hint: <opportunity-id>
---

Draft a follow-up for the opportunity `$ARGUMENTS`.

1. Read `pipeline/$ARGUMENTS.json` for state, contacts, and history (use the dates to gauge
   how long it's been). Read `corpus/profile.md` for voice and any relevant accomplishment
   to reference.
2. Write a short, specific follow-up message to `artifacts/$ARGUMENTS/follow-up.md`
   appropriate to the current state (post-application nudge, post-screen thank-you, post-
   interview note). Reference something concrete and true; keep it brief and warm.
3. Add the path to `artifacts[]`. If the state is `applied` and a follow-up is now sent,
   you may `/advance` to `followed_up` — but only the human sends the message
   (HUMAN GATE). Set `next_action` to the next checkpoint with a due date.

PROVENANCE: any claim about the candidate traces to the corpus. Then run
`python scripts/validate.py`.
