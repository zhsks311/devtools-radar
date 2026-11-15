import json,re,unittest
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1];SLUG='aws-lambda-vs-cloudflare-workers'
def costs(r):
 r=D(r); lam=max(D(0),r-D(1000000))*D('.20')/D(1000000)+max(D(0),r*D('.1')-D(400000))*D('.0000133334')
 worker=D(5)+max(D(0),r-D(10000000))*D('.30')/D(1000000)+max(D(0),r*D(10)-D(30000000))*D('.02')/D(1000000)
 return lam,worker
class LambdaConclusionTests(unittest.TestCase):
 def test_table_and_crossover(self):
  for n,l,w in [(5000000,'2.13','5.40'),(7500000,'5.97','5.90'),(10000000,'9.80','6.40'),(50000000,'71.13','26.40'),(100000000,'147.80','51.40')]:
   a,b=costs(n);self.assertEqual(a.quantize(D('.01')),D(l));self.assertEqual(b.quantize(D('.01')),D(w))
  self.assertLess(*costs(7440000));self.assertGreater(*costs(7460000));self.assertEqual(costs(0),(D(0),D(5)))
 def test_no_unqualified_claim_in_exports_and_metadata(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  texts=[json.dumps(a),json.dumps(b),*( (ROOT/p).read_text() for p in ['dist/llms.txt','dist/llms-full.txt',f'dist/compare/{SLUG}/index.html'])]
  for t in texts:
   self.assertNotIn('Workers is two to three times cheaper',t);self.assertNotIn('Nothing about the code differs',t);self.assertNotIn('cover the whole job',t)
   self.assertIn('$2.13',t);self.assertIn('$5.40',t)
  h=(ROOT/f'dist/compare/{SLUG}/index.html').read_text()
  objs=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S)]
  faq=next(o for o in objs if o.get('@type')=='FAQPage')
  self.assertEqual(faq['mainEntity'][-1]['acceptedAnswer']['text'],a['faqs'][-1]['a'])
 def test_generator_preserves_scoped_conclusion(self):
  from content.killer5_b import WORKERS
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());self.assertEqual(WORKERS,a)
