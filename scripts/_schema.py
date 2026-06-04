"""Shared schema constants and helpers for Career OS pipeline files.

Pure standard library. Imported by validate.py, report.py, and new_opp.py so the
state machine and required-field set are defined in exactly one place.

See CLAUDE.md for the authoritative schema.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

# Repo root is the parent of the scripts/ directory.
ROOT = Path(__file__).resolve().parent.parent
PIPELINE_DIR = ROOT / "pipeline"
REPORTS_DIR = ROOT / "reports"

# The Application State Machine (CLAUDE.md). Order matters for "next state" logic.
STATES = [
    "discovered",
    "scored",
    "tailored",
    "applied",
    "followed_up",
    "screening",
    "interview",
    "offer",
]
# Terminal / branch states reachable from any active state.
TERMINAL_STATES = ["rejected", "ghosted"]
ALL_STATES = STATES + TERMINAL_STATES

# Advancing INTO this state requires explicit human confirmation (HUMAN GATE).
HUMAN_GATE_STATES = {"applied"}

# Top-level required keys for a pipeline entry.
REQUIRED_KEYS = [
    "id",
    "company",
    "title",
    "source",
    "location",
    "comp",
    "state",
    "score",
    "history",
    "next_action",
    "contacts",
    "artifacts",
]

SCORE_KEYS = ["total", "fit", "comp", "visa", "remote", "growth", "notes"]


def next_state(current: str) -> str | None:
    """Return the next state in the linear flow, or None if at/after the end."""
    if current in STATES:
        i = STATES.index(current)
        if i + 1 < len(STATES):
            return STATES[i + 1]
    return None


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
