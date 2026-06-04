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
- `pipeline/` — two opportunities in different states: `dataco-senior-bi-2026` (**scored**,
  fully remote, top fit) and `fintrack-bi-lead-2026` (**tailored**, hybrid/relocation, lower
  remote score).

## Use it as a demo
From the repo root, lint the corpus and drive the pipeline helpers against this data:

```bash
python scripts/validate_corpus.py sample-data/accomplishments   # corpus health report

cp sample-data/profile.md corpus/profile.md
cp sample-data/accomplishments/*.md corpus/accomplishments/
cp sample-data/stories/*.md corpus/stories/
cp sample-data/pipeline/*.json pipeline/

python scripts/validate.py     # both BI entries should pass
python scripts/report.py       # dashboard with the two opportunities
```

## Go live
Once you've seen it work, replace the copied files with your own truthful corpus and delete
the demo pipeline entries. Keep `sample-data/` as-is — it's the reference example and the
fixture the repo ships with.

> Note the PROVENANCE discipline even in the demo: every metric in the sample pipeline's
> `score.notes` points back to a specific accomplishment slug, and each story's `source`
> links to the accomplishment it dramatizes. That's the standard real artifacts must meet too.
