// CODEM — e-mail de notification à chaque nouvelle demande du site
// Secrets : RESEND_API_KEY, NOTIFY_EMAIL (destinataire), WEBHOOK_SECRET, NOTIFY_FROM (facultatif)
// Appelée par le déclencheur SQL demandes_notifier. « Verify JWT » désactivé : protégée par WEBHOOK_SECRET.

const TYPES: Record<string, string> = {
  devis: "Demande de devis",
  rappel: "Demande de rappel",
  visite: "Demande de visite",
  message: "Message",
};

// Libellés lisibles, dans l'ordre d'affichage
const LABELS: [string, string][] = [
  ["projet", "Type de projet"],
  ["type", "Type de visite"],
  ["prenom", "Prénom"],
  ["nom", "Nom"],
  ["organisation", "Organisation"],
  ["telephone", "Téléphone"],
  ["email", "E-mail"],
  ["preference", "Contact préféré"],
  ["canal", "Canal préféré"],
  ["creneau", "Créneau"],
  ["depart", "Ville de départ"],
  ["arrivee", "Ville d'arrivée"],
  ["periode", "Période souhaitée"],
  ["depart_commune", "Départ — commune"],
  ["depart_pays", "Départ — pays"],
  ["depart_type", "Départ — type de logement"],
  ["depart_etage", "Départ — étage"],
  ["depart_ascenseur", "Départ — ascenseur"],
  ["depart_portage", "Départ — portage (m)"],
  ["depart_stationnement", "Départ — stationnement"],
  ["depart_rue_etroite", "Départ — accès"],
  ["arrivee_commune", "Arrivée — commune"],
  ["arrivee_pays", "Arrivée — pays"],
  ["arrivee_type", "Arrivée — type de logement"],
  ["arrivee_etage", "Arrivée — étage"],
  ["arrivee_ascenseur", "Arrivée — ascenseur"],
  ["arrivee_portage", "Arrivée — portage (m)"],
  ["arrivee_stationnement", "Arrivée — stationnement"],
  ["arrivee_rue_etroite", "Arrivée — accès"],
  ["groupage", "Groupage"],
  ["date", "Date souhaitée"],
  ["flexibilite", "Flexibilité"],
  ["urgent", "Urgence"],
  ["contraintes", "Contraintes horaires"],
  ["volume_mode", "Estimation"],
  ["taille", "Taille du logement"],
  ["surface", "Surface (m²)"],
  ["volume", "Volume (m³)"],
  ["annexes", "Cave, grenier, extérieur"],
  ["formule", "Formule pressentie"],
  ["prestations", "Prestations souhaitées"],
  ["objets", "Objets / informations utiles"],
  ["fichiers_noms", "Photos sélectionnées (non transmises)"],
  ["message", "Message"],
  ["marketing", "Accepte les informations commerciales"],
];

// Traduction des valeurs codées
const VALUES: Record<string, Record<string, string>> = {
  projet: { particulier: "Particulier", succession: "Succession", entreprise: "Entreprise", stockage: "Stockage", "monte-meubles": "Monte-meubles", "objet-specialise": "Objet spécialisé", autre: "Autre besoin" },
  type: { domicile: "À domicile", distance: "À distance (vidéo)" },
  preference: { telephone: "Téléphone", email: "E-mail" },
  canal: { telephone: "Téléphone", email: "E-mail" },
  creneau: { matin: "Matin 9 h – 12 h", "apres-midi": "Après-midi 13 h – 18 h", vendredi: "Vendredi 13 h – 17 h", "a-convenir": "À convenir" },
  flexibilite: { fixe: "Date fixe", "3-jours": "± 3 jours", "1-semaine": "± 1 semaine", "a-definir": "À définir" },
  depart_type: { appartement: "Appartement", maison: "Maison", bureaux: "Bureaux ou local", stockage: "Stockage", autre: "Autre" },
  arrivee_type: { appartement: "Appartement", maison: "Maison", bureaux: "Bureaux ou local", stockage: "Stockage", autre: "Autre" },
  depart_ascenseur: { oui: "Oui", non: "Non", "a-verifier": "À vérifier" },
  arrivee_ascenseur: { oui: "Oui", non: "Non", "a-verifier": "À vérifier" },
  depart_stationnement: { facile: "Facile", "a-reserver": "À réserver", difficile: "Difficile", "a-verifier": "À vérifier" },
  arrivee_stationnement: { facile: "Facile", "a-reserver": "À réserver", difficile: "Difficile", "a-verifier": "À vérifier" },
  depart_rue_etroite: { oui: "Rue étroite ou accès contraint" },
  arrivee_rue_etroite: { oui: "Rue étroite ou accès contraint" },
  groupage: { oui: "Souhaite étudier un groupage" },
  urgent: { oui: "Projet urgent" },
  volume_mode: { surface: "Par surface", volume: "Volume déjà estimé" },
  taille: { studio: "Studio / T1", "t2-t3": "T2 – T3", t4: "T4 et plus", maison: "Maison", inconnu: "Ne sait pas" },
  formule: { self: "Self", "self-plus": "Self plus", confort: "Confort", "confort-plus": "Confort plus", "grand-confort": "Grand Confort", "a-definir": "À définir avec CODEM" },
  prestations: { emballage: "Emballage", demontage: "Démontage / remontage", fragiles: "Objets fragiles", "monte-meubles": "Monte-meubles", "garde-meubles": "Garde-meubles", cartons: "Cartons" },
  marketing: { oui: "Oui" },
};

