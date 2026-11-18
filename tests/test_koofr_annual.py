import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price,discount_percent
from tools.product_links import publishable_link,direct_product_url
class KoofrAnnual(unittest.TestCase):
 def test_separate_annual_offer_and_tax_limits(self):
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='koofr-1tb-annual-bf2026')
  self.assertEqual(d['price'],44.26);self.assertEqual(d['currency'],'EUR');self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(discount_percent(d));self.assertIsNone(d['expires_at'])
  self.assertFalse(d['price_review']['coupon']['checkout_verified']);self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  loc=json.loads(Path('data/deal_localizations.json').read_text())[d['id']]
  self.assertEqual(set(loc),{'ko','en','zh','ja','es','fr'})
  for v in loc.values():self.assertIn('BF2026',v['conditions'])
 def test_not_generic_koofr_urls(self):
  for u in ['https://koofr.eu/','https://koofr.eu/blog/','https://koofr.eu/black-friday/?q=1tb']:self.assertFalse(direct_product_url(u))

 def test_storage_image_caption_is_localized(self):
  from product_visuals import product_media,STORAGE_PREVIEW_LABEL
  d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']=='koofr-1tb-annual-bf2026')
  for lang in STORAGE_PREVIEW_LABEL:
   self.assertIn(STORAGE_PREVIEW_LABEL[lang],product_media(d,lang,d['product']))
