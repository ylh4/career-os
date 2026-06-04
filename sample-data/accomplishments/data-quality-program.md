---
metric: "-78% reporting defects (avg 23 → 5 per quarter)"
tags: [data-quality, dbt, testing, data-dictionary, governance, sql]
date: 2024-12
source: "Defect tracker; dbt test coverage report; data dictionary (internal wiki)"
---

# Stood up a data-quality program

**Situation:** Stakeholders kept catching wrong numbers in dashboards at Habesha Pay,
eroding trust — most traced to silent upstream schema changes and undefined metrics.

**Task:** Cut reporting defects and rebuild confidence in the numbers.

**Action:** Added dbt tests (not-null, uniqueness, accepted-values, relationships) across
the core marts, wired test failures into an alert that pages before publish, and authored a
data dictionary that pinned a single owner and definition to every key metric.

**Result:** Reporting defects fell from ~23 to ~5 per quarter (**-78%**); the dictionary
became the team's source of truth and onboarding cut from weeks to days.
