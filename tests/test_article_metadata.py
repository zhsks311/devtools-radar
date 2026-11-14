import copy
import json
from pathlib import Path
import tempfile
import unittest
import build
from article_metadata import DESCRIPTIONS, article_description, validate_description
from tools.check_site import Page, check_site


class ArticleMetadataTests(unittest.TestCase):
    def test_all_current_articles_have_specific_complete_descriptions(self):
        items=json.loads(build.DATA_PATH.read_text())
        self.assertEqual({item['slug'] for item in items}, set(DESCRIPTIONS))
        self.assertEqual(len(DESCRIPTIONS), len(set(DESCRIPTIONS.values())))
        for item in items:
            value=article_description(item)
            self.assertEqual(validate_description(value), value)
            self.assertNotEqual(value, item['hook'][:180])
            parser=Page(); parser.feed(build.generate_comparison_html(item))
            for key in ('description', 'og:description', 'twitter:description'):
                self.assertEqual(parser.metadata[key], [value])

    def test_invalid_description_is_rejected_not_truncated(self):
        for value in (None, '', 'x'*181+'.', 'x'*80, 'x'*80+'…', 'x'*80+'...', '<b>'+'x'*80+'.', 'x'*70+'\nDone.'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_description(value)

    def test_new_article_requires_reviewed_summary(self):
        with self.assertRaises(ValueError): article_description({'slug': 'new-article'})
        value='Compare the documented costs and constraints of these tools with explicit workload assumptions.'
        self.assertEqual(article_description({'slug':'new-article','meta_description':value}), value)

    def test_output_gate_rejects_each_damaged_meta_field(self):
        items=json.loads(build.DATA_PATH.read_text())
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'site'
            build.render_site(items, out, build.load_deals(), build.load_deals(build.DEALS_EN_DATA_PATH))
            page=out/'compare'/items[0]['slug']/'index.html'
            original=page.read_text()
            for field, kind in (('description','name'), ('og:description','property')):
                import re
                changed=re.sub(rf'(<meta {kind}="{field}" content=")[^"]*', r'\g<1>Truncated wor', original, count=1)
                self.assertNotEqual(changed, original)
                page.write_text(changed)
                errors=check_site(out, build.DATA_PATH)
                self.assertTrue(any(field+' must match' in error for error in errors), errors)
            page.write_text(original)
            self.assertEqual(check_site(out, build.DATA_PATH), [])
