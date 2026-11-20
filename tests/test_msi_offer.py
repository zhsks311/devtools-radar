import json,unittest,datetime
from pathlib import Path
from tools.deal_prices import checked_price,validated_price_options
class MSIPrice(unittest.TestCase):
 def test_option_and_price_separation(self):
  d=next(d for d in json.loads(Path('data/deals.json').read_text())['feed'] if d['id']=='msi-mp273q-e7-gmarket')
  self.assertTrue(checked_price(d));self.assertEqual(d['price'],172440)
  self.assertEqual([o['price'] for o in d['price_options']],[167440])
  self.assertEqual(len(validated_price_options(d)),1)
  self.assertTrue(any('142,710' in x['evidence'] for x in d['offer_check_history']))
  self.assertIn('Gmarket Samsung Card',d['price_options'][0]['conditions']['en'])
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],['KR'])
  self.assertIsNone(d['discount_pct']);self.assertIsNone(d['original_price'])
  loc=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(set(loc),{'ko','en','zh','ja','es','fr'})
  for v in loc.values(): self.assertIn('KVM',v['buying_note']);self.assertIn('75',v['summary'])
