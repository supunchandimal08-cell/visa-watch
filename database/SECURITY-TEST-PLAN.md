# VisaWatch client-record security test plan

## Do not use live client data during this test

Use synthetic names and references such as TEST-001 only. Do not use real passport details, bank data, phone numbers, identity numbers, scans or medical information.

## Required test accounts

- Admin A: active admin.
- Counsellor A: active counsellor.
- Counsellor B: active counsellor.
- Disabled user: auth account with no active team_members row, or is_active=false.
- Signed-out browser: private/incognito session with no authenticated session.

## Expected access results

| Test | Expected result |
|---|---|
| Signed-out user reads client_records | Denied / no rows |
| Authenticated user not on active team allow-list reads client_records | Denied / no rows |
| Counsellor A creates a case assigned to self | Allowed |
| Counsellor A creates a case assigned to Counsellor B | Denied |
| Counsellor A reads a case created by or assigned to A | Allowed |
| Counsellor A reads B's unrelated case | Denied |
| Counsellor B reads B's own/assigned case | Allowed |
| Counsellor tries to change team_members role | Denied |
| Counsellor tries to delete a client record | Denied |
| Counsellor tries to read client_record_audit | Denied |
| Admin reads all cases and audit rows | Allowed |
| Admin provisions or deactivates a team member | Allowed |
| Checklist access for inaccessible case | Denied |
| Checklist access for accessible case | Allowed |
| Checklist deletion by counsellor | Denied |

## Additional checks before any production launch

1. Verify RLS is enabled on all three client tables and inspect every policy in the Supabase dashboard.
2. Test the policies through the actual browser client using the publishable key, not only the SQL Editor (SQL Editor commonly runs with elevated privileges and does not prove browser restrictions).
3. Confirm there is no public sign-up, no anonymous read/write policy, and no secret/service-role key in website files, GitHub history, browser bundles, or logs.
4. Confirm the first admin bootstrap procedure is controlled and independently approved. Do not share admin credentials.
5. Confirm MFA policy, session expiry, password recovery, staff offboarding, backups and a successful restore test.
6. Confirm audit events are created for insert/update/delete and are readable only by admins. Verify audit entries do not contain old/new field values or document content.
7. Review retention/deletion and incident-response procedures with management.
8. Obtain privacy/legal approval for the selected provider, hosting region, data-processing terms and the company's obligations before collecting real client data.

## Release gate

Do not connect the public VisaWatch interface to real client records until every applicable test passes, the company formally approves the service and its owner, and the privacy/security review is recorded. A passing test plan is not itself a security certification.
