import unittest,json
from pathlib import Path
import site_i18n as i
class MultilingualTests(unittest.TestCase):
 def setUp(self):
  root=Path(__file__).resolve().parents[1];self.feeds=sum([json.loads((root/f'data/{n}.json').read_text())['feed'] for n in ('deals','deals_en')],[]);self.tr=json.loads((root/'data/deal_localizations.json').read_text())
 def test_complete_translations(self):
  for d in self.feeds:
   for lang in i.LANGS:
    for key in ('product','summary','conditions'):self.assertTrue(self.tr[d['id']][lang][key])
 def test_same_catalog_every_language(self):
  for lang in i.LANGS:
   s=i.catalogue(lang,self.feeds,self.tr)
   self.assertEqual(s.count('<article class="card"'),len(self.feeds))
   self.assertIn('data-market="KR"',s);self.assertIn('data-market="CN"',s)
   for d in self.feeds:self.assertIn('data-id="'+d['id']+'"',s)
   for path in i.PATHS.values():self.assertIn('href="https://devteardown.com'+path+'"',s)
 def test_escape_and_bad_urls(self):
  d=dict(self.feeds[0]);d['product']='<script>';d['id']='unknown';d['link']={'url':'javascript:alert(1)'}
  s=i.catalogue('en',[d],{});self.assertNotIn('javascript:alert',s);self.assertIn('&lt;script&gt;',s)
 def test_filters_preserve_state(self):
  self.assertIn("params.set('market'",i.JS);self.assertIn("params.set('category'",i.JS);self.assertIn('aria-live="polite"',i.catalogue('en',[],{}))
