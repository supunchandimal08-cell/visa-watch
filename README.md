# VisaWatch — Counsellor dashboard and official-source monitor

## What this project does
- Responsive dashboard covering UK, Canada, Australia, UAE/Dubai, New Zealand, Europe/Schengen and USA.
- Rules Library, official-source registry, counsellor checklist and Sinhala/English interface controls.
- Python script checks visible text on listed official pages and records a `Needs review` item when a page fingerprint changes.
- GitHub Actions workflow is scheduled daily at 08:30 Sri Lanka time (03:00 UTC). You can also run it manually from the Actions tab.

## Important accuracy limits
- A page-text change is a detection signal, NOT proof that immigration law or policy changed. Layout, menus, timestamps and unrelated text may trigger it.
- All detected items require a human to verify the exact official page, rule scope, publication date, effective date, exceptions and source evidence before counselling use.
- A failed fetch is recorded as a monitor error and is not equivalent to “no updates.” Some official sites may block automated requests.
- No sample immigration updates are preloaded as current facts. The Rules Library is a checklist for counsellors, not legal advice or an approval guarantee. Verify each applicant's situation against current official instructions.

## Run locally
1. Extract this ZIP to a folder.
2. Open a terminal in that folder and run `python monitor.py`.
3. Run `python -m http.server 8000`.
4. Open `http://localhost:8000` in Chrome.

Opening `index.html` directly with a `file://` address may prevent JSON data from loading; use the local server steps above for a meaningful test.

## Enable scheduled monitoring
1. Create a GitHub repository and upload the extracted project files (including the hidden `.github` folder).
2. In the repository, open **Settings → Actions → General** and allow workflows to run.
3. In **Actions**, enable the workflow if GitHub shows it as disabled. Run it manually once and inspect its logs.
4. Confirm the workflow can commit `data/monitor_state.json` and `data/updates.json`. The workflow needs repository contents write permission; organization policy may override this.
5. Review the first run for source errors before relying on results.

## Deployment and alerts
The deployed static dashboard does not include login, role-based access, a shared database, or browser push notifications. The scheduled workflow writes monitoring results to the repository; ensure the hosting deployment publishes the updated `data/updates.json` and `data/sources.json` for the dashboard to read. A browser-only static page cannot run a reliable daily monitor while closed. Do not put client personal data or confidential company information in a public repository.