// Déjà affichés dans l'encadré du client, ou sans intérêt dans l'e-mail
const HIDDEN = new Set(["consentement", "reference", "website", "viewport", "nom", "telephone", "email"]);

const esc = (v: unknown) =>
  String(v ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

const dateFr = (x: string) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(x);
  if (!m) return x;
  return new Date(Date.UTC(+m[1], +m[2] - 1, +m[3], 12)).toLocaleDateString("fr-FR", { timeZone: "Europe/Paris", weekday: "long", day: "numeric", month: "long", year: "numeric" });
};

const show = (k: string, v: unknown) =>
  (Array.isArray(v) ? v : [v])
    .map((x) => VALUES[k]?.[String(x)] ?? (k === "date" ? dateFr(String(x ?? "")) : String(x ?? "")))
    .filter(Boolean)
    .join(", ");

const row = (label: string, value: string) =>
  `<tr><td style="padding:6px 16px 6px 0;color:#666;vertical-align:top;white-space:nowrap">${esc(label)}</td><td style="padding:6px 0">${esc(value).replace(/\n/g, "<br>")}</td></tr>`;

Deno.serve(async (req) => {
  const secret = Deno.env.get("WEBHOOK_SECRET");
  if (!secret || req.headers.get("x-webhook-secret") !== secret) return new Response("non autorisé", { status: 401 });
  const payload = await req.json().catch(() => null);
  const r = payload?.record;
  if (!r) return new Response("pas de demande", { status: 400 });

  const to = Deno.env.get("NOTIFY_EMAIL");
  const key = Deno.env.get("RESEND_API_KEY");
  const from = Deno.env.get("NOTIFY_FROM") ?? "Site CODEM <onboarding@resend.dev>";
  if (!to || !key) return new Response("secrets manquants", { status: 500 });

  const d: Record<string, unknown> = r.donnees ?? {};
  const titre = TYPES[r.type] ?? "Demande";
  const date = new Date(r.created_at).toLocaleString("fr-FR", { timeZone: "Europe/Paris", dateStyle: "full", timeStyle: "short" });

  const known = new Set(LABELS.map(([k]) => k));
  const lignes = [
    ...LABELS.filter(([k]) => !HIDDEN.has(k) && d[k] !== undefined && show(k, d[k]) !== "").map(([k, label]) => row(label, show(k, d[k]))),
    ...Object.keys(d).filter((k) => !known.has(k) && !HIDDEN.has(k) && show(k, d[k]) !== "").map((k) => row(k, show(k, d[k]))),
  ].join("");

  const tel = r.telephone ? `<a href="tel:${esc(r.telephone)}" style="color:#2f7d1e">${esc(r.telephone)}</a>` : "—";
  const mail = r.email ? `<a href="mailto:${esc(r.email)}" style="color:#2f7d1e">${esc(r.email)}</a>` : "—";

  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;color:#22264f;max-width:640px">
<p style="margin:0 0 4px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5fb03a;font-weight:bold">Site CODEM</p>
<h2 style="margin:0 0 6px;font-size:22px">${esc(titre)}${r.reference ? " · " + esc(r.reference) : ""}</h2>
<p style="margin:0 0 18px;color:#666;font-size:13px">Reçue le ${esc(date)} · page ${esc(r.page)} · ${r.langue === "en" ? "anglais" : "français"}</p>
<div style="background:#f4f6f1;border-radius:10px;padding:14px 16px;margin:0 0 20px">
<p style="margin:0 0 6px;font-size:17px"><strong>${esc(r.nom ?? "Sans nom")}</strong></p>
<p style="margin:0 0 4px">Téléphone : ${tel}</p>
<p style="margin:0">E-mail : ${mail}</p>
</div>
<table style="border-collapse:collapse;font-size:14px;width:100%">${lignes}</table>
</div>`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from,
      to: to.split(",").map((s) => s.trim()),
      reply_to: r.email || undefined,
      subject: `${titre} — ${r.nom ?? "site CODEM"}${r.reference ? " (" + r.reference + ")" : ""}`,
      html,
    }),
  });
  return new Response(await res.text(), { status: res.ok ? 200 : 502 });
});
