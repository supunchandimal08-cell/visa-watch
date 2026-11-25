# VisaWatch secure client-record setup (pre-deployment)

## Status

This is a proposed database foundation only. It is **not connected to the live VisaWatch website** and is not ready for real client data. No database account or project has been created by this repository change.

The company currently has no client-record system. Management must first approve the service owner, budget, data location, access list, retention policy and privacy/security review. A Supabase project is a candidate implementation, not a decision already made for the company.

## What the starter schema provides

Run `client-records-schema.sql` only in a new, company-owned Supabase project after technical review.

- Individual staff accounts linked to an explicit `team_members` allow-list.
- Two roles: `admin` and `counsellor`. A person who is not on the active allow-list cannot access client records.
- Counsellors can read cases they created or are assigned; admins can read all cases.
- Counsellors can create and update their accessible cases. Only admins can delete cases or manage team membership.
- Case metadata, application stage, assigned counsellor and follow-up action/date.
- Document checklist metadata (Pending / Received / Verified / Not required), not the documents themselves.
- An audit table recording actor, time, action and changed field names. It deliberately does not copy old/new field values.
- Row-level security (RLS) policies on all client-related tables.

These policies are a starting point and must be tested in the actual project. They are not a certification or guarantee of legal compliance.

## Setup sequence (admin/technical owner)

1. Obtain written management approval. Decide who owns the account and who is the privacy/security contact.
2. Review the provider's current terms, data-processing terms, available hosting region, subprocessors, backup options and incident process. Confirm the selected hosting location is acceptable for the company's legal obligations, including applicable Sri Lankan data-protection requirements. Get qualified legal advice where needed.
3. Create a company-owned Supabase project with MFA enabled for project administrators. Do not use a personal employee account as the sole owner.
4. In SQL Editor, review and run `client-records-schema.sql` in that project. Do not run it in the public GitHub repository or paste client data into SQL.
5. Create/invite staff accounts with approved email addresses. Disable public sign-up.
6. Bootstrap the first admin from the SQL Editor using the exact Auth user UUID after the admin account has been created:

   ```sql
   insert into public.team_members (user_id, role, is_active)
   values ('REPLACE-WITH-ADMIN-AUTH-USER-UUID', 'admin', true);
   ```

   Only an existing admin should add other staff. Never allow users to set their own role. Keep a controlled record of who approved each access grant.
7. Add each authorised counsellor as `role = 'counsellor'`. Deactivate access promptly when staff leave or change roles.
8. Test with at least: an admin account, two counsellors assigned different cases, and a signed-out/incognito browser. Confirm the signed-out user sees no client data; counsellor A cannot read counsellor B's unassigned case; counsellors cannot manage members or delete cases; only admins can read audit entries.
9. Arrange and test backups and restoration, account recovery, MFA, session expiry, incident response, retention/deletion, and periodic access reviews before launch.

## Data minimisation rules

- Use a generated company client reference. Do not use passport number, NIC number, date of birth or a phone number as the client reference.
- Store only age range, broad study/case details, funding category, stage and follow-up information needed for counselling.
- Do not put passport scans, bank statements, card details, passwords, medical reports, or full identity numbers in these tables, notes, GitHub, chat, or public pages.
- The checklist stores only a document label and status. If document storage is later approved, use a private storage bucket with separate access policies, short-lived signed access, encryption, malware scanning, retention controls and audit logging. That storage is not included in this starter.
- Obtain and record an appropriate privacy notice/consent or other lawful basis before collecting client data. Consent wording and legal basis must be reviewed for the company's actual process.
- Define a retention period and secure deletion process. Do not keep cases indefinitely by default.

## Website integration requirements (not yet implemented)

The static GitHub Pages / Cloudflare Assets website must not connect using a Supabase `service_role` or secret key. A future integration must use the Supabase project URL and publishable/anon key only in the browser, with Authentication and RLS enforced on every table. Never put secret keys in JavaScript, GitHub, Worker assets or chat.

Before integration, implement and test:
- Sign-in, sign-out, password recovery, MFA policy and session expiry.
- No client-record screen or API response for signed-out users.
- RLS tests for every role and every table, including checklist and audit access.
- Safe form validation, output escaping, error handling and no sensitive values in browser logs.
- Admin-only staff provisioning and access removal.
- A privacy notice, retention schedule, backup/restore and incident process.

Do not switch the existing local-browser tracker to real client data until these checks pass. The current dashboard and interview worksheet remain demonstration/intake aids only; they do not submit records to a shared company database.
