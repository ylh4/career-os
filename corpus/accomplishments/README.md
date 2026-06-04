# Accomplishments

**One verifiable achievement per file.** These are the atoms of every resume bullet and
cover-letter claim. Per the PROVENANCE rule (`CLAUDE.md`), if a fact isn't in one of these
files (or `profile.md`), it cannot appear in a generated artifact.

Filename: kebab-case, descriptive — e.g. `reporting-turnaround.md`, `warehouse-cost-cut.md`.

## Format

Each file is **YAML frontmatter + a STAR-story body**:

```markdown
---
metric: "-62% reporting turnaround (5 days → 1.9 days)"
tags: [sql, automation, reporting, etl]
date: 2024-07
source: "BI ops dashboard; manager attestation"
---

# Automated the weekly executive reporting pipeline

**Situation:** The exec team waited ~5 days each week for hand-built reports.
**Task:** Cut the turnaround without adding headcount.
**Action:** What *you* specifically did — concrete, first person.
**Result:** The quantified outcome — must restate the `metric` above, with its baseline.
```

### Frontmatter keys (all required)
| Key | Meaning |
|---|---|
| `metric` | The single headline quantified result — number + unit + baseline. |
| `tags` | YAML list of skills/keywords for matching against job descriptions. |
| `date` | `YYYY-MM` (or `YYYY-MM-DD`) — when it was achieved. |
| `source` | Provenance trail — what you'd point to if challenged (dashboard, report, attestation, URL). |

## Rules
- The **`metric`** must be a real, defensible number with its baseline. No rounding into fiction.
- The body's **Result** restates that metric so resume bullets and STAR answers stay consistent.
- The **`source`** is your provenance — the standard every generated artifact must meet.
- Keep each file to a single accomplishment so it can be selected independently when
  tailoring to a specific role.
- Run `python scripts/validate_corpus.py corpus/accomplishments` to lint these files.

A complete set of worked examples lives in `sample-data/accomplishments/`.
