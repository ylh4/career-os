---
themes: [conflict, influence, trust, data-quality, communication]
tags: [bi, governance, data-quality]
source: "[data-quality-program]"
---

# Rebuilding trust after stakeholders kept catching wrong numbers

At Habesha Pay we hit a rough patch where stakeholders kept finding wrong numbers in the
dashboards — and once that happens, people stop trusting *all* the numbers, even the correct
ones. In one steering meeting an exec basically said, "I can't make decisions on data I have
to double-check." That stung, but he was right, and arguing the data was "mostly fine" would
only have made it worse.

So instead of defending, I owned it. I asked for two weeks to find the root cause before
promising any fix. When I dug in, most of the bad numbers traced back to two things: silent
upstream schema changes that broke models without anyone noticing, and metrics that had no
agreed definition, so two dashboards could both be "right" and still disagree.

I tackled both. I added dbt tests across the core marts — not-null, uniqueness,
accepted-values, relationships — and wired failures to alert *before* anything published, so
we'd catch breakage instead of stakeholders catching it. Then I wrote a data dictionary that
gave every key metric a single owner and a single definition, and I got the steering group to
literally sign off on those definitions so they were bought in, not just informed.

Reporting defects dropped from around 23 to about 5 per quarter — a **78% reduction** — and
the dictionary became the team's source of truth; new analysts onboarded in days instead of
weeks. The exec who'd called it out started citing the dashboards in his own reviews, which
told me the trust was back.

The lesson I carry: when you've lost credibility on data, you don't win it back with a
better chart — you win it back by making the system visibly hard to get wrong, and by letting
the doubters own the definitions.
