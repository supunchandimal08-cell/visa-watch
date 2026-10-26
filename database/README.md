# VisaWatch shared course research database

This folder contains the starter PostgreSQL schema for a future shared course-research workspace.

## Important status

- The current website still saves course records in the current browser only.
- Adding this SQL file does **not** connect the website to a database.
- Do not enter client passport, bank, medical, or other sensitive personal data.
- A database should not be used for live company records until authentication, access controls, backups, and a privacy review are completed.

## Setup steps

1. Create a Supabase project using the company's approved email/account.
2. Open **SQL Editor** in the Supabase dashboard.
3. Open `supabase-schema.sql` from this repository, copy its full contents, and run it in SQL Editor.
4. In Supabase Authentication, enable an approved sign-in method and create/invite only authorised company users. Do not enable public sign-ups for an internal company tool unless the company explicitly requires it.
5. In **Project Settings → API**, use only the project URL and the publishable/anon key in a browser app. Never put a `service_role` or secret key in website JavaScript, GitHub, or a public repository.
6. Before connecting the website, implement and test sign-in/sign-out, session expiry, error handling, and access policies. Confirm all shared records are visible only to authenticated team members.
7. Test with two authorised test accounts and one signed-out browser. The signed-out browser must not read or modify records.
8. Arrange company ownership, backup/restore, retention, and access removal when staff leave.

## Current schema behaviour

- All authenticated users can read shared course-research records.
- Authenticated users can create records only with their own user ID in `created_by`.
- Authenticated users can update or delete shared records.
- Row-level security (RLS) is enabled; anonymous/public access is not granted by the policies in this schema.
- The status field is constrained to the four values used by the website.
- An update trigger records the update timestamp and the user who made the latest update.

This is a starter for course research, not a complete production security review. Add role-based permissions and a formal audit history if the company needs reviewer/administrator separation or a tamper-evident change log.
