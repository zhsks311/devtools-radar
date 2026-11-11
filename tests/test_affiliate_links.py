import copy
import unittest
from html.parser import HTMLParser

import site_i18n
from tools.affiliate_links import aliexpress_promotion_url, verified_aliexpress_url
from tools.product_links import direct_product_url, publishable_link, validate_deal_links


class ProductAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('class') in ('product-title', 'cta'):
            self.links.append(attrs)


def example():
    # Synthetic fixtures only. These are not commissioned or published products.
    source = 'https://www.aliexpress.com/item/1000000000000001.html'
    promotion = 'https://s.click.aliexpress.com/e/_test_only'
    return {
        'id': 'affiliate-test', 'product': 'Synthetic test product',
        'price': 10, 'currency': 'USD', 'category': 'hardware',
        'link': {'url': source, 'tracked': False},
        'link_review': {'status': 'verified_detail', 'url': source,
                        'checked_at': '2026-01-01T12:00:00Z', 'product_match': True,
                        'evidence': 'Synthetic product-review fixture.'},
        'affiliate': {
            'network': 'aliexpress', 'status': 'verified',
            'source_url': source, 'promotion_url': promotion,
            'review': {'promotion_url': promotion, 'resolved_product_url': source,
                       'owner_confirmed': True, 'product_match': True,
                       'checked_at': '2026-01-01T12:00:00Z',
                       'evidence': 'Synthetic owner and redirect-review fixture.'},
        },
    }


class AffiliateLinkTests(unittest.TestCase):
    def test_reviewed_mapping_preserves_canonical_source(self):
        deal = example()
        original = copy.deepcopy(deal)
        self.assertTrue(direct_product_url(deal['link']['url']))
        self.assertTrue(publishable_link(deal))
        self.assertEqual(validate_deal_links([deal]), [])
        for language in site_i18n.LANGS:
            page = site_i18n.catalogue(language, [deal], {})
            parser = ProductAnchors(); parser.feed(page)
            self.assertEqual(len(parser.links), 2)
            self.assertTrue(all(a['href'] == deal['affiliate']['promotion_url'] for a in parser.links))
            self.assertTrue(all('sponsored' in a['rel'].split() for a in parser.links))
            self.assertIn(site_i18n.AFFILIATE_DISCLOSURE[language], page)
            self.assertLess(page.index('affiliate-disclosure'), page.index('class="cta"'))
        self.assertEqual(deal, original)

    def test_no_configuration_uses_the_reviewed_direct_product(self):
        deal = example(); del deal['affiliate']
        self.assertEqual(validate_deal_links([deal]), [])
        page = site_i18n.catalogue('en', [deal], {})
        parser = ProductAnchors(); parser.feed(page)
        self.assertTrue(all(a['href'] == deal['link']['url'] for a in parser.links))
        self.assertNotIn('s.click.aliexpress.com', page)
        self.assertNotIn('affiliate-disclosure', page)

    def test_held_affiliate_never_emits_promotion(self):
        deal = example()
        deal['affiliate'].update(status='held', reason='Owner-issued link is not yet verified.')
        self.assertEqual(validate_deal_links([deal]), [])
        for language in site_i18n.LANGS:
            page = site_i18n.catalogue(language, [deal], {})
            self.assertNotIn(deal['affiliate']['promotion_url'], page)
            self.assertIn(deal['link']['url'], page)
            self.assertNotIn('affiliate-disclosure', page)

    def test_affiliate_cannot_override_a_held_product(self):
        deal = example()
        deal['link_review'] = {'status': 'held', 'reason': 'Product identity not verified.'}
        self.assertTrue(validate_deal_links([deal]))
        for language in site_i18n.LANGS:
            page = site_i18n.catalogue(language, [deal], {})
            self.assertNotIn('class="cta"', page)
            self.assertNotIn(deal['affiliate']['promotion_url'], page)

    def test_incomplete_changed_or_future_review_is_rejected(self):
        mutations = [
            ('network', 'unknown'), ('source_url', 'https://www.aliexpress.com/item/2.html'),
            ('promotion_url', 'https://s.click.aliexpress.com/e/_changed'),
            ('status', 'pending'), ('review', None),
        ]
        reviews = [('owner_confirmed', False), ('owner_confirmed', 'true'),
                   ('product_match', False), ('checked_at', '9999-01-01T00:00:00Z'),
                   ('checked_at', '2026-01-01'), ('evidence', ''),
                   ('resolved_product_url', 'https://www.aliexpress.com/item/2.html'),
                   ('promotion_url', 'https://s.click.aliexpress.com/e/_changed')]
        for target, key, value in [('affiliate', k, v) for k, v in mutations] + [('review', k, v) for k, v in reviews]:
            with self.subTest(target=target, key=key, value=value):
                deal = example()
                (deal['affiliate'] if target == 'affiliate' else deal['affiliate']['review'])[key] = value
                self.assertIsNone(verified_aliexpress_url(deal))
                self.assertTrue(validate_deal_links([deal]))
                self.assertNotIn('s.click.aliexpress.com', site_i18n.catalogue('en', [deal], {}))

    def test_no_tracking_parameters_or_arbitrary_redirects_are_invented(self):
        for url in ['http://s.click.aliexpress.com/e/_test',
                    'https://s.click.aliexpress.com.evil.example/e/_test',
                    'https://s.click.aliexpress.com@evil.example/e/_test',
                    'https://s.click.aliexpress.com/e/_test?redirect=https://evil.example',
                    'https://s.click.aliexpress.com/e/_test#fragment',
                    'https://s.click.aliexpress.com:443/e/_test',
                    'https://s.click.aliexpress.com/e/',
                    'https://s.click.aliexpress.com/e/%5Ftest',
                    'javascript:alert(1)']:
            self.assertFalse(aliexpress_promotion_url(url), url)
        deal = example(); del deal['affiliate']; deal['link']['tracked'] = True
        self.assertTrue(validate_deal_links([deal]))

    def test_canonical_aliexpress_url_never_hides_tracking_or_redirects(self):
        base = example()['link']['url']
        self.assertTrue(direct_product_url(base + '?sku_id=1234'))
        self.assertTrue(direct_product_url(base + '?skuId=1234'))
        for suffix in ['?aff_fcid=foreign', '?aff_fsk=foreign', '?tracking_id=foreign',
                       '?sk=foreign', '?redirect=', '?redirect=https://evil.example',
                       '?sku_id=https://evil.example', '#tracking', '?unknown=1']:
            self.assertFalse(direct_product_url(base + suffix), suffix)

    def test_unsupported_configuration_cannot_silently_publish(self):
        for value in ['', [], True, {}, {'network': 'aliexpress', 'status': 'held'}]:
            deal = example(); deal['affiliate'] = value
            self.assertTrue(validate_deal_links([deal]))

    def test_all_paid_product_anchors_have_sponsored_rel(self):
        deal = example(); del deal['affiliate']
        deal['link']['url'] = 'https://www.coupang.com/vp/products/123'
        deal['link']['tracked'] = True
        deal['link_review']['url'] = deal['link']['url']
        page = site_i18n.catalogue('ko', [deal], {})
        parser = ProductAnchors(); parser.feed(page)
        self.assertEqual(len(parser.links), 2)
        self.assertTrue(all('sponsored' in a['rel'].split() for a in parser.links))
        self.assertIn(site_i18n.AFFILIATE_DISCLOSURE['ko'], page)
