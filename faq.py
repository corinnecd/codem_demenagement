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
 k,anchor,lab=OVERRIDE.get(i,CTA[theme])
 return f'''<article class="qcard {cls}" data-theme="{theme}"><button type="button" class="qcard-btn" aria-expanded="false" aria-controls="qa-{i}" data-q="{i}"><span class="qtag qtag-{theme}">{t(*THEMES[theme])}</span><span class="qcard-q">{q}</span><span class="qcard-plus" aria-hidden="true"></span></button><div class="qcard-a" id="qa-{i}" hidden><p>{a}</p><a class="text-link" href="{url(k)}{anchor}">{t(*lab)}</a></div></article>'''

def featured(photo):
 i=FEATURED;theme=META[i];q,a=b.FAQ_DATA()[i];k,anchor,lab=CTA[theme]
 return f'''<article class="qfeature" data-theme="{theme}"><div class="qfeature-img">{img(photo,t('Déménageurs CODEM au travail','CODEM movers at work'))}</div><div class="qfeature-body"><span class="qtag qtag-light">{t('La question du moment','Question of the moment')}</span><h3>{q}</h3><p>{a}</p><a class="btn btn-cta" href="{url('devis')}">{t('Recevoir mon devis gratuit','Get my free quote')}</a></div></article>'''

def section(pick=None,filters=False,photo='particulier-immeuble',band='band-glacier',more=True,sid='questions'):
 its=[x for x in items() if x[0]!=FEATURED and (pick is None or x[0] in pick)]
 if pick: its.sort(key=lambda x:pick.index(x[0]))
 chips=''
 if filters:
  used=[th for th in THEMES if any(x[1]==th for x in its)]
  chips='<div class="qfilters" role="group" aria-label="'+t('Filtrer par thème','Filter by topic')+'"><button type="button" class="qchip on" data-filter="all" aria-pressed="true">'+t('Toutes','All')+'</button>'+''.join(f'<button type="button" class="qchip" data-filter="{th}" aria-pressed="false">{t(*THEMES[th])}</button>' for th in used)+'</div>'
 cards=''.join(card(*x) for x in its)
 link_more=f'<div class="qmore"><a class="btn outline" href="{url("conseils")}#questions">{t("Toutes les questions","All questions")}</a><a class="text-link" href="{url("contact")}#rappel">{t("Une autre question ? Un conseiller vous rappelle.","Another question? An adviser will call you back.")}</a></div>' if more else f'<div class="qmore"><a class="text-link" href="{url("contact")}#rappel">{t("Une autre question ? Un conseiller vous rappelle.","Another question? An adviser will call you back.")}</a></div>'
 return f'''<section class="section {band} qsection" id="{sid}"><div class="wrap"><div class="section-heading"><div>{eyebrow('Vos questions','Your questions')}<h2>{t('Avant de faire vos cartons,<br><em>les bonnes réponses.</em>','Before you start packing,<br><em>the right answers.</em>')}</h2></div></div>{featured(photo)}{chips}<div class="qgrid">{cards}</div>{link_more}</div></section>'''

def jsonld():
 data={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in b.FAQ_DATA()]}
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
