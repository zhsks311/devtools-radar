#!/usr/bin/env python3
"""Check generated HTML/JSON-LD, expected article files and sitemap membership."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.errors=[]; self.script=None; self.script_text=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        for name,value in attrs.items():
            if name.lower().startswith('on'):
                self.errors.append('inline event handler')
            if name in ('href','src') and value:
                self.links.append(value)
                if value.strip().lower().startswith(('javascript:','data:','vbscript:')):
                    self.errors.append('unsafe URL scheme')
        if tag=='script' and attrs.get('type')=='application/ld+json':
            self.script=True;self.script_text=[]
    def handle_data(self,data):
        if self.script:self.script_text.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.script:
            try:json.loads(''.join(self.script_text))
            except ValueError:self.errors.append('invalid JSON-LD')
            self.script=None

def check_site(output, data):
    output=Path(output);items=json.loads(Path(data).read_text(encoding='utf-8'));errors=[]
    expected={i['slug'] for i in items}
    actual={p.parent.name for p in (output/'compare').glob('*/index.html')}
    if expected != actual: errors.append('article output differs from build input')
    for page in output.rglob('*.html'):
        parser=Page();parser.feed(page.read_text(encoding='utf-8'))
        errors.extend(f'{page.relative_to(output)}: {error}' for error in parser.errors)
        for href in parser.links:
            if href.startswith(('http:','https:','#','mailto:')):continue
            clean=href.split('#')[0].split('?')[0]
            target=output/clean.lstrip('/') if clean.startswith('/') else page.parent/clean
            if not target.suffix:target=target/'index.html'
            if not target.exists():errors.append(f'{page.relative_to(output)}: broken local link {href}')
    root=ET.parse(output/'sitemap.xml').getroot()
    sitemap={e.text for e in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    for slug in expected:
        if not any(url.endswith(f'/compare/{slug}/') for url in sitemap):errors.append(f'missing sitemap entry {slug}')
    return errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'dist');parser.add_argument('--data',type=Path,default=ROOT/'data/tools.json');args=parser.parse_args()
    try:errors=check_site(args.output,args.data)
    except (ValueError,OSError,ET.ParseError) as exc:errors=[str(exc)]
    for error in errors:print(error,file=sys.stderr)
    print('Output verification:', 'FAIL' if errors else 'PASS')
    return bool(errors)

if __name__=='__main__':sys.exit(main())
