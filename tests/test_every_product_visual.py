import json,re,unittest
from pathlib import Path
import site_i18n
from tools.product_links import publishable_link
from tools.deal_candidates import candidate_cards,load_candidates
class EveryProductVisualTest(unittest.TestCase):
 def test_all_catalogue_records_have_safe_purpose_and_visuals_in_six_languages(self):
  rows=sum([json.loads(Path('data/'+f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
  tr=json.loads(Path('data/deal_localizations.json').read_text())
  for lang in site_i18n.LANGS:
   for d in rows:
    field='summary' if publishable_link(d) else 'purpose'
    self.assertTrue(tr[d['id']][lang].get(field), (lang,d['id']))
    card=site_i18n.catalogue(lang,[d],tr)
    self.assertTrue('<svg' in card or '<img' in card,(lang,d['id']))
    self.assertNotIn('<pre',card)
   for card in candidate_cards(lang):
    self.assertIn('<svg',card); self.assertRegex(card,r'class="product-summary">[^<]+</p>')
  self.assertEqual(len(rows)+len(load_candidates()),73)
