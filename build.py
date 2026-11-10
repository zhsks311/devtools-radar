import os
import re
import json
import html
import datetime

BASE_URL = "https://devteardown.com"
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

DEALS_SECTION_HTML = """
    <div style="margin: 3.5rem 0 1.5rem; padding: 1.6rem 1.8rem; background: var(--surface); border: 1px solid var(--border); border-radius: 12px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.8rem; flex-wrap:wrap; gap:0.5rem;">
        <h3 style="margin:0; font-size:1.15rem; color:#fff;">⚡ Verified Tech Deals &amp; Workstation Gear</h3>
        <span class="badge badge-blue">Curated for Builders</span>
      </div>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1.2rem;">
        High-impact developer hardware &amp; workstation picks tested for productivity, with live rocket delivery links.
      </p>
      <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem;">
        <div class="card" style="padding:1.1rem; background:var(--surface-raised);">
          <div style="font-size:0.75rem; color:var(--primary); font-weight:600; text-transform:uppercase; margin-bottom:0.3rem;">Mouse &amp; Desk Setup</div>
          <strong style="display:block; color:#fff; font-size:1rem; margin-bottom:0.4rem;">Logitech MX Master 3S</strong>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.8rem;">Ergonomic silent switches with dual-scroll MagSpeed wheels.</p>
          <a href="https://link.coupang.com/a/iyxFRjouBM" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.8rem;">쿠팡 최저가 보기 →</a>
        </div>
        <div class="card" style="padding:1.1rem; background:var(--surface-raised);">
          <div style="font-size:0.75rem; color:var(--primary); font-weight:600; text-transform:uppercase; margin-bottom:0.3rem;">Workstation / Laptop</div>
          <strong style="display:block; color:#fff; font-size:1rem; margin-bottom:0.4rem;">Apple M4 MacBook Pro</strong>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.8rem;">Unified memory bandwidth for local LLM inference and instant builds.</p>
          <a href="https://link.coupang.com/a/iyxHrMNtyC" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.8rem;">쿠팡 최저가 보기 →</a>
        </div>
        <div class="card" style="padding:1.1rem; background:var(--surface-raised);">
          <div style="font-size:0.75rem; color:var(--primary); font-weight:600; text-transform:uppercase; margin-bottom:0.3rem;">Daily Limited Deals</div>
          <strong style="display:block; color:#fff; font-size:1rem; margin-bottom:0.4rem;">Coupang Goldbox (7AM)</strong>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.8rem;">Daily limited morning flash discounts up to 50% on tech &amp; essentials.</p>
          <a href="https://link.coupang.com/a/iyxEbxQMEK" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.8rem;">골드박스 특가 보기 →</a>
        </div>
      </div>
      <div style="font-size:0.75rem; color:#64748b; margin-top:1rem; padding-top:0.6rem; border-top:1px solid var(--border); text-align:right;">
        * 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
      </div>
    </div>
"""


# ---------------------------------------------------------------- deal portals

DEALS_DATA_PATH = "/workspace/devtools-radar/data/deals.json"
DEALS_EN_DATA_PATH = "/workspace/devtools-radar/data/deals_en.json"
KO_SITE_NAME = "DevTeardown KR"
KO_TAGLINE = "개발자 장비 & 테크 핫딜 레이더"
KO_DISCLOSURE = (
    "이 포스팅은 쿠팡 파트너스 활동의 일환으로, "
    "이에 따른 일정액의 수수료를 제공받습니다."
)

