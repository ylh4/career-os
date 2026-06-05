#!/usr/bin/env bash
# Weekly cadence: discover new opportunities, refresh analytics, commit the results.
#
#   1. /scan   — discovery via headless Claude + the Apify MCP (LLM step)
#   2. funnel  — recompute analytics + reports/pipeline-data.js (deterministic)
#   3. commit  — dated message; COMMIT-ONLY (never pushes unless WEEKLY_PUSH=1)
#
# Prerequisites: `claude` on PATH and authenticated; the Apify MCP usable in this environment
# (an OAuth/http MCP may NOT be authenticated under a bare cron — prefer a Claude Code Routine,
# which runs authenticated, for the /scan step). Pure local; writes only inside the repo.
#
# Wire via cron (Monday 7am):
#   0 7 * * 1  cd /path/to/career-os && ./scripts/weekly.sh >> reports/weekly.log 2>&1
# ...or via a Claude Code Routine (/schedule "Monday 7am ...").
set -euo pipefail

cd "$(dirname "$0")/.."
ts="$(date +%F)"
echo "── weekly run $ts ──"

# 1. Discovery (LLM + Apify MCP). Tools are gated by .claude/settings.json permissions.
if command -v claude >/dev/null 2>&1; then
  claude -p "/scan" || echo "warning: /scan step failed (check claude auth + Apify MCP)"
else
  echo "warning: 'claude' not on PATH — skipping /scan (discovery)"
fi

# 2. Analytics + dashboard data (no LLM needed).
python3 scripts/funnel.py >/dev/null

# 3. Commit results if anything changed (commit-only by default).
git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
else
  git commit -m "chore(weekly): scan + funnel $ts"
  if [ "${WEEKLY_PUSH:-0}" = "1" ]; then
    git push origin "$(git rev-parse --abbrev-ref HEAD)"
  else
    echo "committed locally (set WEEKLY_PUSH=1 to push)"
  fi
fi
echo "── done ──"
