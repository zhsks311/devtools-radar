import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import build
from site_seo import finalize_seo


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
