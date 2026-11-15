import copy,json,re,unittest
from pathlib import Path
import site_i18n
from tools.product_links import publishable_link
class AffiliatePlacementTest(unittest.TestCase):
 def test_tracked_fixture_discloses_before_title_and_next_to_cta(self):
  root=Path(__file__).resolve().parents[1]
  rows=json.loads((root/'data/deals_en.json').read_text())['feed']
  item=copy.deepcopy(next(d for d in rows if publishable_link(d)))
  item['link']['tracked']=True # Rendering-only fixture; never persisted or deployed.
  for lang in site_i18n.LANGS:
   html=site_i18n.catalogue(lang,[item],{})
   card=re.search(r'<article class="card".*?</article>',html,re.S).group()
   text=site_i18n.e(site_i18n.AFFILIATE_DISCLOSURE[lang])
   self.assertEqual(card.count(text),2)
   self.assertLess(card.index(text),card.index('<h2>'))
   self.assertIn('id="product-'+item['id']+'"',card)
   self.assertTrue(card[card.index('>')+1:].startswith('<p class="notice affiliate-disclosure"'))
   self.assertIn('@media(max-width:560px){.grid{grid-template-columns:1fr}',html)
   self.assertIn('overflow-wrap:anywhere',html)
   self.assertIn(text+'</p><a class="cta"',card)
   ident='affiliate-'+item['id']
   self.assertEqual(card.count('id="'+ident+'"'),1)
   self.assertEqual(card.count('aria-describedby="'+ident+'"'),2)
   self.assertEqual(card.count('rel="noopener nofollow sponsored"'),2)
   item['link']['tracked']=False
   ordinary=site_i18n.catalogue(lang,[item],{})
   self.assertNotIn('aria-describedby="'+ident+'"',ordinary)
   self.assertNotIn('id="'+ident+'"',ordinary)
   item['link']['tracked']=True
 def test_fixture_changes_do_not_modify_source_data(self):
  root=Path(__file__).resolve().parents[1]
  path=root/'data/deals_en.json';before=path.read_bytes()
  self.test_tracked_fixture_discloses_before_title_and_next_to_cta()
  self.assertEqual(path.read_bytes(),before)
