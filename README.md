# ⚡ DevTools Radar — comparison teardowns with the arithmetic shown

A static, zero-dependency comparison site for developer tools. Every article treats a vendor's price
sheet as a **penalty table** — which usage does this meter punish — then shows the arithmetic at the
volume you will actually reach, and ends with a decision matrix.

## Pipeline

```
content/facts/{slug}.md        verified facts only (prices, limits, sources) — written by hand
        │
        │  omp --model claude-opus-5-5   (author)
        ▼
content/draft/{slug}.json      article written under the writing standard, restricted to the fact sheet
        │
        │  omp --model gpt-6.1-sol       (reviewer — never the author's model)
        ▼
content/review/{slug}.md       defect list: FACT / META / SLOP / LOGIC / RHYTHM / BORING / WEAK
        │
        │  omp --model <reviewer>        (reviser implements the review)
        ▼
content/final/{slug}.json  →  data/tools.json  →  build.py  →  dist/
```

`tools/lint_content.py` is the gate: banned phrases, meta-text, body length, paragraph length, visual
anchor density, and the shape of `decision_matrix` / `cost_math` / `faqs`. A file that fails does not ship.

```bash
python3 tools/lint_content.py        # gate
python3 build.py                     # render dist/
```

The writing standard itself lives outside this repo at `docs/tech-blog-writing-standard.md`
(four archetypes, hook formulas, the comparison ladder, anti-patterns, prompt contracts).

## Architecture

- `data/tools.json` — one object per comparison: product metadata, hook, sections (markdown subset),
  cost arithmetic, decision matrix, verdict, migration path, FAQs, sources.
- `build.py` — vanilla Python 3, no npm. Renders a markdown subset (headings, lists, tables, fenced
  code, blockquotes, bold, inline code) and emits TechArticle + FAQPage + BreadcrumbList JSON-LD.
- `dist/` — static output; published to the `gh-pages` branch.

## Verify before trusting a number

Each article carries `last_verified` and a `sources` list. Prices in this market move twice a year —
if a figure here disagrees with a vendor's price sheet, the price sheet wins.
