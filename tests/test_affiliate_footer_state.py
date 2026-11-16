import unittest,json,copy
from pathlib import Path
import site_i18n
class AffiliateFooterStateTest(unittest.TestCase):
 def test_zero_commission_footer_matches_actual_catalogue(self):
  rows=sum([json.loads(Path('data/'+f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
  translations=json.loads(Path('data/deal_localizations.json').read_text())
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,rows,translations)
   self.assertIn(site_i18n.NO_ACTIVE_AFFILIATES[lang],page)
 def test_tracked_fixture_switches_footer(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed']
  row=copy.deepcopy(next(x for x in rows if site_i18n.publishable_link(x)))
  row['link']['tracked']=True
  page=site_i18n.catalogue('en',[row],{})
  self.assertNotIn(site_i18n.NO_ACTIVE_AFFILIATES['en'],page)
  self.assertIn('Affiliate links may earn a commission.',page)
