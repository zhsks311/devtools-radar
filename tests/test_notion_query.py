import json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class NotionQueryTests(unittest.TestCase):
 def test_executable_mocks(self):
  subprocess.run(['node',str(ROOT/'tests/notion_query_mock.mjs')],check=True,cwd=ROOT)
 def test_rendered_example_is_tested_source(self):
  a=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']=='notion-vs-obsidian')
  self.assertEqual(a['tool_a']['code_example'],(ROOT/'content/examples/notion-query.mjs').read_text().strip())
  s=(ROOT/'dist/compare/notion-vs-obsidian/index.html').read_text()
  self.assertNotIn('/v1/databases/',s)
  self.assertIn('next_cursor',s)
  self.assertIn('2026-03-11',s)
