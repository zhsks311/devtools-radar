import json
import unittest
from pathlib import Path

class SheetsWorkflow(unittest.TestCase):
    def test_linked_and_imported_modes_are_distinct(self):
        d = next(d for d in json.loads(Path('data/deals_en.json').read_text())['feed'] if d['id'] == 'wpdatatables-1-code')
        self.assertFalse(d['sheets_workflow_review']['linked_table_editable'])
        self.assertFalse(d['sheets_workflow_review']['imported_table_auto_sync'])
        self.assertEqual(len(d['sheets_workflow_review']['sources']), 2)
        loc = json.loads(Path('data/deal_localizations.json').read_text())['wpdatatables-1-code']
        for lang in ['ko', 'en', 'zh', 'ja', 'es', 'fr']:
            self.assertTrue(loc[lang]['buying_note'])
        self.assertIn('자동 동기화되지 않습니다', loc['ko']['buying_note'])
        self.assertIn('separate workflow', loc['en']['buying_note'])
