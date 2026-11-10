"""Shared six-language navigation and one market-aware deal catalogue."""
import html, json, re, datetime
from pathlib import Path
from xml.sax.saxutils import escape
LANGS={'en':'English','ko':'한국어','zh':'中文','ja':'日本語','es':'Español','fr':'Français'}
PATHS={k:('/deals/' if k=='en' else f'/{k}/') for k in LANGS}
# Labels intentionally translate the interface, not the underlying evidence.
LABELS={
'en':['Deals','Tool comparisons','All deals, one place','Filter by market and category. Language does not determine shipping eligibility.','Market','Category','All','Korea','China storefront','Australia','Eligibility unverified','View product','Purchase conditions','Listed price; verify at checkout. Prices and stock can change.','Affiliate links may earn a commission. Korean offers are retained listings, not newly verified prices.','No matching offers.','offers','Source record (original language)','Comparison articles are available in English.','Software','SaaS & cloud','Gaming','Hardware','Keyboards & mice','Laptops','Monitors & desks','After work','Food & snacks','Vouchers','Technology','Source'],
'ko':['딜','도구 비교','모든 딜을 한곳에서','국가와 카테고리로 골라보세요. 표시 언어와 배송 가능 국가는 별개입니다.','국가·판매 지역','카테고리','전체','한국','중국 판매처','호주','구매 가능 국가 미확인','상품 보기','구매 조건','기록된 표시가입니다. 결제 전 가격과 재고를 확인하세요.','제휴 링크로 수수료를 받을 수 있습니다. 한국 상품은 기존 기록이며 가격을 새로 검증한 것은 아닙니다.','조건에 맞는 상품이 없습니다.','개 상품','출처 기록 (원문)','비교글 본문은 영어로 제공됩니다.','소프트웨어','SaaS · 클라우드','게임','하드웨어','키보드 · 마우스','노트북','모니터 · 책상','퇴근 후','먹거리','상품권','테크','출처'],
'zh':['优惠','工具比较','所有优惠，一处浏览','按市场和类别筛选。显示语言不代表可配送地区。','市场','类别','全部','韩国','中国商店','澳大利亚','购买地区未确认','查看商品','购买条件','记录价格；结账时请确认价格及库存。','推广链接可能产生佣金。韩国商品为保留记录，价格未经重新核实。','没有符合条件的商品。','项商品','来源记录（原文）','比较文章正文仅提供英文。','软件','SaaS 与云服务','游戏','硬件','键盘与鼠标','笔记本电脑','显示器与桌面','休闲','食品与零食','礼品券','科技','来源'],
'ja':['セール','ツール比較','すべてのセールを一か所で','販売地域とカテゴリで絞り込み。表示言語と配送可能地域は別です。','販売地域','カテゴリ','すべて','韓国','中国の販売店','オーストラリア','購入可能地域未確認','商品を見る','購入条件','記録された価格です。決済前に価格と在庫をご確認ください。','アフィリエイト収益を得る場合があります。韓国商品は既存の記録であり、価格の再確認はしていません。','該当する商品がありません。','件','出典の記録（原文）','比較記事の本文は英語です。','ソフトウェア','SaaS・クラウド','ゲーム','ハードウェア','キーボード・マウス','ノートパソコン','モニター・デスク','余暇','食品・お菓子','商品券','テクノロジー','出典'],
'es':['Ofertas','Comparativas','Todas las ofertas en un lugar','Filtra por mercado y categoría. El idioma no determina la disponibilidad del envío.','Mercado','Categoría','Todas','Corea','Tienda de China','Australia','Disponibilidad no verificada','Ver producto','Condiciones de compra','Precio registrado; confirma el precio y las existencias al pagar.','Podemos recibir comisiones por enlaces afiliados. Las ofertas coreanas son registros anteriores, sin nueva verificación de precios.','No hay ofertas con estos filtros.','ofertas','Registro de la fuente (idioma original)','Los artículos comparativos están disponibles en inglés.','Software','SaaS y nube','Videojuegos','Hardware','Teclados y ratones','Portátiles','Monitores y escritorios','Ocio','Comida y aperitivos','Vales','Tecnología','Fuente'],
'fr':['Offres','Comparatifs','Toutes les offres au même endroit','Filtrez par marché et catégorie. La langue ne détermine pas les zones de livraison.','Marché','Catégorie','Tout','Corée','Boutique chinoise','Australie','Disponibilité non vérifiée','Voir le produit','Conditions d’achat','Prix relevé ; vérifiez le prix et le stock au paiement.','Les liens affiliés peuvent générer une commission. Les offres coréennes sont des données conservées, sans nouvelle vérification des prix.','Aucune offre ne correspond.','offres','Relevé de la source (langue originale)','Les articles comparatifs sont disponibles en anglais.','Logiciels','SaaS et cloud','Jeux vidéo','Matériel','Claviers et souris','Ordinateurs portables','Écrans et bureaux','Loisirs','Alimentation','Bons cadeaux','Technologie','Source']}
CATS={'software':20,'cloud':21,'gaming':22,'hardware':23,'keyboard-mouse':24,'laptops':25,'monitor-desk':26,'afterwork':27,'snacks':28,'vouchers':29,'tech':30}
CATS={key:value-1 for key,value in CATS.items()}
def e(x):return html.escape(str(x),quote=True)
def safe(x):return x if isinstance(x,str) and (x.startswith(('https://','http://')) or re.fullmatch(r'/assets/deals/[a-z0-9-]+\.png',x)) else '#'
def nav(lang, report=False):
 t=LABELS[lang]
 report_paths={k:('/' if k=='en' else '/reports/'+k+'/') for k in LANGS}
 targets=report_paths if report else PATHS
 switches=''.join(f'<a class="lang" href="{targets[k]}" lang="{k}" hreflang="{k}"'+(' aria-current="page"' if k==lang else '')+f'>{v}</a>' for k,v in LANGS.items())
 report_path=report_paths[lang]
 return f'<header class="unified-header"><a class="brand" href="{PATHS[lang]}">DevTeardown</a><nav aria-label="Navigation"><a href="{PATHS[lang]}">{t[0]}</a><a href="{report_path}">{t[1]}</a></nav><nav class="languages" aria-label="Language">{switches}</nav></header>'
