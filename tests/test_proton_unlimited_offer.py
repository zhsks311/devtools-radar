import json
import unittest
from pathlib import Path
from tools.product_links import publishable_link

class UnlimitedOfferTest(unittest.TestCase):
 def test_annual_total_not_monthly_teaser(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='proton-unlimited-black-friday-annual')
  self.assertEqual(d['price'],77.88)
  self.assertEqual(d['price_review']['verified_price'],77.88)
  self.assertIsNone(d['discount_pct'])
  self.assertIsNone(d['original_price'])
  self.assertTrue(publishable_link(d))
  self.assertIn('119.88',d['price_review']['conditions'][0])
  self.assertIn('not this annual plan',d['price_review']['conditions'][0])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertEqual(d['image']['path'],'/assets/deals/proton-mail.webp')
 def test_localized_terms(self):
  t=json.loads(Path('data/deal_localizations.json').read_text())['proton-unlimited-black-friday-annual']
  for lang in ['en','ko','ja','zh','es','fr']:
   self.assertIn('77.88',t[lang]['conditions'])
   self.assertIn('119.88',t[lang]['conditions'])
   self.assertIn('500',t[lang]['summary'])
