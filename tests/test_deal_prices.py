import copy,json,unittest
from pathlib import Path
from tools.deal_prices import discount_percent,validate_deal_prices,checked_price
import build,site_i18n
ROOT=Path(__file__).resolve().parents[1]
class DiscountTests(unittest.TestCase):
 def setUp(self):
  self.d=copy.deepcopy(json.loads((ROOT/'data/deals_en.json').read_text())['feed'][0])
  self.d.update(price=80,original_price=100,discount_pct=20)
  self.d['price_review']['verified_price']=80
  self.d['discount_review']={'status':'verified','same_product_variant':True,'same_terms':True,'currency':self.d['currency'],'sale_price':80,'reference_price':100,'source_url':self.d['link']['url'],'checked_at':'2026-11-10T12:00:00Z','evidence':'Same exact variant and terms, former seller price recorded.','reference_kind':'seller_previous_price'}
 def test_supported(self):
  self.assertEqual(discount_percent(self.d),20);self.assertEqual(validate_deal_prices([self.d]),[])
 def test_equal_reversed_zero_missing_invalid(self):
  for old in (80,70,0,None,'NaN','Infinity',True):
   d=copy.deepcopy(self.d);d['original_price']=old
   self.assertIsNone(discount_percent(d));self.assertTrue(validate_deal_prices([d]));self.assertNotIn('<s>',build._deal_card(d))
 def test_evidence_scope_and_conditions(self):
  for key,value in [('same_terms',False),('same_product_variant',False),('currency','ZZZ'),('source_url',''),('checked_at',''),('evidence',''),('reference_kind','official_rrp'),('sale_price',79)]:
   d=copy.deepcopy(self.d);d['discount_review'][key]=value
   self.assertIsNone(discount_percent(d));self.assertTrue(validate_deal_prices([d]))
 def test_rounding_not_zero_discount(self):
  self.d['price']=99.999;self.d['price_review']['verified_price']=99.999;self.d['discount_review']['sale_price']=99.999
  self.assertIsNone(discount_percent(self.d))
 def test_price_change_invalidates_claim(self):
  self.d['price']=81
  self.assertFalse(checked_price(self.d));self.assertTrue(validate_deal_prices([self.d]))
 def test_all_thirty_and_six_languages(self):
  feed=sum([json.loads((ROOT/'data'/f).read_text())['feed'] for f in ('deals.json','deals_en.json')],[])
  self.assertEqual(len(feed),30);self.assertEqual(validate_deal_prices(feed),[])
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,feed,{})
   self.assertEqual(page.count('<article class="card"'),30)
   self.assertNotIn('<s>',page);self.assertNotIn('flag-discount',page)
   self.assertIn(site_i18n.NOT_DISCOUNT[lang],page)
  for d in feed:self.assertNotIn('<s>',build._deal_card(d))
