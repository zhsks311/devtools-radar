import os
import re
import json
import html
import datetime

BASE_URL = "https://zhsks311.github.io/devtools-radar"
SITE_NAME = "DevTools Radar"
DIST_DIR = "/workspace/devtools-radar/dist"
DATA_PATH = "/workspace/devtools-radar/data/tools.json"

SHARED_CSS = """
:root {
  --bg: #090d16;
  --surface: #121826;
  --surface-raised: #182234;
  --border: #222f46;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --primary: #38bdf8;
  --primary-glow: rgba(56, 189, 248, 0.15);
  --accent: #10b981;
  --warn: #f59e0b;
  --danger: #f43f5e;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background-color: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.7;
  padding: 0;
  margin: 0;
  -webkit-font-smoothing: antialiased;
}
.container { max-width: 940px; margin: 0 auto; padding: 2rem 1.5rem; }
header {
  border-bottom: 1px solid var(--border);
  padding: 1.1rem 0;
  background: rgba(9, 13, 22, 0.88);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  max-width: 940px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.logo { font-size: 1.2rem; font-weight: 700; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 0.4rem; letter-spacing: -0.02em; }
.logo span { color: var(--primary); }
.nav-link { color: var(--text-muted); text-decoration: none; font-size: 0.88rem; }
.nav-link:hover { color: var(--primary); }
.badge { display: inline-block; padding: 0.18rem 0.6rem; border-radius: 9999px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.02em; }
.badge-blue { background: rgba(56, 189, 248, 0.1); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.3); }
.badge-green { background: rgba(16, 185, 129, 0.1); color: var(--accent); border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-warn { background: rgba(245, 158, 11, 0.1); color: var(--warn); border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-gray { background: #1e293b; color: #94a3b8; border: 1px solid #334155; }
h1 { font-size: 2.15rem; font-weight: 800; line-height: 1.22; margin: 0.75rem 0 1rem; color: #fff; letter-spacing: -0.025em; }
h2 { font-size: 1.45rem; font-weight: 700; color: #fff; margin: 3rem 0 1rem; padding-bottom: 0.55rem; border-bottom: 1px solid var(--border); letter-spacing: -0.01em; }
h3 { font-size: 1.12rem; font-weight: 650; color: #fff; margin: 2rem 0 0.6rem; letter-spacing: -0.01em; }
h4 { font-size: 1rem; font-weight: 650; color: var(--primary); margin: 1.5rem 0 0.4rem; }
p { margin-bottom: 1rem; color: #cbd5e1; font-size: 1rem; }
ul, ol { margin: 0 0 1.1rem 1.35rem; color: #cbd5e1; }
li { margin-bottom: 0.4rem; font-size: 0.98rem; }
li > code, p > code { font-size: 0.86em; }
strong { color: #fff; font-weight: 640; }
a { color: var(--primary); }
blockquote {
  border-left: 3px solid var(--primary);
  background: rgba(56, 189, 248, 0.05);
  padding: 0.9rem 1.2rem;
  margin: 1.3rem 0;
  color: #cbd5e1;
  border-radius: 0 8px 8px 0;
  font-size: 0.97rem;
}
blockquote p:last-child { margin-bottom: 0; }
.lead { font-size: 1.12rem; color: #b6c2d2; margin-bottom: 1.6rem; line-height: 1.72; }
.meta-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; color: var(--text-muted); font-size: 0.82rem; }
.table-wrapper { overflow-x: auto; margin: 1.4rem 0 1.8rem; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem; }
th, td { padding: 0.8rem 1rem; border-bottom: 1px solid var(--border); vertical-align: top; }
th { background: #162032; color: #fff; font-weight: 600; font-size: 0.86rem; text-transform: uppercase; letter-spacing: 0.03em; }
tr:last-child td { border-bottom: none; }
td code { color: var(--primary); }
.btn {
  display: inline-block;
  padding: 0.72rem 1.4rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.94rem;
  text-decoration: none;
  transition: all 0.18s;
  text-align: center;
}
.btn-primary { background: var(--primary); color: #04121b; }
.btn-primary:hover { opacity: 0.92; transform: translateY(-1px); }
.btn-outline { border: 1px solid var(--border); color: var(--text); background: var(--surface); }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.2rem;
  transition: border-color 0.18s, transform 0.18s;
}
a.card { display: block; text-decoration: none; }
a.card:hover { border-color: var(--primary); transform: translateY(-2px); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 1.2rem; margin: 1.8rem 0; }
.verdict-box {
  background: linear-gradient(145deg, #132238 0%, #0d1829 100%);
  border: 1px solid #1e3a5f;
  border-left: 3px solid var(--primary);
  border-radius: 12px;
  padding: 1.4rem 1.5rem;
  margin: 1.5rem 0 2rem;
}
.verdict-box .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--primary); font-weight: 700; }
.verdict-box p { color: #dbe4ef; margin: 0.5rem 0 0; font-size: 1.01rem; }
.pros-cons-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin: 1.4rem 0; }
@media (max-width: 680px) { .pros-cons-grid { grid-template-columns: 1fr; } }
.pros-box { background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 1.1rem; }
.cons-box { background: rgba(244, 63, 94, 0.05); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 10px; padding: 1.1rem; }
.pros-box ul, .cons-box ul { padding-left: 1.1rem; margin: 0.5rem 0 0; }
.pros-box li, .cons-box li { font-size: 0.89rem; margin-bottom: 0.4rem; color: #cbd5e1; }
pre {
  background: #0b1120;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.15rem;
  overflow-x: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.82rem;
  line-height: 1.55;
  color: #9dd7f5;
  margin: 1rem 0 1.2rem;
  tab-size: 2;
}
pre code { color: inherit; background: none; padding: 0; }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  background: rgba(56, 189, 248, 0.09);
  color: #9dd7f5;
  padding: 0.12rem 0.35rem;
  border-radius: 4px;
  font-size: 0.87em;
}
.migration-box {
  background: #121e33;
  border-left: 3px solid var(--primary);
  border-radius: 0 8px 8px 0;
  padding: 1.2rem 1.4rem;
  margin: 1.4rem 0;
}
.migration-box strong { color: #fff; }
.faq-item { border-bottom: 1px solid var(--border); padding: 1.1rem 0; }
.faq-item:last-child { border-bottom: none; }
.faq-q { font-size: 1.02rem; font-weight: 600; color: #fff; margin-bottom: 0.4rem; }
.faq-a { color: var(--text-muted); font-size: 0.94rem; }
.cost-row { display: grid; grid-template-columns: 1fr; gap: 0.35rem; padding: 0.9rem 0; border-bottom: 1px solid var(--border); }
.cost-row:last-child { border-bottom: none; }
.cost-label { font-weight: 600; color: #fff; font-size: 0.95rem; }
.cost-formula { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.83rem; color: var(--text-muted); word-break: break-word; }
.cost-result { color: var(--accent); font-weight: 650; font-size: 0.98rem; }
.matrix-pick { color: var(--primary); font-weight: 600; }
.sources-list { font-size: 0.86rem; color: var(--text-muted); line-height: 1.9; word-break: break-all; }
.updated-note {
  font-size: 0.8rem; color: var(--text-muted);
  border-top: 1px solid var(--border); margin-top: 2.5rem; padding-top: 1rem;
}
.toc { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.1rem 1.3rem; margin: 1.8rem 0; }
.toc-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); font-weight: 700; margin-bottom: 0.6rem; }
.toc ol { margin: 0 0 0 1.1rem; }
.toc li { font-size: 0.9rem; margin-bottom: 0.25rem; }
.toc a { color: #cbd5e1; text-decoration: none; }
.toc a:hover { color: var(--primary); }
footer { border-top: 1px solid var(--border); padding: 2.2rem 0; margin-top: 4rem; text-align: center; color: var(--text-muted); font-size: 0.84rem; }
"""

