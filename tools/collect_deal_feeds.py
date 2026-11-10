#!/usr/bin/env python3
"""Bounded official RSS collection. Never modifies curated/public deal records."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
UA='DevTeardownFeedMonitor/1.0 (+https://devteardown.com/)'
MAX_BYTES=2_000_000

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def read_url(url, headers=None):
    with build_opener(NoRedirect).open(Request(url,headers={'User-Agent':UA,**(headers or {})}),timeout=25) as r:
        body=r.read(MAX_BYTES+1)
        if len(body)>MAX_BYTES: raise ValueError('Response exceeds limit')
        return body,dict(r.headers)

def robots_allowed(url):
    parsed=urlsplit(url)
    if parsed.scheme!='https' or parsed.username or parsed.password: raise ValueError('HTTPS source required')
    robots=f'{parsed.scheme}://{parsed.netloc}/robots.txt'
    try: body,_=read_url(robots)
    except HTTPError as e:
        if e.code==404:return True
        raise
    p=RobotFileParser();p.parse(body.decode('utf-8',errors='replace').splitlines())
    delay = p.crawl_delay(UA) or p.crawl_delay('*') or 0
    if delay > 120:raise ValueError('robots crawl delay exceeds bounded run; review required')
    if delay > 2:time.sleep(delay)
    return p.can_fetch(UA,url)

def parse_feed(body):
    if b'<!DOCTYPE' in body.upper() or b'<!ENTITY' in body.upper():raise ValueError('XML declarations rejected')
    root=ET.fromstring(body)
    if root.tag!='rss':raise ValueError('Expected RSS document')
    count=len(root.findall('./channel/item'))
    if not count:raise ValueError('Empty RSS; preserve last-good state')
    return count

def collect(config,out,previous=None):
    out.mkdir(parents=True,exist_ok=True)
    old=json.loads(previous.read_text()) if previous and previous.exists() else {}
    now=datetime.now(timezone.utc).isoformat()
    result={'attempted_at':now,'published_deals_changed':False,'sources':[]}
    for s in config['sources']:
        status={'id':s['id'],'enabled':s['enabled'],'mode':s['mode'],'note':s['note']}
        prior=next((v for v in old.get('sources',[]) if v['id']==s['id']),{})
        for field in ('last_success_at','etag','last_modified','sha256','items'):
            if field in prior:status[field]=prior[field]
        if not s['enabled']:
            status['status']='disabled';result['sources'].append(status);continue
        cached_ok=False
        cached=None
        try:
            if not robots_allowed(s['url']):raise ValueError('robots.txt disallows source')
            cached = previous.parent/f'{s["id"]}.xml' if previous else None
            cached_ok = bool(cached and cached.exists() and hashlib.sha256(cached.read_bytes()).hexdigest() == prior.get('sha256'))
            headers={}
            if cached_ok and prior.get('etag'):headers['If-None-Match']=prior['etag']
            if cached_ok and prior.get('last_modified'):headers['If-Modified-Since']=prior['last_modified']
            time.sleep(2)
            body,h=read_url(s['url'],headers)
            count=parse_feed(body)
            # Preserve RSS byte-for-byte. No link rewriting or public card auto-generation.
            (out/f'{s["id"]}.xml').write_bytes(body)
            status.update(status='collected',last_success_at=now,items=count,
                sha256=hashlib.sha256(body).hexdigest(),etag=h.get('ETag'),last_modified=h.get('Last-Modified'))
        except HTTPError as e:
            status['status']='not_modified' if e.code==304 else 'blocked' if e.code in (401,403,429) else 'error'
            if e.code==304:
                status['last_success_at']=now
                if cached_ok:(out/f'{s["id"]}.xml').write_bytes(cached.read_bytes())
            status['error']=f'HTTP {e.code}'
        except Exception as e:status.update(status='error',error=str(e)[:200])
        result['sources'].append(status)
    (out/'status.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'collection-output');p.add_argument('--previous',type=Path)
    args=p.parse_args(); result=collect(json.loads((ROOT/'config/deal_sources.json').read_text()),args.output,args.previous)
    print(json.dumps(result,indent=2))
    if any(s['enabled'] and s['status'] in ('blocked','error') for s in result['sources']):raise SystemExit(1)
