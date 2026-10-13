"""Génère sitemap.xml et robots.txt à partir des routes du site."""
import build as b
def write():
 skip={'realisations'}  # pages sans contenu réel : non indexées pour l'instant
 rows=[]
 for k in b.routes:
  if k in skip:continue
  fr,en=b.SITE_URL+b.url(k,'fr'),b.SITE_URL+b.url(k,'en')
  alt=f'<xhtml:link rel="alternate" hreflang="fr" href="{fr}"/><xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
  pr='1.0' if k=='home' else '0.9' if k=='devis' else '0.8' if k in ('particuliers','entreprises','europe','stockage','monte','piano') else '0.5'
  for loc in (fr,en):rows.append(f'<url><loc>{loc}</loc>{alt}<priority>{pr}</priority></url>')
 (b.OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join(rows)+'</urlset>\n')
 (b.OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {b.SITE_URL}/sitemap.xml\n')
