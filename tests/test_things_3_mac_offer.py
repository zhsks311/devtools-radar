import hashlib
import json
import unittest
from datetime import datetime
from pathlib import Path

import site_i18n
from tools.deal_countries import confirmed_countries, target_countries
from tools.deal_prices import seller_price_reference
from tools.product_links import publishable_link


class ThingsMacOfferTest(unittest.TestCase):
    def test_korean_mac_app_not_other_platforms_or_inferred_price(self):
        rows = json.loads(Path('data/deals.json').read_text())['feed']
        ident = 'things-3-mac-kr-bf2026'
        offer, = (row for row in rows if row['id'] == ident)
        self.assertTrue(publishable_link(offer))
        self.assertEqual(offer['link']['url'], 'https://apps.apple.com/kr/app/things-3/id904280696?mt=12')
        self.assertEqual((offer['price'], offer['currency']), (53900, 'KRW'))
        self.assertEqual(target_countries(offer), ('KR',))
        self.assertEqual(confirmed_countries(offer), ())
        self.assertEqual(offer['campaign_end_date'], '2026-11-30')
        self.assertIsNone(offer['expires_at'])
        self.assertIsNone(offer['original_price'])
        self.assertIsNone(offer['discount_pct'])
        when = datetime.fromisoformat(offer['link_review']['checked_at'])
        self.assertIsNone(seller_price_reference(offer, now=when))
        image = offer['image']
        self.assertEqual(image['kind'], 'official_product_ui')
        self.assertEqual(hashlib.sha256(Path(image['path'].lstrip('/')).read_bytes()).hexdigest(), image['sha256'])
        local = json.loads(Path('data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [offer], local, now=when)
            self.assertIn(offer['link']['url'], page)
            self.assertIn(image['path'], page)
            self.assertNotIn('seller-price-reference current-savings', page)
