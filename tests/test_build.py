import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from unittest.mock import patch

import build

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class RendererTests(unittest.TestCase):
    def test_fence_cannot_add_event_attribute(self):
        parser=Parser(); parser.feed(build.md_to_html('```x" onclick="alert(1)\na<b\n```'))
        self.assertEqual(parser.tags, [('pre', {}), ('code', {})])
    def test_link_quote_is_attribute_data(self):
        parser=Parser(); parser.feed(build._inline('[x](https://example.com/"onmouseover="x)'))
        self.assertEqual(set(parser.tags[0][1]), {'href','rel'})
    def test_unsafe_schemes_and_credentials_rejected(self):
        for url in ['javascript:alert(1)', 'data:text/html,x', '//evil.test', 'https://u:p@host/', 'https://host/\nfoo']:
            with self.subTest(url=url), self.assertRaises(ValueError): build._safe_url(url)
    def test_json_ld_cannot_close_script(self):
        payload={'x':'</script><img src=x onerror=alert(1)>&'}
        encoded=build._json_ld(payload, ensure_ascii=False)
        self.assertNotIn('<', encoded); self.assertEqual(json.loads(encoded),payload)
    def test_metadata_is_not_markup(self):
        item=json.loads(build.DATA_PATH.read_text())[0]
        item['tool_a']['name']='<img src=x onerror=alert(1)>'
        item['tool_a']['pros']=['<iframe src=x>']
        for page in [build.generate_comparison_html(item),build.generate_index_html([item])]:
            parser=Parser();parser.feed(page)
            self.assertFalse(any(t in ['img','iframe'] for t,a in parser.tags))
    def test_china_listings_are_honest_and_link_to_products(self):
        payload=json.loads((build.ROOT / 'data/deals_en.json').read_text())
        china=[d for d in payload['feed'] if d.get('category') == 'china']
        self.assertEqual(len(china), 4)
        self.assertEqual(build._won({'price':29.9, 'currency':'CNY'}), 'CNY 29.90')
        for deal in china:
            self.assertIsNone(deal['discount_pct'])
            self.assertIsNone(deal['original_price'])
            self.assertEqual(deal['purchase_eligibility']['countries_confirmed'], [])
            self.assertIn('/product/', deal['link']['url'])
            card=build._deal_card(deal, lang='en')
            self.assertIn('not a verified discount', card)
            self.assertIn('eligibility unverified', card)
        self.assertNotIn('no independently verified offer is published yet', build._source_monitor_html())

    def test_deals_stats_are_escaped(self):
        parser=Parser();parser.feed(build.generate_deals_en_html({'feed':[], 'stats':{'sources':'<img src=x onerror=alert(1)>'}}))
        self.assertFalse(any(t == 'img' for t,a in parser.tags))
    def test_malicious_deal_url_rejected(self):
        with self.assertRaises(ValueError): build._deal_card({'link':{'url':'javascript:alert(1)'}})

