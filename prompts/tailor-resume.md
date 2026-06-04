---
version: 2.0
---

# Prompt: Tailor Resume + Cover Letter

**Invoked by:** `/tailor [id]`
**Reads:** `pipeline/<id>.json`, `corpus/profile.md`, `corpus/accomplishments/*.md`,
`artifacts/<id>/research.md` (if present, for company hooks)
**Writes:** `artifacts/<id>/resume_vN.md`, `artifacts/<id>/cover_vN.md`,
`artifacts/<id>/provenance.md`, and the rendered `*.docx`; registers them in `artifacts[]`;
advances `scored → tailored`.

Produce a resume **and** cover letter tailored to this role, **built only from the corpus.**

## Versioning
Pick `N` = the next version: if `artifacts/<id>/resume_v1.docx` exists, use `v2`, and so on.
Never overwrite a previous version — each `/tailor` run stages a fresh `vN`.

## Method
1. Read the role (`title`, JD captured in the pipeline entry or research brief).
2. Select the `accomplishments/` files whose `tags`/content best match the role.
3. Rewrite each selected accomplishment as a crisp, results-first resume bullet —
   **carrying its metric verbatim.** Order bullets by relevance to this role.
4. Pull identity, headline, and summary from `profile.md`.
5. Draft the cover letter (3–4 short paragraphs, under ~250 words) following
   `prompts/cover-letter.md`: hook (company, from the research brief), proof (1–2
   corpus accomplishments with real metrics), fit & forward.

## PROVENANCE — the hard rule
- Every résumé bullet and every cover-letter claim must trace to a specific
  `accomplishments/` file or to `profile.md`; company claims trace to `research.md`.
- **Never invent** metrics, titles, employers, dates, or skills, and never inflate a real
  number. If the posting demands a claim the corpus cannot support, **do not fabricate it** —
  emit a `GAP: <what's missing>` flag instead. Prefer omission over embellishment.

## Output — three markdown sources + rendered .docx
1. `artifacts/<id>/resume_vN.md` — Header (name/contact from profile), Summary, Experience
   (selected bullets grouped by employer), Skills, Education (if in corpus).
2. `artifacts/<id>/cover_vN.md` — the cover letter.
3. `artifacts/<id>/provenance.md` — a table mapping **each claim → source file** (e.g.
   `"-62% reporting turnaround" → accomplishments/reporting-turnaround.md`), plus any `GAP:`
   flags. This file ships with every tailored resume (HARD RULE 1).
4. Render the two `.docx` deliverables:
   ```bash
   python scripts/render_docx.py artifacts/<id>/resume_vN.md artifacts/<id>/cover_vN.md
   ```
   (`.docx` files are gitignored exports — the `.md` sources and `provenance.md` are the
   tracked, reviewable artifacts.)

Then update `pipeline/<id>.json`: add the `resume_vN.docx`, `cover_vN.docx`, and
`provenance.md` paths to `artifacts[]`, append `{ "state": "tailored", "date": "<today>" }`
to `history[]`, set `state` to `tailored`, and set `next_action` (e.g. "human review &
submit", then `/submit`). Run `python scripts/validate.py`.

**HUMAN GATE:** this only *stages* the resume and letter. The human reviews and submits.
Refuse to run if `python scripts/validate_corpus.py` fails — never tailor on a broken corpus.
