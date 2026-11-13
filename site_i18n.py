"""Shared six-language navigation and one market-aware deal catalogue."""
import html, json, re, datetime
from pathlib import Path
from tools.product_links import publishable_link
from tools.deal_candidates import candidate_cards
from tools.affiliate_links import verified_aliexpress_url
from tools.deal_prices import checked_price, official_srp_comparison
from tools.evidence_dates import observed_timestamp
from tools.deal_countries import confirmed_countries, storefront_country
from xml.sax.saxutils import escape
LANGS={'en':'English','ko':'한국어','zh':'中文','ja':'日本語','es':'Español','fr':'Français'}
FLAGS={'en':'🇺🇸','ko':'🇰🇷','zh':'🇨🇳','ja':'🇯🇵','es':'🇪🇸','fr':'🇫🇷'}
AFFILIATE_DISCLOSURE = {
 'en': 'Paid link: DevTeardown may earn a commission if you buy through this link.',
 'ko': '제휴 광고: 이 링크를 통해 구매하면 DevTeardown이 수수료를 받을 수 있습니다.',
 'zh': '推广链接：通过此链接购买，DevTeardown 可能获得佣金。',
 'ja': '広告リンク：このリンク経由で購入すると、DevTeardown が紹介料を受け取る場合があります。',
 'es': 'Enlace de afiliado: DevTeardown puede recibir una comisión si compras a través de este enlace.',
 'fr': 'Lien affilié : DevTeardown peut recevoir une commission si vous achetez via ce lien.',
}
LANGUAGE_LABEL={'en':'Language','ko':'언어 선택','zh':'选择语言','ja':'言語を選択','es':'Elegir idioma','fr':'Choisir la langue'}
PATHS={k:('/deals/' if k=='en' else f'/{k}/') for k in LANGS}
# Labels intentionally translate the interface, not the underlying evidence.
LABELS={
'en':['Deals','Tool comparisons','All deals, one place','Filter by market and category. Language does not determine shipping eligibility.','Market','Category','All','Korea','China storefront','Australia','Eligibility unverified','View product','Purchase conditions','Listed price; verify at checkout. Prices and stock can change.','Affiliate links may earn a commission. Korean offers are retained listings, not newly verified prices.','No matching offers.','offers','Source record (original language)','Comparison articles are available in English.','Software','SaaS & cloud','Gaming','Hardware','Keyboards & mice','Laptops','Monitors & desks','After work','Food & snacks','Vouchers','Technology','Source'],
'ko':['딜','도구 비교','핫딜','국가와 카테고리로 골라보세요. 표시 언어와 배송 가능 국가는 별개입니다.','국가·판매 지역','카테고리','전체','한국','중국 판매처','호주','구매 가능 국가 미확인','상품 보기','구매 조건','기록된 표시가입니다. 결제 전 가격과 재고를 확인하세요.','제휴 링크로 수수료를 받을 수 있습니다. 한국 상품은 기존 기록이며 가격을 새로 검증한 것은 아닙니다.','조건에 맞는 상품이 없습니다.','개 상품','출처 기록 (원문)','비교글 본문은 영어로 제공됩니다.','소프트웨어','SaaS · 클라우드','게임','하드웨어','키보드 · 마우스','노트북','모니터 · 책상','퇴근 후','먹거리','상품권','테크','출처'],
'zh':['优惠','工具比较','所有优惠，一处浏览','按市场和类别筛选。显示语言不代表可配送地区。','市场','类别','全部','韩国','中国商店','澳大利亚','购买地区未确认','查看商品','购买条件','记录价格；结账时请确认价格及库存。','推广链接可能产生佣金。韩国商品为保留记录，价格未经重新核实。','没有符合条件的商品。','项商品','来源记录（原文）','比较文章正文仅提供英文。','软件','SaaS 与云服务','游戏','硬件','键盘与鼠标','笔记本电脑','显示器与桌面','休闲','食品与零食','礼品券','科技','来源'],
'ja':['セール','ツール比較','すべてのセールを一か所で','販売地域とカテゴリで絞り込み。表示言語と配送可能地域は別です。','販売地域','カテゴリ','すべて','韓国','中国の販売店','オーストラリア','購入可能地域未確認','商品を見る','購入条件','記録された価格です。決済前に価格と在庫をご確認ください。','アフィリエイト収益を得る場合があります。韓国商品は既存の記録であり、価格の再確認はしていません。','該当する商品がありません。','件','出典の記録（原文）','比較記事の本文は英語です。','ソフトウェア','SaaS・クラウド','ゲーム','ハードウェア','キーボード・マウス','ノートパソコン','モニター・デスク','余暇','食品・お菓子','商品券','テクノロジー','出典'],
'es':['Ofertas','Comparativas','Todas las ofertas en un lugar','Filtra por mercado y categoría. El idioma no determina la disponibilidad del envío.','Mercado','Categoría','Todas','Corea','Tienda de China','Australia','Disponibilidad no verificada','Ver producto','Condiciones de compra','Precio registrado; confirma el precio y las existencias al pagar.','Podemos recibir comisiones por enlaces afiliados. Las ofertas coreanas son registros anteriores, sin nueva verificación de precios.','No hay ofertas con estos filtros.','ofertas','Registro de la fuente (idioma original)','Los artículos comparativos están disponibles en inglés.','Software','SaaS y nube','Videojuegos','Hardware','Teclados y ratones','Portátiles','Monitores y escritorios','Ocio','Comida y aperitivos','Vales','Tecnología','Fuente'],
'fr':['Offres','Comparatifs','Toutes les offres au même endroit','Filtrez par marché et catégorie. La langue ne détermine pas les zones de livraison.','Marché','Catégorie','Tout','Corée','Boutique chinoise','Australie','Disponibilité non vérifiée','Voir le produit','Conditions d’achat','Prix relevé ; vérifiez le prix et le stock au paiement.','Les liens affiliés peuvent générer une commission. Les offres coréennes sont des données conservées, sans nouvelle vérification des prix.','Aucune offre ne correspond.','offres','Relevé de la source (langue originale)','Les articles comparatifs sont disponibles en anglais.','Logiciels','SaaS et cloud','Jeux vidéo','Matériel','Claviers et souris','Ordinateurs portables','Écrans et bureaux','Loisirs','Alimentation','Bons cadeaux','Technologie','Source']}
# Storefront country is an editorial browsing facet. Destination eligibility is evidence-only.
FILTER_TEXT = {
 'en': ['Storefront country', 'Confirmed delivery / activation country', 'Storefront unclassified', 'Destination unverified', 'Delivery / activation evidence', 'Seller destination evidence only; stock, postcode, billing, payment and final checkout remain unverified. Unknown means not checked, not unavailable.', 'Reset filters', 'products with verified links', 'No linked products match. Try clearing filters; retained records are listed separately below.', 'Select storefront, destination and category independently. Seller location and page language do not prove purchase eligibility.', 'Korea', 'China', 'Australia', 'United States', 'Japan', 'Spain', 'France', 'All categories', 'All storefronts', 'All destinations'],
 'ko': ['판매처 국가', '배송·사용 가능 국가 (근거 확인)', '판매처 국가 미분류', '배송·사용 가능 국가 미확인', '배송·사용 가능 근거', '판매처의 배송·사용 조건을 확인한 국가입니다. 재고·우편번호·청구지·결제 수단·최종 주문은 별도 확인이 필요합니다. 미확인은 구매 불가라는 뜻이 아닙니다.', '필터 초기화', '개 상품 · 링크 확인', '조건에 맞는 링크 확인 상품이 없습니다. 필터를 초기화해 보세요. 보류된 이전 기록은 아래에 별도로 표시합니다.', '판매처 국가, 배송·사용 가능 국가, 카테고리를 각각 선택하세요. 판매처 위치나 표시 언어로 구매 가능 국가를 추정하지 않습니다.', '한국', '중국', '호주', '미국', '일본', '스페인', '프랑스', '전체 카테고리', '전체 판매처', '전체 국가'],
 'zh': ['商店所在国家', '已确认配送／激活国家', '商店国家未分类', '配送／激活国家未确认', '配送／激活依据', '仅依据卖家的配送／激活说明；库存、邮编、账单地址、付款及最终结账仍待确认。未确认不代表无法购买。', '重置筛选', '件商品（链接已核实）', '没有符合条件且链接已核实的商品。请尝试重置筛选；历史记录在下方单独列出。', '分别选择商店国家、配送／激活国家和类别。商店所在地和页面语言不能证明购买资格。', '韩国', '中国', '澳大利亚', '美国', '日本', '西班牙', '法国', '全部类别', '全部商店', '全部国家'],
 'ja': ['販売店の国', '配送・利用先の国（根拠確認済み）', '販売店の国は未分類', '配送・利用先の国は未確認', '配送・利用先の根拠', '販売店の配送・利用条件に基づきます。在庫・郵便番号・請求先・支払い・最終注文は別途確認が必要です。未確認は購入不可を意味しません。', '絞り込みを解除', '件の商品（リンク確認済み）', '条件に合うリンク確認済みの商品はありません。絞り込みを解除してください。過去の記録は下に別途表示します。', '販売店の国、配送・利用先の国、カテゴリを個別に選択。販売店の所在地や表示言語は購入資格の根拠になりません。', '韓国', '中国', 'オーストラリア', '米国', '日本', 'スペイン', 'フランス', 'すべてのカテゴリ', 'すべての販売店', 'すべての国'],
 'es': ['País de la tienda', 'País de entrega / activación confirmada', 'País de la tienda sin clasificar', 'Destino sin verificar', 'Evidencia de entrega / activación', 'Solo evidencia del vendedor sobre el destino; stock, código postal, facturación, pago y compra final sin verificar. Sin verificar no significa no disponible.', 'Restablecer filtros', 'productos con enlaces verificados', 'No hay productos con enlaces verificados que coincidan. Prueba a restablecer los filtros; los registros anteriores aparecen aparte.', 'Elige tienda, destino y categoría por separado. El país de la tienda y el idioma no prueban que puedas comprar.', 'Corea del Sur', 'China', 'Australia', 'Estados Unidos', 'Japón', 'España', 'Francia', 'Todas las categorías', 'Todas las tiendas', 'Todos los destinos'],
 'fr': ['Pays de la boutique', 'Pays de livraison / activation confirmé', 'Pays de la boutique non classé', 'Destination non vérifiée', 'Justificatif de livraison / activation', 'Selon les indications du vendeur ; stock, code postal, facturation, paiement et commande finale restent à vérifier. Non vérifié ne signifie pas indisponible.', 'Réinitialiser les filtres', 'produits avec liens vérifiés', 'Aucun produit avec lien vérifié ne correspond. Essayez de réinitialiser les filtres ; les anciennes fiches sont présentées séparément.', 'Choisissez séparément boutique, destination et catégorie. Le pays du vendeur et la langue ne prouvent pas l’éligibilité à l’achat.', 'Corée du Sud', 'Chine', 'Australie', 'États-Unis', 'Japon', 'Espagne', 'France', 'Toutes les catégories', 'Toutes les boutiques', 'Toutes les destinations'],
}
COUNTRY_ORDER = ('KR', 'CN', 'AU', 'US', 'JP', 'ES', 'FR')
def country_name(code, lang):
 return FILTER_TEXT[lang][10 + COUNTRY_ORDER.index(code)] if code in COUNTRY_ORDER else code
