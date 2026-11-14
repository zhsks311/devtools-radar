import json,re,unittest
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SLUG='stripe-vs-lemonsqueezy-vs-paddle'
class PaymentFeeEvidenceTests(unittest.TestCase):
 def test_rates_and_arithmetic(self):
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  b=next(x for x in json.loads((ROOT/'data/tools.json').read_text()) if x['slug']==SLUG)
  for x in (a,b):
   text=json.dumps(x,ensure_ascii=False)
   self.assertIn('0.5 percentage points',text)
   self.assertIn('including tax',text)
   self.assertIn('$1,600',text)
   self.assertIn('$1,120',text)
   self.assertIn('Paddle',text)
   self.assertNotIn('on either merchant of record',text)
   self.assertNotIn('6.6%',text)
   self.assertIn('https://docs.lemonsqueezy.com/help/getting-started/fees',x['sources'])
  gross=D(20000); n=D(1000)
  self.assertEqual(gross*D('.041')+n*D('.30'),D(1120))
  self.assertEqual(gross*D('.036')+n*D('.80'),D(1520))
  self.assertEqual(gross*D('.055')+n*D('.50'),D(1600))
  self.assertEqual(gross*D('.05')+n*D('.50'),D(1500))
  self.assertEqual(D(24)*D('.07')+D('.50'),D('2.18'))
  self.assertEqual(D(24)*D('.085')+D('.50'),D('2.54'))
 def test_generated_faq_and_generator(self):
  html=(ROOT/'dist/compare'/SLUG/'index.html').read_text()
  faq=next(json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S) if json.loads(s).get('@type')=='FAQPage')
  a=json.loads((ROOT/'content/final'/f'{SLUG}.json').read_text())
  self.assertEqual([f['acceptedAnswer']['text'] for f in faq['mainEntity']],[f['a'] for f in a['faqs']])
  import sys
  sys.path.insert(0,str(ROOT/'content'))
  from killer5_a import STRIPE
  self.assertEqual(STRIPE,a)
