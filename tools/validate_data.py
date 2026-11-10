"""Validate the exact article data rendered by the site (stdlib only)."""
import datetime
import re
from urllib.parse import urlsplit

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def is_safe_url(value):
    if not isinstance(value, str) or any(ord(c) < 33 or c in '\\<>\"\'' for c in value):
        return False
    try:
        u = urlsplit(value)
        return u.scheme in ('https', 'http') and bool(u.hostname) and not u.username and not u.password
    except ValueError:
        return False


def article_errors(item, deployment=False):
    """Shape checks run before style checks so malformed JSON cannot crash lint."""
    errors = []
    if not isinstance(item, dict):
        return ['article must be an object']
    def string(obj, key, where='', required=True):
        if key not in obj and not required:
            return
        if not isinstance(obj.get(key), str) or not obj.get(key, '').strip():
            errors.append(f'{where}{key} must be a nonempty string')
    for key in ('slug', 'hook', 'verdict_summary'):
        string(item, key)
    if isinstance(item.get('slug'), str) and not SLUG.fullmatch(item['slug']):
        errors.append('slug must contain only lowercase words separated by hyphens')
    rows = {'sections': ('title', 'content'), 'decision_matrix': ('situation', 'pick', 'why'),
            'cost_math': ('label', 'formula', 'result'), 'faqs': ('q', 'a')}
    for key, fields in rows.items():
        value = item.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f'{key} must be a nonempty list')
            continue
        for i, row in enumerate(value):
            if not isinstance(row, dict):
                errors.append(f'{key}[{i}] must be an object')
                continue
            for field in fields:
                string(row, field, f'{key}[{i}].')
    sources = item.get('sources')
    if not isinstance(sources, list) or not sources:
        errors.append('sources must be a nonempty list')
    elif any(not is_safe_url(url) for url in sources):
        errors.append('sources must contain absolute HTTP(S) URLs without credentials or unsafe characters')
    for key in ('published', 'last_verified'):
        if deployment or key in item:
            value = item.get(key)
            try:
                if not isinstance(value, str) or datetime.date.fromisoformat(value).isoformat() != value:
                    raise ValueError()
            except (TypeError, ValueError):
                errors.append(f'{key} must be an ISO date (YYYY-MM-DD)')
    if deployment:
        for key in ('category', 'migration_guide'):
            string(item, key)
        for key in ('tool_a', 'tool_b'):
            tool = item.get(key)
            if not isinstance(tool, dict):
                errors.append(f'{key} must be an object')
                continue
            for field in ('name', 'db', 'pricing', 'self_host', 'realtime', 'ai_readiness', 'lock_in', 'cta_url'):
                string(tool, field, key + '.')
            if not is_safe_url(tool.get('cta_url')):
                errors.append(f'{key}.cta_url must be an absolute HTTP(S) URL')
            for field in ('pros', 'cons'):
                vals = tool.get(field, [])
                if not isinstance(vals, list) or any(not isinstance(v, str) for v in vals):
                    errors.append(f'{key}.{field} must be a list of strings')
            for field in ('badge', 'code_example', 'tagline'):
                if field in tool and not isinstance(tool[field], str):
                    errors.append(f'{key}.{field} must be a string')
    related = item.get('related', [])
    if not isinstance(related, list):
        errors.append('related must be a list')
    else:
        for i, rel in enumerate(related):
            if not isinstance(rel, dict):
                errors.append(f'related[{i}] must be an object')
                continue
            for key in ('slug', 'name', 'why'):
                string(rel, key, f'related[{i}].')
            if not isinstance(rel.get('slug'), str) or not SLUG.fullmatch(rel['slug']):
                errors.append(f'related[{i}].slug is invalid')
    return errors


def validate_items(items, check_content=True):
    if not isinstance(items, list) or not items:
        return ['deployment data must be a nonempty list']
    errors = []
    seen = set()
    for i, item in enumerate(items):
        prefix = f'item[{i}]'
        shape = article_errors(item, deployment=True)
        errors.extend(f'{prefix}: {e}' for e in shape)
        if not isinstance(item, dict):
            continue
        slug = item.get('slug')
        if isinstance(slug, str):
            if slug in seen:
                errors.append(f'duplicate slug: {slug}')
            seen.add(slug)
        if check_content and not shape:
            from tools.lint_content import lint_article
            _, issues, _ = lint_article(item)
            errors.extend(f'{slug}: {e}' for e in issues)
    for item in items:
        if isinstance(item, dict) and isinstance(item.get('related', []), list):
            for rel in item.get('related', []):
                if isinstance(rel, dict) and isinstance(rel.get('slug'), str) and rel['slug'] not in seen:
                    errors.append(f"{item.get('slug')}: unknown related slug: {rel['slug']}")
    return errors
