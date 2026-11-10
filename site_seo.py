"""Search-friendly provenance without invented review dates or endorsements."""
import re
import xml.etree.ElementTree as ET

BASE = 'https://devteardown.com'
POLICY = '/editorial-policy/'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'


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
        page.write_text(text, encoding='utf-8')
    # lastmod is optional. Build time is not a truthful content-modification date.
    # No reliable per-output revision date is stored yet, so omit rather than invent.
    sitemap = output / 'sitemap.xml'
    ET.register_namespace('', NS)
    ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for entry in root:
        for date in list(entry.findall('{'+NS+'}lastmod')):
            entry.remove(date)
    entry = ET.SubElement(root, '{'+NS+'}url')
    ET.SubElement(entry, '{'+NS+'}loc').text = BASE + POLICY
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
