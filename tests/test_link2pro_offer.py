import hashlib
import json
import unittest
from pathlib import Path
from tools.product_links import direct_product_url

ROOT = Path(__file__).resolve().parents[1]
DEAL_ID = 'insta360-link-2-pro-kr-graphite-standard'

class Link2ProOfferTest(unittest.TestCase):
    def test_exact_offer_and_editorial_asset(self):
        data = json.loads((ROOT / 'data/deals.json').read_text())
        deal = next(d for d in data['feed'] if d['id'] == DEAL_ID)
        self.assertEqual((deal['price'], deal['currency']), (321000, 'KRW'))
        self.assertEqual(deal['price_variant'], 'Link 2 Pro · graphite black · standard bundle')
        self.assertEqual(deal['purchase_eligibility']['countries_confirmed'], ['KR'])
        self.assertIsNone(deal['discount_pct'])
        self.assertIsNone(deal['original_price'])
        self.assertIsNone(deal['expires_at'])
        self.assertFalse(deal['link']['tracked'])
        self.assertTrue(direct_product_url(deal['link']['url']))
        self.assertFalse(direct_product_url('https://store.insta360.com/kr/campaign/black-friday-deals'))
        image = deal['image']
        self.assertIn('Media use', image['rights_basis'])
        self.assertEqual(hashlib.sha256((ROOT / image['path'].lstrip('/')).read_bytes()).hexdigest(), image['sha256'])
        localized = json.loads((ROOT / 'data/deal_localizations.json').read_text())[DEAL_ID]
        self.assertEqual(set(localized), {'en', 'ko', 'zh', 'ja', 'es', 'fr'})
