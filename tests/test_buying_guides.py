import json,unittest,copy
from pathlib import Path
from buying_guides import guide,PATHS
import site_i18n,site_seo
class BuyingGuidesTest(unittest.TestCase):
 def setUp(self):
  self.d=next(d for d in json.loads((Path(__file__).resolve().parents[1]/'data/deals_en.json').read_text())['feed'] if d['id']=='0deb259ecfd4')
 def test_prices_follow_reviewed_record(self):
  for lang in PATHS:
   text=guide(lang,self.d)
   for price in ['USD 9.99','USD 19.77','USD 32.95']:self.assertIn(price,text)
   for source in ['https://obsproject.com/','https://mirillis.com/purchase-faq',self.d['link']['url']]:self.assertIn(source,text)
   self.assertNotIn('<del',text)
   self.assertNotIn('aggregateRating',text)
  d=copy.deepcopy(self.d);d['price']=12;d['price_review']['verified_price']=12
  self.assertIn('USD 12.00',guide('en',d));self.assertNotIn('USD 9.99',guide('en',d))
 def test_unverified_price_is_not_a_purchase_quote(self):
  d=copy.deepcopy(self.d);d['price_review']['price_status']='unverified'
  self.assertIn('Price needs rechecking',guide('en',d));self.assertNotIn('USD 9.99',guide('en',d))
 def test_guide_navigation_is_reciprocal_and_truthful(self):
  for path in PATHS.values():self.assertEqual(site_seo.alternates_for(path),dict(PATHS,**{'x-default':PATHS['en']}))
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,[self.d],{})
   self.assertIn('class="buying-guide-link"',page)
   self.assertIn(PATHS.get(lang,PATHS['en']),page)
