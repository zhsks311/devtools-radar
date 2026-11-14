import json,re,sys,unittest
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SLUG='aws-lambda-vs-cloudflare-workers'
class WorkersCpuTests(unittest.TestCase):
 def test_cpu_not_wall_time(self):
  def workers(cpu):return D(5)+max(D(0),D(10000000)*cpu-D(30000000))/D(1000000)*D('.02')
  self.assertEqual(workers(D(10)),D('6.40'))
  self.assertEqual(workers(D(200)),D('44.40'))
  self.assertEqual(((D(10000000)*D(1)*D('.5')-D(400000))*D('.0000133334')+D('1.8')).quantize(D('.01')),D('63.13'))
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  self.assertIn('10M × 10 ms',a['cost_math'][3]['formula']);self.assertIn('$6.40',a['cost_math'][3]['result']);self.assertNotIn('$44.40',a['cost_math'][3]['result'])
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  self.assertIn('Queue CPU up to 5 min, wall time 15 min',b['tool_b']['realtime'])
 def test_source_and_structured_faq(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text());sys.path.insert(0,str(ROOT/'content'));from killer5_b import WORKERS
  for k,v in a.items():self.assertEqual(WORKERS[k],v)
  self.assertIn('https://developers.cloudflare.com/queues/platform/limits/',a['sources'])
  html=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if json.loads(s).get('@type')=='FAQPage')
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
 def test_code_comment_billing_scope(self):
  sys.path.insert(0,str(ROOT/'content'))
  from killer5_b import WORKERS
  a=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for name in ['tool_a','tool_b']:self.assertEqual(a[name]['code_example'],WORKERS[name]['code_example'])
  self.assertIn('PLUS environment-lifetime memory',a['tool_a']['code_example'])
  self.assertNotIn('bill only the 10 ms',a['tool_a']['code_example'])
  self.assertIn('D1 separately meters rows read/written',a['tool_b']['code_example'])
  self.assertNotIn('waiting, not billed',a['tool_b']['code_example'])
  for p in ['dist/compare/'+SLUG+'/index.html','dist/llms-full.txt']:
   self.assertIn('does not make D1 free',(ROOT/p).read_text())
