# VisaWatch Official Source Register

**Status:** Internal reference index — not legal advice  
**Last reviewed:** 25 November 2026  
**Canonical machine-readable list:** [`data/sources.json`](../data/sources.json)

## Purpose

This register explains how VisaWatch's official-source inventory is to be used by counsellors. The JSON file above remains the canonical source list used by the monitoring workflow. Do not maintain a second competing list of URLs in this document.

## Current inventory snapshot

A repository review on 25 November 2026 found **99 source entries** in `data/sources.json`, covering **18 country / jurisdiction labels**:

- Australia
- Canada
- Europe / Schengen
- Finland
- France
- Germany
- Iceland
- Ireland
- Italy
- Japan
- Netherlands
- New Zealand
- Spain
- Sweden
- UAE
- UAE / Dubai
- UK
- USA

The original VisaWatch dashboard's core destination groups remain UK, Canada, Australia, UAE / Dubai, New Zealand, Europe / Schengen and USA. The register also contains country-specific European sources and additional study destinations. A European country source must not be treated as a single Schengen-wide rule.

## Source hierarchy for counsellors

Use sources in this order, selecting the authority that has legal responsibility for the applicant's exact route:

1. **Primary law / official legal instrument** — legislation, regulations and official immigration rules.
2. **Competent immigration authority** — the government department or agency deciding the visa or residence application.
3. **Official education regulator / provider register** — confirms institution, campus, programme or provider status; it does not itself guarantee a visa.
4. **Official embassy / consular instructions** — local filing channel, appointment and country-specific document requirements.
5. **Official government explanatory guidance** — useful for client explanations, but check it against legislation and the competent authority where details conflict.

University marketing pages, agent blogs, social media and third-party summaries are not proof of an immigration rule.

## Counsellor verification steps

Before using a source in a client consultation:

- Match the applicant's destination, visa category, nationality, residence country and intended application date.
- Open the live official URL; confirm it is still controlled by the named authority and applies to the correct jurisdiction.
- Record the exact rule or requirement and the page's publication / last-updated date where shown.
- Separately record the rule's commencement / effective date. A page update date alone does not prove a rule has taken effect.
- Check transitional provisions, exceptions, applicant-specific conditions and the current application form / checklist.
- Compare conflicting official sources. Do not silently choose one; mark the item **Needs review** and escalate to a senior reviewer or the authority.
- Distinguish **Confirmed**, **Proposed**, **Needs review** and **Superseded**. A monitoring alert or page-text change is not confirmation of a legal change.
- Save the source URL, access date, reviewer and a concise explanation in the relevant rule record.
- Re-check fees, financial thresholds, work rights and processing guidance immediately before advising or filing.

## Important limitations in the current inventory

- `data/sources.json` contains URLs and notes, with optional monitoring settings such as `compare_text`. It is a source inventory, not a complete legal rules database.
- All 8 Canada entries now include structured source owner, jurisdiction, category, source type, verification mode and last-verified date fields (reviewed 25 November 2026). Their `compare_text: false` setting is intentional: they are availability-only checks and require manual legal-content review.
- Other entries still have inconsistent structured metadata. Do not assume the Canada metadata migration has been applied to the full 99-entry inventory.
- Some entries are availability-only checks; automated reachability does not mean the page's legal content was compared.
- The monitor detects page changes or availability only. It does not interpret legislation, establish legal effect or approve client advice.
- Publication date, legal effective date and named human reviewer are not yet consistently stored as structured fields across the inventory. Add them only after checking the actual official source and reviewer record; never infer them from a crawl date.
- A source may cover only one emirate, province, state, consular post, course type or permit class. Confirm the precise scope before applying it.
- The current inventory contains multiple European national authorities. Do not describe all European student residence rules as one uniform Schengen student visa.

## Release and review rule

No source entry or extracted rule becomes approved client advice solely because it appears in this register or a monitor run reports success. A trained human reviewer must verify the current official source and approve the specific rule record. If an official source is unavailable, contradictory or unclear, tell the client that confirmation is pending rather than guessing.

## Related project files

- [Canonical source inventory](../data/sources.json)
- [Immigration rule verification checklist](./IMMIGRATION-RULE-VERIFICATION-CHECKLIST.md)
- [Client record security test plan](./SECURITY-TEST-PLAN.md)
- [Management approval checklist](./MANAGEMENT-APPROVAL-CHECKLIST.md)
