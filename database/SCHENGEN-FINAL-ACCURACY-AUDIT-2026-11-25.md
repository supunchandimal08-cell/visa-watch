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


## 8. Targeted official-source recheck — 26 November 2026

The following live official pages were reopened after the structural audit. These findings refine the unresolved-risk list; they do not approve the dashboard entries.

### Romania — student work-hours discrepancy can be narrowed
- The Romanian General Inspectorate for Immigration (IGI) current dedicated “Studies” page states that a foreign student holding temporary residence for study may work under an individual part-time employment contract for **up to 6 hours per day without a separate work permit**. It also describes the long-stay study visa, visa-stage funds at the national gross minimum salary for the visa period, EUR 30,000 medical insurance, residence-stage funds for at least six months, and a 9-month post-graduation job-search / employment / business-formalities extension.
- Official page: https://igi.mai.gov.ro/en/studies/
- The older alternate IGI English page still contains a 4-hour statement, so the country review should retain the discrepancy note and direct counsellors to recheck the current dedicated Studies page and current legal text at the client's filing date. Do not use the old 4-hour text as the current rule without explaining the conflict.

### Latvia — current general residence subsistence table
- PMLP's “The necessary subsistence” page is updated **16 March 2026** and says that from **1 April 2026** the general amount for cases not otherwise specified is **EUR 780/month**, with EUR 234/month for a minor child. The page sets out different amounts for employment and other categories.
- Official page: https://www.pmlp.gov.lv/en/necessary-subsistence-0
- This strengthens the basis for using EUR 780 as a cautious planning reference, but does **not by itself establish that this is the student-specific legal threshold or the required evidence period**. Keep the dashboard rule marked for official-country verification until PMLP confirms the student category and calculation in writing or the primary legal provision is mapped.

### Slovenia — student-specific guidance remains lower and conflicts with general minimum-income figures
- The Study in Slovenia student permit page currently displays **EUR 484.88/month** as the student financial-means figure and lists the student permit fee / application fee / card printing fee. Official page: https://studyinslovenia.si/live/visa-and-residence-permit/temporary-residence-permit-for-studies/
- The broader Study in Slovenia guide still displays EUR 494.09/month in its FAQ. The two national student-information pages are inconsistent, and a higher general minimum-income amount should not automatically be substituted for a student-specific threshold without confirming the applicable statutory calculation. Keep funds unresolved and request written confirmation from the competent Administrative Unit / InfoTujci.

### Lithuania — remain unresolved
- The current review's key risks remain: Singapore as the listed overseas TRP / national visa service point for a Sri Lankan applicant (individual eligibility must be confirmed), different insurance figures on EU and university pages, and 2026 work-hour changes by Bachelor year and TRP issue date. No change to the release decision is justified from this targeted search alone.

### Release effect

The Romania evidence is now stronger for the 6-hour-per-day rule on the current IGI Studies page, but should still be signed off by a reviewer. Latvia's EUR 780 and Slovenia's student-specific EUR 484.88 are recorded as evidence, not universal guaranteed visa-fund requirements. All affected dashboard records remain in human-review status. No immigration rule is marked legally approved by this follow-up.

## 9. Targeted official-source recheck — 26 November 2026

### Latvia
- Rechecked PMLP's necessary-subsistence page: updated 16 March 2026; from 1 April 2026 it states EUR 780/month in cases not otherwise specified and EUR 234/month for a minor child. This is not an explicit student-specific determination. Retain EUR 780 as a cautious planning reference only; request written PMLP confirmation of the student calculation, evidence period and accepted sponsor/bank evidence.
- Rechecked the Integration and Inclusion Agency's international-student guidance: full-time Bachelor's students may work up to 20 hours/week during studies and 40 hours/week during study holidays; full-time Master's and PhD students may work without an hours restriction. Confirm programme status, permit conditions and current law. Do not include assumed wages in proof-of-funds calculations.

### Slovenia
- Rechecked the Study in Slovenia student-permit page: it still displays EUR 484.88/month. GOV.SI's 2026 basic minimum-income table states EUR 507.43 from 1 March 2026. The available official material does not reconcile the student-specific test. The October 2026 proposal to increase general sufficient means is not proof of enactment. No definitive amount is approved; obtain the competent Administrative Unit's written calculation, evidence period and sponsor rules.

