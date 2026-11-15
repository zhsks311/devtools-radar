import json,unittest
from pathlib import Path
class SwitchPriceTest(unittest.TestCase):
 def test_public_and_member_prices_are_separate(self):
  root=Path(__file__).resolve().parents[1]
  d=next(x for x in json.loads((root/'data/deals_en.json').read_text())['feed'] if x['id']=='43ca41d03daa');r=d['price_review']
  self.assertEqual(d['price'],719);self.assertEqual(r['verified_price'],719)
  self.assertEqual(r['member_offer']['price'],678);self.assertTrue(r['member_offer']['requires_paid_membership']);self.assertFalse(r['member_offer']['checkout_verified'])
  self.assertEqual(r['previous_observation']['price'],728)
  for loc in json.loads((root/'data/deal_localizations.json').read_text())[d['id']].values():
   self.assertIn('678',loc['conditions']);self.assertIn('PLUS',loc['conditions']);self.assertNotIn('698',loc['conditions'])
