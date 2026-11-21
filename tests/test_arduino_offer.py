import hashlib
import json
from pathlib import Path
import unittest

from site_i18n import catalogue, LANGS
from tools.deal_countries import confirmed_countries, target_countries
from tools.product_links import direct_product_url, publishable_link


OFFER_ID = 'arduino-uno-r4-minima-us'
URL = 'https://store-usa.arduino.cc/products/uno-r4-minima'


class ArduinoOfferTests(unittest.TestCase):
    def test_exact_offer_and_licensed_original(self):
        d = json.loads(Path('data/deals_en.json').read_text())
        items = [card for card in d['feed'] if card['id'] == OFFER_ID]
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual((item['price'], item['currency'], item['link']['url']), (14, 'USD', URL))
        self.assertEqual(item['availability_review']['status'], 'purchase_ui_observed')
        self.assertEqual(item['campaign_end_date'], '2026-11-30')
        self.assertIsNone(item['expires_at'])
        self.assertIsNone(item['original_price'])
        self.assertIsNone(item['discount_pct'])
        self.assertTrue(publishable_link(item))
        self.assertFalse(direct_product_url('https://store-usa.arduino.cc/pages/black-friday'))
        self.assertEqual(item['storefront_country'], 'US')
        self.assertEqual(target_countries(item), ('US',))
        self.assertEqual(confirmed_countries(item), ())
        self.assertEqual(d['categories']['hardware']['items'][0], item)

        media = item['image']
        image = Path(media['path'].lstrip('/')).read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(), media['sha256'])
        self.assertEqual(media['credit'], 'Arduino')
        self.assertEqual(media['license'], 'CC BY-SA 3.0')
        self.assertTrue(media['unmodified'])

        loc = json.loads(Path('data/deal_localizations.json').read_text())
        for lang in LANGS:
            with self.subTest(lang=lang):
                page = catalogue(lang, [item], loc)
                self.assertIn('data-market="US" data-countries="US" data-delivery-confirmed=""', page)
                self.assertIn('USD 14', page)
                self.assertIn(URL, page)
                self.assertIn(media['path'], page)
                self.assertIn(media['credit_url'], page)
                self.assertIn('rel="license noopener">CC BY-SA 3.0', page)
                self.assertNotIn('notice current-savings', page)
        self.assertIn('Product photo · original', catalogue('en', [item], loc))
