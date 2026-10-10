// CODEM — notification de chaque nouvelle demande du site
// - Devis : dossier PDF premium joint, envoyé à CODEM et en copie au client
// - Rappel, visite, message : e-mail récapitulatif à CODEM
// Secrets : RESEND_API_KEY, NOTIFY_EMAIL (destinataire CODEM), WEBHOOK_SECRET, NOTIFY_FROM (facultatif)
// Appelée par le déclencheur SQL demandes_notifier. « Verify JWT » désactivé : protégée par WEBHOOK_SECRET.

import { PDFDocument, StandardFonts, rgb, type PDFFont, type PDFPage } from "npm:pdf-lib@1.17.1";

const SITE = "https://codemdemenagement.vercel.app";
const CODEM = { adresse: "39 boulevard de Strasbourg, 94130 Nogent-sur-Marne", tel: "01 71 36 18 38", mobile: "06 67 57 09 12" };

const TYPES: Record<string, string> = {
  devis: "Demande de devis",
  rappel: "Demande de rappel",
  visite: "Demande de visite",
  message: "Message",
};

const LABELS: Record<string, string> = {
  projet: "Type de projet", type: "Type de visite", prenom: "Prénom", nom: "Nom", organisation: "Organisation",
  telephone: "Téléphone", email: "E-mail", preference: "Contact préféré", canal: "Canal préféré", creneau: "Créneau de rappel",
  depart: "Ville de départ", arrivee: "Ville d'arrivée", periode: "Période souhaitée",
  depart_commune: "Commune", depart_pays: "Pays", depart_type: "Type de logement", depart_etage: "Étage",
  depart_ascenseur: "Ascenseur", depart_portage: "Portage", depart_stationnement: "Stationnement", depart_rue_etroite: "Accès",
  arrivee_commune: "Commune", arrivee_pays: "Pays", arrivee_type: "Type de logement", arrivee_etage: "Étage",
  arrivee_ascenseur: "Ascenseur", arrivee_portage: "Portage", arrivee_stationnement: "Stationnement", arrivee_rue_etroite: "Accès",
  groupage: "Groupage", date: "Date souhaitée", flexibilite: "Flexibilité", urgent: "Urgence", contraintes: "Contraintes horaires",
  volume_mode: "Estimation", taille: "Taille du logement", surface: "Surface", volume: "Volume estimé",
  annexes: "Annexes", formule: "Formule", prestations: "Prestations",
  objets: "Objets et informations utiles", fichiers_echec: "Fichiers non reçus", message: "Message",
  marketing: "Informations commerciales",
};

const VALUES: Record<string, Record<string, string>> = {
  projet: { particulier: "Particulier", succession: "Succession", entreprise: "Entreprise", stockage: "Stockage", "monte-meubles": "Monte-meubles", "objet-specialise": "Objet spécialisé", autre: "Autre besoin" },
  type: { domicile: "À domicile", distance: "À distance (vidéo)" },
  preference: { telephone: "Téléphone", email: "E-mail" },
  canal: { telephone: "Téléphone", email: "E-mail" },
  creneau: { matin: "Matin, 9 h – 12 h", "apres-midi": "Après-midi, 13 h – 18 h", vendredi: "Vendredi, 13 h – 17 h", "a-convenir": "À convenir" },
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
  taille: { studio: "Studio / T1", "t2-t3": "T2 – T3", t4: "T4 et plus", maison: "Maison", inconnu: "Non précisée" },
  formule: { self: "Self", "self-plus": "Self plus", confort: "Confort", "confort-plus": "Confort plus", "grand-confort": "Grand Confort", "a-definir": "À définir avec CODEM" },
  prestations: { emballage: "Emballage", demontage: "Démontage / remontage", fragiles: "Objets fragiles", "monte-meubles": "Monte-meubles", "garde-meubles": "Garde-meubles", cartons: "Cartons" },
  marketing: { oui: "Accepte de les recevoir" },
};

const UNITS: Record<string, string> = { surface: " m²", volume: " m³", depart_portage: " m", arrivee_portage: " m" };

const esc = (v: unknown) =>
  String(v ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

const dateFr = (x: string, opts: Intl.DateTimeFormatOptions = { weekday: "long", day: "numeric", month: "long", year: "numeric" }) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(x);
  if (!m) return x;
  return new Date(Date.UTC(+m[1], +m[2] - 1, +m[3], 12)).toLocaleDateString("fr-FR", { timeZone: "Europe/Paris", ...opts });
};

