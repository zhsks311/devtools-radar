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
        for key,value in [('current_price',12),('discount',50),('shipping_countries',['KR']),('url','https://www.aliexpress.com/search?q=foo'),('observed_at','2099-01-01T00:00:00Z')]:
            rows=copy.deepcopy(load_candidates());rows[0][key]=value
            with tempfile.TemporaryDirectory() as temp:
                path=Path(temp)/'test.json';path.write_text(json.dumps(rows))
                with self.assertRaises(ValueError):load_candidates(path)