CSS='''*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#172333;font:16px/1.6 system-ui,sans-serif}a{color:#164fc6}a:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #e59400;outline-offset:4px}.unified-header{display:flex;flex-wrap:wrap;gap:18px;align-items:center;padding:18px max(20px,calc((100% - 1180px)/2));background:white;border-bottom:1px solid #dbe1e8}.brand{font-weight:800;color:#172333;text-decoration:none}.unified-header nav{display:flex;gap:16px;flex-wrap:wrap}.languages{margin-left:auto;font-size:14px}.lang[aria-current]{font-weight:bold;text-decoration-thickness:3px}main{max-width:1180px;margin:auto;padding:32px 20px}h1{font-size:clamp(28px,4vw,42px);line-height:1.2;margin:8px 0 16px}.intro{max-width:760px;color:#526071}.filters{display:flex;gap:20px;flex-wrap:wrap;margin:28px 0 12px}.filters label{display:grid;gap:5px;font-weight:600}select{font:inherit;padding:10px 38px 10px 12px;border:1px solid #aab6c5;border-radius:8px;background:white;max-width:100%}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.card{background:white;border:1px solid #dbe1e8;border-radius:14px;padding:24px;display:flex;flex-direction:column;gap:12px;min-width:0}.card[hidden]{display:none}.card h2{font-size:20px;line-height:1.35;margin:0}.card p{margin:0}.meta,.notice,.caption{font-size:13px;color:#526071}.price{font-size:26px;font-weight:750;font-variant-numeric:tabular-nums}.cta{background:#164fc6;color:white;padding:10px 14px;border-radius:8px;text-decoration:none;text-align:center;margin-top:auto}.card details{border-top:1px solid #e2e7ed;padding-top:10px;font-size:14px}.card summary{cursor:pointer;font-weight:650}.card details p{margin-top:10px}.original{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.5 system-ui}.card img{height:110px;max-width:100%;object-fit:contain}.card figure{margin:0}footer{margin-top:32px;border-top:1px solid #dbe1e8;padding-top:20px}.count{margin:15px 0}.original-notice{padding:12px 20px;background:#fff3d5} @media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.languages{margin-left:0;width:100%}}@media(max-width:560px){.grid{grid-template-columns:1fr}.card{padding:20px}.filters{display:grid;grid-template-columns:1fr 1fr;gap:10px}select{font-size:14px;width:100%}.unified-header{gap:12px}}'''
JS='''const market=document.querySelector('#market'),cat=document.querySelector('#category');const cards=[...document.querySelectorAll('.card')];const q=new URLSearchParams(location.search);for(const [el,key] of [[market,'market'],[cat,'category']]){if([...el.options].some(o=>o.value===q.get(key)))el.value=q.get(key)}function filter(){let n=0;for(const c of cards){c.hidden=!(market.value==='all'||c.dataset.market===market.value)||!(cat.value==='all'||c.dataset.category===cat.value);if(!c.hidden)n++}document.querySelector('#count').textContent=n+' '+document.querySelector('#count').dataset.label;document.querySelector('#empty').hidden=n>0;const params=new URLSearchParams();if(market.value!=='all')params.set('market',market.value);if(cat.value!=='all')params.set('category',cat.value);history.replaceState(null,'',location.pathname+(params.size?'?'+params:''));for(const a of document.querySelectorAll('.lang')){const u=new URL(a.href);u.search=params.toString();a.href=u.pathname+u.search}}market.addEventListener('change',filter);cat.addEventListener('change',filter);filter();'''
def catalogue(lang,feeds,translations):
 t=LABELS[lang]; cards=[]
 for d in feeds:
  loc=translations.get(d['id'],{}).get(lang,{})
  title=loc.get('product',d.get('product','')); summary=loc.get('summary',''); conditions=loc.get('conditions',t[10]); conditions=' '.join(conditions) if isinstance(conditions,list) else conditions
  market='KR' if d.get('region')=='kr' else ('CN' if d.get('category')=='china' else ('AU' if 'AU' in d.get('purchase_eligibility',{}).get('countries_confirmed',[]) else 'unknown'))
  cat='hardware' if d.get('category')=='china' else d.get('category','tech'); link=d.get('link',{}); currency=d.get('currency','KRW');price=d.get('price');price=f'{currency} {price:,.2f}'.rstrip('0').rstrip('.') if isinstance(price,(int,float)) else '—'
  record={k:d[k] for k in ('shipping','briefing','purchase_eligibility','source','checked_date','published_at','price_source','disclosure') if k in d}
  media=d.get('image') or {};image=''
  if media.get('path'):
   image=f'<figure><img src="{e(safe(media["path"]))}" alt="{e(title)}" loading="lazy"><figcaption class="caption">{e(media.get("caption",""))} <a href="{e(safe(media.get("credit_url","")))}">{e(media.get("credit",""))}</a></figcaption></figure>'
  source=d.get('source') or {};src=f'<a href="{e(safe(source.get("url","")))}" rel="noopener nofollow">{t[30]}</a>' if source.get('url') else ''
  cards.append(f'''<article class="card" data-id="{e(d['id'])}" data-market="{market}" data-category="{e(cat)}">{image}<div class="meta">{e(t[CATS.get(cat,29)])} · {e(d.get('store',''))}</div><h2>{e(title)}</h2><p>{e(summary)}</p><div class="price">{e(price)}</div><p class="meta">{t[{'KR':7,'CN':8,'AU':9,'unknown':10}[market]]}</p><details><summary>{t[12]}</summary><p>{e(conditions)}</p><p class="notice">{t[13]}</p></details><details><summary>{t[17]}</summary><pre class="original" lang="{'ko' if market=='KR' else 'en'}">{e(json.dumps(record,ensure_ascii=False,indent=2))}</pre>{src}</details><a class="cta" href="{e(safe(link.get('url','')))}" rel="noopener nofollow{' sponsored' if link.get('tracked') else ''}">{t[11]}</a></article>''')
 options=lambda values:''.join(f'<option value="{key}">{e(label)}</option>' for key,label in values)
 schema=json.dumps({'@context':'https://schema.org','@type':'CollectionPage','name':t[2],'url':'https://devteardown.com'+PATHS[lang],'inLanguage':lang,'description':t[3]},ensure_ascii=False).replace('<','\\u003c')
 alternatives=''.join(f'<link rel="alternate" hreflang="{k}" href="https://devteardown.com{p}">' for k,p in PATHS.items())
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t[2]} | DevTeardown</title><meta name="description" content="{e(t[3])}"><meta property="og:type" content="website"><meta property="og:title" content="{e(t[2])} | DevTeardown"><meta property="og:description" content="{e(t[3])}"><meta property="og:url" content="https://devteardown.com{PATHS[lang]}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{schema}</script><link rel="canonical" href="https://devteardown.com{PATHS[lang]}">{alternatives}<link rel="alternate" hreflang="x-default" href="https://devteardown.com/deals/"><style>{CSS}</style></head><body>{nav(lang)}<main><h1>{t[2]}</h1><p class="intro">{t[3]}</p><div class="filters"><label for="market">{t[4]}<select id="market">{options([('all',t[6]),('KR',t[7]),('CN',t[8]),('AU',t[9]),('unknown',t[10])])}</select></label><label for="category">{t[5]}<select id="category">{options([('all',t[6])]+[(key,t[idx]) for key,idx in CATS.items()])}</select></label></div><p id="count" class="count" role="status" aria-live="polite" data-label="{t[16]}">{len(feeds)} {t[16]}</p><p id="empty" hidden>{t[15]}</p><div class="grid">{''.join(cards)}</div><footer><p class="notice">{t[14]}</p></footer></main><script>{JS}</script></body></html>'''
def write_unified(output,items,deals,en_deals):
 output=Path(output);trans=json.loads((Path(__file__).parent/'data/deal_localizations.json').read_text())
 feeds=list(deals.get('feed',[]))+list(en_deals.get('feed',[]))
 for lang,path in PATHS.items():
  dest=output/path.strip('/');dest.mkdir(exist_ok=True,parents=True);(dest/'index.html').write_text(catalogue(lang,feeds,trans),encoding='utf-8')
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
  page=re.sub(r'<header.*?</header>',nav(lang,True),page,flags=re.S)
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