PRICE_CURRENT={'en':'Recorded seller price; not a live quote or verified checkout','ko':'판매페이지 가격 확인 기록 · 실시간 가격·최종 결제 미검증','zh':'卖家标价记录；非实时报价，结算价未验证','ja':'販売価格の確認記録・リアルタイム価格と決済は未確認','es':'Precio del vendedor registrado; no es una cotización en tiempo real ni un pago verificado','fr':'Prix vendeur relevé ; ni prix en temps réel ni paiement vérifié'}
DISCOUNT_UNKNOWN={'en':'Discount / historical low not established','ko':'할인·역대 최저가 근거 미확인','zh':'折扣及历史低价未证实','ja':'割引・過去最安値の根拠は未確認','es':'Descuento y mínimo histórico sin acreditar','fr':'Réduction et minimum historique non établis'}
SRP={
'en':'Recorded price is {percent}% below official {currency} {price} RRP; not a proven historical low',
'ko':'기록된 가격은 공식 권장가 {currency} {price} 대비 {percent}% 낮음 · 역대 최저 여부 미확인',
'zh':'记录价格比官方建议价 {currency} {price} 低{percent}%；非已证实历史低价',
'ja':'記録価格は公式希望価格 {currency} {price} より{percent}%安い・過去最安の証明なし',
'es':'Precio registrado un {percent}% inferior al PVP oficial de {currency} {price}; no mínimo histórico probado',
'fr':'Prix relevé inférieur de {percent} % au prix conseillé officiel de {currency} {price} ; minimum historique non prouvé'}
REVIEW_DATE={'en':'Review recorded','ko':'검토 기록일','zh':'审核记录时间','ja':'確認記録日時','es':'Revisión registrada','fr':'Relevé de vérification'}
NOT_DISCOUNT={'en':'No discount: recorded sale and reference prices are equal','ko':'할인 아님 · 기록된 판매가와 비교가격이 동일','zh':'非折扣：记录售价与参考价相同','ja':'割引ではありません・記録された販売価格と比較価格が同額','es':'Sin descuento: precio registrado igual al de referencia','fr':'Pas de réduction : prix relevé identique au prix de référence'}
ARCHIVE={'en':'Unverified listings (purchase links withheld)','ko':'검증 보류 상품 기록 (구매 링크 없음)','zh':'未核实商品记录（不提供购买链接）','ja':'未確認の商品記録（購入リンクなし）','es':'Registros sin verificar (sin enlace de compra)','fr':'Fiches non vérifiées (sans lien d’achat)'}
ARCHIVE_NOTE={'en':'These older records are not active offers. Their exact product links could not be verified; no search links are substituted.','ko':'정확한 상품 링크를 확인하지 못한 이전 기록입니다. 판매 중인 상품 목록과 분리했으며 검색 링크로 대체하지 않습니다.','zh':'这些是历史记录，并非当前优惠。商品链接未能核实，不以搜索链接代替。','ja':'過去の記録であり、現在の販売リストではありません。商品リンクを確認できないため、検索リンクで代用しません。','es':'Son registros anteriores, no ofertas activas. No se sustituyen enlaces de producto sin verificar por búsquedas.','fr':'Ces anciennes fiches ne sont pas des offres actives. Aucun lien de recherche ne remplace un lien produit non vérifié.'}
HELD_SUMMARY={'en':'Retained listing, not a confirmed current deal. Product identity and current price need verification.','ko':'보존된 이전 상품 기록입니다. 현재 핫딜이 아니며 상품 일치와 현재 가격을 확인 중입니다.','zh':'保留的历史记录，并非已确认的当前优惠。商品身份和当前价格待核实。','ja':'保存された過去の商品記録です。現在の特価ではなく、商品と現行価格は確認中です。','es':'Registro anterior, no una oferta actual confirmada. Producto y precio pendientes de verificar.','fr':'Ancienne fiche conservée, pas une offre actuelle confirmée. Produit et prix à vérifier.'}
PRICE_RECORDED={'en':'Previously recorded price; not reverified','ko':'이전 기록 가격 · 현재 가격 미검증','zh':'历史记录价格，当前价格未核实','ja':'過去の記録価格・現在価格は未確認','es':'Precio registrado anteriormente; sin reverificar','fr':'Prix précédemment relevé ; non revérifié'}
HELD={'en':'Product link awaiting verification','ko':'상품 링크 확인 중','zh':'商品链接待核实','ja':'商品リンクを確認中','es':'Enlace de producto pendiente de verificar','fr':'Lien du produit en attente de vérification'}
CATS={'software':20,'cloud':21,'gaming':22,'hardware':23,'keyboard-mouse':24,'laptops':25,'monitor-desk':26,'afterwork':27,'snacks':28,'vouchers':29,'tech':30}
CATS={key:value-1 for key,value in CATS.items()}
def e(x):return html.escape(str(x),quote=True)
def safe(x):return x if isinstance(x,str) and (x.startswith(('https://','http://')) or re.fullmatch(r'/assets/deals/[a-z0-9-]+\.png',x)) else '#'
LANGUAGE_JS='''const languageMenu=document.querySelector('.languages');document.addEventListener('click',event=>{if(!languageMenu.contains(event.target))languageMenu.open=false});document.addEventListener('keydown',event=>{if(event.key==='Escape'&&languageMenu.open){languageMenu.open=false;languageMenu.querySelector('summary').focus()}});window.addEventListener('pageshow',()=>{languageMenu.open=false});'''
def nav(lang, report=False):
 t=LABELS[lang]
 report_paths={k:('/' if k=='en' else '/reports/'+k+'/') for k in LANGS}
 targets=report_paths if report else PATHS
 switches=''.join(f'<a class="lang" href="{targets[k]}" lang="{k}" hreflang="{k}"'+(' aria-current="page"' if k==lang else '')+f'><span aria-hidden="true">{FLAGS[k]}</span> {v}</a>' for k,v in LANGS.items())
 report_path=report_paths[lang]
 return f'<header class="unified-header"><a class="brand" href="{PATHS[lang]}">DevTeardown</a><nav aria-label="Navigation"><a href="{PATHS[lang]}">{t[0]}</a><a href="{report_path}">{t[1]}</a></nav><details class="languages"><summary aria-label="{LANGUAGE_LABEL[lang]}: {LANGS[lang]}"><span aria-hidden="true">{FLAGS[lang]}</span> {LANGS[lang]} <span class="language-chevron" aria-hidden="true">⌄</span></summary><nav class="language-options" aria-label="{LANGUAGE_LABEL[lang]}">{switches}</nav></details></header><script>{LANGUAGE_JS}</script>'
