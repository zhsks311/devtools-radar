import copy
import json
import unittest
from pathlib import Path
import site_i18n
from tools.product_links import direct_product_url, publishable_link
from tools.deal_prices import checked_price, discount_percent
from tools.deal_countries import confirmed_countries

ROOT = Path(__file__).resolve().parents[1]
class KoreanRecoveryTests(unittest.TestCase):
    def test_query_product_ids_are_required_and_unambiguous(self):
        for base, key in [('https://item.gmarket.co.kr/Item', 'goodsCode'),
                          ('https://artmu.co.kr/product/detail.html', 'product_no')]:
            self.assertTrue(direct_product_url(base+'?'+key+'=123'))
            for tail in ['', '?'+key+'=', '?'+key+'=abc', '?'+key+'=123&'+key+'=456',
                         '?'+key+'=123&'+key.lower()+'=456', '?'+key+'=123&query=',
                         '?'+key+'=123&redirect=https://example.com']:
                self.assertFalse(direct_product_url(base+tail),base+tail)
            self.assertFalse(direct_product_url(base.replace('https://','https://evil.')+'?'+key+'=123'))
    def test_three_restored_korean_offers_have_fresh_seller_and_country_evidence(self):
        data=json.loads((ROOT/'data/deals.json').read_text())
        restored={d['id']:d for d in data['feed'] if publishable_link(d)}
        expected={'deal-belkin-100w-gan':39900, 'deal-ugreen-100w-gan':65100, 'deal-artmu-100w-gb102':35700}
        self.assertEqual(set(restored),set(expected))
        for ident,price in expected.items():
            d=restored[ident]
            self.assertEqual(d['price'],price);self.assertTrue(checked_price(d))
            self.assertEqual(confirmed_countries(d),('KR',));self.assertIsNone(discount_percent(d))
            self.assertFalse(d['link']['tracked']);self.assertFalse(d['rocket'])
            self.assertNotIn('쿠팡',d['store']);self.assertEqual(d['checked_date'],'2026-11-14')
            mutated=copy.deepcopy(d);mutated['link']['url']+='9'
            self.assertFalse(publishable_link(mutated));self.assertFalse(checked_price(mutated))
        tr=json.loads((ROOT/'data/deal_localizations.json').read_text())
        for lang in site_i18n.LANGS:
            page=site_i18n.catalogue(lang,data['feed'],tr)
            self.assertEqual(page.count('class="cta"'),3)
            self.assertIn('data-countries="KR"',page)
            self.assertNotIn('65W+35W', tr['deal-artmu-100w-gb102'][lang]['summary'])
    def test_new_overseas_offers_keep_base_price_and_activation_limits(self):
        payload=json.loads((ROOT/'data/deals_en.json').read_text()); feed=payload['feed']
        self.assertEqual(payload['stats']['feed'],len(feed))
        for ident,price,countries in [('mail-backup-x-individual-v2',49.99,()),('babbel-lifetime-all-languages',249,('US',))]:
            d=next(d for d in feed if d['id']==ident)
            self.assertTrue(publishable_link(d));self.assertTrue(checked_price(d))
            self.assertEqual(d['price'],price);self.assertEqual(confirmed_countries(d),countries)
            self.assertIsNone(discount_percent(d));self.assertIsNone(d['original_price'])
            self.assertIn('30 days',d['purchase_eligibility']['activation'])
            self.assertIn('final sale',d['purchase_eligibility']['returns'])
