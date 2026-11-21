import json
from pathlib import Path
import re
import unittest

import site_i18n


class PDFExpertReturnsTests(unittest.TestCase):
    def test_exact_sku_terms_stay_with_six_localized_cards(self):
        item_id = 'bde198764514'
        url = 'https://www.stacksocial.com/sales/pdf-expert-premium-plan-lifetime'
        data = json.loads(Path('data/deals_en.json').read_text())
        localizations = json.loads(Path('data/deal_localizations.json').read_text())
        card = next(item for item in data['feed'] if item['id'] == item_id)
        category_card = next(item for item in data['categories']['software']['items'] if item['id'] == item_id)
        self.assertEqual(card, category_card)
        self.assertEqual(card['link']['url'], url)
        self.assertEqual(card['service_terms']['url'], url)
        self.assertEqual(card['service_terms']['refund'], card['purchase_eligibility']['returns'])
        self.assertIn('within 30 days', card['service_terms']['refund'])
        self.assertIn('store credit only', card['service_terms']['refund'])
        self.assertIn('once redeemed, all sales are final', card['service_terms']['refund'])
        self.assertFalse(card['purchase_eligibility']['countries_confirmed'])
        self.assertEqual(card['price'], 79.99)
        tokens = {
            'en': ('store credit only', 'No returns after redemption'),
            'ko': ('스토어 크레딧으로만', '등록 후에는 환불할 수 없습니다'),
            'zh': ('仅退店铺余额', '兑换后不退款'),
            'ja': ('ストアクレジットのみ', '引き換え後は返金できません'),
            'es': ('solo devuelve crédito de tienda', 'no admite devolución'),
            'fr': ('uniquement en avoir', 'Aucun remboursement après activation'),
        }
        for lang, expected in tokens.items():
            with self.subTest(lang=lang):
                page = site_i18n.catalogue(lang, [card], localizations)
                details, = re.findall(r'<details class="purchase-details">.*?</details>', page, re.S)
                self.assertIn(f'class="service-terms-source" href="{url}"', details)
                for phrase in expected:
                    self.assertIn(phrase, details)
