import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ScopeCorrectionTests(unittest.TestCase):
 def articles(self,slug):
  return [json.loads((ROOT/'content/final'/f'{slug}.json').read_text()),next(a for a in json.loads((ROOT/'data/tools.json').read_text()) if a['slug']==slug)]
 def test_docker_seat_limit_and_allowance(self):
  for a in self.articles('docker-vs-podman'):
   t=json.dumps(a,ensure_ascii=False);self.assertIn('up to 100 users',t.lower());self.assertIn('$57,600',t);self.assertIn('4,000 − 500',t);self.assertNotIn('200 × $15',t);self.assertNotIn('Business quote-only',t)
  self.assertEqual(200*24*12,57600);self.assertEqual((4000-500)//100*4,140)
 def test_b2b_not_b2c_limit(self):
  for a in self.articles('clerk-vs-auth0'):
   t=json.dumps(a).lower();self.assertIn('unlimited organizations',t);self.assertIn('24 hours after signup',t);self.assertNotIn('neither serves 200',t);self.assertNotIn('allow only 10',t)
 def test_org_seats_not_personal(self):
  for a in self.articles('cursor-vs-github-copilot'):
   t=json.dumps(a,ensure_ascii=False);self.assertIn('Business 10 × $19',t);self.assertNotIn('Pro 10 × $10',t);self.assertIn('low bill alone does not establish',t)
 def test_node_api_is_not_blanket_rebuild(self):
  for a in self.articles('bun-vs-node'):
   t=json.dumps(a);self.assertIn('Node-API',t);self.assertIn('ABI stability',t);self.assertNotIn('every addon has a build',t);self.assertNotIn('Every addon built for Node 24',t);self.assertNotIn('needs a build for NODE_MODULE_VERSION',t)
 def test_dhi_community_production_scope(self):
  for a in self.articles('docker-vs-podman'):
   t=json.dumps(a)
   self.assertIn('Community is free for production',t)
   self.assertIn('Select is optional, not a production licence',t)
   self.assertNotIn('from $5k/repo in production',t)
   self.assertNotIn('$60,000/year floor',t)
  html=(ROOT/'dist/compare/docker-vs-podman/index.html').read_text()
  self.assertIn('Must we buy DHI Select',html)
  self.assertNotIn('Production Hardened Images start',html)
  self.assertIn('Select is optional, not a production licence',(ROOT/'dist/llms-full.txt').read_text())
 def test_clerk_inventory_is_not_mru(self):
  for a in self.articles('clerk-vs-auth0'):
   code=a['tool_a']['code_example']
   self.assertIn('registeredUsers: totalCount',code)
   self.assertIn('not a billing-usage measurement',code)
   self.assertNotIn('if (totalCount >',code)
   self.assertIn('filter alone is not an MRU billing meter',code)
  for p in ['dist/compare/clerk-vs-auth0/index.html','dist/llms-full.txt']:
   s=(ROOT/p).read_text()
   self.assertIn('Do not use getUserList().totalCount as MRU',s)
   self.assertNotIn('MRU — check the plan',s)
 def test_neon_free_storage_shared_cap(self):
  for a in self.articles('planetscale-vs-neon'):
   t=json.dumps(a)
   self.assertIn('20 GB account',t)
   self.assertIn('100 projects does not mean 100 GB',t)
   self.assertIn('Compute remains available for reads or pg_dump',t)
   self.assertIn('inserts, updates and deletes',t)
  for p in ['dist/compare/planetscale-vs-neon/index.html','dist/llms-full.txt']:
   self.assertIn('20 GB account total',(ROOT/p).read_text())