### Romania
- Rechecked the current dedicated IGI Studies page and Study in Romania government work page: both state up to 6 hours/day for a non-EU student holding study residence, under the applicable individual part-time employment contract without a separate work permit. An older/alternate IGI English page has displayed 4 hours; retain the discrepancy and request IGI confirmation where material. This does not authorise full-time work, self-employment or guarantee a job.

### Dashboard changes
- Added three country-specific recheck records to `index.html`, all marked **Pending human review** and linked to existing national sources: Latvia funds/work, Slovenia funds discrepancy, Romania 6-hour work rule.
- No rule was marked legally approved. No final Slovenia student-funds threshold was asserted. No Latvia EUR 780 student-specific legal conclusion was asserted.
- Website validation and Pages deployment for the new commit must complete successfully before treating this dashboard revision as published.


## 10. Poland official-source research — 26 November 2026

A dedicated Poland student-route review was added at `database/POLAND-STUDENT-SOURCE-REVIEW-2026-11-26.md`. This closes the missing-document gap identified in section 4, but does not certify Poland's dashboard entries.

Key evidence and controls:
- Current MOS / Office for Foreigners study guidance gives PLN 1,010 per month for a single applicant and PLN 823 for the applicant and each dependant, with actual housing costs and return funds assessed separately. The older EU Immigration Portal page dated 16 September 2025 displays PLN 776 / PLN 600; retain this as a documented discrepancy and do not quote the older figures as current without authority confirmation.
- The government-supported study.gov.pl page says that from 27 April 2026, study-purpose temporary residence applications are submitted electronically through MOS. This must not be confused with initial national D-type visa filing.
- Study.gov.pl guidance describes a work-permit exemption for eligible non-EU full-time students whose stay is based on a Polish study D visa or study residence permit; part-time / other residence categories may differ. Studies remain the main purpose; no expected wages are to be counted as proof of funds.
- Study.gov.pl describes a possible one-time nine-month graduate temporary residence permit for job-search / business purposes, subject to eligibility. A work-permit exemption after graduation does not itself extend lawful stay.
- The official Poland-in-India D-study visa page lists Sri Lanka within the New Delhi Embassy's jurisdiction and gives e-Konsulat / in-person VAC instructions. Recheck current appointment and VAC details before advising or payment.

Official source URLs are recorded in the Poland review document. All Poland entries must remain **Pending human review** until a senior reviewer confirms the current law, programme eligibility, funds calculation, insurance checklist, consular route and exact work conditions.

### Release effect
Poland now has a dedicated source review file. No Poland rule has been marked legally approved, and no dashboard change is claimed in this section. This is a research/documentation improvement only. Website validation and Pages deployment status must be checked for the latest repository commit before describing any new content as live.


## 9. Portugal targeted official-source recheck — 26 November 2026

- Existing Portugal review file was re-opened and checked against current AIMA, Diário da República and gov.pt pages.
- AIMA's means-of-subsistence page still displays the 2025 minimum wage (€870). The 2026 statutory minimum wage is €920 under Decreto-Lei n.º 139/2025; use the latter for 2026 calculations and flag AIMA's annual figure as stale.
- Portaria n.º 1563/2007 Article 5(4) requires means for 12 months (or exchange-programme duration), calculated by reference to minimum wage. The amount may be reduced by half where accommodation is provided, or up to 90% where both accommodation and food are provided, subject to acceptable evidence and assessment.
- AIMA Article 91 confirms higher-education permit requirements, three-year validity (or programme duration if shorter), and work rights for the relevant permit category under Article 97. The current consolidated Article 97 does not set a general weekly-hour cap in paragraph 1.
- Lei n.º 62/2026 is effective 11 September 2026 and revoked Article 91(4). Do not advise the former in-country higher-education conversion route without a prior residence visa.
- gov.pt's D4 page warns it may be outdated; use current MNE / Embassy instructions for filing. For Sri Lankan applicants, confirm New Delhi filing and VFS residence eligibility directly before booking or legalising originals.
- Dashboard source pt11 now records the primary Portaria legal text. Source pt2 explicitly warns that AIMA's page still displays the 2025 wage figure. Existing Portugal rules remain Pending human review.

### Portugal release status

