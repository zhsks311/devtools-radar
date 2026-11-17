import hashlib,json,unittest
from tools.verify_live_feed import verify
class LiveFeedTests(unittest.TestCase):
 def setUp(self):
  self.xml=b'<rss>original</rss>'
  self.expected={'attempted_at':'2026-11-17T10:00:00Z','sources':[{'id':'dealnews','status':'collected','items':1,'sha256':hashlib.sha256(self.xml).hexdigest(),'last_success_at':'2026-11-17T10:00:00Z'}]}
  self.pages={'status.json':json.dumps(self.expected).encode(),'dealnews.xml':self.xml,'index.html':b'<time>2026-11-17T10:00:00Z</time>'}
  self.html_sha=hashlib.sha256(self.pages['index.html']).hexdigest()
 def test_exact_live_files_pass(self):self.assertEqual(verify(self.expected,self.pages.__getitem__,self.html_sha)['items'],1)
 def test_stale_status_fails(self):
  old=dict(self.expected,attempted_at='old');self.pages['status.json']=json.dumps(old).encode()
  with self.assertRaisesRegex(ValueError,'stale status'):verify(self.expected,self.pages.__getitem__,self.html_sha)
 def test_stale_xml_fails(self):
  self.pages['dealnews.xml']=b'old'
  with self.assertRaisesRegex(ValueError,'XML'):verify(self.expected,self.pages.__getitem__,self.html_sha)
 def test_stale_page_fails(self):
  self.pages['index.html']=b'old'
  with self.assertRaisesRegex(ValueError,'page'):verify(self.expected,self.pages.__getitem__,self.html_sha)
 def test_collection_failure_is_not_success(self):
  self.expected['sources'][0]['status']='error';self.pages['status.json']=json.dumps(self.expected).encode()
  with self.assertRaisesRegex(ValueError,'not successful'):verify(self.expected,self.pages.__getitem__,self.html_sha)
