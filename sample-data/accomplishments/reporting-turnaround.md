---
metric: "-62% reporting turnaround (5 days → 1.9 days)"
tags: [sql, dbt, automation, reporting, etl, power-bi]
date: 2024-07
source: "BI ops runbook; before/after cycle-time log; manager attestation"
---

# Automated the weekly executive reporting pipeline

**Situation:** At Habesha Pay, the exec team waited ~5 business days each week for a deck
hand-assembled from six spreadsheets, and the numbers often disagreed across slides.

**Task:** Cut the turnaround and end the version-mismatch problem without adding headcount.

**Action:** Modeled the source tables in dbt with tested, documented marts; replaced the
manual spreadsheet stitching with a scheduled SQL → Power BI refresh; added freshness and
row-count tests that block a publish on bad data.

**Result:** Reporting turnaround dropped from 5 days to **1.9 days (-62%)**, the exec deck
now refreshes from a single governed source, and cross-slide discrepancies fell to zero.
