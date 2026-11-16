import copy,json,unittest
from pathlib import Path
from datetime import datetime,timezone,timedelta
from tools.deal_prices import current_price_state,validated_price_options,validate_deal_prices
from site_i18n import visible_price_context
class PriceCurrentness(unittest.TestCase):
 def setUp(self):
  self.d=copy.deepcopy(next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='deal-ugreen-100w-gan'))
  self.now=datetime.now(timezone.utc)
  self.d['price_review']['review_completed_at']=self.now.isoformat()
  for item in self.d['price_options']: item['checked_at']=self.now.isoformat()
 def test_age_is_not_just_date_presence(self):
  self.assertEqual(current_price_state(self.d),'observed')
  self.d['price_review']['review_completed_at']=(self.now-timedelta(hours=25)).isoformat()
  self.assertEqual(current_price_state(self.d),'historical')
 def test_failed_new_check_blocks_old_success(self):
  self.d['latest_offer_check']['status']='unverified_current'
  self.assertEqual(current_price_state(self.d),'unverified')
 def test_price_currency_variant_source_match(self):
  for field,value in [('price',60900),('currency','USD')]:
   d=copy.deepcopy(self.d);d[field]=value
   self.assertEqual(current_price_state(d),'unverified')
  for field,value in [('variant','U-45417 · 160W'),('variant',''),('product_id','wrong'),('source_url','https://example.com'),('checked_at','9999-01-01T00:00:00Z'),('conditions',{})]:
   d=copy.deepcopy(self.d);d['price_options'][0][field]=value
   self.assertEqual(len(validated_price_options(d)),1)
   self.assertTrue(validate_deal_prices([d]))
 def test_exact_price_not_recomputed(self):
  self.assertEqual([x['price'] for x in validated_price_options(self.d)],[61850,59850])
  self.assertEqual(self.d['price'],65100)
 def test_six_languages_show_conditions_outside_details(self):
  for lang in ('ko','en','zh','ja','es','fr'):
   html=visible_price_context(self.d,lang)
   self.assertIn('61,850',html);self.assertIn('59,850',html)
   self.assertIn('U-25093',html);self.assertIn('datetime=',html)
   self.assertNotIn('<details',html)
 def test_old_coupon_does_not_inherit_fresh_base_observation(self):
  self.d['price_options'][0]['checked_at']=(self.now-timedelta(hours=25)).isoformat()
  text=visible_price_context(self.d,'en')
  self.assertIn('Historical price · not current',text)
 def test_fractional_coupon_is_not_rounded(self):
  self.d['currency']='USD'
  for item in self.d['price_options']: item['currency']='USD';item['price']='29.99'
  self.assertIn('USD 29.99',visible_price_context(self.d,'en'))
 def test_expiry_script_removes_savings_and_legacy_gate(self):
  import site_i18n,build
  self.assertIn("querySelectorAll('.current-savings')",site_i18n.JS)
  self.d['price_review']['review_completed_at']=(self.now-timedelta(hours=25)).isoformat()
  self.assertNotIn('<s>',build._deal_card(self.d))
 def test_browser_expiry_executes(self):
  import subprocess,shutil,site_i18n
  if not shutil.which('node'): self.skipTest('node unavailable')
  function=site_i18n.JS.split('function expireObservedPrices() {',1)[1].split('\nexpireObservedPrices();',1)[0]
  script='function expireObservedPrices() {'+function+'''
const assert = require('node:assert/strict');
const claim = {hidden:false};
const node = {dataset:{priceState:'observed',observedAt:'2026-11-15T00:00:00Z',staleLabel:'historical'},textContent:'fresh',closest(){return {querySelectorAll(){return [claim]}}}};
const document = {querySelectorAll(){return [node]}};
Date.now = () => Date.parse('2026-11-16T00:00:01Z');
expireObservedPrices();
assert.equal(node.dataset.priceState,'historical');
assert.equal(node.textContent,'historical');
assert.equal(claim.hidden,true);
'''
  subprocess.run(['node','-e',script],check=True,capture_output=True)
