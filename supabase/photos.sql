-- CODEM : espace privé pour les photos et vidéos jointes aux devis
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('devis-photos', 'devis-photos', false, 26214400, array['image/*', 'video/*'])
on conflict (id) do update
  set public = false, file_size_limit = 26214400, allowed_mime_types = array['image/*', 'video/*'];

-- Le site peut seulement DÉPOSER des fichiers dans cet espace ; il ne peut ni les voir, ni les modifier, ni les supprimer.
drop policy if exists "le site depose les photos de devis" on storage.objects;
create policy "le site depose les photos de devis" on storage.objects
  for insert to anon
  with check (bucket_id = 'devis-photos');
