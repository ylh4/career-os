---
version: 2.0
---

# Prompt: Score Job

**Invoked by:** `/score [id]` (no id = score all `discovered`)
**Reads:** `pipeline/<id>.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`
**Writes:** the `score{}` block of `pipeline/<id>.json`; advances `discovered → scored`.

You are scoring one opportunity for fit against the candidate's corpus. Score each
dimension **0–10** (integers), then compute the weighted `total` on a **0–100** scale.

## Dimensions & weights
| Dimension | Weight | What it measures |
|---|---|---|
| `fit` | ×3 | Match between the role's requirements and the candidate's accomplishments/skills. |
| `comp` | ×2 | How the posted/estimated comp compares to the `profile.md` floor/targets. |
| `visa` | ×2 | Sponsorship friendliness (sponsorship needs vs. what the role offers). |
| `remote` | ×1.5 | Location/remote alignment with `profile.md` preferences. |
| `growth` | ×1.5 | Scope, learning, trajectory relative to what the candidate optimizes for. |

```
total = round(fit*3 + comp*2 + visa*2 + remote*1.5 + growth*1.5)   # 0–100
```

Show the arithmetic in `notes`.

## Confidence & tiers
- Set `confidence` to `high | medium | low` based on how complete the inputs are
  (comp posted? sponsorship stated? requirements explicit?).
- Tiers for triage: **≥80 priority · 60–79 standard · <60 backup** (tailor only if the
  pipeline thins).

## Rules
- **PROVENANCE:** any claim that the candidate "has X experience" in `notes` must point to a
  specific `accomplishments/` file. If the job asks for something the corpus can't support,
  say so plainly and let it lower `fit` — do not invent matching experience.
- **VISA DEFAULT:** if sponsorship is unstated, score `visa ≤ 5` with `confidence: low` and
  flag the assumption in `notes` — never assume sponsorship friendliness.
- Missing information (e.g. comp not posted) → score conservatively and note the assumption.
- Be honest about poor fits; a low score is a valid, useful result.

## Output
Update `pipeline/<id>.json`:
- Fill `score`: `{total, fit, comp, visa, remote, growth, confidence, notes}` where `notes`
  carries the rationale, the weighting arithmetic, and the corpus citations.
- Append `{ "state": "scored", "date": "<today>" }` to `history[]` and set `state` to
  `scored` (only if currently `discovered`).
- Set a sensible `next_action` (e.g. `/tailor`, or "park — low fit").

Then summarize the score, its tier, and the single most important reason for it.
