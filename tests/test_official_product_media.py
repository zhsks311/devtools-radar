import json, unittest
from pathlib import Path
from product_visuals import product_media
import site_i18n
class OfficialProductMediaTest(unittest.TestCase):
 def test_proton_screenshots_have_permissions_and_all_locale_credit(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed']
  for d in [x for x in rows if x['id'].startswith('proton-')]:
   self.assertEqual(d['image']['kind'],'official_product_ui')
   self.assertIn('permits free use',d['image']['rights_basis'])
   self.assertTrue(Path(d['image']['path'].lstrip('/')).is_file())
   for lang in site_i18n.LANGS:
    s=product_media(d,lang,d['product'])
    self.assertIn('<img',s);self.assertNotIn('<svg',s);self.assertIn('https://proton.me/media/kit',s)
    self.assertIn('image-error',s)
 def test_unsafe_or_missing_file_fails_closed(self):
  for path in ['/assets/deals/missing.webp','https://example.com/x.png','/assets/deals/../../secret.png']:
   s=product_media({'image':{'path':path,'credit_url':'https://example.com'}},'en','x')
   self.assertNotIn('<img',s)
