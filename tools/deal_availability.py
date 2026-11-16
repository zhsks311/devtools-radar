"""Conservative seller-state classifier for reviewer-extracted visible product text.

Never run this over arbitrary raw HTML: hidden sold-out templates and navigation
buttons can coexist. Pass the exact offer's visible text and observed CTA only.
A quantity limit is a buyer restriction, not an inventory signal. A purchase CTA
is a page observation, not proof that checkout or an unselected variant works.
"""
import re

def classify_visible_offer(text, *, product_matched=False, purchase_cta=False,
                           price_observed=False, option_matched=False,
                           access_ok=True):
    if not access_ok or re.search(r'verify you are human|captcha|access denied|접근.{0,5}제한',text,re.I):
        return 'access_unverified'
    if not product_matched:
        return 'product_unverified'
    if re.search(r'\bsold\s*out\b|\bout\s*of\s*stock\b|품절|売り切れ|售罄',text,re.I):
        return 'sold_out'
    if not option_matched:
        return 'option_unverified'
    if purchase_cta and price_observed:
        return 'purchase_ui_observed'
    return 'availability_unverified'

def blocks_publication(deal):
    review=deal.get('availability_review') or {}
    if review.get('status') in {'sold_out','discontinued','expired'}:
        return True
    # A claimed positive stock state must not be based only on a purchase limit.
    if review.get('status') == 'in_stock' and review.get('basis') == 'purchase_limit':
        return True
    return False
