import json,unittest
from pathlib import Path
from tools.deal_prices import validated_price_options,checked_price
class BelkinPaymentPrice(unittest.TestCase):
 def test_base_and_card_price_remain_distinct(self):
  d=next(x for x in json.loads(Path('data/deals.json').read_text())['feed'] if x['id']=='deal-belkin-100w-gan')
  self.assertEqual(d['price'],39900);self.assertTrue(checked_price(d))
  p=validated_price_options(d)[0]
  self.assertEqual(p['price'],38400);self.assertEqual(p['kind'],'payment')
  self.assertEqual(p['variant'],'WCH025 · 100W');self.assertIn('삼성카드',p['conditions']['ko']);self.assertIn('3만원',p['conditions']['ko'])
  self.assertEqual(d['latest_offer_check']['status'],'seller_text_observed')
  self.assertTrue(any(x['status']=='unverified_current' for x in d['previous_offer_checks']))
