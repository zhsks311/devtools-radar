import json,re,unittest
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1];SLUG='supabase-vs-firebase'
class RealtimeCostTests(unittest.TestCase):
 def test_delivery_math(self):
  messages=50*100*20*60*24*30
  self.assertEqual(messages,4320000000)
  packages=(max(0,messages-5000000)+999999)//1000000
  self.assertEqual(D(packages)*D('2.50'),D('10787.50'))
  self.assertEqual(D(packages)*D('2.50')+25,D('10812.50'))
  self.assertEqual(D(messages)/100000*D('.03'),D(1296))
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for x in (a,b):
   t=json.dumps(x,ensure_ascii=False)
   for bad in ['Nothing in that stream','bill stops tracking the watching','and a flat $25','Supabase wins: that dashboard']:self.assertNotIn(bad,t)
   for good in ['$10,787.50','$10,812.50','2,500','1,666.7','spend cap']:self.assertIn(good,t)
 def test_structured_faq(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());h=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S) if json.loads(s).get('@type')=='FAQPage')
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
  self.assertNotIn('Supabase wins: that dashboard',(ROOT/'content/polish.py').read_text())
