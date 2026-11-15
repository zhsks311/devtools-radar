import json,unittest
from pathlib import Path
class RefundTermsTest(unittest.TestCase):
 def test_koofr_and_adguard_refund_windows_differ(self):
  root=Path(__file__).resolve().parents[1];rows=json.loads((root/'data/deals_en.json').read_text())['feed'];loc=json.loads((root/'data/deal_localizations.json').read_text())
  for ident,days in [('e30c9a510928',15),('3b4097687c74',30)]:
   d=next(d for d in rows if d['id']==ident)
   self.assertIn(f'within {days} days',d['purchase_eligibility']['returns'])
   self.assertFalse(d['price_review']['coupon']['checkout_verified'])
   for lang in ('en','ko','zh','ja','es','fr'):
    self.assertIn(str(days),loc[ident][lang]['conditions'])
   self.assertIn('not a cash refund',loc[ident]['en']['conditions'])
   self.assertNotIn('refund terms remain unverified',loc[ident]['en']['conditions'])
