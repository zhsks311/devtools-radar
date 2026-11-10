import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from content.merge import merge_articles
from tools.lint_content import lint_article
from tools.validate_data import validate_items

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        shutil.copytree(ROOT / 'data', self.base / 'data')
        shutil.copytree(ROOT / 'content' / 'final', self.base / 'content' / 'final')
        self.original = json.loads((self.base / 'data' / 'tools.json').read_text())

    def test_merge_preserves_all_articles_metadata_and_is_idempotent(self):
        result = merge_articles(self.base)
        self.assertEqual([x['slug'] for x in self.original], [x['slug'] for x in result])
        for before, after in zip(self.original, result):
            self.assertEqual(before['last_verified'], after['last_verified'])
            self.assertEqual(before['published'], after['published'])
            self.assertEqual(before['tool_a'], after['tool_a'])
        self.assertEqual(result, merge_articles(self.base))

    def test_removed_final_does_not_silently_delete_existing(self):
        (self.base / 'content' / 'final' / (self.original[0]['slug'] + '.json')).unlink()
        self.assertEqual(len(self.original), len(merge_articles(self.base)))

    def test_invalid_final_does_not_modify_deployment(self):
        target = self.base / 'data' / 'tools.json'
        before = target.read_bytes()
        (self.base / 'content' / 'final' / 'bad.json').write_text('{}')
        with self.assertRaises(ValueError):
            merge_articles(self.base)
        self.assertEqual(before, target.read_bytes())

    def test_empty_final_fails(self):
        shutil.rmtree(self.base / 'content' / 'final')
        with self.assertRaises(ValueError):
            merge_articles(self.base)

    def test_bad_shape_is_reported_not_crashed(self):
        for data in (None, [], {}, {'slug': []}, {'sections': [None]}):
            self.assertTrue(lint_article(data)[1])

    def test_slug_url_and_duplicate_validation(self):
        items = copy.deepcopy(self.original)
        items[0]['slug'] = '../../outside'
        items[1]['tool_a']['cta_url'] = 'javascript:alert(1)'
        items.append(items[2])
        errors = '\n'.join(validate_items(items))
        self.assertIn('slug must', errors)
        self.assertIn('cta_url', errors)
        self.assertIn('duplicate slug', errors)

    def test_data_content_gate_and_related_link(self):
        items = copy.deepcopy(self.original)
        items[0]['hook'] = 'A seamless game-changer'
        items[0]['related'][0]['slug'] = 'missing-page'
        errors = '\n'.join(validate_items(items))
        self.assertIn('banned phrase', errors)
        self.assertIn('unknown related slug', errors)

    def test_new_complete_final_is_added_without_dropping_others(self):
        item = copy.deepcopy(self.original[0])
        item['slug'] = 'new-comparison'
        (self.base / 'content' / 'final' / 'new-comparison.json').write_text(json.dumps(item))
        result = merge_articles(self.base)
        self.assertEqual(len(self.original) + 1, len(result))
        self.assertEqual('new-comparison', result[-1]['slug'])

    def test_new_article_without_metadata_fails_before_write(self):
        target = self.base / 'data' / 'tools.json'
        before = target.read_bytes()
        item = json.loads((self.base / 'content' / 'final' / 'bun-vs-node.json').read_text())
        item['slug'] = 'unknown-comparison'
        (self.base / 'content' / 'final' / 'unknown-comparison.json').write_text(json.dumps(item))
        with self.assertRaises(ValueError):
            merge_articles(self.base)
        self.assertEqual(before, target.read_bytes())

    def test_duplicate_existing_data_fails_before_write(self):
        target = self.base / 'data' / 'tools.json'
        target.write_text(json.dumps(self.original + [self.original[0]]))
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            merge_articles(self.base)
        self.assertEqual(before, target.read_bytes())

    def test_empty_deployment_fails(self):
        self.assertTrue(validate_items([]))

    def test_output_override_preserves_source(self):
        target = self.base / 'data' / 'tools.json'
        before = target.read_bytes()
        dest = self.base / 'out' / 'tools.json'
        self.assertEqual(len(self.original), len(merge_articles(self.base, dest)))
        self.assertEqual(before, target.read_bytes())
        self.assertTrue(dest.exists())


if __name__ == '__main__':
    unittest.main()