const show = (d: Record<string, unknown>, k: string) => {
  const v = d[k];
  if (v === undefined || v === null) return "";
  const s = (Array.isArray(v) ? v : [v])
    .map((x) => VALUES[k]?.[String(x)] ?? (k === "date" ? dateFr(String(x ?? "")) : String(x ?? "").trim()))
    .filter(Boolean)
    .join(", ");
  return s && UNITS[k] && /^[\d.,]+$/.test(s) ? s + UNITS[k] : s;
};

// ---------- PDF ----------
const NAVY = rgb(0x22 / 255, 0x26 / 255, 0x4f / 255);
const GREEN = rgb(0x5f / 255, 0xb0 / 255, 0x3a / 255);
const DARKGREEN = rgb(0x2f / 255, 0x7d / 255, 0x1e / 255);
const GREY = rgb(0.42, 0.43, 0.5);
const LINE = rgb(0.88, 0.89, 0.91);
const PAPER = rgb(0.957, 0.965, 0.945);
const WHITE = rgb(1, 1, 1);

// Les polices standard du PDF ne connaissent que l'alphabet latin (WinAnsi) : on remplace le reste
const clean = (font: PDFFont, s: string) =>
  [...s.replace(/\r/g, "").replace(/[“”]/g, '"').replace(/→/g, "->")]
    .map((ch) => { if (ch === "\n") return ch; try { font.encodeText(ch); return ch; } catch { return ""; } })
    .join("")
    .replace(/ {2,}/g, " ")
    .replace(/ ([.,])/g, "$1");

function wrap(font: PDFFont, size: number, text: string, width: number): string[] {
  const out: string[] = [];
  for (const para of clean(font, text).split("\n")) {
    let line = "";
    for (const word of para.split(/\s+/)) {
      const test = line ? line + " " + word : word;
      if (font.widthOfTextAtSize(test, size) <= width) { line = test; continue; }
      if (line) out.push(line);
      line = word;
      while (font.widthOfTextAtSize(line, size) > width && line.length > 1) {
        let cut = line.length - 1;
        while (cut > 1 && font.widthOfTextAtSize(line.slice(0, cut), size) > width) cut--;
        out.push(line.slice(0, cut));
        line = line.slice(cut);
      }
    }
    out.push(line);
  }
  return out;
}

