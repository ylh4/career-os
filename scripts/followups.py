#!/usr/bin/env python3
"""List what needs a nudge today: application follow-ups AND contact touches.

The read-only data half of `/followups`: the command runs this to learn what's due, then
drafts (never sends) a message per item. Covers two sources — pipeline opportunities whose
`next_action.due` has arrived (terminal states excluded), and contacts whose `next_touch` has
arrived. Sorted oldest-first, flagged OVERDUE/due-today. Idempotent — pure read.

Usage:
    python scripts/followups.py
"""

from __future__ import annotations

import sys

from _schema import (
    TERMINAL_STATES,
    is_iso_date,
    load_contacts,
    load_pipeline,
    today_iso,
)


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


def due_touches(contacts, today: str):
    out = []
    for path, fm, _ in contacts:
        nxt = fm.get("next_touch", "")
        if not (is_iso_date(nxt) and nxt <= today):
            continue
        flag = "OVERDUE" if nxt < today else "due today"
        out.append((nxt, flag, path.stem, fm.get("name", path.stem),
                    fm.get("company", ""), fm.get("relationship", ""), fm.get("last_touch", "")))
    out.sort(key=lambda r: r[0])
    return out


def _mark(flag: str) -> str:
    return "⚠️" if flag == "OVERDUE" else "▶"


def main() -> int:
    today = today_iso()
    apps = due_items(load_pipeline(), today)
    touches = due_touches(load_contacts(), today)

    print(f"# Follow-ups due (as of {today})\n")

    print("## Application follow-ups\n")
    if apps:
        print("| Due | | Id | Company | State | Score | Next action |")
        print("|---|---|---|---|---|---|---|")
        for due, flag, oid, company, state, score, action in apps:
            print(f"| {due} | {_mark(flag)} {flag} | {oid} | {company} | {state} | {score} | {action} |")
    else:
        print("_None due._")

    print("\n## Contact touches due\n")
    if touches:
        print("| Next touch | | Contact | Name | Company | Relationship | Last touch |")
        print("|---|---|---|---|---|---|---|")
        for nxt, flag, slug, name, company, rel, last in touches:
            print(f"| {nxt} | {_mark(flag)} {flag} | {slug} | {name} | {company} | {rel} | {last or '—'} |")
    else:
        print("_None due._")

    total = len(apps) + len(touches)
    print(f"\n{total} item(s) need a message drafted (not sent): "
          f"{len(apps)} application(s), {len(touches)} contact(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
