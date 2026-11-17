#!/usr/bin/env python3
"""Publish a separately attributed, unchanged RSS display; never curate prices."""
import argparse, hashlib, html, json, re, shutil
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

class UnsafeFeed(ValueError): pass
class SafeMarkup(HTMLParser):
    tags={'img','div','p','ul','ol','li','a','br','strong','b','em','i','span','s','strike'}
    attrs={'src','href','alt','title','class','style','width','height','rel','target'}
    def handle_starttag(self,tag,attrs):
        if tag not in self.tags: raise UnsafeFeed('Unsupported feed markup; whole feed held')
        for k,v in attrs:
            if k not in self.attrs: raise UnsafeFeed('Unsupported feed attribute')
            if k in {'src','href'}: safe_url(v)
            if k=='style' and (re.search(r'url|expression|position|@|\\',v,re.I) or not re.fullmatch(r'[a-zA-Z0-9 :;.,%#()\-]+',v)): raise UnsafeFeed('Unsupported feed style')
    def handle_endtag(self,tag):
        if tag not in self.tags: raise UnsafeFeed('Unsupported closing tag')
    def handle_comment(self,data): raise UnsafeFeed('Unsupported comment')
    def handle_decl(self,decl): raise UnsafeFeed('Unsupported declaration')

def safe_url(v):
    p=urlsplit(v or '')
    if p.scheme!='https' or not p.hostname or p.username or p.password: raise UnsafeFeed('Unsafe URL')
    return v

