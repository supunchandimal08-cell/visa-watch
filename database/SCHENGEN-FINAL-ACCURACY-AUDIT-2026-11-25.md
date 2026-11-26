# Schengen student-route final accuracy audit — 25 November 2026

**Status:** Structural audit in progress — all country rules remain Pending human review.  
**Scope:** The 29 Schengen countries only. Ireland and Cyprus are not part of this 29-country Schengen list; do not mix EU membership with Schengen membership.

## 1. Correct counselling principle
There is no single long-stay “Schengen student visa” that grants a Sri Lankan student the right to reside and study in every Schengen country. For study longer than 90 days, the student generally needs the destination country's national long-stay visa and/or student residence permit. Short-stay Schengen C visas are for short visits and are not substitutes for national long-stay student permission. The competent national authority in the destination country makes the decision and issues the residence permission. EU Immigration Portal information is a starting point; national authorities and current national law control the case.

## 2. 29-country scope
The 29 Schengen countries are 25 EU countries — Austria, Belgium, Bulgaria, Croatia, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain and Sweden — plus Iceland, Liechtenstein, Norway and Switzerland.

## 3. Structural findings in VisaWatch
- The dashboard's `index.html` has a dedicated `initialSources` source-register array used by the Rules Library. Before this audit, several researched countries had rule references (for example `gr1`, `hu1`, `is1`, `lv1`, `li1`, `lt1`, `lu1`, `mt1`) without corresponding source-register objects. That caused broken/missing source metadata in the dashboard.
- The `data/sources.json` file is consumed by `monitor.py` as the automated change-detection URL list. It is not the full legal source register. It had grown to 240 entries because detailed research references were appended to it. This would cause the monitor to fetch many non-monitoring URLs and create excessive load / unreliable monitoring.
- Corrective action in this audit: restore `data/sources.json` to the eight configured monitoring sources; add missing source metadata for Greece, Hungary, Iceland, Latvia, Liechtenstein, Lithuania, Luxembourg and Malta to `initialSources`. The full detailed country references remain in the country review Markdown files and relevant dashboard rules.
- This audit does not confirm that a URL is reachable, that legal interpretation is correct, or that every country has complete counsellor guidance.

## 4. Country coverage status at audit start
| Country | Existing country-specific review / evidence | Audit finding |
|---|---|---|
| Austria | Dedicated review and four dashboard source records | Review exists; source links available |
| Belgium | Dedicated review and six dashboard source records | Review exists; source links available |
| Bulgaria | Dedicated review and dashboard records | Review exists |
| Croatia | Dedicated review and dashboard records | Review exists; 2026 law amendment needs human confirmation |
| Czechia | Dedicated review and dashboard records | Review exists |
| Denmark | Dedicated review and dashboard records | Review exists; national opt-out from EU immigration directives must be explicit |
| Estonia | Dedicated review and dashboard records | Review exists |
| Finland | Dedicated review and dashboard records | Review exists |
| France | Dedicated review and dashboard records | Review exists |
| Germany | Covered in Europe jurisdiction review; dashboard rules and source records exist | Needs standalone country review file for easier audit |
| Greece | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Hungary | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Iceland | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Italy | Official sources and dashboard rules exist; standalone review file not found in repository tree | Full dedicated review required |
| Latvia | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Liechtenstein | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Lithuania | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Luxembourg | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Malta | Dedicated review exists; source objects were missing from dashboard register | Source metadata restored in this audit |
| Netherlands | Dedicated review and dashboard records exist | Review exists |
| Norway | Dedicated review and dashboard records exist | Review exists; non-EU Schengen state, national rules apply |
| Poland | No dedicated country review or country-specific source-register group found | Research and add country record required |
| Portugal | Dedicated review and dashboard records exist | Review exists |
| Romania | No dedicated country review or country-specific source-register group found | Research and add country record required |
| Slovakia | No dedicated country review or country-specific source-register group found | Research and add country record required |
| Slovenia | No dedicated country review or country-specific source-register group found | Research and add country record required |
| Spain | Dashboard sources/rules exist; standalone review file not found in repository tree | Full dedicated review required |
| Sweden | Dedicated review and dashboard records exist | Review exists |
| Switzerland | No dedicated country review or source-register group found | Research and add country record required; non-EU Schengen state |

