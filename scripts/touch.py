#!/usr/bin/env python3
"""Log an interaction with a contact and set the next suggested touch (the /touch plumbing).

Creates or updates `contacts/<slug>.md` (YAML frontmatter + an append-only `## Interactions`
log), stamps `last_touch` with today and `next_touch` with today + cadence. Deterministic dates
from the local clock. The same contact records double as reference / recommendation-letter
recommenders (see CLAUDE.md), so this serves both networking and reference workflows.

Usage:
    python scripts/touch.py sara-mehari --note "Coffee chat; will intro me to the hiring mgr"
    python scripts/touch.py jordan-lee --name "Jordan Lee" --role "Recruiter" \
        --company "Acme" --relationship recruiter --cadence 14 --note "Recruiter screen booked"
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from _schema import CONTACTS_DIR, parse_frontmatter, today_iso

FIELDS = ["name", "role", "company", "relationship", "last_touch", "next_touch"]


def _serialize(fm: dict) -> str:
    lines = ["---"]
    for k in FIELDS:
        if fm.get(k):
            lines.append(f"{k}: {fm[k]}")
    lines.append("---")
    return "\n".join(lines)


def _append_interaction(body: str, today: str, note: str) -> str:
    """Append a dated line under `## Interactions` (create the section if missing)."""
    entry = f"- {today} — {note}".rstrip(" —")
    lines = body.rstrip("\n").splitlines()
    if any(ln.strip().lower() == "## interactions" for ln in lines):
        lines.append(entry)
    else:
        if lines and lines[-1].strip():
            lines.append("")
        lines += ["## Interactions", entry]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Log a contact interaction; set the next touch.")
    ap.add_argument("slug", help="contact slug → contacts/<slug>.md")
    ap.add_argument("--note", default="", help="what happened (kept verbatim; don't invent)")
    ap.add_argument("--cadence", type=int, default=28, help="days until the next touch (default 28)")
    ap.add_argument("--name", default="")
    ap.add_argument("--role", default="")
    ap.add_argument("--company", default="")
    ap.add_argument("--relationship", default="", help="referrer|recruiter|recommender|hiring-manager|peer|…")
    args = ap.parse_args()

    today = today_iso()
    next_touch = (date.today() + timedelta(days=args.cadence)).isoformat()
    path = CONTACTS_DIR / f"{args.slug}.md"

    if path.exists():
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        created = False
    else:
        fm, body = {}, f"# {args.name or args.slug}\n"
        created = True

    # Apply overrides / fills; flatten any list values the parser may return to strings.
    for key, val in (("name", args.name or args.slug.replace("-", " ").title()),
                     ("role", args.role), ("company", args.company),
                     ("relationship", args.relationship)):
        if val or key not in fm:
            fm.setdefault(key, val)
        if val:
            fm[key] = val
    fm["last_touch"] = today
    fm["next_touch"] = next_touch
    fm = {k: (v[0] if isinstance(v, list) and v else v) for k, v in fm.items()}

    if args.note:
        body = _append_interaction(body, today, args.note)

    CONTACTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(_serialize(fm) + "\n\n" + body.lstrip("\n").rstrip("\n") + "\n", encoding="utf-8")

    verb = "Created" if created else "Updated"
    print(f"{verb} contacts/{args.slug}.md — last_touch {today}, next_touch {next_touch}"
          + (f"\nlogged: {args.note}" if args.note else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