async function buildPdf(r: any, d: Record<string, unknown>, photos: string[]): Promise<Uint8Array> {
  const pdf = await PDFDocument.create();
  pdf.setTitle(`CODEM — Dossier de demande ${r.reference ?? ""}`);
  pdf.setAuthor("CODEM Déménagement");
  const sans = await pdf.embedFont(StandardFonts.Helvetica);
  const bold = await pdf.embedFont(StandardFonts.HelveticaBold);
  const serif = await pdf.embedFont(StandardFonts.TimesRoman);
  const serifIt = await pdf.embedFont(StandardFonts.TimesRomanItalic);
  let logo: any = null;
  try {
    const res = await fetch(`${SITE}/assets/logo-pdf.png`);
    if (res.ok) logo = await pdf.embedPng(new Uint8Array(await res.arrayBuffer()));
  } catch { /* logo facultatif */ }

  const W = 595.28, H = 841.89, M = 48, CW = W - 2 * M;
  let page: PDFPage = pdf.addPage([W, H]);
  let y = H - M;

  // Texte avec ² et ³ dessinés en exposant (plus sûr que le glyphe dans toutes les visionneuses)
  const text = (s: string, x: number, yy: number, size: number, font: PDFFont, color = NAVY) => {
    let cx = x;
    for (const part of clean(font, s).split(/([²³])/)) {
      if (!part) continue;
      if (part === "²" || part === "³") {
        const sup = part === "²" ? "2" : "3";
        page.drawText(sup, { x: cx + 0.3, y: yy + size * 0.38, size: size * 0.62, font, color });
        cx += font.widthOfTextAtSize(sup, size * 0.62) + 0.6;
      } else {
        page.drawText(part, { x: cx, y: yy, size, font, color });
        cx += font.widthOfTextAtSize(part, size);
      }
    }
  };

  const newPage = () => { page = pdf.addPage([W, H]); y = H - M - 10; };
  const need = (h: number) => { if (y - h < 78) newPage(); };

  // En-tête
  if (logo) {
    const lh = 44, lw = (logo.width / logo.height) * lh;
    page.drawImage(logo, { x: M, y: y - lh, width: lw, height: lh });
  } else {
    text("CODEM", M, y - 32, 30, bold);
  }
  const ref = r.reference ?? "";
  const label = "DOSSIER DE DEMANDE DE DEVIS";
  text(label, W - M - bold.widthOfTextAtSize(label, 8), y - 8, 8, bold, DARKGREEN);
  if (ref) text(ref, W - M - serif.widthOfTextAtSize(ref, 20), y - 30, 20, serif);
  const recu = "Reçu le " + new Date(r.created_at).toLocaleDateString("fr-FR", { timeZone: "Europe/Paris", day: "numeric", month: "long", year: "numeric" });
  text(recu, W - M - sans.widthOfTextAtSize(clean(sans, recu), 9), y - 44, 9, sans, GREY);
  y -= 62;
  page.drawRectangle({ x: M, y, width: CW, height: 2, color: GREEN });
  y -= 42;

  // Titre
  text("Votre projet de déménagement", M, y, 28, serif);
  y -= 22;
  const nom = r.nom || "";
  if (nom) { text("Préparé pour " + nom + (d.organisation ? " — " + String(d.organisation) : ""), M, y, 13, serifIt, GREY); y -= 8; }
  y -= 22;

  // Bandeau trajet
  const dep = show(d, "depart_commune") || show(d, "depart") || "—";
  const arr = show(d, "arrivee_commune") || show(d, "arrivee") || "—";
  const depP = show(d, "depart_pays"), arrP = show(d, "arrivee_pays");
  const bh = 104;
  page.drawRectangle({ x: M, y: y - bh, width: CW, height: bh, color: NAVY });
  const col = (CW - 40) / 3;
  const cell = (i: number, k: string, v: string, sub: string) => {
    const x = M + 20 + i * col;
    text(k.toUpperCase(), x, y - 26, 7.5, bold, GREEN);
    const lines = wrap(serif, 17, v, col - 16).slice(0, 2);
    lines.forEach((l, j) => text(l, x, y - 48 - j * 19, 17, serif, WHITE));
    if (sub) text(sub, x, y - 50 - lines.length * 19, 9, sans, rgb(0.8, 0.82, 0.9));
  };
  cell(0, "Départ", dep, depP);
  cell(1, "Arrivée", arr, arrP);
  cell(2, "Date souhaitée", show(d, "date") ? dateFr(String(d.date), { day: "numeric", month: "long", year: "numeric" }) : "À définir", show(d, "flexibilite"));
  y -= bh + 30;

  // Sections
  type Rows = [string, string][];
  const ROW = 13.5;
  const measure = (rows: Rows, vw: number) => rows.reduce((h, [, v]) => h + wrap(sans, 9.5, v, vw).length * ROW + 4, 0);
  const drawRows = (rows: Rows, x: number, lw: number, vw: number, y0: number) => {
    let yy = y0;
    for (const [k, v] of rows) {
      const lines = wrap(sans, 9.5, v, vw);
      text(k, x, yy, 8.5, sans, GREY);
      lines.forEach((l, j) => text(l, x + lw, yy - j * ROW, 9.5, sans, NAVY));
      yy -= lines.length * ROW + 4;
    }
  };
  const header = (titre: string, x: number, w: number, y0: number) => {
    text(titre, x, y0, 13.5, serif);
    page.drawRectangle({ x, y: y0 - 8, width: w, height: 0.8, color: LINE });
  };
  const keep = (rows: Rows) => rows.filter(([, v]) => v);

  // Une section sur toute la largeur
  const section = (titre: string, rows: Rows) => {
    rows = keep(rows);
    if (!rows.length) return;
    const lw = 140, vw = CW - lw;
    need(28 + Math.min(measure(rows, vw), 200));
    header(titre, M, CW, y);
    y -= 24;
    for (const rw of rows) {
      const h = measure([rw], vw);
      need(h);
      drawRows([rw], M, lw, vw, y);
      y -= h;
    }
    y -= 12;
  };

  // Deux sections côte à côte
  const pair = (t1: string, r1: Rows, t2: string, r2: Rows) => {
    r1 = keep(r1); r2 = keep(r2);
    if (!r1.length || !r2.length) { section(t1, r1); section(t2, r2); return; }
    const gap = 24, w = (CW - gap) / 2, lw = 92, vw = w - lw;
    const h = 24 + Math.max(measure(r1, vw), measure(r2, vw));
    need(h);
    header(t1, M, w, y);
    header(t2, M + w + gap, w, y);
    drawRows(r1, M, lw, vw, y - 24);
    drawRows(r2, M + w + gap, lw, vw, y - 24);
    y -= h + 12;
  };
  const rows = (keys: string[]) => keys.map((k) => [LABELS[k], show(d, k)] as [string, string]);

  pair(
    "Vos coordonnées",
    [["Nom", nom], ...rows(["organisation"]), ["Téléphone", r.telephone ?? ""], ["E-mail", r.email ?? ""], ...rows(["canal", "creneau"])],
    "Le projet",
    rows(["projet", "date", "flexibilite", "urgent", "groupage"]),
  );
  section("Contraintes", rows(["contraintes"]));
  pair(
    "Au départ",
    rows(["depart_commune", "depart_pays", "depart_type", "depart_etage", "depart_ascenseur", "depart_portage", "depart_stationnement", "depart_rue_etroite"]),
    "À l'arrivée",
    rows(["arrivee_commune", "arrivee_pays", "arrivee_type", "arrivee_etage", "arrivee_ascenseur", "arrivee_portage", "arrivee_stationnement", "arrivee_rue_etroite"]),
  );
  pair(
    "Volume à déménager",
    rows(["volume_mode", "taille", "surface", "volume", "annexes"]),
    "Formule et prestations",
    rows(["formule", "prestations"]),
  );
  section("Objets et remarques", rows(["objets", "message"]));
  if (photos.length || d.fichiers_echec) {
    section("Photos et vidéos jointes", [
      [photos.length > 1 ? `${photos.length} fichiers` : "1 fichier", photos.map((p) => p.split("/").pop()!.replace(/^\d+-/, "")).join(", ")],
      ...rows(["fichiers_echec"]),
    ]);
  }

  // Prochaines étapes
  const etapes = [
    "Un conseiller CODEM étudie votre dossier et, si besoin, les photos transmises.",
    `Il vous contacte${show(d, "creneau") && d.creneau !== "a-convenir" ? " sur le créneau choisi (" + show(d, "creneau").toLowerCase() + ")" : ""} pour valider les derniers détails ; une visite technique peut être proposée.`,
    "Vous recevez votre devis chiffré, détaillé et sans engagement.",
  ];
  const lignes = etapes.map((e) => wrap(sans, 10, e, CW - 70));
  const bh2 = 46 + lignes.reduce((a, l) => a + l.length * 14 + 8, 0);
  need(bh2 + 10);
  page.drawRectangle({ x: M, y: y - bh2, width: CW, height: bh2, color: PAPER });
  page.drawRectangle({ x: M, y: y - bh2, width: 3, height: bh2, color: GREEN });
  text("Les prochaines étapes", M + 22, y - 26, 14, serif);
  let yy = y - 50;
  lignes.forEach((ls, i) => {
    page.drawCircle({ x: M + 30, y: yy + 3.5, size: 8, color: NAVY });
    text(String(i + 1), M + 27.3, yy, 9, bold, WHITE);
    ls.forEach((l, j) => text(l, M + 48, yy - j * 14, 10, sans));
    yy -= ls.length * 14 + 8;
  });
  y -= bh2 + 10;

  // Pied de page sur chaque page
  const pages = pdf.getPages();
  pages.forEach((p, i) => {
    p.drawRectangle({ x: M, y: 58, width: CW, height: 0.8, color: LINE });
    const l1 = clean(bold, "CODEM Déménagement") ;
    p.drawText(l1, { x: M, y: 42, size: 8.5, font: bold, color: NAVY });
    p.drawText(clean(sans, `${CODEM.adresse}  ·  ${CODEM.tel}  ·  ${CODEM.mobile}`), { x: M + bold.widthOfTextAtSize(l1, 8.5) + 8, y: 42, size: 8.5, font: sans, color: GREY });
    p.drawText(clean(sans, "Récapitulatif de votre demande — ce document n'est pas un devis chiffré."), { x: M, y: 29, size: 7.5, font: sans, color: GREY });
    const num = `${i + 1} / ${pages.length}`;
    p.drawText(num, { x: W - M - sans.widthOfTextAtSize(num, 8), y: 29, size: 8, font: sans, color: GREY });
  });

  return await pdf.save();
}

