import json,unittest
from pathlib import Path
from tools.deal_countries import target_countries,confirmed_countries
from tools.product_links import publishable_link
class KoreanOffersTest(unittest.TestCase):
 def test_seller_prices_and_coupon_condition_not_community_lower_price(self):
  rows=json.loads(Path('data/deals.json').read_text())['feed'];tr=json.loads(Path('data/deal_localizations.json').read_text())
  for ident,price,countries in [('anker-p31i-d1202-kr',24440,('KR',)),('mega-coffee-hot-americano-kr',1320,())]:
   d=next(x for x in rows if x['id']==ident)
   self.assertEqual(d['price'],price);self.assertEqual(publishable_link(d),False);self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),countries)
   self.assertIsNone(d['discount_pct']);self.assertIsNone(d['published_at']);self.assertFalse(d['link']['tracked'])
   self.assertEqual(set(tr[ident]),{'ko','en','zh','ja','es','fr'})
  self.assertIn('7%',tr['anker-p31i-d1202-kr']['ko']['conditions'])
  self.assertIn('93',tr['mega-coffee-hot-americano-kr']['ko']['conditions'])

 def test_sold_out_anker_not_live_price(self):
  rows=json.loads(Path('data/deals.json').read_text())['feed']
  d=next(x for x in rows if x['id']=='anker-p31i-d1202-kr')
  self.assertEqual(d['availability_review']['status'],'sold_out')
  self.assertIsNone(d['price_review']['verified_price'])
  self.assertEqual(d['price_review']['previous_verified_price'],24440)
  self.assertFalse(publishable_link(d))

 def test_sold_out_coffee_not_live_price(self):
  rows=json.loads(Path('data/deals.json').read_text())['feed']
  d=next(x for x in rows if x['id']=='mega-coffee-hot-americano-kr')
  self.assertEqual(d['availability_review']['status'],'sold_out')
  self.assertIsNone(d['price_review']['verified_price'])
  self.assertEqual(d['price_review']['previous_verified_price'],1320)
  self.assertFalse(publishable_link(d))
