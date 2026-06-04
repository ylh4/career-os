---
metric: "+4.3pt 90-day retention from churn-driver segmentation"
tags: [retention, churn, segmentation, sql, python, product-analytics]
date: 2023-05
source: "Churn analysis notebook; retention dashboard; product PRD reference"
---

# Churn-driver segmentation that lifted retention

**Situation:** Sheba Commerce's 90-day retention had been flat for three quarters and no one
could say which customers were leaving or why.

**Task:** Find the actual churn drivers and hand product a prioritized, evidence-backed list.

**Action:** Segmented customers by onboarding completion, first-order category, and support
contact in the first 30 days; ran survival analysis in Python to isolate the factors most
correlated with churn; translated the findings into three concrete product experiments.

**Result:** The top experiment (a guided onboarding fix) shipped and lifted 90-day retention
by **+4.3 percentage points**, validated against a holdout cohort.
