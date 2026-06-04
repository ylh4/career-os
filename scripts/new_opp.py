#!/usr/bin/env python3
"""Scaffold a new opportunity in the pipeline.

Creates pipeline/<id>.json in the `discovered` state with the full schema skeleton.
Refuses to overwrite an existing file. Pure standard library.

Usage:
    python scripts/new_opp.py --id acme-staff-eng --company "Acme" \
        --title "Staff Software Engineer" --source "Referral — LinkedIn" \
        [--location "Remote (US)"] [--comp "~$250k"] [--due 2026-06-15]
"""

from __future__ import annotations

import argparse
import sys

from _schema import (
    PIPELINE_DIR,
    dump_entry,
    is_iso_date,
    today_iso,
)


def build_skeleton(args) -> dict:
    today = today_iso()
    return {
        "id": args.id,
        "company": args.company,
        "title": args.title,
        "source": args.source,
        "location": args.location,
        "comp": args.comp,
        "state": "discovered",
        "score": {
            "total": 0,
            "fit": 0,
            "comp": 0,
            "visa": 0,
            "remote": 0,
            "growth": 0,
            "notes": "",
        },
        "history": [{"state": "discovered", "date": today}],
        "next_action": {
            "action": args.action or "Score this opportunity (/score)",
            "due": args.due or today,
        },
        "contacts": [],
        "artifacts": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new pipeline opportunity.")
    parser.add_argument("--id", required=True, help="kebab-case slug; becomes the filename")
    parser.add_argument("--company", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source", required=True, help="where the opportunity was found")
    parser.add_argument("--location", default="", help="e.g. 'Remote (US)'")
    parser.add_argument("--comp", default="", help="string or leave blank")
    parser.add_argument("--action", default="", help="override the initial next_action text")
    parser.add_argument("--due", default="", help="next_action due date (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.due and not is_iso_date(args.due):
        print(f"error: --due must be ISO YYYY-MM-DD, got {args.due!r}", file=sys.stderr)
        return 2

    PIPELINE_DIR.mkdir(exist_ok=True)
    out_path = PIPELINE_DIR / f"{args.id}.json"
    if out_path.exists():
        print(f"error: {out_path.relative_to(PIPELINE_DIR.parent)} already exists; refusing to overwrite.",
              file=sys.stderr)
        return 1

    dump_entry(out_path, build_skeleton(args))
    print(f"Created {out_path.relative_to(PIPELINE_DIR.parent)} in state 'discovered'.")
    print("Next: /score", args.id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
