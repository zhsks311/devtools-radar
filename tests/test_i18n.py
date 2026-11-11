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

 def test_language_dropdown(self):
  for lang in i.LANGS:
   for report in (False,True):
    nav=i.nav(lang,report)
    self.assertIn('<details class="languages">',nav)
    self.assertIn('aria-label="'+i.LANGUAGE_LABEL[lang]+': '+i.LANGS[lang]+'"',nav)
    self.assertEqual(nav.count('class="lang"'),6)
    self.assertEqual(nav.count('aria-current="page"'),1)
    for code in i.LANGS:
     self.assertIn(i.FLAGS[code],nav)
     path=('/' if code=='en' else '/reports/'+code+'/') if report else i.PATHS[code]
     self.assertIn('href="'+path+'" lang="'+code+'"',nav)
  self.assertIn("event.key==='Escape'",i.LANGUAGE_JS)
  self.assertIn('pageshow',i.LANGUAGE_JS)
 def test_short_korean_heading(self):
  page=i.catalogue('ko',self.feeds,self.tr)
  self.assertIn('<h1>핫딜</h1>',page)
  self.assertNotIn('모든 딜을 한곳에서',page)
