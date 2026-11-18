"""Verify the deployed feed, fail closed, and expose transport diagnostics."""
import argparse
import hashlib
import html
import re
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

BASE = 'https://devteardown.com/feeds/'

def fetch(name, stamp):
    result = subprocess.run(['curl', '--fail', '--silent', '--show-error',
        '--location', '--proto', '=https', '--proto-redir', '=https',
        '--connect-timeout', '10', '--max-time', '20',
        '--header', 'Cache-Control: no-cache',
        BASE + name + '?check=' + quote(stamp, safe='')],
        capture_output=True, timeout=25)
    if result.returncode:
        raise RuntimeError(f'curl exit {result.returncode}: {result.stderr.decode(errors="replace")[:300]}')
    return result.stdout

def canonical_html(body):
    """Undo only the CDN's observed, lossless public-email obfuscation.

    No elements or arbitrary scripts are ignored. All other bytes must match.
    JSON and XML always retain raw-byte verification.
    """
    text = body.decode('utf-8')
    pattern = r'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</a>'
    def decode(match):
        encoded = bytes.fromhex(match.group(1))
        if len(encoded) < 2:
            raise ValueError('Invalid CDN email encoding')
        email = bytes(x ^ encoded[0] for x in encoded[1:]).decode('utf-8')
        if '@' not in email or any(ord(c) < 32 for c in email):
            raise ValueError('Invalid CDN email text')
        return html.escape(email)
    text = re.sub(pattern, decode, text)
    text = text.replace('<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>', '')
    return text.encode('utf-8')

def verify(expected, get, html_sha256):
    live = json.loads(get('status.json'))
    if live.get('attempted_at') != expected['attempted_at']:
        raise ValueError(f"stale status: observed {live.get('attempted_at')!r}, expected {expected['attempted_at']!r}")
    source = next(s for s in live['sources'] if s['id'] == 'dealnews')
    wanted = next(s for s in expected['sources'] if s['id'] == 'dealnews')
    if source.get('sha256') != wanted.get('sha256'):
        raise ValueError('Live source fingerprint does not match committed collection')
    if hashlib.sha256(get('dealnews.xml')).hexdigest() != wanted['sha256']:
        raise ValueError('Live XML does not match committed collection')
    html_bytes = get('index.html')
    if hashlib.sha256(html_bytes).hexdigest() != html_sha256:
        raise ValueError('Live page fingerprint does not match committed HTML')
    html = html_bytes.decode('utf-8')
    if wanted['last_success_at'] not in html:
        raise ValueError('Live page does not contain the committed last-success timestamp')
    if source['status'] not in ('collected', 'not_modified'):
        raise ValueError('Last-good data published with error notice; collection was not successful')
    return source

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--wait-seconds', type=int, default=600)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    html_sha256 = hashlib.sha256(args.expected.with_name('index.html').read_bytes()).hexdigest()
    benefit_dirs = [args.expected.parent/name for name in ('startup-benefits','saasoffers')]
    deadline = time.monotonic() + args.wait_seconds
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        try:
            source = verify(expected, lambda name: fetch(name, expected['attempted_at']), html_sha256)
            for benefits in benefit_dirs:
                if benefits.exists():
                    for name in ('data.json','index.html'):
                        resource = benefits.name+'/'+name
                        actual = fetch(resource, expected['attempted_at'])
                        wanted = (benefits/name).read_bytes()
                        if name == 'index.html':
                            actual = canonical_html(actual)
                        actual_hash = hashlib.sha256(actual).hexdigest()
                        wanted_hash = hashlib.sha256(wanted).hexdigest()
                        if actual_hash != wanted_hash:
                            raise ValueError(f'{resource}: live SHA256 {actual_hash} ({len(actual)} bytes), expected {wanted_hash} ({len(wanted)} bytes)')
            print(f"Verified live status, XML fingerprint and page timestamp: {expected['attempted_at']}; {source['items']} items", flush=True)
            return
        except (ValueError, KeyError, StopIteration, RuntimeError, subprocess.TimeoutExpired) as error:
            print(f'Live verification attempt {attempt}: {type(error).__name__}: {error}', flush=True)
        time.sleep(min(10, max(0, deadline-time.monotonic())))
    raise SystemExit('Pages build requested, but live feed was not verified before the deadline')

if __name__ == '__main__':
    main()
