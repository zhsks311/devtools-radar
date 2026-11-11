import json
import re
import contextlib
import copy
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import build
from site_seo import finalize_seo, language_groups, REPORT_META
from tools.check_site import Page, check_site, schema_nodes
from tools.product_links import publishable_link


class SEOTests(unittest.TestCase):
    def test_article_source_and_brand(self):
        item = json.loads(build.DATA_PATH.read_text())[0]
        page = build.generate_comparison_html(item)
        schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]
        article = next(x for x in schemas if x['@type'] == 'TechArticle')
        self.assertEqual(article['citation'], item['sources'])
        self.assertEqual(article['author']['name'], 'DevTeardown')
        self.assertIn('not a live price or checkout check', page)
        self.assertNotIn('<strong>Core engine</strong>', page)

    def test_policy_links_and_no_fake_lastmod(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'index.html').write_text('<html><footer></footer></html>')
            (root/'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://devteardown.com/</loc><lastmod>2099-01-01</lastmod></url></urlset>')
            finalize_seo(root, [], '')
            self.assertIn('/editorial-policy/', (root/'index.html').read_text())
            self.assertNotIn('lastmod', (root/'sitemap.xml').read_text())
            self.assertIn('editorial-policy', (root/'sitemap.xml').read_text())
            self.assertIn('do not guarantee', (root/'editorial-policy/index.html').read_text())

    def test_llm_directory_does_not_overclaim(self):
        text = build.generate_llms_txt([], {}, {})
        self.assertIn('/editorial-policy/', text)
        self.assertNotIn('Every number', text)
        self.assertNotIn('daily', text)

    def test_evidence_export_preserves_context_and_sources(self):
        item = copy.deepcopy(json.loads(build.DATA_PATH.read_text())[0])
        item['sections'][0]['content'] = ('Cost context. ' * 100) + 'Only on the annual plan; taxes are excluded.'
        text = build.generate_llms_full_txt([item], {}, {})
        self.assertIn(item['sections'][0]['content'], text)
        self.assertIn(item['verdict_summary'], text)
        self.assertIn(item['last_verified'], text)
        for source in item['sources']:
            self.assertIn(source, text)
        self.assertIn('not a new source review', text)
        self.assertNotIn('Export generated:', text)

    def test_evidence_export_omits_held_links_and_distinguishes_price_checks(self):
        ko = build.load_deals()
        en = build.load_deals(build.DEALS_EN_DATA_PATH)
        text = build.generate_llms_full_txt([], ko, en)
        for deal in ko['feed'] + en['feed']:
            if publishable_link(deal):
                self.assertIn(deal['link']['url'], text)
            else:
                self.assertNotIn(deal['link']['url'], text)
                self.assertNotIn(deal['product'], text)
        self.assertIn('Retained price; current seller price unverified', text)
        self.assertIn('Seller price observation dated', text)
        self.assertIn('not proof of current stock', text)

    def test_invalid_or_future_price_evidence_is_not_promoted_in_export(self):
        deal = copy.deepcopy(next(d for d in build.load_deals(build.DEALS_EN_DATA_PATH)['feed']
                                  if d.get('price_review', {}).get('price_status') == 'seller_page_display_confirmed'))
        for change in ({'review_completed_at': '2099-01-01'}, {'evidence': []}, {'verified_price': 999999}):
            bad = copy.deepcopy(deal)
            bad['price_review'].update(change)
            text = build.generate_llms_full_txt([], {}, {'feed': [bad]})
            self.assertIn('Retained price; current seller price unverified', text)
            self.assertNotIn('Seller price observation dated', text)


class DiscoveryOutputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'site'
        with contextlib.redirect_stdout(io.StringIO()):
            build.build_site(output=self.output)

    def page(self, path):
        target = self.output / path.strip('/') / 'index.html'
        page = Page()
        page.feed(target.read_text())
        return page

    def errors(self):
        return '\n'.join(check_site(self.output, build.DATA_PATH))

    def edit(self, path, before, after):
        page = self.output / path
        text = page.read_text()
        self.assertIn(before, text)
        page.write_text(text.replace(before, after, 1))

    def test_complete_output_passes_discovery_gate(self):
        self.assertEqual('', self.errors())

    def test_language_groups_are_distinct_reciprocal_and_include_default(self):
        for group in language_groups():
            expected = {lang: build.BASE_URL + path for lang, path in group.items()}
            for path in set(group.values()):
                self.assertEqual(expected, self.page(path).alternates)
        self.assertNotEqual(self.page('/').alternates['ko'], self.page('/deals/').alternates['ko'])

    def test_localized_indexes_have_local_metadata_and_english_article_labels(self):
        for lang, (name, description) in REPORT_META.items():
            path = '/' if lang == 'en' else f'/reports/{lang}/'
            page = self.page(path)
            self.assertEqual([name + ' | DevTeardown'], page.titles)
            self.assertEqual([description], page.metadata['description'])
            self.assertEqual([build.BASE_URL + path], page.metadata['og:url'])
            self.assertIn('class="index-list" lang="en"',
                          (self.output / path.strip('/') / 'index.html').read_text())

    def test_stable_structured_identity_has_no_fabricated_product_ratings(self):
        for path in ('/', '/deals/', '/reports/ko/', '/editorial-policy/', '/compare/bun-vs-node/'):
            page = self.page(path)
            nodes = list(schema_nodes(page.schemas))
            entity = next(n for n in nodes if n.get('@id') == build.BASE_URL + path + '#webpage')
            self.assertEqual(page.lang, entity['inLanguage'])
            self.assertEqual({'@id': build.BASE_URL + '/#publisher'}, entity['publisher'])
            self.assertFalse(any(n.get('@type') in ('Product', 'Offer', 'Review', 'AggregateRating') for n in nodes))

    def test_finalizer_does_not_duplicate_sitemap_language_or_schema_nodes(self):
        finalize_seo(self.output, [], '')
        self.assertEqual('', self.errors())
        nodes = list(schema_nodes(self.page('/').schemas))
        for type_ in ('WebSite', 'Organization', 'CollectionPage'):
            self.assertEqual(1, sum(n.get('@type') == type_ for n in nodes))

    def test_gate_rejects_missing_or_filtered_canonical(self):
        self.edit('deals/index.html', 'rel="canonical" href="https://devteardown.com/deals/"',
                  'rel="canonical" href="https://devteardown.com/deals/?country=KR"')
        self.assertIn('canonical must match', self.errors())

    def test_gate_rejects_wrong_social_url(self):
        self.edit('reports/ko/index.html', 'property="og:url" content="https://devteardown.com/reports/ko/"',
                  'property="og:url" content="https://devteardown.com/"')
        self.assertIn('Open Graph URL', self.errors())

    def test_gate_rejects_broken_reciprocal_hreflang(self):
        self.edit('ko/index.html', '<link rel="alternate" hreflang="fr" href="https://devteardown.com/fr/">', '')
        self.assertIn('not reciprocal', self.errors())
        self.assertIn('sitemap/HTML hreflang mismatch', self.errors())

    def test_gate_rejects_sitemap_duplicates_and_missing_entries(self):
        target = self.output / 'sitemap.xml'
        root = ET.parse(target).getroot()
        root.append(copy.deepcopy(root[0]))
        root.remove(root[1])
        ET.ElementTree(root).write(target, encoding='utf-8')
        self.assertIn('duplicate sitemap URL', self.errors())
        self.assertIn('exactly the generated', self.errors())

    def test_gate_rejects_missing_titles_and_noindex(self):
        self.edit('index.html', '<title>Developer tool comparisons | DevTeardown</title>',
                  '<meta name="robots" content="noindex,follow">')
        self.assertIn('one nonempty title', self.errors())
        self.assertIn('has noindex', self.errors())

    def test_gate_rejects_blocked_search_bot(self):
        self.edit('robots.txt', 'User-agent: OAI-SearchBot\nAllow: /', 'User-agent: OAI-SearchBot\nDisallow: /')
        self.assertIn('blocked by robots.txt for OAI-SearchBot', self.errors())

    def test_gate_rejects_structured_citation_without_visible_source_link(self):
        item = json.loads(build.DATA_PATH.read_text())[0]
        from html import escape
        self.edit(f'compare/{item["slug"]}/index.html', 'href="' + escape(item['sources'][0], quote=True) + '"',
                  'href="https://example.com/other-source"')
        self.assertIn('citation is not linked', self.errors())
