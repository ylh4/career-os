---
description: Discover postings via Apify Actors (LinkedIn + Indeed), dedupe, and write new pipeline files (discovered).
argument-hint: "[--dry-run] [--linkedin-only|--indeed-only] [--cap N] [extra keywords]"
---

Discover new opportunities by scraping job boards through the **Apify MCP**.
**Discovery only — NEVER auto-score** (that's `/score`). Apify tokens are never echoed
(HARD RULE 4); never solve CAPTCHAs or defeat bot-detection (HARD RULE 3).

## Actors (configurable — change these two constants to swap providers)
- **LinkedIn:** `worldunboxer/rapid-linkedin-scraper` — cap param `jobs_entries`.
- **Indeed:** `kaix/indeed-scraper` — cap param `maxItems`.

If you swap an Actor, first call `mcp__apify__fetch-actor-details` for the new one and adjust
the input/output mapping accordingly.

## Steps

1. **Read targets.** Parse `corpus/profile.md` for Role Targets (titles), Location & Remote
   prefs, and any keywords. Apply `$ARGUMENTS` overrides: `--cap N` (default **25**),
   `--linkedin-only` / `--indeed-only`, `--dry-run`, and any extra free-text keywords.

2. **Resolve inputs & caps.** `per_source_cap = ceil(cap / nSources)`. With multiple target
   titles, split per-source cap across them (`cap_param = max(1, per_source_cap // nTitles)`).
   Build each Actor's input:
   - **worldunboxer:** `{ job_title, location: <pref or "Worldwide">, jobs_entries: <cap_param>,
     work_arrangement: "Remote" (if profile is remote-first), posted_within: "Past Month" }`
   - **kaix:** `{ keyword, location: <pref or "remote">, country: <derive from location, else "US">,
     remote: "remote" (if remote-first), maxItems: <cap_param>, searchMode: "basic" }`

3. **Dry-run plan (always print first).** Show, per Actor: `fullName`, the exact input
   object(s), the per-source cap, and an **estimated cost** (`results × per-result price`,
   plus any start fee). If `--dry-run`, **stop here** — make no `call-actor` call.

4. **Fetch.** For each enabled Actor: `mcp__apify__call-actor` with the input, then read
   results with `mcp__apify__get-dataset-items`. **Rate limits:** if any call returns 429 /
   rate-limited, back off exponentially (1s → 2s → 4s, ≤3 retries) and never burst; the Actor
   manages its own scrape rate internally. Keep total results within `cap`.

5. **Normalize** each dataset item to the common shape and keep the original under `raw`:
   `{company, title, url, location, comp, source, description, raw}`.
   - **worldunboxer →** company=`company_name`, title=`job_title`, url=`job_url`,
     location=`location`, comp=`salary_range` (or ""), description=`job_description`,
     source=`"linkedin"`.
   - **kaix →** company=`company.name`, title=`title.text`, url=`urls.indeed` (fallback
     `urls.external`), location=`location.formatted` (or `"Remote"` if
     `workArrangement.isRemote`), comp=`salary.text` (or ""), description=`description.text`,
     source=`"indeed"`.

6. **Ingest (dedupe + write).** Write the normalized array to
   `pipeline/_raw/_incoming.json`, then run:
   ```bash
   python scripts/scan_ingest.py --input pipeline/_raw/_incoming.json --cap <cap>
   ```
   (add `--dry-run` if the command is in dry-run mode). It dedupes on company+title+url
   against existing `pipeline/*.json`, scaffolds `pipeline/<id>.json` in `discovered`
   (id = `YYYY-MM-<company>-<role>`), and saves each raw posting to `pipeline/_raw/<id>.json`.

7. **Report & validate.** Relay the script's summary table (per source: fetched / new /
   duplicates, plus the new ids). Run `python scripts/validate.py`. Suggest `/score` next.