DEAL_CSS = """
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");

body { font-family: "Pretendard Variable", Pretendard, "Apple SD Gothic Neo", -apple-system,
  BlinkMacSystemFont, "Segoe UI", "Malgun Gothic", Roboto, sans-serif; }

.ko-hero { padding: 3.4rem 0 1.2rem; }
.ko-hero h1 { font-size: clamp(2rem, 4.6vw, 2.9rem); line-height: 1.25; margin: 0.7rem 0 1rem; }
.ko-hero .lead { font-size: 1.05rem; line-height: 1.85; color: #b8c5d6; max-width: 720px; }
.ko-stats { display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 1.5rem 0 0.2rem; }
.ko-stat {
  background: #111a2b; border: 1px solid var(--border); border-radius: 10px;
  padding: 0.55rem 0.85rem; font-size: 0.76rem; color: #8fa1b8;
}
.ko-stat strong { color: #eaf2ff; font-size: 0.95rem; margin-right: 0.35rem; }
.disclosure-bar {
  background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3);
  color: #f1c98d; font-size: 0.78rem; line-height: 1.65; padding: 0.7rem 0.95rem;
  border-radius: 10px; margin: 1.3rem 0 0;
}

/* ---------- quick filter tabs ---------- */
.quick-tabs {
  position: sticky; top: 57px; z-index: 20; display: flex; gap: 0.45rem;
  overflow-x: auto; scrollbar-width: none; padding: 0.75rem 0;
  margin: 0.6rem 0 1.2rem; background: rgba(9, 13, 22, 0.94);
  backdrop-filter: blur(10px); border-bottom: 1px solid var(--border);
}
.quick-tabs::-webkit-scrollbar { display: none; }
.tab {
  flex: none; border: 1px solid var(--border); background: #101828; color: #a9b8cb;
  font-size: 0.85rem; font-weight: 600; padding: 0.5rem 0.95rem; border-radius: 999px;
  cursor: pointer; transition: all 0.16s; font-family: inherit; white-space: nowrap;
}
.tab:hover { color: #e6f1ff; border-color: #33506f; }
.tab.is-active { background: var(--primary); border-color: var(--primary); color: #04121b; }
.tab .n { opacity: 0.65; font-size: 0.76rem; margin-left: 0.2rem; }

/* ---------- deal cards ---------- */
.deal-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.2rem; margin: 0.4rem 0 0.5rem; }
.deal-card {
  display: flex; flex-direction: column; position: relative;
  background: linear-gradient(168deg, #131d2e 0%, #101725 100%);
  border: 1px solid #24344c; border-radius: 16px; padding: 1.35rem 1.4rem 1.2rem;
  transition: border-color 0.18s, transform 0.18s, box-shadow 0.18s;
}
.deal-card:hover { border-color: #3b82f6; transform: translateY(-3px); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35); }
.deal-card.is-hidden { display: none; }
.deal-top { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; }
.cat-chip {
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.01em;
  color: #9ad8ff; background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.32); border-radius: 999px; padding: 0.22rem 0.65rem;
}
.deal-src { font-size: 0.74rem; color: #7c8ca3; }
.deal-title {
  font-size: 1.06rem; line-height: 1.52; color: #f4f8ff; font-weight: 700;
  margin: 0 0 0.85rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.deal-price { display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 0.55rem; }
.deal-price strong {
  font-size: clamp(1.6rem, 4.4vw, 1.85rem); font-weight: 800; color: #7dd3fc;
  letter-spacing: -0.03em; line-height: 1.15;
}
.deal-price s { color: #64748b; font-size: 0.88rem; }
.deal-price .unknown { font-size: 1rem; color: #94a3b8; font-weight: 600; }
.deal-flags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.9rem; }
.flag {
  font-size: 0.74rem; font-weight: 800; padding: 0.24rem 0.6rem; border-radius: 7px; letter-spacing: 0.01em;
}
.flag-discount { background: #f43f5e; color: #fff; }
.flag-free { background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.45); }
.flag-ship { background: #1e293b; color: #cbd5e1; border: 1px solid #334155; }
.flag-rocket { background: rgba(56, 189, 248, 0.16); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.4); }

.deal-facts { margin: 0 0 1.05rem; display: flex; flex-direction: column; gap: 0.45rem; }
.deal-facts .fact { display: grid; grid-template-columns: 5.6rem 1fr; gap: 0.5rem; align-items: start; }
.deal-facts dt { font-size: 0.75rem; font-weight: 700; color: #8ea3bd; letter-spacing: 0.01em; padding-top: 0.08rem; }
.deal-facts dd { margin: 0; font-size: 0.86rem; line-height: 1.6; color: #c3d0e0; }
.deal-check { margin: -0.5rem 0 0.9rem; font-size: 0.74rem; color: #7288a3; line-height: 1.55; }

.cta {
  display: block; width: 100%; text-align: center; text-decoration: none;
  background: linear-gradient(92deg, #38bdf8 0%, #22d3ee 100%);
  color: #04121b; font-weight: 800; font-size: 0.95rem; letter-spacing: -0.01em;
  padding: 0.82rem 1rem; border-radius: 11px; margin-top: auto;
  box-shadow: 0 6px 18px rgba(56, 189, 248, 0.22); transition: transform 0.15s, box-shadow 0.15s;
}
.cta:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(56, 189, 248, 0.32); }
.cta.secondary { background: #1c2a40; color: #cfe4ff; box-shadow: none; border: 1px solid #2f4664; }
.deal-foot { display: flex; justify-content: space-between; align-items: center; gap: 0.6rem; margin-top: 0.55rem; }
.deal-foot a { font-size: 0.74rem; color: #6f8098; text-decoration: none; }
.deal-foot a:hover { color: var(--primary); }
.deal-foot .note { font-size: 0.7rem; color: #5f6f86; }

.cat-head { display: flex; align-items: baseline; gap: 0.7rem; flex-wrap: wrap; margin-top: 3.2rem; }
.cat-head h2 { margin: 0; border-bottom: none; padding-bottom: 0; font-size: 1.35rem; }
.cat-sub { color: #8798ae; font-size: 0.84rem; }
.cat-list { list-style: none; margin: 0.9rem 0 0; padding: 0; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; background: #0e1624; }
.cat-list li { display: flex; align-items: center; gap: 0.9rem; padding: 0.85rem 1.1rem; border-bottom: 1px solid #1b2637; margin: 0; }
.cat-list li:last-child { border-bottom: none; }
.cat-list a { color: #dbe7f5; text-decoration: none; font-size: 0.93rem; flex: 1; line-height: 1.45; }
.cat-list a:hover { color: var(--primary); }
.cat-list .p { color: #7dd3fc; font-weight: 800; font-size: 0.95rem; white-space: nowrap; }
.cat-list .s { color: #7c8ca3; font-size: 0.74rem; white-space: nowrap; }

.pick-card {
  display: block; text-decoration: none; background: linear-gradient(160deg, #142033 0%, #0f1725 100%);
  border: 1px solid #24344c; border-radius: 14px; padding: 1.2rem 1.3rem;
  transition: border-color 0.18s, transform 0.18s;
}
.pick-card:hover { border-color: var(--primary); transform: translateY(-2px); }
.pick-kicker { font-size: 0.7rem; color: #7dd3fc; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; }
.pick-card strong { display: block; color: #fff; margin: 0.4rem 0 0.35rem; font-size: 1.02rem; }
.pick-card p { font-size: 0.85rem; color: #9fb0c6; margin: 0 0 0.7rem; line-height: 1.65; }
.pick-card span.go { font-size: 0.83rem; color: var(--primary); font-weight: 700; }

.goldbox {
  margin: 2.4rem 0 0; padding: 1.4rem 1.6rem;
  background: linear-gradient(120deg, rgba(56,189,248,0.12), rgba(16,185,129,0.08));
  border: 1px solid #24425f; border-radius: 16px;
  display: flex; justify-content: space-between; align-items: center; gap: 1.2rem; flex-wrap: wrap;
}
.goldbox h3 { margin: 0 0 0.35rem; font-size: 1.08rem; }
.goldbox p { margin: 0; font-size: 0.86rem; color: #9fb0c6; }
.method-note { font-size: 0.8rem; color: #8ea3bd; line-height: 1.85; margin-top: 2.8rem; padding-top: 1.2rem; border-top: 1px solid var(--border); }

@media (max-width: 640px) {
  .container { padding: 1.2rem 1rem; }
  .ko-hero { padding-top: 2rem; }
  .deal-grid { grid-template-columns: 1fr; gap: 1rem; }
  .deal-card { padding: 1.15rem 1.05rem 1rem; border-radius: 14px; }
  .deal-facts .fact { grid-template-columns: 4.9rem 1fr; }
  .quick-tabs { top: 53px; }
}
"""

