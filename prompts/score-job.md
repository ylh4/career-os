# Prompt: Score Job

**Invoked by:** `/score <id>`
**Reads:** `pipeline/<id>.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`
**Writes:** the `score{}` block of `pipeline/<id>.json`; advances `discovered → scored`.

You are scoring one opportunity for fit against the candidate's corpus. Score each
dimension **0–10** (integers), then compute a weighted `total`.

## Dimensions & weights
| Dimension | Weight | What it measures |
|---|---|---|
| `fit` | 0.40 | Match between the role's requirements and the candidate's accomplishments/skills. |
| `comp` | 0.20 | How the posted/estimated comp compares to `profile.md` targets. |
| `visa` | 0.15 | Work-authorization compatibility (sponsorship needs vs. what the role offers). |
| `remote` | 0.15 | Location/remote alignment with `profile.md` preferences. |
| `growth` | 0.10 | Scope, learning, trajectory relative to what the candidate optimizes for. |

`total = round(10 * (0.40*fit + 0.20*comp + 0.15*visa + 0.15*remote + 0.10*growth) / 10)`
— i.e. the weighted average on the same 0–10 scale. Show the arithmetic in `notes`.

## Rules
- **PROVENANCE:** any claim that the candidate "has X experience" in `notes` must point to a
  specific `accomplishments/` file. If the job asks for something the corpus can't support,
  say so plainly and let it lower `fit` — do not invent matching experience.
- Missing information (e.g. comp not posted) → score conservatively and note the assumption.
- Be honest about poor fits; a low score is a valid, useful result.

## Output
Update `pipeline/<id>.json`:
- Fill `score`: `{total, fit, comp, visa, remote, growth, notes}` where `notes` carries the
  rationale, the weighting arithmetic, and the corpus citations.
- Append `{ "state": "scored", "date": "<today>" }` to `history[]` and set `state` to
  `scored` (only if currently `discovered`).
- Set a sensible `next_action` (e.g. `/research` or `/tailor`, or "park — low fit").

Then summarize the score and the single most important reason for it.
