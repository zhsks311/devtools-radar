import json,unittest
from pathlib import Path
from tools.product_links import publishable_link
class AceOfferTest(unittest.TestCase):
 def test_selected_bundle_not_banner(self):
  d=next(d for d in json.loads(Path('data/deals.json').read_text())['feed'] if d['id']=='insta360-ace-pro-2-kr-dual-battery')
  self.assertEqual(d['price'],437000)
  self.assertEqual(d['price_review']['verified_price'],437000)
  self.assertIsNone(d['discount_pct']); self.assertIsNone(d['original_price'])
  self.assertTrue(publishable_link(d));self.assertEqual(d['country_targeting']['countries'],['KR'])
  self.assertIn('Media use',d['image']['rights_basis'])
  self.assertTrue(Path(d['image']['path'].lstrip('/')).is_file())
 def test_locales(self):
  tr=json.loads(Path('data/deal_localizations.json').read_text())['insta360-ace-pro-2-kr-dual-battery']
  for lang in ('en','ko','ja','zh','es','fr'):
   self.assertTrue(tr[lang]['summary']);self.assertIn('437',tr[lang]['conditions']);self.assertTrue(tr[lang]['buying_note'])
