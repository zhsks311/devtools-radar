import json,unittest
from pathlib import Path
from tools.product_links import direct_product_url,publishable_link
from tools.deal_prices import checked_price,discount_percent
from tools.deal_countries import confirmed_countries
import site_i18n as i
R=Path(__file__).resolve().parents[1]
class NewReviewedOffersTests(unittest.TestCase):
 def test_exact_routes_not_search_or_questions(self):
  for url in ['https://appsumo.com/products/otter-ab/','https://trip.coupang.com/m/tp/products/10000011273690?vendorItemId=70000236938095&itemId=20002152486536']:self.assertTrue(direct_product_url(url))
  for url in ['https://appsumo.com/products/otter-ab/questions/','https://appsumo.com/search?q=otter','https://appsumo.com/products/otter-ab/?search=foo','https://trip.coupang.com/m/tp/products/10000011273690','https://trip.coupang.com/m/tp/products/10000011273690?vendorItemId=1&vendorItemId=2&itemId=3']:self.assertFalse(direct_product_url(url))
 def test_new_offers_preserve_scope_no_discount_no_country_guess(self):
  feed=sum([json.loads((R/f'data/{n}.json').read_text())['feed'] for n in ('deals','deals_en')],[]);tr=json.loads((R/'data/deal_localizations.json').read_text())
  expected={'seoagent-tier-1':69,'moonitor-solo':45.9,'otter-ab-tier-1':67.15,'deal-oliveyoung-gift-card-20k':19600}
  for id,price in expected.items():
   matches=[d for d in feed if d['id']==id];self.assertEqual(len(matches),1);d=matches[0]
   self.assertEqual(d['price'],price);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(discount_percent(d));self.assertEqual(confirmed_countries(d),())
   for lang in i.LANGS:
    self.assertTrue(tr[id][lang]['conditions']);page=i.catalogue(lang,[d],tr);self.assertIn('class="cta"',page);self.assertNotIn('class="notice link-held"',page)
  self.assertIn('AI article writing/editing excluded',tr['seoagent-tier-1']['en']['conditions'])
  self.assertIn('not covered by We Got Your Back',tr['moonitor-solo']['en']['conditions'])
  self.assertIn('Not Otter.ai',tr['otter-ab-tier-1']['en']['conditions'])
