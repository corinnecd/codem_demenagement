"""Blocs de conversion : faits de confiance, avis Google, devis express."""
import build as b
from build import t,url,link,img,eyebrow,PHONE,PHONE_HREF

# Engagement de délai affiché près des boutons, à confirmer par CODEM
REPONSE=('Réponse sous 24 h ouvrées','Reply within 1 working day')
def reponse():return t(*REPONSE)

# ---------------------------------------------------------------------------
# 1. Faits VRAIS, visibles par tous
FAITS=[('Note Google 4,9/5 · 65 avis','Google rating 4.9/5 · 65 reviews'),('Agence à Nogent-sur-Marne','Office in Nogent-sur-Marne'),
 ('Devis gratuit et sans engagement','Free quote, no obligation'),
 REPONSE,
 ('5 formules, de Self à Grand Confort','5 packages, from Self to Grand Confort')]
def faits_band(cls='',sans=()):
 return f'<ul class="facts-band {cls}" aria-label="{t("Pourquoi CODEM","Why CODEM")}">'+''.join(f'<li><span class="fact-dot" aria-hidden="true"></span>{t(a,c)}</li>' for a,c in FAITS if a not in sans)+'</ul>'

STARS='<span class="stars" aria-hidden="true">★★★★★</span>'
# ---------------------------------------------------------------------------
# 2. Avis Google de CODEM (confirmés par CODEM) de CODEM (texte d'origine, non modifié ; relevés le 13/10/2026)
GOOGLE_COUNT=65
GOOGLE_NOTE=('4,9','4.9')
GOOGLE_URL='https://www.google.com/maps/search/?api=1&query=CODEM+D%C3%A9m%C3%A9nagements+39+boulevard+de+Strasbourg+Nogent-sur-Marne'
AVIS_GOOGLE=[
 ('Benjamin Benhamo','août 2026','August 2026','Excellente expérience avec cette équipe de déménageurs ! Ils ont été ponctuels, rapides, efficaces et très soigneux avec nos meubles et nos cartons. Toute l’équipe était également très sympathique, professionnelle et agréable tout au long du déménagement. Tout s’est déroulé dans de très bonnes conditions, sans stress et avec beaucoup de sérieux. Nous sommes vraiment satisfaits de leur prestation et nous les recommandons sans hésiter !'),
 ('Sylvain A.','novembre 2025','November 2025','Déménagement de 35 m2 avec un passage par garde meuble pendant 2 mois : nous sommes très satisfaits, du devis jusqu’à la livraison de nos affaires. Amabilité, ponctualité, bonne protection, et ils ont réussi à s’arranger pour être dispo après un changement de date tardif de notre part. Au final un très bon rapport qualité / prix avec une équipe très pro.'),
 ('Hélène Olive','octobre 2025','October 2025','CODEM a réalisé notre déménagement et tout s’est très bien passé ! Ponctuels, précautionneux avec les affaires, nous sommes très satisfaits de la prestation, avec un prix très compétitif. Encore merci !'),
 ('LN Ako','septembre 2025','September 2025','Je vous recommande fortement cette entreprise de déménagements. Équipe au top, très professionnelle, rapide et efficace et prix très attractifs par rapport à la concurrence. Équipe vraiment sympathique et ponctuelle. Bravo !'),
 ('Marion Coudeyre','octobre 2025','October 2025','Nous avons été ravis de la prestation réalisée cette été, par une équipe efficace et sympathique. Quel plaisir de faire travailler une entreprise locale qui en plus a les meilleurs tarifs !'),
]
def google_cards(idx):
 lang='' if b.LANG=='fr' else ' lang="fr"'
 return ''.join(f'<figure class="review-card real-review"><blockquote{lang}>« {a[3]} »</blockquote><figcaption><strong>{a[0]}</strong><span>{t("Avis Google","Google review")} · {t(a[1],a[2])}</span></figcaption></figure>' for a in (AVIS_GOOGLE[i] for i in idx))
def google_note():
 return f'<p class="google-note"><span class="gn-score"><strong>{t(*GOOGLE_NOTE)}/5</strong>{STARS}</span><span class="gn-count">{t("Note Google","Google rating")} · {GOOGLE_COUNT} {t("avis clients","client reviews")}</span><a class="text-link" href="{GOOGLE_URL}" target="_blank" rel="noopener">{t("Voir tous les avis sur Google","See all reviews on Google")}</a></p>'+('' if b.LANG=='fr' else '<p class="fine-print">Reviews shown in their original French.</p>')
def home_reviews():
 return f'<section class="section band-ivory real-proofs"><div class="wrap"><div class="section-heading"><div>{eyebrow("Ils nous ont confié leur déménagement","They trusted us with their move")}<h2>{t("Ce que nos clients<br><em>disent de CODEM.</em>","What our clients<br><em>say about CODEM.</em>")}</h2></div></div>{google_note()}<div class="review-grid">{google_cards([0,1,2])}</div><div class="actions">{link("devis",t("Recevoir mon devis gratuit","Get my free quote"),"btn btn-cta")}{link("avis",t("Lire tous les avis","Read all reviews"),"text-link")}{link("realisations",t("Voir nos réalisations","See our case studies"),"text-link")}</div></div></section>'
def avis_page():
 from pages import crumb
 return crumb('avis')+f'<section class="page-title band-ivory"><div class="wrap">{eyebrow(*b.labels["avis"])}<h1>{t("Ils nous ont confié<br><em>leur déménagement.</em>","They trusted us<br><em>with their move.</em>")}</h1><p class="lead">{t("Des avis laissés par nos clients sur Google, reproduits tels quels avec le nom affiché par leur auteur et la date de publication.","Reviews left by our clients on Google, shown as written, with the name displayed by their author and the date of publication.")}</p>{google_note()}</div></section><section class="section band-sand"><div class="wrap"><div class="review-grid">{google_cards(range(len(AVIS_GOOGLE)))}</div></div></section>'+b.cta(t('Votre déménagement,<br><em>le prochain avis ?</em>','Your move,<br><em>the next review?</em>'))
def quote_proof():
 a=AVIS_GOOGLE[2];lg='' if b.LANG=='fr' else ' lang="fr"'
 return f'<div class="quote-proof real-review"><p class="qp-rating"><strong>{t(*GOOGLE_NOTE)}/5</strong>{STARS}<span>{GOOGLE_COUNT} {t("avis Google","Google reviews")}</span></p><blockquote{lg}>« {a[3]} »</blockquote><cite>{a[0]} · {t("Avis Google","Google review")}</cite></div>'

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
