import json,unittest
from pathlib import Path
class BuhoAlternatives(unittest.TestCase):
 def test_trial_and_fork_are_not_price_refresh(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='buhobarx-single-lifetime')
  self.assertEqual(d['price'],7.99);self.assertTrue(d['price_review']['review_completed_at'].startswith('2026-11-16T16:33:15'))
  self.assertIn('https://github.com/jordanbaird/Ice',[x['url'] for x in d['alternative_review']['sources']])
  for v in json.loads(Path('data/deal_localizations.json').read_text())[d['id']].values():
   for s in ('7','Ice','14','27','Sh7ne'):self.assertIn(s,v['buying_note'])
