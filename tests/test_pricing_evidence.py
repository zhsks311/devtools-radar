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

    def test_cache_accounting_and_controls(self):
        article = json.loads((ROOT / 'content/final' / (SLUG + '.json')).read_text())
        deployed = next(a for a in json.loads((ROOT / 'data/tools.json').read_text()) if a['slug'] == SLUG)
        for item in (article, deployed):
            text = json.dumps(item)
            self.assertIn('top-level cache_control', text)
            self.assertIn('opt-in', text)
            self.assertIn('0.05(n-1)', text)
            self.assertIn('2 + 2 = 4', text)
            for wrong in ('1.25 + 0.10n', '77.5%', '2.0 write + 0.10 read', 'needs three reads'):
                self.assertNotIn(wrong, text)
        for write, first_profitable in ((1.25, 2), (2, 3), (2.5, 3)):
            for n in range(1, 11):
                self.assertEqual(write + .05 * (n-1) < n, n >= first_profitable)
        self.assertAlmostEqual(1-(1.25+.05*9)/10, .83)
        self.assertAlmostEqual(1-(1.25+.1*9)/10, .785)
        self.assertAlmostEqual(2.5+.05, 2.55)
        self.assertIn('prompt_cache_breakpoint', deployed['tool_b']['code_example'])
        self.assertNotIn('0.10x', deployed['tool_a']['code_example'])

    def test_generated_faq_matches_source(self):
        import re
        html = (ROOT / 'dist/compare' / SLUG / 'index.html').read_text()
        schemas = [json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
        faq = next(s for s in schemas if s.get('@type') == 'FAQPage')
        article = json.loads((ROOT / 'content/final' / (SLUG + '.json')).read_text())
        self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']], [f['a'] for f in article['faqs']])

    def test_current_openai_rates_are_distinct_from_historical_worked_example(self):
        article = json.loads((ROOT / 'content/final' / (SLUG + '.json')).read_text())
        deployed = next(a for a in json.loads((ROOT / 'data/tools.json').read_text()) if a['slug'] == SLUG)
        self.assertEqual(article['sections'], deployed['sections'])
        update = article['sections'][0]['content']
        self.assertIn('| GPT-6.2 Sol | $2.00 | $10.00 | $0.10 | $2.50 | $5.00 |', update)
        self.assertIn('| GPT-6.2 Astra | $8.00 | $40.00 | $0.40 | $10.00 | $20.00 |', update)
        self.assertIn('272,000 input tokens', update)
        self.assertIn('for the full request', update)
        self.assertIn('$1/$5 for Sol and $4/$20 for Astra', update)
        self.assertIn('Neither GPT-6.2 model supports Flex', update)
        self.assertIn('GPT-6.1 Sol', article['cost_math'][0]['formula'])
        self.assertIn('$1,844', article['cost_math'][0]['result'])

        outputs = (
            ROOT / 'dist/compare' / SLUG / 'index.html',
            ROOT / 'dist/llms-full.txt',
        )
        for path in outputs:
            output = path.read_text()
            self.assertIn('Neither GPT-6.2 model supports Flex', output)
            self.assertIn('GPT-6.2 Astra', output)
            self.assertIn('$1,844', output)
        for path in (ROOT / 'dist/index.html', ROOT / 'dist/reports/ko/index.html'):
            self.assertIn('GPT-6.2 Sol lists $2 input and $10 output', path.read_text())
