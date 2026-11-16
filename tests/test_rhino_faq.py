import unittest,json
from pathlib import Path
class RhinoFaq(unittest.TestCase):
 def test_language_and_network_limits(self):
  data=json.loads(Path('data/deals_en.json').read_text())
  d=next(d for d in data['feed'] if d['id']=='rhino-voice-1-mac')
  self.assertEqual(d['language_privacy_review']['default_language'],'English-optimized')
  self.assertEqual(d['language_privacy_review']['permissions'],['Microphone','Accessibility'])
  loc=json.loads(Path('data/deal_localizations.json').read_text())['rhino-voice-1-mac']
  for l in ['ko','en','zh','ja','es','fr']: self.assertTrue(loc[l]['buying_note'])
  self.assertIn('한국어 정확도',loc['ko']['buying_note'])
  self.assertIn('2026-11-16T17:06:',d['price_review']['review_completed_at'])