CAT_SHORT = {
    "laptops": "노트북·PC",
    "monitor-desk": "모니터·데스크",
    "keyboard-mouse": "키보드·마우스",
    "afterwork": "커피·간식",
    "tech": "테크 장비",
}

FACT_ICONS = [
    ("실구매가", "💰 실구매가"),
    ("추천", "🎯 추천"),
    ("스펙", "⚙️ 스펙"),
    ("체크", "⚡ 체크"),
    ("Price", "💰 Price"),
    ("Good for", "🎯 Good for"),
    ("Specs", "⚙️ Specs"),
    ("Shipping", "🚚 Shipping"),
    ("Check", "⚡ Check"),
    ("Key", "🔑 Key"),
]


def load_deals(path: str = DEALS_DATA_PATH) -> dict:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data.get("feed") is not None:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "generated_at": "",
        "feed": [],
        "categories": {},
        "picks": [
            {"category": "keyboard-mouse", "kicker": "Mouse & Desk Setup",
             "title": "로지텍 MX Master 3S",
             "desc": "무소음 스위치와 MagSpeed 휠. 하루 8시간 손목 부담을 줄이는 개발자 기본 장비.",
             "url": "https://link.coupang.com/a/iyxFRjouBM", "tracked": True},
            {"category": "laptops", "kicker": "Workstation / Laptop",
             "title": "Apple M4 MacBook Pro",
             "desc": "통합 메모리 대역폭으로 로컬 LLM 추론과 빌드를 한 대에서. 14/16인치.",
             "url": "https://link.coupang.com/a/iyxHrMNtyC", "tracked": True},
        ],
        "goldbox": {"url": "https://link.coupang.com/a/iyxEbxQMEK",
                    "label": "쿠팡 골드박스 — 매일 오전 7시 특가"},
        "disclosure": KO_DISCLOSURE,
    }


