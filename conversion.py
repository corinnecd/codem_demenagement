"""Blocs de conversion : faits de confiance, preuves (exemples en mode aperçu), devis express."""
import build as b
from build import t,url,link,img,eyebrow,PHONE,PHONE_HREF

# Engagement de délai affiché près des boutons, à confirmer par CODEM
REPONSE=('Réponse sous 24 h ouvrées','Reply within 1 working day')
def reponse():return t(*REPONSE)

# ---------------------------------------------------------------------------
# 1. Faits VRAIS, visibles par tous
FAITS=[('Agence à Nogent-sur-Marne','Office in Nogent-sur-Marne'),
 ('Devis gratuit et sans engagement','Free quote, no obligation'),
 REPONSE,
 ('Équipe FR · PT · ES · EN','Team speaks FR · PT · ES · EN'),
 ('5 formules, de Self à Grand Confort','5 packages, from Self to Grand Confort')]
def faits_band(cls='',sans=()):
 return f'<ul class="facts-band {cls}" aria-label="{t("Pourquoi CODEM","Why CODEM")}">'+''.join(f'<li><span class="fact-dot" aria-hidden="true"></span>{t(a,c)}</li>' for a,c in FAITS if a not in sans)+'</ul>'

# ---------------------------------------------------------------------------
# 2. Preuves d'EXEMPLE : visibles uniquement en mode aperçu (?apercu=1), jamais au public.
#    À remplacer par les vraies données CODEM, puis retirer la classe demo-proof.
def badge():return f'<span class="demo-badge">{t("Exemple à remplacer","Example to replace")}</span>'
STARS='<span class="stars" aria-label="5/5">★★★★★</span>'
AVIS=[
 ('Sophie M.','Paris 11e → Nogent-sur-Marne · T3','Paris 11th → Nogent-sur-Marne · 2-bed flat','Équipe ponctuelle et très soigneuse. Rien d’abîmé, même le miroir ancien de ma grand-mère. Le conseiller avait tout anticipé.','Punctual, very careful team. Nothing damaged, not even my grandmother’s antique mirror. The adviser had planned everything.'),
 ('Karim B.','Vincennes → Lyon · Maison','Vincennes → Lyon · House','Devis clair, conseiller joignable du début à la fin, et le camion était devant chez nous à 8 h pile.','Clear quote, an adviser who was always reachable, and the truck was outside at 8 am sharp.'),
 ('Cabinet Delorme','Transfert de bureaux · 25 postes','Office relocation · 25 workstations','Déménagement de nos bureaux un vendredi soir : tout était réinstallé et étiqueté le lundi matin. Aucune journée perdue.','Our office moved on a Friday evening: everything was set up and labelled by Monday morning. Not a single day lost.'),
 ('Ana P.','Paris → Porto · Groupage','Paris → Porto · Shared load','Une équipe qui parle portugais, c’est très rassurant pour un déménagement à l’étranger. Livraison dans les délais annoncés.','A team that speaks Portuguese is very reassuring for a move abroad. Delivered on the date we were given.'),
 ('Thomas L.','Garde-meubles · 4 mois','Storage · 4 months','Stockage entre deux appartements, meubles rendus dans l’état exact où je les avais laissés. Simple et sans surprise.','Storage between two flats; furniture returned exactly as I left it. Simple, no surprises.'),
 ('Hélène D.','Piano droit · 4e sans ascenseur','Upright piano · 4th floor, no lift','J’avais très peur pour le piano. Ils ont pris le temps d’étudier l’escalier et tout s’est passé parfaitement.','I was very worried about the piano. They took the time to study the staircase and everything went perfectly.'),
]
def avis_cards(idx):
 return ''.join(f'<figure class="review-card">{STARS}<blockquote>« {t(a[3],a[4])} »</blockquote><figcaption><strong>{a[0]}</strong><span>{t(a[1],a[2])}</span></figcaption></figure>' for a in (AVIS[i] for i in idx))
