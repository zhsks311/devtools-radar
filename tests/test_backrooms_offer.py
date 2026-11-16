import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url,publishable_link
from tools.deal_countries import confirmed_countries
class BackroomsOfferTest(unittest.TestCase):
 def test_exact_product_basegame_and_regions(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='escape-backrooms-directgames-kr-jp')
  self.assertEqual((d['price'],d['currency']),(6900,'KRW')); self.assertTrue(publishable_link(d))
  self.assertEqual(confirmed_countries(d),('JP','KR')); self.assertIsNone(d['discount_pct']); self.assertIsNone(d['expires_at'])
  self.assertIn('timezone not specified',d['price_review']['evidence'][0]['result'])
 def test_reject_catalogue_and_bad_id(self):
  for u in ['https://www.directg.net/game/game_view.html','https://www.directg.net/game/game_view.html?product_id=search','https://www.directg.net/promotion/promotion_ing_list.html','https://www.directg.net/game/game_view.html?product_id=c4166ba4-60be-462b-b0f6-375a8d4398e5&product_id=x']:
   self.assertFalse(direct_product_url(u))
