import unittest
from datetime import datetime,timezone
from tools.publish_startup_benefits import prepare,render,prepare_saasoffers
class BenefitTests(unittest.TestCase):
 def row(self,**kw):
  return dict(slug='sample',url='https://that.promo/sample',official_url='https://example.com/product',status='live',last_verified='2026-11-01',name='<script>alert(1)</script>',provider='Sample',expiry='ongoing',who_qualifies='New customers',**kw)
 def test_safe_and_attributed(self):
  x=prepare({'offers':[self.row()], 'generated_at':'2026-11-01'},datetime(2026,11,18,tzinfo=timezone.utc));s=render(x)
  self.assertIn('&lt;script&gt;',s);self.assertIn('New customers',s);self.assertIn('2026-11-01',s);self.assertIn('https://example.com/product',s)
 def test_dedupe(self):
  self.assertEqual(prepare({'offers':[self.row(),self.row()]},datetime(2026,11,18,tzinfo=timezone.utc))['count'],1)
 def test_reject_unsafe(self):
  r=self.row();r['official_url']='javascript:alert(1)'
  with self.assertRaises(ValueError):prepare({'offers':[r]},datetime(2026,11,18,tzinfo=timezone.utc))
 def test_ended_sponsored_expired_excluded(self):
  for changes in [{'status':'ended'},{'sponsored':True},{'expiry':'2026-11-18'}]:
   r=self.row();r.update(changes)
   with self.assertRaises(ValueError):prepare({'offers':[r]},datetime(2026,11,18,tzinfo=timezone.utc))
 def test_unknown_date_not_fabricated(self):
  r=self.row();r['last_verified']=None
  s=render(prepare({'offers':[r]},datetime(2026,11,18,tzinfo=timezone.utc)));self.assertIn('미기재',s);self.assertIn('재확인 필요',s)

class SaaSOfferTests(unittest.TestCase):
 def test_premium_and_codes_held(self):
  r={'slug':'one','name':'one','access':'free','url':'https://saasoffers.tech/offers/one','offer':'credits','eligibility':'Startups'}
  x=prepare_saasoffers({'deals':[r,dict(r,slug='two',access='premium'),dict(r,slug='three',description='Use code XYZ')]},datetime(2026,11,18,tzinfo=timezone.utc))
  self.assertEqual(x['count'],1);self.assertIsNone(x['offers'][0]['official_url']);self.assertIn('Direct merchant link not supplied',render(x));self.assertNotIn('XYZ',render(x))
