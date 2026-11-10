import os
import re
import json
import html
import datetime
import argparse
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from tools.validate_data import validate_items

BASE_URL = "https://devteardown.com"
SITE_NAME = "DevTools Radar"
ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
DATA_PATH = ROOT / "data" / "tools.json"

SHARED_CSS = """
:root { --bg:#f6f4ee; --surface:#fffdf8; --surface-raised:#eeece4; --border:#d7d5cb;
  --text:#252923; --text-muted:#60665e; --primary:#315c46; --accent:#315c46; --warn:#815a20; --danger:#984732; }
* { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; scroll-padding-top:2rem; }
body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; line-height:1.7; -webkit-font-smoothing:antialiased; }
.container,.header-inner { max-width:1000px; margin:0 auto; padding:2rem 1.5rem; }
header { border-bottom:1px solid var(--border); }
.header-inner { display:flex; justify-content:space-between; align-items:center; gap:1.5rem; padding-top:1.25rem; padding-bottom:1.25rem; }
.logo { color:var(--text); font-weight:750; text-decoration:none; font-size:1.16rem; letter-spacing:-.04em; white-space:nowrap; }
.logo span { color:var(--primary); margin-left:.25rem; font-weight:450; }
.nav-link { color:var(--text-muted); font-size:.82rem; text-decoration:none; }
a { color:var(--primary); text-underline-offset:3px; }
a:hover { text-decoration:underline; }
a:focus-visible,button:focus-visible { outline:2px solid var(--primary); outline-offset:4px; }
h1,h2,h3,h4,strong { color:var(--text); }
h1 { font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.2rem,5vw,3.6rem); font-weight:400; line-height:1.12; letter-spacing:-.045em; margin:.9rem 0 1.3rem; }
h2 { font-size:1.35rem; margin:2.8rem 0 1rem; line-height:1.35; letter-spacing:-.025em; }
h3 { font-size:1.05rem; margin:1.6rem 0 .6rem; line-height:1.45; }
h4 { margin:1.4rem 0 .4rem; }
p { margin-bottom:1rem; }
ul,ol { margin:0 0 1.1rem 1.35rem; }
li { margin-bottom:.35rem; }
.lead { color:var(--text-muted); font-size:1.08rem; max-width:700px; line-height:1.8; }
.lead p { color:inherit; font-size:inherit; }
.badge { display:inline-block; font-size:.73rem; font-weight:500; letter-spacing:.02em; color:var(--text-muted); }
.badge-blue,.badge-green { color:var(--primary); }
.badge-gray { color:var(--text-muted); }
.badge-warn { color:var(--warn); }
.meta-row { display:flex; flex-wrap:wrap; align-items:center; gap:.6rem; font-size:.8rem; color:var(--text-muted); }
.table-wrapper { overflow-x:auto; margin:1.5rem 0 2rem; border-top:2px solid var(--text); border-bottom:1px solid var(--border); }
table { width:100%; border-collapse:collapse; text-align:left; font-size:.9rem; }
th,td { padding:.85rem 1rem; border-bottom:1px solid var(--border); vertical-align:top; }
th { background:var(--surface-raised); font-weight:600; }
.btn { display:inline-block; padding:.65rem 1rem; font-size:.88rem; text-decoration:none; border:1px solid var(--border); text-align:center; }
.btn-primary { background:var(--primary); color:var(--surface); border-color:var(--primary); }
.btn-outline { color:var(--primary); }
.card { padding:1.3rem; border:1px solid var(--border); }
a.card { display:block; text-decoration:none; }
a.card:hover { border-color:var(--primary); }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); gap:1.2rem; margin:1.5rem 0; }
.index-intro { padding:2rem 0 2.5rem; border-bottom:2px solid var(--text); }
.eyebrow,.section-label { color:var(--primary); font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:.74rem; letter-spacing:.07em; text-transform:uppercase; }
.index-intro h1 { max-width:650px; }
.index-list { display:grid; grid-template-columns:1fr 1fr; column-gap:3rem; }
a.index-entry { display:block; color:inherit; text-decoration:none; border-bottom:1px solid var(--border); padding:1.7rem 0; }
.index-entry h2 { font-family:Georgia,"Times New Roman",serif; font-size:1.6rem; font-weight:400; margin:.55rem 0 .65rem; }
.index-entry:hover h2 { color:var(--primary); text-decoration:underline; text-underline-offset:5px; }
.index-entry p { font-size:.9rem; color:var(--text-muted); margin:0; }
.entry-meta { display:flex; justify-content:space-between; gap:1rem; color:var(--text-muted); font-size:.73rem; }
.verdict-box { border-left:3px solid var(--primary); background:var(--surface-raised); padding:1.2rem 1.5rem; margin:1.6rem 0; }
.verdict-box .label,.toc-title { font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:.74rem; color:var(--primary); margin-bottom:.5rem; }
.verdict-box p:last-child { margin-bottom:0; }
.toc { border-block:1px solid var(--border); padding:1rem 0; margin:2rem 0; }
.toc ol { margin-bottom:0; }
.toc a { color:var(--text-muted); font-size:.9rem; }
.pros-cons-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.25rem; margin:1.5rem 0; }
.pros-box,.cons-box { padding:.8rem 0; }
.pros-box ul,.cons-box ul { margin:.6rem 0 0 1.1rem; font-size:.9rem; }
pre { background:#252d29; color:#e8ede5; padding:1.2rem; overflow-x:auto; font-size:.82rem; line-height:1.6; margin:1rem 0; tab-size:2; }
code { font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:.87em; background:var(--surface-raised); color:var(--primary); padding:.1rem .25rem; overflow-wrap:anywhere; }
pre code { color:inherit; background:none; padding:0; overflow-wrap:normal; }
blockquote,.migration-box { border-left:2px solid var(--border); padding:.5rem 1.2rem; margin:1.4rem 0; }
.faq-item { border-bottom:1px solid var(--border); padding:1.1rem 0; }
.faq-q { font-weight:600; margin-bottom:.4rem; }
.faq-a { font-size:.94rem; color:var(--text-muted); }
.cost-row { display:grid; gap:.35rem; padding:1rem 0; border-bottom:1px solid var(--border); }
.cost-label { font-weight:600; }
.cost-formula { font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:.82rem; color:var(--text-muted); overflow-wrap:anywhere; }
.cost-result,.matrix-pick { color:var(--primary); font-weight:600; }
.sources-list { font-size:.86rem; overflow-wrap:anywhere; }
.updated-note,.method-note { font-size:.82rem; color:var(--text-muted); border-top:1px solid var(--border); margin-top:2.5rem; padding-top:1.2rem; }
.gear-note { border-top:1px solid var(--border); margin-top:3rem; padding-top:1.2rem; }
.gear-note h3 { margin:0 0 .5rem; font-size:.9rem; }
.gear-note p { font-size:.82rem; color:var(--text-muted); }
.gear-links { display:flex; flex-wrap:wrap; gap:.5rem 1.5rem; }
footer { border-top:1px solid var(--border); margin-top:3rem; color:var(--text-muted); }
footer p { font-size:.8rem; margin:0; }
@media(max-width:680px) {
  .container,.header-inner { padding:1.25rem; }
  .header-inner { align-items:flex-start; flex-direction:column; gap:.6rem; }
  .header-inner>div { flex-wrap:wrap; }
  .index-intro { padding:1.5rem 0 2rem; }
  .index-list,.pros-cons-grid { grid-template-columns:1fr; }
  th,td { padding:.65rem; min-width:120px; }
}
@media(prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } }
"""

# ---------------------------------------------------------------- markdown


def _esc(text):
    return html.escape(text, quote=True)


def _safe_url(value):
    """Only absolute HTTP(S) URLs are accepted from content."""
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        raise ValueError("Invalid URL")
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.username:
        raise ValueError("Only absolute HTTP(S) URLs without credentials are allowed")
    return html.escape(value, quote=True)


