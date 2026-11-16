import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url
class SnippetyOfferTest(unittest.TestCase):
 def test_exact_app_and_distinct_store_prices(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='snippety-pro-apple-black-friday')
  self.assertEqual((d['price'],d['currency'],d['storefront_country']),(29.99,'USD','US'))
  self.assertIsNone(d['discount_pct']);self.assertIsNone(d['original_price'])
  self.assertTrue(direct_product_url(d['link']['url']))
  self.assertFalse(direct_product_url('https://apps.apple.com/us/search?term=snippety'))
  self.assertFalse(direct_product_url('https://apps.apple.com/us/iphone/today'))
  tr=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertIn('49,000',tr['ko']['conditions']);self.assertIn('라틴',tr['ko']['conditions'])
