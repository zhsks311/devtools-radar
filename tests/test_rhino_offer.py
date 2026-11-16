import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link
class RhinoOffer(unittest.TestCase):
 def test_not_like_for_like_discount(self):
  d=next(d for d in json.loads(Path('data/deals_en.json').read_text())['feed'] if d['id']=='rhino-voice-1-mac')
  self.assertEqual(d['price'],12);self.assertEqual(d['price_variant'],'1 Code / 1 Mac')
  self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct'])
  for v in json.loads(Path('data/deal_localizations.json').read_text())[d['id']].values():
   self.assertIn('2000',v['conditions']);self.assertIn('$20',v['conditions']);self.assertIn('60',v['conditions'])
