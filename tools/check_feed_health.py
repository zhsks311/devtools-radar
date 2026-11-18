"""Fail a run on held/failed sources, after healthy sources have published."""
import json
from pathlib import Path
import sys


def assert_healthy(status):
    sources = status.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('Missing collection status')
    failed = [s.get('id', 'unknown') for s in sources
              if s.get('enabled') and s.get('status') not in ('collected', 'not_modified')]
    if failed:
        raise ValueError('Source collection failed or held: ' + ', '.join(failed))


if __name__ == '__main__':
    assert_healthy(json.loads(Path(sys.argv[1]).read_text()))
