"""Discount evidence gate: recorded prices are not verified savings."""
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from datetime import datetime
from tools.product_links import publishable_link
from tools.validate_data import is_safe_url

def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)): return None
    try:
        n = Decimal(str(value))
        return n if n.is_finite() and n >= 0 else None
    except InvalidOperation: return None

def dated(value):
    try: return datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None
    except (AttributeError, ValueError, TypeError): return False

def checked_price(d):
    r=d.get('price_review') or {}
    return (r.get('price_status')=='seller_page_display_confirmed' and
            number(d.get('price')) is not None and number(r.get('verified_price'))==number(d.get('price')) and
            r.get('currency')==d.get('currency','KRW') and r.get('seller_url')==(d.get('link') or {}).get('url') and
            dated(r.get('review_completed_at')) and bool(r.get('evidence')) and publishable_link(d))

def discount_percent(d):
    """Only exact comparable price evidence can enable a strike-through/percentage."""
    p, old=number(d.get('price')), number(d.get('original_price'))
    r=d.get('discount_review') or {}
    if p is None or old is None or old <= p or not checked_price(d): return None
    if not (r.get('status')=='verified' and r.get('same_product_variant') is True and
            r.get('same_terms') is True and r.get('currency')==d.get('currency','KRW') and
            number(r.get('reference_price'))==old and number(r.get('sale_price'))==p and
            dated(r.get('checked_at')) and is_safe_url(r.get('source_url')) and r.get('evidence') and
            r.get('reference_kind')=='seller_previous_price'): return None
    percent=((old-p)*100/old).quantize(Decimal('0.01'),rounding=ROUND_DOWN)
    return percent if percent > 0 else None

def validate_deal_prices(feed):
    errors=[]
    for d in feed:
        ident=d.get('id','?'); r=d.get('price_review') or {}
        if number(d.get('price')) is None: errors.append(f'{ident}: invalid price')
        if r.get('price_status')=='seller_page_display_confirmed' and not checked_price(d):
            errors.append(f'{ident}: checked price must match dated seller evidence, currency and product URL')
        if d.get('original_price') is not None or d.get('discount_pct') is not None:
            pct=discount_percent(d)
            if pct is None: errors.append(f'{ident}: unsupported discount; move legacy values to historical_claims')
            elif number(d.get('discount_pct'))!=pct: errors.append(f'{ident}: discount_pct must equal computed {pct}')
    return errors
