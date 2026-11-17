import json,unittest
from pathlib import Path
from tools.deal_prices import checked_price
from tools.product_links import publishable_link,direct_product_url
class ActionClipOffer(unittest.TestCase):
 def test_single_mac_and_explicit_limitations(self):
  k='actionclip-individual-lifetime';d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price'],9);self.assertTrue(checked_price(d));self.assertTrue(publishable_link(d));self.assertIsNone(d['original_price'])
  self.assertFalse(direct_product_url('https://actionclip.app/other'));self.assertFalse(direct_product_url('https://actionclip.app/?q=other'))
  self.assertEqual(d['expires_at'],'2026-11-29T23:59:00+00:00');self.assertEqual(d['purchase_eligibility']['countries_confirmed'],[])
  for l,v in json.loads(Path('data/deal_localizations.json').read_text())[k].items():
   self.assertIn('30',v['buying_note']);self.assertIn('API',v['buying_note']);self.assertIn('15',v['conditions'])
 def test_ocr_privacy_is_separate_from_price_observation(self):
  k='actionclip-individual-lifetime';d=next(x for x in json.loads(Path('data/deals_en.json').read_text())['feed'] if x['id']==k)
  self.assertEqual(d['price_review']['review_completed_at'],'2026-11-17T02:56:42.954301+00:00')
  self.assertFalse(d['privacy_review']['local_ocr_uploads_image'])
  self.assertEqual(d['privacy_review']['source_url'],'https://actionclip.app/privacy')
  self.assertIn('anonymous install ID',d['privacy_review']['microsoft_online_ocr_route'])
  for v in json.loads(Path('data/deal_localizations.json').read_text())[k].values():
   for phrase in ['OCR','Microsoft','Azure','Apple','ActionClip']: self.assertIn(phrase,v['buying_note'])
   self.assertIn('15',v['conditions'])
