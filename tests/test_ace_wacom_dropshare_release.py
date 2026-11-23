import json
from datetime import datetime,timedelta
from hashlib import sha256
from pathlib import Path
import re
import unittest

import site_i18n
from tools.deal_prices import seller_price_reference,validated_price_options
from tools.product_links import direct_product_url,publishable_link

class VerifiedAceWacomDropshareRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kr={r['id']:r for r in json.loads(Path('data/deals.json').read_text())['feed']}
        cls.en={r['id']:r for r in json.loads(Path('data/deals_en.json').read_text())['feed']}
        cls.tr=json.loads(Path('data/deal_localizations.json').read_text())

    def test_insta360_only_same_config_current_seller_comparisons(self):
        for i, price, reference in (
            ('insta360-ace-pro-kr-standard',299000,401000),
            ('insta360-ace-pro-2-kr-dual-battery',437000,547000),
            ('insta360-go-ultra-kr-standard-black',523000,616000),
            ('insta360-x5-kr-standard',645000,759000),
        ):
            d=self.kr[i]; stamp=datetime.fromisoformat(d['price_review']['review_completed_at'])
            self.assertEqual(seller_price_reference(d,now=stamp)['price'],reference)
            self.assertEqual(d['price'],price)
            self.assertIsNone(d.get('original_price'))
            self.assertFalse(d.get('price_options'))
            self.assertIsNone(seller_price_reference(d,now=stamp+timedelta(hours=24,seconds=1)))
            for lang in site_i18n.LANGS:
                x=site_i18n.catalogue(lang,[d],self.tr,now=stamp)
                self.assertIn(f'<s>KRW {reference:,}</s>',x)
                self.assertIn(f'<div class="price">KRW {price:,}</div>',x)
                self.assertIn(site_i18n.SELLER_PRICE_LABELS[lang]['seller_displayed_compare'],x)
        a=self.kr['insta360-ace-pro-kr-standard']
        self.assertEqual(a['image']['license'],'CC BY-SA 4.0')
        self.assertEqual(a['image']['credit'],'TaurusEmerald')
        self.assertEqual(a['image']['sha256'],sha256(Path(a['image']['path'][1:]).read_bytes()).hexdigest())
        self.assertIn('first generation',a['price_variant'])

    def test_archived_wacom_keeps_record_without_active_price_or_cta(self):
        d=self.kr['wacom-intuos-small-wired-black-kr']
        self.assertFalse(publishable_link(d))
        self.assertNotIn('expires_at',d)
        self.assertEqual((d['price'],d['latest_offer_check']['price']), (55000,62000))
        self.assertEqual(d['previous_offer_check']['price'],55000)
        for lang in site_i18n.LANGS:
            h=site_i18n.catalogue(lang,[d],self.tr)
            self.assertRegex(h,r'<article[^>]*data-offer-expired="true"')
            self.assertIn(site_i18n.OFFER_ENDED[lang],h)
            self.assertNotIn('55,000',h);self.assertNotIn('62,000',h)
            self.assertNotIn('class="cta"',h)

    def test_dropshare_coupon_not_unconditional_markdown(self):
        d=self.en['dropshare-6-personal-bf2026']
        self.assertEqual(d['price'],39)
        self.assertEqual([x['price'] for x in validated_price_options(d)],[29])
        self.assertIsNone(seller_price_reference(d))
        self.assertTrue(publishable_link(d))
        self.assertFalse(direct_product_url('https://new.dropshare.app/'))
        self.assertFalse(direct_product_url('https://new.dropshare.app/?q=pricing#pricing'))
        for lang in site_i18n.LANGS:
            h=site_i18n.catalogue(lang,[d],self.tr)
            self.assertIn('<div class="price">USD 39</div>',h)
            self.assertIn('<p class="conditional-price">USD 29</p>',h)
            self.assertIn('blackfriday2026',h)
            self.assertNotIn('<s>',h)
            self.assertIn('Dropshare press kit',h)
        im=d['image']; self.assertEqual(im['sha256'],sha256(Path(im['path'][1:]).read_bytes()).hexdigest())
