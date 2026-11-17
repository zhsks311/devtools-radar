import json, unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link, direct_product_url
from product_visuals import product_media
import site_i18n
class UlyssesOffer(unittest.TestCase):
 def test_price_eligibility_and_actual_image(self):
  k='ulysses-howiwrite-first-year'
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],19.99);self.assertIsNone(d['original_price']);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertFalse(direct_product_url('https://ulysses.app/'))
  self.assertFalse(d['link']['tracked']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  for l,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn('HOWIWRITE',v['conditions']);self.assertIn('19.99',v['conditions']);self.assertIn('39.99',v['conditions']);self.assertIn('24',v['buying_note']);self.assertIn('Apple',v['buying_note']);self.assertTrue(site_i18n.billing_label(d,l))
   media=product_media(d,l,v['product']);self.assertIn('/assets/deals/ulysses.webp',media);self.assertIn('https://ulysses.app/press/media/',media);self.assertNotIn('<svg',media)
