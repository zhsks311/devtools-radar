import hashlib
import json
import unittest
from pathlib import Path

import site_i18n
from tools.product_links import direct_product_url, publishable_link

class Go3sOfferTest(unittest.TestCase):
    def test_selected_variant_and_asset(self):
        d, = (d for d in json.loads(Path('data/deals.json').read_text())['feed'] if d['id'] == 'insta360-go-3s-kr-128gb-black')
        self.assertEqual((d['price'], d['price_review']['verified_price']), (359000, 359000))
        self.assertIn('128GB', d['price_variant'])
        self.assertIn('449,000', d['price_review']['evidence'][0]['result'])
        self.assertEqual(d['purchase_eligibility']['countries_confirmed'], ['KR'])
        self.assertIsNone(d['discount_pct'])
        self.assertIsNone(d['original_price'])
        self.assertIsNone(d['expires_at'])
        self.assertTrue(publishable_link(d))
        self.assertEqual(d['link']['url'], 'https://store.insta360.com/kr/product/go-3s')
        self.assertFalse(direct_product_url('https://store.insta360.com/kr/product/go-3sx'))
        self.assertFalse(direct_product_url('https://store.insta360.com/kr/product/go-3s?query=black'))
        local = json.loads(Path('data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            self.assertIn('359', local[d['id']][lang]['conditions'])
            self.assertIn('449', local[d['id']][lang]['conditions'])
            card = site_i18n.catalogue(lang, [d], local)
            self.assertIn('insta360-go-3s-black.webp', card)
            self.assertIn('JettM9104', card)
        im = d['image']
        self.assertEqual(im['license_url'], 'https://creativecommons.org/licenses/by-sa/4.0/')
        image = Path(im['path'].lstrip('/')).read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(), im['sha256'])
        self.assertNotIn(b'EXIF', image)
