"""Éventail de photos de chantiers (inspiré du « card fan carousel »), en HTML + JS léger, sans dépendance."""
import build as b
from build import t,url,img,eyebrow,link

def cartes():
 """Une seule carte par catégorie de chantier : la photo la plus représentative."""
 from realisations import CAS
 out=[(c['photos'][0],c,i) for i,c in enumerate(CAS)]
 # 7e carte : votre projet, pour que l'éventail montre 7 cartes distinctes
 out.insert(len(out)//2+1,('ancien-22',{'tag':('Votre projet','Your move'),'lieu':('Le prochain chantier ?','Our next job?'),'devis':True},-1))
 return out

def fan(titre=True,cls='band-ivory'):
 cards=''
 for n,(p,c,i) in enumerate(cartes()):
  alt=t(*c['tag'])+' · '+t(*c['lieu'])
  im=img(p,alt).replace('<img ','<img draggable="false" ').replace('sizes="(max-width:640px) 90vw, 50vw"','sizes="(max-width:640px) 62vw, 290px"')
  href=url('devis') if c.get('devis') else f'{url("realisations")}#cas-{i+1}'
  cards+=(f'<a class="fan-card" href="{href}" data-i="{n}" tabindex="-1">'
   +im+
   f'<span class="fan-cap"><small>{t(*c["tag"])}</small>{t(*c["lieu"])}</span></a>')
 head=(f'<div class="fan-head">{eyebrow("Nos réalisations","Our work")}<h2>{t("Nos chantiers,<br><em>photographiés par nos équipes.</em>","Our jobs,<br><em>photographed by our teams.</em>")}</h2>'
  f'<p class="lead">{t("Monte-meubles en façade, maisons, objets d’art, musée : de vraies photos de nos équipes au travail.","Furniture lifts, houses, artwork, a museum: real photos of our crews at work.")}</p></div>') if titre else ''
 return (f'<section class="section {cls} fan-section">{"<div class=wrap>"+head+"</div>" if head else ""}'
  f'<div class="fan" data-fan role="region" aria-roledescription="carrousel" aria-label="{t("Photos de nos chantiers","Photos of our jobs")}">'
  f'<div class="fan-stage">{cards}</div>'
  f'<div class="fan-nav"><button type="button" class="fan-arrow" data-dir="-1" aria-label="{t("Photo précédente","Previous photo")}"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg></button>'
  f'<div class="fan-dots" aria-hidden="true"></div>'
  f'<button type="button" class="fan-arrow" data-dir="1" aria-label="{t("Photo suivante","Next photo")}"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button></div>'
  f'<p class="fan-live sr-only" aria-live="polite"></p>'
  +(f'<p class="fan-more">{link("realisations",t("Voir toutes nos réalisations","See all our work"),"btn")}</p>' if titre else '')+
  '</div></section>')
