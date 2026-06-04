# Stories (STAR)

Longer, first-person **narrative** versions of behavioral-interview answers, in STAR form
(Situation, Task, Action, Result). One story per file. Drawn on by `/interview-prep`. Same
provenance discipline applies — results trace back to a corpus accomplishment.

Filename: kebab-case by theme — e.g. `ambiguous-mandate.md`, `stakeholder-pushback.md`.

## Format

**Light frontmatter + a narrative body:**

```markdown
---
themes: [ambiguity, influence, stakeholder-management]
tags: [bi, analytics]
source: "[outreach-reallocation]"
---

# <Story title>

A longer, spoken-style narrative STAR version — enough detail to deliver out loud in an
interview. Weave Situation → Task → Action → Result naturally; keep any metric exactly as
it appears in the linked accomplishment.
```

### Frontmatter keys
| Key | Meaning |
|---|---|
| `themes` | The interview themes this story answers (leadership, conflict, ambiguity, failure, influence, ...) — used to select the right story. |
| `tags` | Domain/skill keywords. |
| `source` | Provenance — link back to an accomplishment slug in `[brackets]`, or an attestation. |

## Rules
- Map each story to the **themes** interviewers probe so prep can pick the right one.
- Any metric in the narrative must match the linked accomplishment's `metric` (PROVENANCE).

Worked examples live in `sample-data/stories/`.
