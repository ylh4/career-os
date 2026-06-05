"""Shared schema constants and helpers for Career OS pipeline files.

Pure standard library. Imported by validate.py, report.py, and new_opp.py so the
state machine and required-field set are defined in exactly one place.

See CLAUDE.md for the authoritative schema.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

# Repo root is the parent of the scripts/ directory.
ROOT = Path(__file__).resolve().parent.parent
PIPELINE_DIR = ROOT / "pipeline"
RAW_DIR = PIPELINE_DIR / "_raw"  # raw scraped postings, kept for provenance
REPORTS_DIR = ROOT / "reports"
CONTACTS_DIR = ROOT / "contacts"  # one .md per person (recruiters, referrers, recommenders)

# The Application State Machine (CLAUDE.md). Order matters for "next state" logic.
STATES = [
    "discovered",
    "scored",
    "tailored",
    "applied",
    "screening",
    "interview",
    "offer",
]
# Terminal / branch states reachable from any active state.
TERMINAL_STATES = ["rejected", "ghosted", "withdrawn"]
ALL_STATES = STATES + TERMINAL_STATES

# Advancing INTO this state requires explicit human confirmation (HUMAN GATE).
HUMAN_GATE_STATES = {"applied"}

# Top-level required keys for a pipeline entry.
REQUIRED_KEYS = [
    "id",
    "company",
    "title",
    "source",
    "url",
    "location",
    "comp",
    "state",
    "score",
    "history",
    "next_action",
    "contacts",
    "artifacts",
]

SCORE_KEYS = ["total", "fit", "comp", "visa", "remote", "growth", "confidence", "notes"]


def next_state(current: str) -> str | None:
    """Return the next state in the linear flow, or None if at/after the end."""
    if current in STATES:
        i = STATES.index(current)
        if i + 1 < len(STATES):
            return STATES[i + 1]
    return None


def slugify(text: str, max_len: int = 40) -> str:
    """Lowercase, ASCII-ish, hyphen-separated slug for ids and filenames."""
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s[:max_len].strip("-")


def make_entry(
    id: str,
    company: str,
    title: str,
    source: str,
    url: str = "",
    location: str = "",
    comp: str = "",
    today: str | None = None,
    action: str = "",
    due: str = "",
) -> dict:
    """Return a fresh pipeline entry skeleton in the `discovered` state.

    Single definition of the entry shape — used by new_opp.py and scan_ingest.py so the
    schema lives in exactly one place (see CLAUDE.md for the authoritative schema).
    """
    today = today or today_iso()
    return {
        "id": id,
        "company": company,
        "title": title,
        "source": source,
        "url": url,
        "location": location,
        "comp": comp,
        "state": "discovered",
        "score": {
            "total": 0,
            "fit": 0,
            "comp": 0,
            "visa": 0,
            "remote": 0,
            "growth": 0,
            "confidence": "",
            "notes": "",
        },
        "history": [{"state": "discovered", "date": today}],
        "next_action": {
            "action": action or "Score this opportunity (/score)",
            "due": due or today,
        },
        "contacts": [],
        "artifacts": [],
    }


def is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def today_iso() -> str:
    return date.today().isoformat()


def load_pipeline() -> list[tuple[Path, dict]]:
    """Load all pipeline/*.json files as (path, data) tuples, sorted by filename."""
    out: list[tuple[Path, dict]] = []
    if not PIPELINE_DIR.exists():
        return out
    for p in sorted(PIPELINE_DIR.glob("*.json")):
        with p.open(encoding="utf-8") as fh:
            out.append((p, json.load(fh)))
    return out


def dump_entry(path: Path, data: dict) -> None:
    """Write a pipeline entry back to disk with stable, human-readable formatting."""
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _strip(value: str) -> str:
    return value.strip().strip('"').strip("'").strip()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Frontmatter is {} if absent.

    Supports `key: value` and inline list `tags: [a, b]` plus YAML block lists
    (subsequent `- item` lines). Quotes around scalar values are stripped. Shared by the
    corpus linter (accomplishments) and the contacts loader.
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n")
    if parts[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text  # unterminated frontmatter -> treat as no frontmatter

    fm: dict = {}
    current_key: str | None = None
    for raw in parts[1:end]:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and current_key:  # block-list continuation
            fm.setdefault(current_key, [])
            if isinstance(fm[current_key], list):
                fm[current_key].append(_strip(line.lstrip()[2:]))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        current_key = key
        if value == "":
            fm[key] = []  # likely a block list to follow
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fm[key] = [_strip(v) for v in inner.split(",")] if inner else []
        else:
            fm[key] = _strip(value)

    return fm, "\n".join(parts[end + 1 :])


def load_contacts() -> list[tuple[Path, dict, str]]:
    """Load all contacts/*.md as (path, frontmatter, body), sorted by filename."""
    out: list[tuple[Path, dict, str]] = []
    if not CONTACTS_DIR.exists():
        return out
    for p in sorted(CONTACTS_DIR.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        out.append((p, fm, body))
    return out
