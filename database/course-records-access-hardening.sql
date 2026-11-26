-- VisaWatch shared course-record access hardening
-- Prerequisite: run database/client-records-schema.sql first so the
-- team_members allow-list and vw_is_active_member()/vw_is_admin() exist.
-- Then run database/supabase-schema.sql, followed by this migration.
-- Disable Supabase public sign-ups in Authentication settings as well.
-- RLS is still the enforcement boundary; UI sign-up removal is not security.

drop policy if exists "Authenticated team can read course records"
  on public.course_verification_records;
drop policy if exists "Authenticated team can add course records"
  on public.course_verification_records;
drop policy if exists "Authenticated team can update course records"
  on public.course_verification_records;
drop policy if exists "Authenticated team can delete course records"
  on public.course_verification_records;

drop policy if exists "Active VisaWatch members read course records"
  on public.course_verification_records;
create policy "Active VisaWatch members read course records"
  on public.course_verification_records
  for select to authenticated
  using (public.vw_is_active_member());

drop policy if exists "Active VisaWatch members add course records"
  on public.course_verification_records;
create policy "Active VisaWatch members add course records"
  on public.course_verification_records
  for insert to authenticated
  with check (
    public.vw_is_active_member()
    and created_by = auth.uid()
  );

drop policy if exists "Active VisaWatch members update course records"
  on public.course_verification_records;
create policy "Active VisaWatch members update course records"
  on public.course_verification_records
  for update to authenticated
  using (public.vw_is_active_member())
  with check (public.vw_is_active_member());

drop policy if exists "Only VisaWatch admins delete course records"
  on public.course_verification_records;
create policy "Only VisaWatch admins delete course records"
  on public.course_verification_records
  for delete to authenticated
  using (public.vw_is_admin());

comment on table public.course_verification_records is
  'Shared VisaWatch course research. Access requires an active team_members allow-list entry; deletion is admin-only. Human verification is required before counselling use.';
