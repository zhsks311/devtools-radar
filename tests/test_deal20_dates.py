import json,unittest
from pathlib import Path
import site_i18n as i
R=Path(__file__).resolve().parents[1]
class CouponDatesTests(unittest.TestCase):
 def test_five_cards_keep_date_only_campaign_and_unverified_checkout(self):
  ids={'2f57dcdf2174':24.97,'3b4097687c74':14.97,'3b4c5d317572':23.97,'mail-backup-x-individual-v2':49.99,'babbel-lifetime-all-languages':249}
  feed=json.loads((R/'data/deals_en.json').read_text())['feed'];tr=json.loads((R/'data/deal_localizations.json').read_text())
  for d in feed:
   if d['id'] not in ids:continue
   self.assertEqual(d['price'],ids[d['id']]); c=d['price_review']['coupon']
   self.assertEqual(c['valid_through_date'],'2026-11-15');self.assertIsNone(c['timezone']);self.assertIsNone(c['ends_at']);self.assertFalse(c['checkout_verified'])
   self.assertTrue(c['exclusions_apply']);self.assertIn('/collections/',c['source_url']);self.assertNotIn('Expiry unknown.',d['disclosure'])
   for lang in i.LANGS:
    self.assertNotIn('DEAL20',tr[d['id']][lang]['conditions']); self.assertNotIn('US$24',tr[d['id']][lang]['conditions'])
