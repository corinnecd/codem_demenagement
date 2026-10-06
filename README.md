# CODEM — site bilingue

Site statique français / anglais. 17 pages dans chaque langue et accueil racine.

## Mise à jour
Exécuter `python3 build.py`, `python3 pages.py`, puis `python3 content.py`. Les styles et interactions sont dans `dist/assets` (`brand.css` porte la couche de marque : vert du logo, bandes de couleur, devis 9 étapes). Les contenus métier repris de l’ancienne version sont dans `v1content.py`. Vérifier avec `python3 verify.py`.

## Réception des demandes
Renseigner `FORM_ENDPOINT` dans `pages.py` (URL qui accepte un POST multipart : e-mail, CRM ou fonction serveur) puis reconstruire. Tant qu’il est vide, le devis, le rappel, la visite et le message n’envoient rien et affichent le numéro de téléphone.

## Avant ouverture au public
- Configurer une véritable destination de réception pour les formulaires (service serveur, messagerie ou CRM) ; les formulaires actuels n'envoient aucune donnée et ne simulent jamais de réussite.
- Fournir les noms et périmètres exacts des cinq formules, sans inventer de prix.
- Confirmer les deux numéros de téléphone et l'adresse à Nogent-sur-Marne.
- Fournir les informations légales de l'entreprise, du directeur de publication et de l'hébergeur ; finaliser la notice de confidentialité selon la future collecte.
- Confirmer les droits des visuels. Les quatre vidéos sont des illustrations IA ; leur nature est signalée sur le site.
- Aucun témoignage, avis, statistique ou certification inventé. Les photographies de véhicules et de monte-meubles fournies sont utilisées comme éléments concrets.
- Aucun traceur analytique activé. Configurer le suivi des clics et envois seulement avec une destination et un mécanisme de consentement adaptés.

## Médias
Les originaux fournis n'ont pas été modifiés. Images WebP en deux tailles, vidéos optimisées en 720p, couverture immédiate, pause accessible, réduction des mouvements et mode économie de données pris en charge. Aucun accès Higgsfield et aucune clé privée dans le site.
