from datetime import datetime,timedelta
from hashlib import sha256
import json
from pathlib import Path
import re
import unittest
import site_i18n
from tools.deal_prices import checked_price,seller_price_reference,validated_price_options
from tools.product_links import direct_product_url

class PasteAnnualOfferTest(unittest.TestCase):
    def test_exact_annual_price_and_conditional_first_year(self):
        d,=(d for d in json.loads(Path('data/deals_en.json').read_text())['feed']
            if d['id']=='paste-annual-first-year-bf2026')
        self.assertTrue(checked_price(d))
        self.assertTrue(direct_product_url(d['link']['url']))
        self.assertFalse(direct_product_url('https://pasteapp.io/black-friday-2025'))
        self.assertFalse(direct_product_url('https://pasteapp.io/black-friday-2026?q=annual'))
        self.assertEqual(d['price'],29.99)
        self.assertEqual([x['price'] for x in validated_price_options(d)],[14.99])
        self.assertIsNone(seller_price_reference(d))
        self.assertIsNone(d['expires_at'])
        self.assertFalse(d['purchase_eligibility']['countries_confirmed'])
        im=d['image']
        self.assertEqual(sha256(Path(im['path'][1:]).read_bytes()).hexdigest(),im['sha256'])
        loc=json.loads(Path('data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            html=site_i18n.catalogue(lang,[d],loc)
            card=re.search(r'<article.*?</article>',html,re.S)[0]
            self.assertIn('<div class="price">USD 29.99</div>',card)
            self.assertIn('<p class="conditional-price">USD 14.99</p>',card)
            self.assertIn('BLACKFRIDAY2026',card)
            self.assertIn('Paste media kit',card)
            self.assertNotIn('<s>',card)
            self.assertNotIn('data-expires-at=',card)
