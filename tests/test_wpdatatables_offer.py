import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link
from product_visuals import illustration
class WPDataTablesOffer(unittest.TestCase):
 def setUp(self):
  self.d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='wpdatatables-1-code')
 def test_live_price_supersedes_search_extract(self):
  self.assertEqual(self.d['price'],69)
  self.assertTrue(checked_price(self.d));self.assertTrue(publishable_link(self.d))
  self.assertIsNone(self.d['original_price']);self.assertIsNone(self.d['discount_pct'])
  self.assertIn('expired USD 59',self.d['price_review']['evidence'][0]['result'])
 def test_scope_no_invented_country_or_coupon(self):
  self.assertEqual(self.d['purchase_eligibility']['countries_confirmed'],[])
  self.assertEqual(self.d['price_variant'],'1 Code · 5 Domains')
  self.assertNotIn('price_options',self.d)
 def test_localized_purpose_terms_and_original_diagram(self):
  tr=json.loads(Path('data/deal_localizations.json').read_text())[self.d['id']]
  for lang in ('en','ko','zh','ja','es','fr'):
   self.assertTrue(tr[lang]['summary']);self.assertIn('60',tr[lang]['conditions'])
   self.assertIn('<svg',illustration(self.d,lang))
