from hashlib import sha256
import json
from pathlib import Path
import unittest

import site_i18n
from tools.deal_countries import confirmed_countries
from tools.deal_prices import checked_price, discount_percent
from tools.product_links import direct_product_url


class PS5AccessOfferTests(unittest.TestCase):
    def test_exact_kr_product_and_licensed_example(self):
        ident = 'ps5-access-controller-cfi-zac1-kr'
        offer = next(d for d in json.loads(Path('data/deals.json').read_text())['feed'] if d['id'] == ident)
        translations = json.loads(Path('data/deal_localizations.json').read_text())
        url = offer['link']['url']
        self.assertTrue(checked_price(offer))
        self.assertFalse(direct_product_url(url.replace('/131/', '/132/')))
        self.assertFalse(direct_product_url('https://www.playshop.co.kr/'))
        self.assertEqual((offer['currency'], offer['price']), ('KRW', 104700))
        self.assertIsNone(discount_percent(offer))
        self.assertEqual(confirmed_countries(offer), ('KR',))
        self.assertIsNone(offer['expires_at'])
        self.assertFalse(offer['link']['tracked'])
        img = offer['image']
        self.assertEqual(sha256(Path(img['path'].lstrip('/')).read_bytes()).hexdigest(), img['sha256'])
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [offer], translations)
            self.assertIn(img['path'], page)
            self.assertIn(img['notes'][lang], page)
            self.assertIn('>CC BY-SA 4.0</a>', page)
            self.assertIn('>InclusiveGameLab</a>', page)
            self.assertIn('class="cta"', page)
            self.assertIn('104,700', page)
            self.assertNotIn('data-expires-at=', page)
