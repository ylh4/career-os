#!/usr/bin/env python3
"""Career OS analytics — funnel report + dashboard data export.

Reads a candidate's pipeline (+ corpus + contacts) and computes:
  - Funnel reach & conversion across the linear states.
  - Response rate by source (of those that reached `applied`, the share reaching `screening`+).
  - Average time-in-state (from each entry's append-only history).
  - Active-application counts (active = non-terminal; applied = currently out).

Writes `reports/funnel-<today>.md` (human report) and `reports/pipeline-data.js` (the data the
self-contained `reports/dashboard.html` reads). Read-only over the corpus/pipeline. Stdlib only.

Usage:
    python scripts/funnel.py                     # live dirs (pipeline/, corpus/, contacts/)
    python scripts/funnel.py --source sample-data  # the fictitious demo set
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date

from _schema import (
    REPORTS_DIR,
    ROOT,
    STATES,
    TERMINAL_STATES,
    is_iso_date,
    parse_frontmatter,
    today_iso,
)

RESPONSE_STATES = {"screening", "interview", "offer"}

# Where each input lives, per --source. live mirrors the kernel layout; sample-data is flat.
SOURCES = {
    "live": {"pipeline": "pipeline", "contacts": "contacts",
             "accomplishments": "corpus/accomplishments", "stories": "corpus/stories"},
    "sample-data": {"pipeline": "sample-data/pipeline", "contacts": "sample-data/contacts",
                    "accomplishments": "sample-data/accomplishments", "stories": "sample-data/stories"},
}


# ── loaders (source-parameterized) ───────────────────────────────────────────
def _load_pipeline(base) -> list[dict]:
    d = ROOT / base
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))] if d.exists() else []


def _load_md(base):
    d = ROOT / base
    if not d.exists():
        return []
    out = []
    for p in sorted(d.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        out.append((p, fm, body))
    return out


def states_reached(entry: dict) -> set[str]:
    reached = {h.get("state") for h in entry.get("history", []) if isinstance(h, dict)}
    reached.add(entry.get("state"))
    return {s for s in reached if s}


# ── metrics ──────────────────────────────────────────────────────────────────
def compute_funnel(data: list[dict]) -> dict:
    reach = {s: 0 for s in STATES}
    for d in data:
        rs = states_reached(d)
        for s in STATES:
            if s in rs:
                reach[s] += 1
    conversion = {}
    prev = None
    for s in STATES:
        conversion[s] = round(100 * reach[s] / reach[prev]) if prev and reach[prev] else None
        prev = s

    applied_by_src: dict[str, int] = defaultdict(int)
    responded_by_src: dict[str, int] = defaultdict(int)
    for d in data:
        rs = states_reached(d)
        if "applied" in rs:
            src = d.get("source", "unknown") or "unknown"
            applied_by_src[src] += 1
            if rs & RESPONSE_STATES:
                responded_by_src[src] += 1
    response_by_source = {
        src: {"applied": applied_by_src[src], "responded": responded_by_src[src],
              "rate": round(100 * responded_by_src[src] / applied_by_src[src]) if applied_by_src[src] else None}
        for src in sorted(applied_by_src)
    }

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
    time_in_state = {s: {"transitions": len(v), "avgDays": round(sum(v) / len(v), 1)}
                     for s, v in durations.items() if v}

    terminal = {s: sum(1 for d in data if d.get("state") == s) for s in TERMINAL_STATES}
    active = sum(1 for d in data if d.get("state") not in TERMINAL_STATES)
    applied = sum(1 for d in data if d.get("state") == "applied")

    return {"total": len(data), "reach": reach, "conversion": conversion,
            "responseBySource": response_by_source, "timeInState": time_in_state,
            "terminal": terminal, "active": active, "applied": applied}


def corpus_summary(accomplishments, stories) -> dict:
    tags: dict[str, int] = defaultdict(int)
    dates = []
    for _, fm, _ in accomplishments:
        for t in fm.get("tags", []) if isinstance(fm.get("tags"), list) else []:
            tags[t] += 1
        if fm.get("date"):
            dates.append(str(fm["date"]))
    return {"accomplishments": len(accomplishments), "stories": len(stories),
            "tags": dict(sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))),
            "dateRange": [min(dates), max(dates)] if dates else []}


def contacts_summary(contacts, today: str) -> list[dict]:
    out = []
    for _, fm, _ in contacts:
        nxt = fm.get("next_touch", "")
        out.append({"name": fm.get("name", ""), "company": fm.get("company", ""),
                    "relationship": fm.get("relationship", ""),
                    "last_touch": fm.get("last_touch", ""), "next_touch": nxt,
                    "overdue": bool(is_iso_date(nxt) and nxt <= today)})
    return out


# ── outputs ──────────────────────────────────────────────────────────────────
def _pct(v):
    return f"{v}%" if v is not None else "—"


def build_report(f: dict) -> str:
    today = today_iso()
    L = [f"# Funnel Report — {today}", "", f"Total opportunities: **{f['total']}**",
         f"Active applications: **{f['applied']}** out · **{f['active']}** active overall", ""]
    L += ["## Funnel (reach & conversion)", "", "| State | Reached | Conversion from prev |", "|---|---|---|"]
    for s in STATES:
        L.append(f"| {s} | {f['reach'][s]} | {_pct(f['conversion'][s])} |")
    L.append("")
    if any(f["terminal"].values()):
        L += ["**Terminal outcomes:** " + ", ".join(f"{s} {n}" for s, n in f["terminal"].items() if n), ""]
    L += ["## Response rate by source", ""]
    if f["responseBySource"]:
        L += ["| Source | Applied | Responded | Rate |", "|---|---|---|---|"]
        for src, r in f["responseBySource"].items():
            L.append(f"| {src} | {r['applied']} | {r['responded']} | {_pct(r['rate'])} |")
    else:
        L.append("_No opportunities have reached `applied` yet._")
    L += ["", "## Time-in-state (avg days)", ""]
    if f["timeInState"]:
        L += ["| State | Transitions | Avg days |", "|---|---|---|"]
        for s in STATES + TERMINAL_STATES:
            t = f["timeInState"].get(s)
            if t:
                L.append(f"| {s} | {t['transitions']} | {t['avgDays']} |")
    else:
        L.append("_Not enough history to measure time-in-state._")
    return "\n".join(L) + "\n"


def build_data(source: str = "live") -> dict:
    """Assemble the window.CAREER_OS dict for the dashboard from the chosen source."""
    dirs = SOURCES[source]
    today = today_iso()
    pipeline = _load_pipeline(dirs["pipeline"])
    return {
        "generatedAt": today,
        "source": source,
        "pipeline": pipeline,
        "funnel": compute_funnel(pipeline),
        "corpus": corpus_summary(_load_md(dirs["accomplishments"]), _load_md(dirs["stories"])),
        "contacts": contacts_summary(_load_md(dirs["contacts"]), today),
    }


def write_pipeline_data(source: str = "live"):
    """Write reports/pipeline-data{.sample}.js. live → pipeline-data.js; sample → .sample.js."""
    data = build_data(source)
    REPORTS_DIR.mkdir(exist_ok=True)
    name = "pipeline-data.sample.js" if source == "sample-data" else "pipeline-data.js"
    out = REPORTS_DIR / name
    out.write_text("window.CAREER_OS = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Funnel report + dashboard data export.")
    ap.add_argument("--source", choices=list(SOURCES), default="live")
    args = ap.parse_args()
    today = today_iso()

    report = build_report(compute_funnel(_load_pipeline(SOURCES[args.source]["pipeline"])))
    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / f"funnel-{today}.md").write_text(report, encoding="utf-8")
    out = write_pipeline_data(args.source)

    print(report)
    print(f"[wrote reports/funnel-{today}.md and reports/{out.name} (source: {args.source})]")
    print("Open reports/dashboard.html to view.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
