"""Cartes questions : FAQ visuelle, filtrable, avec action adaptée à chaque question."""
import json
import build as b
from build import t,url,img,eyebrow

THEMES={'devis':('Devis & prix','Quotes & prices'),'preparer':('Préparer','Getting ready'),'acces':('Accès & stationnement','Access & parking'),'international':('International','International'),'garde':('Garde-meubles','Storage'),'assurance':('Vos biens protégés','Protection')}
# Ordre identique à build.FAQ_DATA()
META=['devis','devis','devis','preparer','acces','preparer','preparer','garde','international','preparer','acces','assurance','preparer','international','devis','devis']
CTA={'devis':('devis','',('Recevoir mon devis gratuit','Get my free quote')),'preparer':('devis','',('Recevoir mon devis gratuit','Get my free quote')),'acces':('contact','#rappel',('Être rappelé par un conseiller','Request a callback')),'international':('europe','',('Déménager à l’étranger','Moving abroad')),'garde':('stockage','',('Découvrir le garde-meubles','Explore storage')),'assurance':('piano','',('Protéger mes objets de valeur','Protect valuable items'))}
FEATURED=9  # « Combien de temps à l’avance faut-il réserver ? »

def items():
 return [(i,META[i],q,a) for i,(q,a) in enumerate(b.FAQ_DATA())]

OVERRIDE={3:('conseils','#volume',('Calculer mon volume pièce par pièce','Calculate my volume room by room'))}
def card(i,theme,q,a,cls=''):
 k,anchor,lab=OVERRIDE.get(i,CTA[theme]);qq=q.replace(' ?','\u00a0?')
 return f'''<article class="qcard {cls}" data-theme="{theme}"><button type="button" class="qcard-btn" aria-expanded="false" aria-controls="qa-{i}" data-q="{i}"><span class="qtag qtag-{theme}">{t(*THEMES[theme])}</span><span class="qcard-q">{qq}</span><span class="qcard-plus" aria-hidden="true"></span></button><div class="qcard-a" id="qa-{i}" hidden><p>{a}</p>{deeplink(i)}<a class="text-link" href="{url(k)}{anchor}">{t(*lab)}</a></div></article>'''

def featured(photo):
 i=FEATURED;theme=META[i];q,a=b.FAQ_DATA()[i];k,anchor,lab=CTA[theme]
 return f'''<article class="qfeature" data-theme="{theme}"><div class="qfeature-img">{img(photo,t('Déménageurs CODEM au travail','CODEM movers at work'))}</div><div class="qfeature-body"><span class="qtag qtag-light">{t('La question du moment','Question of the moment')}</span><h3>{q}</h3><p>{a}</p><div class="qf-cta"><a class="btn btn-cta" href="{url('devis')}">{t('Recevoir mon devis gratuit','Get my free quote')}</a>{b.mascot("montre-g","feat-mascot",150)}</div></div></article>'''

# Chaque réponse renvoie vers son article détaillé du guide (ou, à défaut, la page service)
ARTICLE={0:'devis',1:'devis',2:'devis',3:'volume',4:'stationnement',5:'vaisselle',6:'formule',8:'portugal',9:'checklist',10:'stationnement',11:'devis',12:'visite',13:'portugal',14:'mutation',15:'prix'}
SERVICE={7:('stockage',('Le garde-meubles CODEM','CODEM storage'))}
TOP=[15,9,3,4,11,12]
def deep(i):
 if i in ARTICLE:
  import guide;a=guide.BYKEY[ARTICLE[i]];return url('g-'+ARTICLE[i]),t(*a['title'])
 if i in SERVICE:k,lab=SERVICE[i];return url(k),t(*lab)
 return None
def deeplink(i,cls='qdeep'):
 d=deep(i)
 return f'<a class="{cls}" href="{d[0]}">{t("Pour aller plus loin","Read more")} : {d[1]} <span aria-hidden="true">→</span></a>' if d else ''

