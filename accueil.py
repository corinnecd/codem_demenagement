"""Sections dynamiques de la page d'accueil : cartes, carrousels, frise, cartes à retourner, bande de photos."""
import build as b
from build import t,url,link,img,eyebrow

def _ctrl(n,lab):
 return f'<div class="car-ctrl"><span class="car-count" aria-live="polite"><b data-cur>01</b> / {str(n).zfill(2)}</span><button class="car-arrow" type="button" data-prev aria-label="{t(lab[0],lab[1])} {t("précédent","previous")}">←</button><button class="car-arrow" type="button" data-next aria-label="{t(lab[0],lab[1])} {t("suivant","next")}">→</button></div>'

# 1. L'approche CODEM : une phrase + 4 cartes photo
def approche():
 data=[('agence-codem','Une agence de proximité','A local office','À Nogent-sur-Marne, un conseiller suit votre projet du devis au jour J.','In Nogent-sur-Marne, one adviser follows your move from quote to moving day.'),
  ('particulier-housse','Des biens protégés','Belongings protected','Housses, couvertures et emballages adaptés à chaque objet.','Covers, blankets and packing matched to each item.'),
  ('equipe','Des moyens adaptés','The right equipment','Véhicules capitonnés, monte-meubles et équipe dimensionnée selon le volume.','Padded vehicles, furniture lift and a team sized to your volume.'),
  ('particulier-fauteuil','Une installation soignée','Careful set-up','Remontage et mise en place du mobilier selon la formule choisie.','Reassembly and furniture placement depending on your package.')]
 cards=''.join(f'<article class="ap-card reveal" style="--d:{i*90}ms"><div class="ap-img">{img(im,t(a,c))}</div><div class="ap-body"><span class="ap-num">0{i+1}</span><h3>{t(a,c)}</h3><p>{t(d,e)}</p></div></article>' for i,(im,a,c,d,e) in enumerate(data))
 return f'<section class="section band-ivory ap-section" id="approche"><div class="wrap"><div class="ap-head reveal"><div>{eyebrow("L’approche CODEM","The CODEM approach")}<h2>{t("Vous imaginez la suite.<br><em>Nous préparons le départ.</em>","You imagine what’s next.<br><em>We prepare the move.</em>")}</h2></div><p class="lead">{t("Déménageurs à Nogent-sur-Marne, nous accompagnons particuliers et entreprises en France et en Europe, du premier inventaire à la remise en place.","Movers based in Nogent-sur-Marne, we support households and businesses across France and Europe, from first inventory to final set-up.")}</p></div><div class="ap-grid">{cards}</div></div></section>'

# 2. Carrousel des savoir-faire (cartes qui s'ouvrent)
SERVICES=[('particuliers','particulier-canape','Appartement, maison ou succession : nous organisons tout, du premier carton à la remise en place.','Flat, house or estate: we organise everything, from the first box to final set-up.'),
 ('entreprises','entreprise-chargement','Bureaux, archives et parc informatique transférés sans interrompre votre activité.','Offices, records and IT equipment moved without interrupting your business.'),
 ('europe','camion-campagne','Départs réguliers vers le Portugal, l’Espagne et l’Italie, avec groupage possible.','Regular departures to Portugal, Spain and Italy, with shared loads available.'),
 ('piano','ancien-28','Statuettes, tableaux, pianos et mobilier ancien emballés sur mesure.','Statuettes, paintings, pianos and antique furniture custom-packed.'),
 ('stockage','garde-meubles-box','Box sécurisés, à l’abri de la poussière et de l’humidité, pour la durée qu’il vous faut.','Secure units, protected from dust and damp, for as long as you need.'),
 ('monte','ancien-21','Par la fenêtre quand l’escalier ne suffit pas, avec un technicien aux commandes.','Through the window when the stairs are not enough, with an operator at the controls.'),
 ('cartons','particulier-emballage','Cartons, penderies, housses et papier bulle pour emballer vous-même.','Boxes, wardrobe boxes, covers and bubble wrap to pack yourself.')]
def services():
 n=len(SERVICES)
 cards=''.join(f'<article class="svc-card{" on" if i==0 else ""}"><div class="svc-ph">{img(im,b.label(k))}<span class="svc-num">{str(i+1).zfill(2)}</span></div><div class="svc-body"><h3>{b.label(k)}</h3><div class="svc-more"><div><p>{t(fr,en)}</p><a class="svc-go" href="{url(k)}">{t("Découvrir","Discover")} <span aria-hidden="true">→</span></a></div></div></div></article>' for i,(k,im,fr,en) in enumerate(SERVICES))
 return f'<section class="section band-sand car svc-car" id="approche" data-carousel data-expand data-autoplay="6000" aria-roledescription="{t("carrousel","carousel")}" aria-label="{t("Nos savoir-faire","Our expertise")}"><div class="wrap car-head"><div>{eyebrow("Nos savoir-faire","Our expertise")}<h2>{t("Chaque projet est singulier.<br><em>Notre attention reste la même.</em>","Every move is different.<br><em>Our care stays the same.</em>")}</h2></div>{_ctrl(n,("Service","Service"))}</div><div class="car-track" data-track tabindex="0">{cards}</div><div class="wrap"><div class="car-progress" data-progress></div><div class="car-foot">{link("devis",t("Recevoir mon devis gratuit","Get my free quote"),"btn btn-cta")}<span class="car-hint">{t("Glissez, cliquez sur les flèches ou laissez défiler.","Swipe, use the arrows or let it play.")}</span></div></div></section>'

