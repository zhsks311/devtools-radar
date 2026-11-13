"""Explicitly unverified discoveries, separate from verified offers and their gates."""
import html
import json
import re
from pathlib import Path
from tools.evidence_dates import observed_timestamp

TEXT = {
'en': ('AliExpress · discovery', 'Current price not checked', 'Source-reported product. Price, discount, variant, stock and shipping (including South Korea) are unverified. Not a confirmed hot deal. No affiliate tracking.', 'View product', 'Source', 'Source inspected'),
'ko': ('알리익스프레스 · 발견 상품', '현재 가격 미확인', '외부 출처에서 찾은 상품입니다. 현재 가격·할인·옵션·재고·한국 등 배송 가능 국가는 미확인입니다. 확인된 핫딜이 아니며 제휴 추적이 없는 링크입니다.', '상품 보기', '출처', '출처 확인 시각'),
'zh': ('速卖通 · 发现的商品', '当前价格未确认', '来自第三方来源。价格、折扣、选项、库存和配送国家（包括韩国）均未验证。并非已确认的优惠，无联盟追踪。', '查看商品', '来源', '来源查看时间'),
'ja': ('AliExpress · 見つけた商品', '現在価格は未確認', '第三者の情報です。価格・割引・仕様・在庫・韓国を含む配送先は未確認。確認済みセールではなく、アフィリエイト追跡もありません。', '商品を見る', '出典', '出典確認日時'),
'es': ('AliExpress · descubrimiento', 'Precio actual sin verificar', 'Producto de una fuente externa. Precio, descuento, variante, existencias y envío (incluida Corea del Sur) no verificados. No es una oferta confirmada. Sin seguimiento de afiliados.', 'Ver producto', 'Fuente', 'Fuente consultada'),
'fr': ('AliExpress · découverte', 'Prix actuel non vérifié', 'Produit signalé par une source tierce. Prix, réduction, variante, stock et livraison (Corée du Sud comprise) non vérifiés. Pas une promotion confirmée. Sans suivi affilié.', 'Voir le produit', 'Source', 'Source consultée'),
}

def load_candidates(path=None):
    path = path or Path(__file__).resolve().parents[1] / 'data/aliexpress_candidates.json'
    rows = json.loads(Path(path).read_text())
    seen = set()
    for d in rows:
        pid = d.get('product_id', '')
        if (not re.fullmatch(r'\d{10,20}', pid) or d.get('id') in seen
            or d.get('url') != f'https://www.aliexpress.com/item/{pid}.html'
            or d.get('source_url') != f'https://www.pricearchive.org/aliexpress.com/item/{pid}'
            or observed_timestamp(d.get('observed_at')) is None
            or d.get('category') not in {'hardware', 'keyboard-mouse', 'laptops', 'monitor-desk'}
            or d.get('status') != 'source_reported_candidate'
            or d.get('current_price') is not None or d.get('discount') is not None
            or d.get('shipping_countries') != [] or not d.get('product') or not d.get('evidence')):
            raise ValueError('Invalid or overstated discovery candidate')
        seen.add(d['id'])
    return rows

def candidate_cards(lang):
    e=lambda v: html.escape(str(v), quote=True)
    t=TEXT[lang]
    cards=[]
    for d in load_candidates():
        title=d.get('product_ko') if lang=='ko' else d['product']
        cards.append(f'''<article class="card discovery-candidate" data-kind="discovery" data-id="{e(d['id'])}" data-search="{e(d['product']+' '+d.get('product_ko','')+' AliExpress 알리익스프레스')}" data-market="unknown" data-countries="" data-category="{e(d['category'])}"><div class="meta">{e(t[0])}</div><h2><a href="{e(d['url'])}" rel="noopener nofollow">{e(title)}</a></h2><p class="price">{e(t[1])}</p><p class="notice">{e(t[2])}</p><p class="meta">{e(t[5])}: <time datetime="{e(d['observed_at'])}">{e(d['observed_at'][:16].replace('T',' '))} UTC</time></p><p><a href="{e(d['source_url'])}" rel="noopener nofollow">{e(t[4])}: PriceArchive</a></p><a class="cta" href="{e(d['url'])}" rel="noopener nofollow">{e(t[3])}</a></article>''')
    return cards
