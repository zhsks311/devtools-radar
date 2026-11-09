import os
import json
import datetime

BASE_URL = "https://zhsks311.github.io/devtools-radar"
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
  --danger: #f43f5e;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background-color: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.65;
  padding: 0;
  margin: 0;
}
.container { max-width: 920px; margin: 0 auto; padding: 2rem 1.5rem; }
header {
  border-bottom: 1px solid var(--border);
  padding: 1.25rem 0;
  background: rgba(9, 13, 22, 0.85);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  max-width: 920px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo { font-size: 1.25rem; font-weight: 700; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
.logo span { color: var(--primary); }
.badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
.badge-blue { background: rgba(56, 189, 248, 0.1); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.3); }
.badge-green { background: rgba(16, 185, 129, 0.1); color: var(--accent); border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-gray { background: #1e293b; color: #94a3b8; border: 1px solid #334155; }
h1 { font-size: 2.25rem; font-weight: 800; line-height: 1.25; margin: 1rem 0; color: #fff; }
h2 { font-size: 1.5rem; font-weight: 700; color: #fff; margin: 2.5rem 0 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
h3 { font-size: 1.2rem; font-weight: 600; color: #fff; margin: 1.5rem 0 0.5rem; }
p { margin-bottom: 1rem; color: #cbd5e1; font-size: 1rem; }
.lead { font-size: 1.15rem; color: var(--text-muted); margin-bottom: 2rem; }
.meta-row { display: flex; align-items: center; gap: 1rem; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.5rem; }
.table-wrapper { overflow-x: auto; margin: 1.5rem 0 2rem; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
th, td { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border); }
th { background: #162032; color: #fff; font-weight: 600; }
tr:last-child td { border-bottom: none; }
.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  text-align: center;
}
.btn-primary { background: var(--primary); color: #000; }
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-outline { border: 1px solid var(--border); color: var(--text); background: var(--surface); }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.75rem;
  margin-bottom: 1.5rem;
  transition: border-color 0.2s, transform 0.2s;
}
.card:hover { border-color: #3b82f6; transform: translateY(-2px); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0; }
.verdict-box {
  background: linear-gradient(145deg, #132238 0%, #0d1829 100%);
  border: 1px solid #1e3a5f;
  border-radius: 12px;
  padding: 1.75rem;
  margin: 1.5rem 0 2.5rem;
}
.pros-cons-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0; }
@media (max-width: 680px) { .pros-cons-grid { grid-template-columns: 1fr; } }
.pros-box { background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 1.25rem; }
.cons-box { background: rgba(244, 63, 94, 0.05); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 10px; padding: 1.25rem; }
.pros-box ul, .cons-box ul { padding-left: 1.25rem; margin-top: 0.5rem; }
.pros-box li, .cons-box li { font-size: 0.9rem; margin-bottom: 0.4rem; color: #cbd5e1; }
pre {
  background: #0d121d;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  overflow-x: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85rem;
  color: #38bdf8;
  margin: 1rem 0;
}
.migration-box {
  background: #121e33;
  border-left: 4px solid var(--primary);
  border-radius: 0 8px 8px 0;
  padding: 1.25rem 1.5rem;
  margin: 1.5rem 0;
}
.faq-item { border-bottom: 1px solid var(--border); padding: 1.25rem 0; }
.faq-q { font-size: 1.1rem; font-weight: 600; color: #fff; margin-bottom: 0.5rem; }
.faq-a { color: var(--text-muted); font-size: 0.95rem; }
footer { border-top: 1px solid var(--border); padding: 2.5rem 0; margin-top: 4rem; text-align: center; color: var(--text-muted); font-size: 0.875rem; }
"""

def generate_index_html(items):
    cards_html = ""
    for item in items:
        a = item["tool_a"]
        b = item["tool_b"]
        cards_html += f"""
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
            <span class="badge badge-blue">{item['category']}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">{item['reading_time']}</span>
          </div>
          <h2 style="font-size:1.35rem; color:#fff; margin-bottom:0.5rem; border-bottom:none; padding-bottom:0;">{a['name']} vs {b['name']}</h2>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1.25rem; line-height:1.5;">{item['verdict_summary'][:130]}...</p>
          <a href="./compare/{item['slug']}/" class="btn btn-outline" style="width:100%; display:block;">Read In-Depth Comparison →</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevTools Radar — Unbiased Developer Software Comparisons (2026)</title>
  <meta name="description" content="Data-driven side-by-side architecture, pricing, and performance benchmarks for modern developer platforms and developer tools.">
  <link rel="canonical" href="{BASE_URL}/">
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="./" class="logo">⚡ DevTools<span>Radar</span></a>
      <span class="badge badge-green">2026 Developer Directory</span>
    </div>
  </header>

  <main class="container">
    <div style="text-align: center; max-width: 720px; margin: 2rem auto 3.5rem;">
      <span class="badge badge-blue" style="margin-bottom:1rem;">Programmatic Developer Intelligence</span>
      <h1>Zero-Fluff Developer Tool Comparisons</h1>
      <p class="lead">We parse pricing formulas, cold starts, vendor lock-in risks, and API specs so you can architect with confidence without reading 40 biased sponsored blog posts.</p>
    </div>

    <div class="grid">
      {cards_html}
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 DevTools Radar. Generated programmatically from open benchmark datasets.</p>
      <p style="margin-top:0.5rem; font-size:0.8rem;">Independent developer intelligence with zero paid sponsored placement.</p>
    </div>
  </footer>
</body>
</html>"""

def generate_comparison_html(item):
    a = item["tool_a"]
    b = item["tool_b"]
    slug = item["slug"]
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f["a"]
                }
            }
            for f in item["faqs"]
        ]
    }

    # Pros and Cons
    a_pros_html = "".join([f"<li>✓ {p}</li>" for p in a.get("pros", [])])
    a_cons_html = "".join([f"<li>✗ {c}</li>" for c in a.get("cons", [])])
    b_pros_html = "".join([f"<li>✓ {p}</li>" for p in b.get("pros", [])])
    b_cons_html = "".join([f"<li>✗ {c}</li>" for c in b.get("cons", [])])

    # Deep dive sections
    deep_dive_html = ""
    for sec in item.get("deep_dive_sections", []):
        deep_dive_html += f"""
        <h3>{sec['title']}</h3>
        <p>{sec['content'].replace(chr(10), '</p><p>')}</p>
        """

    # FAQs
    faqs_html = ""
    for f in item["faqs"]:
        faqs_html += f"""
        <div class="faq-item">
          <div class="faq-q">Q: {f['q']}</div>
          <div class="faq-a">{f['a']}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{a['name']} vs {b['name']} (2026 Benchmark): Which is Best?</title>
  <meta name="description" content="In-depth developer guide comparing {a['name']} and {b['name']}. Analyze pricing formulas, database architectures, vendor lock-in, and self-hosting options.">
  <link rel="canonical" href="{BASE_URL}/compare/{slug}/">
  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="../../" class="logo">⚡ DevTools<span>Radar</span></a>
      <a href="../../" style="color:var(--text-muted); text-decoration:none; font-size:0.9rem;">← All Comparisons</a>
    </div>
  </header>

  <main class="container">
    <div class="meta-row">
      <span class="badge badge-blue">{item['category']}</span>
      <span>• Updated November 2026</span>
      <span>• {item['reading_time']}</span>
    </div>

    <h1>{a['name']} vs {b['name']} (2026 Developer Benchmark)</h1>
    <p class="lead">An objective, architectural breakdown for engineering teams deciding between {a['name']} and {b['name']}.</p>

    <div class="verdict-box">
      <h3 style="color:#fff; margin-top:0; font-size:1.15rem;">🎯 Executive Verdict</h3>
      <p style="color:var(--text); line-height:1.6; margin-bottom:0;">{item['verdict_summary']}</p>
    </div>

    <h2>1. Key Metric Comparison</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Metric / Dimension</th>
            <th>{a['name']} <span class="badge badge-blue">{a['badge']}</span></th>
            <th>{b['name']} <span class="badge badge-green">{b['badge']}</span></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Core Engine / Architecture</strong></td>
            <td>{a['db']}</td>
            <td>{b['db']}</td>
          </tr>
          <tr>
            <td><strong>Pricing & Free Tier</strong></td>
            <td>{a['pricing']}</td>
            <td>{b['pricing']}</td>
          </tr>
          <tr>
            <td><strong>Self-Hostable</strong></td>
            <td><strong>{a['self_host']}</strong></td>
            <td>{b['self_host']}</td>
          </tr>
          <tr>
            <td><strong>Realtime & Concurrency</strong></td>
            <td>{a['realtime']}</td>
            <td>{b['realtime']}</td>
          </tr>
          <tr>
            <td><strong>AI & Vector Readiness</strong></td>
            <td>{a['ai_readiness']}</td>
            <td>{b['ai_readiness']}</td>
          </tr>
          <tr>
            <td><strong>Vendor Lock-In Risk</strong></td>
            <td><span style="color:var(--accent); font-weight:600;">{a['lock_in']}</span></td>
            <td><span style="color:var(--danger); font-weight:600;">{b['lock_in']}</span></td>
          </tr>
          <tr>
            <td><strong>Official Action</strong></td>
            <td><a href="{a['cta_url']}" target="_blank" rel="noopener" class="btn btn-primary" style="padding:0.4rem 0.85rem; font-size:0.85rem;">Try {a['name']} →</a></td>
            <td><a href="{b['cta_url']}" target="_blank" rel="noopener" class="btn btn-outline" style="padding:0.4rem 0.85rem; font-size:0.85rem;">Try {b['name']} →</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>2. Side-by-Side Code & SDK Experience</h2>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
      <div>
        <span class="badge badge-blue" style="margin-bottom:0.5rem;">{a['name']} Code Sample</span>
        <pre><code>{a.get('code_example', '')}</code></pre>
      </div>
      <div>
        <span class="badge badge-green" style="margin-bottom:0.5rem;">{b['name']} Code Sample</span>
        <pre><code>{b.get('code_example', '')}</code></pre>
      </div>
    </div>

    <h2>3. Architectural Deep Dive</h2>
    <div style="margin: 1.5rem 0;">
      {deep_dive_html}
    </div>

    <h2>4. Pros & Cons Analysis</h2>
    <div class="pros-cons-grid">
      <div class="card" style="padding:1.25rem;">
        <h3 style="color:var(--primary); margin-top:0;">{a['name']} Analysis</h3>
        <div class="pros-box" style="margin-bottom:1rem;">
          <strong style="color:var(--accent); font-size:0.9rem;">Advantages</strong>
          <ul>{a_pros_html}</ul>
        </div>
        <div class="cons-box">
          <strong style="color:var(--danger); font-size:0.9rem;">Limitations</strong>
          <ul>{a_cons_html}</ul>
        </div>
      </div>
      <div class="card" style="padding:1.25rem;">
        <h3 style="color:var(--accent); margin-top:0;">{b['name']} Analysis</h3>
        <div class="pros-box" style="margin-bottom:1rem;">
          <strong style="color:var(--accent); font-size:0.9rem;">Advantages</strong>
          <ul>{b_pros_html}</ul>
        </div>
        <div class="cons-box">
          <strong style="color:var(--danger); font-size:0.9rem;">Limitations</strong>
          <ul>{b_cons_html}</ul>
        </div>
      </div>
    </div>

    <h2>5. Migration Guide & Considerations</h2>
    <div class="migration-box">
      <strong style="color:#fff; font-size:1.05rem;">Switching Paths:</strong>
      <p style="margin-top:0.5rem; margin-bottom:0;">{item.get('migration_guide', '')}</p>
    </div>

    <h2>6. Frequently Asked Questions</h2>
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:1.5rem;">
      {faqs_html}
    </div>

    <div style="text-align:center; margin: 3.5rem 0 1rem;">
      <h3 style="margin-bottom:1rem;">Ready to build?</h3>
      <a href="{a['cta_url']}" target="_blank" rel="noopener" class="btn btn-primary" style="margin-right:1rem;">Start on {a['name']} for Free →</a>
      <a href="{b['cta_url']}" target="_blank" rel="noopener" class="btn btn-outline">Explore {b['name']} →</a>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>© 2026 DevTools Radar. Independent developer analysis.</p>
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
    <lastmod>{today}</lastmod>
    <priority>0.8</priority>
  </url>\n"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    # 1. Landing Page
    index_html = generate_index_html(items)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 2. Comparison Pages
    for item in items:
        page_dir = os.path.join(DIST_DIR, "compare", item["slug"])
        os.makedirs(page_dir, exist_ok=True)
        html = generate_comparison_html(item)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # 3. Sitemap & Robots
    sitemap = generate_sitemap(items)
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

    print(f"Build complete! Generated {len(items) + 1} deep pages in {DIST_DIR}")

if __name__ == "__main__":
    main()
