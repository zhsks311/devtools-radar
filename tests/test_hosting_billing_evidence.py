import json,re,unittest
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1];SLUG='vercel-vs-cloudflare-pages'
class HostingEvidenceTests(unittest.TestCase):
 def test_conditions_and_math(self):
  self.assertEqual(D(5)+D(40)*D('.30')+D(320)*D('.02'),D('23.40'))
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for x in (a,b):
   t=json.dumps(x,ensure_ascii=False)
   for bad in ['$307.20','Queue consumer invocations allow 15 minutes','Vercel lists a 5-minute function duration','10M CDN requests, every GB']:self.assertNotIn(bad,t)
   for good in ['1,800','Flat Rate CDN','1M CDN','wall-clock','$23.40']:self.assertIn(good,t)
 def test_faq_and_source(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());h=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S) if json.loads(s).get('@type')=='FAQPage')
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
  self.assertNotIn('$307.20',(ROOT/'content/polish.py').read_text())
  self.assertNotIn('$307.20',(ROOT/'content/merge.py').read_text())