# 3. Frise : 4 étapes reliées par une ligne qui se remplit au défilement
def frise():
 data=[('Votre projet','Your move','Vous décrivez votre besoin, votre trajet et la période envisagée.','Tell us about your needs, your route and preferred dates.','1 minute en ligne','1 minute online'),
  ('L’étude & le devis','Assessment & quote','Un conseiller vous rappelle, examine le volume et les accès, puis établit une proposition.','An adviser calls you back, assesses volume and access, then sends a proposal.','Rappel sous 24 h ouvrées','Call back within 1 working day'),
  ('La préparation','Preparation','Emballages, protections et moyens de manutention sont précisés.','Packing, protection and handling equipment are agreed.','Visite à domicile ou en vidéo','Home or video survey'),
  ('Le jour du départ','Moving day','Les prestations convenues sont coordonnées jusqu’à la remise en place.','Your agreed services are coordinated through to final set-up.','À la date convenue','On the agreed date')]
 steps=''.join(f'<li class="fr-step"><span class="fr-dot" aria-hidden="true">{i+1}</span><div class="fr-card"><span class="step-chip">{t(e,f)}</span><h3>{t(a,c)}</h3><p>{t(d,g)}</p></div></li>' for i,(a,c,d,g,e,f) in enumerate(data))
 return f'<section class="section band-glacier frise" data-frise><div class="wrap">{eyebrow("Un déménagement bien préparé","A well-prepared move")}<h2>{t("Un chemin clair.<br><em>Du premier échange à l’arrivée.</em>","A clear path.<br><em>From our first conversation to arrival.</em>")}</h2><div class="fr-wrap"><div class="fr-line" aria-hidden="true"><i></i></div><ol class="fr-list">{steps}</ol></div><div class="actions inset">{link("devis",t("Préparer ma demande","Start my request"),"btn btn-cta")}</div></div></section>'

# 4. Protection : 3 cartes à retourner
def protection():
 data=[('ancien-10','Le mobilier','Furniture','Couvertures, sangles et démontage si besoin : les meubles voyagent enveloppés, sans frottement.','Blankets, straps and dismantling if needed: furniture travels wrapped, with no rubbing.'),
  ('particulier-tableau','Tableaux & miroirs','Paintings & mirrors','Papier bulle, coins de protection et caisses adaptées pour les cadres et les surfaces vitrées.','Bubble wrap, corner guards and suitable crates for frames and glass.'),
  ('piano','Pianos & pièces lourdes','Pianos & heavy items','Matériel de manutention, sanglage et accès étudiés avant l’intervention.','Handling equipment, strapping and access assessed before the job.')]
 cards=''.join(f'<li><button type="button" class="flip" aria-pressed="false"><span class="flip-in"><span class="flip-front">{img(im,t(a,c))}<span class="flip-title">{t(a,c)}<small>{t("Voir comment nous protégeons","See how we protect it")} ↻</small></span></span><span class="flip-back"><span class="flip-k">{t(a,c)}</span><span class="flip-txt">{t(d,e)}</span><small>↻ {t("Revenir à la photo","Back to the photo")}</small></span></span></button></li>' for im,a,c,d,e in data)
 return f'<section class="section band-ivory prot"><div class="wrap"><div class="ap-head reveal"><div>{eyebrow("La protection de vos biens","Protecting your belongings")}<h2>{t("Le soin commence<br><em>avant le transport.</em>","Care begins<br><em>before the journey.</em>")}</h2></div><p class="lead">{t("Chaque objet a sa protection. Retournez les cartes pour voir comment nous préparons vos biens.","Every item gets its own protection. Flip the cards to see how we prepare your belongings.")}</p></div><ul class="flip-grid">{cards}</ul><p class="prot-link">{link("piano",t("Confier un objet particulier","Arrange care for a specialist item"),"text-link")}</p></div></section>'

# 5. Bande de photos réelles qui défile
TERRAIN=['chantier-camion','ancien-02','ancien-19','ancien-26','ancien-16','ancien-29','ancien-22','ancien-12','ancien-33','ancien-20','ancien-25','ancien-06']
def terrain():
 alt=t('Chantier CODEM','CODEM job')
 row=''.join(f'<li><a href="{url("realisations")}">{img(p,alt)}</a></li>' for p in TERRAIN);row2=row.replace('<a ','<a tabindex="-1" ')
 return f'<section class="section band-ivory terrain"><div class="wrap ap-head reveal"><div>{eyebrow("CODEM, sur le terrain","CODEM in the field")}<h2>{t("Des chantiers réels.<br><em>Photographiés par nos équipes.</em>","Real jobs.<br><em>Photographed by our teams.</em>")}</h2></div><div>{link("realisations",t("Voir nos réalisations","See our case studies"),"btn outline")}</div></div><div class="marquee" data-marquee><ul class="mq-row">{row}</ul><ul class="mq-row" aria-hidden="true">{row2}</ul></div></section>'

