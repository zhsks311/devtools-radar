"""Public that.promo data, commercially reusable with attribution and dates.
Separate source-reported benefits, never verified prices or main deal cards.
"""
import argparse, html, json, re
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from urllib.parse import urlsplit
from tools.collect_deal_feeds import read_url, robots_allowed
URL='https://that.promo/offers.json'
def text(v): return html.escape(v if isinstance(v,str) and v.strip() else 'Not stated · 미기재')
def link(v, source=False):
    p=urlsplit(v or '')
    if p.scheme!='https' or not p.hostname or p.username or p.password or (source and p.hostname not in ('that.promo','saasoffers.tech')):
        raise ValueError('Invalid source or official link')
    return html.escape(v,quote=True)
def expired(value, now):
    """Use explicit source timestamps; date-only or timezone-less ends fail closed.

    Prose such as 'ongoing' is not an invented timestamp and remains visible.
    """
    if not isinstance(value,str): return False
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
        return datetime.fromisoformat(value).date() <= now.date()
    if re.match(r'^\d{4}-\d{2}-\d{2}T',value):
        end=datetime.fromisoformat(value.replace('Z','+00:00'))
        if end.tzinfo is None: return end.date() <= now.date()
        return end <= now
    return False
def prepare(data, now):
    if not isinstance(data.get('offers'),list) or not 1<=len(data['offers'])<=1000:raise ValueError('Invalid offer list')
    seen=set(); offers=[]
    for row in data['offers']:
        slug=row.get('slug')
        if not isinstance(slug,str) or not re.fullmatch('[a-z0-9-]+',slug):raise ValueError('Invalid slug')
        if slug in seen:continue
        seen.add(slug)
        if row.get('status') not in ('live','changed') or row.get('sponsored'):continue
        link(row.get('url'),True);link(row.get('official_url'))
        verified=row.get('last_verified')
        if verified is not None:
            dt=datetime.fromisoformat(verified.replace('Z','+00:00'))
            if dt.replace(tzinfo=dt.tzinfo or timezone.utc)>now:raise ValueError('Future source verification')
        if expired(row.get('expiry'),now):continue
        offers.append(row)
    return {'source':'that.promo','policy_url':'https://that.promo/developers','collected_at':now.isoformat(),
      'source_generated_at':data.get('generated_at'),'count':len(offers),'offers':offers}
def prepare_saasoffers(data, now):
    rows=data.get('deals')
    if not isinstance(rows,list) or not 1<=len(rows)<=1000:raise ValueError('Invalid SaaSOffers list')
    offers=[];seen=set()
    for r in rows:
        if r.get('access')!='free':continue
        # Do not redistribute access/promo codes; hold even ambiguous code-bearing entries.
        if re.search(r'\b(?:code|coupon|promo)\b',json.dumps(r),re.I):continue
        slug=r.get('slug')
        if not isinstance(slug,str) or not re.fullmatch('[a-z0-9-]+',slug):raise ValueError('Invalid slug')
        if slug in seen:continue
        seen.add(slug);link(r.get('url'),True)
        if urlsplit(r['url']).hostname!='saasoffers.tech':raise ValueError('Wrong source host')
        expiry=r.get('expires_at')
        if expired(expiry,now):continue
        offers.append({'slug':slug,'url':r['url'],'name':r.get('name'),'provider':r.get('name'),
          'category':r.get('category'),'summary':r.get('description'),'value':r.get('offer'),
          'who_qualifies':r.get('eligibility'),'expiry':expiry,'last_verified':None,'official_url':None,
          'caveats':'Source lists free access to this offer, not unconditional free software. Eligibility and current merchant terms must be checked. Country availability is not supplied.',
          'how_to_claim':'Read the SaaSOffers source detail page. This API does not provide a direct merchant URL.'})
    return {'source':'SaaSOffers','policy_url':'https://saasoffers.tech/ai','collected_at':now.isoformat(),
      'source_generated_at':data.get('updated'),'count':len(offers),'offers':offers}