class EditorialTests(unittest.TestCase):
    def test_excerpt_preserves_short_text_and_word_boundaries(self):
        self.assertEqual(build._excerpt("A short **note**."), "A short note.")
        self.assertEqual(build._excerpt("first second third", 14), "first second…")

    def test_index_keeps_all_comparison_links_without_fake_verification(self):
        items=json.loads(build.DATA_PATH.read_text())
        page=build.generate_index_html(items)
        parser=Parser();parser.feed(page)
        links=[attrs.get('href') for tag,attrs in parser.tags if tag=='a']
        for item in items:
            self.assertIn(f"./compare/{item['slug']}/",links)
        self.assertNotIn('Verified Nov 2026',page)
        self.assertNotIn('tested for productivity',page)
        self.assertIn('affiliate links',page)
        self.assertIn('sponsored',page)

    def test_comparison_does_not_repeat_verdict(self):
        item=json.loads(build.DATA_PATH.read_text())[0]
        page=build.generate_comparison_html(item)
        self.assertIn('class="verdict-box"',page)
        self.assertNotIn('class="answer-box"',page)
        self.assertIn('Code and configuration',page)
        self.assertIn(item['last_verified'],page)

    def test_portals_label_collected_prices_without_lowest_price_claim(self):
        ko=build.generate_ko_html(build.load_deals())
        en=build.generate_deals_en_html(build.load_deals(build.DEALS_EN_DATA_PATH))
        for page in (ko,en):
            self.assertNotIn('Updated daily',page)
            self.assertNotIn('매일 갱신',page)
            self.assertNotIn('쿠팡 최저가',page)
        self.assertIn('원문 게시글 기준',ko)
        self.assertIn('Browse the offers',en)
        self.assertNotRegex(en, r'[가-힣]')
        self.assertIn('View product →',en)
        self.assertEqual(en.count('<figure class="deal-media">'), 2)
        self.assertIn('App preview; storage shown is illustrative.', en)
        self.assertIn('A$728', en)
        self.assertIn('checkout was not completed',en)
        for deal in build.load_deals(build.DEALS_EN_DATA_PATH)['feed']:
            self.assertEqual(deal['link']['label_kind'], 'retailer')
            self.assertTrue(deal['link']['url'].startswith(('https://www.stacksocial.com/sales/', 'https://www.ebgames.com.au/product/', 'https://store.dji.com/cn/product/', 'https://item.lenovo.com.cn/product/')))
            self.assertIsNone(deal['discount_pct'])
            self.assertIsNone(deal['published_at'])

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.output=self.base/'out';self.data=self.base/'data.json'
        self.items=json.loads(build.DATA_PATH.read_text())
        self.data.write_text(json.dumps(self.items))
    def run_build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return build.build_site(self.data,self.output)
    def test_complete_build_and_stale_cleanup_preserve_custom_file(self):
        self.run_build(); removed=self.items.pop()['slug']
        for item in self.items:
            item['related']=[r for r in item.get('related',[]) if r['slug']!=removed]
        custom=self.output/'custom.txt';custom.write_text('keep')
        self.data.write_text(json.dumps(self.items));self.run_build()
        self.assertFalse((self.output/'compare'/removed/'index.html').exists())
        self.assertEqual(custom.read_text(),'keep')
        self.assertEqual(len(list((self.output/'compare').glob('*/index.html'))),len(self.items))
    def test_legacy_generated_page_cleaned_without_manifest(self):
        self.run_build();(self.output/build.MANIFEST).unlink()
        stale=self.output/'compare'/'obsolete'/'index.html';stale.parent.mkdir();stale.write_text('<title>DevTools</title>Key metric comparison')
        self.run_build();self.assertFalse(stale.exists())
    def test_invalid_data_does_not_touch_output(self):
        self.run_build();old=(self.output/'index.html').read_bytes()
        self.data.write_text('[]')
        with self.assertRaises(ValueError):self.run_build()
        self.assertEqual((self.output/'index.html').read_bytes(),old)
    def test_render_error_does_not_touch_output(self):
        self.run_build();old=(self.output/'index.html').read_bytes()
        with patch.object(build,'generate_comparison_html',side_effect=ValueError('bad')):
            with self.assertRaises(ValueError):self.run_build()
        self.assertEqual((self.output/'index.html').read_bytes(),old)
    def test_promotion_failure_restores_previous_output(self):
        self.run_build();old=(self.output/'index.html').read_bytes()
        original=Path.rename
        def rename(path, target):
            if path.name == 'site' and Path(target) == self.output:
                raise OSError('simulated promotion failure')
            return original(path,target)
        with patch.object(Path,'rename',rename):
            with self.assertRaises(OSError): self.run_build()
        self.assertEqual((self.output/'index.html').read_bytes(),old)
    def test_repeated_build_has_identical_owned_paths(self):
        first=self.run_build();second=self.run_build();self.assertEqual(first,second)
    def test_git_output_rejected(self):
        with self.assertRaises(ValueError):build.build_site(self.data,build.ROOT/'.git')
    def test_unsafe_manifest_rejected(self):
        self.run_build();(self.output/build.MANIFEST).write_text('["../outside"]')
        with self.assertRaises(ValueError):self.run_build()
    def test_symlink_output_rejected(self):
        real=self.base/'real';real.mkdir();self.output.symlink_to(real)
        with self.assertRaises(ValueError):self.run_build()
    def test_source_output_rejected(self):
        with self.assertRaises(ValueError):build.build_site(self.data, self.base)
    def test_malformed_deals_rejected(self):
        malformed=self.base/'bad.json';malformed.write_text('{')
        with self.assertRaises(ValueError):build.load_deals(malformed)
    def test_run_from_unrelated_working_directory(self):
        result=subprocess.run([sys.executable,str(build.ROOT/'build.py'),'--output',str(self.output)],cwd=self.base,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue((self.output/'ko'/'index.html').exists())

if __name__=='__main__': unittest.main()
