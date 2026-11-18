import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price,discount_percent
from tools.product_links import publishable_link,direct_product_url
class CrabOffer(unittest.TestCase):
 def test_exact_product_price_region_and_media(self):
  k='everything-is-crab-directgames-kr-jp';d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']==k)
  self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertEqual(d['price'],7700);self.assertIsNone(discount_percent(d));self.assertIsNone(d['expires_at']);self.assertEqual(d['country_targeting']['countries'],['KR','JP']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR','JP']);self.assertTrue(Path(d['image']['path'].lstrip('/')).is_file())
  for v in json.loads(Path('data/deal_localizations.json').read_text())[k].values():self.assertIn('Steam',v['conditions']);self.assertIn('23:59',v['conditions'])

 def test_non_www_detail_gate_rejects_search_and_bad_ids(self):
  for url in ['https://directg.net/', 'https://directg.net/game/game_search.html?q=crab','https://directg.net/game/game_view.html?product_id=123','https://directg.net.evil.example/game/game_view.html?product_id=c4c5e959-7130-4828-82de-8e0a2a7ce5a1']:
   self.assertFalse(direct_product_url(url))
