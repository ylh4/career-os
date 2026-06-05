#!/usr/bin/env python3
"""List active opportunities whose next_action is due today or overdue.

The read-only data half of `/followups`: the command runs this to learn what needs a nudge,
then drafts (never sends) a message per item. Terminal opportunities are excluded. Sorted by
due date, oldest first. Idempotent — pure read.

Usage:
    python scripts/followups.py
"""

from __future__ import annotations

import sys

from _schema import TERMINAL_STATES, is_iso_date, load_pipeline, today_iso


def due_items(entries, today: str):
    out = []
    for path, d in entries:
        if d.get("state") in TERMINAL_STATES:
            continue
        na = d.get("next_action") or {}
        due = na.get("due", "")
        if not (is_iso_date(due) and due <= today):
            continue
        flag = "OVERDUE" if due < today else "due today"
        score = d.get("score", {}).get("total", "") if isinstance(d.get("score"), dict) else ""
        out.append((due, flag, path.stem, d.get("company", ""), d.get("state", ""),
                    score, na.get("action", "")))
    out.sort(key=lambda r: r[0])
    return out


def main() -> int:
    today = today_iso()
    items = due_items(load_pipeline(), today)

    print(f"# Follow-ups due (as of {today})\n")
    if not items:
        print("Nothing due or overdue. ✅")
        return 0

    print("| Due | | Id | Company | State | Score | Next action |")
    print("|---|---|---|---|---|---|---|")
    for due, flag, oid, company, state, score, action in items:
        mark = "⚠️" if flag == "OVERDUE" else "▶"
        print(f"| {due} | {mark} {flag} | {oid} | {company} | {state} | {score} | {action} |")
    print(f"\n{len(items)} opportunity(ies) need a follow-up drafted (not sent).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
