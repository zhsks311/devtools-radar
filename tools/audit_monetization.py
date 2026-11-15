"""Report published commission-link coverage, not earned revenue or attribution."""
import json
from pathlib import Path
from tools.product_links import publishable_link
from tools.affiliate_links import verified_aliexpress_url

def audit(rows):
    active = [d for d in rows if publishable_link(d)]
    commission = [d['id'] for d in active if verified_aliexpress_url(d) or (d.get('link') or {}).get('tracked')]
    held = [d['id'] for d in rows if not publishable_link(d) and ((d.get('link') or {}).get('tracked') or d.get('affiliate'))]
    return {'published_products': len(active), 'published_commission_link_ids': commission,
            'held_commission_link_ids': held,
            'ordinary_link_ids': [d['id'] for d in active if d['id'] not in commission],
            'attribution_and_earnings': 'not_verified'}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    rows = sum([json.loads((root/'data'/name).read_text())['feed'] for name in ('deals.json','deals_en.json')], [])
    print(json.dumps(audit(rows),ensure_ascii=False,indent=2))
