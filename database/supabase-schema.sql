-- VisaWatch shared course research database (Supabase PostgreSQL)
-- Setup only: this schema does not connect the website by itself.
-- Run in Supabase SQL Editor after creating a project.
-- Access is limited to authenticated users. All authenticated team members can
-- read/update shared research records; unauthenticated/public access is denied.

create table if not exists public.course_verification_records (
  id uuid primary key default gen_random_uuid(),
  institution text not null default '',
  course text not null default '',
  destination text not null default '',
  campus text not null default '',
  intake text not null default '',
  duration text not null default '',
  tuition text not null default '',
  entry_requirements text not null default '',
  official_course_url text not null default '',
  official_register_url text not null default '',
  verification_status text not null default 'Not verified'
    check (verification_status in (
      'Not verified',
      'Partially checked',
      'Verified against official sources',
      'Not suitable / do not recommend yet'
    )),
  checked_by text not null default '',
  checked_date date,
  notes text not null default '',
  created_by uuid not null references auth.users(id) on delete restrict,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists course_verification_records_destination_idx
  on public.course_verification_records (destination);
create index if not exists course_verification_records_status_idx
  on public.course_verification_records (verification_status);
create index if not exists course_verification_records_updated_at_idx
  on public.course_verification_records (updated_at desc);

alter table public.course_verification_records enable row level security;

drop policy if exists "Authenticated team can read course records"
  on public.course_verification_records;
create policy "Authenticated team can read course records"
  on public.course_verification_records
  for select to authenticated
  using (auth.uid() is not null);

drop policy if exists "Authenticated team can add course records"
  on public.course_verification_records;
create policy "Authenticated team can add course records"
  on public.course_verification_records
  for insert to authenticated
  with check (auth.uid() = created_by);

drop policy if exists "Authenticated team can update course records"
  on public.course_verification_records;
create policy "Authenticated team can update course records"
  on public.course_verification_records
  for update to authenticated
  using (auth.uid() is not null)
  with check (auth.uid() is not null);

drop policy if exists "Authenticated team can delete course records"
  on public.course_verification_records;
create policy "Authenticated team can delete course records"
  on public.course_verification_records
  for delete to authenticated
  using (auth.uid() is not null);

create or replace function public.set_course_record_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  new.updated_by = auth.uid();
  return new;
end;
$$;

drop trigger if exists set_course_record_updated_at
  on public.course_verification_records;
create trigger set_course_record_updated_at
before update on public.course_verification_records
for each row execute function public.set_course_record_updated_at();

comment on table public.course_verification_records is
  'Shared VisaWatch course research only. Do not store sensitive client personal data. Verification status requires human evidence review.';
