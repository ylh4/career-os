#!/usr/bin/env python3
"""Lint Career OS accomplishment files and print a corpus health report.

Each accomplishment file must be YAML frontmatter + a STAR-story body:

    ---
    metric: "-62% reporting turnaround (5 days -> 1.9 days)"
    tags: [sql, dbt, automation]
    date: 2024-07
    source: "BI ops runbook; manager attestation"
    ---

    # Title
    **Situation:** ... **Task:** ... **Action:** ... **Result:** ...

Checks
  FAIL (exit 1): frontmatter present with all required keys (metric, tags, date,
                 source); a non-empty body after the frontmatter.
  WARN (report): body missing a STAR marker (Situation/Task/Action/Result);
                 `date` not YYYY-MM or YYYY-MM-DD; empty `tags`.

Pure standard library — frontmatter is parsed by a small hand-rolled parser, so there
is no PyYAML dependency.

Usage:
    python scripts/validate_corpus.py [directory]   # default: corpus/accomplishments
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _schema import ROOT, parse_frontmatter

REQUIRED_KEYS = ["metric", "tags", "date", "source"]
STAR_MARKERS = ["situation", "task", "action", "result"]
DATE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")


def body_text(body: str) -> str:
    """Body content excluding the leading markdown title, for the empty check."""
    lines = [ln for ln in body.splitlines() if not ln.lstrip().startswith("#")]
    return "\n".join(lines).strip()


def lint_file(path: Path) -> tuple[list[str], list[str], dict]:
    """Return (errors, warnings, frontmatter) for one accomplishment file."""
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if not fm:
        errors.append("missing or malformed YAML frontmatter")
        return errors, warnings, fm

    for key in REQUIRED_KEYS:
        if key not in fm or fm[key] in ("", [], None):
            errors.append(f"missing/empty required frontmatter key: {key!r}")

    # Non-empty body.
    if not body_text(body):
        errors.append("body is empty (no STAR content after frontmatter)")

    # Warnings.
    date = fm.get("date", "")
    if date and not DATE_RE.match(str(date)):
        warnings.append(f"date {date!r} is not YYYY-MM or YYYY-MM-DD")
    tags = fm.get("tags")
    if isinstance(tags, list) and not tags:
        warnings.append("tags list is empty")
    low = body.lower()
    missing = [m for m in STAR_MARKERS if m not in low]
    if missing:
        warnings.append(f"body missing STAR marker(s): {', '.join(missing)}")

    return errors, warnings, fm


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "corpus" / "accomplishments"
    if not target.is_absolute():
        target = (Path.cwd() / target).resolve()

    if not target.exists():
        print(f"error: directory not found: {target}", file=sys.stderr)
        return 2

    files = sorted(p for p in target.glob("*.md") if p.name.lower() != "readme.md")

    print(f"# Corpus health — {target.relative_to(ROOT) if ROOT in target.parents or target == ROOT else target}")
    print()
    if not files:
        print("No accomplishment files found (only README). Nothing to lint.")
        return 0

    n_pass = n_warn = n_fail = 0
    all_tags: dict[str, int] = {}
    dates: list[str] = []

    for path in files:
        try:
            errors, warnings, fm = lint_file(path)
        except Exception as exc:  # noqa: BLE001 - report, don't crash the run
            errors, warnings, fm = [f"could not parse: {exc}"], [], {}

        if errors:
            n_fail += 1
            print(f"✗ {path.name}")
            for e in errors:
                print(f"    - {e}")
            for w in warnings:
                print(f"    ~ {w}")
        elif warnings:
            n_warn += 1
            print(f"⚠ {path.name}")
            for w in warnings:
                print(f"    ~ {w}")
        else:
            n_pass += 1
            print(f"✓ {path.name}")

        # Aggregate health stats from files that parsed.
        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        for t in tags:
            all_tags[t] = all_tags.get(t, 0) + 1
        if fm.get("date"):
            dates.append(str(fm["date"]))

    print()
    print("## Summary")
    print(f"- Files: {len(files)}  |  ✓ {n_pass}  ⚠ {n_warn}  ✗ {n_fail}")
    if dates:
        print(f"- Date range: {min(dates)} → {max(dates)}")
    if all_tags:
        top = sorted(all_tags.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
        print(f"- Distinct tags: {len(all_tags)}  |  top: " +
              ", ".join(f"{t}({c})" for t, c in top))
    print()

    if n_fail:
        print(f"FAILED: {n_fail} file(s) with errors.")
        return 1
    print("OK: all files have valid frontmatter and a non-empty body.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
