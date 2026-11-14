import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.deal_candidates import load_candidates, candidate_cards, TEXT
from tools.product_links import publishable_link

class CandidateTests(unittest.TestCase):
    def test_records_are_unverified_not_offers(self):
        rows=load_candidates()
        self.assertEqual(len(rows),5)
        for row in rows:
            self.assertFalse(publishable_link(row))
            self.assertIsNone(row['current_price'])
            self.assertEqual(row['shipping_countries'],[])
    def test_six_locales_have_direct_links_and_disclosure(self):
        for lang in TEXT:
            cards=candidate_cards(lang)
            self.assertEqual(len(cards),5)
            for card in cards:
                self.assertIn('data-countries=""',card)
                self.assertIn('data-market="unknown"',card)
                self.assertIn('www.aliexpress.com/item/',card)
                self.assertIn('PriceArchive',card)
                self.assertNotIn('<del',card)
                self.assertNotIn('s.click',card)
    def test_unverified_fields_fail_closed(self):
        for key,value in [('category','unknown'),('category',None),('current_price',12),('discount',50),('shipping_countries',['KR']),('url','https://www.aliexpress.com/search?q=foo'),('observed_at','2099-01-01T00:00:00Z')]:
            rows=copy.deepcopy(load_candidates());rows[0][key]=value
            with tempfile.TemporaryDirectory() as temp:
                path=Path(temp)/'test.json';path.write_text(json.dumps(rows))
                with self.assertRaises(ValueError):load_candidates(path)
    def test_aggregate_and_empty_copy_do_not_verify_discoveries(self):
        import site_i18n
        ROOT=Path(__file__).resolve().parents[1]
        feed=sum([json.loads((ROOT/'data'/name).read_text())['feed'] for name in ('deals.json','deals_en.json')],[])
        tr=json.loads((ROOT/'data/deal_localizations.json').read_text())
        for lang in TEXT:
            page=site_i18n.catalogue(lang,feed,tr,discoveries=True)
            self.assertIn('18 '+site_i18n.FILTER_TEXT[lang][7]+' · 5 '+site_i18n.DISCOVERY_LABEL[lang],page)
            self.assertNotIn('23 '+site_i18n.FILTER_TEXT[lang][7],page)
            self.assertIn(site_i18n.EMPTY_LABEL[lang],page)
            self.assertIn(site_i18n.UNKNOWN_SHORTCUT[lang],page)
            self.assertEqual(page.count('data-kind="discovery"'),5)

    def test_keyboard_has_specific_category(self):
        rows=load_candidates()
        self.assertEqual(rows[0]['category'],'keyboard-mouse')
        for lang in TEXT:
            self.assertIn('data-category="keyboard-mouse"', candidate_cards(lang)[0])
            self.assertIn('data-category="hardware"', candidate_cards(lang)[1])
