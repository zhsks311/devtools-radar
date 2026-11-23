import copy,json,re,unittest
from pathlib import Path
import site_i18n
from tools.product_links import publishable_link
class BuyerCopyTest(unittest.TestCase):
 def test_audit_details_collapsed_and_caveats_visible(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed']
  d=next(x for x in rows if publishable_link(x))
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,[d],{})
   card=re.search(r'<article class="card".*?</article>',page,re.S).group()
   self.assertIn('<details class="price-evidence"><summary>'+site_i18n.PRICE_DETAILS[lang],card)
   self.assertNotIn(site_i18n.PRICE_CURRENT[lang],card)
   self.assertIn(site_i18n.REVIEW_DATE[lang],card)
   self.assertIn('class="product-title"',card)
   self.assertIn('class="cta"',card)
   self.assertLess(card.index('class="cta"'),card.index('<details class="purchase-details">'))
   self.assertLess(card.index('class="cta"'),card.index('<details class="price-evidence">'))
   self.assertNotIn('<pre',card)
   self.assertNotIn('purchase_eligibility',card)
   self.assertTrue('<svg' in card or '<img' in card)
 def test_unknowns_are_not_repeated_labels(self):
  page=site_i18n.catalogue('ko',json.loads(Path('data/deals_en.json').read_text())['feed'],{})
  self.assertNotIn('판매처 국가: 판매처 국가 미분류',page)
  self.assertNotIn('배송·사용 가능 국가 (근거 확인): 배송·사용 가능 국가 미확인',page)
  self.assertNotIn(site_i18n.DESTINATION_NOTE['ko'],page)
