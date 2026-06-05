#!/usr/bin/env python3
"""Transition an opportunity to a new state — validated, idempotent, append-only.

The deterministic core of `/advance` and `/submit`. Enforces the kernel state machine
(CLAUDE.md): transitions move exactly one step forward OR to a terminal state; no skipping,
no going backward, and no leaving a terminal state. Advancing INTO `applied` is the HUMAN
GATE and requires `--confirm` (so a stray `/advance … applied` can't bypass `/submit`).

Idempotent: advancing to the state an entry is already in is a no-op (no duplicate history,
exit 0), so the command is safe to re-run. History is append-only and never rewritten. Dates
come from the local clock (today).

Usage:
    python scripts/advance.py <id> [target_state] [--confirm] \
        [--action "next action text"] [--due YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta

from _schema import (
    ALL_STATES,
    HUMAN_GATE_STATES,
    PIPELINE_DIR,
    TERMINAL_STATES,
    dump_entry,
    is_iso_date,
    next_state,
    today_iso,
)

# Default next_action per target state: (text, days-from-today for the due date).
DEFAULT_NEXT_ACTION = {
    "scored": ("Tailor resume (/tailor)", 3),
    "tailored": ("Human review & submit (/submit)", 2),
    "applied": ("Follow up on application", 7),
    "screening": ("Prep for interview (/prep)", 3),
    "interview": ("Send post-interview follow-up", 1),
    "offer": ("Review the offer", 3),
}


def _due_in(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def _default_next_action(target: str) -> dict:
    if target in TERMINAL_STATES:
        return {"action": f"Closed ({target})", "due": today_iso()}
    text, days = DEFAULT_NEXT_ACTION.get(target, ("Review opportunity", 3))
    return {"action": text, "due": _due_in(days)}


def transition(data: dict, target: str | None, confirm: bool,
               action: str, due: str) -> tuple[bool, str]:
    """Mutate `data` in place. Return (changed, message)."""
    current = data.get("state")
    if current not in ALL_STATES:
        return False, f"refuse: current state {current!r} is not a valid state"

    target = target or next_state(current)
    if target is None:
        return False, f"refuse: {current!r} is the last linear state — only a terminal move is possible"
    if target not in ALL_STATES:
        return False, f"refuse: {target!r} is not a valid state (allowed: {', '.join(ALL_STATES)})"

    # Idempotent no-op.
    if target == current:
        return False, f"no-op: already in {current!r} (nothing to do)"

    # Legality.
    if current in TERMINAL_STATES:
        return False, f"refuse: {current!r} is terminal — cannot transition out of it"
    if target not in TERMINAL_STATES and target != next_state(current):
        legal = [next_state(current)] + TERMINAL_STATES
        legal = [s for s in legal if s]
        return False, (f"refuse: illegal transition {current!r} → {target!r} "
                       f"(no skipping/backward). Legal: {', '.join(legal)}")
    if target in HUMAN_GATE_STATES and not confirm:
        return False, (f"refuse: advancing to {target!r} is the HUMAN GATE — use /submit "
                       f"(or pass --confirm) after a human has submitted the application")

    # Apply (append-only history; never rewrite).
    data.setdefault("history", []).append({"state": target, "date": today_iso()})
    data["state"] = target
    if action:
        data["next_action"] = {"action": action, "due": due or today_iso()}
    else:
        na = _default_next_action(target)
        if due:
            na["due"] = due
        data["next_action"] = na
    return True, f"{current} → {target} (next: {data['next_action']['action']} · due {data['next_action']['due']})"


def main() -> int:
    ap = argparse.ArgumentParser(description="Validated, idempotent state transition.")
    ap.add_argument("id", help="opportunity id (filename stem, with or without .json)")
    ap.add_argument("target", nargs="?", default=None, help="target state (default: next linear state)")
    ap.add_argument("--confirm", action="store_true", help="required to advance INTO 'applied' (human gate)")
    ap.add_argument("--action", default="", help="override next_action text")
    ap.add_argument("--due", default="", help="override next_action due date (YYYY-MM-DD)")
    args = ap.parse_args()

    if args.due and not is_iso_date(args.due):
        print(f"error: --due must be ISO YYYY-MM-DD, got {args.due!r}", file=sys.stderr)
        return 2

    stem = args.id[:-5] if args.id.endswith(".json") else args.id
    path = PIPELINE_DIR / f"{stem}.json"
    if not path.exists():
        print(f"error: {path.relative_to(PIPELINE_DIR.parent)} not found", file=sys.stderr)
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))
    changed, msg = transition(data, args.target, args.confirm, args.action, args.due)
    if changed:
        dump_entry(path, data)
        print(f"{stem}: {msg}")
        return 0
    # No-op is success (idempotent); a refusal is an error.
    if msg.startswith("no-op"):
        print(f"{stem}: {msg}")
        return 0
    print(f"{stem}: {msg}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
