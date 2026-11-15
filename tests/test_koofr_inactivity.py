import json,unittest
from pathlib import Path
import site_i18n
class KoofrInactivityTest(unittest.TestCase):
 def test_contact_is_not_a_fixed_deletion_deadline(self):
  root=Path(__file__).resolve().parents[1]
  d=next(d for d in json.loads((root/'data/deals_en.json').read_text())['feed'] if d['id']=='e30c9a510928')
  loc=json.loads((root/'data/deal_localizations.json').read_text())
  self.assertIn('contact',d['service_terms']['inactivity'])
  self.assertIn('No precise automatic deletion deadline',d['service_terms']['inactivity'])
  self.assertIn('do not say',loc[d['id']]['en']['conditions'])
  for lang in site_i18n.LANGS:
   self.assertIn('2',loc[d['id']][lang]['conditions'])
   page=site_i18n.catalogue(lang,[d],loc)
   self.assertIn('class="service-terms-source" href="https://koofr.eu/tos/"',page)
