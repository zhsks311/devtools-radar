import json
from pathlib import Path
import unittest
from tools.audit_monetization import audit
from tools.product_links import publishable_link
import site_i18n
from tests.catalog_fixture_clock import CATALOG_AS_OF

class MonetizationTests(unittest.TestCase):
    def setUp(self):
        root=Path(__file__).resolve().parents[1]
        self.rows=sum([json.loads((root/'data'/name).read_text())['feed'] for name in ('deals.json','deals_en.json')],[])
    def test_held_tracking_never_counts_as_published(self):
        report=audit(self.rows)
        self.assertFalse(set(report['held_commission_link_ids']) & set(report['published_commission_link_ids']))
        self.assertEqual(report['attribution_and_earnings'],'not_verified')
        self.assertEqual(report['published_products'],len(report['ordinary_link_ids'])+len(report['published_commission_link_ids']))
    def test_product_links_are_stable_across_locales(self):
        for lang in site_i18n.LANGS:
            page=site_i18n.catalogue(lang,self.rows,{},now=CATALOG_AS_OF)
            for d in self.rows:
                if publishable_link(d):
                    self.assertIn('id="product-'+d['id']+'"',page)
                    self.assertIn('href="'+site_i18n.PATHS[lang]+'#product-'+d['id']+'"',page)
            self.assertIn(site_i18n.PRODUCT_PERMALINK[lang],page)
