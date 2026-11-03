# VisaWatch — Counsellor dashboard and official-source monitor

## What this project does
- Responsive dashboard covering UK, Canada, Australia, UAE/Dubai, New Zealand, Europe/Schengen and USA.
- Rules Library, official-source registry, counsellor checklist and Sinhala/English interface controls.
- Python script checks visible text on listed official pages and records monitoring results.
- GitHub Actions workflow is scheduled daily at **09:00 Sri Lanka time (03:30 UTC)**. You can also run it manually from the Actions tab.
- The deployed Cloudflare Worker serves the dashboard and its JSON data files.

## Live website and automated checks
- Website: https://visa-watch.supunchandimal08.workers.dev/
- Repository: https://github.com/supunchandimal08-cell/visa-watch
- Daily monitoring workflow: `.github/workflows/daily-monitor.yml`
- Website validation checks JSON structure, required source entries, Python syntax, data paths and required safety labels.
- Live smoke test checks that the deployed dashboard, `/data/sources.json` and `/data/updates.json` respond and have the expected structure.

## Important accuracy limits
- A page-text change is a detection signal, **not** proof that immigration law or policy changed. Layout, menus, timestamps and unrelated text may trigger it.
- A successful HTTP response only means the page was reachable; it does not mean every rule was reviewed.
- All detected items require a human to verify the exact official page, rule scope, publication date, effective date, exceptions and source evidence before counselling use.
- A failed fetch is recorded as a monitor error and is not equivalent to “no updates.” Some official sites may block automated requests or time out.
- The Rules Library is a counselling research checklist, not legal advice or an approval guarantee. Verify each applicant's situation against current official instructions.
- Never promise visa approval, a job, or part-time work. Confirm the applicant's course, institution, visa conditions, dates and individual eligibility.

## Human review workflow
1. Open the official source link from the dashboard.
2. Compare the relevant official wording, not just the website's appearance.
3. Record the exact rule/topic, source owner, jurisdiction, publication/effective date (if published), date checked, reviewer and evidence/reference.
4. Mark a rule as verified only after a qualified human reviewer confirms it applies to the applicant's intended application date and circumstances.
5. If the page is unreachable or automated access is blocked, leave it marked for manual review. Never interpret a timeout or HTTP 403 as “no change.”

## Run locally
1. Extract this repository or ZIP to a folder.
2. Open a terminal in that folder and run `python monitor.py`.
3. Run `python -m http.server 8000`.
4. Open `http://localhost:8000` in Chrome.

Opening `index.html` directly with a `file://` address may prevent JSON data from loading; use the local server steps above.

## Current deployment configuration
- Static assets are configured in `wrangler.jsonc`; `.assetsignore` limits published assets to the dashboard and required JSON files.
- GitHub Actions validates the repository and performs a live smoke test after relevant changes.
- The daily monitor currently checks source availability and visible-page text fingerprints; it does **not** perform legal interpretation, approve rules, or replace counsellor review.

## One-time Cloudflare GitHub deployment setup

The repository deploys the Worker from GitHub Actions. Add these two repository Actions secrets once:

1. In Cloudflare, create an API token with permission to edit Workers for the account that owns the `visa-watch` Worker. Do not use the Global API Key.
2. In GitHub, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Add `CLOUDFLARE_API_TOKEN` with the token value.
4. Add `CLOUDFLARE_ACCOUNT_ID` with the Cloudflare account ID (not the Worker ID).
5. Do not paste either value into chat, source files, or workflow logs.

After both secrets exist, each relevant push to `main` runs **VisaWatch Cloudflare Deploy**. The workflow deploys the Worker and then checks the live homepage, training page, official-source registry and monitoring JSON. The live smoke test runs only after a successful deployment.

If a deployment fails, open **Actions → VisaWatch Cloudflare Deploy** and inspect the failed step. A missing-secret error means the one-time GitHub secret setup above is incomplete.
