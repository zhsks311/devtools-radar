import copy
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from tools.check_editorial_evidence import digest, validate
from content.editorial_prompts import render

ROOT = Path(__file__).resolve().parents[1]


class EditorialEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.article = {'slug': 'a-vs-b', 'hook': 'A conditional claim'}
        self.deployment = dict(self.article, category='Test')
        self.record = {
            'schema_version': 1, 'slug': 'a-vs-b',
            'article_sha256': digest(self.article), 'deployment_sha256': digest(self.deployment),
            'author': 'writer', 'reviewer': 'independent-reader', 'review_status': 'approved',
            'coverage': 'all_published_high_risk_claims', 'decision': 'insufficient_evidence',
            'revised_at': '2026-11-14', 'reviewed_at': '2026-11-14',
            'claims': [{'id': 'plan-claim', 'claim': 'Example scoped claim', 'status': 'supported',
                        'source_kind': 'official_primary', 'source_url': 'https://example.com/docs',
                        'support': 'Short paraphrase', 'scope': 'US annual Pro',
                        'source_checked_at': '2026-11-14', 'evidence_expires_at': '2026-11-21'}]}

    def check(self, record=None):
        return validate(record or self.record, self.article, self.deployment, date(2026, 11, 14))

    def test_valid_record_is_not_a_truth_claim(self):
        self.assertEqual(self.check(), [])

    def test_changed_content_and_metadata_invalidate_review(self):
        self.article['hook'] = 'Changed'
        self.deployment['pricing'] = '$1'
        self.assertEqual(len(self.check()), 2)

    def test_no_self_review_or_missing_coverage(self):
        self.record['reviewer'] = 'writer'
        self.record['coverage'] = 'one_issue_only'
        self.assertEqual(len(self.check()), 2)

    def test_stale_future_contradicted_and_missing_evidence_fail(self):
        for mutation in [dict(status='contradicted'), dict(evidence_expires_at='2026-11-13'),
                         dict(source_checked_at='2026-11-15'), dict(source_url='')]:
            record = copy.deepcopy(self.record)
            record['claims'][0].update(mutation)
            self.assertTrue(self.check(record))
        self.record['claims'] = []
        self.assertTrue(self.check())

    def test_duplicate_claims_fail(self):
        self.record['claims'] *= 2
        self.assertTrue(self.check())

    def test_unrecorded_revision_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(ROOT/'tools/check_editorial_evidence.py'),
                                     '--slug', 'a-vs-b', '--root', tmp], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('BLOCKED', result.stdout)

    def test_prompts_have_no_legacy_angles_and_support_uncertainty(self):
        for stage in ['write', 'review', 'revise']:
            prompt = render(stage, 'supabase-vs-firebase')
            self.assertIn('no_comparable_evidence', prompt)
            self.assertIn('not verified truth', prompt)
            self.assertIn('Independent', prompt)
            self.assertNotIn('4.32', prompt)
            self.assertNotIn('ONLY source', prompt)

    def test_generators_portable_and_cover_new_slugs(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = Path(tmp)/'content/final'
            final.mkdir(parents=True)
            (final/'new-vs-new.json').write_text('{}')
            for name in ['make_prompts.py', 'make_review_prompts.py', 'make_revise_prompts.py']:
                subprocess.run([sys.executable, str(ROOT/'content'/name), '--root', tmp], check=True,
                               capture_output=True)
            self.assertEqual(len(list((Path(tmp)/'content/prompts').glob('*.md'))), 3)
