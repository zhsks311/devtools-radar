"""An observation must identify a real, timezone-aware instant, never the future."""
from datetime import datetime, timezone


def observed_timestamp(value, *, now=None):
    if not isinstance(value, str):
        return None
    try:
        observed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        current = now if now is not None else datetime.now(timezone.utc)
        if observed.tzinfo is None or current.tzinfo is None:
            return None
        observed = observed.astimezone(timezone.utc)
        if observed > current:
            return None
        return observed
    except (ValueError, TypeError, OverflowError):
        return None
