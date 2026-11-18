import json, unittest
from pathlib import Path
from product_visuals import product_media
class DJIPhotoTests(unittest.TestCase):
 def test_base_model_uses_attributed_photo_not_svg(self):
  deal=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='dji-osmo-mobile-7-cn')
  self.assertEqual(deal['price'],349)
  self.assertEqual(deal['currency'],'CNY')
  self.assertIsNone(deal['discount_pct'])
  for lang in ('ko','en','zh','ja','es','fr'):
   html=product_media(deal,lang,deal['product'])
   self.assertIn('/assets/deals/dji-osmo-mobile-7.webp',html)
   self.assertIn('DJI Europe',html)
   self.assertNotIn('<svg',html)
  self.assertIn('no phone or optional tracking module',deal['image']['alt'])
