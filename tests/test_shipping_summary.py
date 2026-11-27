import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import site_i18n


class ShippingSummaryTest(unittest.TestCase):
    def test_localized_shipping_visible_before_cta_only_with_current_evidence(self):
        catalogues = (('deals.json', 'logitech-g304-black-pouch-kream-kr'),
                      ('deals_en.json', 'insta360-go-3s-us-128gb-midnight-bh'))
        local = json.loads(Path('data/deal_localizations.json').read_text())
        for file, ident in catalogues:
            data = json.loads(Path('data', file).read_text())
            deal, = (d for d in data['feed'] if d['id'] == ident)
            now = datetime.fromisoformat(deal['link_review']['checked_at'])
            for lang in site_i18n.LANGS:
                with self.subTest(ident=ident, lang=lang):
                    page = site_i18n.catalogue(lang, [deal], local, now=now)
                    card = page.split(f'id="product-{ident}"', 1)[1].split('</article>', 1)[0]
                    line = site_i18n.e(local[ident][lang]['shipping_summary'])
                    self.assertLess(card.index('class="price"'), card.index(line))
                    self.assertLess(card.index(line), card.index('class="cta"'))
                    self.assertLess(card.index(line), card.index('class="purchase-details"'))
                    for old, at in ((deal, now + timedelta(hours=25)),
                                    ({**deal, 'availability_review': {'status': 'sold_out'}, 'link_review': {'status': 'held', 'reason': 'sold out'}}, now)):
                        self.assertNotIn(line, site_i18n.catalogue(lang, [old], local, now=at))
