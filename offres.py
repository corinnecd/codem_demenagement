"""Programme Coulisses et offres saisonnières : bandeau, bandes et page dédiée.

Les taux, les fenêtres de dates et les modalités de droit à l'image sont
rassemblés dans build.py (COULISSES_*, CREUX_REMISE, REMISE_MAX, OFFRES)
afin que CODEM puisse les modifier en un seul endroit.
"""
import build as b
from build import t,url,link,eyebrow,cta,COULISSES_REMISE,COULISSES_PLACES,CREUX_REMISE,REMISE_MAX

# ── Décor festif (SVG inline, aucun fichier externe) ────────────────
FLOCON='<svg class="fx-flake" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7M12 2l-2.2 2.2M12 2l2.2 2.2M12 22l-2.2-2.2M12 22l2.2-2.2"/></svg>'
CADEAU='<svg class="fx-gift" viewBox="0 0 32 32" aria-hidden="true"><rect x="4" y="13" width="24" height="16" rx="2" fill="#b3122e"/><rect x="2.5" y="9" width="27" height="6" rx="1.5" fill="#d61f3f"/><rect x="14" y="9" width="4" height="20" fill="#f3c969"/><path d="M16 9c-3-5-8-5-8-2s5 2 8 2zm0 0c3-5 8-5 8-2s-5 2-8 2z" fill="none" stroke="#f3c969" stroke-width="2"/></svg>'
def lien(o):return url('devis')+'?offre='+o['cle']
def neige(n=14):return '<span class="fx-snow" aria-hidden="true">'+''.join(f'<i style="--x:{(i*37)%100}%;--d:{6+(i*7)%9}s;--s:{.6+((i*13)%10)/10}"></i>' for i in range(n))+'</span>'
def compte(o):return f'<span class="fx-count" data-fin="{o["au"]}">{t(*o["fin_txt"])}</span>'

# ── Bandeau festif sous l'en-tête (pages intérieures) ───────────────
def bar(key):
 o=b.offre_active()
 if not o or key in ('devis','home'):return ''  # accueil : pastille dans le hero (le header y est flottant)
 return (f'<a class="offre-bar fx fx-{o.get("theme","")}" href="{lien(o)}">{neige()}'
  f'{CADEAU}<span class="ob-seal">−{o["pct"]}<small>%</small></span>'
  f'<span class="ob-txt"><strong>{t(*o["titre"])}</strong><span class="ob-pitch">{t(*o["pitch"])}</span></span>'
  f'{compte(o)}<span class="ob-cta">{t("J’en profite","Claim it")} <span aria-hidden="true">→</span></span></a>')

def hero_pill():
 o=b.offre_active()
 if not o:return ''
 return (f'<a class="hero-offre fx fx-{o.get("theme","")}" href="{lien(o)}">{neige(8)}{CADEAU}'
  f'<span class="ho-seal">−{o["pct"]} %</span><span class="ho-txt"><strong>{t(*o["titre"])}</strong>{compte(o)}</span>'
  f'<span class="ho-go" aria-hidden="true">→</span></a>')

# ── Bannière en tête de la page devis : l'offre est visible et transmise ──
def devis_banner():
 o=b.offre_active()
 if not o:return ''
 d0,d1=o['demenagement']
 val=f'{t(*o["titre"])} (−{o["pct"]} %)'
 return (f'<div class="wrap"><section class="devis-offre fx fx-{o.get("theme","")}" data-offre-banner data-offre-label="{val}" data-offre-debut="{d0}" data-offre-fin="{d1}" aria-live="polite">{neige(18)}'
  f'<div class="do-seal"><strong>−{o["pct"]}<small>%</small></strong><span>{t("sur votre devis","off your quote")}</span></div>'
  f'<div class="do-body"><p class="do-kicker">{CADEAU}<span data-offre-etat>{t("Offre activée pour votre demande","Offer applied to your request")}</span></p>'
  f'<h2>{t(*o["titre"])}</h2><p class="do-pitch">{t(*o["pitch"])} {t("La remise est notée sur votre demande : votre conseiller l’applique directement au devis.","The discount is recorded with your request: your adviser applies it directly to the quote.")}</p>'
  f'<p class="do-date" data-offre-date hidden></p></div>'
  f'<div class="do-timer">{compte(o)}</div></section></div>')

