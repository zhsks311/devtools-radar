import copy
import json
import unittest
from pathlib import Path
from tools.product_links import direct_product_url, publishable_link, validate_deal_links
import site_i18n

class ProductLinkTests(unittest.TestCase):
    def test_no_search_home_category_shortener_or_redirect(self):
        for u in ['https://www.coupang.com/np/search?q=mouse','https://www.coupang.com/',
                  'https://link.coupang.com/a/abc','https://www.stacksocial.com/collections/apps',
                  'https://www.stacksocial.com/sales/test?q=x',
                  'https://store.dji.com/cn/product/test?redirect=https://evil.example',
                  'https://www.coupang.com.evil.example/vp/products/123',
                  'javascript:alert(1)','https://www.coupang.com:bad/vp/products/123']:
            self.assertFalse(direct_product_url(u),u)
    def test_valid_route_not_enough(self):
        d={'id':'test','link':{'url':'https://www.coupang.com/vp/products/123?itemId=456'}}
        self.assertTrue(direct_product_url(d['link']['url']))
        self.assertFalse(publishable_link(d))
        self.assertTrue(validate_deal_links([d]))
        d['link_review']={'status':'verified_detail','checked_at':'2026-11-10T12:00:00Z',
                          'url':d['link']['url'],'product_match':True,'evidence':'Exact model and variant observed on seller page.'}
        self.assertTrue(publishable_link(d))
        d['link']['url']='https://www.coupang.com/vp/products/999'
        self.assertFalse(publishable_link(d))
    def test_held_never_has_cta_in_any_language(self):
        root=Path(__file__).resolve().parents[1]
        d=copy.deepcopy(json.loads((root/'data/deals.json').read_text())['feed'][0])
        d['link_review']={'status':'held','reason':'Access denied; exact product cannot be verified'}
        for lang in site_i18n.LANGS:
            page=site_i18n.catalogue(lang,[d],{})
            self.assertNotIn('class="cta"',page)
            self.assertIn(site_i18n.HELD[lang],page)
    def test_registered_links(self):
        root=Path(__file__).resolve().parents[1]
        feeds=sum([json.loads((root/'data'/f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
        self.assertEqual(validate_deal_links(feeds),[])

    def test_price_review_and_publication_counts_all_languages(self):
        root=Path(__file__).resolve().parents[1]
        feeds=sum([json.loads((root/'data'/f).read_text())['feed'] for f in ['deals.json','deals_en.json']],[])
        tr=json.loads((root/'data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            page=site_i18n.catalogue(lang,feeds,tr)
            self.assertEqual(page.count('class="cta"'),13)
            self.assertEqual(page.count('class="notice link-held"'),17)
            self.assertEqual(page.count(site_i18n.PRICE_CURRENT[lang]),10)
            self.assertEqual(page.count(site_i18n.PRICE_RECORDED[lang]),20)
            self.assertNotIn('href="https://link.coupang.com/',page)
