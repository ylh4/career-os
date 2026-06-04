---
description: Fetch postings via Apify Actors per profile targets, dedupe, and write new pipeline files (discovered).
argument-hint: "[query/source overrides]  (optional)"
---

Discover new opportunities. **Discovery only — never auto-score** (that's `/score`).

1. Read `corpus/profile.md` for role targets, location/remote prefs, and comp floor; use
   them (plus any `$ARGUMENTS` overrides) to build the search.
2. Use **Apify** Actors (job-board scrapers via the Apify MCP). Check each Actor's input
   schema first. **Cap 25 results per run.** Back off on HTTP 429; watch compute cost.
3. **Dedupe** against existing `pipeline/*.json` (and any new hits) on the key
   **company + title + url**. Skip anything already present — re-running must never create
   duplicates.
4. Preserve each raw scraped posting at `pipeline/_raw/<id>.json` for provenance.
5. For each genuinely new posting, scaffold a pipeline file in `discovered`:
   ```bash
   python scripts/new_opp.py --id <YYYY-MM-company-role> --company "<co>" \
     --title "<title>" --source <referral|linkedin|indeed|company_site|job_board> \
     --url "<url>" --location "<loc>" --comp "<comp>"
   ```
   Use the kernel id convention `YYYY-MM-<company-slug>-<role-slug>` (month = today).

Report how many were fetched, how many were new vs deduped, and the new ids. Then run
`python scripts/validate.py`. Suggest `/score` as the next step. (Do not solve CAPTCHAs or
defeat bot-detection; prefer official application paths — HARD RULE 3.)
