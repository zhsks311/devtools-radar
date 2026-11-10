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
    def test_deals_stats_are_escaped(self):
        parser=Parser();parser.feed(build.generate_deals_en_html({'feed':[], 'stats':{'sources':'<img src=x onerror=alert(1)>'}}))
        self.assertFalse(any(t == 'img' for t,a in parser.tags))
    def test_malicious_deal_url_rejected(self):
        with self.assertRaises(ValueError): build._deal_card({'link':{'url':'javascript:alert(1)'}})

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
