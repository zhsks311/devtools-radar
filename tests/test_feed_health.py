import unittest
from tools.check_feed_health import assert_healthy


class FeedHealthTests(unittest.TestCase):
    def test_collected_and_not_modified_are_healthy(self):
        for value in ('collected', 'not_modified'):
            assert_healthy({'sources': [{'id': 'dealnews', 'enabled': True, 'status': value}]})

    def test_failed_blocked_and_publisher_held_are_not_success(self):
        for value in ('error', 'blocked', None):
            with self.assertRaises(ValueError):
                assert_healthy({'sources': [{'id': 'dealnews', 'enabled': True, 'status': value}]})

    def test_disabled_sources_do_not_fail_run(self):
        assert_healthy({'sources': [{'id': 'disabled', 'enabled': False, 'status': 'disabled'}]})

    def test_missing_status_is_not_success(self):
        for value in ({}, {'sources': []}):
            with self.assertRaises(ValueError):
                assert_healthy(value)
