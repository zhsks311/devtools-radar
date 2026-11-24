from copy import deepcopy
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import unittest

from tools.deal_prices import seller_price_reference
from tools.product_links import direct_product_url, publishable_link

ROOT = Path(__file__).resolve().parents[1]
ID = 'logitech-g304-lightspeed-black-kr-gfesta'
URL = 'https://www.logitech-gamingstore.com/shop/list/item/index?no=20'


class LogitechG304OfferTests(unittest.TestCase):
    def setUp(self):
        self.deal = next(d for d in json.loads((ROOT / 'data/deals.json').read_text())['feed'] if d['id'] == ID)

    def test_exact_product_link_only(self):
        self.assertEqual(self.deal['link']['url'], URL)
        self.assertTrue(publishable_link(self.deal))
        for url in (URL.replace('20', '25'), URL + '&no=20', URL + '&no=25', URL + '#other',
                    URL.replace('/item/index', '/index'), URL + '&keyword=mouse'):
            self.assertFalse(direct_product_url(url), url)

    def test_evidence_expires_and_does_not_cross_variants(self):
        when = datetime.fromisoformat(self.deal['link_review']['checked_at'])
        self.assertIsNotNone(seller_price_reference(self.deal, now=when + timedelta(minutes=1)))
        self.assertIsNone(seller_price_reference(self.deal, now=when + timedelta(hours=25)))
        other = deepcopy(self.deal)
        other['price_variant'] = 'G304 LIGHTSPEED · White'
        self.assertIsNone(seller_price_reference(other, now=when + timedelta(minutes=1)))
        self.assertIsNone(self.deal['expires_at'])
        self.assertEqual(self.deal['campaign_end_date'], '2026-12-01')

    def test_real_image_attributed_and_captioned(self):
        visual = self.deal['image']
        self.assertEqual(visual['license'], 'CC BY-SA 4.0')
        self.assertEqual(hashlib.sha256((ROOT / visual['path'].lstrip('/')).read_bytes()).hexdigest(), visual['sha256'])
        self.assertEqual(set(visual['notes']), {'en', 'ko', 'zh', 'ja', 'es', 'fr'})
        for caption in visual['notes'].values():
            self.assertIn('G305', caption)
        self.assertEqual(self.deal['purchase_eligibility']['countries_confirmed'], ['KR'])
