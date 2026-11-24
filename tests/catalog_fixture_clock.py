"""Clock for catalog snapshot assertions; never used by the real site build."""

from datetime import datetime, timezone


# The Paste release snapshot was checked in before My Little Puppy's live
# November 23 17:00 UTC cutoff. These snapshots test catalog membership at
# that point, not today's offers. test_offer_expiry checks the actual boundary.
CATALOG_AS_OF = datetime(2026, 11, 23, 12, 15, 5, tzinfo=timezone.utc)
