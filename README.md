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
# Deal collection and purchase eligibility

## Scheduled discovery, not automatic publication

`Check official deal feeds` runs at minute 17 every six hours (UTC 00:17,
06:17, 12:17, 18:17; Asia/Seoul 09:17, 15:17, 21:17, 03:17).
GitHub schedules are best-effort, can be delayed, and may be disabled by GitHub
on inactive public repositories. Check the Actions run history, not this document,
for actual execution. `workflow_dispatch` also permits an authorized manual run.

Only DealNews official RSS is enabled initially. Its RSS terms require preserving
content and links unchanged. The job therefore saves the original XML as a short-lived
Actions artifact and a status JSON; it does NOT rewrite feed links or publish source
articles onto DevTeardown. No paid API, added secret, login, or page scraping is used.
The token is `contents: read`; scheduled code cannot edit the website or repository.

Other discovered sources have explicit disabled/review states in
`config/deal_sources.json`. Do not enable a source merely because it has an RSS URL.
Slickdeals/StackSocial forbid unapproved scraping, Woot needs approved API access,
SMZDM's feed returned 403, and OzBargain reuse permission remains under review.

The collector checks robots, waits two seconds, uses conditional HTTP headers when
available, caps response size at 2 MB, uses a 25-second timeout, rejects redirects,
DTD/entities and empty feeds, and stops on 401/403/429. It does not solve challenges,
change identity or try another access path. Source failures keep the last-success
metadata in the cache and produce a failed run rather than a fake successful update.

Artifacts are retained for seven days. The last XML and status are also cached and carried forward on HTTP 304. GitHub cache is best effort. Last-good published
products remain in Git and their actual price-check dates are never changed by a crawl.
Operators should review the original feeds, independently verify the actual merchant
URL, current price/currency, region, delivery, activation, tax, refund and coupon terms,
and then intentionally update curated `data/deals_en.json`. Keep source attribution.
Never copy product images without a usable permission basis. Archive superseded data.

## Country statements

`purchase_eligibility` separates confirmed destination evidence from unknown billing,
activation, payment and refund restrictions. Digital delivery, a USD/CNY price, an
English/Chinese interface or a source's country is NOT evidence of worldwide/local
purchase eligibility. No guessed country allowlists. China candidates remain unpublished
until a current mainland offer is independently verified.

## Validation

Run `python3 tools/check.py` before publication. For an authorized live feed check:
`python3 tools/collect_deal_feeds.py --output collection-output`.

## Unified multilingual catalogue

`site_i18n.py` renders the same curated Korean and international records in six languages.
English uses `/deals/`; `/ko/`, `/zh/`, `/ja/`, `/es/`, `/fr/` share the same catalogue.
Market and category filters are combined and retained in the URL when changing language.
`data/deal_localizations.json` contains the translated product summary and purchase caveats.
The expandable original source record is deliberately not translated or presented as new verification.
Korean records retain their historical prices; inclusion does not reverify availability.
Comparison articles remain English, with a clearly labeled original-language fallback and common navigation.

### Product-link registration gate

Product buttons must use the exact seller product detail URL, never search, category,
store homepage or a short/redirect link. Preserve the original URL in `link_original`
when correcting a record. `tools/product_links.py` recognizes reviewed seller-detail
routes and rejects search/redirect query parameters; add a new seller deliberately
with regression tests rather than treating arbitrary non-search paths as products.

For publication, each record needs `link_review.status=verified_detail`, the identical
`url`, a real ISO `checked_at`, `product_match=true`, and nonempty `evidence` describing
the observed model/variant. A URL pattern or HTTP 200 is **not** product verification.
Check the final redirected URL and product content manually, including variants and
country. When blocked, ambiguous, expired, redirected to search, or unverified, set
`status=held` and `reason`; all six language views retain the record but remove the
purchase button. Do not bypass access restrictions or fabricate product IDs.

The build/CI fails on unreviewed new records. Review metadata is a human evidence
attestation, not a live-stock guarantee; a later retailer redirect still requires a
fresh check. RSS collection remains staging-only and cannot publish unchecked cards.
