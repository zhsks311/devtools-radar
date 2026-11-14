#!/usr/bin/env python3
"""Check generated HTML/JSON-LD, expected article files and sitemap membership."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://devteardown.com'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.errors=[]; self.script=None; self.script_text=[]; self.links=[]
        self.lang=None; self.canonicals=[]; self.alternates={}; self.metadata={}; self.schemas=[]
        self.titles=[]; self.in_title=False; self.h1_count=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag == 'html': self.lang=attrs.get('lang')
        if tag == 'title': self.titles.append(''); self.in_title=True
        if tag == 'h1': self.h1_count+=1
        if tag == 'meta':
            key=attrs.get('name') or attrs.get('property')
            if key: self.metadata.setdefault(key,[]).append(attrs.get('content',''))
        if tag == 'link':
            if attrs.get('rel') == 'canonical': self.canonicals.append(attrs.get('href'))
            if attrs.get('rel') == 'alternate' and attrs.get('hreflang'):
                lang=attrs['hreflang']
                if lang in self.alternates: self.errors.append('duplicate hreflang '+lang)
                self.alternates[lang]=attrs.get('href')
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
        if self.in_title:self.titles[-1]+=data
    def handle_endtag(self,tag):
        if tag == 'title': self.in_title=False
        if tag=='script' and self.script:
            try:self.schemas.append(json.loads(''.join(self.script_text)))
            except ValueError:self.errors.append('invalid JSON-LD')
            self.script=None


def schema_nodes(schemas):
    for value in schemas:
        if isinstance(value, list):
            yield from schema_nodes(value)
        elif isinstance(value, dict):
            yield value
            yield from schema_nodes(value.get('@graph', []))


def check_discovery(pages, entries, robots_text):
    """Fail the build for conflicting identity, language or crawl declarations."""
    errors=[]
    sitemap={}
    for entry in entries:
        url=entry.findtext('{'+NS+'}loc')
        if url in sitemap: errors.append('duplicate sitemap URL '+str(url))
        sitemap[url]=entry
    if set(sitemap) != set(pages):
        errors.append('sitemap must contain exactly the generated canonical HTML pages')
    robot=RobotFileParser(); robot.parse(robots_text.splitlines())
    if BASE+'/sitemap.xml' not in (robot.site_maps() or []):
        errors.append('robots.txt missing canonical sitemap')
    for url, page in pages.items():
        if not page.lang: errors.append(url+': missing document language')
        if len(page.titles)!=1 or not page.titles[0].strip(): errors.append(url+': expected one nonempty title')
        descriptions=page.metadata.get('description',[])
        if len(descriptions)!=1 or not descriptions[0].strip(): errors.append(url+': expected one description')
        if page.h1_count!=1: errors.append(url+': expected one H1')
        if page.canonicals != [url]: errors.append(url+': canonical must match page URL without filters')
        if page.metadata.get('og:url') != [url]: errors.append(url+': Open Graph URL differs from canonical')
        if any('noindex' in value.lower() for value in page.metadata.get('robots',[])):
            errors.append(url+': indexable page has noindex')
        for agent in ('Googlebot','Bingbot','OAI-SearchBot','PerplexityBot'):
            if not robot.can_fetch(agent,url): errors.append(url+': blocked by robots.txt for '+agent)
        for lang, target in page.alternates.items():
            if target not in pages:
                errors.append(url+': hreflang target is not a canonical generated page'); continue
            other=pages[target]
            if lang!='x-default' and other.lang!=lang:
                errors.append(url+': hreflang target language mismatch '+lang)
            if other.alternates!=page.alternates:
                errors.append(url+': hreflang set is not reciprocal')
        if page.alternates and page.alternates.get(page.lang)!=url:
            errors.append(url+': hreflang set must include itself')
        entry=sitemap.get(url)
        if entry is not None:
            xml_links=entry.findall('{'+XHTML+'}link')
            xml_alts={node.get('hreflang'):node.get('href') for node in xml_links}
            if len(xml_links)!=len(xml_alts) or xml_alts!=page.alternates:
                errors.append(url+': sitemap/HTML hreflang mismatch')
        definitions=list(schema_nodes(page.schemas))
        page_schema=next((node for node in definitions if node.get('@id')==url+'#webpage'),None)
        if not page_schema or page_schema.get('url')!=url or page_schema.get('inLanguage')!=page.lang:
            errors.append(url+': structured page identity/language mismatch')
        for node in definitions:
            if node.get('@type')=='TechArticle':
                if node.get('mainEntityOfPage')!=url: errors.append(url+': article identity mismatch')
                if not node.get('citation'): errors.append(url+': article is missing citations')
                elif any(source not in page.links for source in node['citation']):
                    errors.append(url+': structured citation is not linked on the visible page')
    return errors

def check_site(output, data):
    output=Path(output);items=json.loads(Path(data).read_text(encoding='utf-8'));errors=[]
    expected={i['slug'] for i in items}
    actual={p.parent.name for p in (output/'compare').glob('*/index.html')}
    if expected != actual: errors.append('article output differs from build input')
    pages={}
    for page in output.rglob('*.html'):
        parser=Page();parser.feed(page.read_text(encoding='utf-8'))
        relative=page.relative_to(output).as_posix()
        path='/' + (relative[:-10] if relative.endswith('index.html') else relative)
        pages[BASE+path]=parser
        errors.extend(f'{page.relative_to(output)}: {error}' for error in parser.errors)
        for href in parser.links:
            if href.startswith(('http:','https:','#','mailto:')):continue
            clean=href.split('#')[0].split('?')[0]
            target=output/clean.lstrip('/') if clean.startswith('/') else page.parent/clean
            if not target.suffix:target=target/'index.html'
            if not target.exists():errors.append(f'{page.relative_to(output)}: broken local link {href}')
    # Check exact reviewed summaries as well as shape: punctuation alone cannot
    # establish that prose is accurate or that a word was not silently sliced.
    sys.path.insert(0, str(ROOT))
    from article_metadata import article_description, validate_description
    for item in items:
        url=BASE+'/compare/'+item['slug']+'/'
        page=pages.get(url)
        if page is None: continue
        try: expected_description=article_description(item)
        except ValueError as exc:
            errors.append(url+': '+str(exc)); continue
        for field in ('description', 'og:description', 'twitter:description'):
            values=page.metadata.get(field, [])
            if values != [expected_description]:
                errors.append(url+': '+field+' must match the complete reviewed summary')
            for value in values:
                try: validate_description(value)
                except ValueError as exc: errors.append(url+': '+field+': '+str(exc))
    root=ET.parse(output/'sitemap.xml').getroot()
    sitemap={e.text for e in root.iter('{'+NS+'}loc')}
    for slug in expected:
        if not any(url.endswith(f'/compare/{slug}/') for url in sitemap):errors.append(f'missing sitemap entry {slug}')
    errors.extend(check_discovery(pages,list(root),(output/'robots.txt').read_text(encoding='utf-8')))
    return errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'dist');parser.add_argument('--data',type=Path,default=ROOT/'data/tools.json');args=parser.parse_args()
    try:errors=check_site(args.output,args.data)
    except (ValueError,OSError,ET.ParseError) as exc:errors=[str(exc)]
    for error in errors:print(error,file=sys.stderr)
    print('Output verification:', 'FAIL' if errors else 'PASS')
    return bool(errors)

if __name__=='__main__':sys.exit(main())
