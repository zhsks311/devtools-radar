import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url,publishable_link
class ChronoidOfferTest(unittest.TestCase):
 def test_lifetime_scope_and_evidence(self):
  d=json.loads(Path('data/deals_en.json').read_text());r=next(x for x in d['feed'] if x['id']=='chronoid-lifetime-black-friday')
  self.assertEqual(r['price'],74.5);self.assertEqual(r['currency'],'USD');self.assertIsNone(r['original_price']);self.assertIsNone(r['discount_pct']);self.assertIsNone(r['expires_at']);self.assertEqual(r['purchase_eligibility']['countries_confirmed'],[])
  self.assertEqual(r,next(x for x in d['categories']['cloud']['items'] if x['id']==r['id']))
  self.assertEqual(r['price_review']['campaign']['ends_on'],'2026-12-03');self.assertIsNone(r['price_review']['campaign']['timezone']);self.assertTrue(publishable_link(r))
  loc=json.loads(Path('data/deal_localizations.json').read_text())[r['id']]
  self.assertEqual(set(loc),{'en','ko','zh','ja','es','fr'})
  for v in loc.values():
   for word in ['74.50','30','2026','BLACKFRIDAY26']:self.assertIn(word,v['conditions'])
  self.assertIn('product',loc['en']['conditions']);self.assertIn('AI',loc['en']['conditions'])
 def test_product_route_only(self):
  self.assertTrue(direct_product_url('https://www.chronoid.app/pricing'))
  for u in ['https://www.chronoid.app/','https://www.chronoid.app/terms','https://www.chronoid.app/pricing?q=test']:
   self.assertFalse(direct_product_url(u))
