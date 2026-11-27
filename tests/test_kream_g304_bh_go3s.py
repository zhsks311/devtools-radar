import json
import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

import site_i18n
from tools.deal_countries import confirmed_countries
from tools.deal_prices import seller_price_reference, validated_price_options
from tools.product_links import direct_product_url


class KoreaAndUsDealTests(unittest.TestCase):
    def test_exact_variants_market_price_and_image(self):
        for file, ident, market, price, reference, image in (
            ('deals.json', 'logitech-g304-black-pouch-kream-kr', 'KR', 34900, 59900, 'logitech-g304-lightspeed-black.webp'),
            ('deals_en.json', 'insta360-go-3s-us-128gb-midnight-bh', 'US', 299.99, 379.99, 'insta360-go-3s-black.webp'),
        ):
            with self.subTest(ident=ident):
                rows = json.loads(Path('data', file).read_text())['feed']
                row, = (r for r in rows if r['id'] == ident)
                url = row['link']['url']
                self.assertTrue(direct_product_url(url))
                self.assertFalse(direct_product_url(url + '?query=other'))
                self.assertEqual(confirmed_countries(row), (market,))
                self.assertEqual(row['price'], price)
                when = datetime.fromisoformat(row['link_review']['checked_at'])
                self.assertEqual(seller_price_reference(row, now=when)['price'], Decimal(str(reference)))
                self.assertIsNone(seller_price_reference(row, now=when + timedelta(hours=25)))
                self.assertEqual(row['image']['license'], 'CC BY-SA 4.0')
                self.assertTrue(row['image']['path'].endswith(image))
                options = validated_price_options(row)
                self.assertEqual([o['price'] for o in options], [32500] if market == 'KR' else [])
                local = json.loads(Path('data/deal_localizations.json').read_text())
                for lang in site_i18n.LANGS:
                    page = site_i18n.catalogue(lang, [row], local, now=when)
                    self.assertIn(url, page)
                    self.assertIn(image, page)
                    self.assertIn('seller-price-reference current-savings', page)