**Research refresh completed; legal approval not granted.** The 2026 funds benchmark is €11,040 for one adult over 12 months before any evidence-based reduction; it is a calculation from the statutory €920 monthly minimum wage, not a universally published fixed bank-balance requirement. The Article 91 work rule must not be extended to secondary students, unpaid trainees or volunteers. Embassy/VFS filing eligibility for Sri Lankan residents remains a live operational confirmation.



## 10. Slovakia targeted official-source recheck — 26 November 2026

- Rechecked Slovak MFA residence guidance and Ministry of Labour indexation. Section 24 study residence may cover the expected study duration up to six years; university study has a separate checklist. The one-adult subsistence minimum effective 1 July 2026 is EUR 295.22/month, making EUR 3,542.64 the 12-month statutory means calculation. This is not tuition or a realistic all-in living-cost budget.
- Rechecked the New Delhi Embassy university D visa checklist: EUR 90 administrative fee, passport, admission decision in Slovak, criminal records with required legalisation/translation, flight reservation and 120-day health cover. The EUR 56/day amount belongs to the separate language-school checklist, not the university D visa checklist.
- Added a source record for the Embassy 10 August 2026 academic-year 2025/2026 appointment notice. Institution submits appointment request; applicants/agents cannot request directly. After BLS/VFS submission, mandatory Embassy interview is scheduled for the following day. Confirm the 2026/2027 procedure before filing.
- Sri Lankan public documents require relevant Sri Lankan MFA legalisation followed by Slovak Embassy New Delhi superlegalisation. Italy representation in Colombo applies to short-stay Schengen visa applications only; it does not establish Slovak national D visa handling.
- University students holding study-purpose temporary residence may work up to 80 hours/month without an employment permit. Eligible university graduates may apply for a nine-month job-search/business extension subject to requirements. Neither work nor post-study extension guarantees employment.
- Slovakia dashboard remains **Pending human review**. The current academic-year appointment schedule and applicant-specific consular acceptance remain operational checks.


## 11. Spain targeted official-source recheck — 26 November 2026

- Rechecked the Spanish Ministry of Inclusion study-stay guidance, New Delhi Embassy's current English study-visa checklist, and Royal Decree 1155/2024 on BOE. The national study visa is for eligible stays exceeding 90 days; it must not be conflated with a Schengen short-stay C visa.
- New Delhi's official checklist explicitly gives the 2026 maintenance reference as EUR 600/month for the student, EUR 450/month for the first accompanying family member and EUR 300/month for each additional family member. It requests original sponsor bank statements for the previous six months, signed and stamped. A 12-month student-only calculation is EUR 7,200; tuition and return costs remain separate, and pre-paid accommodation may reduce the maintenance amount under the applicable rule.
- Article 57 provides automatic employed/self-employed work permission for eligible higher-education study authorisations where work is compatible with studies. General limit: 30 hours/week, subject to the intensive vocational-training exception; work is geographically limited to the autonomous community of the study authorisation, with the statutory neighbouring-locality exception. This is not a job or income guarantee.
- The New Delhi Embassy confirms Sri Lanka is in its consular district; Colombo is an honorary consulate. The Embassy's current study-visa page directs applicants to BLS VAC by prior appointment, but the exact currently designated centre and acceptance procedure for Sri Lankan residents must be confirmed directly. Do not infer that an India-based VAC is accessible.
- Current checklist requires Spain-authorised health insurance with broad public-health-equivalent cover and, for adult applicants staying over 180 days, criminal-record certificates covering the previous five years of residence and a medical certificate. Indian PCC/apostille instructions must not be copied to Sri Lankan applicants; confirm Sri Lankan issuing, legalisation and translation steps with the Embassy.
- Eligible graduates reaching at least EQF level 6 may qualify for the job-search/business-project residence route under Article 190(10) and Law 14/2013. It is not automatic for every course and does not itself authorise work.
- Dashboard sources es1–es3 were refreshed to the current New Delhi checklist, English Ministry study-stay page and BOE consolidated regulation. A Sri Lanka-specific document/insurance review rule was added. All Spain records remain **Pending human review**; no legal approval or automated monitoring coverage is claimed.


## 12. Sweden targeted official-source recheck — 26 November 2026

