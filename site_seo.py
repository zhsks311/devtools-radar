"""Search-friendly provenance without invented review dates or endorsements."""
import re
import html
import json
import xml.etree.ElementTree as ET

BASE = 'https://devteardown.com'
POLICY = '/editorial-policy/'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'

# These are localized navigation indexes. The linked articles stay English.
REPORT_META = {
    'en': ('Developer tool comparisons', 'Developer tool comparisons with published pricing, worked cost examples, and practical trade-offs.'),
    'ko': ('개발 도구 비교 가이드', '개발 도구의 공개 가격과 비용 계산, 장단점을 비교하세요. 비교글 본문은 영어 원문입니다.'),
    'zh': ('开发工具比较指南', '比较开发工具的公开价格、成本计算和优缺点。比较文章正文为英文。'),
    'ja': ('開発ツール比較ガイド', '開発ツールの公開料金、費用計算、長所と短所を比較。比較記事の本文は英語です。'),
    'es': ('Comparativas de herramientas de desarrollo', 'Compara precios publicados, ejemplos de costes y ventajas de herramientas de desarrollo. Los artículos están en inglés.'),
    'fr': ('Comparatifs des outils de développement', 'Comparez les tarifs publiés, les exemples de coûts et les compromis des outils de développement. Les articles sont en anglais.'),
}


def language_groups():
    from site_i18n import PATHS
    reports = {lang: '/' if lang == 'en' else f'/reports/{lang}/' for lang in REPORT_META}
    return (dict(PATHS, **{'x-default': PATHS['en']}),
            dict(reports, **{'x-default': reports['en']}))


def alternates_for(path):
    if path.startswith('/compare/'):
        return {'en': path, 'x-default': path}
    return next((group for group in language_groups() if path in group.values()), {})


def set_meta(text, kind, key, value):
    tag = f'<meta {kind}="{key}" content="{html.escape(value, quote=True)}">'
    pattern = rf'<meta\s+{kind}="{re.escape(key)}"[^>]*>'
    if re.search(pattern, text):
        return re.sub(pattern, lambda _: tag, text)
    return text.replace('</head>', tag + '\n</head>', 1)


