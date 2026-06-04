---
metric: "-31% warehouse compute cost (~$96k/yr saved)"
tags: [bigquery, cost-optimization, sql-tuning, dbt, finops, performance]
date: 2025-04
source: "Cloud billing export; query cost dashboard; optimization changelog"
---

# Cut data-warehouse compute cost

**Situation:** Habesha Pay's BigQuery bill was growing faster than data volume; a handful of
unpartitioned models and full-table dashboard queries dominated spend.

**Task:** Reduce warehouse cost without slowing down analysts or breaking dashboards.

**Action:** Profiled the most expensive queries from billing exports, partitioned and
clustered the heaviest dbt models, replaced SELECT-* dashboard queries with incremental
aggregates, and set per-user query cost guardrails.

**Result:** Warehouse compute cost dropped **31% (~$96k/yr)** with no SLA regressions; the
cost dashboard now governs ongoing usage.
