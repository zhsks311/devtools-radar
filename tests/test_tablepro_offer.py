import json, unittest
from pathlib import Path
from tools.product_links import direct_product_url
class TableProOfferTest(unittest.TestCase):
 def test_exact_purchase_and_media(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='tablepro-pro-onetime-bf2026')
  self.assertEqual(d['price'],47.4)
  self.assertIsNone(d['original_price'])
  self.assertEqual(d['expires_at'],'2026-12-01T08:00:00+00:00')
  self.assertTrue(direct_product_url(d['link']['url']))
  self.assertEqual(d['image']['kind'],'official_app_icon')
  self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  self.assertTrue(Path('assets/deals/tablepro-icon.png').is_file())
  l=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(set(l),{'ko','en','zh','ja','es','fr'})
  for v in l.values():self.assertTrue(v['summary']);self.assertTrue(v['conditions'])
