# Checkout service latency rewrite

- **Role / Employer:** Senior Software Engineer @ Nimbus Retail
- **When:** 2023-01 to 2023-09
- **Context:** The checkout service's p99 latency had crept to 1.9s, hurting conversion
  during peak traffic and triggering frequent timeout alerts.
- **Action:** Re-architected the request path — replaced synchronous fan-out with a
  batched, cached aggregation layer; introduced connection pooling and a read-through
  cache; added load-shedding under saturation. Led a team of 3 and owned the rollout.
- **Metric:** Cut p99 latency from 1.9s to 0.72s (-62%); eliminated timeout-driven paging
  (from ~15/week to 0); measured +1.1% checkout conversion in the post-launch A/B test.
- **Skills:** distributed systems, caching, performance, Go, observability, load shedding
- **Source:** Perf dashboard snapshots Q3'25; launch A/B readout deck; promo packet 2024.
