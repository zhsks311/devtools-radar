import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url,publishable_link
from tools.deal_countries import target_countries,confirmed_countries
class AdobeOfferTest(unittest.TestCase):
 def test_commitment_and_cancel_terms(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='adobe-creative-cloud-kr-bf-monthly-annual')
  self.assertEqual(d['price'],34800);self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),())
  self.assertTrue(publishable_link(d));self.assertFalse(d['link']['tracked']);self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct']);self.assertIsNone(d['expires_at'])
  t=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(set(t),{'en','ko','zh','ja','es','fr'})
  for loc in t.values():
   for v in ['14','10%','87,900','396,217','2026-11-13']:
    self.assertIn(v,loc['conditions'])
   self.assertIn('417,600',loc['summary']);self.assertIn('34,800',loc['summary'])
 def test_route_not_general_search(self):
  self.assertTrue(direct_product_url('https://www.adobe.com/kr/creativecloud.html'))
  for url in ['https://www.adobe.com/','https://www.adobe.com/kr/creativecloud/plans.html','https://www.adobe.com/kr/creativecloud.html?q=foo']:
   self.assertFalse(direct_product_url(url))
