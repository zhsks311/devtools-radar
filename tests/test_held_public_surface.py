"""Internal rejected evidence must not leak through collapsed public details."""
import copy,json,re,unittest
from pathlib import Path
import site_i18n as i
from tools.product_links import publishable_link
ROOT=Path(__file__).resolve().parents[1]
class HeldPublicSurfaceTests(unittest.TestCase):
 def setUp(self):
  self.feeds=json.loads((ROOT/'data/deals.json').read_text())['feed']
  self.tr=json.loads((ROOT/'data/deal_localizations.json').read_text())
 def test_all_languages_hide_raw_held_records_without_mutation(self):
  held=[d for d in self.feeds if not publishable_link(d)]
  self.assertTrue(held)
  before=copy.deepcopy(held)
  for lang in i.LANGS:
   page=i.catalogue(lang,held,self.tr)
   for d in held:
    card=re.search(r'<article[^>]*data-id="'+re.escape(d['id'])+r'".*?</article>',page,re.S).group()
    for bad in ('<pre','<details','href=', 'seller_url', '6W', '1,000원 안팎','가성비 종결'):
     self.assertNotIn(bad,card)
    self.assertIn(i.SOLD_OUT_LABEL[lang] if (d.get("availability_review") or {}).get("status")=="sold_out" else i.HELD_SUMMARY[lang],card)
    self.assertIn(i.PRICE_RECORDED[lang],card)
  self.assertEqual(before,held)
 def test_nested_rejected_urls_and_ads_cannot_reappear(self):
  d=copy.deepcopy(next(d for d in self.feeds if not publishable_link(d)))
  marker='UNVERIFIED_AD_DO_NOT_PUBLISH'
  d['briefing']=[marker];d['source']={'url':'https://example.com/search?q='+marker}
  d['shipping']=marker;d['price_review']['evidence']=[{'url':'https://example.com/search?q='+marker}]
  tr={d['id']:{lang:{'product':'Archived product','summary':marker,'conditions':marker} for lang in i.LANGS}}
  for lang in i.LANGS:self.assertNotIn(marker,i.catalogue(lang,[d],tr))

 def test_active_cards_keep_purchase_and_evidence_sections(self):
  feeds=json.loads((ROOT/'data/deals_en.json').read_text())['feed']
  tr=json.loads((ROOT/'data/deal_localizations.json').read_text())
  active=[d for d in feeds if publishable_link(d)]
  self.assertTrue(active)
  for lang in i.LANGS:
   page=i.catalogue(lang,active,tr)
   self.assertEqual(page.count('class="cta"'),len(active))
   self.assertEqual(page.count('<pre class="original"'),0)
   self.assertEqual(page.count('class="price-evidence"'),len(active))
   self.assertNotIn('class="notice link-held"',page)
