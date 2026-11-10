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
python3 tools/check.py               # final lint + deployment lint + tests + merge/build/output QA
# Publish preparation (local files only; does not push or deploy):
python3 content/merge.py             # refresh editorial fields, preserve all existing slugs/metadata
python3 build.py                     # validates actual input, staged render, removes stale generated pages
python3 tools/check_site.py          # local links, article set, sitemap, JSON-LD, unsafe markup
```

Python 3.11+ and the standard library are sufficient. Commands work from any working directory.
`tools/check.py` uses disposable copies for merge and build, so it does not modify `data/` or `dist/`.
GitHub Actions runs the same check on pushes and pull requests; it does not deploy.

`build.py --data PATH --output DIR --deals PATH --deals-en PATH` supports isolated builds.
Invalid/empty deployment input, duplicate or unsafe slugs, unresolved related articles, unsafe
external URLs, and corrupt/missing deal feeds fail before replacing the output. HTML text and
attributes are escaped, external links allow HTTP(S) only, and JSON-LD cannot close its script tag.

The output `.generated-files.json` tracks generated files. A successful build removes obsolete
owned pages but retains unmanaged assets; a failed validation/render leaves the previous output
intact. First-time migration recognizes legacy comparison pages by their generated page markers.
Do not hand-edit generated pages or place source files/symlinks inside the output directory.

Article dates and metadata are not refreshed just by running merge. New final articles require
complete deployment metadata either in the final JSON or an existing data entry; missing metadata
is an error. Removing a final file does not implicitly delete a published article. To intentionally
retire one, remove its final file and deployment entry and update related references together.


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
