#!/usr/bin/env python3
"""Render a staged Career OS markdown artifact (resume / cover letter) to .docx.

The pipeline tracks markdown sources (resume_v1.md, cover_v1.md, provenance.md);
this renders the human-facing .docx deliverable that gets uploaded to an ATS. Per
.gitignore, the .docx is a throwaway export — regenerate it any time from the .md.

Supported markdown subset (enough for resumes/letters):
  #, ##, ###        -> Word headings 1/2/3
  - item / * item   -> bullet list
  **bold**          -> bold runs (inline, anywhere in a line)
  blank line        -> paragraph break
  everything else   -> a normal paragraph

Requires python-docx (installed in the project venv).

Usage:
    python scripts/render_docx.py artifacts/<id>/resume_v1.md            # -> resume_v1.docx
    python scripts/render_docx.py artifacts/<id>/resume_v1.md out.docx   # explicit output
    python scripts/render_docx.py artifacts/<id>/*.md                    # batch
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def add_inline(paragraph, text: str) -> None:
    """Add text to a paragraph, turning **bold** spans into bold runs."""
    pos = 0
    for m in BOLD_RE.finditer(text):
        if m.start() > pos:
            paragraph.add_run(text[pos : m.start()])
        paragraph.add_run(m.group(1)).bold = True
        pos = m.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def render(md_path: Path, out_path: Path) -> None:
    doc = Document()
    for raw in md_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue  # collapse blank lines; python-docx spaces paragraphs itself
        h = HEADING_RE.match(line)
        if h:
            level = min(len(h.group(1)), 4)
            doc.add_heading(h.group(2).strip(), level=level)
            continue
        b = BULLET_RE.match(line)
        if b:
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, b.group(1).strip())
            continue
        add_inline(doc.add_paragraph(), line)
    doc.save(str(out_path))


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    # Two-arg form: explicit input + output. Otherwise treat every arg as an input.
    pairs: list[tuple[Path, Path]] = []
    if len(args) == 2 and args[1].lower().endswith(".docx"):
        pairs.append((Path(args[0]), Path(args[1])))
    else:
        for a in args:
            src = Path(a)
            pairs.append((src, src.with_suffix(".docx")))

    rc = 0
    for src, out in pairs:
        if not src.is_file():
            print(f"error: not a file: {src}", file=sys.stderr)
            rc = 1
            continue
        render(src, out)
        print(f"rendered {src} -> {out}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
