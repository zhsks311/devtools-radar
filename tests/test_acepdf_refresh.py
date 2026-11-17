import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
class AcePDFRefresh(unittest.TestCase):
 def test_price_and_refund(self):
  k='3b4c5d317572';d=next(d for d in json.loads(Path('data/deals_en.json').read_text())['feed'] if d['id']==k)
  self.assertEqual(d['price'],23.97);self.assertTrue(checked_price(d));self.assertIsNone(d['original_price']);self.assertIsNone(d['discount_pct'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertEqual(d['latest_offer_check']['previous_recorded_price'],29.99)
  self.assertEqual(d['price_review']['coupon']['valid_through_date'],'2026-11-15')
  for v in json.loads(Path('data/deal_localizations.json').read_text())[k].values():
   self.assertIn('30',v['conditions']);self.assertNotIn('DEAL20',v['conditions'])
