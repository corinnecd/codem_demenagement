"""Page Réalisations : vrais chantiers CODEM, photos prises par les équipes (reprises du site d'origine).
Seules les photos réelles sont utilisées (pas de photos d'illustration ni d'images retouchées)."""
import build as b
from build import t,url,link,img,eyebrow,label

CAS=[
 dict(photos=['ancien-21','ancien-22','ancien-24','ancien-25'],tag=('Monte-meubles','Furniture lift'),lieu=('Immeubles parisiens','Paris apartment buildings'),
  titre=('Monter les meubles<br><em>par la façade.</em>','Lifting furniture<br><em>up the facade.</em>'),
  texte=('Quand l’escalier est trop étroit ou l’ascenseur trop petit, le monte-meubles passe par la fenêtre. Trottoir balisé, technicien aux commandes, meubles protégés avant la montée : les étages élevés ne posent plus de problème.','When the stairs are too narrow or the lift too small, the furniture lift goes through the window. Pavement marked off, an operator at the controls, furniture protected before lifting: upper floors are no longer a problem.'),
  points=[('Balisage du trottoir','Pavement marked off'),('Technicien qualifié','Qualified operator'),('Accès difficiles','Difficult access')],svc='monte'),
 dict(photos=['ancien-26'],tag=('Manutention spécialisée','Specialist handling'),lieu=('Musée océanographique de Monaco','Oceanographic Museum of Monaco'),
  titre=('Un socle à déplacer<br><em>au musée.</em>','A plinth to move<br><em>at the museum.</em>'),
  texte=('Manutention d’un socle au Musée océanographique de Monaco : une pièce lourde, dans un lieu patrimonial, déplacée avec méthode par une équipe dédiée.','Moving a plinth at the Oceanographic Museum of Monaco: a heavy piece, in a heritage building, moved methodically by a dedicated team.'),
  points=[('Pièce lourde','Heavy piece'),('Lieu patrimonial','Heritage site'),('Équipe dédiée','Dedicated team')],svc='piano'),
 dict(photos=['ancien-19','ancien-03','ancien-12'],tag=('Particuliers','Home moves'),lieu=('Maison avec extérieur','House with grounds'),
  titre=('Une maison entière,<br><em>chargée avec soin.</em>','A whole house,<br><em>loaded with care.</em>'),
  texte=('Poids lourd et utilitaire sur place, rampe de chargement, mobilier protégé et cartons préparés : pour une maison, l’équipe et les véhicules sont dimensionnés selon le volume.','A heavy truck and a van on site, a loading ramp, protected furniture and ready boxes: for a house, the team and vehicles are sized to the volume.'),
  points=[('Véhicules capitonnés','Padded vehicles'),('Rampe de chargement','Loading ramp'),('Équipe dimensionnée','Right-sized team')],svc='particuliers'),
 dict(photos=['ancien-16','ancien-02','ancien-20','ancien-06'],tag=('En ville','In town'),lieu=('Paris et Val-de-Marne','Paris and Val-de-Marne'),
  titre=('Déménager en ville,<br><em>au pied de l’immeuble.</em>','Moving in town,<br><em>right outside the building.</em>'),
  texte=('Camion stationné au plus près de l’entrée, hayon élévateur, chargement rapide pour libérer la voie : les déménagements en centre-ville se préparent jusqu’à l’emplacement du véhicule.','Truck parked as close to the entrance as possible, tail lift, quick loading to free the street: town-centre moves are planned right down to where the vehicle parks.'),
  points=[('Stationnement anticipé','Parking planned ahead'),('Hayon élévateur','Tail lift'),('Chargement rapide','Quick loading')],svc='zones'),
 dict(photos=['ancien-28','ancien-14','ancien-29','ancien-10'],tag=('Objets d’art et mobilier ancien','Artwork and antique furniture'),lieu=('Biens de valeur','Valuable belongings'),
  titre=('Objets d’art<br><em>et mobilier de valeur.</em>','Artwork<br><em>and valuable furniture.</em>'),
  texte=('Statuettes, céramiques et bronzes emballés un par un, chaises anciennes et tables de style manipulées pièce par pièce, meubles enveloppés de couvertures et sanglés : chaque objet est protégé avant de quitter la pièce.','Statuettes, ceramics and bronzes wrapped one by one, antique chairs and period tables handled piece by piece, furniture wrapped in blankets and strapped: every item is protected before it leaves the room.'),
  points=[('Emballage sur mesure','Custom packing'),('Manipulation pièce par pièce','Handled piece by piece'),('Couvertures et sanglage','Blankets and strapping')],svc='piano'),
 dict(photos=['ancien-33'],tag=('Garde-meubles','Storage'),lieu=('Stockage sécurisé','Secure storage'),
  titre=('Des meubles emballés<br><em>pour le stockage.</em>','Furniture packed<br><em>for storage.</em>'),
  texte=('Mobilier filmé et protégé, chargé en conteneur pour un stockage à l’abri de la poussière et de l’humidité, le temps d’un séjour à l’étranger ou de travaux.','Furniture wrapped and protected, loaded into a container for storage away from dust and damp, during a stay abroad or building work.'),
  points=[('Mobilier filmé','Furniture wrapped'),('Stockage en conteneur','Container storage'),('Courte ou longue durée','Short or long term')],svc='stockage'),
]

