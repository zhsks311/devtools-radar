# ⚡ DevTools Radar — Programmatic SEO Static Site Generator

A production-ready, zero-cost programmatic SEO comparison directory for developer tools and SaaS products.

## Architecture

- **Data Layer**: `data/tools.json` (Structured benchmark metrics for competing developer tools)
- **Compiler**: `build.py` (Vanilla Python 3 — zero npm/node dependencies, generates modern responsive dark-mode HTML)
- **Distribution**: `dist/` (Static HTML pages + `sitemap.xml` + `robots.txt` + `JSON-LD` Rich Snippet schema)
- **Hosting**: Designed for **Cloudflare Pages** (Free tier, zero bandwidth fees, global anycast edge)

## Quick Start

```bash
# 1. Compile the site
python3 build.py

# 2. Deploy to Cloudflare Pages via GitHub
git init
git add .
git commit -m "Deploy DevTools Radar"
gh repo create devtools-radar --public --source=. --push
```

In Cloudflare Pages Dashboard:
- Connect your GitHub repository `devtools-radar`
- Set **Build command**: `python3 build.py`
- Set **Build output directory**: `dist`
- Click **Deploy**!
