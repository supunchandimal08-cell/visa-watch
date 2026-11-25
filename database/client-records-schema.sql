-- VisaWatch client-record workflow: Supabase PostgreSQL starter
-- NOT connected to the live website. Run only in a company-owned Supabase project
-- after management approval and a privacy/security review.
-- Store minimum necessary case-management data only. Do NOT store passport numbers,
-- bank-account details, card data, medical records, passwords, or document scans here.

create extension if not exists pgcrypto;

create table if not exists public.team_members (
  user_id uuid primary key references auth.users(id) on delete restrict,
  role text not null check (role in ('admin', 'counsellor')),
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

alter table public.team_members enable row level security;

create or replace function public.vw_is_active_member()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members tm
    where tm.user_id = auth.uid() and tm.is_active = true
  );
$$;

create or replace function public.vw_is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members tm
    where tm.user_id = auth.uid()
      and tm.is_active = true
      and tm.role = 'admin'
  );
$$;

revoke all on function public.vw_is_active_member() from public;
revoke all on function public.vw_is_admin() from public;
grant execute on function public.vw_is_active_member() to authenticated;
grant execute on function public.vw_is_admin() to authenticated;

drop policy if exists "Members can read own membership or admins all" on public.team_members;
create policy "Members can read own membership or admins all"
on public.team_members for select to authenticated
using (user_id = auth.uid() or public.vw_is_admin());

drop policy if exists "Admins manage team membership" on public.team_members;
create policy "Admins manage team membership"
on public.team_members for all to authenticated
using (public.vw_is_admin())
with check (public.vw_is_admin());

