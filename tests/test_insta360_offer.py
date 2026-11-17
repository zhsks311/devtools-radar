import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link
from product_visuals import product_media
class Insta360Offer(unittest.TestCase):
 def test_exact_bundle_price_and_licensed_photo(self):
  k='insta360-x5-kr-standard';d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],645000);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(d['discount_pct']);self.assertIsNone(d['original_price']);self.assertFalse(d['link']['tracked'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR']);self.assertNotIn('price_options',d)
  loc=json.loads(Path('data/deal_localizations.json').read_text())[k];self.assertEqual(len(loc),6)
  for l,v in loc.items():
   self.assertIn('SD',v['conditions']);self.assertIn('15',v['buying_note']);self.assertIn('Gold',v['conditions'])
   m=product_media(d,l,v['product']);self.assertIn('insta360-x5.webp',m);self.assertNotIn('<svg',m);self.assertNotIn('sample UI',m)
