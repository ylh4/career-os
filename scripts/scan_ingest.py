#!/usr/bin/env python3
"""Ingest normalized job postings into the Career OS pipeline (the /scan plumbing).

`/scan` (the command) calls Apify Actors via MCP, normalizes each posting, and writes the
batch to a JSON file; this script does the deterministic, testable part: dedupe against the
existing pipeline, scaffold `pipeline/<id>.json` in `discovered`, and preserve the raw
posting under `pipeline/_raw/<id>.json`. It NEVER scores — discovery and scoring stay
separate (see CLAUDE.md).

Input: a JSON array of normalized postings, each:
    {
      "company": "Acme", "title": "Senior BI Analyst",
      "url": "https://...", "location": "Remote", "comp": "$90-110k",
      "source": "linkedin" | "indeed", "description": "full posting text",
      "raw": { ...original Actor item... }
    }

Dedup key is company+title+url (broadened so a job cross-posted to both boards is not added
twice): a posting is a duplicate if its normalized URL matches, OR its normalized
(company, title) matches — checked against existing pipeline files and earlier items in the
same batch.

Pure standard library. Idempotent: re-running on the same input creates nothing new.

Usage:
    python scripts/scan_ingest.py --input pipeline/_raw/_incoming.json [--cap 25] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _schema import (
    PIPELINE_DIR,
    RAW_DIR,
    dump_entry,
    load_pipeline,
    make_entry,
    slugify,
    today_iso,
)


def _norm(text: str) -> str:
    return " ".join(str(text or "").lower().split())


def _norm_url(url: str) -> str:
    """Normalize a URL for dedup: drop scheme, query/fragment, and trailing slash."""
    u = str(url or "").strip().lower()
    for prefix in ("https://", "http://"):
        if u.startswith(prefix):
            u = u[len(prefix):]
            break
    if u.startswith("www."):
        u = u[4:]
    u = u.split("?", 1)[0].split("#", 1)[0]
    return u.rstrip("/")


def existing_keys(entries) -> tuple[set, set]:
    """Return (url_keys, company_title_keys) for all current pipeline entries."""
    urls, cts = set(), set()
    for _, d in entries:
        if d.get("url"):
            urls.add(_norm_url(d["url"]))
        cts.add((_norm(d.get("company", "")), _norm(d.get("title", ""))))
    return urls, cts


def unique_id(company: str, title: str, today: str, taken: set) -> str:
    """Build YYYY-MM-<company>-<title> id, suffixing -2/-3… on collision."""
    month = today[:7]  # YYYY-MM
    base = f"{month}-{slugify(company, 24)}-{slugify(title, 32)}".strip("-")
    base = base or f"{month}-opportunity"
    candidate, n = base, 1
    while candidate in taken or (PIPELINE_DIR / f"{candidate}.json").exists():
        n += 1
        candidate = f"{base}-{n}"
    taken.add(candidate)
    return candidate


def ingest(postings: list[dict], cap: int, dry_run: bool) -> dict:
    today = today_iso()
    entries = load_pipeline()
    seen_urls, seen_cts = existing_keys(entries)
    taken_ids: set = set()

    per_source: dict[str, dict[str, int]] = {}
    new_ids: list[str] = []
    capped = 0

    def bump(src: str, field: str) -> None:
        per_source.setdefault(src, {"fetched": 0, "new": 0, "duplicates": 0})[field] += 1

    for p in postings:
        src = p.get("source", "unknown") or "unknown"
        bump(src, "fetched")

        url_key = _norm_url(p.get("url", ""))
        ct_key = (_norm(p.get("company", "")), _norm(p.get("title", "")))
        is_dup = (url_key and url_key in seen_urls) or ct_key in seen_cts
        if is_dup:
            bump(src, "duplicates")
            continue

        # Reserve the keys now so later batch items dedup against this one.
        if url_key:
            seen_urls.add(url_key)
        seen_cts.add(ct_key)

        if len(new_ids) >= cap:
            capped += 1
            continue

        bump(src, "new")
        oid = unique_id(p.get("company", ""), p.get("title", ""), today, taken_ids)
        new_ids.append(oid)

        if not dry_run:
            entry = make_entry(
                id=oid,
                company=p.get("company", ""),
                title=p.get("title", ""),
                source=src,
                url=p.get("url", ""),
                location=p.get("location", ""),
                comp=p.get("comp", "") or "",
                today=today,
            )
            PIPELINE_DIR.mkdir(exist_ok=True)
            dump_entry(PIPELINE_DIR / f"{oid}.json", entry)
            RAW_DIR.mkdir(parents=True, exist_ok=True)
            raw = p.get("raw", p)
            (RAW_DIR / f"{oid}.json").write_text(
                json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )

    return {"per_source": per_source, "new_ids": new_ids, "capped": capped}


def print_summary(result: dict, dry_run: bool) -> None:
    mode = "DRY RUN — nothing written" if dry_run else "ingested"
    print(f"# /scan ingest ({mode})\n")
    print("| Source | Fetched | New | Duplicates |")
    print("|---|---|---|---|")
    tot = {"fetched": 0, "new": 0, "duplicates": 0}
    for src in sorted(result["per_source"]):
        c = result["per_source"][src]
        for k in tot:
            tot[k] += c[k]
        print(f"| {src} | {c['fetched']} | {c['new']} | {c['duplicates']} |")
    print(f"| **total** | **{tot['fetched']}** | **{tot['new']}** | **{tot['duplicates']}** |")
    print()
    if result["capped"]:
        print(f"⚠️  {result['capped']} new posting(s) dropped by the --cap limit (not silently ignored).")
    verb = "Would create" if dry_run else "Created"
    if result["new_ids"]:
        print(f"{verb} {len(result['new_ids'])} opportunity file(s):")
        for oid in result["new_ids"]:
            print(f"  - {oid}")
    else:
        print("No new opportunities.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest normalized postings into the pipeline.")
    ap.add_argument("--input", required=True, help="JSON file of normalized postings (or '-' for stdin)")
    ap.add_argument("--cap", type=int, default=25, help="max NEW opportunities to create (default 25)")
    ap.add_argument("--dry-run", action="store_true", help="report decisions without writing")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    try:
        postings = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: input is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(postings, list):
        print("error: input must be a JSON array of postings", file=sys.stderr)
        return 2

    result = ingest(postings, cap=args.cap, dry_run=args.dry_run)
    print_summary(result, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
