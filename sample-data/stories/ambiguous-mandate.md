---
themes: [ambiguity, influence, stakeholder-management, business-impact]
tags: [bi, analytics, marketing-analytics]
source: "[outreach-reallocation]"
---

# Turning "is our outreach working?" into a $1.2M decision

So at Sheba Commerce we were spending about $3.1M a year on outreach, split more or less
evenly across channels — and it was split evenly mostly because no one could prove it
shouldn't be. The CMO asked me a deceptively simple question one Monday: "Is our outreach
actually working?" No brief, no definition of "working," no owner. Just that.

I decided the first job was to make the question answerable rather than argue about it. I
went back and reframed "working" as: which channels bring customers who actually stay and
contribute margin, not just who sign up. Then I built customer cohorts by acquisition
channel in SQL and Python, tracked 90-day retention and contribution margin per cohort, and
controlled for seasonality so we weren't fooled by a good quarter.

What came back was stark — two channels were essentially break-even once you accounted for
churn, while three others were running about 3x ROI. The hard part wasn't the analysis, it
was getting finance and marketing to act on it without it feeling like an attack on the
marketing team's past calls. So I framed it as "here's where the next dollar goes furthest"
rather than "here's what you got wrong," and I walked them through the cohort curves live so
they could poke at the assumptions.

Finance reallocated **$1.2M** from the break-even channels into the three high-ROI ones, and
over the next two quarters our blended retained-customer CAC improved 27%. The lasting win
was cultural: budget conversations started opening with "what do the cohorts say?"

What I took from it: when a mandate is vague, the highest-leverage move is to turn it into a
measurable question first — most of the disagreement evaporates once people are looking at
the same curve.
