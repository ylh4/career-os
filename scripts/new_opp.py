#!/usr/bin/env python3
"""Scaffold a new opportunity in the pipeline.

Creates pipeline/<id>.json in the `discovered` state with the full schema skeleton.
Refuses to overwrite an existing file. Pure standard library.

The id follows the kernel convention YYYY-MM-<company-slug>-<role-slug>.

Usage:
    python scripts/new_opp.py --id 2026-06-acme-staff-eng --company "Acme" \
        --title "Staff Software Engineer" --source referral \
        [--url "https://..."] [--location "Remote (US)"] [--comp "~$250k"] \
        [--due 2026-06-15]
"""

from __future__ import annotations

import argparse
import sys

from _schema import (
    PIPELINE_DIR,
    dump_entry,
    is_iso_date,
    make_entry,
)


def build_skeleton(args) -> dict:
    return make_entry(
        id=args.id,
        company=args.company,
        title=args.title,
        source=args.source,
        url=args.url,
        location=args.location,
        comp=args.comp,
        action=args.action,
        due=args.due,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new pipeline opportunity.")
    parser.add_argument("--id", required=True,
                        help="kebab-case slug YYYY-MM-<company>-<role>; becomes the filename")
    parser.add_argument("--company", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source", required=True,
                        help="referral | linkedin | indeed | company_site | job_board")
    parser.add_argument("--url", default="", help="link to the posting")
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
