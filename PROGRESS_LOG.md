# Nightlies — Progress Log

**Repo:** https://github.com/The412Banner/Nightlies
**Local path:** `/data/data/com.termux/files/home/Nightlies`
**Rules:** No pull requests ever. Log every change. Push commits as needed.

---

## Session — 2026-03-06

### [feat] — Dynamic release notes + upstream change tracking (2026-03-06)
**Commit:** `c783331`

#### What changed

**Upstream-watcher.yml:**
- Added `NAMES` array mapping each repo URL to a friendly display name
- Before overwriting `upstream_hashes.txt`, captures old hash per repo to detect what changed
- For each changed repo: fetches commit message + date from GitHub API
- Builds `CHANGED_JSON` array (repo, name, old hash, new hash, full hash, message, date)
- Writes `upstream_changes.json` with `triggered_at` timestamp + `changed` array
- Commits both `upstream_hashes.txt` and `upstream_changes.json` when changes detected
- Triggers `new-All-in-one-nightly+zips-latest-stable.yml` (unchanged trigger mechanism)

**new-All-in-one-nightly+zips-latest-stable.yml (create-release job):**
- Added `actions/checkout@v4` step so the job can read `upstream_changes.json`
- Added `Build Release Body` step:
  - Queries GitHub API live for all 6 upstream repos (latest commit hash, message, date)
  - Marks any repo updated in last 24h with 🆕 badge in status table
  - Reads `upstream_changes.json` — if written within the last 3 hours, generates "🔄 What Triggered This Build" table with old→new commit links
  - Writes full release body to `release_body.md`
- Switched from `body:` (static inline) to `body_path: release_body.md` in softprops action
- Added disclaimer to top of every nightly release body:
  `⚠️ DISCLAIMER: NIGHTLY BUILDS ARE NOT ALWAYS STABLE OR RECOMMENDED! USE AT YOUR OWN RISK! STABLE RELEASES ARE ALWAYS BEST TO USE!`

#### Files touched
- `.github/workflows/Upstream-watcher.yml`
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`

---

### [chore] — Disclaimer added to all existing nightly releases (2026-03-06)
**Method:** `gh release edit` loop via CLI (no commit)

#### What changed
- Prepended disclaimer to all 9 existing nightly release descriptions:
  - nightly-20260306-143533
  - nightly-20260306-135338
  - nightly-20260306-124048
  - nightly-20260306-112704
  - nightly-20260306-103204
  - nightly-20260306-090646
  - nightly-20260306-073819
  - nightly-20260305-223528
  - nightly-20260305-192208
- Non-nightly releases (Steam-clients, Bionic-Ludashi-proton, Box64, FexCore, etc.) left untouched

---

### [docs] — Progress log created (2026-03-06)
**Commit:** (this file)
#### What changed
- Created PROGRESS_LOG.md to track all changes to this repo going forward
