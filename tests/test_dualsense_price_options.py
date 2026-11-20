import json,unittest
from pathlib import Path
from tools.deal_prices import validated_price_options
class DualSensePrices(unittest.TestCase):
 def test_main_price_excludes_coupon_and_card(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='ps5-dualsense-midnight-black-kr')
  from site_i18n import billing_label
  for lang in ['ko','en','zh','ja','es','fr']: self.assertEqual(billing_label(d,lang),'')
  self.assertEqual(d['price'],87500)
  self.assertEqual(d['price_review']['verified_price'],87500)
  self.assertEqual([o['price'] for o in d['price_options']],[86000])
  self.assertEqual([o['price'] for o in validated_price_options(d)], [86000])
  self.assertTrue(any('69,570' in x['evidence'] for x in d['offer_check_history']))
  self.assertEqual(d['price_options'][0]['kind'],'payment')
  self.assertIn('Hana Card',d['price_options'][0]['conditions']['en'])
  for o in d['price_options']:
   self.assertEqual(o['variant'],d['price_variant'])
   self.assertEqual(o['checked_at'],d['price_review']['review_completed_at'])
   self.assertEqual(set(o['conditions']),{'ko','en','zh','ja','es','fr'})
