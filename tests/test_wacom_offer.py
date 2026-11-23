from pathlib import Path
import hashlib
import json
import unittest

from tools.deal_prices import checked_price
from tools.product_links import direct_product_url

class WacomOffer(unittest.TestCase):
    def test_exact_kr_offer_and_image(self):
        deals=json.loads(Path('data/deals.json').read_text())
        row=next(x for x in deals['feed'] if x['id']=='wacom-intuos-small-wired-black-kr')
        self.assertFalse(checked_price(row))
        self.assertEqual(row['availability_review']['status'],'expired')
        self.assertEqual(row['latest_offer_check']['price'],62000)
        self.assertEqual(row['price_review']['verified_price'],55000)
        self.assertEqual(row['price'],55000)
        self.assertIn('K0-CX wired black, new',row['price_variant'])
        self.assertIsNone(row['original_price'])
        self.assertNotIn('expires_at',row)
        self.assertIn('2026-11-22',row['promotion_end_text'])
        self.assertFalse(row['link']['tracked'])
        self.assertEqual(row['purchase_eligibility']['countries_confirmed'],['KR'])
        self.assertFalse(direct_product_url('https://estore.wacom.kr/ko-kr/wacomblackfriday2026'))
        self.assertFalse(direct_product_url('https://estore.wacom.kr/ko-kr/ctl-4100-k0-cx-4.html'))
        self.assertEqual(row['image']['license'],'CC BY-SA 4.0')
        self.assertEqual(row['image']['credit'],'Smitop')
        self.assertEqual(hashlib.sha256(Path(row['image']['path'][1:]).read_bytes()).hexdigest(),row['image']['sha256'])
        loc=json.loads(Path('data/deal_localizations.json').read_text())[row['id']]
        self.assertEqual(set(loc),{'en','ko','zh','ja','es','fr'})
