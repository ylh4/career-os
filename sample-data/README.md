# Sample Data — fictitious candidate

Everything in this folder is **invented** for demos, forks, and testing. The candidate
"Dawit Alemu", his employers (Habesha Pay, Sheba Commerce), and the opportunities (DataCo,
FinTrack) do not exist. Metrics are illustrative. It exists so Career OS runs the moment you
clone it — and it's the set we demo and that students fork.

## The candidate
**Dawit Alemu** — an Addis-Ababa-based data analyst targeting **remote Senior BI Analyst**
roles. His corpus shows the full format and a realistic remote-vs-onsite scoring contrast.

## What's here
- `profile.md` — a complete worked profile (skills, target roles, comp floor, location/remote
  prefs, work-authorization status, hard constraints).
- `accomplishments/` — **six** files in the `{metric, tags, date, source}` frontmatter +
  STAR-body format: `reporting-turnaround`, `outreach-reallocation`, `self-serve-dashboards`,
  `data-quality-program`, `churn-cohort-analysis`, `warehouse-cost-cut`.
- `stories/` — **two** interview stories (light frontmatter + narrative):
  `ambiguous-mandate` (→ outreach-reallocation) and `stakeholder-pushback` (→ data-quality-program).
- `pipeline/` — three opportunities across states: `2026-05-dataco-senior-bi` (**scored** 90,
  fully remote, top fit), `2026-05-fintrack-bi-lead` (**tailored** 74, hybrid/relocation), and
  `2026-06-meridian-sr-bi` (**tailored** 88, remote, priority — the `/tailor` demo). Ids follow
  the kernel `YYYY-MM-<company>-<role>` convention.
- `contacts/` — one `.md` per person, frontmatter `{name, role, company, relationship,
  last_touch, next_touch}` + an `## Interactions` log (`priya-raman` — overdue touch demo,
  `selam-tesfaye`, `sara-mehari`). `relationship: recommender` doubles the file as a
  reference / recommendation-letter tracker.
- `artifacts/<id>/` — staged `/tailor` + `/prep` output: `resume_v1.md`, `cover_v1.md`,
  `provenance.md`, and (for Meridian) a `research.md` brief and `prep.md` interview prep — the
  tracked, reviewable sources. The `.docx` deliverables are gitignored render outputs;
  regenerate with e.g.
  `python scripts/render_docx.py sample-data/artifacts/2026-06-meridian-sr-bi/resume_v1.md sample-data/artifacts/2026-06-meridian-sr-bi/cover_v1.md`.
  `2026-06-meridian-sr-bi/` is the worked example: `provenance.md` (provenance map + GAP list)
  and `prep.md` (questions paired with story/accomplishment hooks).

## Use it as a demo
From the repo root, lint the corpus and drive the pipeline helpers against this data:

```bash
python scripts/validate_corpus.py sample-data/accomplishments   # corpus health report

cp sample-data/profile.md corpus/profile.md
cp sample-data/accomplishments/*.md corpus/accomplishments/
cp sample-data/stories/*.md corpus/stories/
cp -r sample-data/contacts/* contacts/ 2>/dev/null; mkdir -p contacts
cp sample-data/pipeline/*.json pipeline/

python scripts/validate.py     # both BI entries should pass
python scripts/report.py       # dashboard with the two opportunities
python scripts/funnel.py       # funnel analytics
```

## Go live
Once you've seen it work, replace the copied files with your own truthful corpus and delete
the demo pipeline entries. Keep `sample-data/` as-is — it's the reference example and the
fixture the repo ships with.

> Note the PROVENANCE discipline even in the demo: every metric in the sample pipeline's
> `score.notes` points back to a specific accomplishment slug, and each story's `source`
> links to the accomplishment it dramatizes. That's the standard real artifacts must meet too.
