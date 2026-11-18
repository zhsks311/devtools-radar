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
 def test_unlimited_comparison_keeps_standalone_and_unknowns(self):
  import json
  from pathlib import Path
  d=json.loads(Path('data/deals_en.json').read_text());t=json.loads(Path('data/deal_localizations.json').read_text())
  for row in d['feed']:
   if row['id'].startswith('proton-') and row['id'] != 'proton-pass-family-black-friday-annual':
    self.assertEqual(row['purchase_eligibility']['countries_confirmed'],[])
    self.assertEqual(row['alternative_review']['sources'][0]['url'],'https://proton.me/mail/black-friday')
    for lang,loc in t[row['id']].items():
     for value in ['77.88','119.88','500','Unlimited']:
      self.assertIn(value,loc['buying_note'])
    self.assertIn('not annual renewal',row['alternative_review']['evidence'])

 def test_family_has_separate_billing_and_eligibility(self):
  import json
  from pathlib import Path
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='proton-pass-family-black-friday-annual')
  t=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(d['price'],33.48)
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertIsNone(d['original_price'])
  self.assertEqual(d['image']['path'],'/assets/deals/proton-pass.webp')
  for loc in t.values():
   self.assertIn('59.88',loc['conditions'])
   self.assertIn('33.48',loc['conditions'])
   self.assertIn('Visionary',loc['conditions'])

 def test_drive_alternative_does_not_replace_standard_offer(self):
  import json
  from pathlib import Path
  row=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='proton-drive-plus-black-friday-annual')
  self.assertEqual(row['price'],29.88)
  self.assertEqual(row['link']['url'],'https://proton.me/drive/black-friday')
  self.assertIn('https://proton.me/l/encrypted-cloud-storage-pfm-fapp',[s['url'] for s in row['alternative_review']['sources']])
  self.assertEqual(row['purchase_eligibility']['countries_confirmed'],[])
  for loc in json.loads(Path('data/deal_localizations.json').read_text())[row['id']].values():
   for value in ['23.94','47.88','PREMIUM_DRIVE_DEAL']: self.assertIn(value,loc['buying_note'])
