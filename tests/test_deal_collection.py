import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from tools import collect_deal_feeds as c
import build

RSS=b'<rss><channel><item><title>Test</title><link>https://shop.test/p</link></item></channel></rss>'
CONFIG={'sources':[{'id':'test','enabled':True,'mode':'unaltered_feed_archive','url':'https://feed.test/rss','note':'Official test feed'}]}

class CollectionTests(unittest.TestCase):
    def test_parse_rejects_empty_and_entities(self):
        for value in [b'<rss><channel/></rss>',b'<!DOCTYPE rss><rss/>',b'<!ENTITY x "x"><rss/>',b'<html/>']:
            with self.assertRaises(ValueError):c.parse_feed(value)
    def test_success_preserves_exact_feed_and_never_publishes(self):
        with tempfile.TemporaryDirectory() as d, patch.object(c,'robots_allowed',return_value=True), patch.object(c,'read_url',return_value=(RSS,{'ETag':'one'})),patch.object(c.time,'sleep'):
            p=Path(d); r=c.collect(CONFIG,p)
            self.assertEqual((p/'test.xml').read_bytes(),RSS)
            self.assertFalse(r['published_deals_changed'])
            self.assertEqual(r['sources'][0]['items'],1)
    def test_disabled_source_is_not_fetched(self):
        config=json.loads(json.dumps(CONFIG));config['sources'][0]['enabled']=False
        with tempfile.TemporaryDirectory() as d,patch.object(c,'read_url') as get:
            self.assertEqual(c.collect(config,Path(d))['sources'][0]['status'],'disabled');get.assert_not_called()
    def test_robots_disallow_does_not_fetch_feed(self):
        with tempfile.TemporaryDirectory() as d,patch.object(c,'robots_allowed',return_value=False),patch.object(c,'read_url') as get:
            self.assertEqual(c.collect(CONFIG,Path(d))['sources'][0]['status'],'error');get.assert_not_called()
    def test_block_preserves_last_success(self):
        with tempfile.TemporaryDirectory() as d,patch.object(c,'robots_allowed',return_value=True),patch.object(c,'read_url',side_effect=HTTPError('https://feed.test/rss',403,'Forbidden',{},None)),patch.object(c.time,'sleep'):
            p=Path(d);prev=p/'previous.json';prev.write_text(json.dumps({'sources':[{'id':'test','last_success_at':'2026-01-01','items':5}]}))
            r=c.collect(CONFIG,p,prev)['sources'][0]
            self.assertEqual(r['status'],'blocked');self.assertEqual(r['last_success_at'],'2026-01-01');self.assertEqual(r['items'],5)
    def test_304_carries_forward_hash_verified_cached_feed(self):
        with tempfile.TemporaryDirectory() as d,patch.object(c,'robots_allowed',return_value=True),patch.object(c,'read_url',side_effect=HTTPError('https://feed.test/rss',304,'Not Modified',{},None)) as get,patch.object(c.time,'sleep'):
            p=Path(d);cached=p/'cache';cached.mkdir();(cached/'test.xml').write_bytes(RSS)
            prev=cached/'status.json';prev.write_text(json.dumps({'sources':[{'id':'test','sha256':c.hashlib.sha256(RSS).hexdigest(),'etag':'one','items':1}]}))
            result=c.collect(CONFIG,p/'out',prev)
            self.assertEqual((p/'out/test.xml').read_bytes(),RSS)
            self.assertEqual(result['sources'][0]['status'],'not_modified')
            self.assertEqual(get.call_args.args[1]['If-None-Match'],'one')

    def test_country_unknown_not_worldwide(self):
        d={'region':'global','link':{'url':'https://shop.test/product','label_kind':'retailer'},'product':'test'}
        page=build._deal_card(d,lang='en')
        self.assertIn('Country eligibility unverified',page)
        self.assertNotIn('Available worldwide',page)
    def test_country_values_escaped(self):
        page=build._eligibility_rows({'purchase_eligibility':{'label':'<img onerror=x>'}})
        self.assertNotIn('<img',page)
    def test_source_schedule_documented(self):
        page=build._source_monitor_html()
        self.assertIn('every six hours',page)
        self.assertIn('not verified product offers',page)
        config=json.loads((c.ROOT/'config/deal_sources.json').read_text())
        self.assertEqual([s['id'] for s in config['sources'] if s['enabled']],['dealnews'])
