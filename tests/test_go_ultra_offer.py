import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class GoUltraTests(unittest.TestCase):
 def test_exact_bundle_price_and_destination(self):
  d=next(x for x in json.loads((R/'data/deals.json').read_text())['feed'] if x['id']=='insta360-go-ultra-kr-standard-black')
  self.assertEqual(d['price'],523000);self.assertEqual(d['currency'],'KRW');self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR']);self.assertIn('no SD card',d['price_variant'])
  self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertIsNone(d['expires_at']);self.assertFalse(d['link']['tracked']);self.assertIn('/KR/product/go-ultra',d['link']['url']);self.assertEqual(d['image']['kind'],'official_product_photo');self.assertTrue((R/d['image']['path'].lstrip('/')).is_file())
  tr=json.loads((R/'data/deal_localizations.json').read_text())[d['id']]
  for lang in ('en','ko','zh','ja','es','fr'):self.assertIn('microSD',tr[lang]['conditions'])
