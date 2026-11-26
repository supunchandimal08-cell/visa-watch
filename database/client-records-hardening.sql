-- VisaWatch client-record workflow hardening
-- Run only after database/client-records-schema.sql in the company-owned project.
-- This migration prevents inactive/non-team assignment and counsellor self-reassignment.
-- It does not replace browser/RLS testing or management/privacy approval.

create or replace function public.vw_guard_client_record_changes()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  if tg_op = 'INSERT' then
    if new.created_by is distinct from auth.uid() then
      raise exception 'created_by must match the signed-in user';
    end if;
  else
    if new.created_by is distinct from old.created_by then
      raise exception 'created_by cannot be changed';
    end if;
    if new.id is distinct from old.id then
      raise exception 'client record id cannot be changed';
    end if;
    if new.assigned_to is distinct from old.assigned_to
       and not public.vw_is_admin() then
      raise exception 'Only an admin can reassign a client record';
    end if;
  end if;

  if new.assigned_to is not null and not exists (
    select 1
    from public.team_members tm
    where tm.user_id = new.assigned_to
      and tm.is_active = true
  ) then
    raise exception 'assigned_to must be an active VisaWatch team member';
  end if;

  return new;
end;
$$;

revoke all on function public.vw_guard_client_record_changes() from public;

drop trigger if exists guard_client_record_changes on public.client_records;
create trigger guard_client_record_changes
before insert or update on public.client_records
for each row execute function public.vw_guard_client_record_changes();

comment on function public.vw_guard_client_record_changes() is
  'Validates active team assignment and protects client-record creator and assignment provenance.';
