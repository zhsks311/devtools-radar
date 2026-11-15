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
 def test_korean_offer_separate_from_usd(self):
  from tools.deal_countries import target_countries,confirmed_countries
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='hostinger-premium-black-friday-48-months')
  self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),())
  self.assertEqual(d['price'],95.52);self.assertEqual(d['currency'],'USD')
  self.assertEqual(15319*48,735312)
  self.assertEqual(d['alternative_review']['sources'][0]['url'],'https://www.hostinger.com/kr/black-friday-web-hosting-deals')
  self.assertNotIn('proton',json.dumps(d['alternative_review']).lower())
  for loc in json.loads(Path('data/deal_localizations.json').read_text())[d['id']].values():
   for value in ['133,392','15,319','735,312']:
    self.assertIn(value,loc['buying_note'])
   for value in ['166,992','200,112']:
    self.assertNotIn(value,loc['buying_note'])
 def test_refund_exceptions_have_dated_source(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='hostinger-premium-black-friday-48-months')
  self.assertFalse(d['refund_review']['korean_order_verified'])
  self.assertEqual(d['refund_review']['policy_url'],'https://www.hostinger.com/legal/refund-policy')
  self.assertIn('non-refundable',d['purchase_eligibility']['returns'])
  words={'ko':'암호화폐','en':'Cryptocurrency','zh':'加密货币','ja':'暗号資産','es':'criptomonedas','fr':'cryptomonnaies'}
  for lang,loc in json.loads(Path('data/deal_localizations.json').read_text())[d['id']].items():
   self.assertIn(words[lang],loc['conditions'])
   self.assertIn('95.52',loc['summary'])
