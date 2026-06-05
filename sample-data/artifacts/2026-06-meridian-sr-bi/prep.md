# Interview prep — Meridian Health · Senior BI Analyst

> Built from `research.md` (sample brief) + `corpus/stories/` + `corpus/accomplishments/`.
> A live `/prep` would source the company facts from the Apify RAG Web Browser; here they come
> from the seeded sample brief.

## Role & company snapshot (from research.md)
- Digital-health company; mission to make care decisions genuinely data-driven; remote-first.
- Role owns decision-support analytics + governed self-serve reporting for product/ops.
- Stack signals: SQL, dbt, semantic layer (Looker/Power BI), data-quality testing, BigQuery/Snowflake.

## Likely questions, each with an answer hook
**Behavioral**
- *"Tell me about a time you were handed an ambiguous mandate."*
  → **story: ambiguous-mandate** (themes: ambiguity, influence) — reframed "is our outreach
  working?" into cohort analysis that **reallocated $1.2M** to 3x-ROI channels.
- *"Describe a time stakeholders pushed back / you lost credibility on data."*
  → **story: stakeholder-pushback** (themes: conflict, trust, data-quality) — owned the bad
  numbers, added dbt tests + a signed-off data dictionary, cut reporting defects **78%**.
- *"How do you drive adoption of self-serve analytics?"*
  → **accomplishment: self-serve-dashboards** — semantic layer + ~20 Looker dashboards grew
  usage **0 → 180 weekly active users in 6 months**.

**Technical / role**
- *"How do you keep a BI layer trustworthy at scale?"*
  → **accomplishment: data-quality-program** — dbt tests (not-null/uniqueness/accepted-values)
  + data dictionary, **−78% defects**.
- *"Walk me through optimizing a slow/expensive warehouse."*
  → **accomplishment: warehouse-cost-cut** — SQL/dbt tuning on BigQuery, **−31% (~$96k/yr)**.
- *"How do you measure retention / cohorts?"*
  → **accomplishment: churn-cohort-analysis** — churn-driver segmentation, **+4.3pt 90-day retention**.
- *"How do you speed up executive reporting?"*
  → **accomplishment: reporting-turnaround** — dbt marts + SQL→Power BI, **−62% (5d→1.9d)**.

## STAR bank (metrics verbatim)
- **Ambiguous mandate → $1.2M reallocation** (ambiguous-mandate): S—$3.1M outreach split evenly,
  no proof; T—make "is it working?" answerable; A—cohorts by channel in SQL/Python, 90-day
  retention + contribution margin, controlled for seasonality; R—finance moved **$1.2M** to 3x-ROI
  channels, blended retained-CAC improved 27%.
- **Restoring data trust → −78% defects** (stakeholder-pushback): S—stakeholders catching wrong
  numbers; T—rebuild trust; A—dbt tests alerting pre-publish + a signed-off data dictionary;
  R—defects **23 → 5/qtr (−78%)**, exec started citing the dashboards.

## Questions to ask them
- How does Meridian currently govern metric definitions across product and ops? (ties to my
  data-dictionary work)
- What's the split between net-new modeling vs. maintaining existing reporting in year one?
- How are analytics decisions actually acted on — who owns the "what do we do about it"?
- Remote/EOR logistics for a non-US contributor (per the open question in the brief).

## Risks & gaps (candid)
- **GAP: healthcare / claims / clinical (HIPAA) data.** No corpus experience — I'd be honest:
  strong transferable BI/governance, no health-data domain yet; quick to ramp on the data model.
- **GAP: managing a team of analysts.** I've led initiatives and run data-literacy enablement,
  but no direct reports — frame scope accurately.
