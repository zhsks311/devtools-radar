import copy
import json
import re
import shutil
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import site_i18n
from tools.deal_prices import seller_price_reference


class SellerPriceReferenceTest(unittest.TestCase):
    def setUp(self):
        self.deal, = (d for d in json.loads(Path('data/deals.json').read_text())['feed']
                      if d['id'] == 'insta360-go-3s-kr-128gb-black')
        self.reference = self.deal['price_review']['seller_reference']
        self.observed = datetime.fromisoformat(self.reference['current_checked_at'])
        self.now = self.observed + timedelta(minutes=1)

    def test_same_seller_comparison_precedes_main_price_in_six_locales(self):
        ref = seller_price_reference(self.deal, now=self.now)
        self.assertEqual((ref['currency'], ref['price']), ('KRW', 449000))
        for lang in site_i18n.LANGS:
            page = site_i18n.catalogue(lang, [self.deal], {}, now=self.now)
            comparison = re.search(r'<p class="seller-price-reference current-savings">.*?</p>', page)[0]
            self.assertIn(site_i18n.SELLER_PRICE_LABELS[lang]['seller_displayed_compare'], comparison)
            self.assertIn('<s>KRW 449,000</s>', comparison)
            self.assertIn(f'datetime="{self.observed.isoformat()}"', comparison)
            self.assertIn(comparison + '<div class="price">KRW 359,000</div>', page)

    def test_previously_verified_requires_independent_earlier_observation(self):
        r = self.reference
        r['kind'] = 'seller_previous_price'
        self.assertIsNone(seller_price_reference(self.deal, now=self.now))
        r['reference_observed_at'] = (self.observed - timedelta(days=2)).isoformat()
        result = seller_price_reference(self.deal, now=self.now)
        self.assertEqual(result['kind'], 'seller_previous_price')
        self.assertIn('Previously verified seller price', site_i18n.visible_seller_price_reference(self.deal, 'en', now=self.now))
        r['reference_observed_at'] = (self.observed + timedelta(seconds=1)).isoformat()
        self.assertIsNone(seller_price_reference(self.deal, now=self.now))

    def test_incomparable_and_conditioned_references_fail_closed(self):
        for field, value in (
            ('product_id','copied'), ('variant','64GB'), ('source_url','https://store.insta360.com/kr'),
            ('currency','USD'), ('reference_price',359000), ('reference_price',358999),
            ('current_price',335000), ('same_terms',False), ('unconditional',False),
            ('kind','official_srp'), ('kind','coupon'), ('kind','payment'), ('kind','renewal'),
            ('evidence','  '), ('current_checked_at','2000-01-01T00:00:00Z'),
            ('reference_observed_at','2000-01-01T00:00:00Z'),
        ):
            with self.subTest(field=field, value=value):
                d = copy.deepcopy(self.deal)
                d['price_review']['seller_reference'][field] = value
                self.assertIsNone(seller_price_reference(d, now=self.now))
        d = copy.deepcopy(self.deal)
        del d['price_review']['seller_reference']
        d['original_price'] = 450000
        self.assertIsNone(seller_price_reference(d, now=self.now))

    def test_stale_sold_out_unverified_and_expired(self):
        for now in (self.observed + timedelta(hours=24, seconds=1), self.observed - timedelta(seconds=1)):
            self.assertIsNone(seller_price_reference(self.deal, now=now))
        for change in ({'expires_at':self.observed.isoformat()}, {'expires_at':'2026-11-30'},
                       {'availability_review':{'status':'sold_out'}}, {'latest_offer_check':{'status':'unverified_current'}}):
            d = {**self.deal, **change}
            self.assertIsNone(seller_price_reference(d, now=self.now))
        self.assertNotIn('<s>KRW 449,000</s>', site_i18n.catalogue('en', [self.deal], {}, now=self.observed + timedelta(days=2)))

    def test_client_hides_comparison_after_24_hours(self):
        if not shutil.which('node'): self.skipTest('node unavailable')
        fn = site_i18n.JS.split('function expireObservedPrices() {',1)[1].split('\nexpireObservedPrices();',1)[0]
        js = 'function expireObservedPrices() {'+fn+'''
const assert = require('node:assert/strict');
const crossedOutRow = {hidden:false};
const node = {dataset:{observedAt:'2026-11-23T09:30:00Z',staleLabel:'last checked',priceState:'observed'},closest(){return {querySelectorAll(q){assert.equal(q,'.current-savings');return [crossedOutRow]}}}};
globalThis.document = {querySelectorAll(){return [node]}};
Date.now = () => Date.parse('2026-11-24T09:30:00Z');
expireObservedPrices(); assert.equal(crossedOutRow.hidden,false);
Date.now = () => Date.parse('2026-11-24T09:30:01Z');
expireObservedPrices(); assert.equal(crossedOutRow.hidden,true); assert.equal(node.textContent,'last checked');
'''
        subprocess.run(['node','-e',js],check=True,capture_output=True)
