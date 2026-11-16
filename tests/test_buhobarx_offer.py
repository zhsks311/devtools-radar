import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link,direct_product_url
class BuhoBarXOffer(unittest.TestCase):
 def test_single_license_not_bundle_or_subscription(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='buhobarx-single-lifetime')
  self.assertFalse(direct_product_url('https://www.drbuho.com/black-friday-sale'));self.assertFalse(direct_product_url('https://www.drbuho.com/buhobarx?q=other'))
  self.assertEqual(d['price'],7.99);self.assertEqual(d['price_variant'],'Lifetime - Single (1 Mac)')
  self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d))
  self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertIn('subtotal',d['purchase_eligibility']['tax']);self.assertIn('exclusions',d['purchase_eligibility']['returns'])
  loc=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  for l in ('en','ko','zh','ja','es','fr'):
   self.assertIn('30',loc[l]['conditions']);self.assertIn('14',loc[l]['conditions'])