def _json_ld(value, **kwargs):
    return json.dumps(value, **kwargs).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _inline(text):
    """Inline markdown -> HTML. Code spans are protected from other rules."""
    code_spans = []

    def grab(m):
        code_spans.append(m.group(1))
        return "\x00%d\x00" % (len(code_spans) - 1)

    text = re.sub(r"`([^`]+)`", grab, text)
    text = _esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" rel="noopener">\1</a>',
        text,
    )
    for i, code in enumerate(code_spans):
        text = text.replace("\x00%d\x00" % i, "<code>%s</code>" % _esc(code))
    return text


def _split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def md_to_html(md):
    """Renders the markdown subset allowed by docs/tech-blog-writing-standard.md."""
    if not md:
        return ""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = ' class="language-%s"' % lang if re.fullmatch(r'[A-Za-z0-9_+-]+', lang) else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, _esc("\n".join(buf))))
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            header = _split_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i].strip()))
                i += 1
            th = "".join("<th>%s</th>" % _inline(c) for c in header)
            body = ""
            for r in rows:
                body += "<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r)
            out.append(
                '<div class="table-wrapper"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                % (th, body)
            )
            continue

        # headings (only ### and below; ## comes from section titles)
        m = re.match(r"^(#{3,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)), 4)
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2)), level))
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            out.append('<hr style="border:none;border-top:1px solid var(--border);margin:2rem 0;">')
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % _inline(" ".join(buf)))
            continue

        # ordered list
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
                while i < n and lines[i].strip() and not re.match(
                    r"^(\d+\.\s|[-*]\s|#{1,6}\s|\||>)", lines[i].strip()
                ) and lines[i].startswith("  "):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % _inline(x) for x in items))
            continue

        # bullet list
        if re.match(r"^[-*]\s", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
                while i < n and lines[i].strip() and lines[i].startswith("  ") and not re.match(
                    r"^(\d+\.\s|[-*]\s|#{1,6}\s|\||>)", lines[i].strip()
                ):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline(x) for x in items))
            continue

        # paragraph: gather until blank / block start
        buf = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt or re.match(r"^(#{1,6}\s|```|\||>|[-*]\s|\d+\.\s)", nxt):
                break
            buf.append(nxt)
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(buf)))
    return "\n".join(out)


def _plain(text):
    """Card excerpts: strip markdown markers so the teaser reads as prose."""
    return re.sub(r"[`*_]", "", text)


def slugify(text):
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", s)


def word_count(md):
    text = re.sub(r"[`*|>#-]", " ", md)
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def reading_time(item):
    body = " ".join(
        [s.get("content", "") for s in item.get("sections", [])]
        + [s.get("content", "") for s in item.get("deep_dive_sections", [])]
    )
    words = word_count(body) + 180  # chrome: table, matrix, faq
    return "%d min read" % max(4, round(words / 200))


def first_sentence(markdown: str) -> str:
    """Direct Answer 블록용 한 문장. 마크다운 기호를 걷어낸다."""
    text = re.sub(r"[`*_>#]", "", markdown or "")
    text = re.sub(r"\s+", " ", text).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text[:220]).strip()


def generate_llms_txt(items, ko_deals, en_deals) -> str:
    """llmstxt.org 형식: AI 검색엔진이 읽는 사이트 디렉토리."""
    lines = [
        "# DevTeardown",
        "",
        "> Independent teardowns of developer tools priced in arithmetic, plus a daily tech-deals radar",
        "> for Korean and global hardware deals. Every number is taken from a vendor price sheet or a",
        "> source post; derived figures print their formula. No paid placement.",
        "",
        "## Teardowns",
        "",
    ]
    for item in items:
        lines.append(f"- [{item['tool_a']['name']} vs {item['tool_b']['name']}]({BASE_URL}/compare/{item['slug']}/): "
                     f"{first_sentence(item.get('verdict_summary', ''))}")
    lines += [
        "",
        "## Deals",
        "",
        f"- [Korean tech deals]({BASE_URL}/ko/): {len(ko_deals.get('feed', []))} collected hardware deals from "
        "뽐뿌, 클리앙, 퀘이사존, 에펨코리아 and 폴센트, with source price and shipping.",
        f"- [Global tech deals]({BASE_URL}/deals/): {len(en_deals.get('feed', []))} collected deals from "
        "retailers and deal sources, with direct product links and dated checks. China listings are not verified discounts.",
        "",
        "## Optional",
        "",
        f"- [Full text for LLMs]({BASE_URL}/llms-full.txt): every teardown verdict and the current deal list.",
        f"- [Sitemap]({BASE_URL}/sitemap.xml)",
    ]
    return "\n".join(lines) + "\n"


