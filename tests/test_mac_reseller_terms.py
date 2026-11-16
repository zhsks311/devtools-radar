import json,unittest
from pathlib import Path
class MacTerms(unittest.TestCase):
 def test_cash_refund_not_promised(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed'];loc=json.loads(Path('data/deal_localizations.json').read_text())
  for k in ('de0f62d0487f','9caac4280b19'):
   d=next(d for d in rows if d['id']==k)
   self.assertIn('store credit',d['service_terms']['refund']);self.assertIn('sales final',d['service_terms']['refund'])
   for l in ('en','ko','zh','ja','es','fr'):self.assertIn('30',loc[k][l]['conditions'])
  d=next(d for d in rows if d['id']=='de0f62d0487f');self.assertIn('cost extra',d['service_terms']['updates'])
