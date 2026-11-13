import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'anthropic-vs-openai-api-pricing'

class PricingEvidenceTests(unittest.TestCase):
    def test_corrected_tokenizer_scope_and_sensitivity(self):
        article = json.loads((ROOT / 'content/final' / (SLUG + '.json')).read_text())
        deployed = next(a for a in json.loads((ROOT / 'data/tools.json').read_text()) if a['slug'] == SLUG)
        for item in (article, deployed):
            text = json.dumps(item)
            self.assertNotIn('$2,397', text)
            self.assertNotIn('$1,844 × 1.3', text)
            self.assertIn('not between Claude and GPT', text)
            self.assertIn('unchanged output $500', text)
            self.assertIn('$2,247.20', text)
            self.assertIn('No. Anthropic compares newer and earlier Claude tokenizers', item['faqs'][2]['a'])
        self.assertAlmostEqual((400 + 144 + 800) * 1.3 + 500, 2247.2)