def _case(i,c):
 ph=c['photos'];alt=t(*c['tag'])+' · '+t(*c['lieu'])
 main=f'<div class="image-wrap rc-main">{img(ph[0],alt)}</div>'
 thumbs=''.join(f'<div class="image-wrap rc-thumb">{img(p,alt)}</div>' for p in ph[1:])
 media=f'<div class="rc-media{" solo" if len(ph)==1 else ""}">{main}'+(f'<div class="rc-thumbs n{len(ph)-1}">{thumbs}</div>' if thumbs else '')+'</div>'
 pts=''.join(f'<li>{t(a,c2)}</li>' for a,c2 in c['points'])
 body=f'<div class="rc-body"><span class="eyebrow">{str(i+1).zfill(2)} · {t(*c["tag"])}</span><p class="rc-place">{t(*c["lieu"])}</p><h2>{t(*c["titre"])}</h2><p>{t(*c["texte"])}</p><ul class="rc-points">{pts}</ul>{link(c["svc"],t("Voir le service","See the service"),"text-link")}</div>'
 return f'<article class="rcase{" rev" if i%2 else ""}">{media}{body}</article>'

def page():
 from pages import crumb
 body=crumb('realisations')+f'''<section class="page-title band-ivory"><div class="wrap">{eyebrow("Réalisations","Case studies")}<h1>{t("Nos chantiers,<br><em>en images.</em>","Our jobs,<br><em>in pictures.</em>")}</h1><p class="lead">{t("Monte-meubles en façade, maisons, centre-ville, objets d’art, musée : des déménagements réalisés par les équipes CODEM, photographiés sur place.","Furniture lifts, houses, town centres, artwork, a museum: moves carried out by CODEM teams, photographed on site.")}</p></div></section>
<section class="section band-sand rcases"><div class="wrap">{"".join(_case(i,c) for i,c in enumerate(CAS))}</div></section>'''+b.cta(t('Votre déménagement,<br><em>notre prochain chantier.</em>','Your move,<br><em>our next job.</em>'))
 desc=t('Réalisations CODEM Déménagements : monte-meubles en façade, maisons, centre-ville, objets d’art et mobilier ancien, manutention au Musée océanographique de Monaco. Photos de nos chantiers.','CODEM Moving case studies: furniture lifts, houses, town-centre moves, artwork and antique furniture, handling at the Oceanographic Museum of Monaco. Photos from our jobs.')
 return body,desc

def write_all():
 body,desc=page();b.write('realisations',body,desc)
