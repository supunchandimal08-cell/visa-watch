# VisaWatch — Client record access permission matrix

This matrix is a proposed least-privilege model for the first client-record release. It is not active access control until the approved database, authentication and row-level security policies are configured and tested.

| Action | Admin | Counsellor |
|---|---:|---:|
| View all client records | Yes | No |
| View own created or assigned client records | Yes | Yes |
| Create a client record | Yes | Yes |
| Update an accessible client record | Yes | Yes |
| Delete a client record | Yes, controlled process | No |
| Add or update checklist status for an accessible case | Yes | Yes |
| View audit history | Yes | No |
| Add/remove team members or change roles | Yes | No |
| Change another staff member's role | Yes, controlled process | No |
| Export client data | Only if separately approved | No by default |

## Required controls

1. Require authenticated, active staff accounts. No public sign-up.
2. Require MFA for every staff account where supported.
3. Enforce permissions in the database with row-level security; hiding buttons in the website is not a security control.
4. Counsellors must only see records they created or that are assigned to them.
5. Admin privileges must be limited to named, authorised staff and reviewed regularly.
6. Log record creation, updates, deletion and checklist changes without copying sensitive field values into audit logs.
7. Remove access promptly when a staff member leaves or changes role.
8. Do not use shared staff logins.
9. Test with separate admin, counsellor A, counsellor B, inactive and signed-out accounts.
10. Do not enable exports or document uploads until separately reviewed and approved.

## Acceptance tests

- Signed-out user cannot read or change any client record.
- Inactive staff member cannot read or change records.
- Counsellor A cannot read or modify Counsellor B's unassigned case, including by guessing its UUID.
- Counsellor cannot manage team roles or delete client records.
- Counsellor cannot read audit history.
- Admin can perform only the approved administrative actions.
- Every test is performed through the actual application client, not only a privileged SQL console.

## Important

The matrix is a proposed design. The company must approve it, and technical tests must pass before real client data is entered.
