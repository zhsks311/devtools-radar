import unittest
from datetime import datetime, timezone
from tools.evidence_dates import observed_timestamp


class EvidenceDatesTests(unittest.TestCase):
    def test_aware_past_boundary_and_equivalent_offsets(self):
        now = datetime(2026, 11, 11, 12, tzinfo=timezone.utc)
        for value in ('2026-11-10T12:00:00Z', '2026-11-11T12:00:00Z',
                      '2026-11-11T21:00:00+09:00', '2000-01-01T00:00:00Z'):
            with self.subTest(value=value):
                self.assertIsNotNone(observed_timestamp(value, now=now))

    def test_future_and_malformed_fail_closed(self):
        now = datetime(2026, 11, 11, 12, tzinfo=timezone.utc)
        for value in ('2026-11-11T12:00:00.000001Z', '2026-11-11T12:00:00-01:00',
                      '2026-11-11', '2026-11-11T12:00:00', 'yesterday', '',
                      '0001-01-01T00:00:00+01:00', '9999-12-31T23:59:59-01:00',
                      None, False, 0, [], {}):
            with self.subTest(value=value):
                self.assertIsNone(observed_timestamp(value, now=now))
