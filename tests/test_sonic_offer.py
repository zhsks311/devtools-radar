import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
class SonicOffer(unittest.TestCase):
 def test_base_price_region_and_current_specs(self):
  k='sonic-racing-crossworlds-directgames'; d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],23500); self.assertTrue(checked_price(d)); self.assertIsNone(d['original_price']); self.assertIsNone(d['expires_at'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR'])
  self.assertEqual(d['price_review']['seller_displayed_comparison']['reference_price'],44800)
  for v in json.loads(Path('data/deal_localizations.json').read_text())[k].values():
   self.assertIn('20 GB',v['buying_note']); self.assertIn('AVX',v['buying_note']);self.assertNotIn('58 GB',v['buying_note'])
