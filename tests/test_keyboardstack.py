import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url
class KeyboardStackTest(unittest.TestCase):
 def test_product_page_and_terms(self):
  self.assertTrue(direct_product_url('https://keyboardstack.com/'))
  self.assertFalse(direct_product_url('https://keyboardstack.com/search?q=app'))
  root=Path(__file__).resolve().parents[1]
  d=next(x for x in json.loads((root/'data/deals_en.json').read_text())['feed'] if x['id']=='keyboardstack-premium')
  self.assertEqual(d['price'],14.99);self.assertIsNone(d['discount_pct']);self.assertFalse(d['link']['tracked']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  for loc in json.loads((root/'data/deal_localizations.json').read_text())[d['id']].values():
   self.assertIn('27',loc['conditions']);self.assertIn('Grid Mode',loc['conditions'])
