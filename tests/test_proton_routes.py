import unittest
from tools.product_links import direct_product_url
class ProtonRoutesTest(unittest.TestCase):
 def test_product_campaign_routes_only(self):
  for product in ['mail','drive','pass']:
   self.assertTrue(direct_product_url(f'https://proton.me/{product}/black-friday'))
  for url in ['https://proton.me/','https://proton.me/search','https://proton.me/mail/black-friday?q=mail','https://proton.me.evil.test/mail/black-friday']:
   self.assertFalse(direct_product_url(url))
 def test_annual_totals_and_renewal_not_monthly_discount(self):
  import json
  from pathlib import Path
  from tools.product_links import publishable_link
  from tools.deal_countries import confirmed_countries,target_countries
  import site_i18n
  data=json.loads(Path('data/deals_en.json').read_text());tr=json.loads(Path('data/deal_localizations.json').read_text())
  for product,price,renewal in [('mail',29.88,47.88),('drive',29.88,47.88),('pass',23.88,35.88)]:
   ident=f'proton-{product}-plus-black-friday-annual';d=next(x for x in data['feed'] if x['id']==ident)
   self.assertEqual(d['price'],price);self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertIsNone(d['expires_at']);self.assertTrue(publishable_link(d))
   self.assertEqual(target_countries(d),());self.assertEqual(confirmed_countries(d),())
   self.assertFalse(d['link']['tracked'])
   for lang in site_i18n.LANGS:
    self.assertIn(str(renewal),tr[ident][lang]['conditions']);self.assertIn('12',tr[ident][lang]['product']);self.assertNotIn('NaN',tr[ident][lang]['summary'])
