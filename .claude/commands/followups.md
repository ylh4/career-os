---
description: List overdue actions + due contact touches across the pipeline and draft (not send) follow-up messages.
argument-hint: "[id]  (optional — limit to one opportunity)"
---

Surface what needs a nudge and draft the messages — never send them (HUMAN GATE).

1. Run `python scripts/followups.py`. It prints two sections: **Application follow-ups**
   (active opportunities whose `next_action.due` has arrived) and **Contact touches due**
   (people in `contacts/` whose `next_touch` has arrived) — both oldest-first, OVERDUE/due-today
   flagged. If `$ARGUMENTS` names an id, limit your drafting to that one.
2. For each listed **opportunity**, read `pipeline/<id>.json` (state, contacts, history dates)
   and `corpus/profile.md` for voice. Draft a short, specific follow-up to
   `artifacts/<id>/follow-up.md` appropriate to the state (post-application nudge,
   post-screen thank-you, post-interview note). Reference something concrete and true; keep
   it brief and warm. Add the path to `artifacts[]`.
   For each listed **contact touch**, draft a brief, warm check-in (or, for a `recommender`, a
   recommendation-letter nudge) and, after the human sends it, log it with
   `python scripts/touch.py <slug> --note "…"` (which resets `next_touch`).
3. Follow-ups do **not** change state — an `applied` opp stays `applied`. To reset a cadence,
   edit that entry's `next_action` directly (advancing to the same state is a deliberate
   no-op). After **2 follow-ups and 21 days of silence** on an `applied` opp, propose moving
   it to `ghosted` (`python scripts/advance.py <id> ghosted`) — but only the human decides.

PROVENANCE: any claim about the candidate traces to the corpus. HUMAN GATE: messages are
staged only — the human sends them. Then run `python scripts/validate.py`.
