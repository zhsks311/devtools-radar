import json,unittest,re
from pathlib import Path
import site_i18n
class BillingUnitsTest(unittest.TestCase):
 def test_exact_reviewed_offers_show_units_next_to_price(self):
  rows=sum([json.loads(Path('data/'+f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
  tr=json.loads(Path('data/deal_localizations.json').read_text())
  found=[]
  for row in rows:
   if row['id'] not in site_i18n.BILLING_KIND: continue
   found.append(row['id'])
   for lang in site_i18n.LANGS:
    card=site_i18n.catalogue(lang,[row],tr)
    self.assertRegex(card,r'<div class="price">[^<]+<span class="billing-unit">[^<]+</span></div>')
    self.assertLess(card.index('billing-unit">'),card.index('class="cta"'))
  self.assertEqual(len(found),5)
 def test_no_inferred_units_for_other_products(self):
  self.assertEqual(site_i18n.billing_label({'id':'unknown'},'en'),'')
  self.assertEqual(site_i18n.billing_label({'id':'proton-unknown'},'ko'),'')