CSS='''*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#172333;font:16px/1.6 system-ui,sans-serif}a{color:#164fc6}a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #e59400;outline-offset:4px}.unified-header{display:flex;flex-wrap:wrap;gap:18px;align-items:center;padding:18px max(20px,calc((100% - 1180px)/2));background:white;border-bottom:1px solid #dbe1e8}.brand{font-weight:800;color:#172333;text-decoration:none}.unified-header nav{display:flex;gap:16px;flex-wrap:wrap}.languages{position:relative;margin-left:auto;font-size:14px}.languages>summary{display:flex;align-items:center;gap:8px;list-style:none;cursor:pointer;min-height:44px;padding:8px 12px;border:1px solid #dbe1e8;border-radius:8px;background:#fff;white-space:nowrap}.languages>summary::-webkit-details-marker{display:none}.language-chevron{margin-left:6px}.languages[open] .language-chevron{transform:rotate(180deg)}.unified-header .language-options{position:absolute;right:0;top:calc(100% + 6px);z-index:20;display:grid;gap:2px;min-width:176px;max-width:calc(100vw - 40px);padding:6px;background:#fff;border:1px solid #dbe1e8;border-radius:10px;box-shadow:0 10px 28px #17233320}.language-options .lang{display:block;padding:10px 12px;min-height:44px;border-radius:6px;color:#172333;text-decoration:none}.language-options .lang:hover,.language-options .lang:focus-visible{background:#edf3ff}.lang[aria-current]{font-weight:700;background:#edf3ff}main{max-width:1180px;margin:auto;padding:32px 20px}h1{font-size:clamp(28px,4vw,42px);line-height:1.2;margin:8px 0 16px}.intro{max-width:760px;color:#526071}.filters{display:flex;gap:20px;flex-wrap:wrap;margin:28px 0 12px}.filters label{display:grid;gap:5px;font-weight:600}#reset-filters{font:inherit;padding:8px 12px;border:1px solid #aab6c5;border-radius:8px;background:white;cursor:pointer}button:focus-visible{outline:3px solid #e59400;outline-offset:4px}input[type=search]{font:inherit;padding:10px 12px;border:1px solid #aab6c5;border-radius:8px;background:white;min-width:0;max-width:100%;width:100%}select{font:inherit;padding:10px 38px 10px 12px;border:1px solid #aab6c5;border-radius:8px;background:white;max-width:100%}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.card{background:white;border:1px solid #dbe1e8;border-radius:14px;padding:24px;display:flex;flex-direction:column;gap:12px;min-width:0}.card[hidden],.held-archive[hidden]{display:none}.held-archive{margin-top:32px;border-top:1px solid #dbe1e8;padding-top:20px}.held-archive>summary{cursor:pointer;font-weight:650}.held-archive>.grid{margin-top:20px}.product-title{color:inherit;text-decoration:underline;text-underline-offset:4px}.card h2{overflow-wrap:anywhere;font-size:20px;line-height:1.35;margin:0}.card p{margin:0}.meta,.notice,.caption{overflow-wrap:anywhere;font-size:13px;color:#526071}.price{font-size:26px;font-weight:750;font-variant-numeric:tabular-nums}.cta{background:#164fc6;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;text-align:center;margin-top:auto}.card details{border-top:1px solid #e2e7ed;padding-top:10px;font-size:14px}.card summary{cursor:pointer;font-weight:650}.card details p{margin-top:10px}.original{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.5 system-ui}.card img{height:110px;max-width:100%;object-fit:contain}.card figure{margin:0}footer{margin-top:32px;border-top:1px solid #dbe1e8;padding-top:20px}.count{margin:15px 0}.original-notice{padding:12px 20px;background:#fff3d5} @media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.languages{margin-left:auto}}@media(max-width:560px){.grid{grid-template-columns:1fr}.card{padding:20px}.filters{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}select{font-size:14px;width:100%}.unified-header{gap:12px}}'''
SEARCH_LABEL = {'en':'Search products or stores','ko':'상품명·판매처 검색','zh':'搜索商品或商店','ja':'商品名・ストアを検索','es':'Buscar productos o tiendas','fr':'Rechercher un produit ou une boutique'}
JS = """
const market = document.querySelector('#market');
const search = document.querySelector('#product-search');
const normalizeSearch = value => value.normalize('NFKC').toLowerCase().trim();
const country = document.querySelector('#country');
const cat = document.querySelector('#category');
const controls = [[market, 'market'], [country, 'country'], [cat, 'category']];
const cards = [...document.querySelectorAll('#active-products .card')];
const archived = [...document.querySelectorAll('#held-products .card')];
function restore() {
  const q = new URLSearchParams(location.search);
  search.value = q.get('q') || '';
  for (const [el, key] of controls) {
    const value = q.get(key);
    el.value = [...el.options].some(o => o.value === value) ? value : 'all';
  }
}
function matches(card) {
  const terms = normalizeSearch(search.value).split(/\\s+/).filter(Boolean);
  const searchMatch = terms.every(term => normalizeSearch(card.dataset.search || '').includes(term));
  const destinations = (card.dataset.countries || '').split(' ').filter(Boolean);
  const destinationMatch = country.value === 'all' || (country.value === 'unknown'
    ? destinations.length === 0 : destinations.includes(country.value));
  return searchMatch && (market.value === 'all' || card.dataset.market === market.value) && destinationMatch &&
    (cat.value === 'all' || card.dataset.category === cat.value);
}
function filter(historyMode = 'replace') {
  let n = 0, hn = 0;
  for (const card of cards) { card.hidden = !matches(card); if (!card.hidden) n++; }
  for (const card of archived) { card.hidden = !matches(card); if (!card.hidden) hn++; }
  document.querySelector('#archive-count').textContent=hn;
  document.querySelector('.held-archive').hidden = hn === 0;
  document.querySelector('#count').textContent = n + ' ' + document.querySelector('#count').dataset.label;
  document.querySelector('#empty').hidden = n > 0;
  document.querySelector('#reset-filters').hidden = controls.every(([el]) => el.value === 'all') && !search.value.trim();
  const params = new URLSearchParams(location.search);
  for (const [el, key] of controls) {
    if (el.value === 'all') params.delete(key); else params.set(key, el.value);
  }
  if (search.value.trim()) params.set('q', search.value.trim()); else params.delete('q');
  const nextURL = location.pathname + (params.size ? '?' + params : '') + location.hash;
  if (nextURL !== location.pathname + location.search + location.hash) {
    history[historyMode === 'push' ? 'pushState' : 'replaceState'](null, '', nextURL);
  }
  const filters = new URLSearchParams();
  if (search.value.trim()) filters.set('q', search.value.trim());
  for (const [el, key] of controls) if (el.value !== 'all') filters.set(key, el.value);
  for (const a of document.querySelectorAll('.lang')) {
    const url = new URL(a.href); url.search = filters.toString(); a.href = url.pathname + url.search;
  }
}
search.addEventListener('input', () => filter());
for (const [el] of controls) el.addEventListener('change', () => filter('push'));
document.querySelector('#reset-filters').addEventListener('click', () => {
  search.value = ''; for (const [el] of controls) el.value = 'all'; filter('push'); market.focus();
});
window.addEventListener('popstate', () => { restore(); filter(); });
window.addEventListener('pageshow', () => { restore(); filter(); });
restore(); filter();
"""
def catalogue(lang,feeds,translations,discoveries=False):
 t=LABELS[lang]; f=FILTER_TEXT[lang]; cards=candidate_cards(lang) if discoveries else []; held_cards=[]
 for d in feeds:
  loc=translations.get(d['id'],{}).get(lang,{})
  title=loc.get('product',d.get('product','')); summary=loc.get('summary',''); conditions=loc.get('conditions',t[10]); conditions=' '.join(conditions) if isinstance(conditions,list) else conditions
  search_text=' '.join([d.get('product',''), d.get('store',''), *[entry.get('product','') for entry in translations.get(d['id'],{}).values()]])
  market=storefront_country(d); countries=confirmed_countries(d)
  cat=d.get('category','tech'); link=d.get('link',{}); currency=d.get('currency','KRW');price=d.get('price');price=f'{currency} {price:,.2f}'.rstrip('0').rstrip('.') if isinstance(price,(int,float)) else '—'
  record={k:d[k] for k in ('storefront_country','shipping','briefing','purchase_eligibility','source','checked_date','published_at','price_source','disclosure','price_review') if k in d}
  media=d.get('image') or {};image=''
  if media.get('path'):
   image=f'<figure><img src="{e(safe(media["path"]))}" alt="{e(title)}" loading="lazy"><figcaption class="caption">{e(media.get("caption",""))} <a href="{e(safe(media.get("credit_url","")))}">{e(media.get("credit",""))}</a></figcaption></figure>'
  source=d.get('source') or {};src=f'<a href="{e(safe(source.get("url","")))}" rel="noopener nofollow">{t[30]}</a>' if source.get('url') else ''
  linked=publishable_link(d)
  promotion=verified_aliexpress_url(d) if linked else None
  destination=promotion or link.get('url','')
  tracked=bool(promotion or link.get('tracked'))
  link_rel='noopener nofollow' + (' sponsored' if tracked else '')
  disclosure=f'<p class="notice affiliate-disclosure">{e(AFFILIATE_DISCLOSURE[lang])}</p>' if linked and tracked else ''
  cta=(f'{disclosure}<a class="cta" href="{e(destination)}" rel="{link_rel}">{t[11]}</a>' if linked else f'<p class="notice link-held" role="status">{HELD[lang]}</p>')
  review=d.get('price_review') or {}; current=checked_price(d)
  if not publishable_link(d): summary=HELD_SUMMARY[lang]
  price_note=f'<p class="notice">{PRICE_CURRENT[lang] if current else PRICE_RECORDED[lang]}</p>'
  srp=official_srp_comparison(d)
  savings=SRP[lang].format(percent=srp['percent'],currency=srp['currency'],price=f"{srp['price']:,.2f}") if srp else (NOT_DISCOUNT[lang] if review.get('deal_status')=='not_a_discount' else DISCOUNT_UNKNOWN[lang])
  price_note+=f'<p class="notice">{e(savings)}</p>'
  comparison=(review.get('comparison') or {}).get('url')
  if comparison: price_note+=f'<a class="meta" href="{e(safe(comparison))}" rel="noopener nofollow">{t[30]}</a>'
  reviewed=observed_timestamp(review.get('review_completed_at'))
  if reviewed: price_note+=f'<p class="meta">{e(REVIEW_DATE[lang])}: <time datetime="{e(review["review_completed_at"])}">{reviewed.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</time></p>'
  eligibility=f'<p class="meta">{e(f[0])}: {e(country_name(market,lang) if market!="unknown" else f[2])}</p><p class="meta eligibility">{e(f[1])}: {e(", ".join(country_name(c,lang) for c in countries) if countries else f[3])}</p>'
  info=d.get('purchase_eligibility') or {}
  evidence=f'<p><a href="{e(safe(info.get("evidence_url")))}" rel="noopener nofollow">{e(f[4])}</a> · <time datetime="{e(info.get("checked_at"))}">{e(info.get("checked_at"))}</time></p>' if countries else ''
  linked_title=f'<a class="product-title" href="{e(destination)}" rel="{link_rel}">{e(title)}</a>' if linked else e(title)
  (cards if publishable_link(d) else held_cards).append(f'''<article class="card" data-id="{e(d['id'])}" data-search="{e(search_text)}" data-market="{market}" data-countries="{e(' '.join(countries))}" data-category="{e(cat)}">{image}<div class="meta">{e(t[CATS.get(cat,29)])} · {e(d.get('store',''))}</div><h2>{linked_title}</h2><p>{e(summary)}</p><div class="price">{e(price)}</div>{price_note}{eligibility}<details><summary>{t[12]}</summary><p>{e(conditions)}</p>{evidence}<p class="notice">{t[13]}</p></details><details><summary>{t[17]}</summary><pre class="original" lang="{'ko' if d.get('region')=='kr' else 'en'}">{e(json.dumps(record,ensure_ascii=False,indent=2))}</pre>{src}</details>{cta}</article>''')
 options=lambda values:''.join(f'<option value="{key}">{e(label)}</option>' for key,label in values)
 storefronts=sorted({storefront_country(d) for d in feeds}-{"unknown"})
 destinations=list(COUNTRY_ORDER)+sorted({c for d in feeds for c in confirmed_countries(d)}-set(COUNTRY_ORDER))
 schema=json.dumps({'@context':'https://schema.org','@type':'CollectionPage','name':t[2],'url':'https://devteardown.com'+PATHS[lang],'inLanguage':lang,'description':f[9]},ensure_ascii=False).replace('<','\\u003c')
 alternatives=''.join(f'<link rel="alternate" hreflang="{k}" href="https://devteardown.com{p}">' for k,p in PATHS.items())
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t[2]} | DevTeardown</title><meta name="description" content="{e(f[9])}"><meta property="og:type" content="website"><meta property="og:title" content="{e(t[2])} | DevTeardown"><meta property="og:description" content="{e(f[9])}"><meta property="og:url" content="https://devteardown.com{PATHS[lang]}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{schema}</script><link rel="canonical" href="https://devteardown.com{PATHS[lang]}">{alternatives}<link rel="alternate" hreflang="x-default" href="https://devteardown.com/deals/"><style>{CSS}</style></head><body>{nav(lang)}<main><h1>{t[2]}</h1><p class="intro">{e(f[9])}</p><div class="filters"><label for="product-search">{e(SEARCH_LABEL[lang])}<input id="product-search" type="search" autocomplete="off" spellcheck="false"></label><label for="market">{e(f[0])}<select id="market">{options([('all',f[18])]+[(code,country_name(code,lang)) for code in storefronts]+[('unknown',f[2])])}</select></label><label for="country">{e(f[1])}<select id="country" aria-describedby="country-help">{options([('all',f[19])]+[(code,country_name(code,lang)) for code in destinations]+[('unknown',f[3])])}</select></label><label for="category">{t[5]}<select id="category">{options([('all',f[17])]+[(key,t[idx]) for key,idx in CATS.items()])}</select></label></div><p id="country-help" class="notice">{e(f[5])}</p><button type="button" id="reset-filters" hidden>{e(f[6])}</button><p id="count" class="count" role="status" aria-live="polite" data-label="{e(f[7])}">{len(cards)} {e(f[7])}</p><p id="empty" hidden>{e(f[8])}</p><div class="grid" id="active-products">{''.join(cards)}</div><details class="held-archive"><summary>{ARCHIVE[lang]} · <span id="archive-count">{len(held_cards)}</span></summary><p class="notice">{ARCHIVE_NOTE[lang]}</p><div class="grid" id="held-products">{''.join(held_cards)}</div></details><footer><p class="notice">{t[14]}</p></footer></main><script>{JS}</script></body></html>'''
def write_unified(output,items,deals,en_deals):
 output=Path(output);trans=json.loads((Path(__file__).parent/'data/deal_localizations.json').read_text())
 feeds=list(deals.get('feed',[]))+list(en_deals.get('feed',[]))
 for lang,path in PATHS.items():
  dest=output/path.strip('/');dest.mkdir(exist_ok=True,parents=True);(dest/'index.html').write_text(catalogue(lang,feeds,trans,discoveries=True),encoding='utf-8')
 # Comparison content stays English; do not claim unrelated deal pages are translations.
 for page in [output/'index.html',*output.glob('compare/*/index.html')]:
  text=page.read_text();text=re.sub(r'<header>.*?</header>',nav('en',True),text,flags=re.S)
  text=re.sub(r'<link[^>]+hreflang="ko"[^>]*>','',text)
  text=text.replace('</head>',f'<style>{CSS.split("main{")[0]}</style></head>')
  text=text.replace('<main ', '<p class="original-notice">English comparison articles · 비교글 영어 원문 · 比较文章为英文 · 比較記事は英語 · Artículos en inglés · Articles en anglais</p><main ',1)
  page.write_text(text,encoding='utf-8')
 # Localized report navigation; article content remains explicitly marked English.
 report_text=(output/'index.html').read_text()
 headings={
 'ko':['소프트웨어 선택 가이드','다음 도구를 고르기 전에.','가격과 활용 범위, 장단점을 비교합니다. 비교글 본문은 영어 원문입니다.','도구 비교'],
 'zh':['软件选择指南','选择下一个工具之前。','比较价格、用途和取舍。比较文章正文为英文。','工具比较'],
 'ja':['ソフトウェア選びのガイド','次のツールを選ぶ前に。','価格、用途、トレードオフを比較。記事本文は英語です。','ツール比較'],
 'es':['Guía para elegir software','Antes de elegir tu próxima herramienta.','Compara precios, usos y limitaciones. Los artículos están en inglés.','Comparativas'],
 'fr':['Bien choisir ses logiciels','Avant de choisir votre prochain outil.','Comparez les prix, les usages et les compromis. Les articles sont en anglais.','Comparatifs']}
 for lang,h in headings.items():
  page=report_text.replace('href="./','href="/').replace('<html lang="en">',f'<html lang="{lang}">')
  page=re.sub(r'<header.*?</header><script>.*?</script>',lambda _:nav(lang,True),page,count=1,flags=re.S)
  catalog_cta={'ko':'상품 목록 보기','zh':'浏览商品目录','ja':'商品一覧を見る','es':'Ver el catálogo de productos','fr':'Voir le catalogue de produits'}
  page=page.replace('href="/deals/">Browse the product catalog',f'href="{PATHS[lang]}">{catalog_cta[lang]}')
  page=page.replace('Notes on choosing software',h[0]).replace('Before you pick<br>the next tool.',h[1]).replace('What it costs, where it fits, and what you give up. Comparisons of developer tools, with pricing examples you can check against your own workload.',h[2]).replace('The comparisons',h[3])
  page=re.sub(r'<link[^>]+rel="alternate"[^>]*>','',page)
  page=re.sub(r'<link rel="canonical"[^>]*>',f'<link rel="canonical" href="https://devteardown.com/reports/{lang}/">',page)
  dest=output/'reports'/lang;dest.mkdir(parents=True,exist_ok=True);(dest/'index.html').write_text(page,encoding='utf-8')
 urls=['/']+['/reports/'+k+'/' for k in LANGS if k!='en']+list(PATHS.values())+[f'/compare/{x["slug"]}/' for x in items]
 records=[]
 modified=datetime.date.today().isoformat()
 for path in urls:
  alternates=''.join(f'<xhtml:link rel="alternate" hreflang="{k}" href="https://devteardown.com{v}"/>' for k,v in PATHS.items()) if path in PATHS.values() else ''
  records.append(f'<url><loc>https://devteardown.com{escape(path)}</loc><lastmod>{modified}</lastmod>{alternates}</url>')
 (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join(records)+'</urlset>',encoding='utf-8')