# ── Bande « Coulisses » pour l'accueil ──────────────────────────────
FILM=[
 ('J-30',"Le projet se décide","The move is decided","Le logement encore en place, les premières questions, le tri qui commence.","The home still as it was, the first questions, the sorting that begins."),
 ('J-15',"Les cartons arrivent","The boxes arrive","Les fournitures livrées, la première pièce emballée, la checklist au mur.","Supplies delivered, the first room packed, the checklist on the wall."),
 ('J-7',"La dernière semaine","The final week","Les démarches, les enfants qui aident, l’appartement qui se vide.","The paperwork, the children helping, the flat emptying out."),
 ('Jour J',"L’équipe arrive","The team arrives","Le camion devant la porte, la protection des sols, le premier meuble qui descend.","The truck at the door, floors protected, the first piece of furniture going down."),
 ('Jour J',"Le chargement","Loading","Le monte-meubles, les gestes de l’équipe, le dernier tour du logement vide.","The furniture lift, the crew at work, one last look round the empty home."),
 ('Jour J',"L’arrivée","Arrival","Le déchargement, le remontage, la première pièce installée.","Unloading, reassembly, the first room set up."),
 ('J+15',"Votre témoignage","Your story","Quelques phrases chez vous, installé, en toute liberté.","A few words at home, settled in, entirely in your own terms."),
]

def band():
 """Bande d'appel : programme Coulisses + offre saisonnière si elle est active."""
 o=b.offre_active()
 saison=''
 if o:
  saison=(f'<a class="cb-saison" href="{lien(o)}"><span class="cbs-tag">−{o["pct"]} %</span>'
   f'<div><p class="cbs-title">{t(*o["titre"])}</p><p>{t(*o["pitch"])} <em>{t(*o["fin_txt"])}.</em></p></div></a>')
 puces=''.join(f'<li><span>{a}</span>{t(fr,en)}</li>' for a,fr,en,_d,_e in FILM[:4])
 return (f'<section class="section band-navy coulisses-band" id="coulisses">'
  f'<div class="wrap cb-grid"><div class="cb-text">{eyebrow("Programme Coulisses","Behind-the-scenes programme")}'
  f'<h2>{t("Votre déménagement<br><em>raconté en vidéo.</em>","Your move,<br><em>told in video.</em>")}</h2>'
  f'<p class="lead">{t(f"Chaque mois, nous suivons en vidéo {COULISSES_PLACES} déménagements, du premier carton au dernier. Vous aidez les familles qui hésitent encore à se projeter — et nous vous remercions de {COULISSES_REMISE} % sur votre devis.",f"Each month we follow {COULISSES_PLACES} moves on video, from the first box to the last. You help families who are still hesitating to picture it — and we thank you with {COULISSES_REMISE}% off your quote.")}</p>'
  f'<ul class="cb-steps">{puces}<li class="cb-more"><span>…</span>{t("et votre témoignage, une fois installé","and your story, once you’re settled")}</li></ul>'
  f'<div class="actions">{link("coulisses",t("Comment ça marche","How it works"),"btn")}{link("devis",t("Demander un devis","Request a quote"),"text-link")}</div>'
  f'<p class="fine-print">{t("Zones privées exclues, relecture avant publication, retrait possible à tout moment.","Private areas excluded, you review before publication, and you can withdraw at any time.")}</p></div>'
  f'<aside class="cb-card"><span class="cb-badge">−{COULISSES_REMISE} %</span>'
  f'<p class="cb-badge-txt">{t("sur votre devis","off your quote")}</p>'
  f'<p class="cb-places">{t(f"{COULISSES_PLACES} déménagements par mois",f"{COULISSES_PLACES} moves a month")}</p>'
  f'{b.mascot("montre","cb-mascot",150)}{saison}</aside></div></section>')

# ── Note contextuelle dans l'étape Calendrier du devis ──────────────
def saison_note():
 o=b.offre_active()
 attrs=''
 if o:
  attrs=(f' data-offre-debut="{o["demenagement"][0]}" data-offre-fin="{o["demenagement"][1]}"'
   f' data-offre="{t(*o["titre"])} : −{o["pct"]} % sur cette date. {t(*o["pitch"])}"')
 creux=t(f"Bonne nouvelle : cette date tombe en semaine, hors haute saison. Une remise de {CREUX_REMISE} % peut s’appliquer — votre conseiller vous le confirme.",
  f"Good news: this date falls midweek, outside the busy season. A {CREUX_REMISE}% discount may apply — your adviser will confirm it.")
 return f'<p class="saison-note" data-saison-note hidden data-creux="{creux}"{attrs}></p>'

