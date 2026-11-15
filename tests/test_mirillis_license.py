import json,unittest
from pathlib import Path
import site_i18n
from tools.deal_prices import checked_price,official_srp_comparison
class MirillisLicenseTest(unittest.TestCase):
 def test_different_license_prices_never_become_discount(self):
  root=Path(__file__).resolve().parents[1]
  d=next(d for d in json.loads((root/'data/deals_en.json').read_text())['feed'] if d['id']=='0deb259ecfd4')
  loc=json.loads((root/'data/deal_localizations.json').read_text())
  self.assertTrue(checked_price(d)); self.assertIsNone(official_srp_comparison(d))
  self.assertFalse(d['link']['tracked']);self.assertIsNone(d['discount_pct'])
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,[d],loc)
   for price in ['$9.99','$19.77','$32.95']: self.assertIn(price,page)
   self.assertIn('class="notice buying-note"',page)
   self.assertIn('https://mirillis.com/purchase-faq',page)
   self.assertIn('https://mirillis.com/store-action-paysafecard',page)
   self.assertNotIn('<del',page)
   self.assertNotIn('rel="noopener nofollow sponsored"',page)
