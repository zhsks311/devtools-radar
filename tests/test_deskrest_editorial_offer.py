from hashlib import sha256
import json
from pathlib import Path
import re
import unittest

import site_i18n
from tools.deal_prices import checked_price, discount_percent
from tools.product_links import direct_product_url


class DeskrestEditorialOfferTests(unittest.TestCase):
    def test_exact_seller_one_mac_and_official_editorial_screenshot(self):
        data = json.loads(Path('data/deals_en.json').read_text())
        rows = [d for d in data['feed'] if d['id'] == 'deskrest-1-mac-lifetime']
        self.assertEqual(len(rows), 1)
        offer = rows[0]
        self.assertTrue(checked_price(offer))
        self.assertFalse(direct_product_url('https://deskrest.com/'))
        self.assertEqual(offer['price'], 5)
        self.assertFalse(offer['link']['tracked'])
        self.assertIsNone(offer['expires_at'])
        self.assertIsNone(discount_percent(offer))
        self.assertFalse(offer['purchase_eligibility']['countries_confirmed'])
        photo = offer['image']
        raster = Path(photo['path'].lstrip('/')).read_bytes()
        self.assertEqual(sha256(raster).hexdigest(), photo['sha256'])
        tr = json.loads(Path('data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [offer], tr)
            self.assertIn('https://deskrest.com/presskit/images/',page)
            self.assertIn('USD 5</div>',page)
            self.assertNotIn('<s>',page)

    def test_localized_access_setup_does_not_replace_photo_terms(self):
        ident = 'ps5-access-controller-cfi-zac1-kr'
        offer = next(d for d in json.loads(Path('data/deals.json').read_text())['feed'] if d['id']==ident)
        translations = json.loads(Path('data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [offer], translations)
            details, = re.findall(r'<details class="purchase-details">.*?</details>', page, re.S)
            self.assertIn(offer['service_terms']['setup_urls'][lang], details)
            self.assertIn('DualSense', details)
            self.assertIn(offer['image']['notes'][lang],page)
            self.assertIn('104,700',page)
