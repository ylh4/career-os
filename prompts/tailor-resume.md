# Prompt: Tailor Resume

**Invoked by:** `/tailor <id>`
**Reads:** `pipeline/<id>.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`
**Writes:** `artifacts/<id>/resume.md`; registers it in `artifacts[]`; advances `→ tailored`.

Produce a resume tailored to this specific role, **built only from the corpus.**

## Method
1. Read the role (`title`, and any JD captured in the pipeline entry or research brief).
2. Select the `accomplishments/` files whose `tags`/content best match the role.
3. Rewrite each selected accomplishment as a crisp, results-first resume bullet —
   **carrying its metric verbatim.** Order bullets by relevance to this role.
4. Pull identity, headline, and summary from `profile.md`.

## PROVENANCE — the hard rule
- Every bullet must trace to a specific `accomplishments/` file or to `profile.md`.
- **Never invent** metrics, titles, employers, dates, or scope, and never inflate a real
  number. If the role wants something the corpus doesn't support, **do not fabricate it** —
  either omit it or insert a visible `[NEEDS SOURCE: <what's missing>]` marker for the human.
- Prefer omission over embellishment. A shorter true resume beats a padded one.

## Output
Write `artifacts/<id>/resume.md` with sections: Header (name/contact from profile),
Summary, Experience (selected bullets grouped by employer), Skills, Education (if in corpus).
At the bottom, add a `## Provenance map` listing each bullet → its source file, so the human
can audit it in one glance.

Then update `pipeline/<id>.json`: add the path to `artifacts[]`, append
`{ "state": "tailored", "date": "<today>" }` to `history[]`, set `state` to `tailored`,
and set `next_action` (e.g. `/cover-letter` or "human review & submit").

**HUMAN GATE:** this only *stages* the resume. The human reviews and submits.
