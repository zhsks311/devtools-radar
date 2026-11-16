import json,unittest
from pathlib import Path
from tools.product_links import publishable_link,direct_product_url
from tools.deal_prices import checked_price
import site_i18n
class ElevenOffer(unittest.TestCase):
 def test_annual_eligibility_and_plan_separation(self):
  k='elevenlabs-creator-bf-first-year'
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],99);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d))
  self.assertIsNone(d['original_price']);self.assertEqual(d['expires_at'],'2026-12-02T04:59:00+00:00')
  self.assertFalse(direct_product_url('https://join.elevenlabs.io/'))
  for lang,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertTrue(site_i18n.billing_label(d,lang)); self.assertIn('121',v['summary']);self.assertIn('UTC',v['conditions']);self.assertIn('495',v['buying_note']);self.assertIn('API',v['buying_note'])
 def test_credit_cycle_and_price_timestamp_preserved(self):
  k='elevenlabs-creator-bf-first-year'
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price_review']['review_completed_at'],'2026-11-16T21:37:12.079241+00:00')
  self.assertEqual(d['price'],99)
  self.assertIn('monthly',d['credit_allocation_review']['annual_allocation'])
  self.assertTrue(any(s['url'].endswith('/administration/billing') for s in d['alternative_review']['sources']))
  words={'ko':'이월','en':'roll','zh':'结转','ja':'繰り越','es':'traslad','fr':'report'}
  for lang,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn(words[lang],v['buying_note'])
