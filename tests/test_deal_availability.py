import copy,json,unittest
from pathlib import Path
from tools.deal_availability import classify_visible_offer,blocks_publication
from tools.product_links import publishable_link
class AvailabilityTests(unittest.TestCase):
 def test_purchase_limit_alone_does_not_prove_inventory(self):
  self.assertEqual(classify_visible_offer('최대구매수량 1일당 1개 (구매가능: 1개)',product_matched=True,option_matched=True),'availability_unverified')
 def test_sold_out_wins_over_limit_and_stale_buy_button(self):
  self.assertEqual(classify_visible_offer('SOLD OUT 최대구매수량 1일당 1개 (구매가능: 1개)',product_matched=True,purchase_cta=True,price_observed=True,option_matched=True),'sold_out')
 def test_captcha_is_not_product_or_stock(self):
  self.assertEqual(classify_visible_offer('CAPTCHA',product_matched=True,purchase_cta=True,price_observed=True,option_matched=True),'access_unverified')
 def test_variant_and_purchase_ui_are_not_checkout_guarantee(self):
  kw=dict(product_matched=True,purchase_cta=True,price_observed=True)
  self.assertEqual(classify_visible_offer('Buy now',**kw),'option_unverified')
  self.assertEqual(classify_visible_offer('Buy now',option_matched=True,**kw),'purchase_ui_observed')
 def test_negative_availability_blocks_even_old_verified_link(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='ps5-dualsense-midnight-black-kr')
  for review in [{'status':'sold_out'},{'status':'in_stock','basis':'purchase_limit'}]:
   clone=copy.deepcopy(d);clone['availability_review']=review
   self.assertFalse(publishable_link(clone))
 def test_failed_recheck_has_visible_warning_not_sold_out(self):
  import site_i18n
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='ps5-dualsense-midnight-black-kr')
  d=copy.deepcopy(d);d['latest_offer_check']={'status':'unverified_current'}
  tr=json.loads(Path('data/deal_localizations.json').read_text())
  for lang in site_i18n.LANGS:
   html=site_i18n.catalogue(lang,[d],tr)
   self.assertIn(site_i18n.CURRENT_OFFER_UNVERIFIED[lang],html)
   self.assertNotIn(site_i18n.SOLD_OUT_LABEL[lang],html)
 def test_audit_keeps_failed_checks_separate_from_last_good_price(self):
  rows=sum([json.loads(Path('data/'+f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
  for d in rows:
   r=d.get('latest_offer_check') or {}
   if r.get('status')=='unverified_current':
    self.assertIsNone(r['price'])
    self.assertIsNotNone(d['price'])
    self.assertNotEqual(r['observed_at'],d['price_review']['review_completed_at'])