def render(body,status):
    if len(body)>2_000_000 or b'<!DOCTYPE' in body.upper() or b'<!ENTITY' in body.upper(): raise UnsafeFeed('Unsafe XML')
    root=ET.fromstring(body);channel=root.find('channel')
    if root.tag!='rss' or channel is None: raise UnsafeFeed('Expected RSS')
    items=channel.findall('item')
    if not 1<=len(items)<=200: raise UnsafeFeed('Unexpected item count')
    cards=[]
    for item in items:
        title=item.findtext('title');link=safe_url(item.findtext('link'));desc=item.findtext('description') or ''
        if not title or not desc: raise UnsafeFeed('Incomplete item')
        SafeMarkup().feed(desc) # Reject rather than delete or rewrite source content.
        metadata=[]
        for e in item:
            if e.tag in {'title','link','description'}:continue
            name=e.tag.split('}')[-1];value=(e.text or '')+(' '+json.dumps(e.attrib,ensure_ascii=False) if e.attrib else '')
            metadata.append('<dt>'+html.escape(name)+'</dt><dd>'+html.escape(value)+'</dd>')
        cards.append('<article><h2><a href="'+html.escape(link,quote=True)+'">'+html.escape(title)+'</a></h2><div class="source-content">'+desc+'</div><details><summary>RSS metadata · 원문 메타데이터</summary><dl>'+''.join(metadata)+'</dl></details></article>')
    success=status.get('last_success_at',''); datetime.fromisoformat(success.replace('Z','+00:00'))
    issue='' if status.get('status') in {'collected','not_modified'} else '<p class="warning">Latest collection failed. Last-good feed retained. 최근 수집 실패, 이전 원문을 보존했습니다.</p>'
    # Notices stay outside the unchanged source display. No affiliate rewrites, translations or filtering.
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>DealNews RSS · DevTeardown</title><style>body{font:16px/1.6 system-ui;margin:auto;max-width:1100px;padding:24px;background:#f6f7f9;color:#172333}a{color:#164fc6}header,.warning{padding:20px;border:1px solid #dce2ea;border-radius:12px;background:#fff}article{padding:24px;margin:20px 0;background:white;border:1px solid #dce2ea;border-radius:12px;display:flow-root}h2{font-size:21px;line-height:1.4}.source-content{display:flow-root;overflow-wrap:anywhere}.source-content img{max-width:100%;height:auto}dl{font-size:12px;overflow-wrap:anywhere}dt{font-weight:bold}dd{margin:0 0 6px}details{clear:both;margin-top:16px}.warning{background:#fff3d5}nav{display:flex;gap:18px;flex-wrap:wrap}@media(max-width:600px){body{padding:14px}article{padding:16px}.source-content img{float:none!important;display:block;margin:0 auto 16px!important}}</style><header><nav><a href="/ko/">검증 상품 목록</a><a href="/deals/">Curated deals</a><a href="dealnews.xml">Original RSS</a></nav><h1>DealNews · 외부 딜 피드</h1><p>This is an automatically refreshed, unmodified DealNews RSS display, not DevTeardown-verified product cards. Links lead to DealNews, not necessarily the merchant. Prices, stock, coupons, expiry and delivery countries are source claims and may change. No DevTeardown affiliate links are inserted.</p><p>공식 RSS 원문을 자동 게시합니다. 판매처·가격·쿠폰·재고·배송 국가를 직접 검증한 상품 목록이 아닙니다. 링크는 DealNews 원문이며 상품 국가 필터에 합산하지 않습니다. 국내 커뮤니티 자동 게시는 아직 지원하지 않습니다.</p><p>Every 6 hours · Last successful collection / 마지막 수집: <time id="collected">'''+html.escape(success)+'''</time></p><p id="stale" class="warning" hidden>Over 12 hours since collection: feed may be stale. 수집 후 12시간 이상 경과했습니다. 원문 가격과 종료 여부를 확인하세요.</p>'''+issue+'''<p>Source: <a href="https://www.dealnews.com/">DealNews</a> · <a href="https://www.dealnews.com/pages/rss.html">RSS usage terms</a>. Original English content below; no translation or link changes.</p></header><section aria-label="Unmodified DealNews RSS"><h2>'''+html.escape(channel.findtext('title') or '')+'</h2><p>'+html.escape(channel.findtext('description') or '')+'</p>'+''.join(cards)+'''</section><script>function freshness(){document.querySelector('#stale').hidden=Date.now()-Date.parse(document.querySelector('#collected').textContent)<=12*3600000}freshness();setInterval(freshness,60000)</script></html>'''

def publish(collected,destination):
    status=json.loads((collected/'status.json').read_text());s=next(x for x in status['sources'] if x['id']=='dealnews')
    current=collected/'dealnews.xml'; previous=destination/'dealnews.xml'
    body=current.read_bytes() if current.exists() else previous.read_bytes() if previous.exists() else None
    if body is None: raise UnsafeFeed('No successful feed; nothing published')
    if hashlib.sha256(body).hexdigest()!=s.get('sha256'):raise UnsafeFeed('Feed integrity mismatch')
    try:
        output=render(body,s) # Validate all items before writing anything.
    except (UnsafeFeed, ET.ParseError, ValueError) as exc:
        prior_status=destination/'status.json'
        if not previous.exists() or not prior_status.exists(): raise
        old=next(x for x in json.loads(prior_status.read_text())['sources'] if x['id']=='dealnews')
        body=previous.read_bytes()
        if hashlib.sha256(body).hexdigest()!=old.get('sha256'): raise UnsafeFeed('Last-good integrity mismatch')
        for key in ('last_success_at','sha256','items','etag','last_modified'):
            if key in old:s[key]=old[key]
        s.update(status='error',error='New feed held: '+str(exc)[:160])
        output=render(body,s)

    destination.mkdir(parents=True,exist_ok=True)
    (destination/'index.html').write_text(output)
    (destination/'dealnews.xml').write_bytes(body)
    (destination/'status.json').write_text(json.dumps(status,indent=2)+'\n')
    return len(ET.fromstring(body).findall('channel/item'))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--collected',type=Path,required=True);p.add_argument('--destination',type=Path,required=True);a=p.parse_args();print('Published source RSS items:',publish(a.collected,a.destination))