def page_discovery(text, path):
    """Normalize identity after localization, never invent translations or reviews."""
    url = BASE + path
    lang_match = re.search(r'<html[^>]*lang="([^"]+)"', text)
    lang = lang_match.group(1) if lang_match else 'en'
    if path == '/' or path.startswith('/reports/'):
        name, description = REPORT_META[lang]
        text = re.sub(r'<title>.*?</title>', lambda _: f'<title>{html.escape(name)} | DevTeardown</title>', text, count=1, flags=re.S)
        text = set_meta(text, 'name', 'description', description)
        text = set_meta(text, 'name', 'twitter:title', name + ' | DevTeardown')
        text = set_meta(text, 'name', 'twitter:description', description)
        text = set_meta(text, 'property', 'og:title', name + ' | DevTeardown')
        text = set_meta(text, 'property', 'og:description', description)
        # Screen readers should not pronounce untranslated abstracts in the UI language.
        text = text.replace('class="index-list">', 'class="index-list" lang="en">')
        for section in ('gear-note', 'updated-note'):
            text = text.replace(f'class="{section}">', f'class="{section}" lang="en">')
    text = set_meta(text, 'property', 'og:url', url)
    text = set_meta(text, 'property', 'og:site_name', 'DevTeardown')
    group = alternates_for(path)
    if group:
        text = re.sub(r'<link[^>]+rel="alternate"[^>]+hreflang="[^"]+"[^>]*>', '', text)
        links = ''.join(f'<link rel="alternate" hreflang="{language}" href="{BASE}{target}">'
                        for language, target in group.items())
        text = text.replace('</head>', links + '\n</head>', 1)

    title = re.search(r'<title>(.*?)</title>', text, re.S)
    description = re.search(r'<meta name="description" content="([^"]*)"', text)
    if title and 'property="og:title"' not in text:
        text = set_meta(text, 'property', 'og:title', html.unescape(title.group(1)))
    if description and 'property="og:description"' not in text:
        text = set_meta(text, 'property', 'og:description', html.unescape(description.group(1)))
    text = set_meta(text, 'property', 'og:type', 'article' if path.startswith('/compare/') else 'website')
    text = set_meta(text, 'name', 'twitter:card', 'summary')
    page_type = ('AboutPage' if path == POLICY else 'WebPage' if path.startswith('/compare/')
                 else 'CollectionPage' if group else 'WebPage')
    page = {'@type': page_type, '@id': url + '#webpage', 'url': url,
            'name': html.unescape(title.group(1)) if title else 'DevTeardown',
            'inLanguage': lang, 'isPartOf': {'@id': BASE + '/#website'},
            'publisher': {'@id': BASE + '/#publisher'}}
    if description:
        page['description'] = html.unescape(description.group(1))
    if path.startswith('/compare/'):
        page['mainEntity'] = {'@id': url + '#article'}
    elif path == '/' or path.startswith('/reports/'):
        page['mainEntity'] = {'@id': url + '#comparisons'}

    def update_schema(match):
        value = json.loads(match.group(1))
        # Replace copied site/page definitions with one consistent graph below.
        own_graph = any(node.get('@id') == BASE + '/#website' for node in value.get('@graph', []))
        if value.get('@type') in ('WebSite', 'CollectionPage') or own_graph:
            return ''
        if value.get('@type') == 'ItemList':
            value['@id'] = url + '#comparisons'
        return '<script type="application/ld+json">' + json.dumps(value, ensure_ascii=False).replace('<', '\\u003c') + '</script>'

    text = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_schema, text, flags=re.S)
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': BASE + '/#publisher', 'name': 'DevTeardown', 'url': BASE + POLICY},
        {'@type': 'WebSite', '@id': BASE + '/#website', 'name': 'DevTeardown', 'url': BASE + '/',
         'publisher': {'@id': BASE + '/#publisher'}, 'inLanguage': list(REPORT_META)}, page]}
    schema = json.dumps(graph, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    text = text.replace('</head>', '<script type="application/ld+json">' + schema + '</script>\n</head>', 1)
    # Removing old metadata must not leave whitespace-only lines in generated diffs.
    head, separator, body = text.partition('</head>')
    return re.sub(r'(?m)^[ \t]+$', '', head) + separator + body


def finalize_seo(output, items, css):
    policy = output / 'editorial-policy' / 'index.html'
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Editorial and source policy | DevTeardown</title>
<meta name="description" content="How to read DevTeardown comparisons, price calculations, deal sources and country eligibility, and how to report a correction.">
<link rel="canonical" href="https://devteardown.com/editorial-policy/">
<style>''' + css + '''</style></head><body>
<header><div class="container"><a href="/">DevTeardown comparisons</a> · <a href="/deals/">Deal catalog</a></div></header>
<main class="container"><h1>Editorial and source policy</h1>
<p class="lead">A comparison is a starting point for a decision, not a substitute for the vendor's terms or a live checkout.</p>
<h2>What this site is</h2><p>DevTeardown publishes developer-tool comparisons and a multilingual catalog of product and software offers. The publisher is identified by this site brand. Brand authorship does not imply a named independent expert or a laboratory test.</p>
<h2>Sources and calculations</h2><p>Comparison articles link to their source material. Published vendor documentation and pricing are the basis for source-based claims. Cost examples use stated assumptions; they are not measured performance benchmarks or guaranteed invoices. A conclusion or recommendation is editorial interpretation, not a vendor endorsement.</p>
<p>A recorded source-review date describes the date stored with an article. It does not mean every linked page was rechecked on the day you visit. Rebuilding or translating a page is not a fresh verification. Follow the original sources for current limits, currency, tax, regional pricing and terms.</p>
<h2>Deals and purchase eligibility</h2><p>A deal-source link explains where an offer was found; a product link leads to the seller. Neither alone proves current stock or a successful purchase. Displayed prices are observations, not live quotes. A manufacturer listing without a verified discount must not be read as a confirmed bargain.</p>
<p>Language and purchase country are separate. A translated page does not establish delivery, activation, payment eligibility or local warranty. Read each offer's regional conditions. Unknown eligibility is not approval to buy. Check the seller's checkout before paying.</p>
<h2>Editorial and shopping links</h2><p>Shopping links are identified separately from comparison prose. Some shopping links may be affiliate links where disclosed; a link or inclusion is not a guarantee of quality. This site does not ask you to rely on a fabricated customer rating, test result or personal-use claim.</p>
<h2>Translations and automated assistance</h2><p>The catalog has multiple language views of the same inventory. Comparison articles remain English unless a page explicitly says otherwise. Translation can lose detail; use the linked original terms to resolve ambiguity. Automated collection and text processing do not replace source checks.</p>
<h2>Corrections</h2><p><a href="https://github.com/zhsks311/devtools-radar/issues">Report a correction in the public repository</a> with the page URL, disputed statement and a primary source. Do not include account details, private receipts, personal contact information or other secrets in a public issue. Corrections can change conclusions; a review date alone is not proof that a claim is correct.</p>
<h2>Search and AI use</h2><p>Static page text, source links, structured data and a sitemap help systems interpret this site. They do not guarantee indexing, ranking, rich results or AI citations. The plain-text directory is an optional convenience, not a special search requirement.</p>
</main><footer><div class="container"><a href="/">Comparisons</a> · <a href="/deals/">Deals</a></div></footer></body></html>''', encoding='utf-8')
    # Apply after localization so every generated page has the same provenance link.
    for page in output.rglob('*.html'):
        text = page.read_text(encoding='utf-8')
        if 'href="/editorial-policy/"' not in text:
            text = text.replace('</footer>', '<p style="text-align:center"><a href="/editorial-policy/" lang="en">Editorial &amp; source policy (English)</a></p></footer>')
        path = '/' + page.parent.relative_to(output).as_posix().strip('./')
        if path != '/':
            path += '/'
        page.write_text(page_discovery(text, path), encoding='utf-8')
    # lastmod is optional. Build time is not a truthful content-modification date.
    # No reliable per-output revision date is stored yet, so omit rather than invent.
    sitemap = output / 'sitemap.xml'
    ET.register_namespace('', NS)
    ET.register_namespace('xhtml', XHTML)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for entry in root:
        for date in list(entry.findall('{'+NS+'}lastmod')):
            entry.remove(date)
        for alternate in list(entry.findall('{'+XHTML+'}link')):
            entry.remove(alternate)
        location = entry.find('{'+NS+'}loc').text
        for language, path in alternates_for(location.removeprefix(BASE)).items():
            ET.SubElement(entry, '{'+XHTML+'}link', {'rel': 'alternate', 'hreflang': language, 'href': BASE + path})
    if not any(entry.find('{'+NS+'}loc').text == BASE + POLICY for entry in root):
        entry = ET.SubElement(root, '{'+NS+'}url')
        ET.SubElement(entry, '{'+NS+'}loc').text = BASE + POLICY
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