def generate_llms_full_txt(items, ko_deals, en_deals) -> str:
    """LLM 인용용 전문: 테어다운 요약 + 현재 딜 목록."""
    out = ["# DevTeardown — full text for LLMs", "",
           "Source: https://devteardown.com · Updated: " + datetime.date.today().isoformat(), ""]
    for item in items:
        a, b = item["tool_a"]["name"], item["tool_b"]["name"]
        out += [
            f"## {a} vs {b}",
            f"URL: {BASE_URL}/compare/{item['slug']}/",
            f"Category: {item['category']} · Prices verified: {item.get('last_verified', '')}",
            "",
            "Verdict: " + first_sentence(item.get("verdict_summary", "")),
            "",
        ]
        for sec in item.get("sections", []):
            body = re.sub(r"[`*_>#]", "", sec.get("content", ""))
            out.append(f"### {sec['title']}")
            out.append(re.sub(r"\s+", " ", body).strip()[:900])
            out.append("")
    out += ["## Current deals (KR)", ""]
    for d in ko_deals.get("feed", [])[:10]:
        out.append(f"- {d['product']} — {d.get('price') or 'see source'} KRW at {d.get('store') or 'source'} "
                   f"({d.get('category_label')}) {d.get('source', {}).get('url', '')}")
    out += ["", "## Current deals (global)", ""]
    for d in en_deals.get("feed", []):
        out.append(f"- {d['product']} — {d.get('price')} {d.get('currency')} at {d.get('store') or 'source'} "
                   f"({d.get('category_label')}) {d.get('link', {}).get('url', '')} "
                   f"Purchase eligibility: {d.get('purchase_eligibility', {}).get('label', 'unverified')}. "
                   f"{next((line[7:] for line in d.get('briefing', []) if line.startswith('Check: ')), '')}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- pages

DEALS_SECTION_HTML = """
    <aside class="gear-note" aria-label="Affiliate links">
      <h3>Elsewhere: desk gear</h3>
      <p>Optional shopping links, separate from the comparisons. Check the seller for current prices and stock.</p>
      <p class="gear-links">
        <a href="https://link.coupang.com/a/iyxFRjouBM" target="_blank" rel="noopener nofollow sponsored">Logitech MX Master 3S</a>
        <a href="https://link.coupang.com/a/iyxHrMNtyC" target="_blank" rel="noopener nofollow sponsored">Apple M4 MacBook Pro</a>
        <a href="https://link.coupang.com/a/iyxEbxQMEK" target="_blank" rel="noopener nofollow sponsored">Coupang Goldbox</a>
      </p>
      <p>These are affiliate links; purchases may earn a commission.<br>
      이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
    </aside>
"""


# ---------------------------------------------------------------- deal portals

DEALS_DATA_PATH = ROOT / "data" / "deals.json"
DEALS_EN_DATA_PATH = ROOT / "data" / "deals_en.json"
KO_SITE_NAME = "DevTeardown KR"
KO_TAGLINE = "개발자 장비 & 테크 핫딜 레이더"
KO_DISCLOSURE = (
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, "
    "이에 따른 일정액의 수수료를 제공받습니다."
)

DEAL_CSS = """
.ko-hero { padding:2rem 0 1rem; }
.ko-hero h1 { font-family:inherit; font-size:clamp(2rem,4vw,2.7rem); font-weight:650; letter-spacing:-.05em; }
.ko-stats { display:flex; flex-wrap:wrap; gap:.5rem 1.5rem; margin:1.4rem 0; }
.ko-stat { font-size:.78rem; color:var(--text-muted); }
.ko-stat strong { margin-right:.4rem; }
.disclosure-bar { border-left:2px solid var(--border); padding:.5rem .9rem; font-size:.78rem; color:var(--text-muted); }
.quick-tabs { display:flex; gap:.5rem; overflow-x:auto; padding:.6rem 0 1rem; margin-bottom:1rem; }
.tab { flex:none; background:transparent; color:var(--text-muted); border:1px solid var(--border); padding:.5rem .8rem; font:inherit; font-size:.8rem; cursor:pointer; }
.tab.is-active { background:var(--primary); color:var(--surface); border-color:var(--primary); }
.tab .n { margin-left:.3rem; }
.deal-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr)); gap:1.5rem; }
.deal-card { display:flex; flex-direction:column; border:1px solid var(--border); background:var(--surface); padding:1.3rem; }
.deal-card.is-hidden { display:none; }
.international-deals .deal-grid { grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); gap:1rem; }
.international-deals .deal-title { font-size:1.3rem; line-height:1.3; min-height:3.4em; }
.international-deals .deal-card { padding:1.15rem; }
.deal-media { margin:0 0 1rem; }
.deal-media img { width:100%; height:150px; object-fit:contain; display:block; background:#fff; }
.deal-media figcaption { font-size:.68rem; line-height:1.4; color:var(--text-muted); margin-top:.35rem; }
.international-deals .deal-summary { font-size:.86rem; color:var(--text-muted); margin:0 0 .75rem; }
.international-deals .deal-facts { font-size:0.85rem; }
.international-deals .deal-check { font-size:0.8rem; line-height:1.5; }
.deal-top,.deal-foot { display:flex; justify-content:space-between; gap:.5rem; margin-bottom:.8rem; }
.cat-chip,.deal-src,.deal-foot { font-size:.73rem; color:var(--text-muted); }
.deal-title { margin:0 0 1rem; font-size:1.08rem; line-height:1.6; }
.deal-price { display:flex; align-items:baseline; flex-wrap:wrap; gap:.7rem; margin-bottom:.6rem; }
.deal-price strong { font-size:1.55rem; font-weight:600; }
.deal-price s,.deal-price .unknown { font-size:.85rem; color:var(--text-muted); }
.deal-flags { display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1rem; }
.flag { color:var(--primary); font-size:.74rem; }
.deal-facts { margin:0 0 1rem; }
.deal-facts .fact { display:grid; grid-template-columns:5rem 1fr; gap:.6rem; margin-bottom:.5rem; font-size:.82rem; }
.deal-facts dt { color:var(--text-muted); }
.deal-facts dd { margin:0; }
.deal-check { color:var(--text-muted); font-size:.74rem; }
.cta { display:block; text-align:center; padding:.7rem 1rem; background:var(--primary); color:var(--surface); text-decoration:none; font-size:.85rem; margin-top:auto; }
.cta.secondary { background:var(--surface-raised); color:var(--primary); }
.deal-foot { margin:.6rem 0 0; font-size:.72rem; }
.cat-head { display:flex; align-items:baseline; flex-wrap:wrap; gap:.7rem; margin-top:2.6rem; }
.cat-head h2 { margin:0; }
.cat-sub { color:var(--text-muted); font-size:.8rem; }
.cat-list { list-style:none; margin:1rem 0; border-top:1px solid var(--border); }
.cat-list li { display:flex; align-items:baseline; flex-wrap:wrap; gap:.7rem; padding:.8rem 0; border-bottom:1px solid var(--border); margin:0; }
.cat-list a { flex:1; min-width:180px; font-size:.9rem; }
.cat-list .p { font-weight:600; font-size:.9rem; }
.cat-list .s { font-size:.74rem; color:var(--text-muted); }
.pick-card { padding:1.2rem 0; border-block:1px solid var(--border); text-decoration:none; }
.pick-kicker { font-size:.72rem; color:var(--text-muted); }
.pick-card strong { display:block; margin:.5rem 0; }
.pick-card p,.pick-card .go { font-size:.85rem; }
.goldbox { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1.2rem; padding:1.5rem 0; margin-top:2rem; border-block:1px solid var(--border); }
.goldbox h3 { margin:0 0 .3rem; }
.goldbox p { font-size:.85rem; color:var(--text-muted); margin:0; }
"""

CAT_SHORT = {
    "vouchers": "상품권·쿠폰",
    "snacks": "과자·스낵",
    "keyboard-mouse": "키보드·마우스",
    "tech": "테크 장비",
    "monitor-desk": "모니터·데스크",
    "laptops": "노트북·PC",
    "afterwork": "커피·음료",
}

FACT_ICONS = [
    ("실구매가", "실구매가"),
    ("추천", "추천"),
    ("스펙", "스펙"),
    ("체크", "체크"),
    ("Price", "Price"),
    ("Good for", "Good for"),
    ("Specs", "Specs"),
    ("Shipping", "Shipping"),
    ("Check", "Check"),
    ("Key", "Key"),
    ("Region", "Region"),
    ("Condition", "Condition"),
    ("Checked", "Checked"),
]


def load_deals(path=DEALS_DATA_PATH):
    # Do not replace corrupt/missing production input with an apparently valid feed.
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("feed"), list):
        raise ValueError(f"Invalid deals feed: {path}")
    if not isinstance(data.get("categories", {}), dict) or not isinstance(data.get("picks", []), list):
        raise ValueError(f"Invalid deals categories/picks: {path}")
    return data


def _won(deal: dict) -> str:
    price = deal.get("price")
    if not price:
        return ""
    cur = deal.get("currency", "KRW")
    if cur == "KRW":
        return f"{int(price):,}원"
    prefix = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "CA$", "AUD": "A$"}.get(cur, cur + " ")
    return f"{prefix}{price:,.2f}" if price % 1 else f"{prefix}{int(price):,}"


def _fact_rows(deal: dict) -> str:
    rows = ""
    check = ""
    for line in deal.get("briefing", []):
        label, sep, value = line.partition(":")
        key = label.strip()
        if not sep or key in ("핵심", "Key"):
            continue
        if key in ("체크", "Check"):
            check = value.strip()
            continue
        icon = dict(FACT_ICONS).get(key, "")
        if not icon:
            continue
        rows += (f'<div class="fact"><dt>{html.escape(icon)}</dt>'
                 f'<dd>{html.escape(value.strip())}</dd></div>')
    facts = f'<dl class="deal-facts">{rows}</dl>' if rows else ""
    if check:
        facts += f'<p class="deal-check">{html.escape(check)}</p>'
    return facts


def _eligibility_rows(deal: dict) -> str:
    info = deal.get("purchase_eligibility") or {}
    values = [
        ("Purchase country", info.get("label", "Country eligibility unverified")),
        ("Delivery", info.get("delivery", "Not verified")),
        ("Activation", info.get("activation", "Not verified")),
        ("Payment", info.get("payment", "Not verified")),
        ("Tax & fees", info.get("tax", "Not verified")),
        ("Returns", info.get("returns", "Check retailer terms")),
        ("Evidence date", info.get("checked_at") or deal.get("checked_date") or "Unknown"),
    ]
    rows = "".join(f"<dt>{html.escape(k)}</dt><dd>{html.escape(str(v))}</dd>" for k,v in values)
    for policy in info.get('policy_urls', []):
        rows += '<dt>Retailer policy</dt><dd><a target="_blank" rel="noopener" href="' + _safe_url(policy) + '">Source terms</a></dd>'
    return '<details class="purchase-terms"><summary>Purchase eligibility: ' + html.escape(values[0][1]) + '</summary><dl>' + rows + '</dl></details>'