create table if not exists public.client_records (
  id uuid primary key default gen_random_uuid(),
  client_ref text not null unique check (length(client_ref) between 3 and 40),
  age_range text not null default '' check (length(age_range) <= 30),
  nationality text not null default '' check (length(nationality) <= 80),
  current_residence text not null default '' check (length(current_residence) <= 100),
  destination text not null default '' check (length(destination) <= 80),
  qualification_summary text not null default '' check (length(qualification_summary) <= 1000),
  english_level text not null default '' check (length(english_level) <= 50),
  study_interest text not null default '' check (length(study_interest) <= 500),
  funding_category text not null default '' check (length(funding_category) <= 80),
  application_stage text not null default 'New enquiry'
    check (application_stage in (
      'New enquiry','Eligibility review','Provider verification pending',
      'Offer pending','Offer received','Documents pending','File QA complete',
      'Submitted — awaiting authority','Additional information requested',
      'Entry permission issued','Residence permit issued',
      'On hold','Declined','Withdrawn'
    )),
  assigned_to uuid references auth.users(id) on delete set null,
  next_follow_up date,
  next_action text not null default '' check (length(next_action) <= 500),
  consent_recorded_at timestamptz,
  consent_method text not null default '' check (length(consent_method) <= 100),
  created_by uuid not null references auth.users(id) on delete restrict,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists client_records_assigned_to_idx on public.client_records(assigned_to);
create index if not exists client_records_stage_idx on public.client_records(application_stage);
create index if not exists client_records_follow_up_idx on public.client_records(next_follow_up);

alter table public.client_records enable row level security;

drop policy if exists "Active team read assigned or created cases" on public.client_records;
create policy "Active team read assigned or created cases"
on public.client_records for select to authenticated
using (
  public.vw_is_active_member()
  and (public.vw_is_admin() or assigned_to = auth.uid() or created_by = auth.uid())
);

drop policy if exists "Active counsellors create own cases" on public.client_records;
create policy "Active counsellors create own cases"
on public.client_records for insert to authenticated
with check (
  public.vw_is_active_member()
  and created_by = auth.uid()
  and (public.vw_is_admin() or assigned_to = auth.uid() or assigned_to is null)
);

drop policy if exists "Assigned counsellor creator or admin update cases" on public.client_records;
create policy "Assigned counsellor creator or admin update cases"
on public.client_records for update to authenticated
using (
  public.vw_is_active_member()
  and (public.vw_is_admin() or assigned_to = auth.uid() or created_by = auth.uid())
)
with check (
  public.vw_is_active_member()
  and (public.vw_is_admin() or assigned_to = auth.uid() or created_by = auth.uid())
);

drop policy if exists "Only admins delete cases" on public.client_records;
create policy "Only admins delete cases"
on public.client_records for delete to authenticated
using (public.vw_is_admin());

create table if not exists public.client_checklist_items (
  id uuid primary key default gen_random_uuid(),
  client_record_id uuid not null references public.client_records(id) on delete cascade,
  item_label text not null check (length(item_label) between 1 and 160),
  item_status text not null default 'Pending'
    check (item_status in ('Pending','Received','Verified','Not required')),
  follow_up_date date,
  counsellor_note text not null default '' check (length(counsellor_note) <= 500),
  checked_by uuid references auth.users(id) on delete set null,
  checked_at timestamptz,
  created_by uuid not null references auth.users(id) on delete restrict,
  created_at timestamptz not null default now()
);

create index if not exists client_checklist_record_idx
on public.client_checklist_items(client_record_id);

alter table public.client_checklist_items enable row level security;

drop policy if exists "Team read checklist for accessible cases" on public.client_checklist_items;
create policy "Team read checklist for accessible cases"
on public.client_checklist_items for select to authenticated
using (
  public.vw_is_active_member()
  and exists (
    select 1 from public.client_records cr
    where cr.id = client_record_id
      and (public.vw_is_admin() or cr.assigned_to = auth.uid() or cr.created_by = auth.uid())
  )
);

drop policy if exists "Team add checklist for accessible cases" on public.client_checklist_items;
create policy "Team add checklist for accessible cases"
on public.client_checklist_items for insert to authenticated
with check (
  public.vw_is_active_member()
  and created_by = auth.uid()
  and exists (
    select 1 from public.client_records cr
    where cr.id = client_record_id
      and (public.vw_is_admin() or cr.assigned_to = auth.uid() or cr.created_by = auth.uid())
  )
);

drop policy if exists "Team update checklist for accessible cases" on public.client_checklist_items;
create policy "Team update checklist for accessible cases"
on public.client_checklist_items for update to authenticated
using (
  public.vw_is_active_member()
  and exists (
    select 1 from public.client_records cr
    where cr.id = client_record_id
      and (public.vw_is_admin() or cr.assigned_to = auth.uid() or cr.created_by = auth.uid())
  )
)
with check (
  public.vw_is_active_member()
  and exists (
    select 1 from public.client_records cr
    where cr.id = client_record_id
      and (public.vw_is_admin() or cr.assigned_to = auth.uid() or cr.created_by = auth.uid())
  )
);

drop policy if exists "Only admins delete checklist items" on public.client_checklist_items;
create policy "Only admins delete checklist items"
on public.client_checklist_items for delete to authenticated
using (public.vw_is_admin());

-- Audit records contain changed field names, not old/new values or client document contents.
create table if not exists public.client_record_audit (
  id bigint generated always as identity primary key,
  table_name text not null,
  record_id uuid not null,
  action text not null check (action in ('INSERT','UPDATE','DELETE')),
  actor_user_id uuid,
  changed_fields text[] not null default '{}',
  occurred_at timestamptz not null default now()
);

create index if not exists client_record_audit_record_idx
on public.client_record_audit(table_name, record_id, occurred_at desc);

alter table public.client_record_audit enable row level security;

drop policy if exists "Only admins read client audit" on public.client_record_audit;
create policy "Only admins read client audit"
on public.client_record_audit for select to authenticated
using (public.vw_is_admin());

create or replace function public.vw_audit_client_changes()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_id uuid;
  v_fields text[] := '{}';
begin
  if tg_op = 'INSERT' then
    v_id := new.id;
    select coalesce(array_agg(key order by key), '{}')
      into v_fields from jsonb_object_keys(to_jsonb(new)) as key;
  elsif tg_op = 'UPDATE' then
    v_id := new.id;
    select coalesce(array_agg(n.key order by n.key), '{}')
      into v_fields
      from jsonb_each(to_jsonb(new)) n
      left join jsonb_each(to_jsonb(old)) o on o.key = n.key
      where n.value is distinct from o.value;
  else
    v_id := old.id;
    select coalesce(array_agg(key order by key), '{}')
      into v_fields from jsonb_object_keys(to_jsonb(old)) as key;
  end if;

  insert into public.client_record_audit(table_name, record_id, action, actor_user_id, changed_fields)
  values (tg_table_name, v_id, tg_op, auth.uid(), v_fields);

  if tg_op = 'DELETE' then return old; end if;
  return new;
end;
$$;

revoke all on function public.vw_audit_client_changes() from public;

drop trigger if exists audit_client_record_changes on public.client_records;
create trigger audit_client_record_changes
after insert or update or delete on public.client_records
for each row execute function public.vw_audit_client_changes();

drop trigger if exists audit_client_checklist_changes on public.client_checklist_items;
create trigger audit_client_checklist_changes
after insert or update or delete on public.client_checklist_items
for each row execute function public.vw_audit_client_changes();

create or replace function public.vw_set_client_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  new.updated_by = auth.uid();
  return new;
end;
$$;

drop trigger if exists set_client_record_updated_at on public.client_records;
create trigger set_client_record_updated_at
before update on public.client_records
for each row execute function public.vw_set_client_updated_at();

comment on table public.client_records is
  'Minimal VisaWatch case metadata only. Do not store identity numbers, bank details, medical data or document scans.';
comment on table public.client_checklist_items is
  'Checklist metadata only; store status and verification notes, never the underlying sensitive document.';
comment on table public.client_record_audit is
  'Append-only through application policies; admin-readable metadata audit. No old/new client field values.';
