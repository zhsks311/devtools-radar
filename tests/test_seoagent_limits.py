import unittest,json
from pathlib import Path
class SEOAgentLimitsTest(unittest.TestCase):
 def test_quantity_does_not_invent_reset_period(self):
  root=Path(__file__).resolve().parents[1];d=next(d for d in json.loads((root/'data/deals_en.json').read_text())['feed'] if d['id']=='seoagent-tier-1');l=d['price_review']['limits']
  self.assertEqual((l['keyword_research_runs'],l['ai_visibility_questions'],l['tracked_keywords']),(5,4,50));self.assertIsNone(l['reset_period']);self.assertEqual(l['credits_per_month'],1000)
  loc=json.loads((root/'data/deal_localizations.json').read_text())['seoagent-tier-1']
  for lang in ['en','ko','zh','ja','es','fr']:
   for n in ['5','4','50']:self.assertIn(n,loc[lang]['conditions'])
  self.assertIn('not stated',loc['en']['conditions']);self.assertIn('명시되지 않았',loc['ko']['conditions'])
