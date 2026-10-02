from pathlib import Path
from html.parser import HTMLParser
import base64,struct,json
R=Path(__file__).resolve().parent
class Plan(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.images=[];self.tags={};self.parent_link=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags[tag]=self.tags.get(tag,0)+1
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a':self.parent_link=a.get('href');self.links.append(self.parent_link)
  if tag=='img':self.images.append((self.parent_link,a))
 def handle_endtag(self,tag):
  if tag=='a':self.parent_link=None
p=Plan();p.feed((R/'plan.html').read_text());assert p.tags.get('h1')==1;assert p.tags.get('script',0)==0;assert p.tags.get('button',0)==0;assert len(p.images)==18
for href in p.links:
 if href.startswith('#'):assert href[1:] in p.ids,href
 elif not href.startswith(('https://','http://')):assert (R/href.split('#')[0]).is_file(),href
for href,a in p.images:
 raw=base64.b64decode(a['src'].split(',',1)[1]);assert raw==(R/href).read_bytes(),href
 assert raw.startswith(b'\x89PNG\r\n\x1a\n'),href
 assert struct.unpack('>II',raw[16:24])==(1440,900),href
print(json.dumps({'image_sources_identical':18,'size':'1440x900','local_links':'pass','toc':'pass','scripts':0,'custom_buttons':0}))