def _source_monitor_html() -> str:
    config = json.loads((ROOT / "config/deal_sources.json").read_text())
    rows = "".join('<li><a href="' + _safe_url(s['policy_url']) + '">' + html.escape(s['name']) + '</a>: ' + html.escape(s['note']) + '</li>' for s in config['sources'])
    return '<section class="method-note"><h2>Source monitoring</h2><p>Official feed checks are scheduled every six hours. GitHub schedules can be delayed. New feed items are review candidates, not verified product offers. Existing price-check dates are never refreshed by a feed check.</p><p><a href="https://github.com/zhsks311/devtools-radar/actions/workflows/deal-feeds.yml">Latest collection runs and source status</a></p><ul>' + rows + '</ul><p>China storefront listings are labeled separately. Listed prices are not verified discounts; address-specific stock, delivery and payment eligibility may be unverified. A Chinese source or CNY price alone does not prove purchase eligibility.</p></section>'


def _deal_card(deal: dict, lang: str = "ko") -> str:
    link = deal.get("link") or {}
    url = _safe_url(link.get("url", ""))
    tracked = bool(link.get("tracked"))
    is_global = deal.get("region") == "global"
    if is_global:
        cta = "View product →" if link.get("label_kind") == "retailer" else "View deal →"
        rel = "noopener nofollow"
    elif tracked:
        cta, rel = "쿠팡에서 보기 →", "noopener nofollow sponsored"
    else:
        cta, rel = "쿠팡에서 검색 →", "noopener nofollow"

    price = _won(deal)
    price_html = f"<strong>{html.escape(price)}</strong>" if price else (
        '<span class="unknown">원문 가격 확인</span>' if lang == "ko" else '<span class="unknown">See price at source</span>')
    if deal.get("original_price"):
        orig = deal["original_price"]
        orig_txt = _won({"price": orig, "currency": deal.get("currency", "KRW")})
        price_html += f"<s>{html.escape(orig_txt)}</s>"

    flags = ""
    if deal.get("discount_pct"):
        flags += f'<span class="flag flag-discount">-{html.escape(str(deal["discount_pct"]))}%</span>'
    ship = deal.get("shipping") or ""
    if "무료" in ship or ship == "Free shipping":
        flags += f'<span class="flag flag-free">{html.escape(ship)}</span>'
    elif ship:
        flags += f'<span class="flag flag-ship">{html.escape(ship)}</span>'
    if deal.get("rocket"):
        flags += '<span class="flag flag-rocket">로켓배송</span>'

    note = ""
    if not tracked and not is_global:
        note = '<span class="note">제휴 링크 없음 · 쿠팡 검색</span>'
    foot = ""
    src_url = _safe_url((deal.get("source") or {}).get("url", "")) if (deal.get("source") or {}).get("url") else ""
    if src_url and src_url != url:
        label = "원문 보기" if lang == "ko" else "Source post"
        foot = f'<div class="deal-foot"><a href="{src_url}" target="_blank" rel="noopener nofollow">{label}</a>{note}</div>'

    media = deal.get("image") or {}
    media_html = ""
    if lang == "en" and re.fullmatch(r"/assets/deals/[a-z0-9-]+\.png", media.get("path", "")):
        media_html = (f'<figure class="deal-media"><img src="{html.escape(media["path"])}" '
                      f'alt="{html.escape(media.get("alt", ""))}" loading="lazy" decoding="async">'
                      f'<figcaption>{html.escape(media.get("caption", ""))} '
                      f'<a href="{_safe_url(media.get("credit_url", ""))}" target="_blank" rel="noopener">'
                      f'{html.escape(media.get("credit", ""))}</a></figcaption></figure>')
    summary = next((line[5:].strip() for line in deal.get("briefing", []) if line.startswith("Key: ")), "") if lang == "en" else ""
    summary_html = f'<p class="deal-summary">{html.escape(summary)}</p>' if summary else ""
    cat_label = deal.get("category_label", "")
    cat = html.escape(CAT_SHORT.get(deal.get("category", ""), cat_label) if lang == "ko" else cat_label)
    return f"""
      <article class="deal-card" data-cat="{html.escape(deal.get('category', 'tech'))}">
        {media_html}
        <div class="deal-top">
          <span class="cat-chip">{cat}</span>
          <span class="deal-src">{html.escape(deal.get('store') or (deal.get('source') or {}).get('label', ''))}</span>
        </div>
        <h3 class="deal-title">{html.escape(deal.get('product', ''))}</h3>
        {summary_html}
        <div class="deal-price">{price_html}</div>
        <div class="deal-flags">{flags}</div>
        {_fact_rows(deal)}
        {_eligibility_rows(deal) if lang == "en" else ""}
        <a class="cta" href="{url}" target="_blank" rel="{rel}">{cta}</a>
        {foot}
      </article>"""


def _tabs(categories: dict, labels: list[tuple[str, str]], total: int, lang: str = "ko") -> str:
    tabs = f'<button class="tab is-active" data-filter="all">전체 <span class="n">{total}</span></button>' if lang == "ko" \
        else f'<button class="tab is-active" data-filter="all">All <span class="n">{total}</span></button>'
    for slug, label in labels:
        count = len((categories.get(slug) or {}).get("items", []))
        tabs += (f'<button class="tab" data-filter="{slug}">{html.escape(label)}'
                 f' <span class="n">{count}</span></button>')
    return f'<nav class="quick-tabs" id="quickTabs">{tabs}</nav>'


TABS_JS = """
<script>
(function () {
  var tabs = document.querySelectorAll('#quickTabs .tab');
  var cards = document.querySelectorAll('#feedGrid .deal-card');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) { t.classList.remove('is-active'); });
      tab.classList.add('is-active');
      var f = tab.getAttribute('data-filter');
      cards.forEach(function (c) {
        var show = (f === 'all') || (c.getAttribute('data-cat') === f);
        c.classList.toggle('is-hidden', !show);
      });
    });
  });
})();
</script>
"""


