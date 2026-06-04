---
description: List overdue actions + due contact touches across the pipeline and draft (not send) follow-up messages.
argument-hint: "[id]  (optional — limit to one opportunity)"
---

Surface what needs a nudge and draft the messages — never send them (HUMAN GATE).

1. Run `python scripts/report.py` to get every active opportunity with an ⚠️ OVERDUE or
   due-today `next_action`. If `$ARGUMENTS` names an id, limit to that one.
2. For each, read `pipeline/<id>.json` (state, contacts, history dates) and
   `corpus/profile.md` for voice. Draft a short, specific follow-up to
   `artifacts/<id>/follow-up.md` appropriate to the state (post-application nudge,
   post-screen thank-you, post-interview note). Reference something concrete and true; keep
   it brief and warm. Add the path to `artifacts[]`.
3. Follow-ups do **not** change state — an `applied` opp stays `applied`. After **2
   follow-ups and 21 days of silence** on an `applied` opp, propose moving it to `ghosted`
   (via `/advance`), but only the human decides. Set each `next_action` to the next
   checkpoint with a due date.

PROVENANCE: any claim about the candidate traces to the corpus. HUMAN GATE: messages are
staged only — the human sends them. Then run `python scripts/validate.py`.
