#!/usr/bin/env python3
"""Regenerate reports/pipeline-data.js — the data the dashboard reads.

Two ways to run:
  - Manually: `python scripts/export_dashboard_data.py` rebuilds it from the live pipeline.
  - As a Claude Code PostToolUse hook: `… --hook` reads the tool event from stdin and rebuilds
    ONLY when the change touched the pipeline (so editing prompts/scripts/etc. is a no-op).

Fail-safe by design: the skip path does only a stdin read + a regex (no heavy imports), and the
script ALWAYS exits 0 — a hook must never disrupt the tool call that triggered it.

Hook config (.claude/settings.json):
  PostToolUse matcher "Write|Edit|MultiEdit|Bash" →
    command: python3 "$CLAUDE_PROJECT_DIR/scripts/export_dashboard_data.py" --hook
"""

from __future__ import annotations

import json
import re
import sys

# A Bash command that likely mutated the pipeline (script-driven writes don't go through Edit).
_MUTATORS = re.compile(r"(advance|new_opp|scan_ingest|touch)\.py\b|(^|[\s/])pipeline/")


def _should_regen(event: dict) -> bool:
    """True if this PostToolUse event changed a pipeline file."""
    ti = event.get("tool_input") or {}
    fp = ti.get("file_path")
    if fp:  # Write/Edit/MultiEdit
        fp = fp.replace("\\", "/")
        return "/pipeline/" in fp and fp.endswith(".json") and "/pipeline/_raw/" not in fp
    cmd = ti.get("command")
    if cmd:  # Bash
        return bool(_MUTATORS.search(cmd))
    return False


def main() -> int:
    hook = "--hook" in sys.argv[1:]
    if hook:
        try:
            event = json.loads(sys.stdin.read() or "{}")
        except (json.JSONDecodeError, ValueError):
            return 0  # malformed payload — do nothing, never disrupt
        if not _should_regen(event):
            return 0  # not a pipeline change — silent no-op

    try:
        from funnel import write_pipeline_data  # lazy: only when actually regenerating
        out = write_pipeline_data("live")
        if not hook:  # stay silent in hook mode; print only for manual runs
            print(f"wrote {out.relative_to(out.parent.parent)}")
    except Exception:  # noqa: BLE001 - a hook must never fail the triggering tool
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
