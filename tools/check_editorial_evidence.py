#!/usr/bin/env python3
"""Fail closed for an explicitly selected editorial revision, never certify legacy articles."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def validate(record, article, deployment, today=None):
    today = today or date.today()
    errors = []
    if record.get('schema_version') != 1:
        errors.append('schema_version must be 1')
    if record.get('slug') != article.get('slug') or record.get('slug') != deployment.get('slug'):
        errors.append('slug mismatch')
    for key, value in [('article_sha256', article), ('deployment_sha256', deployment)]:
        if record.get(key) != digest(value):
            errors.append(f'{key}: revision changed or not reviewed')
    if record.get('decision') not in {'conditional_choice', 'no_comparable_evidence', 'insufficient_evidence'}:
        errors.append('missing valid decision')
    author, reviewer = record.get('author'), record.get('reviewer')
    if not isinstance(author, str) or not author.strip() or not isinstance(reviewer, str) or not reviewer.strip() or author == reviewer:
        errors.append('independent author and reviewer required')
    if record.get('review_status') != 'approved' or record.get('coverage') != 'all_published_high_risk_claims':
        errors.append('explicit completed high-risk source review required')
    for key in ['revised_at', 'reviewed_at']:
        try:
            if date.fromisoformat(record[key]) > today:
                raise ValueError()
        except (KeyError, ValueError, TypeError):
            errors.append(f'{key}: valid non-future date required')
    claims = record.get('claims')
    if not isinstance(claims, list) or not claims:
        errors.append('nonempty claim evidence required')
        return errors
    ids = set()
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append('claim must be an object')
            continue
        cid = claim.get('id')
        if not isinstance(cid, str) or not cid or cid in ids:
            errors.append('claim IDs must be unique nonempty strings')
        else:
            ids.add(cid)
        if claim.get('status') != 'supported':
            errors.append(f'{cid}: unsupported/expired/contradicted claim cannot pass')
        for key in ['claim', 'support', 'scope', 'source_kind']:
            if not isinstance(claim.get(key), str) or not claim[key].strip():
                errors.append(f'{cid}: {key} required')
        if claim.get('source_kind') != 'official_primary':
            errors.append(f'{cid}: official primary evidence required')
        url = urlparse(str(claim.get('source_url', '')))
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            errors.append(f'{cid}: invalid primary source URL')
        try:
            checked = date.fromisoformat(claim['source_checked_at'])
            expires = date.fromisoformat(claim['evidence_expires_at'])
            if not checked <= today <= expires or checked > expires:
                raise ValueError()
        except (KeyError, ValueError, TypeError):
            errors.append(f'{cid}: stale, future or invalid evidence dates')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slug', required=True)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
        parser.error('invalid slug')
    try:
        article = json.loads((args.root / 'content/final' / f'{args.slug}.json').read_text())
        record = json.loads((args.root / 'content/evidence' / f'{args.slug}.json').read_text())
        deployments = json.loads((args.root / 'data/tools.json').read_text())
        deployment = next(item for item in deployments if item['slug'] == args.slug)
        errors = validate(record, article, deployment)
    except (OSError, ValueError, StopIteration, KeyError, TypeError) as exc:
        errors = [f'missing/invalid evidence or article: {exc}']
    if errors:
        for error in errors:
            print(f'BLOCKED: {error}')
        return 1
    print('Evidence record and reviewed revision match. This is not independent verification of source truth.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