- Rechecked the live Swedish Migration Agency higher-education page, the 11 June 2026 new-rules notice, the 1 October 2026 student-family notice, the post-study job-search guidance, and the Sweden Abroad Sri Lanka residence-permit page.
- 2026 maintenance requirement remains SEK 10,656/month (calculated SEK 127,872 for 12 months). Qualifying free food reduces the monthly requirement by SEK 2,960 and qualifying free accommodation by SEK 4,736. Bank statements must be no more than four months old on the requested permit start date; private individuals are not formal sponsors and family funds must be transferred to the applicant's accessible account. Employment income needs an employment certificate and payslips; a job offer is insufficient.
- For applicable Bachelor's/Master's permits granted on or after 11 June 2026, paid work is generally limited to 15 hours/week during semesters. June–August and specified education/institution-related exceptions apply. Overwork may cause revocation or refusal of extension. Do not repeat the former unrestricted-work advice.
- The same 2026 reforms require 37.5 credits in the first study year and 45 credits per subsequent year, plus address notification within 30 days, subject to transitional/population-registration provisions.
- From 1 October 2026, accompanying family members staying up to one year need comprehensive health insurance; the legal-guardian condition applies to specified children. Student-family maintenance amounts remain unchanged.
- Sri Lanka biometrics must be submitted at the Embassy of Sweden in New Delhi. The Sweden Abroad Sri Lanka page lists Colombo permit-card collection by appointment Tue–Thu, 10:00–12:00; confirm card arrival and appointment before travel.
- Sweden dashboard source notes and financial rule updated; expected future part-time earnings and job offers are expressly excluded from proof-of-funds calculations. All Sweden rules remain **Pending human review**.


## 13. Switzerland targeted official-source recheck — 26 November 2026

- Rechecked the Embassy of Switzerland in Sri Lanka national-visa landing page and jurisdiction page (both published 31 August 2026), the student D-visa checklist (printed 02/2026; the current document page lists the PDF as updated 9 June 2026), SEM FAQ Working / Entry and the cantonal student guidance.
- Sri Lankan residents apply for national visas at the Embassy of Switzerland in Colombo. Student applications are forwarded to the competent canton; the Embassy may issue the visa only after cantonal approval.
- The checklist requires personal appearance by prior appointment, three signed D forms, four photos, academic/CV evidence, study rationale and future plan, admission and tuition-payment proof, sponsor undertaking, six months of bank movements and balance proof, sponsor ID and relationship proof, language test and official translations. Sinhala/Tamil/Dhivehi documents need official translation into English, German, French or Italian. Two A4 copy sets are required. Listed visa fee is free.
- Processing-time discrepancy: the current Embassy web page estimates 8–12 weeks total, varying by canton and case; the PDF printed 02/2026 says approximately three months for cantonal decision plus up to five further days for visa after authorisation. Neither is a guarantee; confirm directly before client commitments.
- The checklist contains no universal CHF amount. Federal and cantonal sources require sufficient means but the amount/evidence must be confirmed for the intended canton. Do not quote CHF 21,000/30,000 as a national student threshold.
- Non-EU/EFTA university/UAS students may seek cantonal work approval no earlier than six months after course start, generally max 15 hours/week outside holidays, with university compatibility confirmation and employer application. Work is not automatic. Eligible Swiss higher-education graduates may have up to six months to seek qualified work, subject to the overriding scientific/economic interest test.
- All Switzerland rules remain **Pending human review**; no job, visa or processing outcome is guaranteed.


## 14. Liechtenstein official-source recheck — 26 November 2026

