-- CODEM : table des demandes envoyées depuis le site
create table if not exists public.demandes (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  type text not null check (type in ('devis','rappel','visite','message')),
  reference text,
  nom text,
  email text,
  telephone text,
  langue text,
  page text,
  donnees jsonb not null default '{}'::jsonb,
  statut text not null default 'nouveau',
  constraint demandes_taille check (pg_column_size(donnees) < 30000)
);

alter table public.demandes enable row level security;

-- Le site peut seulement AJOUTER une demande ; il ne peut ni lire, ni modifier, ni supprimer.
revoke all on public.demandes from anon, authenticated;
grant insert on public.demandes to anon;

drop policy if exists "le site ajoute des demandes" on public.demandes;
create policy "le site ajoute des demandes" on public.demandes
  for insert to anon
  with check (statut = 'nouveau');