CHIFFRES=[('4,9/5','4.9/5','Note Google · 180 avis','Google rating · 180 reviews'),('1 500+','1,500+','Déménagements réalisés','Moves completed'),('15 ans','15 years','D’expérience à Nogent-sur-Marne','Of experience in Nogent-sur-Marne'),('98 %','98%','Clients qui nous recommandent','Clients who recommend us')]
def chiffres():
 return '<div class="stats-row">'+''.join(f'<div class="stat"><strong>{t(a,b2)}</strong><span>{t(c,d)}</span></div>' for a,b2,c,d in CHIFFRES)+'</div>'
def logos():
 return f'<div class="logo-row" aria-label="{t("Entreprises clientes","Business clients")}">'+''.join(f'<span class="logo-ph">{t("Logo client","Client logo")} {i}</span>' for i in range(1,7))+'</div>'
CAS=[('entreprise-camion','Transfert de bureaux · 25 postes','Office relocation · 25 workstations','Paris 8e → Montreuil','Paris 8th → Montreuil','Déménager sans interrompre l’activité.','Move without interrupting business.','Inventaire et étiquetage par service, chargement le vendredi à 18 h, réinstallation pendant le week-end.','Inventory and labelling by department, loading on Friday at 6 pm, set-up over the weekend.','Bureaux opérationnels le lundi 9 h','Offices up and running Monday 9 am'),
 ('particulier-immeuble','Appartement T4 · Paris → Porto','3-bed flat · Paris → Porto','Paris 16e → Porto','Paris 16th → Porto','Un départ à l’étranger avec un budget maîtrisé.','A move abroad on a controlled budget.','Groupage sur poids lourd, emballage du fragile, échanges en portugais avec la famille.','Shared heavy-goods load, fragile items packed, communication in Portuguese with the family.','Livré en 6 jours, budget respecté','Delivered in 6 days, on budget'),
 ('piano','Piano droit · 4e étage sans ascenseur','Upright piano · 4th floor, no lift','Vincennes','Vincennes','Descendre un piano de 230 kg par un escalier étroit.','Bring a 230 kg piano down a narrow staircase.','Visite technique, sangles et protections sur mesure, équipe de quatre déménageurs.','Technical visit, custom straps and protection, a team of four movers.','Zéro rayure, accordage préservé','Not a scratch, tuning preserved')]
def cas_cards():
 return '<div class="case-grid">'+''.join(f'<article class="case-card"><div class="image-wrap">{img(im,t(a,c))}</div><div class="case-body"><span class="eyebrow">{t(d,e)}</span><h3>{t(a,c)}</h3><dl><dt>{t("Le besoin","The need")}</dt><dd>{t(f,g)}</dd><dt>{t("La solution","The solution")}</dt><dd>{t(h,i)}</dd></dl><p class="case-result">{t(j,k)}</p></div></article>' for im,a,c,d,e,f,g,h,i,j,k in CAS)+'</div>'

def demo(inner,cls='section band-ivory'):
 return f'<section class="demo-proof {cls}" data-demo><div class="wrap">{badge()}{inner}</div></section>'

def home_proofs():
 return demo(f'<div class="section-heading"><div>{eyebrow("Ils nous ont confié leur déménagement","They trusted us with their move")}<h2>{t("Ce que nos clients<br><em>retiennent de CODEM.</em>","What our clients<br><em>remember about CODEM.</em>")}</h2></div></div>{chiffres()}<div class="review-grid">{avis_cards([0,1,2])}</div><div class="actions">{link("devis",t("Recevoir mon devis gratuit","Get my free quote"),"btn btn-cta")}{link("avis",t("Lire tous les avis","Read all reviews"),"text-link")}</div>')
def entreprises_proofs():
 return demo(f'{eyebrow("Ils nous font confiance","They trust us")}<h2>{t("Des entreprises<br><em>qui ont déménagé avec CODEM.</em>","Businesses<br><em>that moved with CODEM.</em>")}</h2>{logos()}<div class="review-grid one">{avis_cards([2])}</div>','section band-glacier')
def avis_demo():
 return demo(f'{chiffres()}<div class="review-grid">{avis_cards(range(len(AVIS)))}</div>')
def realisations_demo():
 return demo(cas_cards())
