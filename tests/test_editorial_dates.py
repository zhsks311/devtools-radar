import copy
import json
import re
import tempfile
import unittest
from pathlib import Path
import build
from site_seo import finalize_seo
from tools.validate_data import validate_items

class EditorialDatesTests(unittest.TestCase):
    def test_explicit_modification_is_separate(self):
        items = json.loads(build.DATA_PATH.read_text())
        for item in items:
            page = build.generate_comparison_html(item)
            schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]
            article = next(x for x in schemas if x['@type'] == 'TechArticle')
            self.assertEqual(article['datePublished'], item['published'])
            if item.get('modified'):
                self.assertEqual(article['dateModified'], '2026-11-20')
                self.assertIn('Updated <time datetime="2026-11-20">2026-11-20</time>', page)
                self.assertIn('Source review recorded '+item['last_verified'], page)
            else:
                self.assertNotIn('dateModified', article)
        bad = copy.deepcopy(items)
        bad[0]['modified'] = 'not-a-date'
        self.assertTrue(any('modified' in str(e) for e in validate_items(bad)))

    def test_sitemap_only_explicit_canonical_revisions(self):
        items = json.loads(build.DATA_PATH.read_text())
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'index.html').write_text('<html><footer></footer></html>')
            (root/'sitemap.xml').write_text(build.generate_sitemap(items))
            finalize_seo(root, items, '')
            text = (root/'sitemap.xml').read_text()
            self.assertEqual(text.count('<lastmod>'), 2)
            self.assertEqual(text.count('<lastmod>2026-11-20</lastmod>'), 2)
