import json,unittest
from pathlib import Path
from tools.deal_prices import validated_price_options
class DualSensePrices(unittest.TestCase):
 def test_main_price_excludes_coupon_and_card(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='ps5-dualsense-midnight-black-kr')
  self.assertEqual(d['price'],83110)
  self.assertEqual(d['price_review']['verified_price'],83110)
  self.assertEqual([o['price'] for o in d['price_options']],[74800,69570])
  self.assertEqual([o['price'] for o in validated_price_options(d)], [74800,69570])
  self.assertTrue(d['offer_check_history'])
  for o in d['price_options']:
   self.assertEqual(o['variant'],d['price_variant'])
   self.assertEqual(o['checked_at'],d['price_review']['review_completed_at'])
   self.assertEqual(set(o['conditions']),{'ko','en','zh','ja','es','fr'})
