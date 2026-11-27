import copy
import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from build import generate_index_html
from buying_guides import guide, PATHS
import site_i18n
import site_seo


class BuyingGuidesTest(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / 'data/deals_en.json'
        self.deal = next(d for d in json.loads(source.read_text())['feed'] if d['id'] == '0deb259ecfd4')
        self.now = datetime.fromisoformat(self.deal['price_review']['review_completed_at']) + timedelta(hours=1)

    def test_current_offer_uses_same_record_and_keeps_license_distinction(self):
        for lang in PATHS:
            with self.subTest(lang=lang):
                page = guide(lang, self.deal, now=self.now)
                self.assertIn('USD 9.99', page)
                self.assertIn(self.deal['link']['url'], page)
                self.assertIn('#product-0deb259ecfd4', page)
                self.assertNotIn('USD 19.77', page)
                self.assertNotIn('USD 32.95', page)
                self.assertNotIn('<del', page)
                self.assertNotIn('aggregateRating', page)
        deal = copy.deepcopy(self.deal)
        deal['price'] = 12
        deal['price_review']['verified_price'] = 12
        self.assertIn('USD 12.00', guide('en', deal, now=self.now))

    def test_unavailable_offers_do_not_appear_in_either_evergreen_guide(self):
        changes = {
            'stale': {},
            'expired-date': {'expires_at': self.now.replace(microsecond=0).isoformat()},
            'expired-status': {'availability_review': {'status': 'expired'}},
            'sold-out': {'availability_review': {'status': 'sold_out'}},
            'held-link': {'link_review': {}},
            'unverified-price': {'price_review': {}},
        }
        for lang in PATHS:
            cases = [('missing', None, self.now)]
            for reason, change in changes.items():
                now = self.now + timedelta(days=2) if reason == 'stale' else self.now
                cases.append((reason, {**self.deal, **change}, now))
            for reason, deal, now in cases:
                with self.subTest(lang=lang, reason=reason):
                    page = guide(lang, deal, now=now)
                    self.assertIn('https://obsproject.com/', page)
                    self.assertIn('https://mirillis.com/purchase-faq', page)
                    self.assertIn('https://mirillis.com/store-action-paysafecard', page)
                    self.assertNotIn('StackSocial', page)
                    self.assertNotIn('USD 9.99', page)
                    self.assertNotIn('#product-0deb259ecfd4', page)

    def test_comparison_hubs_link_to_guides_even_with_empty_deal_catalog(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text(generate_index_html([]), encoding='utf-8')
            site_i18n.write_unified(root, [], {'feed': []}, {'feed': []})
            for lang, hub in [('en', root / 'index.html'), ('ko', root / 'reports/ko/index.html')]:
                self.assertIn(f'lang="{lang}" href="{PATHS[lang]}"', hub.read_text(encoding='utf-8'))
                page = root / PATHS[lang].strip('/') / 'index.html'
                self.assertIn('https://obsproject.com/', page.read_text(encoding='utf-8'))
                self.assertNotIn('#product-', page.read_text(encoding='utf-8'))

    def test_guide_navigation_is_reciprocal_and_truthful(self):
        for path in PATHS.values():
            self.assertEqual(site_seo.alternates_for(path), {**PATHS, 'x-default': PATHS['en']})
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [self.deal], {}, now=self.now)
            self.assertIn('class="buying-guide-link"', page)
            self.assertIn(PATHS.get(lang, PATHS['en']), page)
