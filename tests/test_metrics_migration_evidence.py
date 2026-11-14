import json,re,sys,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SLUG='datadog-vs-grafana-cloud'
class MetricsMigrationTests(unittest.TestCase):
 def test_pipeline_and_generator(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for x in (a,b):
   t=json.dumps(x,ensure_ascii=False)
   for bad in ['library pushes to a remote-write','can point at a remote write endpoint and stop','agent can also forward','migration pays for itself in a quarter']:self.assertNotIn(bad,t)
   for good in ['prometheus.scrape','prometheus.remote_write','authentication','duplicates','November 10']:self.assertIn(good,t)
  sys.path.insert(0,str(ROOT/'content'));from killer5_b import DATADOG
  for k,v in a.items():self.assertEqual(DATADOG[k],v)
 def test_structured_faq(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  html=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if json.loads(s).get('@type')=='FAQPage')
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
