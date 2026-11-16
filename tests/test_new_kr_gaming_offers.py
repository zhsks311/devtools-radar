import json,unittest
from pathlib import Path
from tools.product_links import publishable_link
from tools.deal_countries import target_countries,confirmed_countries
class NewKRGamingOffersTest(unittest.TestCase):
 def test_seller_prices_are_not_effective_points_prices(self):
  rows={x['id']:x for x in json.loads(Path('data/deals.json').read_text())['feed']}
  for ident,price in [('google-play-100k-kr',92000),('ps5-dualsense-midnight-black-kr',74800)]:
   d=rows[ident];self.assertTrue(publishable_link(d));self.assertEqual(d['price'],price)
   self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertFalse(d['link']['tracked'])
   self.assertEqual(target_countries(d),('KR',))
  self.assertEqual(confirmed_countries(rows['google-play-100k-kr']),())
  self.assertEqual(confirmed_countries(rows['ps5-dualsense-midnight-black-kr']),('KR',))
