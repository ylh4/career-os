# Zero-downtime database migration

- **Role / Employer:** Staff Software Engineer @ Nimbus Retail
- **When:** 2024-02 to 2024-08
- **Context:** A 40-engineer org was blocked by a single overloaded Postgres primary;
  scaling and schema changes had become high-risk and slow.
- **Action:** Designed and led a zero-downtime migration to a horizontally sharded
  topology with dual-write/backfill/cutover phases. Wrote the migration runbook, built the
  shadow-read verification harness, and coordinated 6 teams through the cutover.
- **Metric:** Migrated 4.2 TB across 12 shards with **zero downtime** and zero data-loss
  incidents; unblocked schema changes (lead time dropped from ~2 weeks to ~1 day); write
  headroom increased ~8x.
- **Skills:** databases, sharding, migrations, technical leadership, cross-team coordination
- **Source:** Migration runbook (internal wiki); cutover postmortem (no incidents); promo
  packet 2024 — Staff.
