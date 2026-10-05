from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
root=Path(__file__).parent/'dist';errors=[];count=0
class Check(HTMLParser):
 def __init__(self,path):super().__init__();self.path=path;self.ids=set();self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:
   if a['id'] in self.ids:errors.append(f'Duplicate id {self.path}: {a["id"]}')
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='img' and not a.get('alt'):errors.append(f'Alt missing: {self.path}')
  for attr in ['href','src','poster','data-src']:
   ref=a.get(attr,'')
   if ref.startswith('/'):
    target=root/ref.lstrip('/').split('#')[0]
    if ref.endswith('/'):target=target/'index.html'
    if not target.exists():errors.append(f'Missing {ref} from {self.path}')
for p in root.rglob('*.html'):
 c=Check(p);c.feed(p.read_text());count+=1
 if c.h1!=1:errors.append(f'H1 count {p}: {c.h1}')
for p in root.rglob('*'):
 if p.is_file() and p.stat().st_size>25*1024*1024:errors.append(f'Large asset: {p}')
print(f'{count} HTML pages checked; {len(errors)} errors.');print('\n'.join(errors))
raise SystemExit(bool(errors))
