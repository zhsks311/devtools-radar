import json,unittest
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SLUG='vercel-vs-cloudflare-pages'
class WorkersCacheWebSocketEvidenceTests(unittest.TestCase):
 def test_cache_request_cpu_arithmetic(self):
  requests=D(50); hits=D('.8'); cpu_per=D(7)
  request_cost=(requests-D(10))*D('.30')
  cpu_cost=(requests*(1-hits)*cpu_per-D(30))*D('.02')
  self.assertEqual(request_cost,D(12));self.assertEqual(cpu_cost,D('.80'))
  self.assertEqual(D(5)+request_cost+cpu_cost,D('17.80'))
  self.assertEqual(D(100)/D(20),D(5))
 def test_canonical_data_and_rendered_copy(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  texts=[json.dumps(x,ensure_ascii=False) for x in (a,b)]
  texts += [(ROOT/'dist/compare'/SLUG/'index.html').read_text(),(ROOT/'dist/llms-full.txt').read_text()]
  for text in texts:
   for bad in ['messages bill nothing','recalculate both request count and CPU from actual executions']:
    self.assertNotIn(bad,text)
   for required in ['Workers Caching hits remain billed requests','20:1','Durable Objects','$17.80']:
    self.assertIn(required,text)
  self.assertIn('https://developers.cloudflare.com/durable-objects/platform/pricing/',a['sources'])
 def test_metadata_defaults_do_not_restore_claim(self):
  from content.merge import META
  tb=META[SLUG]['tool_b']
  self.assertNotIn('messages bill nothing',json.dumps(tb))
  self.assertIn('Workers Caching hits remain billed requests',json.dumps(tb))