def generate_ko_html(deals: dict) -> str:
    feed = deals.get("feed", [])
    categories = deals.get("categories", {})
    picks = deals.get("picks", [])
    goldbox = deals.get("goldbox") or {"url": "https://link.coupang.com/a/iyxEbxQMEK", "label": "쿠팡 골드박스"}
    updated = deals.get("generated_at", "")[:10].replace("-", ".") or "2026.11.10"

    feed_cards = "".join(_deal_card(d) for d in feed[:24])
    if not feed_cards:
        feed_cards = ('<p style="color:var(--text-muted);font-size:0.92rem;padding:1rem 0;">'
                      '지금 수집된 신규 테크 핫딜이 없습니다. 아래 큐레이션과 골드박스를 확인하세요.</p>')

    tabs = _tabs(
        categories,
        [("vouchers", "상품권·쿠폰"), ("snacks", "과자·스낵"),
         ("keyboard-mouse", "키보드·마우스"), ("tech", "테크 장비"),
         ("monitor-desk", "모니터·데스크"), ("laptops", "노트북·PC"),
         ("afterwork", "커피·음료")],
        len(feed[:24]),
    )

    cat_html = ""
    for slug in ("vouchers", "snacks", "keyboard-mouse", "tech", "monitor-desk", "laptops", "afterwork"):
        cat = categories.get(slug) or {}
        rows = ""
        for d in cat.get("items", [])[:4]:
            link = d.get("link") or {}
            price = _won(d) or "가격 확인"
            rows += (f'<li><a href="{_safe_url(link.get("url", ""))}" target="_blank" '
                     f'rel="noopener nofollow sponsored">{html.escape(d.get("product", ""))}</a>'
                     f'<span class="p">{price}</span>'
                     f'<span class="s">{html.escape(d.get("store") or "")}</span></li>')
        body = f'<ul class="cat-list">{rows}</ul>' if rows else (
            '<p style="color:var(--text-muted);font-size:0.88rem;">이 카테고리에 새로 올라온 핫딜이 없습니다. 아래 큐레이션을 참고하세요.</p>')
        cat_html += f"""
    <div class="cat-head" id="{slug}">
      <h2>{html.escape(cat.get('label', slug))}</h2>
      <span class="cat-sub">{html.escape(cat.get('audience', ''))}</span>
    </div>
    {body}"""

    pick_cards = ""
    for p in picks:
        pick_cards += f"""
      <a class="pick-card" href="{_safe_url(p['url'])}" target="_blank" rel="noopener nofollow sponsored">
        <div class="pick-kicker">{html.escape(p.get('kicker', ''))}</div>
        <strong>{html.escape(p.get('title', ''))}</strong>
        <p>{html.escape(p.get('desc', ''))}</p>
        <span class="go">쿠팡에서 가격 확인 →</span>
      </a>"""

    schema = {
        "@context": "https://schema.org", "@type": "WebSite", "name": KO_SITE_NAME,
        "alternateName": KO_TAGLINE, "url": f"{BASE_URL}/ko/", "inLanguage": "ko-KR",
        "description": "개발자 장비·테크 핫딜을 원문 가격 그대로 모아 실구매가와 추천 대상을 정리하는 한글 핫딜 레이더.",
    }

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{KO_SITE_NAME} — {KO_TAGLINE} (2026)</title>
  <meta name="description" content="개발자 장비·테크 핫딜을 뽐뿌·클리앙·퀘이사존·에펨코리아·폴센트에서 모아 가격·할인율·배송 조건을 정리하고, 실구매가와 추천 대상을 한눈에 보여주는 한글 핫딜 레이더.">
  <link rel="canonical" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/deals/">
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
  <meta property="og:site_name" content="{KO_SITE_NAME}">
  <meta property="og:title" content="{KO_SITE_NAME} — {KO_TAGLINE}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/ko/">
  <meta property="og:locale" content="ko_KR">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{KO_SITE_NAME} — {KO_TAGLINE}">
  <meta name="twitter:description" content="원문 가격 그대로 모은 개발자 장비·테크 핫딜. 실구매가와 추천 대상만 남겼습니다.">
  <script type="application/ld+json">
  {_json_ld({
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "수집된 테크 핫딜",
      "itemListElement": [
          {"@type": "ListItem", "position": i + 1,
           "name": d.get("product", ""),
           "url": (d.get("link") or {}).get("url", "")}
          for i, d in enumerate(feed[:24])
      ],
  }, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {_json_ld(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}{DEAL_CSS} .purchase-terms {{ font-size:.85rem; margin:1rem 0; }} .purchase-terms summary {{ cursor:pointer; font-weight:600; }} .purchase-terms dl {{ display:grid; grid-template-columns:1fr; gap:.2rem; }} .purchase-terms dd {{ margin:0 0 .65rem; color:var(--text-muted); }}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="/ko/" class="logo">DevTeardown<span>KR</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="#feed">수집된 핫딜</a>
        <a class="nav-link" href="/deals/">Global Deals</a>
        <a class="nav-link" href="/">EN Reports</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="ko-hero">
      <span class="badge badge-blue">원문 게시글 기준</span>
      <h1>장비 살 때, 가격부터 비교.</h1>
      <p class="lead">뽐뿌·클리앙·퀘이사존·에펨코리아·폴센트에 올라온 테크 핫딜을 한곳에 모아,
      게시글에 적힌 가격과 배송 조건을 정리했습니다.
      할인 조건과 재고는 구매 전에 판매 페이지에서 확인하세요.</p>
      <div class="ko-stats">
        <div class="ko-stat"><strong>{len(feed)}건</strong>수집된 핫딜</div>
        <div class="ko-stat"><strong>{len(categories)}개</strong>핫딜 카테고리</div>
        <div class="ko-stat"><strong>{html.escape(updated)}</strong>업데이트</div>
      </div>
      <div class="disclosure-bar">
        {html.escape(deals.get('disclosure', KO_DISCLOSURE))}
      </div>
    </div>

    <h2 id="feed" style="margin-top:2.4rem;">수집된 테크 · 개발자 핫딜</h2>
    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:-0.3rem;">
      가격·할인율·배송은 수집 시점의 원문 표기입니다. 품절·가격 변동은 원문에서 확인하세요.
    </p>
    {tabs}
    <div class="deal-grid" id="feedGrid">{feed_cards}</div>

    <div class="goldbox">
      <div>
        <h3>쿠팡 골드박스</h3>
        <p>현재 판매 상품과 할인 조건은 쿠팡에서 확인하세요.</p>
      </div>
      <a class="cta" style="width:auto; padding:0.75rem 1.2rem;" href="{_safe_url(goldbox['url'])}" target="_blank" rel="noopener nofollow sponsored">{html.escape(goldbox.get('label', '골드박스 보기'))} →</a>
    </div>

    {cat_html}

    <h2 style="margin-top:3.4rem;">함께 볼 만한 책상 장비</h2>
    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:-0.3rem;">
      할인 여부와 별개로 모아 둔 장비입니다. 아래 링크는 제휴 링크입니다.</p>
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));">{pick_cards}</div>

    <div class="method-note">
      <strong style="color:var(--text-muted);">이 페이지가 가격을 다루는 방식</strong><br>
      모든 가격은 수집한 원문 게시글의 표기를 그대로 옮깁니다. 할인율은 원문에 정가가 있을 때만 계산하고,
      없으면 추정하지 않습니다. 쿠팡 링크는 파트너스 트래킹 링크이며, 트래킹 링크가 없는 상품은
      '쿠팡 검색'으로 표시해 수익 링크와 구분합니다. 가격·재고는 언제든 바뀌므로 결제 전 원문 확인이 필요합니다.<br><br>
      {html.escape(deals.get('disclosure', KO_DISCLOSURE))}
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 {KO_SITE_NAME}. 개발자 장비 핫딜 큐레이션. 가격은 원문 표기 기준입니다.</p>
      <p style="margin-top:0.4rem;"><a href="/deals/" style="color:var(--text-muted);">Global deals →</a>
      &nbsp;·&nbsp;<a href="/" style="color:var(--text-muted);">English teardowns →</a></p>
    </div>
  </footer>
  {TABS_JS}
</body>
</html>"""


def generate_deals_en_html(payload: dict) -> str:
    """해외 딜 포털 (/deals/) — 영문."""
    feed = payload.get("feed", [])
    categories = payload.get("categories", {})
    updated = payload.get("generated_at", "")[:10] or "2026-11-10"

    feed_cards = "".join(_deal_card(d, lang="en") for d in feed)
    if not feed_cards:
        feed_cards = ('<p style="color:var(--text-muted);font-size:0.92rem;padding:1rem 0;">'
                      'No new tech deals collected right now. Check back after the next run.</p>')

    tabs = _tabs(
        categories,
        [(slug, cat.get("label", slug)) for slug, cat in categories.items()],
        len(feed), lang="en",
    )

    cat_html = ""
    for slug in ():  # Cards already provide the complete category listing.
        cat = categories.get(slug) or {}
        rows = ""
        for d in cat.get("items", [])[:4]:
            link = d.get("link") or {}
            price = _won(d) or "see source"
            rows += (f'<li><a href="{_safe_url(link.get("url", ""))}" target="_blank" '
                     f'rel="noopener nofollow">{html.escape(d.get("product", ""))}</a>'
                     f'<span class="p">{price}</span>'
                     f'<span class="s">{html.escape(d.get("store") or "")}</span></li>')
        body = f'<ul class="cat-list">{rows}</ul>' if rows else (
            '<p style="color:var(--text-muted);font-size:0.88rem;">No new deals in this category yet.</p>')
        cat_html += f"""
    <div class="cat-head" id="{slug}">
      <h2>{html.escape(cat.get('label', slug))}</h2>
      <span class="cat-sub">{html.escape(cat.get('audience', ''))}</span>
    </div>
    {body}"""

    schema = {
        "@context": "https://schema.org", "@type": "WebSite", "name": "DevTeardown Deals",
        "url": f"{BASE_URL}/deals/", "inLanguage": "en",
        "description": "Software offers with direct retailer links and price-check notes.",
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevTeardown Deals — Software & Tech Offers (2026)</title>
  <meta name="description" content="Software offers checked on retailer product pages, with prices and license conditions.">
  <link rel="canonical" href="{BASE_URL}/deals/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/deals/">
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/deals/">
  <meta property="og:site_name" content="DevTeardown Deals">
  <meta property="og:title" content="DevTeardown Deals — software and tech offers">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/deals/">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="DevTeardown Deals — software and tech offers">
  <meta name="twitter:description" content="Software offers with direct product links and dated price checks.">
  <script type="application/ld+json">
  {_json_ld({
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Browse the offers",
      "itemListElement": [
          {"@type": "ListItem", "position": i + 1,
           "name": d.get("product", ""),
           "url": (d.get("link") or {}).get("url", "")}
          for i, d in enumerate(feed)
      ],
  }, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {_json_ld(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}{DEAL_CSS} .purchase-terms {{ font-size:.85rem; margin:1rem 0; }} .purchase-terms summary {{ cursor:pointer; font-weight:600; }} .purchase-terms dl {{ display:grid; grid-template-columns:1fr; gap:.2rem; }} .purchase-terms dd {{ margin:0 0 .65rem; color:var(--text-muted); }}</style>
</head>
<body class="international-deals">
  <header>
    <div class="header-inner">
      <a href="/deals/" class="logo">DevTeardown<span>Deals</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="/ko/">Korean deals</a>
        <a class="nav-link" href="/">Teardowns</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="ko-hero">
      <span class="badge badge-blue">Direct retailer links</span>
      <h1>Tech offers. Clear purchase terms.</h1>
      <p class="lead">Offers labelled with purchase eligibility evidence, not by the currency or the source website.
      Every button opens the actual product page, not a search or community post.
      Prices keep their original currency. Country restrictions, activation, delivery and checkout conditions are listed on each card.</p>
      <div class="ko-stats">
        <div class="ko-stat"><strong>{len(feed)}</strong>product offers</div>
        <div class="ko-stat"><strong>{sum(bool(c.get("items")) for c in categories.values())}</strong>categories with deals</div>
        <div class="ko-stat"><strong>{html.escape(updated)}</strong>updated</div>
        <div class="ko-stat"><strong>{html.escape(str(payload.get('stats', {}).get('sources', 0)))}</strong>sources</div>
      </div>
    </div>

    <h2 id="feed" style="margin-top:2.4rem;">Browse the offers</h2>
    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:-0.3rem;">
      Listed prices exclude untested coupon savings. Australia delivery is confirmed only where noted; digital country eligibility and checkout totals remain unverified.
      Redemption deadlines apply; review refund terms before activating a license.
    </p>
    {tabs}
    <div class="deal-grid" id="feedGrid">{feed_cards}</div>

    {cat_html}

    {_source_monitor_html()}
    <div class="method-note">
      <strong style="color:var(--text-muted);">How prices are handled</strong><br>
      Retailer prices and visible availability were checked at the time noted on each card; checkout was not completed.
      A source post alone does not verify the current price. Crossed-out prices are retailer comparisons,
      not proof of a historical low. These direct product links carry no DevTeardown affiliate tracking.
      Confirm eligibility, tax and the final total before buying. “Lifetime” refers to the offer’s license or service terms, not an unlimited guarantee.
      Official media assets are credited where supplied; other product images remain on retailer pages.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 DevTeardown Deals. Software and tech curation. Check the retailer for the current total.</p>
      <p style="margin-top:0.4rem;"><a href="/ko/" style="color:var(--text-muted);">Korean deals →</a>
      &nbsp;·&nbsp;<a href="/" style="color:var(--text-muted);">English teardowns →</a></p>
    </div>
  </footer>
  {TABS_JS}
</body>
</html>"""


def _excerpt(text, limit=175):
    text = " ".join(_plain(text).split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def generate_index_html(items):

    cards_html = ""
    for item in items:
        a = item["tool_a"]
        b = item["tool_b"]
        cards_html += f"""
        <a class="index-entry" href="./compare/{item['slug']}/">
          <div class="entry-meta"><span>{html.escape(item['category'])}</span><span>{reading_time(item)}</span></div>
          <h2>{html.escape(a['name'])} <span style="color:var(--text-muted);">/</span> {html.escape(b['name'])}</h2>
          <p>{html.escape(_excerpt(item.get('hook', item['verdict_summary'])))}</p>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME} — Developer tool comparisons</title>
  <meta name="description" content="Developer tool comparisons with published pricing, worked cost examples, and practical trade-offs.">
  <link rel="canonical" href="{BASE_URL}/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/">
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:description" content="Independent teardowns of developer tools: billing units, worked cost arithmetic, and a decision matrix you can paste into a design doc.">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{SITE_NAME} — Developer Tool Teardowns">
  <meta name="twitter:description" content="Compare developer tools, their costs, and their trade-offs.">
  <meta property="og:title" content="{SITE_NAME} — Developer Tool Teardowns">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/">
  <script type="application/ld+json">
  {_json_ld({
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Developer tool teardowns",
      "itemListElement": [
          {"@type": "ListItem", "position": i + 1,
           "url": f"{BASE_URL}/compare/{it['slug']}/",
           "name": f"{it['tool_a']['name']} vs {it['tool_b']['name']}"}
          for i, it in enumerate(items)
      ],
  }, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {_json_ld({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": SITE_NAME,
      "url": BASE_URL,
      "inLanguage": "en",
      "description": "Developer tool comparisons with pricing and trade-offs.",
  }, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="./" class="logo">DevTools<span>Radar</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="./deals/">Deals</a>
        <a class="nav-link" href="./ko/">한국어 핫딜</a>
      </div>
    </div>
  </header>

  <main class="container">
    <section class="index-intro">
      <div class="eyebrow">Notes on choosing software</div>
      <h1>Before you pick<br>the next tool.</h1>
      <p class="lead">What it costs, where it fits, and what you give up. Comparisons of developer tools, with pricing examples you can check against your own workload.</p>
    </section>
    <h2 class="section-label">The comparisons · {len(items):02d}</h2>
    <div class="index-list">
      {cards_html}
    </div>

    {DEALS_SECTION_HTML}

    <div class="updated-note">
      <strong>A note on the numbers.</strong> Articles link to vendor pricing and documentation.
      Cost examples show their assumptions and formulas; they are not measured benchmarks.
      Check each article's verification date and the current vendor price before making a decision.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 {SITE_NAME}. Developer tool comparisons. Shopping links are marked separately.</p>
    </div>
  </footer>
</body>
</html>"""


def generate_comparison_html(item):
    a = item["tool_a"]
    b = item["tool_b"]
    slug = item["slug"]
    updated = item.get("last_verified", "2026-11-10")
    rt = reading_time(item)

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in item["faqs"]
        ],
    }
    schema_article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": f"{a['name']} vs {b['name']}: a 2026 engineering teardown",
        "description": item["hook"].replace('"', "'"),
        "dateModified": updated,
        "datePublished": item.get("published", updated),
        "author": {"@type": "Organization", "name": "DevTeardown Team"},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
        "mainEntityOfPage": f"{BASE_URL}/compare/{slug}/",
    }
    schema_crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Comparisons", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2,
             "name": f"{a['name']} vs {b['name']}", "item": f"{BASE_URL}/compare/{slug}/"},
        ],
    }

    a_pros_html = "".join(f"<li>{html.escape(p)}</li>" for p in a.get("pros", []))
    a_cons_html = "".join(f"<li>{html.escape(c)}</li>" for c in a.get("cons", []))
    b_pros_html = "".join(f"<li>{html.escape(p)}</li>" for p in b.get("pros", []))
    b_cons_html = "".join(f"<li>{html.escape(c)}</li>" for c in b.get("cons", []))

    sections = item.get("sections") or item.get("deep_dive_sections", [])

    # table of contents
    toc_items = ""
    for idx, sec in enumerate(sections, start=1):
        toc_items += f'<li><a href="#s{idx}">{html.escape(sec["title"])}</a></li>'
    for name, anchor in (("Cost arithmetic", "cost"),
                         ("Decision matrix", "matrix"),
                         ("Migration path", "migration"),
                         ("FAQ", "faq")):
        if (name == "Cost arithmetic" and item.get("cost_math")) or \
           (name == "Decision matrix" and item.get("decision_matrix")) or \
           (name == "Migration path" and item.get("migration_guide")) or name == "FAQ":
            toc_items += f'<li><a href="#{anchor}">{name}</a></li>'

    # sections
    sections_html = ""
    for idx, sec in enumerate(sections, start=1):
        sections_html += f"""
      <h2 id="s{idx}">{idx}. {html.escape(sec['title'])}</h2>
      {md_to_html(sec.get('content', ''))}
"""

    # cost math
    cost_html = ""
    if item.get("cost_math"):
        rows = ""
        for c in item["cost_math"]:
            rows += f"""
        <div class="cost-row">
          <div class="cost-label">{_inline(c['label'])}</div>
          <div class="cost-formula">{html.escape(c['formula'])}</div>
          <div class="cost-result">{_inline(c['result'])}</div>
        </div>"""
        cost_html = f"""
      <h2 id="cost">Cost arithmetic at volume</h2>
      <p>These are computed from the published unit prices, not measured. Each row prints its own formula,
      so you can replace our assumption with your traffic and redo it.</p>
      <div class="card" style="padding:0.4rem 1.4rem;">{rows}</div>"""

    # decision matrix
    matrix_html = ""
    if item.get("decision_matrix"):
        trs = ""
        for r in item["decision_matrix"]:
            trs += (
                f"<tr><td>{_inline(r['situation'])}</td>"
                f"<td class=\"matrix-pick\">{_inline(r['pick'])}</td>"
                f"<td>{_inline(r['why'])}</td></tr>"
            )
        matrix_html = f"""
      <h2 id="matrix">Decision matrix</h2>
      <p>Rows are the situation you are actually in. Pick the row before you read the pricing page again.</p>
      <div class="table-wrapper"><table>
        <thead><tr><th>If this is you</th><th>Take</th><th>Because</th></tr></thead>
        <tbody>{trs}</tbody>
      </table></div>"""

    # faqs
    faqs_html = ""
    for f in item["faqs"]:
        faqs_html += f"""
        <div class="faq-item">
          <div class="faq-q">{_inline(f['q'])}</div>
          <div class="faq-a">{_inline(f['a'])}</div>
        </div>"""

    # sources
    sources_html = ""
    if item.get("sources"):
        links = "".join(
            f'<a href="{_safe_url(u)}" rel="noopener nofollow" target="_blank">{html.escape(u)}</a><br>'
            for u in item["sources"]
        )
        sources_html = f"""
      <h2>Sources &amp; verification</h2>
      <p class="sources-list">Prices and limits were read from these pages on <strong>{html.escape(updated)}</strong>.
      Vendor marketing claims are quoted as claims. Anything derived is arithmetic on the numbers below.</p>
      <div class="card"><p class="sources-list">{links}</p></div>"""

    migration_html = ""
    if item.get("migration_guide"):
        migration_html = f"""
      <h2 id="migration">Migration path</h2>
      <div class="migration-box">
        <strong>What switching actually takes</strong>
        <div style="margin-top:0.5rem;">{md_to_html(item['migration_guide'])}</div>
      </div>"""

    related = item.get("related", [])
    related_html = ""
    if related:
        rel_cards = ""
        for r in related:
            rel_cards += f"""
          <a class="card" href="../{r['slug']}/" style="padding:1.1rem;">
            <h3 style="margin:0 0 0.3rem; font-size:1rem; color:var(--text-muted);">{html.escape(r['name'])}</h3>
            <p style="margin:0; font-size:0.85rem; color:var(--text-muted);">{html.escape(r['why'])}</p>
          </a>"""
        related_html = f"""
      <h2>Keep reading</h2>
      <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr));">{rel_cards}</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(a['name'])} vs {html.escape(b['name'])} (2026): Cost, Limits and the Decision Matrix</title>
  <meta name="description" content="{html.escape(item['hook'][:180], quote=True)}">
  <link rel="canonical" href="{BASE_URL}/compare/{slug}/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/compare/{slug}/">
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/compare/{slug}/">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{html.escape(a['name'])} vs {html.escape(b['name'])} — 2026 teardown">
  <meta property="og:description" content="{html.escape(item['hook'][:180], quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{BASE_URL}/compare/{slug}/">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{html.escape(a['name'])} vs {html.escape(b['name'])}: cost, limits and the decision matrix">
  <meta name="twitter:description" content="{html.escape(first_sentence(item['verdict_summary'])[:180], quote=True)}">
  <script type="application/ld+json">
  {_json_ld(schema_article, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {_json_ld(schema_faq, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {_json_ld(schema_crumb, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="../../" class="logo">DevTools<span>Radar</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a href="../../deals/" class="nav-link">Deals</a>
        <a href="../../ko/" class="nav-link">한국어 핫딜</a>
        <a href="../../" class="nav-link">← All teardowns</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="meta-row">
      <span class="badge badge-blue">{html.escape(item['category'])}</span>
      <span class="badge badge-gray">{html.escape(a['name'])} vs {html.escape(b['name'])}</span>
      <span>Prices verified {html.escape(updated)}</span>
      <span>·</span>
      <span>{rt}</span>
    </div>

    <h1>{html.escape(a['name'])} vs {html.escape(b['name'])}</h1>
    <div class="lead">{md_to_html(item['hook'])}</div>

    <div class="verdict-box">
      <div class="label">Verdict</div>
      {md_to_html(item['verdict_summary'])}
    </div>

    <div class="toc">
      <div class="toc-title">In this teardown</div>
      <ol>{toc_items}</ol>
    </div>

    <h2>At a glance</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Dimension</th>
            <th>{html.escape(a['name'])} <span class="badge badge-blue">{html.escape(a.get('badge',''))}</span></th>
            <th>{html.escape(b['name'])} <span class="badge badge-green">{html.escape(b.get('badge',''))}</span></th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Core engine</strong></td><td>{html.escape(a['db'])}</td><td>{html.escape(b['db'])}</td></tr>
          <tr><td><strong>Pricing model</strong></td><td>{html.escape(a['pricing'])}</td><td>{html.escape(b['pricing'])}</td></tr>
          <tr><td><strong>Self-hostable</strong></td><td><strong>{html.escape(a['self_host'])}</strong></td><td>{html.escape(b['self_host'])}</td></tr>
          <tr><td><strong>Realtime and concurrency</strong></td><td>{html.escape(a['realtime'])}</td><td>{html.escape(b['realtime'])}</td></tr>
          <tr><td><strong>AI and vector readiness</strong></td><td>{html.escape(a['ai_readiness'])}</td><td>{html.escape(b['ai_readiness'])}</td></tr>
          <tr><td><strong>Lock-in risk</strong></td><td>{html.escape(a['lock_in'])}</td><td>{html.escape(b['lock_in'])}</td></tr>
          <tr>
            <td><strong>Vendor</strong></td>
            <td><a href="{_safe_url(a['cta_url'])}" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="padding:0.4rem 0.8rem; font-size:0.82rem;">{html.escape(a['name'])} →</a></td>
            <td><a href="{_safe_url(b['cta_url'])}" target="_blank" rel="noopener nofollow" class="btn btn-outline" style="padding:0.4rem 0.8rem; font-size:0.82rem;">{html.escape(b['name'])} →</a></td>
          </tr>
        </tbody>
      </table>
    </div>
{sections_html}{cost_html}{matrix_html}

    <h2>Code and configuration</h2>
    <div style="display:grid; grid-template-columns:1fr; gap:1rem;">
      <div>
        <span class="badge badge-blue" style="margin-bottom:0.4rem;">{html.escape(a['name'])}</span>
        <pre><code>{html.escape(a.get('code_example',''))}</code></pre>
      </div>
      <div>
        <span class="badge badge-green" style="margin-bottom:0.4rem;">{html.escape(b['name'])}</span>
        <pre><code>{html.escape(b.get('code_example',''))}</code></pre>
      </div>
    </div>

    <h2>What you gain, what you give up</h2>
    <div class="pros-cons-grid">
      <div class="card" style="padding:1.2rem;">
        <h3 style="color:var(--primary); margin-top:0;">{html.escape(a['name'])}</h3>
        <div class="pros-box" style="margin-bottom:0.9rem;">
          <strong style="color:var(--accent); font-size:0.85rem; text-transform:uppercase; letter-spacing:0.04em;">You gain</strong>
          <ul>{a_pros_html}</ul>
        </div>
        <div class="cons-box">
          <strong style="color:var(--danger); font-size:0.85rem; text-transform:uppercase; letter-spacing:0.04em;">You give up</strong>
          <ul>{a_cons_html}</ul>
        </div>
      </div>
      <div class="card" style="padding:1.2rem;">
        <h3 style="color:var(--accent); margin-top:0;">{html.escape(b['name'])}</h3>
        <div class="pros-box" style="margin-bottom:0.9rem;">
          <strong style="color:var(--accent); font-size:0.85rem; text-transform:uppercase; letter-spacing:0.04em;">You gain</strong>
          <ul>{b_pros_html}</ul>
        </div>
        <div class="cons-box">
          <strong style="color:var(--danger); font-size:0.85rem; text-transform:uppercase; letter-spacing:0.04em;">You give up</strong>
          <ul>{b_cons_html}</ul>
        </div>
      </div>
    </div>
{migration_html}

    <h2 id="faq">Common questions</h2>
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:0.4rem 1.4rem;">
      {faqs_html}
    </div>
{sources_html}{related_html}

    <div style="text-align:center; margin: 3rem 0 1rem;">
      <a href="{_safe_url(a['cta_url'])}" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="margin:0.35rem;">Try {html.escape(a['name'])} →</a>
      <a href="{_safe_url(b['cta_url'])}" target="_blank" rel="noopener nofollow" class="btn btn-outline" style="margin:0.35rem;">Explore {html.escape(b['name'])} →</a>
    </div>

    {DEALS_SECTION_HTML}

    <div class="updated-note">
      Prices and limits verified on {html.escape(updated)}. Prices can change. If a number here looks wrong,
      the vendor's own price sheet wins. Derived figures are arithmetic on published unit prices, not
      measured benchmarks.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 {SITE_NAME}. Developer tool comparisons. Shopping links are marked separately.</p>
    </div>
  </footer>
</body>
</html>"""


