#!/usr/bin/env python3
"""Validate every pipeline/*.json against the Career OS schema.

Checks: required keys present, state is valid, score block well-formed (ints 0-10),
history is a non-empty list of {state, date} with ISO dates in chronological order,
the final history state matches the entry's `state`, and next_action has an ISO due date.

Exits 0 if all entries pass, 1 if any fail. Pure standard library.

Usage:
    python scripts/validate.py
"""

from __future__ import annotations

import sys

from _schema import (
    ALL_STATES,
    REQUIRED_KEYS,
    SCORE_KEYS,
    is_iso_date,
    load_pipeline,
)


def validate_entry(path, data) -> list[str]:
    """Return a list of error strings for one entry (empty == valid)."""
    errors: list[str] = []
    fname = path.name

    # Required top-level keys.
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing required key: {key!r}")

    # id should match filename stem.
    if data.get("id") and data["id"] != path.stem:
        errors.append(f"id {data['id']!r} does not match filename stem {path.stem!r}")

    # State.
    state = data.get("state")
    if state not in ALL_STATES:
        errors.append(f"invalid state: {state!r} (allowed: {', '.join(ALL_STATES)})")

    # Score block.
    score = data.get("score")
    if isinstance(score, dict):
        for k in SCORE_KEYS:
            if k not in score:
                errors.append(f"score missing key: {k!r}")
        for k in ["total", "fit", "comp", "visa", "remote", "growth"]:
            v = score.get(k)
            if v is not None and (not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 10):
                errors.append(f"score.{k} must be an int 0-10, got {v!r}")
    elif score is not None:
        errors.append("score must be an object")

    # History.
    history = data.get("history")
    if not isinstance(history, list) or not history:
        errors.append("history must be a non-empty list")
    else:
        last_date = ""
        for i, h in enumerate(history):
            if not isinstance(h, dict) or "state" not in h or "date" not in h:
                errors.append(f"history[{i}] must be {{state, date}}")
                continue
            if h["state"] not in ALL_STATES:
                errors.append(f"history[{i}].state invalid: {h['state']!r}")
            if not is_iso_date(h["date"]):
                errors.append(f"history[{i}].date not ISO YYYY-MM-DD: {h['date']!r}")
            elif h["date"] < last_date:
                errors.append(f"history[{i}].date {h['date']} is out of order (< {last_date})")
            else:
                last_date = h["date"]
        # Final history state should match current state.
        if history and isinstance(history[-1], dict):
            if history[-1].get("state") != state:
                errors.append(
                    f"state {state!r} does not match last history entry "
                    f"{history[-1].get('state')!r}"
                )

    # next_action.
    na = data.get("next_action")
    if isinstance(na, dict):
        if "action" not in na or "due" not in na:
            errors.append("next_action must have {action, due}")
        elif na.get("due") and not is_iso_date(na["due"]):
            errors.append(f"next_action.due not ISO YYYY-MM-DD: {na['due']!r}")
    elif na is not None:
        errors.append("next_action must be an object")

    # contacts / artifacts shapes.
    if "contacts" in data and not isinstance(data["contacts"], list):
        errors.append("contacts must be a list")
    if "artifacts" in data and not isinstance(data["artifacts"], list):
        errors.append("artifacts must be a list")

    return errors


def main() -> int:
    entries = load_pipeline()
    if not entries:
        print("No pipeline/*.json files found. Nothing to validate.")
        return 0

    total_errors = 0
    for path, data in entries:
        try:
            errs = validate_entry(path, data)
        except Exception as exc:  # noqa: BLE001 - report, don't crash the whole run
            errs = [f"could not validate: {exc}"]
        if errs:
            total_errors += len(errs)
            print(f"✗ {path.name}")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"✓ {path.name}")

    print()
    if total_errors:
        print(f"FAILED: {total_errors} error(s) across {len(entries)} file(s).")
        return 1
    print(f"OK: {len(entries)} file(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
