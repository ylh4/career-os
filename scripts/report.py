#!/usr/bin/env python3
"""Render a Career OS pipeline dashboard.

Reads every pipeline/*.json and prints a markdown dashboard to stdout and to
reports/pipeline-<today>.md: counts by state, the top-scored active opportunities,
and any next_actions that are overdue or due soon.

Pure standard library.

Usage:
    python scripts/report.py
"""

from __future__ import annotations

import sys

from _schema import (
    ALL_STATES,
    REPORTS_DIR,
    STATES,
    TERMINAL_STATES,
    is_iso_date,
    load_pipeline,
    today_iso,
)


def build_report(entries) -> str:
    today = today_iso()
    lines: list[str] = []
    lines.append(f"# Pipeline Dashboard — {today}")
    lines.append("")
    lines.append(f"Total opportunities: **{len(entries)}**")
    lines.append("")

    # Counts by state.
    counts = {s: 0 for s in ALL_STATES}
    for _, d in entries:
        counts[d.get("state", "?")] = counts.get(d.get("state", "?"), 0) + 1

    lines.append("## By state")
    lines.append("")
    lines.append("| State | Count |")
    lines.append("|---|---|")
    for s in STATES + TERMINAL_STATES:
        if counts.get(s):
            lines.append(f"| {s} | {counts[s]} |")
    lines.append("")

    # Pipeline grouped by state — each opportunity with its score and next action.
    lines.append("## Pipeline by state")
    lines.append("")
    by_state: dict[str, list] = {}
    for _, d in entries:
        by_state.setdefault(d.get("state", "?"), []).append(d)
    any_listed = False
    for s in STATES + TERMINAL_STATES:
        group = by_state.get(s)
        if not group:
            continue
        any_listed = True
        lines.append(f"### {s} ({len(group)})")
        group.sort(
            key=lambda d: d["score"]["total"] if isinstance(d.get("score"), dict)
            and isinstance(d["score"].get("total"), int) else -1,
            reverse=True,
        )
        for d in group:
            score = d["score"]["total"] if isinstance(d.get("score"), dict) and isinstance(
                d["score"].get("total"), int) else "—"
            na = d.get("next_action") or {}
            due = na.get("due", "")
            flag = ""
            if is_iso_date(due) and s not in TERMINAL_STATES:
                if due < today:
                    flag = " ⚠️ OVERDUE"
                elif due == today:
                    flag = " ▶ due today"
            action = na.get("action", "—")
            due_str = f" (due {due}{flag})" if due else ""
            lines.append(
                f"- **{score}** · {d.get('company','')} — {d.get('title','')} · {action}{due_str}"
            )
        lines.append("")
    if not any_listed:
        lines.append("_No opportunities yet._")
        lines.append("")

    active = [(p, d) for p, d in entries if d.get("state") not in TERMINAL_STATES]

    # Top-scored active opportunities.
    scored = [
        (d.get("score", {}).get("total", 0), d)
        for _, d in active
        if isinstance(d.get("score"), dict) and isinstance(d["score"].get("total"), int)
    ]
    scored.sort(key=lambda t: t[0], reverse=True)
    lines.append("## Top-scored (active)")
    lines.append("")
    if scored:
        lines.append("| Score | Company | Title | State |")
        lines.append("|---|---|---|---|")
        for total, d in scored[:10]:
            lines.append(
                f"| {total} | {d.get('company','')} | {d.get('title','')} | {d.get('state','')} |"
            )
    else:
        lines.append("_No scored opportunities yet._")
    lines.append("")

    # Next actions: overdue / due.
    lines.append("## Next actions")
    lines.append("")
    rows = []
    for _, d in active:
        na = d.get("next_action") or {}
        due = na.get("due", "")
        action = na.get("action", "")
        if not action:
            continue
        flag = ""
        if is_iso_date(due):
            if due < today:
                flag = "⚠️ OVERDUE"
            elif due == today:
                flag = "▶ due today"
        rows.append((due or "9999-99-99", due, d.get("company", ""), action, flag))
    rows.sort()
    if rows:
        lines.append("| Due | Company | Action | |")
        lines.append("|---|---|---|---|")
        for _, due, company, action, flag in rows:
            lines.append(f"| {due or '—'} | {company} | {action} | {flag} |")
    else:
        lines.append("_No open next actions._")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    entries = load_pipeline()
    report = build_report(entries)

    # Write to reports/.
    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / f"pipeline-{today_iso()}.md"
    out_path.write_text(report, encoding="utf-8")

    # Echo to stdout.
    print(report)
    print(f"[written to {out_path.relative_to(REPORTS_DIR.parent)}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
