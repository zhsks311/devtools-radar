"""Accept reviewed publisher-issued links without manufacturing tracking URLs.

The canonical product URL and its identity/price review stay independent from the
paid destination. Validation is an editorial attestation, not an API verification
of commission attribution or a guarantee that a short link is still active.
"""
import re
from urllib.parse import parse_qsl, urlsplit

from tools.evidence_dates import observed_timestamp
from tools.validate_data import is_safe_url

ALIEXPRESS_PRODUCT_HOSTS = frozenset({
    'aliexpress.com', 'www.aliexpress.com', 'ko.aliexpress.com',
    'ja.aliexpress.com', 'es.aliexpress.com', 'fr.aliexpress.com',
    'www.aliexpress.us',
})


def aliexpress_product_url(url):
    if not is_safe_url(url):
        return False
    parsed = urlsplit(url)
    return (parsed.scheme == 'https' and parsed.hostname in ALIEXPRESS_PRODUCT_HOSTS
            and not parsed.netloc.endswith(':') and parsed.netloc == parsed.hostname
            and not parsed.fragment and
            all(key.lower() in {'sku_id', 'skuid'} and value.isdigit()
                for key, value in parse_qsl(parsed.query, keep_blank_values=True)) and
            bool(re.fullmatch(r'/item/[0-9]+\.html', parsed.path)))


def aliexpress_promotion_url(url):
    """Only the observed official link-generator URL family; no arbitrary redirects."""
    if not is_safe_url(url):
        return False
    parsed = urlsplit(url)
    return (parsed.scheme == 'https' and parsed.netloc == 's.click.aliexpress.com'
            and bool(re.fullmatch(r'/e/[A-Za-z0-9_-]+', parsed.path))
            and not parsed.query and not parsed.fragment)


def verified_aliexpress_url(deal):
    affiliate = deal.get('affiliate')
    if not isinstance(affiliate, dict) or affiliate.get('status') != 'verified':
        return None
    review = affiliate.get('review')
    if not isinstance(review, dict):
        return None
    source = (deal.get('link') or {}).get('url')
    if not (affiliate.get('network') == 'aliexpress' and
            aliexpress_product_url(source) and
            affiliate.get('source_url') == source and
            aliexpress_promotion_url(affiliate.get('promotion_url')) and
            review.get('promotion_url') == affiliate.get('promotion_url') and
            review.get('resolved_product_url') == source and
            review.get('owner_confirmed') is True and
            review.get('product_match') is True and
            observed_timestamp(review.get('checked_at')) is not None and
            isinstance(review.get('evidence'), str) and review['evidence'].strip()):
        return None
    return affiliate['promotion_url']


def validate_affiliate_link(deal, product_verified):
    ident = deal.get('id', '?')
    affiliate = deal.get('affiliate')
    if affiliate is None:
        if aliexpress_product_url((deal.get('link') or {}).get('url')) and (deal.get('link') or {}).get('tracked'):
            return [f'{ident}: AliExpress tracking needs a separately reviewed affiliate link']
        return []
    if not isinstance(affiliate, dict) or affiliate.get('network') != 'aliexpress':
        return [f'{ident}: unsupported affiliate configuration']
    if affiliate.get('status') == 'held':
        reason = affiliate.get('reason')
        return [] if isinstance(reason, str) and reason.strip() else [f'{ident}: held affiliate link needs a reason']
    if product_verified and verified_aliexpress_url(deal):
        return []
    return [f'{ident}: affiliate link needs a verified product, publisher ownership and dated exact-destination review; mark held if unverifiable']
