import json,subprocess,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ResendIdempotencyTests(unittest.TestCase):
 def test_mock_outcomes(self):
  subprocess.run(['node',str(ROOT/'tests/resend_attempt_mock.mjs')],check=True,cwd=ROOT)
 def test_generated_code_and_limits(self):
  sys.path.insert(0,str(ROOT/'content'))
  from killer5_c import RESEND
  a=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']=='resend-vs-sendgrid')
  code=(ROOT/'content/examples/resend-attempt.mjs').read_text().strip()
  self.assertEqual(RESEND['tool_a']['code_example'],code)
  self.assertEqual(a['tool_a']['code_example'],code)
  for p in ['dist/compare/resend-vs-sendgrid/index.html','dist/llms-full.txt']:
   s=(ROOT/p).read_text();self.assertIn('24 hours only',s);self.assertIn('reconcile ambiguous outcomes',s)