# ---------------------------------------------------------------- markdown


def _esc(text):
    return html.escape(text, quote=False)


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
            cls = ' class="language-%s"' % lang if lang else ""
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


# ---------------------------------------------------------------- pages


def generate_index_html(items):
    cards_html = ""
    for item in items:
        a = item["tool_a"]
        b = item["tool_b"]
        cards_html += f"""
        <a class="card" href="./compare/{item['slug']}/">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.7rem;">
            <span class="badge badge-blue">{item['category']}</span>
            <span style="font-size:0.78rem; color:var(--text-muted);">{reading_time(item)}</span>
          </div>
          <h2 style="font-size:1.22rem; color:#fff; margin:0 0 0.5rem; border-bottom:none; padding-bottom:0;">{a['name']} vs {b['name']}</h2>
          <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1rem; line-height:1.6;">{_plain(item.get('hook', item['verdict_summary']))[:175]}…</p>
          <span style="color:var(--primary); font-size:0.86rem; font-weight:600;">Read the teardown →</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME} — Developer Tool Teardowns, Priced in Arithmetic (2026)</title>
  <meta name="description" content="Independent teardowns of competing developer tools: what each vendor's billing unit punishes, worked cost arithmetic from published price sheets, and a decision matrix you can paste into a design doc.">
  <link rel="canonical" href="{BASE_URL}/">
  <meta property="og:title" content="{SITE_NAME} — Developer Tool Teardowns">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/">
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="./" class="logo">⚡ DevTools<span>Radar</span></a>
      <span class="badge badge-green">Verified Nov 2026</span>
    </div>
  </header>

  <main class="container">
    <div style="max-width: 760px; margin: 1.5rem 0 2.5rem;">
      <span class="badge badge-blue">No sponsored placement</span>
      <h1>Every comparison is a billing question in disguise.</h1>
      <p class="lead">We take each vendor's published price sheet and read it as a penalty table: which
      usage does this meter punish, what does that make impossible, and what does it cost at the volume
      you will actually reach. No hand-waved benchmarks — the arithmetic is shown, with formulas.</p>
    </div>

    <div class="grid">
      {cards_html}
    </div>

    <div class="updated-note">
      <strong>How to read this site.</strong> Every number here is either taken from a vendor's own price
      sheet or documentation, or derived from it with the formula printed next to it. Vendor performance
      claims are labelled as vendor claims. Each article carries the date its prices were verified,
      because this market reprices itself twice a year.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 {SITE_NAME}. Independent developer analysis. Nothing here is paid placement.</p>
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
        "author": {"@type": "Organization", "name": SITE_NAME},
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

    a_pros_html = "".join(f"<li>{p}</li>" for p in a.get("pros", []))
    a_cons_html = "".join(f"<li>{c}</li>" for c in a.get("cons", []))
    b_pros_html = "".join(f"<li>{p}</li>" for p in b.get("pros", []))
    b_cons_html = "".join(f"<li>{c}</li>" for c in b.get("cons", []))

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
            f'<a href="{html.escape(u)}" rel="noopener nofollow" target="_blank">{html.escape(u)}</a><br>'
            for u in item["sources"]
        )
        sources_html = f"""
      <h2>Sources &amp; verification</h2>
      <p class="sources-list">Prices and limits were read from these pages on <strong>{updated}</strong>.
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
            <h3 style="margin:0 0 0.3rem; font-size:1rem; color:#fff;">{r['name']}</h3>
            <p style="margin:0; font-size:0.85rem; color:var(--text-muted);">{r['why']}</p>
          </a>"""
        related_html = f"""
      <h2>Keep reading</h2>
      <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr));">{rel_cards}</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{a['name']} vs {b['name']} (2026): Cost, Limits and the Decision Matrix</title>
  <meta name="description" content="{html.escape(item['hook'][:180], quote=True)}">
  <link rel="canonical" href="{BASE_URL}/compare/{slug}/">
  <meta property="og:title" content="{a['name']} vs {b['name']} — 2026 teardown">
  <meta property="og:description" content="{html.escape(item['hook'][:180], quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{BASE_URL}/compare/{slug}/">
  <script type="application/ld+json">
  {json.dumps(schema_article, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(schema_faq, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(schema_crumb, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="../../" class="logo">⚡ DevTools<span>Radar</span></a>
      <a href="../../" class="nav-link">← All teardowns</a>
    </div>
  </header>

  <main class="container">
    <div class="meta-row">
      <span class="badge badge-blue">{item['category']}</span>
      <span class="badge badge-gray">{a['name']} vs {b['name']}</span>
      <span>Prices verified {updated}</span>
      <span>·</span>
      <span>{rt}</span>
    </div>

    <h1>{a['name']} vs {b['name']}</h1>
    <p class="lead">{md_to_html(item['hook'])}</p>

    <div class="verdict-box">
      <div class="label">Verdict</div>
      <p>{md_to_html(item['verdict_summary'])}</p>
    </div>

    <div class="toc">
      <div class="toc-title">In this teardown</div>
      <ol>{toc_items}</ol>
    </div>

    <h2>Key metric comparison</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Dimension</th>
            <th>{a['name']} <span class="badge badge-blue">{a.get('badge','')}</span></th>
            <th>{b['name']} <span class="badge badge-green">{b.get('badge','')}</span></th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Core engine</strong></td><td>{a['db']}</td><td>{b['db']}</td></tr>
          <tr><td><strong>Pricing model</strong></td><td>{a['pricing']}</td><td>{b['pricing']}</td></tr>
          <tr><td><strong>Self-hostable</strong></td><td><strong>{a['self_host']}</strong></td><td>{b['self_host']}</td></tr>
          <tr><td><strong>Realtime and concurrency</strong></td><td>{a['realtime']}</td><td>{b['realtime']}</td></tr>
          <tr><td><strong>AI and vector readiness</strong></td><td>{a['ai_readiness']}</td><td>{b['ai_readiness']}</td></tr>
          <tr><td><strong>Lock-in risk</strong></td><td>{a['lock_in']}</td><td>{b['lock_in']}</td></tr>
          <tr>
            <td><strong>Vendor</strong></td>
            <td><a href="{a['cta_url']}" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="padding:0.4rem 0.8rem; font-size:0.82rem;">{a['name']} →</a></td>
            <td><a href="{b['cta_url']}" target="_blank" rel="noopener nofollow" class="btn btn-outline" style="padding:0.4rem 0.8rem; font-size:0.82rem;">{b['name']} →</a></td>
          </tr>
        </tbody>
      </table>
    </div>
{sections_html}{cost_html}{matrix_html}

    <h2>Same task, two SDKs</h2>
    <div style="display:grid; grid-template-columns:1fr; gap:1rem;">
      <div>
        <span class="badge badge-blue" style="margin-bottom:0.4rem;">{a['name']}</span>
        <pre><code>{html.escape(a.get('code_example',''))}</code></pre>
      </div>
      <div>
        <span class="badge badge-green" style="margin-bottom:0.4rem;">{b['name']}</span>
        <pre><code>{html.escape(b.get('code_example',''))}</code></pre>
      </div>
    </div>

    <h2>What you gain, what you give up</h2>
    <div class="pros-cons-grid">
      <div class="card" style="padding:1.2rem;">
        <h3 style="color:var(--primary); margin-top:0;">{a['name']}</h3>
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
        <h3 style="color:var(--accent); margin-top:0;">{b['name']}</h3>
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

    <h2 id="faq">Questions that change the decision</h2>
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:0.4rem 1.4rem;">
      {faqs_html}
    </div>
{sources_html}{related_html}

    <div style="text-align:center; margin: 3rem 0 1rem;">
      <a href="{a['cta_url']}" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="margin:0.35rem;">Try {a['name']} →</a>
      <a href="{b['cta_url']}" target="_blank" rel="noopener nofollow" class="btn btn-outline" style="margin:0.35rem;">Explore {b['name']} →</a>
    </div>

    <div class="updated-note">
      Prices and limits verified on {updated}. This market reprices often — if a number below looks wrong,
      the vendor's own price sheet wins. Derived figures are arithmetic on published unit prices, not
      measured benchmarks.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 {SITE_NAME}. Independent developer analysis. No paid placement, no affiliate ranking.</p>
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
  </url>\n"""
    for item in items:
        urls += f"""  <url>
    <loc>{BASE_URL}/compare/{item['slug']}/</loc>
    <lastmod>{item.get('last_verified', today)}</lastmod>
    <priority>0.8</priority>
  </url>\n"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

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

    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

    print(f"Build complete: {len(items) + 1} pages in {DIST_DIR}")


if __name__ == "__main__":
    main()
