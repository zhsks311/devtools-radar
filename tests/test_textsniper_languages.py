import json,unittest
from pathlib import Path
class TextSniperLanguages(unittest.TestCase):
 def test_os_and_language_scope_not_price_refresh(self):
  k='de0f62d0487f';d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price_review']['review_completed_at'],'2026-11-16T08:57:57.638591+00:00')
  self.assertEqual(d['price'],3.99)
  self.assertEqual(d['language_support_review']['korean_japanese_minimum'],'macOS 13 Ventura')
  self.assertEqual(d['language_support_review']['catalina_languages'],['English'])
  for v in json.loads(Path('data/deal_localizations.json').read_text())[k].values():
   for s in ['10.15','Catalina','13 Ventura','1.6.0']: self.assertIn(s,v['buying_note'])
