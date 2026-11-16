import html,json,re,unittest
from pathlib import Path
import site_i18n
class ProductUseSearchTest(unittest.TestCase):
 def test_reviewed_use_searchable_across_languages(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed']
  tr=json.loads(Path('data/deal_localizations.json').read_text())
  item=next(d for d in rows if d['id']=='moonitor-solo')
  for lang in site_i18n.LANGS:
   page=site_i18n.catalogue(lang,[item],tr)
   searchable=html.unescape(re.search(r'data-search="([^"]+)"',page).group(1))
   for language in site_i18n.LANGS:
    self.assertIn(tr[item['id']][language]['summary'],searchable)
 def test_held_old_claim_never_becomes_searchable(self):
  item={'id':'held-test','product':'Safe name','category':'hardware','briefing':['OLD UNSUPPORTED CLAIM']}
  tr={'held-test':{'en':{'product':'Safe name','summary':'OLD UNSUPPORTED CLAIM','purpose':'Keyboard for typing'}}}
  page=site_i18n.catalogue('en',[item],tr)
  self.assertNotIn('OLD UNSUPPORTED CLAIM',page)
  self.assertIn('Keyboard for typing',page)
 def test_supporting_visuals_leave_room_for_product_information(self):
  self.assertIn('width:100%;height:88px',site_i18n.CSS)
  self.assertIn('min-height:110px',site_i18n.CSS)
  self.assertNotIn('width:100%;height:150px',site_i18n.CSS)
