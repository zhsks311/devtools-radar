import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url,publishable_link
class SteamOfferTest(unittest.TestCase):
 def test_only_product_routes(self):
  self.assertTrue(direct_product_url('https://store.steampowered.com/app/2102040/?cc=kr&l=koreana'))
  for url in ('https://store.steampowered.com/search/?term=puppy','https://store.steampowered.com/','https://store.steampowered.com/app/2102040/?q=puppy'):
   self.assertFalse(direct_product_url(url))
 def test_korean_offer_is_exact_package_not_checkout_guarantee(self):
  from tools.deal_prices import checked_price
  from tools.deal_countries import target_countries,confirmed_countries
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='my-little-puppy-steam-kr')
  self.assertEqual(d['price'],17400);self.assertTrue(checked_price(d))
  self.assertEqual(d['expires_at'],'2026-11-23T17:00:00Z')
  self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),())
  loc=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(len(loc),6)
  for l in loc.values():self.assertIn('751340',l['conditions'])
