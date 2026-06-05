---
description: Advance an opportunity to its next state (validated, idempotent; enforces the Human Gate).
argument-hint: <opportunity-id> [target-state]
---

Advance the opportunity `$ARGUMENTS`.

Run the validated transition helper (it enforces the kernel state machine — forward one step
or to a terminal state; no skipping, no backward, no leaving a terminal — and is idempotent):

```bash
python scripts/advance.py <id> [target-state]
```

- With no target, it moves to the next linear state. With a target, it must be the next linear
  state or a terminal one (`rejected`/`ghosted`/`withdrawn`); illegal moves are refused.
- It appends `{state, date: today}` to `history[]` (append-only), sets `state`, and sets a
  sensible `next_action` with a date computed from today. Re-running to the same state is a
  safe no-op.
- **HUMAN GATE:** advancing into `applied` is refused here. That move only happens through
  `/submit` after the human confirms they submitted — relay that and stop if asked to.

After it runs, relay the helper's message and run `python scripts/validate.py` to confirm the
entry is still valid.