def _won(deal: dict) -> str:
    price = deal.get("price")
    if not price:
        return ""
    cur = deal.get("currency", "KRW")
    if cur == "KRW":
        return f"{int(price):,}원"
    return f"${price:,.2f}" if price % 1 else f"${int(price):,}"


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
        facts += f'<p class="deal-check">⚡ {html.escape(check)}</p>'
    return facts


def _deal_card(deal: dict, lang: str = "ko") -> str:
    link = deal.get("link") or {}
    url = html.escape(link.get("url", ""))
    tracked = bool(link.get("tracked"))
    is_global = deal.get("region") == "global"
    if is_global:
        cta, rel = "View deal →", "noopener nofollow"
    elif tracked:
        cta, rel = "쿠팡에서 보기 →", "noopener nofollow sponsored"
    else:
        cta, rel = "쿠팡에서 검색 →", "noopener nofollow"

    price = _won(deal)
    price_html = f"<strong>{price}</strong>" if price else (
        '<span class="unknown">원문 가격 확인</span>' if lang == "ko" else '<span class="unknown">See price at source</span>')
    if deal.get("original_price"):
        orig = deal["original_price"]
        orig_txt = f"{int(orig):,}원" if deal.get("currency", "KRW") == "KRW" else f"${orig:,.2f}"
        price_html += f"<s>{orig_txt}</s>"

    flags = ""
    if deal.get("discount_pct"):
        flags += f'<span class="flag flag-discount">-{deal["discount_pct"]}%</span>'
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
    src_url = html.escape((deal.get("source") or {}).get("url", ""))
    if src_url and src_url != url:
        label = "원문 보기" if lang == "ko" else "Source post"
        foot = f'<div class="deal-foot"><a href="{src_url}" target="_blank" rel="noopener nofollow">{label}</a>{note}</div>'

    cat_label = deal.get("category_label", "")
    cat = html.escape(CAT_SHORT.get(deal.get("category", ""), cat_label) if lang == "ko" else cat_label)
    return f"""
      <article class="deal-card" data-cat="{html.escape(deal.get('category', 'tech'))}">
        <div class="deal-top">
          <span class="cat-chip">{cat}</span>
          <span class="deal-src">{html.escape(deal.get('store') or (deal.get('source') or {}).get('label', ''))}</span>
        </div>
        <h3 class="deal-title">{html.escape(deal.get('product', ''))}</h3>
        <div class="deal-price">{price_html}</div>
        <div class="deal-flags">{flags}</div>
        {_fact_rows(deal)}
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

    feed_cards = "".join(_deal_card(d) for d in feed[:12])
    if not feed_cards:
        feed_cards = ('<p style="color:#94a3b8;font-size:0.92rem;padding:1rem 0;">'
                      '지금 수집된 신규 테크 핫딜이 없습니다. 아래 큐레이션과 골드박스를 확인하세요.</p>')

    tabs = _tabs(
        categories,
        [("monitor-desk", "모니터·데스크"), ("keyboard-mouse", "키보드·마우스"),
         ("laptops", "노트북·PC"), ("afterwork", "커피·간식")],
        len(feed[:12]),
    )

    cat_html = ""
    for slug in ("laptops", "monitor-desk", "keyboard-mouse", "afterwork"):
        cat = categories.get(slug) or {}
        rows = ""
        for d in cat.get("items", [])[:4]:
            link = d.get("link") or {}
            price = _won(d) or "가격 확인"
            rows += (f'<li><a href="{html.escape(link.get("url", "#"))}" target="_blank" '
                     f'rel="noopener nofollow sponsored">{html.escape(d.get("product", ""))}</a>'
                     f'<span class="p">{price}</span>'
                     f'<span class="s">{html.escape(d.get("store") or "")}</span></li>')
        body = f'<ul class="cat-list">{rows}</ul>' if rows else (
            '<p style="color:#8798ae;font-size:0.88rem;">이 카테고리에 새로 올라온 핫딜이 없습니다. 아래 큐레이션을 참고하세요.</p>')
        cat_html += f"""
    <div class="cat-head" id="{slug}">
      <h2>{html.escape(cat.get('label', slug))}</h2>
      <span class="cat-sub">{html.escape(cat.get('audience', ''))}</span>
    </div>
    {body}"""

    pick_cards = ""
    for p in picks:
        pick_cards += f"""
      <a class="pick-card" href="{html.escape(p['url'])}" target="_blank" rel="noopener nofollow sponsored">
        <div class="pick-kicker">{html.escape(p.get('kicker', ''))}</div>
        <strong>{html.escape(p.get('title', ''))}</strong>
        <p>{html.escape(p.get('desc', ''))}</p>
        <span class="go">쿠팡 최저가 확인 →</span>
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
  <link rel="alternate" hreflang="en" href="{BASE_URL}/deals/">
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <meta property="og:title" content="{KO_SITE_NAME} — {KO_TAGLINE}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/ko/">
  <meta property="og:locale" content="ko_KR">
  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}{DEAL_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="/ko/" class="logo">⚡ DevTeardown<span>KR</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="#feed">실시간 핫딜</a>
        <a class="nav-link" href="/deals/">Global Deals</a>
        <a class="nav-link" href="/">EN Reports</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="ko-hero">
      <span class="badge badge-blue">매일 갱신 · 원문 가격 기준</span>
      <h1>개발자 장비, 살 때만 사세요.</h1>
      <p class="lead">뽐뿌·클리앙·퀘이사존·에펨코리아·폴센트에 올라온 테크 핫딜을 한곳에 모아,
      원문에 적힌 가격과 배송 조건만으로 실구매가를 다시 계산합니다. 과장된 "역대급" 대신
      지금 사도 되는지 판단할 수 있는 숫자만 남겼습니다.</p>
      <div class="ko-stats">
        <div class="ko-stat"><strong>{len(feed)}건</strong>실시간 핫딜</div>
        <div class="ko-stat"><strong>4개</strong>장비 카테고리</div>
        <div class="ko-stat"><strong>{updated}</strong>업데이트</div>
        <div class="ko-stat"><strong>0원</strong>가입 비용</div>
      </div>
      <div class="disclosure-bar">
        {html.escape(deals.get('disclosure', KO_DISCLOSURE))}
      </div>
    </div>

    <h2 id="feed" style="margin-top:2.4rem;">실시간 테크 · 개발자 핫딜</h2>
    <p style="color:#8ea3bd; font-size:0.9rem; margin-top:-0.3rem;">
      가격·할인율·배송은 수집 시점의 원문 표기입니다. 품절·가격 변동은 원문에서 확인하세요.
    </p>
    {tabs}
    <div class="deal-grid" id="feedGrid">{feed_cards}</div>

    <div class="goldbox">
      <div>
        <h3>⏰ 오늘의 골드박스</h3>
        <p>매일 오전 7시, 한정 수량 특가. 개발 장비부터 사무 간식까지.</p>
      </div>
      <a class="cta" style="width:auto; padding:0.75rem 1.2rem;" href="{html.escape(goldbox['url'])}" target="_blank" rel="noopener nofollow sponsored">{html.escape(goldbox.get('label', '골드박스 보기'))} →</a>
    </div>

    {cat_html}

    <h2 style="margin-top:3.4rem;">지금 사도 되는 장비 큐레이션</h2>
    <p style="color:#8ea3bd; font-size:0.9rem; margin-top:-0.3rem;">
      핫딜이 뜰 때까지 기다리지 않아도 되는, 개발자 책상 기본 장비.</p>
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(280px,1fr));">{pick_cards}</div>

    <div class="method-note">
      <strong style="color:#fff;">이 페이지가 가격을 다루는 방식</strong><br>
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

    feed_cards = "".join(_deal_card(d, lang="en") for d in feed[:12])
    if not feed_cards:
        feed_cards = ('<p style="color:#94a3b8;font-size:0.92rem;padding:1rem 0;">'
                      'No new tech deals collected right now. Check back after the next run.</p>')

    tabs = _tabs(
        categories,
        [("laptops", "Laptops"), ("monitor-desk", "Monitors"),
         ("keyboard-mouse", "Keyboards"), ("afterwork", "Office fuel")],
        len(feed[:12]), lang="en",
    )

    cat_html = ""
    for slug in ("laptops", "monitor-desk", "keyboard-mouse", "afterwork"):
        cat = categories.get(slug) or {}
        rows = ""
        for d in cat.get("items", [])[:4]:
            link = d.get("link") or {}
            price = _won(d) or "see source"
            rows += (f'<li><a href="{html.escape(link.get("url", "#"))}" target="_blank" '
                     f'rel="noopener nofollow">{html.escape(d.get("product", ""))}</a>'
                     f'<span class="p">{price}</span>'
                     f'<span class="s">{html.escape(d.get("store") or "")}</span></li>')
        body = f'<ul class="cat-list">{rows}</ul>' if rows else (
            '<p style="color:#8798ae;font-size:0.88rem;">No new deals in this category yet.</p>')
        cat_html += f"""
    <div class="cat-head" id="{slug}">
      <h2>{html.escape(cat.get('label', slug))}</h2>
      <span class="cat-sub">{html.escape(cat.get('audience', ''))}</span>
    </div>
    {body}"""

    schema = {
        "@context": "https://schema.org", "@type": "WebSite", "name": "DevTeardown Deals",
        "url": f"{BASE_URL}/deals/", "inLanguage": "en",
        "description": "Tech deals for developers: hardware from Reddit, Slickdeals and Dealabs, priced in the currency of the source.",
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevTeardown Deals — Developer Hardware Deals (2026)</title>
  <meta name="description" content="Developer hardware deals collected from r/buildapcsales, Slickdeals and Dealabs: price, discount and what the deal is actually good for. No sponsored placement.">
  <link rel="canonical" href="{BASE_URL}/deals/">
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/deals/">
  <meta property="og:title" content="DevTeardown Deals — developer hardware deals">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/deals/">
  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}{DEAL_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="/deals/" class="logo">⚡ DevTeardown<span>Deals</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="/ko/">한국어 핫딜</a>
        <a class="nav-link" href="/">Teardowns</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="ko-hero">
      <span class="badge badge-blue">Updated daily · source prices</span>
      <h1>Hardware deals, without the hype.</h1>
      <p class="lead">Developer-relevant deals pulled from r/buildapcsales, Slickdeals and Dealabs.
      Each card shows the price exactly as the source lists it, the discount only when the source gives
      a list price, and who the deal actually fits. No paid placement.</p>
      <div class="ko-stats">
        <div class="ko-stat"><strong>{len(feed)}</strong>live deals</div>
        <div class="ko-stat"><strong>4</strong>categories</div>
        <div class="ko-stat"><strong>{updated}</strong>updated</div>
        <div class="ko-stat"><strong>{payload.get('stats', {}).get('sources', 0)}</strong>sources</div>
      </div>
    </div>

    <h2 id="feed" style="margin-top:2.4rem;">Live tech deals</h2>
    <p style="color:#8ea3bd; font-size:0.9rem; margin-top:-0.3rem;">
      Prices are the source's own listing at collection time. Stock, tax and shipping vary by region.
    </p>
    {tabs}
    <div class="deal-grid" id="feedGrid">{feed_cards}</div>

    {cat_html}

    <div class="method-note">
      <strong style="color:#fff;">How prices are handled</strong><br>
      Every price is copied from the source post; discounts are computed only when the post states a
      list price. Links go to the source deal page, and DevTeardown takes no commission on them.
      Prices and stock move fast — confirm on the retailer page before buying.
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 DevTeardown Deals. Developer hardware curation. Prices as listed at the source.</p>
      <p style="margin-top:0.4rem;"><a href="/ko/" style="color:var(--text-muted);">한국어 핫딜 →</a>
      &nbsp;·&nbsp;<a href="/" style="color:var(--text-muted);">English teardowns →</a></p>
    </div>
  </footer>
  {TABS_JS}
</body>
</html>"""


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
  <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/">
  <link rel="alternate" hreflang="en" href="{BASE_URL}/">
  <meta property="og:title" content="{SITE_NAME} — Developer Tool Teardowns">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/">
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="./" class="logo">⚡ DevTools<span>Radar</span></a>
      <div style="display:flex; gap:1rem; align-items:center;">
        <a class="nav-link" href="./deals/">Deals</a>
        <a class="nav-link" href="./ko/">한국어 핫딜</a>
        <span class="badge badge-green">Verified Nov 2026</span>
      </div>
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

    {DEALS_SECTION_HTML}

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
      <div style="display:flex; gap:1rem; align-items:center;">
        <a href="../../deals/" class="nav-link">Deals</a>
        <a href="../../ko/" class="nav-link">한국어 핫딜</a>
        <a href="../../" class="nav-link">← All teardowns</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="meta-row">
      <span class="badge badge-blue">{item['category']}</span>
      <span class="badge badge-gray">{a['name']} vs {b['name']}</span>
      <span>DevTeardown Team</span>
      <span>·</span>
      <span>Prices verified {updated}</span>
      <span>·</span>
      <span>{rt}</span>
    </div>

    <h1>{a['name']} vs {b['name']}</h1>
    <div class="lead">{md_to_html(item['hook'])}</div>

    <div class="verdict-box">
      <div class="label">Verdict</div>
      {md_to_html(item['verdict_summary'])}
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

    {DEALS_SECTION_HTML}

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
  </url>\n  <url>
    <loc>{BASE_URL}/ko/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.9</priority>
  </url>\n  <url>
    <loc>{BASE_URL}/deals/</loc>
    <lastmod>{today}</lastmod>
    <priority>0.9</priority>
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

    # 한글 핫딜 포털 (/ko/)
    deals = load_deals()
    ko_dir = os.path.join(DIST_DIR, "ko")
    os.makedirs(ko_dir, exist_ok=True)
    with open(os.path.join(ko_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_ko_html(deals))
    print(f"  {'ko-portal':<28} feed={len(deals.get('feed', []))} deals  "
          f"picks={len(deals.get('picks', []))}  updated={deals.get('generated_at', '-')}")

    en_deals = load_deals(DEALS_EN_DATA_PATH)
    en_dir = os.path.join(DIST_DIR, "deals")
    os.makedirs(en_dir, exist_ok=True)
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_deals_en_html(en_deals))
    print(f"  {'deals-portal-en':<28} feed={len(en_deals.get('feed', []))} deals  "
          f"updated={en_deals.get('generated_at', '-')}")

    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

    with open(os.path.join(DIST_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("devteardown.com\n")

    print(f"Build complete: {len(items) + 3} pages in {DIST_DIR}")


if __name__ == "__main__":
    main()
