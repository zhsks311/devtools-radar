import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class BabbelLearnTests(unittest.TestCase):
 def test_conditional_coupon_does_not_replace_base_or_us_limit(self):
  x=json.loads((R/'data/deals_en.json').read_text()); d=next(d for d in x['feed'] if d['id']=='babbel-lifetime-all-languages')
  self.assertEqual(d['price'],249); self.assertEqual(d['price_review']['verified_price'],249)
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['US'])
  c=d['price_review']['current_coupon']; self.assertEqual(c['code'],'LEARN'); self.assertEqual(c['displayed_price'],159); self.assertFalse(c['checkout_verified']); self.assertIsNone(c['ends_at'])
  tr=json.loads((R/'data/deal_localizations.json').read_text())[d['id']]
  for lang in ('en','ko','zh','ja','es','fr'):
   self.assertIn('LEARN',tr[lang]['conditions']); self.assertIn('159',tr[lang]['conditions']); self.assertIn('249',tr[lang]['conditions']); self.assertNotIn('DEAL20',tr[lang]['conditions'])
