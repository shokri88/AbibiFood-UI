"""Check standalone pages and local references; standard library only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[1]/'dist'
errors=[]
class Check(HTMLParser):
 def __init__(self,file):super().__init__();self.file=file
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for key in ('href','src'):
   link=a.get(key,'');u=urlsplit(link)
   if not link or u.scheme or u.netloc or not u.path:continue
   target=(self.file.parent/unquote(u.path)).resolve()
   if not target.exists():errors.append(f'{self.file.name}: missing {link}')
  if tag=='html' and (a.get('lang')!='fa' or a.get('dir')!='rtl'):errors.append(f'{self.file.name}: missing Persian RTL')
for f in root.glob('*.html'):Check(f).feed(f.read_text())
assert not errors,'\n'.join(errors)
print(f'PASS: {len(list(root.glob("*.html")))} standalone HTML pages; all local href/src targets exist; Persian RTL metadata present.')