## 5. High-risk audit checks required for every country
1. Long-stay route and threshold: D visa, residence permit, direct residence application, or special route; exact 90-day / six-month distinction.
2. Institution and course eligibility: recognised institution, full-time status, qualification level, language and programme conditions.
3. Funds: current national amount, calculation period, family members, acceptable evidence, sponsor/parent rules and tuition/accommodation treatment.
4. Insurance: minimum cover, territory, dates, deductible and exemptions.
5. Work: hourly/week limits, academic-year/holiday rules, employer permit, student permit wording and transitional dates.
6. Post-study: qualification level, duration, deadline, financial conditions and whether it permits work or only job search.
7. Dependants: eligibility, financial and accommodation thresholds.
8. Sri Lanka route: competent embassy, VFS/consulate jurisdiction, appointment and document legalisation.
9. Fees and processing: government fee, VFS fee, service fee and non-guaranteed processing estimates.
10. Current legislation and transition provisions: compare national legal text and authority guidance; record publication date separately from effective date.

## 6. Non-negotiable counsellor warnings
- Never say a Schengen tourist visa can automatically be converted into a student residence permit.
- Never quote one country's funds or work-hours rule for another country.
- Never imply a national student residence permit gives a right to work or settle in all Schengen states.
- A valid residence permit from one Schengen country may permit short visits to other Schengen states within the 90/180 rule; it does not authorise long-term study or employment in another country.
- Student work is conditional; no job or visa outcome is guaranteed.
- Keep every rule Pending human review until the designated reviewer records approval and audit evidence.

## 7. Official cross-country references
- European Commission — EU immigration competence and national authority roles: https://home-affairs.ec.europa.eu/policies/migration-and-asylum/eu-immigration-portal/who-does-what_en
- European Commission — student category, common minimum framework and national variation: https://home-affairs.ec.europa.eu/policies/migration-and-asylum/eu-immigration-portal/what-category-do-i-fit_en
- European Commission — Schengen 29-country list and short/long stay student visa distinction: https://education.ec.europa.eu/uk/news/student-visas-in-europe-what-you-need-to-know

---
This is an operational data-quality audit, not legal approval. National legal sources and Sri Lanka consular instructions must be rechecked at each client's intended filing date.


## 7. Follow-up structural verification — 26 November 2026

This follow-up is a repository/data-integrity check, not a legal opinion or approval of immigration rules.

- The current `index.html` contains **279 unique source IDs**. No duplicate IDs were found.
- The dashboard contains **244 rule objects** across **35 country/jurisdiction labels** (including the Europe / Schengen overview and Ireland, which is not in Schengen).
- The 244 rule objects use **153 distinct primary source references**; every referenced ID resolves to a source ID present in the deployed HTML. No missing primary source references were found.
- Rule-status labels currently include: **229 Pending human review**, **11 Needs official-country verification**, **2 Country-specific**, **1 Scope check**, and **1 Proposed — not yet in force**. The remaining entries use computed/derived status labels. Do not convert any of these to approved merely because the structural validation passes.
- `data/sources.json` contains **20 unique HTTPS monitoring URLs**. This is the monitor list, not the complete Rules Library source register. This check confirms URL shape and uniqueness, not live reachability or legal currency.
- The repository contains country review documents for the main destinations and Schengen countries, plus Ireland and a separate USA F-1 review. The detailed review files are supporting research records; they do not replace a qualified human review of each rule.
- GitHub Actions for commit `75a32ed8f5f741fe27e07cd763199f7893048569` completed successfully: Website Validation, Daily Monitoring, and GitHub Pages build/deployment. This confirms those workflows completed for that commit; it does not certify legal accuracy or the separate Cloudflare Worker deployment.

### Release decision

**Technical website deployment: passed for the above commit. Legal/content release: not yet approved.** Before presenting the Rules Library as verified advice, a designated senior reviewer must resolve the 11 country-verification items, review the 229 pending rules and the special-status entries, confirm the underlying official URLs and effective dates, and record reviewer/date/decision in the system. In particular, conflicting or time-sensitive items identified in the country review files (including Latvia funds/work/post-study, Lithuania insurance and Sri Lanka application route, Romania student work hours, Slovenia funds, and Croatia's 2026 amendment) require explicit source-level sign-off.

**Client records: not released.** The company has no approved client-record system yet. The documented workflow remains a proposal; do not store real client data until management/privacy approval, authentication, database row-level security, role-based security tests, backup/restore tests, staff training and written release sign-off are complete.
