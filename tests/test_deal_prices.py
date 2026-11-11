import copy,json,unittest
from pathlib import Path
from tools.deal_prices import discount_percent,validate_deal_prices,checked_price,official_srp_comparison
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
 def test_future_price_and_discount_dates_fail_closed(self):
  for section,field in [('price_review','review_completed_at'),('discount_review','checked_at')]:
   for value in ('9999-01-01T00:00:00Z',None,{},'2026-11-10'):
    with self.subTest(section=section,value=value):
     d=copy.deepcopy(self.d);d[section][field]=value
     self.assertIsNone(discount_percent(d));self.assertTrue(validate_deal_prices([d]))
     self.assertNotIn('<s>',build._deal_card(d))
     if section=='price_review':
      self.assertFalse(checked_price(d))
      for lang in site_i18n.LANGS:
       self.assertNotIn(site_i18n.PRICE_CURRENT[lang],site_i18n.catalogue(lang,[d],{}))
 def test_price_evidence_requires_matching_url_and_observation(self):
  for value in (True,'observed',[{}],[{'url':self.d['link']['url'],'result':' '}],
                [{'url':'https://example.com/','result':'different seller'}]):
   with self.subTest(value=value):
    d=copy.deepcopy(self.d);d['price_review']['evidence']=value
    self.assertFalse(checked_price(d));self.assertTrue(validate_deal_prices([d]))
 def test_srp_comparison_uses_verified_numbers_instead_of_fixed_copy(self):
  d=copy.deepcopy(next(d for d in json.loads((ROOT/'data/deals_en.json').read_text())['feed'] if d['id']=='43ca41d03daa'))
  self.assertEqual(str(official_srp_comparison(d)['percent']),'5.45')
  d['price']=700;d['price_review']['verified_price']=700
  self.assertEqual(str(official_srp_comparison(d)['percent']),'9.09')
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,[d],{})
   self.assertIn('9.09',page);self.assertNotIn('5.45%',page)
  for field,value in [('currency','USD'),('price',699),('same_product_variant',False),
                      ('product_id','other'),('checked_at','9999-01-01T00:00:00Z'),
                      ('evidence',' '),('reference_kind','seller_previous_price'),('url','javascript:alert(1)')]:
   bad=copy.deepcopy(d);bad['price_review']['comparison'][field]=value
   with self.subTest(field=field,value=value):
    self.assertIsNone(official_srp_comparison(bad));self.assertTrue(validate_deal_prices([bad]))
    for lang in site_i18n.LANGS:
     page=site_i18n.catalogue(lang,[bad],{})
     self.assertNotIn('9.09%',page);self.assertIn(site_i18n.DISCOUNT_UNKNOWN[lang],page)
  d['price']=800;d['price_review']['verified_price']=800
  self.assertIsNone(official_srp_comparison(d))
 def test_all_thirty_and_six_languages(self):
  feed=sum([json.loads((ROOT/'data'/f).read_text())['feed'] for f in ('deals.json','deals_en.json')],[])
  self.assertEqual(len(feed),30);self.assertEqual(validate_deal_prices(feed),[])
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,feed,{})
   self.assertEqual(page.count('<article class="card"'),30)
   self.assertNotIn('<s>',page);self.assertNotIn('flag-discount',page)
   self.assertIn(site_i18n.NOT_DISCOUNT[lang],page)
  for d in feed:self.assertNotIn('<s>',build._deal_card(d))
