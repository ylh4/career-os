# Disagreement over the migration cutover plan

- **Themes:** conflict, influence, technical leadership, decision-making
- **Situation:** During the database migration (2024), a senior peer pushed hard for a
  big-bang cutover to save weeks; I believed it carried unacceptable data-loss risk for a
  40-engineer org.
- **Task:** Reach a decision the whole group could commit to without it becoming a standoff.
- **Action:** Instead of arguing in the abstract, I built a small shadow-read harness that
  quantified divergence risk on real traffic, and laid out a phased dual-write/backfill plan
  with explicit rollback gates. I invited the peer to co-own the verification step.
- **Result:** The data changed the conversation — we went phased and migrated 4.2 TB across
  12 shards with **zero downtime and zero data loss**. The peer became the plan's strongest
  advocate.
- **Source:** Ties to [team-lead-migration]; cutover postmortem (no incidents).
- **Reflection:** Turning a values clash into a measurable question defused the conflict and
  produced a better plan than either of us started with.
