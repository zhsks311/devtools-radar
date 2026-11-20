import json,unittest
from pathlib import Path
from tools.product_links import publishable_link
from tools.deal_countries import target_countries,confirmed_countries
class NewKRGamingOffersTest(unittest.TestCase):
 def test_seller_prices_are_not_effective_points_prices(self):
  rows={x['id']:x for x in json.loads(Path('data/deals.json').read_text())['feed']}
  for ident,price in [('google-play-100k-kr',92000),('ps5-dualsense-midnight-black-kr',87500)]:
   d=rows[ident];self.assertEqual(publishable_link(d), ident != 'google-play-100k-kr');self.assertEqual(d['price'],price)
   self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertFalse(d['link']['tracked'])
   self.assertEqual(target_countries(d),('KR',))
  self.assertEqual(confirmed_countries(rows['google-play-100k-kr']),())
  self.assertEqual(confirmed_countries(rows['ps5-dualsense-midnight-black-kr']),('KR',))

 def test_sold_out_overrides_purchase_limit_in_all_languages(self):
  import site_i18n
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='google-play-100k-kr')
  self.assertEqual(d['availability_review']['status'],'sold_out')
  self.assertIn('not stock',d['availability_review']['evidence'])
  tr=json.loads(Path('data/deal_localizations.json').read_text())
  for lang in site_i18n.LANGS:
   html=site_i18n.catalogue(lang,[d],tr)
   self.assertIn(site_i18n.SOLD_OUT_LABEL[lang],html)
   self.assertNotIn(d['link']['url'],html)
