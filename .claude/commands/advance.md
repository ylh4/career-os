---
description: Advance an opportunity to its next state (appends history, enforces the Human Gate).
argument-hint: <opportunity-id> [target-state]
---

Advance the opportunity `$ARGUMENTS` to its next state.

1. Read `pipeline/<id>.json`. Determine the next state: the linear flow is
   `discovered → scored → tailored → applied → followed_up → screening → interview → offer`,
   plus the branch states `rejected` and `ghosted` (reachable from any active state). If the
   user named a specific target state, use that; otherwise use the next linear state.
2. **HUMAN GATE:** if the target state is `applied`, you must NOT proceed automatically.
   Confirm with the human that *they* have reviewed the staged artifacts and submitted the
   application. Only after explicit confirmation may you set `state` to `applied`.
3. Append `{state: <new>, date: <today>}` to `history[]`, set `state`, and update
   `next_action` to the sensible next step (e.g. moving to `applied` → set a follow-up;
   `screening` → `/interview-prep`).
4. Run `python scripts/validate.py` to confirm the entry is still valid, then summarize the
   transition.

Never skip states silently or overwrite history — it is append-only.
