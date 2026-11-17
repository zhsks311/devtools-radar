import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link
class YakuzaOffer(unittest.TestCase):
 def test_price_region_and_edition(self):
  k='yakuza-kiwami3-dark-ties-directgames';d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']==k)
  self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertEqual(d['price'],25800);self.assertIsNone(d['original_price']);self.assertIsNone(d['expires_at'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR'])
  for l,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn('02:00',v['conditions']);self.assertIn('7',v['buying_note']);self.assertIn('Denuvo',v['buying_note'])
