import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

import build
import site_i18n
from tools.deal_availability import explicit_offer_expiry


class OfferExpiryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.offer = next(d for d in json.loads(Path('data/deals.json').read_text())['feed']
                         if d['id'] == 'my-little-puppy-steam-kr')
        cls.translations = json.loads(Path('data/deal_localizations.json').read_text())
        cls.end = datetime(2026, 11, 23, 17, tzinfo=timezone.utc)

    def test_only_explicit_valid_zoned_values(self):
        self.assertEqual(explicit_offer_expiry('2026-11-24T02:00:00+09:00'), self.end)
        self.assertEqual(explicit_offer_expiry('2026-11-23T17:00:00Z'), self.end)
        for value in (None, '2026-11-23', '2026-11-23T17:00:00',
                      '2026-11-23T17:00:00-00:00', '2026-11-23T17:00:00+08:65',
                      '2026-11-31T17:00:00Z', '2026-11-23T24:00:00Z', 0):
            with self.subTest(value=value):
                self.assertIsNone(explicit_offer_expiry(value))
                if value != 0:  # Includes missing and date-only seller observations.
                    row = dict(self.offer, expires_at=value, campaign_end_date='2026-11-23')
                    page = site_i18n.catalogue('en', [row], self.translations, now=self.end)
                    self.assertIn('class="cta"', page)
                    self.assertNotIn('data-expires-at=', page)

    def test_server_before_exact_after_in_six_locales(self):
        for language in site_i18n.LANGS:
            for seconds in (-1, 0, 1):
                with self.subTest(language=language, seconds=seconds):
                    page = site_i18n.catalogue(language, [self.offer], self.translations,
                                                now=self.end + timedelta(seconds=seconds))
                    card, = re.findall(r'<article\b[^>]*data-id="my-little-puppy-steam-kr".*?</article>', page, re.S)
                    self.assertEqual(page.count('id="product-my-little-puppy-steam-kr"'), 1)
                    self.assertEqual(page.index(card) > page.index('id="held-products"'), seconds >= 0)
                    self.assertEqual('class="cta"' in card, seconds < 0)
                    self.assertEqual('17,400' in card, seconds < 0)
                    self.assertEqual('data-expires-at=' in card, seconds < 0)
                    if seconds >= 0:
                        self.assertNotIn('store.steampowered.com', card)
                        self.assertNotIn('purchase-details', card)
                        self.assertIn(site_i18n.OFFER_ENDED[language], card)

    def test_machine_readable_export_uses_same_boundary(self):
        feed = {'feed':[copy.deepcopy(self.offer)]}
        for seconds in (-1, 0, 1):
            content = build.generate_llms_full_txt([], feed, {}, now=self.end + timedelta(seconds=seconds))
            self.assertEqual('store.steampowered.com' in content, seconds < 0)
            self.assertEqual('1 ended offers are omitted' in content, seconds >= 0)

    @unittest.skipUnless(shutil.which('node'), 'node unavailable')
    def test_runtime_reregisters_expiry_under_archive_and_hash(self):
        script = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const code = require('node:fs').readFileSync(0,'utf8');
const end = Date.parse('2026-11-23T17:00:00+00:00');
let now = end - 1;
const oldPromo = {tagName:'DETAILS', classList:{contains:()=>false}, remove(){card.children.splice(card.children.indexOf(this),1)}};
const oldCta = {...oldPromo,tagName:'A'};
const heading = {tagName:'H2',textContent:'Puppy'};
const card = {dataset:{id:'puppy', kind:'active', country:'KR', market:'KR', category:'games', countries:'KR',
                       search:'puppy', expiresAt:'2026-11-23T17:00:00+00:00', expiredLabel:'Offer ended'},
              children:[heading,oldPromo,oldCta], scrolled:false, querySelector(){return heading},
              append(node){this.children.push(node)}, scrollIntoView(){this.scrolled=true}};
const selectors = new Map();
for(const id of ['market','country','category','product-search','archive-count','discovery-count','count','unknown-destinations','empty','reset-filters','held-products']){
  selectors.set('#'+id,{value:'all', options:[{value:'all'},{value:'US'}], dataset:{label:'active',discoveryLabel:'discovery'}, addEventListener(){}});
}
for(const id of ['.held-archive','.discovery-section']) selectors.set(id,{open:false});
let moved = [];
selectors.get('#held-products').append = node => moved.push(node);
const events={}, timers=[];
const location = {search:'?q=puppy',hash:'#product-puppy',pathname:'/deals/'};
const document = {querySelector:x=>selectors.get(x),querySelectorAll:x=>
  x==='#active-products .card, #discovery-products .card'?[card]:[],
  createElement:()=>({})};
vm.runInNewContext(code,{document, location, history:{replaceState(){}}, window:{addEventListener:(x,y)=>events[x]=y},
  URLSearchParams, Date:{parse:Date.parse, now:()=>now},setInterval(fn, interval){timers.push([fn,interval]);}});
assert.equal(selectors.get('#count').textContent,'1 active · 0 discovery');
assert.equal(moved.length,0);
const tick=timers.find(t=>t[1]===1000)[0];
now=end; tick();
assert.equal(selectors.get('#count').textContent,'0 active · 0 discovery');
assert.equal(selectors.get('#archive-count').textContent,1);
assert.deepEqual(moved,[card]);
assert.equal(card.children.length,2);
assert.equal(card.children[1].textContent,'Offer ended');
assert.equal(selectors.get('.held-archive').open,true);
assert.equal(card.scrolled,true);
now=end+1;tick();assert.equal(moved.length,1);
location.hash='';location.search='?country=US';events.popstate();
assert.equal(selectors.get('#archive-count').textContent,0);assert.equal(card.hidden,true);
location.hash='#product-puppy';events.hashchange();
assert.equal(selectors.get('#archive-count').textContent,1);assert.equal(card.hidden,false);
"""
        subprocess.run(['node','-e',script],input=site_i18n.JS,text=True,check=True)
