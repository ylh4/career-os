# Sample Data — fictitious candidate

Everything in this folder is **invented** for demos, forks, and testing. The candidate
"Maya Chen", her employers (Nimbus Retail), and the opportunities (Acme Cloud, Globex) do
not exist. Metrics are illustrative. It exists so Career OS runs the moment you clone it.

## What's here
- `profile.md` — a complete worked profile.
- `accomplishments/` — four accomplishment files showing the one-achievement-per-file format
  (`latency-rewrite`, `team-lead-migration`, `cost-savings`, `oss-contribution`).
- `stories/` — two STAR stories (`conflict-resolution`, `ambiguous-project`).
- `pipeline/` — two opportunities in different states: `acme-staff-eng-2026` (**scored**)
  and `globex-platform-2026` (**tailored**).

## Use it as a demo
From the repo root you can drive the helpers against this data by copying it into the live
folders:

```bash
cp sample-data/profile.md corpus/profile.md
cp sample-data/accomplishments/*.md corpus/accomplishments/
cp sample-data/stories/*.md corpus/stories/
cp sample-data/pipeline/*.json pipeline/

python scripts/validate.py     # both entries should pass
python scripts/report.py       # dashboard with the two opportunities
```

## Go live
Once you've seen it work, replace the copied files with your own truthful corpus and
delete the demo pipeline entries. Keep `sample-data/` as-is — it's the reference example
and the fixture the repo ships with.

> Note the PROVENANCE discipline even in the demo: every metric in the sample pipeline's
> `score.notes` points back to a specific accomplishment file. That's the standard real
> artifacts must meet too.
