import json,unittest
from pathlib import Path
from decimal import Decimal
from tools.product_links import direct_product_url
class HostingerOfferTest(unittest.TestCase):
 def test_commitment_renewal_and_unknown_country(self):
  root=Path(__file__).resolve().parents[1]
  data=json.loads((root/'data/deals_en.json').read_text())
  ident='hostinger-premium-black-friday-48-months'
  d=next(x for x in data['feed'] if x['id']==ident)
  self.assertEqual(d['price'],95.52)
  self.assertEqual(Decimal('1.99')*48,Decimal('95.52'))
  self.assertEqual(Decimal('10.99')*48,Decimal('527.52'))
  self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertIsNone(d['expires_at'])
  self.assertEqual(d['price_review']['campaign']['ends_on'],'2026-12-14')
  self.assertIsNone(d['price_review']['campaign']['timezone'])
  loc=json.loads((root/'data/deal_localizations.json').read_text())[ident]
  for lang in ('en','ko','zh','ja','es','fr'):
   text=json.dumps(loc[lang],ensure_ascii=False)
   for term in ('48','95.52','10.99','527.52'):
    self.assertIn(term,text,lang)
  self.assertEqual(d,next(x for x in data['categories']['cloud']['items'] if x['id']==ident))
 def test_exact_product_page_not_generic_campaign(self):
  self.assertTrue(direct_product_url('https://www.hostinger.com/web-hosting'))
  for url in ('https://www.hostinger.com/','https://www.hostinger.com/black-friday','https://www.hostinger.com/web-hosting?q=plan'):
   self.assertFalse(direct_product_url(url))
