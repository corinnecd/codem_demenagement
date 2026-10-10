-- CODEM : envoie chaque nouvelle demande à la fonction notifier-demande (e-mail)
create extension if not exists pg_net with schema extensions;

create or replace function public.notifier_demande()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
  perform net.http_post(
    url := 'https://hzeohzbdckhehbkjxxws.supabase.co/functions/v1/notifier-demande',
    body := jsonb_build_object('type', 'INSERT', 'table', 'demandes', 'record', to_jsonb(new)),
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'x-webhook-secret', '874b9ff2d391c0cbb8f4c63c4280981967be89b86ed3973e'
    )
  );
  return new;
end;
$$;

revoke execute on function public.notifier_demande() from public, anon, authenticated;

drop trigger if exists demandes_notifier on public.demandes;
create trigger demandes_notifier
  after insert on public.demandes
  for each row execute function public.notifier_demande();
