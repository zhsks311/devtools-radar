import json,re,sys,unittest
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SLUG='resend-vs-sendgrid'
class EmailBillingEvidenceTests(unittest.TestCase):
 def test_bucket_boundaries_and_claims(self):
  # Use integer ceiling before decimal currency arithmetic.
  def bill(n):return Decimal(20)+Decimal((max(0,n-50000)+999)//1000)*Decimal('.90')
  for n,expected in [(50000,'20'),(50003,'20.90'),(51415,'21.80'),(66000,'34.40'),(66001,'35.30')]:self.assertEqual(bill(n),Decimal(expected))
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for item in (a,b):
   t=json.dumps(item,ensure_ascii=False)
   for bad in ['account converts to a paid plan','account moves to a paid plan','then $19.95','equals $35 at 16,666']:self.assertNotIn(bad,t)
   for good in ['66,001','Transactional Overages','Partner/reseller','sending stops','$21.80']:self.assertIn(good,t)
 def test_faq_and_generator_match(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  sys.path.insert(0,str(ROOT/'content'))
  from killer5_c import RESEND
  for k,v in a.items():self.assertEqual(RESEND[k],v)
  html=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if json.loads(s).get('@type')=='FAQPage')
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
