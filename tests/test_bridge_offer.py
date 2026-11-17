import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link
class BridgeOffer(unittest.TestCase):
 def test_region_price_and_refund(self):
  k='bridge-constructor-studio-directgames';d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']==k)
  self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertEqual(d['price'],3100);self.assertIsNone(d['original_price']);self.assertIsNone(d['expires_at'])
  self.assertEqual(d['country_targeting']['countries'],['KR','JP','SG']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR','JP','SG'])
  for l,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn('Steam',v['conditions']);self.assertIn('23:59',v['conditions']);self.assertIn('7',v['buying_note'])
