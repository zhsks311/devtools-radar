import json,unittest
from pathlib import Path
import site_i18n
class NoCodeAlternativeTest(unittest.TestCase):
 def test_free_plan_limits_and_sources_survive_six_languages(self):
  data=json.loads(Path('data/deals_en.json').read_text()); loc=json.loads(Path('data/deal_localizations.json').read_text())
  d=next(x for x in data['feed'] if x['id']=='nocodebackend-tier-1')
  self.assertEqual(d['alternative_review']['free_plan'],{'monthly_usd':0,'active_projects':2,'database_mb':500,'inactivity_pause_days':7})
  self.assertEqual(d,next(x for x in data['categories']['cloud']['items'] if x['id']==d['id']))
  for lang in site_i18n.LANGS:
   note=loc[d['id']][lang]['buying_note']; self.assertIn('Supabase',note);self.assertIn('500',note);self.assertIn('Postgres',note)
   page=site_i18n.catalogue(lang,[d],loc)
   self.assertIn('https://supabase.com/pricing',page)
   self.assertNotIn('data breach',note)
