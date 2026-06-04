#!/usr/bin/env python3
"""Compute Career OS funnel analytics and write a report.

From every pipeline/*.json (using each entry's append-only history[]) it computes:
  - Funnel reach & conversion: how many opportunities reached each linear state, and
    the stage-to-stage conversion rate.
  - Response rate by source: of opportunities that reached `applied`, the share that
    drew a real response (reached `screening` or later), grouped by `source`.
  - Time-in-state: average days spent in each state, from consecutive history dates.

Writes reports/funnel-<today>.md and echoes it to stdout. Pure standard library.

Usage:
    python scripts/funnel.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from datetime import date

from _schema import (
    REPORTS_DIR,
    STATES,
    TERMINAL_STATES,
    is_iso_date,
    load_pipeline,
    today_iso,
)

# A "response" means the opportunity reached at least this far.
RESPONSE_STATES = {"screening", "interview", "offer"}


def states_reached(entry: dict) -> set[str]:
    """All states an entry has ever been in (from history, plus current state)."""
    reached = {h.get("state") for h in entry.get("history", []) if isinstance(h, dict)}
    reached.add(entry.get("state"))
    return {s for s in reached if s}


def _pct(num: int, den: int) -> str:
    return f"{(100 * num / den):.0f}%" if den else "—"


def build_report(entries) -> str:
    data = [d for _, d in entries]
    L: list[str] = []
    today = today_iso()
    L += [f"# Funnel Report — {today}", "", f"Total opportunities: **{len(data)}**", ""]

    # ── Funnel reach & conversion ────────────────────────────────────────────
    reach = {s: 0 for s in STATES}
    for d in data:
        rs = states_reached(d)
        for s in STATES:
            if s in rs:
                reach[s] += 1

    L += ["## Funnel (reach & conversion)", "", "| State | Reached | Conversion from prev |", "|---|---|---|"]
    prev = None
    for s in STATES:
        conv = _pct(reach[s], reach[prev]) if prev else "—"
        L.append(f"| {s} | {reach[s]} | {conv} |")
        prev = s
    L.append("")

    # Terminal outcomes.
    term = {s: sum(1 for d in data if d.get("state") == s) for s in TERMINAL_STATES}
    if any(term.values()):
        L += ["**Terminal outcomes:** " + ", ".join(f"{s} {n}" for s, n in term.items() if n), ""]

    # ── Response rate by source ──────────────────────────────────────────────
    applied_by_src: dict[str, int] = defaultdict(int)
    responded_by_src: dict[str, int] = defaultdict(int)
    for d in data:
        rs = states_reached(d)
        if "applied" in rs:
            src = d.get("source", "unknown") or "unknown"
            applied_by_src[src] += 1
            if rs & RESPONSE_STATES:
                responded_by_src[src] += 1

    L += ["## Response rate by source", "", "_Of opportunities that reached `applied`, the share that reached `screening`+._", ""]
    if applied_by_src:
        L += ["| Source | Applied | Responded | Rate |", "|---|---|---|---|"]
        for src in sorted(applied_by_src):
            a, r = applied_by_src[src], responded_by_src[src]
            L.append(f"| {src} | {a} | {r} | {_pct(r, a)} |")
    else:
        L.append("_No opportunities have reached `applied` yet._")
    L.append("")

    # ── Time-in-state ────────────────────────────────────────────────────────
    durations: dict[str, list[int]] = defaultdict(list)
    for d in data:
        hist = [h for h in d.get("history", []) if isinstance(h, dict) and is_iso_date(h.get("date", ""))]
        for i in range(len(hist) - 1):
            try:
                days = (date.fromisoformat(hist[i + 1]["date"]) - date.fromisoformat(hist[i]["date"])).days
            except ValueError:
                continue
            if days >= 0:
                durations[hist[i]["state"]].append(days)

    L += ["## Time-in-state (avg days)", "", "_Average days between entering a state and the next transition._", ""]
    if durations:
        L += ["| State | Transitions | Avg days |", "|---|---|---|"]
        for s in STATES + TERMINAL_STATES:
            vals = durations.get(s)
            if vals:
                L.append(f"| {s} | {len(vals)} | {sum(vals) / len(vals):.1f} |")
    else:
        L.append("_Not enough history to measure time-in-state._")
    L.append("")

    return "\n".join(L) + "\n"


def main() -> int:
    entries = load_pipeline()
    report = build_report(entries)
    REPORTS_DIR.mkdir(exist_ok=True)
    out = REPORTS_DIR / f"funnel-{today_iso()}.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"[written to {out.relative_to(REPORTS_DIR.parent)}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
