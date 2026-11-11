"""Fail-closed publication gate. URL shape is not proof of product identity/stock.
A reviewer must record the final seller URL, exact product/variant match and dated
source evidence. HTTP 200 alone, a search hit or a blocked request is insufficient.
"""
import re
from urllib.parse import urlsplit, parse_qs, unquote
from tools.validate_data import is_safe_url
from tools.evidence_dates import observed_timestamp
from tools.affiliate_links import ALIEXPRESS_PRODUCT_HOSTS, aliexpress_product_url, validate_affiliate_link

DETAIL_ROUTES = {
    'www.coupang.com': r'/vp/products/\d+/?',
    'www.stacksocial.com': r'/sales/[a-z0-9][a-z0-9-]+/?',
    'store.dji.com': r'/(?:[a-z]{2}/)?product/[a-z0-9][a-z0-9-]+/?',
    'item.lenovo.com.cn': r'/product/\d+\.html',
    'www.ebgames.com.au': r'/product/[^/]+/\d+-[^/]+/?',
}
DETAIL_ROUTES.update({host: r'/item/\d+\.html' for host in ALIEXPRESS_PRODUCT_HOSTS})

def direct_product_url(url):
    if not is_safe_url(url): return False
    u = urlsplit(url)
    try:
        if u.scheme != 'https' or u.port not in (None, 443): return False
    except ValueError: return False
    path = unquote(u.path).lower()
    query = {k.lower() for k in parse_qs(u.query)}
    if query & {'q','query','keyword','keywords','search','searchtext','searchquery','redirect','url','target'}: return False
    if u.hostname in ALIEXPRESS_PRODUCT_HOSTS: return aliexpress_product_url(url)
    pattern = DETAIL_ROUTES.get(u.hostname)
    return bool(pattern and re.fullmatch(pattern, path))

def publishable_link(deal):
    link = deal.get('link') or {}
    evidence = deal.get('link_review') or {}
    if observed_timestamp(evidence.get('checked_at')) is None: return False
    return (direct_product_url(link.get('url')) and evidence.get('status') == 'verified_detail'
            and evidence.get('url') == link.get('url') and evidence.get('product_match') is True
            and isinstance(evidence.get('evidence'), str) and bool(evidence['evidence'].strip()))

def validate_deal_links(feeds):
    errors = []
    for d in feeds:
        errors.extend(validate_affiliate_link(d, publishable_link(d)))
        review = d.get('link_review') or {}
        if review.get('status') == 'held':
            if not review.get('reason'): errors.append(f"{d.get('id')}: held link needs a reason")
        elif not publishable_link(d):
            errors.append(f"{d.get('id')}: product URL needs direct detail route and dated exact-product review; mark held if unverifiable")
    return errors
