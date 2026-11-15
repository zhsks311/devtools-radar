import json
import unittest
from decimal import Decimal
from pathlib import Path
from content.merge import META

ROOT = Path(__file__).resolve().parents[1]

class NeonBranchEvidence(unittest.TestCase):
    def test_hourly_arithmetic(self):
        def fee(branches, hours):
            return max(branches - 10, 0) * Decimal(str(hours)) * Decimal('0.002')
        self.assertEqual(fee(20, 730), Decimal('14.60'))
        self.assertEqual(fee(10, 730), 0)
        self.assertEqual(fee(11, 1), Decimal('0.002'))

    def test_canonical_scope_and_source_discrepancy(self):
        d = json.loads((ROOT/'content/final/planetscale-vs-neon.json').read_text())
        for value in (d['verdict_summary'], d['sections'][3]['content'], d['decision_matrix'][0]['why']):
            self.assertIn('10', value)
            self.assertIn('$0.002', value)
            self.assertIn('compute', value)
        self.assertIn('$14.60', d['cost_math'][2]['result'])
        self.assertIn('$1.50', d['sections'][3]['content'])
        self.assertIn('Source discrepancy', d['sections'][3]['content'])
        self.assertNotIn('a branch per pull request costs $1.50', json.dumps(d))
        self.assertIn('$0.002/branch-hour', json.dumps(META['planetscale-vs-neon']))