- Rechecked the Liechtenstein Migration and Passport Office study L-permit page, general third-country residence page, University of Liechtenstein FAQ/housing guidance and the joint 2026 Swiss Embassy Colombo student D-visa checklist.
- The Article 19 study L-permit is expressly described as available to all nationalities; max 12 months at a time, renewable before expiry if studies continue. Full application due at least 14 days before study/training starts; visa-required applicants should apply earlier. Third-country applicants must wait abroad for visa assurance/issuance.
- The general third-country residence page's discretionary permit policy must not be misrepresented as a student L-permit quota. The special Article 19 route must be assessed on its own requirements and the exact programme.
- Work: non-EEA/non-Swiss students at the University of Liechtenstein may work up to 35% only where work is study-related, and all employment requires prior authorisation. The University says the employer submits the employment-commencement request. Do not promise unrestricted holiday work.
- University admission as a guest student is insufficient for residence. Published non-EU tuition is CHF 1,250/semester for degree programmes; estimated living costs CHF 1,500/month; dormitory rooms around CHF 400–600/month. These are budgeting references, not a statutory maintenance amount. University CHF 3,000 deposit/bank guarantee is a separate institution arrangement, not a government fee.
- Joint Colombo D-visa checklist requires three D forms, four photos, academic/CV evidence, personal study/future/departure letter, admission and tuition payment, sponsor undertaking and six-month bank evidence, sponsor ID/relationship, language-test proof (with stated scholarship exception), family-bond evidence, two A4 copy sets and official translations.
- CHF 30/day is a short-stay student border reference only, not a long-stay L-permit funds rule. No official universal student maintenance amount was located.
- All Liechtenstein rules remain **Pending human review**; do not promise visa, work, or post-study outcomes.


## 15. Luxembourg official-source corrections — 26 November 2026

- **Funds correction:** the current FNS table at June 2026 index 992.24 gives a one-adult maximum REVIS inclusion allowance of EUR 1,944.40 (adult base EUR 972.20 + household common-cost component EUR 972.20). 80% arithmetic reference = EUR 1,555.52/month. The old EUR 777.76 figure was only 80% of the adult base component and must not be used as the single-adult total. Guichet does not define the REVIS household base for foreign students, so no fixed threshold is certified; obtain Immigration confirmation.
- **Sri Lanka route:** New Delhi Embassy updated 23 November 2026 says Sri Lankan long-stay D applications are processed by New Delhi and couriered through Honorary Consulate Colombo. EUR 50 fee is listed for new D process. The 25–30 working-day recommendation is under the old AST transitional section only, not a new-route service guarantee.
- **Arrival:** first residence card page updated 1 October 2026 requires commune arrival declaration within 3 days, medical/TB screening and first residence permit filing no later than 3 months before Visa D expiry. Residence card issuance fee EUR 80; biometrics and suitable accommodation evidence required.
- **Work:** current Guichet page sets average 15 hours/week over a month outside studies; paid school-holiday work, doctoral research and University of Luxembourg assistant contracts are exceptions. Employer must submit declaration before hiring/contract changes and notify start within 3 working days. Older EU Portal first-two-semester Bachelor restriction remains an unresolved discrepancy; no automatic harmonisation.
- **Post-study:** current Guichet page states a non-renewable 12-month job-search/business-creation permit for eligible Luxembourg Master's graduates and doctoral graduates. Apply at least 30 days before expiry; funds at 80% REVIS and comprehensive insurance. This supersedes the 9-month statement in the prior draft. Ordinary Bachelor's graduates are not listed.
- **Separate graduate work route:** current student renewal page describes a simplified salaried/self-employed route for graduates completing a university course of at least 5 years, with work directly related to academic training. Keep separate from the 12-month search permit.
- **Renewal:** student permit renewal due at least 2 months before expiry; EUR 80 card fee.
- All Luxembourg rules remain Pending human review.


### Family reunification — do not state a blanket refusal or entitlement
- The current Guichet family Visa D page (updated 1 October 2026) lists a spouse/registered partner aged over 18 and unmarried children under 18 as potential family-reunification applicants joining a third-country sponsor. The sponsor must show stable and sufficient resources (assessed against the average monthly social minimum wage over 12 months), suitable accommodation and health-insurance coverage for the family.
- The student Visa D page does not expressly confirm whether every student permit holder may sponsor dependants or whether additional conditions apply. The correct counselling status is **case-specific / unconfirmed**, not "automatic entitlement" and not a categorical "not eligible". Obtain written confirmation from Immigration before promising spouse/child applications.
- Official page: https://guichet.public.lu/en/citoyens/immigration/vivre/non-luxembourg/immigration/pays-tiers/membre-famille/regroupement-familial.html

### Medical screening source
- The current Guichet medical page confirms that third-country nationals staying over 3 months generally need a medical examination and tuberculosis screening; the health certificate is required before the residence-permit application can be processed. Official page: https://guichet.public.lu/en/citoyens/immigration/vivre/luxembourg/autres/controle-medical.html
