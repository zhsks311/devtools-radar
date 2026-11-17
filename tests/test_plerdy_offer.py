import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link,direct_product_url
import site_i18n
class PlerdyOffer(unittest.TestCase):
 def test_offer_and_renewal(self):
  k='plerdy-startup-bf-first-year'
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],126);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(d['original_price'])
  self.assertEqual(d['expires_at'],'2026-12-03T07:59:00+00:00');self.assertFalse(direct_product_url('https://www.plerdy.com/'))
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  for l,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn('126',v['conditions']);self.assertIn('252',v['conditions']);self.assertIn('plerdyBF2026',v['conditions']);self.assertIn('30',v['buying_note']);self.assertTrue(site_i18n.billing_label(d,l))