def quote_proof():
 return f'<div class="demo-proof quote-proof" data-demo>{badge()}<p class="qp-rating"><strong>4,9/5</strong> {STARS}<span>{t("180 avis Google","180 Google reviews")}</span></p><blockquote>« {t(AVIS[1][3],AVIS[1][4])} »</blockquote><cite>{AVIS[1][0]}</cite></div>'

# ---------------------------------------------------------------------------
# 3. Devis express
def surfaces():return [('','Sélectionner','Select'),('moins-30','Moins de 30 m²','Under 30 m²'),('30-50','30 à 50 m²','30 to 50 m²'),('50-80','50 à 80 m²','50 to 80 m²'),('80-120','80 à 120 m²','80 to 120 m²'),('120-180','120 à 180 m²','120 to 180 m²'),('plus-180','Plus de 180 m²','Over 180 m²'),('inconnu','Je ne sais pas','I don’t know')]
PAYS=[('France','France','France'),('Portugal','Portugal','Portugal'),('Espagne','Espagne','Spain'),('Italie','Italie','Italy'),('Autre','Autre pays','Other country')]
CRENEAUX=[('','Sélectionner','Select'),('matin','Matin 9 h – 12 h','Morning 9 am – 12 pm'),('apres-midi','Après-midi 13 h – 18 h','Afternoon 1 pm – 6 pm'),('a-convenir','À convenir','To be agreed')]
def express(PROJECTS,field,SELECT,privacy,status_msg,FORM_ENDPOINT):
 projets=[('',t('Votre projet','Your project'),t('Votre projet','Your project'))]+[(v,a,c) for v,a,c,_,__ in PROJECTS]
 tailles=[SELECT,('studio','Studio / T1','Studio / 1 room'),('t2-t3','T2 – T3','2 – 3 rooms'),('t4','T4 et plus','4 rooms or more'),('maison','Maison','House'),('bureaux','Bureaux','Offices'),('inconnu','Je ne sais pas','I don’t know')]
 form=f'''<form class="express-card" id="express-form" data-kind="devis" data-endpoint="{FORM_ENDPOINT}" novalidate>
<span class="eyebrow">{t('Devis express · 1 minute','Express quote · 1 minute')}</span><h1>{t('Recevez votre devis<br><em>gratuit.</em>','Get your<br><em>free quote.</em>')}</h1>
<p class="express-lead">{t('L’essentiel suffit : votre trajet et votre numéro. Un conseiller CODEM vous rappelle pour préciser le reste.','The essentials are enough: your route and your number. A CODEM adviser calls you back to cover the rest.')}</p>
<input type="hidden" name="mode" value="express">
<p class="ex-group">{t('1. Votre projet','1. Your move')}</p><div class="fields">{field('projet','Projet','Project',required=True,options=projets,fid='ex-projet')}{field('surface_tranche','Surface du logement','Floor area',options=surfaces(),fid='ex-surface')}{field('depart_commune','Ville de départ','Moving from',required=True,fid='ex-depart')}{field('arrivee_commune','Ville d’arrivée','Moving to',required=True,fid='ex-arrivee')}{field('arrivee_pays','Pays d’arrivée','Destination country',options=PAYS,fid='ex-pays')}{field('date','Date souhaitée (facultatif)','Preferred date (optional)',kind='date',attrs='data-min-today',fid='ex-date')}<p class="field full ex-help"><a href="{url('conseils')}#volume">{t('Vous ne connaissez pas votre surface ? Calculez votre volume pièce par pièce','Not sure of your floor area? Calculate your volume room by room')}</a></p><div class="field full"><label class="check"><input type="checkbox" name="arrivee_inconnue" value="oui" id="ex-inconnue"><span>{t('Je ne connais pas encore mon adresse d’arrivée','I don’t know my destination address yet')}</span></label></div></div><p class="ex-group">{t('2. Vos coordonnées','2. Your details')}</p><div class="fields">{field('nom','Nom','Name',required=True,fid='ex-nom')}{field('telephone','Téléphone','Phone',kind='tel',required=True,fid='ex-tel')}{field('email','E-mail (pour recevoir une copie)','Email (to receive a copy)',kind='email',fid='ex-email')}{field('creneau','Quand vous rappeler ?','When should we call?',options=CRENEAUX,fid='ex-creneau')}</div>
{privacy()}<button class="btn btn-cta btn-lg express-submit" type="submit">{t('Recevoir mon devis gratuit','Get my free quote')}</button>
<p class="express-promise">{t('Sans engagement','No obligation')} · {reponse()}</p>{status_msg()}
<div class="express-done" hidden><div class="confirm-icon" aria-hidden="true">✓</div><h2 tabindex="-1">{t('Demande envoyée','Request sent')}</h2><p>{t('Numéro de demande :','Request number:')} <strong data-ex-ref></strong></p><p>{t('Un conseiller CODEM vous rappelle.','A CODEM adviser will call you back.')} {reponse()}.</p><div class="express-more"><p><strong>{t('Envie d’un devis encore plus précis ?','Want an even more accurate quote?')}</strong><br>{t('Ajoutez les accès, le volume et des photos : votre demande est déjà pré-remplie.','Add access details, volume and photos: your request is already pre-filled.')}</p><a class="btn" data-ex-complete href="#">{t('Compléter ma demande','Complete my request')}</a></div><a class="text-link" href="{PHONE_HREF}" data-zone="confirmation">{t('Ou appelez-nous','Or call us')} : {PHONE}</a></div>
</form>'''
 aside=f'''<aside class="express-side"><h2>{t('Comment ça marche','How it works')}</h2><ol class="express-steps"><li><strong>{t('Vous envoyez l’essentiel','You send the essentials')}</strong><span>{t('Trajet, logement, coordonnées : une minute.','Route, property, contact details: one minute.')}</span></li><li><strong>{t('Un conseiller vous rappelle','An adviser calls you back')}</strong><span>{reponse()}{t(', pour préciser le volume et les accès.',', to confirm volume and access.')}</span></li><li><strong>{t('Vous recevez votre devis','You receive your quote')}</strong><span>{t('Détaillé, gratuit et sans engagement, avec visite si besoin.','Detailed, free and with no obligation, with a visit if needed.')}</span></li></ol>{faits_band('stacked',sans=('Équipe FR · PT · ES · EN',))}{quote_proof()}<a class="express-call" href="{PHONE_HREF}" data-zone="devis-aside"><span>{t('Vous souhaitez parler à un conseiller CODEM ?<br>Contactez-nous au :','Would you like to speak to a CODEM adviser?<br>Call us on:')}</span><strong>{PHONE}</strong><small class="nosurtax">{t('Appel non surtaxé','Standard call rate')}</small></a></aside>'''
 return f'''<section class="express-page" data-express-page><div class="wrap express-grid">{form}{aside}</div><div class="wrap express-switch"><p>{t('Vous préférez tout détailler maintenant (accès, volume, photos) ?','Prefer to give every detail now (access, volume, photos)?')}</p><a class="btn outline" href="?detail=1" data-open-detail>{t('Demande détaillée en 9 étapes','Detailed request in 9 steps')}</a></div></section>'''

def valeur_box():
 return f'''<section class="section band-sand valeur-band"><div class="wrap valeur-box"><div>{eyebrow('Vos biens protégés','Your belongings protected')}<h2>{t('La déclaration de valeur,<br><em>simplement.</em>','The declaration of value,<br><em>made simple.</em>')}</h2></div><div><p>{t('Avant le déménagement, vous remplissez une déclaration de valeur : vous y indiquez la valeur totale de votre mobilier et vous listez à part vos objets de valeur. Elle fixe le montant maximal d’indemnisation en cas de dommage.','Before the move, you complete a declaration of value: you state the total value of your belongings and list valuable items separately. It sets the maximum compensation in case of damage.')}</p><ul class="check-list light-list"><li>{t('Votre conseiller CODEM vous aide à la remplir','Your CODEM adviser helps you complete it')}</li><li>{t('Pensez aux tableaux, bijoux, instruments et objets anciens','Remember paintings, jewellery, instruments and antiques')}</li><li>{t('Elle est jointe au contrat de déménagement','It is attached to the moving contract')}</li></ul>{link('devis',t('Recevoir mon devis gratuit','Get my free quote'),'btn btn-cta')}</div></div></section>'''
