#!/usr/bin/env python3
"""PreToolUse guard — block writing a tailored resume/cover when the corpus is broken.

Wired as a PreToolUse hook on Write|Edit|MultiEdit. It only acts when the write targets a
`/tailor` deliverable (artifacts/.../resume_vN or cover_vN .md/.docx); for anything else it
exits 0 immediately. When it does act, it runs `validate_corpus.py` on the corpus that feeds
that artifact and, if the corpus is invalid, exits 2 to DENY the write — so no document is ever
generated from a broken corpus (HARD RULE 1 / PROVENANCE). Fail-open: any error in the guard
itself exits 0 (a guard bug must never block legitimate work).

Hook config (.claude/settings.json):
  PreToolUse matcher "Write|Edit|MultiEdit" →
    command: python3 "$CLAUDE_PROJECT_DIR/scripts/guard_corpus.py"
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLE = re.compile(r"/artifacts/[^/]+/(resume|cover)_v\d+\.(md|docx)$")


def main() -> int:
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, ValueError):
        return 0  # unparseable payload — don't block

    if event.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        return 0
    fp = ((event.get("tool_input") or {}).get("file_path") or "").replace("\\", "/")
    if not DELIVERABLE.search(fp):
        return 0  # not a tailored deliverable — nothing to guard

    # Validate the corpus that feeds this artifact (sample artifacts → sample corpus).
    corpus = (ROOT / "sample-data/accomplishments") if "/sample-data/artifacts/" in fp \
        else (ROOT / "corpus/accomplishments")

    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_corpus.py"), str(corpus)],
            capture_output=True, text=True, timeout=60,
        )
    except Exception:  # noqa: BLE001 - never block on a guard failure
        return 0

    if proc.returncode != 0:
        rel = corpus.relative_to(ROOT)
        print(
            f"BLOCKED: corpus is invalid — refusing to generate {Path(fp).name} from a broken "
            f"corpus (PROVENANCE rule). Fix `{rel}` so `validate_corpus.py` passes, then retry.\n"
            + (proc.stdout or "")[-1200:],
            file=sys.stderr,
        )
        return 2  # deny the write
    return 0


if __name__ == "__main__":
    sys.exit(main())
