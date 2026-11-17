import unittest
from tools.publish_deal_feed import render,UnsafeFeed
class FeedPublicationTests(unittest.TestCase):
 def feed(self,desc):
  return ('<rss><channel><title>DealNews</title><description>Original</description><item><title>Exact title</title><link>https://www.dealnews.com/1.html?iref=rss</link><description><![CDATA['+desc+']]></description><pubDate>Original date</pubDate></item></channel></rss>').encode()
 def test_preserves_full_source_content_and_referral(self):
  desc='<p>Original $99 offer <a href="https://www.dealnews.com/lw/click.html?code=unchanged">Shop</a></p>'
  out=render(self.feed(desc),{'last_success_at':'2026-11-17T09:00:00Z','status':'collected'})
  self.assertIn(desc,out);self.assertIn('https://www.dealnews.com/1.html?iref=rss',out)
  self.assertIn('not DevTeardown-verified',out);self.assertIn('noindex',out);self.assertIn('국내 커뮤니티 자동 게시는 아직 지원하지 않습니다',out)
 def test_rejects_entire_unsafe_feed_without_rewriting(self):
  for desc in ['<script>alert(1)</script>','<img src="https://x.test/x" onerror="alert(1)">','<a href="javascript:alert(1)">bad</a>','<div style="background:url(https://x.test)">x</div>']:
   with self.assertRaises(UnsafeFeed):render(self.feed(desc),{'last_success_at':'2026-11-17T09:00:00Z'})
 def test_failure_and_staleness_are_not_claimed_current(self):
  out=render(self.feed('<p>original</p>'),{'last_success_at':'2026-11-17T09:00:00Z','status':'error'})
  self.assertIn('Last-good feed retained',out);self.assertIn('12*3600000',out)
 def test_unsafe_new_feed_preserves_previous_with_error_notice(self):
  import tempfile,json,hashlib
  from pathlib import Path
  from tools.publish_deal_feed import publish
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);out=root/'out';dest=root/'published';out.mkdir();dest.mkdir()
   good=self.feed('<p>previous valid content</p>');bad=self.feed('<script>bad()</script>')
   old={'id':'dealnews','status':'collected','last_success_at':'2026-11-17T08:00:00Z','sha256':hashlib.sha256(good).hexdigest(),'items':1}
   (dest/'dealnews.xml').write_bytes(good);(dest/'status.json').write_text(json.dumps({'sources':[old]}))
   new=dict(old,last_success_at='2026-11-17T09:00:00Z',sha256=hashlib.sha256(bad).hexdigest())
   (out/'dealnews.xml').write_bytes(bad);(out/'status.json').write_text(json.dumps({'attempted_at':'2026-11-17T09:00:00Z','sources':[new]}))
   publish(out,dest)
   self.assertEqual((dest/'dealnews.xml').read_bytes(),good)
   live=json.loads((dest/'status.json').read_text())['sources'][0]
   self.assertEqual(live['status'],'error');self.assertEqual(live['last_success_at'],old['last_success_at'])
   self.assertIn('Last-good feed retained',(dest/'index.html').read_text())
 def test_workflow_uses_latest_branch_not_snapshot_and_handles_collection_failure(self):
  from pathlib import Path
  w=Path('.github/workflows/deal-feeds.yml').read_text()
  self.assertIn('continue-on-error: true',w)
  self.assertIn('git pull --rebase origin gh-pages',w)
  self.assertIn('git add feeds/index.html feeds/dealnews.xml feeds/status.json',w)
  self.assertIn('pages/builds',w)
  self.assertIn("'.build_type'",w);self.assertIn('tools/verify_live_feed.py --expected',w)
  self.assertIn('timeout-minutes: 20',w)
  self.assertNotIn('upload-pages-artifact',w);self.assertNotIn('deploy-pages@',w)
  self.assertIn("source['status'] not in",Path('tools/verify_live_feed.py').read_text())
 def test_feed_commit_rebase_preserves_concurrent_site_commit(self):
  import tempfile,subprocess
  from pathlib import Path
  def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],stderr=subprocess.DEVNULL,text=True).strip()
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);remote=root/'remote.git';subprocess.run(['git','init','--bare',str(remote)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   a=root/'a';b=root/'b';subprocess.run(['git','clone',str(remote),str(a)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   git(a,'checkout','-b','gh-pages');git(a,'config','user.email','test@example.com');git(a,'config','user.name','test')
   (a/'index.html').write_text('old site');git(a,'add','.');git(a,'commit','-m','initial');git(a,'push','origin','gh-pages')
   subprocess.run(['git','clone','-b','gh-pages',str(remote),str(b)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   git(b,'config','user.email','test@example.com');git(b,'config','user.name','test')
   (b/'feeds').mkdir();(b/'feeds/index.html').write_text('new feed');git(b,'add','feeds');git(b,'commit','-m','feed')
   (a/'index.html').write_text('new concurrent site');git(a,'add','.');git(a,'commit','-m','site');git(a,'push','origin','gh-pages')
   git(b,'pull','--rebase','origin','gh-pages');git(b,'push','origin','HEAD:gh-pages')
   self.assertEqual((b/'index.html').read_text(),'new concurrent site');self.assertEqual((b/'feeds/index.html').read_text(),'new feed')