def generate_sitemap(items):
    today = datetime.date.today().isoformat()
    urls = f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/"/>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>
  </url>\n  <url>
    <loc>{BASE_URL}/ko/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/deals/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>
  </url>\n  <url>
    <loc>{BASE_URL}/deals/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/deals/"/>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/deals/"/>
  </url>\n"""
    for item in items:
        urls += f"""  <url>
    <loc>{BASE_URL}/compare/{item['slug']}/</loc>
    <lastmod>{item.get('last_verified', today)}</lastmod>
    <priority>0.8</priority>
  </url>\n"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{urls}</urlset>"""


def render_site(items, output, deals, en_deals):
    DIST_DIR = output
    os.makedirs(DIST_DIR, exist_ok=True)

    index_html = generate_index_html(items)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    for item in items:
        page_dir = os.path.join(DIST_DIR, "compare", item["slug"])
        os.makedirs(page_dir, exist_ok=True)
        page = generate_comparison_html(item)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        body = " ".join(s.get("content", "") for s in item.get("sections", []))
        print(f"  {item['slug']:<28} body={len(body):>5} chars  sections={len(item.get('sections', []))}  {reading_time(item)}")

    sitemap = generate_sitemap(items)
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # 한글 핫딜 포털 (/ko/)
    ko_dir = os.path.join(DIST_DIR, "ko")
    os.makedirs(ko_dir, exist_ok=True)
    with open(os.path.join(ko_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_ko_html(deals))
    print(f"  {'ko-portal':<28} feed={len(deals.get('feed', []))} deals  "
          f"picks={len(deals.get('picks', []))}  updated={deals.get('generated_at', '-')}")

    en_dir = os.path.join(DIST_DIR, "deals")
    os.makedirs(en_dir, exist_ok=True)
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_deals_en_html(en_deals))
    print(f"  {'deals-portal-en':<28} feed={len(en_deals.get('feed', []))} deals  "
          f"updated={en_deals.get('generated_at', '-')}")

    robots = (
        "# Search engines\n"
        "User-agent: Googlebot\nAllow: /\n\n"
        "User-agent: Yeti\nAllow: /\n\n"
        "User-agent: Bingbot\nAllow: /\n\n"
        "# AI search / LLM agents\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: Claude-Web\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
        f"# LLM directory: {BASE_URL}/llms.txt\n"
    )
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    with open(os.path.join(DIST_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(generate_llms_txt(items, deals, en_deals))
    with open(os.path.join(DIST_DIR, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write(generate_llms_full_txt(items, deals, en_deals))

    with open(os.path.join(DIST_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("devteardown.com\n")

    if (ROOT / "assets" / "deals").exists():
        shutil.copytree(ROOT / "assets" / "deals", Path(DIST_DIR) / "assets" / "deals", dirs_exist_ok=True)

    print(f"Rendered {len(items) + 3} pages")


MANIFEST = ".generated-files.json"


def build_site(data_path=DATA_PATH, output=DIST_DIR, deals_path=DEALS_DATA_PATH,
               en_deals_path=DEALS_EN_DATA_PATH):
    output = Path(output).absolute()
    inputs = [Path(p).resolve() for p in (data_path, deals_path, en_deals_path)]
    if output.is_symlink() or output == ROOT or output == Path(output.anchor) or ".git" in output.parts:
        raise ValueError("Unsafe output directory")
    resolved = output.resolve()
    if ".git" in resolved.parts or any(p == resolved or resolved in p.parents for p in [ROOT, *inputs]):
        raise ValueError("Output must not contain source files")
    with open(data_path, encoding="utf-8") as f:
        items = json.load(f)
    errors = validate_items(items)
    if errors:
        raise ValueError("Invalid build input:\n" + "\n".join(errors))
    deals, en_deals = load_deals(deals_path), load_deals(en_deals_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".radar-build-", dir=output.parent) as temp:
        stage = Path(temp) / "site"
        stage.mkdir()
        render_site(items, stage, deals, en_deals)
        generated = sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file())
        # Preserve user-managed assets. Remove only manifest-owned (or recognizable legacy) output.
        if output.exists():
            if not output.is_dir() or any(p.is_symlink() for p in output.rglob("*")):
                raise ValueError("Output must be a directory without symlinks")
            manifest = output / MANIFEST
            if manifest.exists():
                previous = json.loads(manifest.read_text(encoding="utf-8"))
                if not isinstance(previous, list) or any(not isinstance(v, str) or Path(v).is_absolute()
                    or ".." in Path(v).parts for v in previous):
                    raise ValueError("Unsafe generated file manifest")
            else:
                previous = []
                for page in (output / "compare").glob("*/index.html"):
                    if "DevTools" in page.read_text(encoding="utf-8") and any(
                        marker in page.read_text(encoding="utf-8")
                        for marker in ("Key metric comparison", "At a glance")
                    ):
                        previous.append(str(page.relative_to(output)))
            owned = set(previous) | set(generated) | {MANIFEST}
            for file in output.rglob("*"):
                relative = file.relative_to(output)
                if file.is_file() and str(relative) not in owned:
                    target = stage / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, target)
        (stage / MANIFEST).write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
        backup = Path(temp) / "previous"
        existed = output.exists()
        if existed:
            output.rename(backup)
        try:
            stage.rename(output)
        except BaseException:
            if existed:
                backup.rename(output)
            raise
    print(f"Build complete: {output}")
    return generated


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and render the static site safely")
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    parser.add_argument("--output", type=Path, default=DIST_DIR)
    parser.add_argument("--deals", type=Path, default=DEALS_DATA_PATH)
    parser.add_argument("--deals-en", type=Path, default=DEALS_EN_DATA_PATH)
    args = parser.parse_args(argv)
    try:
        build_site(args.data, args.output, args.deals, args.deals_en)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")


if __name__ == "__main__":
    main()
