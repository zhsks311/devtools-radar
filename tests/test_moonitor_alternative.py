import json,unittest
from pathlib import Path
class MoonitorAlternativeTest(unittest.TestCase):
 def test_scope_and_primary_evidence(self):
  root=Path(__file__).resolve().parents[1]
  d=next(x for x in json.loads((root/'data/deals_en.json').read_text())['feed'] if x['id']=='moonitor-solo')
  self.assertFalse(d['link']['tracked']);self.assertEqual(d['price_review']['verified_price'],45.9)
  self.assertEqual(len(d['alternative_review']['sources']),3)
  loc=json.loads((root/'data/deal_localizations.json').read_text())['moonitor-solo']
  for lang in ['en','ko','zh','ja','es','fr']:
   for term in ['50','20','60','UptimeRobot','Moonitor']:self.assertIn(term,loc[lang]['buying_note'])
  self.assertIn('not tested',loc['en']['buying_note']);self.assertIn('paid',loc['en']['buying_note'])