def helpcenter(sid='questions',band='band-glacier',title=None,eb=None):
 """Format « centre d’aide » : recherche + thèmes à gauche + questions en lignes à droite (une seule réponse ouverte)."""
 its=items()
 cnt=lambda th:sum(1 for x in its if x[1]==th)
 nav=f'<button type="button" class="hc-th on" data-hc="top" aria-pressed="true">{t("Les plus posées","Most asked")}<span>{len(TOP)}</span></button>'+''.join(f'<button type="button" class="hc-th" data-hc="{th}" aria-pressed="false">{t(*THEMES[th])}<span>{cnt(th)}</span></button>' for th in THEMES if cnt(th))
 rows=''
 for i,th,q,a in its:
  qq=q.replace(' ?','\u00a0?')
  top=f' data-top="{TOP.index(i)}"' if i in TOP else ''
  rows+=f'<div class="hc-row" data-theme="{th}"{top}><button type="button" class="hc-q" aria-expanded="false" aria-controls="hc-{i}"><span><small>{t(*THEMES[th])}</small>{qq}</span><span class="hc-plus" aria-hidden="true"></span></button><div class="hc-a" id="hc-{i}" hidden><p>{a}</p>{deeplink(i)}</div></div>'
 search=f'<div class="hc-search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><label class="sr-only" for="hc-input">{t("Rechercher une question","Search a question")}</label><input id="hc-input" type="search" autocomplete="off" placeholder="{t("Tapez votre question : stationnement, prix, volume…","Type your question: parking, price, volume…")}"></div>'
 cody=f'<div class="hc-cta">{b.mascot("tel","hc-mascot",96)}<p><strong>{t("Vous ne trouvez pas votre réponse ?","Can’t find your answer?")}</strong>{t("Un conseiller CODEM vous rappelle, sans engagement.","A CODEM adviser calls you back, no obligation.")}</p><a class="btn btn-cta" href="{url("contact")}#rappel">{t("Être rappelé","Call me back")}</a></div>'
 return f'''<section class="section {band} qsection hc" id="{sid}" data-help><div class="wrap"><div class="section-heading"><div>{eyebrow(*(eb or ('Vos questions','Your questions')))}<h2>{t(*(title or ('Avant de faire vos cartons,<br><em>les bonnes réponses.</em>','Before you start packing,<br><em>the right answers.</em>')))}</h2></div></div>{search}<div class="hc-grid"><nav class="hc-themes" aria-label="{t("Thèmes","Topics")}">{nav}</nav><div class="hc-list"><h3 class="hc-title" aria-live="polite">{t("Les questions les plus posées","Most asked questions")}</h3>{rows}<p class="hc-empty" hidden>{t("Aucune question trouvée. Un conseiller peut vous répondre.","No question found. An adviser can answer you.")}</p></div></div>{cody}</div></section>'''

def section(pick=None,filters=False,photo='particulier-immeuble',band='band-glacier',more=True,sid='questions',featured_on=True,title=None,eb=None):
 if filters:return helpcenter(sid,band,title,eb)
 its=[x for x in items() if (x[0]!=FEATURED or not featured_on) and (pick is None or x[0] in pick)]
 if pick: its.sort(key=lambda x:pick.index(x[0]))
 chips=''
 if filters:
  used=[th for th in THEMES if any(x[1]==th for x in its)]
  chips='<div class="qfilters" role="group" aria-label="'+t('Filtrer par thème','Filter by topic')+'"><button type="button" class="qchip on" data-filter="all" aria-pressed="true">'+t('Toutes','All')+'</button>'+''.join(f'<button type="button" class="qchip" data-filter="{th}" aria-pressed="false">{t(*THEMES[th])}</button>' for th in used)+'</div>'
 cards=''.join(card(*x) for x in its)
 link_more=f'<div class="qmore"><a class="btn outline" href="{url("conseils")}#questions">{t("Toutes les questions","All questions")}</a><a class="text-link" href="{url("contact")}#rappel">{t("Une autre question ? Un conseiller vous rappelle.","Another question? An adviser will call you back.")}</a></div>' if more else f'<div class="qmore"><a class="text-link" href="{url("contact")}#rappel">{t("Une autre question ? Un conseiller vous rappelle.","Another question? An adviser will call you back.")}</a></div>'
 return f'''<section class="section {band} qsection" id="{sid}"><div class="wrap"><div class="section-heading"><div>{eyebrow(*(eb or ('Vos questions','Your questions')))}<h2>{t(*(title or ('Avant de faire vos cartons,<br><em>les bonnes réponses.</em>','Before you start packing,<br><em>the right answers.</em>')))}</h2></div></div>{featured(photo) if featured_on else ''}{chips}<div class="qgrid">{cards}</div>{link_more}</div></section>'''

def jsonld():
 data={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in b.FAQ_DATA()]}
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
