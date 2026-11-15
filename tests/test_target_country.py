import json,unittest
from pathlib import Path
from tools.deal_countries import target_countries,confirmed_countries
from tools.product_links import publishable_link
from tests.test_deal_countries import FilterParser
import site_i18n
class TargetCountryTest(unittest.TestCase):
 def test_domestic_audience_keeps_delivery_evidence_separate(self):
  rows=json.loads(Path('data/deals.json').read_text())['feed']
  self.assertEqual(sum('KR' in target_countries(x) for x in rows),20)
  self.assertEqual(sum(publishable_link(x) and 'KR' in target_countries(x) for x in rows),6)
  self.assertEqual(sum('KR' in confirmed_countries(x) for x in rows),4)
  for lang in site_i18n.LANGS:
   p=FilterParser();p.feed(site_i18n.catalogue(lang,rows,{}))
   self.assertEqual(sum(x['countries']=='KR' for x in p.cards),6)
   self.assertEqual(sum(x['countries']=='KR' for x in p.archived),14)
   for c in p.cards:
    if '100w' in c['id']:self.assertEqual(c['category'],'hardware')
 def test_community_inference_and_import_exception(self):
  d={'source':{'url':'https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&no=123'}}
  self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),())
  d['country_targeting']={'fulfilment':'overseas_only'};self.assertEqual(target_countries(d),())
  d['country_targeting']['fulfilment']='cross_border_to_korea';self.assertEqual(target_countries(d),('KR',))
  for url in ['https://ppomppu.co.kr.evil.test/a','https://www.ozbargain.com.au/node/123']:
   d['source']['url']=url;self.assertEqual(target_countries(d),())
  self.assertEqual(target_countries({'region':'kr','currency':'KRW'}),())
 def test_software_audience_is_not_reseller_activation(self):
  rows=json.loads(Path('data/deals_en.json').read_text())['feed']
  d=next(x for x in rows if x['id']=='de0f62d0487f')
  self.assertEqual(target_countries(d),('KR',));self.assertEqual(confirmed_countries(d),())
  self.assertEqual(sum('KR' in target_countries(x) for x in rows),1)
