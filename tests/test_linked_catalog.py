import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
import site_i18n
from tools.product_links import publishable_link

class CatalogParser(HTMLParser):
    def __init__(self):
        super().__init__();self.area=None;self.active=[];self.held=[];self.links=[];self.archive_closed=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='details' and a.get('class')=='held-archive':self.archive_closed='open' not in a
        if a.get('id') in ('active-products','held-products'):self.area=a['id']
        if tag=='article' and a.get('class')=='card':
            (self.active if self.area=='active-products' else self.held).append(a['data-id'])
        if tag=='a' and a.get('class') in ('cta','product-title'):self.links.append((self.area,a['href']))

class LinkedCatalogTests(unittest.TestCase):
    def test_default_catalog_only_has_linked_products_in_all_languages(self):
        root=Path(__file__).resolve().parents[1]
        feed=sum([json.loads((root/'data'/n).read_text())['feed'] for n in ['deals.json','deals_en.json']],[])
        tr=json.loads((root/'data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            parser=CatalogParser();parser.feed(site_i18n.catalogue(lang,feed,tr))
            self.assertEqual(parser.active,[d['id'] for d in feed if publishable_link(d)])
            self.assertEqual(parser.held,[d['id'] for d in feed if not publishable_link(d)])
            self.assertTrue(parser.archive_closed)
            self.assertEqual(len(parser.links),2*len(parser.active))
            self.assertTrue(all(area=='active-products' for area,url in parser.links))
    def test_filters_count_active_and_archive_separately(self):
        self.assertIn("querySelectorAll('#active-products .card')",site_i18n.JS)
        self.assertIn("querySelectorAll('#held-products .card')",site_i18n.JS)
        self.assertIn("querySelector('#archive-count').textContent=hn",site_i18n.JS)