# ── Bloc à cocher dans l'étape Coordonnées du devis ─────────────────
def devis_block():
 return (f'<div class="offre-check"><span class="oc-tag">−{COULISSES_REMISE} %</span><div class="oc-body">'
  f'<p class="oc-title">{t("Programme Coulisses","Behind-the-scenes programme")}</p>'
  f'<p class="oc-txt">{t(f"Vous acceptez que votre déménagement soit filmé pour nos réseaux sociaux ? Nous vous remercions de {COULISSES_REMISE} % sur votre devis. Tournage discret, zones privées exclues, relecture avant publication.",f"Happy for your move to be filmed for our social media? We thank you with {COULISSES_REMISE}% off your quote. Discreet filming, private areas excluded, and you review before publication.")}</p>'
  f'<label class="check"><input type="checkbox" name="coulisses" value="oui"><span>{t("Ce programme m’intéresse, parlons-en.","I’m interested — let’s talk about it.")}</span></label>'
  f'<p class="fine-print"><a href="{url("coulisses")}" target="_blank" rel="noopener">{t("Ce qui est filmé, ce qui ne l’est jamais","What is filmed, and what never is")} →</a></p></div></div>')

# ── Page dédiée ─────────────────────────────────────────────────────
JAMAIS=[
 ("Les chambres d’enfants et le visage des mineurs, sans votre accord écrit.","Children’s bedrooms and minors’ faces, without your written consent."),
 ("Vos papiers, vos écrans, votre courrier et vos objets de valeur.","Your paperwork, screens, post and valuables."),
 ("Le montant de votre devis et vos coordonnées.","Your quote amount and your contact details."),
 ("Les voisins et les passants identifiables.","Identifiable neighbours and passers-by."),
 ("Toute pièce ou tout moment que vous nous demandez de laisser de côté, le jour même, sans justification à donner.","Any room or moment you ask us to leave out, on the day, with no explanation needed."),
]
DROITS=[
 ("Relecture","You review first","Vous voyez chaque vidéo avant sa publication et vous pouvez demander une coupe.","You see every video before it is published and can ask for a cut."),
 ("Retrait","Withdrawal","Vous pouvez retirer votre accord à tout moment : nous dépublions les vidéos concernées.","You can withdraw your consent at any time: we take the videos down."),
 ("Diffusion","Where it appears","Les vidéos sont diffusées sur les réseaux sociaux de CODEM et sur ce site, et nulle part ailleurs.","The videos appear on CODEM’s social media and on this site, nowhere else."),
 ("Aucune cession","Never sold on","Les images ne sont ni vendues ni cédées à un tiers, et ne servent jamais à de la publicité payante sans votre accord.","The footage is never sold or passed to a third party, and never used in paid advertising without your agreement."),
]
COMMENT=[
 ("1","Vous nous le dites","You tell us","Cochez la case « Programme Coulisses » dans votre demande de devis, ou mentionnez-le à votre conseiller. Nous revenons vers vous sous 24 h ouvrées.","Tick the “Behind-the-scenes programme” box in your quote request, or mention it to your adviser. We come back to you within one working day."),
 ("2","Nous cadrons ensemble","We agree the frame","Avant le tournage, nous décidons avec vous de ce qui peut être filmé et de ce qui reste privé. C’est écrit dans l’autorisation de droit à l’image que vous signez.","Before filming, we decide together what can be filmed and what stays private. It is written into the image-rights agreement you sign."),
 ("3",f"La remise s’applique sur le devis","The discount lands on the quote",f"Les {COULISSES_REMISE} % apparaissent directement sur votre devis, avant signature. Rien à réclamer après coup.",f"The {COULISSES_REMISE}% appears directly on your quote, before you sign. Nothing to claim afterwards."),
]

