# VisaWatch — Management approval checklist

## Decision required before creating the production database

VisaWatch is currently a public static website and does not have a secure shared client-record database. The proposed Supabase implementation is not yet approved, provisioned, or connected.

Management should record a decision for each item below before any real client data is collected.

## Approval checklist

- [ ] Approve a company-owned Supabase project (or nominate another approved provider).
- [ ] Name a company owner for the project and a backup administrator.
- [ ] Approve the budget and billing owner; confirm expected ongoing costs and limits.
- [ ] Review current provider terms, data-processing agreement, subprocessors, hosting region and backup locations.
- [ ] Obtain privacy/legal review for applicable Sri Lankan data-protection requirements and any cross-border processing.
- [ ] Approve the minimum data fields and client privacy notice/lawful basis.
- [ ] Approve staff roles, access list, MFA requirements and offboarding procedure.
- [ ] Approve retention period, deletion process, backup/restore process and incident response contact.
- [ ] Approve a test period using dummy data only.
- [ ] Authorise production launch only after the security test plan passes.

## Proposed initial scope

The first release should store only:
- Generated client reference (not passport/NIC number or phone number).
- Age range and broad education/counselling details.
- Destination, study interest, application stage and assigned counsellor.
- Funding category (not bank-account numbers or statements).
- Follow-up date and action.
- Document checklist label and status only.

Do not store identity document scans, passport numbers, bank statements, payment-card data, passwords, medical information or unnecessary sensitive personal details in the initial database.

## Proposed responsibilities

- Company management: approve provider, budget, lawful use and launch.
- System owner/admin: manage team access, MFA, account recovery and access reviews.
- Counsellor: access only assigned/created cases and maintain accurate case status.
- Reviewer: review eligibility and record the outcome using the approved company process.
- Technical maintainer: monitor availability, security updates, backups and restore tests.

## Release gate

The website must not be connected to real client data until management approval is recorded, hosting/privacy review is complete, authentication is configured, row-level security is tested with separate accounts, backup/restore is tested, and the production owner signs off.

This checklist is a planning document, not legal advice or a claim of regulatory compliance.