const b64 = (bytes: Uint8Array) => {
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
};

// ---------- E-mails ----------
const row = (label: string, value: string) =>
  `<tr><td style="padding:6px 16px 6px 0;color:#666;vertical-align:top;white-space:nowrap">${esc(label)}</td><td style="padding:6px 0">${esc(value).replace(/\n/g, "<br>")}</td></tr>`;

const shell = (inner: string) =>
  `<div style="font-family:Arial,sans-serif;font-size:15px;color:#22264f;max-width:640px;line-height:1.5">${inner}</div>`;

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
  const codemTo = to.split(",").map((s) => s.trim());

  const d: Record<string, unknown> = r.donnees ?? {};
  const titre = TYPES[r.type] ?? "Demande";
  const quand = new Date(r.created_at).toLocaleString("fr-FR", { timeZone: "Europe/Paris", dateStyle: "full", timeStyle: "short" });
  const tel = r.telephone ? `<a href="tel:${esc(r.telephone)}" style="color:#2f7d1e">${esc(r.telephone)}</a>` : "—";
  const mail = r.email ? `<a href="mailto:${esc(r.email)}" style="color:#2f7d1e">${esc(r.email)}</a>` : "—";

  // Photos : liens privés valables 30 jours (pour CODEM uniquement)
  const photos: string[] = Array.isArray(d.fichiers) ? (d.fichiers as string[]) : [];
  let blocPhotos = "";
  if (photos.length) {
    const base = Deno.env.get("SUPABASE_URL");
    const service = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    const liens = await Promise.all(photos.map(async (path, i) => {
      const nomF = path.split("/").pop()!.replace(/^\d+-/, "");
      try {
        const res = await fetch(`${base}/storage/v1/object/sign/devis-photos/${path}`, {
          method: "POST",
          headers: { Authorization: `Bearer ${service}`, apikey: service!, "Content-Type": "application/json" },
          body: JSON.stringify({ expiresIn: 60 * 60 * 24 * 30 }),
        });
        const j = await res.json();
        if (!res.ok || !j.signedURL) throw new Error();
        return `<li style="margin:0 0 6px"><a href="${esc(base + "/storage/v1" + j.signedURL)}" style="color:#2f7d1e">${esc(nomF || "Fichier " + (i + 1))}</a></li>`;
      } catch {
        return `<li style="margin:0 0 6px">${esc(nomF)} (à voir dans Supabase → Storage → devis-photos)</li>`;
      }
    }));
    blocPhotos = `<h3 style="margin:24px 0 8px;font-size:16px">Photos et vidéos jointes (${photos.length})</h3><ul style="margin:0;padding-left:18px;font-size:14px">${liens.join("")}</ul><p style="margin:6px 0 0;color:#666;font-size:12px">Liens valables 30 jours, puis consultables dans Supabase → Storage → devis-photos.</p>`;
  }

  const send = (body: Record<string, unknown>) =>
    fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from, ...body }),
    });

  // ----- Devis : PDF à CODEM + copie au client -----
  if (r.type === "devis") {
    let pdfB64 = "";
    try { pdfB64 = b64(await buildPdf(r, d, photos)); } catch (e) { console.error("PDF", e); }
    const fichier = `CODEM-dossier-${r.reference ?? "devis"}.pdf`;
    const pj = pdfB64 ? [{ filename: fichier, content: pdfB64 }] : undefined;
    const trajet = `${show(d, "depart_commune") || "—"} → ${show(d, "arrivee_commune") || "—"}`;
    const dateV = show(d, "date") || "à définir";

    const htmlCodem = shell(`
<p style="margin:0 0 4px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5fb03a;font-weight:bold">Site CODEM</p>
<h2 style="margin:0 0 6px;font-size:22px">Nouvelle demande de devis${r.reference ? " · " + esc(r.reference) : ""}</h2>
<p style="margin:0 0 18px;color:#666;font-size:13px">Reçue le ${esc(quand)}</p>
<div style="background:#f4f6f1;border-radius:10px;padding:14px 16px;margin:0 0 18px">
<p style="margin:0 0 6px;font-size:17px"><strong>${esc(r.nom ?? "Sans nom")}</strong>${d.organisation ? " · " + esc(d.organisation) : ""}</p>
<p style="margin:0 0 4px">Téléphone : ${tel}</p>
<p style="margin:0">E-mail : ${mail}</p>
</div>
<table style="border-collapse:collapse;font-size:14px">
${row("Trajet", trajet)}${row("Date souhaitée", dateV)}${show(d, "formule") ? row("Formule", show(d, "formule")) : ""}${show(d, "creneau") ? row("Rappel", show(d, "creneau")) : ""}
</table>
<p style="margin:18px 0 0">Le dossier complet est joint en PDF${pdfB64 ? "" : " (PDF indisponible : voir la table demandes dans Supabase)"}.</p>
${blocPhotos}`);

    const res = await send({ to: codemTo, reply_to: r.email || undefined, subject: `Devis ${r.reference ?? ""} — ${r.nom ?? "site CODEM"} · ${trajet}`, html: htmlCodem, attachments: pj });

    // Copie au client (nécessite un domaine vérifié dans Resend pour écrire à n'importe quelle adresse)
    let client = "pas d'e-mail client";
    if (r.email && pdfB64) {
      const prenom = String(r.nom ?? "").split(" ")[0];
      const htmlClient = shell(`
<img src="${SITE}/assets/logo-pdf.png" alt="CODEM" width="150" style="display:block;margin:0 0 22px">
<p style="margin:0 0 14px">Bonjour${prenom ? " " + esc(prenom) : ""},</p>
<p style="margin:0 0 14px">Merci pour votre confiance. Nous avons bien reçu votre demande de devis <strong>${esc(r.reference ?? "")}</strong> pour votre déménagement <strong>${esc(trajet)}</strong>.</p>
<p style="margin:0 0 14px">Vous trouverez en pièce jointe le récapitulatif de votre projet. Un conseiller CODEM l'étudie et vous recontacte${show(d, "creneau") && d.creneau !== "a-convenir" ? " sur le créneau choisi (" + esc(show(d, "creneau").toLowerCase()) + ")" : ""} afin de vous adresser un devis chiffré, détaillé et sans engagement.</p>
<p style="margin:0 0 22px">Une précision à apporter ? Répondez simplement à cet e-mail ou appelez-nous au <a href="tel:+33171361838" style="color:#2f7d1e">${CODEM.tel}</a>.</p>
<p style="margin:0">À très bientôt,<br><strong>L'équipe CODEM Déménagement</strong></p>
<p style="margin:26px 0 0;padding-top:14px;border-top:1px solid #e3e5ea;color:#888;font-size:12px">CODEM · ${esc(CODEM.adresse)} · ${CODEM.tel}</p>`);
      const rc = await send({ to: [r.email], reply_to: codemTo[0], subject: `Votre demande de devis CODEM — ${r.reference ?? ""}`, html: htmlClient, attachments: pj });
      client = rc.ok ? "copie client envoyée" : "copie client refusée : " + (await rc.text());
      console.log(client);
    }
    return new Response(JSON.stringify({ codem: res.status, client }), { status: res.ok ? 200 : 502 });
  }

  // ----- Rappel, visite, message : récapitulatif à CODEM -----
  const ordre = ["projet", "type", "preference", "creneau", "depart", "arrivee", "periode", "message"];
  const lignes = ordre.filter((k) => show(d, k)).map((k) => row(LABELS[k], show(d, k))).join("");
  const html = shell(`
<p style="margin:0 0 4px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5fb03a;font-weight:bold">Site CODEM</p>
<h2 style="margin:0 0 6px;font-size:22px">${esc(titre)}</h2>
<p style="margin:0 0 18px;color:#666;font-size:13px">Reçue le ${esc(quand)} · page ${esc(r.page)}</p>
<div style="background:#f4f6f1;border-radius:10px;padding:14px 16px;margin:0 0 20px">
<p style="margin:0 0 6px;font-size:17px"><strong>${esc(r.nom ?? "Sans nom")}</strong></p>
<p style="margin:0 0 4px">Téléphone : ${tel}</p>
<p style="margin:0">E-mail : ${mail}</p>
</div>
<table style="border-collapse:collapse;font-size:14px;width:100%">${lignes}</table>`);
  const res = await send({ to: codemTo, reply_to: r.email || undefined, subject: `${titre} — ${r.nom ?? "site CODEM"}`, html });
  return new Response(await res.text(), { status: res.ok ? 200 : 502 });
});
