import unittest
from product_visuals import illustration

class ProductVisualPurposeTest(unittest.TestCase):
    def test_distinct_use_diagrams(self):
        ids = ['deal-silent-mech-keyboard','baseus-power-bank','deal-artmu-100w-gb102','moonitor-solo','seoagent-tier-1','otter-ab-tier-1']
        arts = [illustration({'id': i, 'category': 'keyboard-mouse' if 'keyboard' in i else 'hardware'}, 'en') for i in ids]
        self.assertEqual(len(set(arts)), len(ids))
        for art in arts:
            self.assertIn('not a product screenshot', art)
            self.assertNotIn('<image', art)
            self.assertNotIn('100W', art)
    def test_unknown_product_keeps_generic_fallback(self):
        self.assertIn('<svg', illustration({'id': 'unknown'}, 'ko'))

    def test_window_manager_is_not_a_physical_keyboard(self):
        art = illustration({'id': 'keyboardstack-premium', 'category': 'software'}, 'en')
        self.assertNotIn('M80 90h200', art)
