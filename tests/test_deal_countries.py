import copy
import json
import shutil
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path
import site_i18n
from tools.deal_countries import confirmed_countries, storefront_country, validate_deal_countries
from tools.product_links import publishable_link

ROOT = Path(__file__).resolve().parents[1]


class FilterParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.area = ''; self.select = None
        self.cards = []; self.archived = []; self.selects = {}; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id') in ('active-products', 'held-products'): self.area = a['id']
        if tag == 'article' and 'card' in a.get('class', '').split():
            (self.cards if self.area == 'active-products' else self.archived).append({
                'id': a['data-id'], 'kind': a.get('data-kind', 'verified'), 'search': a['data-search'], 'market': a['data-market'],
                'countries': a['data-countries'], 'category': a['data-category']})
        if tag == 'select':
            self.select = a['id']; self.selects[self.select] = []
        if tag == 'option' and self.select:
            self.selects[self.select].append(a['value'])
        if tag == 'a' and a.get('class') == 'lang': self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag == 'select': self.select = None


class CountryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed = sum([json.loads((ROOT / 'data' / name).read_text())['feed']
                        for name in ('deals.json', 'deals_en.json')], [])
        cls.tr = json.loads((ROOT / 'data/deal_localizations.json').read_text())
    def test_storefront_does_not_grant_country_eligibility(self):
        self.assertEqual(validate_deal_countries(self.feed), [])
        for d in self.feed:
            self.assertEqual(confirmed_countries(d), ('AU',) if d['id'] == '43ca41d03daa' else ())
        d = {'region': 'kr', 'category': 'china', 'currency': 'USD', 'target': 'en'}
        self.assertEqual(confirmed_countries(d), ())
        self.assertEqual(storefront_country(d), 'unknown')
    def test_multiple_countries_and_evidence_fail_closed(self):
        d = copy.deepcopy(next(d for d in self.feed if d['id'] == '43ca41d03daa'))
        d['purchase_eligibility']['countries_confirmed'] = ['AU', 'NZ', 'AU']
        self.assertEqual(confirmed_countries(d), ('AU', 'NZ'))
        for key, value in [('status', 'unverified'), ('evidence_url', None), ('delivery', ''),
                           ('checked_at', '2999-01-01'), ('checked_at', 'yesterday'),
                           ('countries_confirmed', ['GLOBAL']), ('countries_confirmed', ['ZZ']),
                           ('countries_confirmed', 'AU')]:
            bad = copy.deepcopy(d); bad['purchase_eligibility'][key] = value
            with self.subTest(key=key, value=value):
                self.assertEqual(confirmed_countries(bad), ())
                self.assertTrue(validate_deal_countries([bad]))
    def test_categories_and_country_data_same_in_all_languages(self):
        for lang in site_i18n.LANGS:
            p = FilterParser(); p.feed(site_i18n.catalogue(lang, self.feed, self.tr))
            cards = {d['id']: d for d in p.cards + p.archived}
            self.assertEqual(cards['lenovo-gk10-rt60-cn']['category'], 'keyboard-mouse')
            self.assertEqual(cards['lenovo-loq-25-10-cn']['category'], 'monitor-desk')
            self.assertEqual(cards['lenovo-gk10-rt60-cn']['market'], 'CN')
            self.assertEqual(cards['lenovo-gk10-rt60-cn']['countries'], '')
            self.assertEqual(cards['43ca41d03daa']['countries'], 'AU')
            self.assertEqual(len(p.cards), 13); self.assertEqual(len(p.archived), 17)
            self.assertEqual(set(p.selects), {'market', 'country', 'category'})
            self.assertIn('unknown', p.selects['country'])
            self.assertIn('KR', p.selects['country'])
            self.assertTrue(all(len(site_i18n.FILTER_TEXT[lang][i]) > 0 for i in range(20)))
    def test_link_verified_price_unverified_does_not_claim_unknown_identity(self):
        page = site_i18n.catalogue('en', [next(d for d in self.feed if d['id'] == 'lenovo-gk10-rt60-cn')], self.tr)
        self.assertIn('Magnetic-switch keyboard in black.', page)
        self.assertNotIn('Product identity and current price need verification.', page)
    def test_koofr_limit_is_per_person_not_account(self):
        expected = {'en': 'per person for their lifetime', 'ko': '1인당 평생 코드 1개',
                    'zh': '每人终身限兑换一个代码', 'ja': '1人につき生涯1コード',
                    'es': 'por persona durante toda su vida', 'fr': 'par personne pour toute sa vie'}
        for lang, phrase in expected.items():
            self.assertIn(phrase, self.tr['e30c9a510928'][lang]['conditions'])
    @unittest.skipUnless(shutil.which('node'), 'Node is needed to execute browser filter JavaScript')
    def test_filter_javascript_all_combinations_and_navigation(self):
        pages = []
        for lang in site_i18n.LANGS:
            p = FilterParser(); p.feed(site_i18n.catalogue(lang, self.feed, self.tr, discoveries=True))
            pages.append({'lang': lang, 'cards': p.cards, 'archived': p.archived,
                          'selects': p.selects, 'links': p.links})
        result = subprocess.run(['node', str(ROOT / 'tests/filter_behavior.cjs')],
                                input=json.dumps({'js': site_i18n.JS, 'pages': pages}),
                                text=True, capture_output=True, check=True)
        self.assertIn('3240 filter combinations passed', result.stdout)