def page():
 o=b.offre_active()
 comment=''.join(f'<li><span class="cm-num">{n}</span><h3>{t(fr,en)}</h3><p>{t(d,e)}</p></li>' for n,fr,en,d,e in COMMENT)
 frise=''.join(f'<li><span class="fl-day">{a}</span><h3>{t(fr,en)}</h3><p>{t(d,e)}</p></li>' for a,fr,en,d,e in FILM)
 jamais=''.join(f'<li>{t(fr,en)}</li>' for fr,en in JAMAIS)
 droits=''.join(f'<div><h3>{t(fr,en)}</h3><p>{t(d,e)}</p></div>' for fr,en,d,e in DROITS)
 saison=''
 if o:
  saison=(f'<section class="section band-sand"><div class="wrap offre-saison"><span class="os-tag">−{o["pct"]} %</span>'
   f'<div>{eyebrow("Offre en cours","Current offer")}<h2>{t(*o["titre"])}</h2>'
   f'<p class="lead">{t(*o["pitch"])}</p><p>{t(*o["detail"])}</p>'
   f'<p class="os-end">{t(*o["fin_txt"])}</p>'
   f'<div class="actions"><a class="btn btn-cta" href="{lien(o)}">{t("J’en profite","Claim the offer")}</a></div></div></div></section>')
 return (f'<section class="section band-ivory coulisses-hero" style="padding-top:28px"><div class="wrap ch-grid"><div>'
  f'{eyebrow("Programme Coulisses","Behind-the-scenes programme")}'
  f'<h1>{t("Votre déménagement<br><em>raconté en vidéo.</em>","Your move,<br><em>told in video.</em>")}</h1>'
  f'<p class="lead">{t(f"Les futurs clients veulent voir à quoi ressemble vraiment un déménagement : les cartons de la première semaine, le camion devant la porte, la première pièce installée. Chaque mois, nous suivons {COULISSES_PLACES} déménagements en vidéo. Si vous acceptez que le vôtre en fasse partie, nous vous remercions de {COULISSES_REMISE} % sur votre devis.",f"Future customers want to see what a move really looks like: the first week’s boxes, the truck at the door, the first room set up. Each month we follow {COULISSES_PLACES} moves on video. If you agree to yours being one of them, we thank you with {COULISSES_REMISE}% off your quote.")}</p>'
  f'<div class="actions">{link("devis",t("Demander mon devis","Get my quote"),"btn btn-cta")}<a class="text-link" href="#jamais">{t("Ce que nous ne filmons jamais","What we never film")}</a></div></div>'
  f'<aside class="ch-badge"><strong>−{COULISSES_REMISE} %</strong><span>{t("sur votre devis","off your quote")}</span>'
  f'<p>{t(f"{COULISSES_PLACES} déménagements par mois",f"{COULISSES_PLACES} moves a month")}</p>{b.mascot("pouce","ch-mascot",150)}</aside></div></section>'
  f'<section class="section"><div class="wrap">{eyebrow("En trois étapes","In three steps")}'
  f'<h2>{t("Comment ça se passe.","How it works.")}</h2><ol class="cm-grid">{comment}</ol></div></section>'
  f'<section class="section band-navy film-band"><div class="wrap">{eyebrow("Le fil du tournage","The filming thread")}'
  f'<h2>{t("Du premier carton<br><em>au premier café chez vous.</em>","From the first box<br><em>to your first coffee at home.</em>")}</h2>'
  f'<p class="lead">{t("Quelques minutes de tournage à chaque étape, jamais une journée entière avec une caméra dans le dos.","A few minutes of filming at each stage — never a whole day with a camera behind you.")}</p>'
  f'<ol class="film-line">{frise}</ol></div></section>'
  f'<section class="section band-ivory" id="jamais"><div class="wrap two-col-note"><div>{eyebrow("Votre intimité","Your privacy")}'
  f'<h2>{t("Ce que nous ne filmons<br><em>jamais.</em>","What we never<br><em>film.</em>")}</h2>'
  f'<p>{t("La liste ci-dessous s’applique par défaut, sans que vous ayez à la demander. Vous pouvez l’allonger autant que vous le souhaitez avant le tournage.","The list below applies by default, without you having to ask. You can add to it as much as you like before filming.")}</p></div>'
  f'<ul class="never-list">{jamais}</ul></div></section>'
  f'<section class="section"><div class="wrap">{eyebrow("Vos droits","Your rights")}'
  f'<h2>{t("Vous gardez la main,<br><em>du début à la fin.</em>","You stay in control,<br><em>from start to finish.</em>")}</h2>'
  f'<div class="droits-grid">{droits}</div>'
  f'<p class="fine-print">{t(f"Programme limité à {COULISSES_PLACES} déménagements par mois. La remise n’est pas cumulable au-delà de {REMISE_MAX} % avec une offre saisonnière. Les modalités définitives figurent dans l’autorisation de droit à l’image signée avant le tournage.",f"Programme limited to {COULISSES_PLACES} moves a month. The discount cannot be combined beyond {REMISE_MAX}% with a seasonal offer. The final terms are set out in the image-rights agreement signed before filming.")}</p></div></section>'
  f'{saison}{cta(t("Et si c’était<br><em>votre déménagement ?</em>","What if it were<br><em>your move?</em>"))}')

def write_all():
 b.write('coulisses',page(),t(
  f'Programme Coulisses CODEM : acceptez que votre déménagement soit filmé et bénéficiez de {COULISSES_REMISE} % sur votre devis. Zones privées exclues, relecture avant publication.',
  f'CODEM’s behind-the-scenes programme: agree to your move being filmed and get {COULISSES_REMISE}% off your quote. Private areas excluded, you review before publication.'))
