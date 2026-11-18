import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CrabComparisonTests(unittest.TestCase):
    def test_direct_purchase_is_not_external_key_refund(self):
        item = next(x for x in json.loads((ROOT / 'data/deals.json').read_text())['feed'] if x['id'] == 'everything-is-crab-directgames-kr-jp')
        comparison = item['alternative_review']['comparison']
        self.assertEqual(comparison['alternative_price'] - comparison['seller_price'], comparison['difference'])
        self.assertEqual(comparison['country'], 'KR')
        self.assertIn('external keys', comparison['limitations'])
        self.assertIn('steam_refunds', comparison['refund_source_url'])
        self.assertIsNone(item['discount_pct'])
        localizations = json.loads((ROOT / 'data/deal_localizations.json').read_text())[item['id']]
        for lang in ('ko', 'en', 'zh', 'ja', 'es', 'fr'):
            self.assertIn('Steam', localizations[lang]['buying_note'])
            self.assertIn('Direct Games', localizations[lang]['buying_note'])
