import json
import html
import re
import unittest
from pathlib import Path

import site_i18n
from tools.deal_countries import confirmed_countries
from tools.deal_prices import checked_price, discount_percent
from tools.product_links import direct_product_url, publishable_link


ROOT = Path(__file__).resolve().parents[1]
IDENT = 'nocodebackend-tier-1'
URL = 'https://appsumo.com/products/nocodebackend/'


class NoCodeBackendOfferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / 'data/deals_en.json').read_text())
        cls.deal = next(d for d in cls.payload['feed'] if d['id'] == IDENT)
        cls.translations = json.loads((ROOT / 'data/deal_localizations.json').read_text())

    def test_exact_seller_price_not_discount_or_country_evidence(self):
        d = self.deal
        self.assertEqual(sum(p['id'] == IDENT for p in self.payload['feed']), 1)
        self.assertEqual(d['link']['url'], URL)
        self.assertTrue(direct_product_url(URL))
        self.assertTrue(publishable_link(d))
        self.assertEqual(d['price'], 79)
        self.assertEqual(d['currency'], 'USD')
        self.assertTrue(checked_price(d))
        self.assertIsNone(d['original_price'])
        self.assertIsNone(d['discount_pct'])
        self.assertIsNone(discount_percent(d))
        self.assertFalse(d['link']['tracked'])
        self.assertIsNone(d['storefront_country'])
        self.assertEqual(confirmed_countries(d), ())
        self.assertIn('not tested', d['purchase_eligibility']['payment'])

    def test_current_tier_limits_not_marketing_or_legacy_limits(self):
        condition = self.translations[IDENT]['en']['conditions']
        for required in (
            'New users only', 'existing accounts cannot redeem or upgrade',
            '2 databases, 25,000 records each', '2 Prehooks',
            'MCP, built-in user authentication, user invites, Smart AI credits, webhooks, custom domains and database snapshots are excluded',
            'future Starter Plan updates', 'activate within 60 days',
            'refunds within 60 days of purchase', 'no We Got Your Back guarantee',
            'Extra record capacity costs more', 'final checkout are unverified',
        ):
            self.assertIn(required, condition)
        self.assertNotIn('50,000', condition)
        evidence = ' '.join(self.deal['price_review']['limitations'])
        self.assertIn('older August', evidence)
        self.assertIn('25,000-per-database', evidence)
        self.assertIn('688 / 89%', evidence)

    def test_six_languages_render_limits_and_actual_product_link(self):
        expected = {
            'en': ('New users only', 'are excluded', 'unverified'),
            'ko': ('신규 사용자만', '제외됩니다', '미확인'),
            'zh': ('仅限新用户', '不含MCP', '未核实'),
            'ja': ('新規ユーザー限定', '対象外', '未確認'),
            'es': ('Solo nuevos usuarios', 'Excluye MCP', 'sin verificar'),
            'fr': ('Nouveaux utilisateurs uniquement', 'sont exclus', 'non vérifiés'),
        }
        for lang, markers in expected.items():
            with self.subTest(lang=lang):
                local = self.translations[IDENT][lang]
                page = site_i18n.catalogue(lang, [self.deal], self.translations)
                display = html.unescape(re.sub(r'<pre class="original".*?</pre>', '', page, flags=re.S))
                self.assertIn('class="cta"', page)
                self.assertIn(URL, page)
                for marker in markers:
                    self.assertIn(marker, local['conditions'])
                    self.assertIn(marker, page)
                for term in ('MCP', 'Prehooks', 'Smart AI', 'Starter Plan', '60', 'We Got Your Back'):
                    self.assertIn(term, local['conditions'])
                self.assertIn(local['buying_note'], display)
                self.assertNotIn('89%', display)
                self.assertNotIn('$688', display)

    def test_category_copy_and_feed_count_are_consistent(self):
        copy = next(d for d in self.payload['categories']['cloud']['items'] if d['id'] == IDENT)
        self.assertEqual(copy, self.deal)
        self.assertEqual(self.payload['stats']['feed'], len(self.payload['feed']))


if __name__ == '__main__':
    unittest.main()