# 6. Carrousel des destinations (villes et trajets)
def terrain_strip():
 """Bande de photos réelles intégrée sous les avis (preuve visuelle)."""
 alt=t('Chantier CODEM','CODEM job')
 row=''.join(f'<li><a href="{url("realisations")}">{img(p,alt)}</a></li>' for p in TERRAIN);row2=row.replace('<a ','<a tabindex="-1" ')
 return f'<div class="terrain-strip"><p class="ts-label wrap">{t("Nos chantiers, photographiés par nos équipes","Our jobs, photographed by our teams")} · {link("realisations",t("Voir nos réalisations","See our case studies"),"text-link")}</p><div class="marquee" data-marquee><ul class="mq-row">{row}</ul><ul class="mq-row" aria-hidden="true">{row2}</ul></div></div>'
def destinations():
 import villes as v
 cards=''
 order=['paris','nogent','vincennes','saintmande','saintmaur','fontenay','perreux','champigny']
 for k in order:
  d=v.VILLES[k];cp=d['cp'] if d['cp']!='75' else 'Paris'
  cards+=f'<a class="dest-card" href="{url("zones")}#{k}"><span class="dest-k">{cp}</span><span class="dest-name">{d["nom"]}</span><span class="dest-txt">{t(*d["lead"]).split(". ")[0].rstrip(".")}.</span><span class="dest-go">{t("Déménager ","Moving ")}{v._a(k)} →</span></a>'
 for k,d in v.TRAJETS.items():
  cards+=f'<a class="dest-card dest-intl" href="{url("t-"+k)}"><span class="dest-k">{t("International","International")}</span><span class="dest-name">Paris → {t(*d["nom"])}</span><span class="dest-txt">{t(*d["distance"])}</span><span class="dest-go">{t("Voir le trajet","See the route")} →</span></a>'
 n=len(order)+len(v.TRAJETS)
 return f'<section class="section band-sand car dest-car" data-carousel aria-roledescription="{t("carrousel","carousel")}" aria-label="{t("Nos destinations","Our destinations")}"><div class="wrap car-head"><div>{eyebrow("Zones desservies","Areas covered")}<h2>{t("Près de chez vous<br><em>ou à l’autre bout de l’Europe.</em>","Close to home<br><em>or across Europe.</em>")}</h2></div>{_ctrl(n,("Destination","Destination"))}</div><div class="car-track" data-track tabindex="0">{cards}</div><div class="wrap car-foot">{link("devis",t("Faire vérifier mon trajet","Check my route"),"btn btn-cta")}{link("zones",t("Toutes les zones desservies","All areas covered"),"text-link")}</div></section>'

# 3 bis. « Ce n'est pas seulement une question d'adresse » : photos qui changent au défilement
INTERIEURS=[('ancien-14','Des protections adaptées à vos biens','Protection suited to your belongings','Mobilier ancien, objets fragiles : chaque pièce est emballée selon sa nature.','Antique furniture, fragile items: each piece is packed according to its nature.'),
 ('ancien-24','Des accès étudiés avant le déménagement','Access assessed before moving day','Étages, escaliers, stationnement, monte-meubles : tout est vérifié en amont.','Floors, stairs, parking, furniture lift: everything is checked beforehand.'),
 ('ancien-03','Une organisation selon vos prestations','A plan built around your services','Véhicules, équipe et planning sont adaptés à votre volume et à votre formule.','Vehicles, team and schedule are matched to your volume and package.')]
def interieurs():
 pts=''.join(f'<li class="it-pt{" on" if i==0 else ""}" data-i="{i}"><span class="it-n">0{i+1}</span><div><strong>{t(a,c)}</strong><p>{t(d,e)}</p></div><div class="it-ph-m">{img(im,t(a,c))}</div></li>' for i,(im,a,c,d,e) in enumerate(INTERIEURS))
 ph=''.join(f'<figure class="it-ph{" on" if i==0 else ""}" data-i="{i}">{img(im,t(a,c))}</figure>' for i,(im,a,c,d,e) in enumerate(INTERIEURS))
 return f'<section class="interieurs dark" data-interieurs><div class="it-sticky"><div class="wrap it-grid"><div class="it-text">{eyebrow("Tous les intérieurs, la même attention","Every home, the same care")}<h2>{t("Ce n’est pas seulement<br><em>une question d’adresse.</em>","It’s about more<br><em>than an address.</em>")}</h2><p class="it-lead">{t("Un premier appartement, une maison de famille, un intérieur d’exception : le même soin pour les biens qui font votre vie.","A first flat, a family home, an exceptional interior: the same care for the belongings that make up your life.")}</p><ol class="it-pts">{pts}</ol><div class="it-bar" aria-hidden="true"><i></i></div>{link("particuliers",t("Découvrir notre accompagnement","Discover how we help"),"btn light")}</div><div class="it-stage" aria-hidden="true">{ph}</div></div></div></section>'