def render(data):
    cards=[]
    categories=sorted({r.get('category') for r in data['offers'] if isinstance(r.get('category'),str) and r['category'].strip()},key=str.casefold)
    category_options=''.join('<option value="'+html.escape(c,quote=True)+'">'+html.escape(c)+'</option>' for c in categories)
    now=datetime.fromisoformat(data['collected_at'])
    for r in data['offers']:
        stale=not r.get('last_verified') or (now.date()-datetime.fromisoformat(r['last_verified'].replace('Z','+00:00')).date()).days>30
        fields=''.join('<dt>'+label+'</dt><dd>'+text(r.get(key))+'</dd>' for key,label in [
          ('value','Benefit · 혜택'),('who_qualifies','Eligibility · 신청 자격'),('expiry','Expiry · 종료 조건'),('caveats','Limitations · 주의사항'),('how_to_claim','How to claim · 이용 방법')])
        official=('<a rel="nofollow noopener" href="'+link(r['official_url'])+'">Official terms · 공식 조건 확인 ↗</a>') if r.get('official_url') else '<span>Direct merchant link not supplied · 판매처 직접 링크 미제공</span>'
        cards.append('<article data-category="'+html.escape(r.get('category') or '',quote=True)+'"><p class="provider">'+text(r.get('provider'))+' · '+text(r.get('category'))+'</p><h2>'+text(r.get('name'))+'</h2><p>'+text(r.get('summary'))+'</p><p>Source verified · 출처 확인일: '+text(r.get('last_verified'))+(' · <strong>Over 30 days old or unknown · 재확인 필요</strong>' if stale else '')+'</p><dl>'+fields+'</dl><p class="links">'+official+'<a href="'+link(r['url'],True)+'">'+text(data['source'])+' source ↗</a></p></article>')
    if not cards: cards.append('<p>No currently eligible offers from this source · 현재 표시할 혜택이 없습니다.</p>')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>SaaS & developer benefits · DevTeardown</title><style>body{font:16px/1.65 system-ui;background:#f6f7f9;color:#172333;max-width:1080px;margin:auto;padding:24px}header,article{background:white;border:1px solid #dde3eb;border-radius:14px;padding:24px;margin:20px 0}h1{font-size:30px;line-height:1.2}h2{font-size:22px;line-height:1.35;margin:8px 0}a{color:#164fc6}dt{font-weight:650;margin-top:12px}dd{margin:2px 0;overflow-wrap:anywhere}.provider{color:#526173}.links,nav{display:flex;gap:20px;flex-wrap:wrap}input,select{font:inherit;padding:12px;width:100%;box-sizing:border-box}article[hidden]{display:none}@media(max-width:600px){body{padding:12px}header,article{padding:18px}h1{font-size:26px}}</style><header><nav><a href="/ko/">핫딜</a><a href="/feeds/">DealNews feed</a><a href="/feeds/startup-benefits/">that.promo</a><a href="/feeds/saasoffers/">SaaSOffers</a></nav><h1>SaaS & developer benefits<br>개발자·스타트업 혜택</h1><p>Source-reported credits and programs, not cash discounts or guaranteed eligibility. Country availability, final terms and expiry must be checked on the official page. No automatic signups. Sponsored entries excluded.</p><p>출처가 제공하는 크레딧·프로그램 정보입니다. 확정 할인 상품이 아니며, 한국 등 국가별 이용 가능 여부와 자격·종료 조건은 공식 페이지에서 확인하세요. 판매가격·재고로 환산하거나 국가 필터에 합산하지 않습니다. 원문은 영어이며 자동 가입은 하지 않습니다.</p><p>Source: <a href="'''+link(data['policy_url'])+'''">'''+text(data['source'])+''' · reuse terms</a>. Each source verification date is shown separately from our collection time.</p><p>Collection · 수집: '''+text(data['collected_at'])+' · '+str(data['count'])+''' offers</p><p>Source dataset generated · 원본 생성: '''+text(data.get('source_generated_at'))+'''</p><label for="category">Category · 카테고리</label><select id="category"><option value="">All categories · 전체</option>'''+category_options+'''</select><label for="search">Search provider, benefit or eligibility · 검색</label><input id="search" type="search" placeholder="e.g. credits, open source, startup"><p id="search-count" role="status" aria-live="polite"></p><p id="no-results" hidden>No matching offers. Try a provider or a shorter keyword.<br>검색 결과가 없습니다. 서비스명이나 짧은 검색어로 다시 검색해 보세요.</p></header><main>'''+''.join(cards)+'''</main><script>const search=document.querySelector('#search');const category=document.querySelector('#category');const cards=[...document.querySelectorAll('article')];function filterOffers(){const q=search.value.trim().toLowerCase();let count=0;cards.forEach(x=>{x.hidden=!x.textContent.toLowerCase().includes(q)||(category.value!==''&&x.dataset.category!==category.value);if(!x.hidden)count++});document.querySelector('#search-count').textContent=count+' / '+cards.length+' offers · 검색 결과';document.querySelector('#no-results').hidden=count>0||cards.length===0}search.addEventListener('input',filterOffers);category.addEventListener('change',filterOffers);filterOffers()</script></html>'''
def main():
    p=argparse.ArgumentParser();p.add_argument('--destination',type=Path,required=True);p.add_argument('--input',type=Path);p.add_argument('--source',choices=('thatpromo','saasoffers'),default='thatpromo');a=p.parse_args()
    url=URL if a.source=='thatpromo' else 'https://saasoffers.tech/deals.json'
    if a.input: body=a.input.read_bytes()
    else:
        if not robots_allowed(url):raise ValueError('robots disallows source')
        body,_=read_url(url)
    data=(prepare if a.source=='thatpromo' else prepare_saasoffers)(json.loads(body),datetime.now(timezone.utc)); page=render(data)
    a.destination.mkdir(parents=True,exist_ok=True)
    (a.destination/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (a.destination/'index.html').write_text(page)
    print('Published source-reported benefits:',data['count'])
if __name__=='__main__':main()
