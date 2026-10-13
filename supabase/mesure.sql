-- CODEM : mesure d'audience anonyme (sans cookie) + objectifs + tableau de bord
-- À coller dans Supabase → SQL Editor → Run. Peut être relancé sans risque.

-- 1. Table des événements (pages vues, clics d'action, étapes des devis)
create table if not exists public.evenements (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  nom text not null check (char_length(nom) <= 40),
  page text check (char_length(page) <= 200),
  session text check (char_length(session) <= 20),
  appareil text check (appareil in ('mobile','ordinateur')),
  details jsonb not null default '{}'::jsonb,
  constraint evenements_taille check (pg_column_size(details) < 2000)
);
create index if not exists evenements_date on public.evenements (created_at);
create index if not exists evenements_nom on public.evenements (nom);

alter table public.evenements enable row level security;
revoke all on public.evenements from anon, authenticated;
grant insert on public.evenements to anon;
drop policy if exists "le site ajoute des evenements" on public.evenements;
create policy "le site ajoute des evenements" on public.evenements for insert to anon with check (true);

-- 2. Objectifs (modifiables directement dans Table Editor → objectifs)
create table if not exists public.objectifs (
  indicateur text primary key,
  cible numeric not null,
  unite text not null,
  explication text
);
alter table public.objectifs enable row level security;
revoke all on public.objectifs from anon, authenticated;
insert into public.objectifs (indicateur, cible, unite, explication) values
  ('taux_conversion',       4,  '%',   'Demandes (devis + rappel + visite + message) ÷ visiteurs. Repère du secteur : 2 à 5 %.'),
  ('demandes_mois',         30, 'nb',  'Nombre de demandes reçues sur le mois. À ajuster selon la capacité de CODEM.'),
  ('express_envoi',         60, '%',   'Devis express envoyés ÷ devis express commencés.'),
  ('detail_achevement',     40, '%',   'Devis détaillés envoyés ÷ devis détaillés ouverts.'),
  ('clic_devis',            12, '%',   'Visiteurs qui cliquent au moins une fois sur un bouton de devis.'),
  ('clic_tel',               3, '%',   'Visiteurs qui touchent le numéro de téléphone (surtout sur mobile).')
on conflict (indicateur) do nothing;

-- 3. Tableau de bord par mois : réel vs objectif
create or replace view public.tableau_de_bord with (security_invoker = true) as
with m as (
  select date_trunc('month', created_at)::date as mois,
    count(distinct session) filter (where nom = 'page_vue')                      as visiteurs,
    count(distinct session) filter (where nom = 'clic_devis')                    as visiteurs_clic_devis,
    count(distinct session) filter (where nom = 'clic_tel')                      as visiteurs_clic_tel,
    count(distinct session) filter (where nom = 'express_debut')                 as express_commences,
    count(*)               filter (where nom = 'express_envoye')                 as express_envoyes,
    count(distinct session) filter (where nom = 'detail_ouvert')                 as detail_ouverts,
    count(*)               filter (where nom = 'devis_envoye')                   as detail_envoyes
  from public.evenements group by 1
), d as (
  select date_trunc('month', created_at)::date as mois, count(*) as demandes,
    count(*) filter (where type = 'devis') as devis
  from public.demandes group by 1
)
select m.mois, m.visiteurs, coalesce(d.demandes,0) as demandes, coalesce(d.devis,0) as devis,
  round(100.0 * coalesce(d.demandes,0) / nullif(m.visiteurs,0), 1)           as taux_conversion_pct,
  (select cible from public.objectifs where indicateur='taux_conversion')      as objectif_conversion_pct,
  (select cible from public.objectifs where indicateur='demandes_mois')        as objectif_demandes,
  round(100.0 * m.express_envoyes / nullif(m.express_commences,0), 1)          as express_envoi_pct,
  (select cible from public.objectifs where indicateur='express_envoi')        as objectif_express_pct,
  round(100.0 * m.detail_envoyes / nullif(m.detail_ouverts,0), 1)              as detail_achevement_pct,
  (select cible from public.objectifs where indicateur='detail_achevement')    as objectif_detail_pct,
  round(100.0 * m.visiteurs_clic_devis / nullif(m.visiteurs,0), 1)             as clic_devis_pct,
  round(100.0 * m.visiteurs_clic_tel / nullif(m.visiteurs,0), 1)               as clic_tel_pct
from m left join d using (mois)
order by m.mois desc;

-- 4. Entonnoir du devis détaillé : à quelle étape les visiteurs abandonnent (30 derniers jours)
create or replace view public.entonnoir_devis with (security_invoker = true) as
select (details->>'etape')::int as etape, count(distinct session) as visiteurs
from public.evenements
where nom = 'devis_etape' and created_at > now() - interval '30 days'
group by 1 order by 1;

-- 5. D'où viennent les visiteurs et quels boutons fonctionnent (30 derniers jours)
create or replace view public.sources_et_boutons with (security_invoker = true) as
select 'source' as type, coalesce(details->>'source','direct') as valeur, count(distinct session) as visiteurs
from public.evenements where nom = 'page_vue' and created_at > now() - interval '30 days' group by 2
union all
select nom, coalesce(details->>'zone','?'), count(*)
from public.evenements where nom in ('clic_devis','clic_tel','clic_rappel') and created_at > now() - interval '30 days' group by 1,2
order by 1, 3 desc;

revoke all on public.tableau_de_bord, public.entonnoir_devis, public.sources_et_boutons from anon, authenticated;

-- 6. Conservation : 13 mois maximum (à lancer de temps en temps, ou à planifier avec pg_cron)
-- delete from public.evenements where created_at < now() - interval '13 months';
