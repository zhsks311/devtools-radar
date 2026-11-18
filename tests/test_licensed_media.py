import unittest
from product_visuals import product_media


class LicensedMediaTests(unittest.TestCase):
    def setUp(self):
        self.media = {
            'path': '/assets/deals/dualsense-midnight-black.webp',
            'kind': 'licensed_product_photo',
            'credit': 'Chris Woodrich',
            'credit_url': 'https://commons.wikimedia.org/wiki/File:Example.jpg',
            'source_page': 'https://commons.wikimedia.org/wiki/File:Example.jpg',
            'rights_basis': 'CC BY-SA',
            'license': 'CC BY-SA 4.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
        }

    def test_license_credit_and_modification_displayed_in_all_languages(self):
        for lang in ('ko', 'en', 'zh', 'ja', 'es', 'fr'):
            html = product_media({'image': self.media}, lang, 'DualSense')
            self.assertIn('Chris Woodrich', html)
            self.assertIn('CC BY-SA 4.0', html)
            self.assertIn('rel="license noopener"', html)
            self.assertNotIn('<svg', html)

    def test_missing_license_falls_back(self):
        self.media.pop('license_url')
        self.assertIn('<svg', product_media({'image': self.media}, 'en', 'DualSense'))
