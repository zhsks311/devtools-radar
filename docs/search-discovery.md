# Search and AI discovery checks

## What the build guarantees

`python3 tools/check.py` runs the content, unit, filter-JavaScript and generated-output
gates without modifying repository data. `python3 build.py` intentionally regenerates
`dist/`; run `python3 tools/check_site.py` against that final output before deployment.

- Every generated page has one title, description, H1 and query-free self-canonical URL.
  Open Graph and structured page identity must match that URL.
- The six catalog views form one reciprocal language group. The comparison indexes
  form a separate group. `/ko/` is a catalog, not a translation of an English article.
  Localized comparison indexes identify their articles as English and mark their
  English abstracts accordingly. They do not claim the articles were translated.
- HTML and sitemap language alternates match, including self and `x-default`.
  The sitemap contains exactly the generated canonical pages, with no duplicates.
  Build time is not presented as a new content revision or source-review date.
- Page, site and publisher identities use consistent JSON-LD IDs. Article source
  citations must be linked visibly. No fabricated product offers, ratings, reviews
  or personal-use experience are added for search appearance.
- The crawl check covers Googlebot, Bingbot, OAI-SearchBot and PerplexityBot.
  OAI-SearchBot is explicitly allowed for ChatGPT search. The prior GPTBot/training
  crawl policy is unchanged; training permission is not a search requirement.
- The optional `llms-full.txt` export includes complete article section text and
  vendor source links. It does not cut qualifiers at an arbitrary character limit.
  Product URLs pass the same reviewed-link gate as visible cards. Held records are
  omitted. Seller-price observations require the existing dated evidence gate;
  other amounts are labeled retained and unverified. Exporting is not rechecking.

Filter query URLs retain the unfiltered canonical. Filters are useful navigation,
not independently verified landing pages. Do not add every filter combination to
the sitemap or claim translated navigation establishes local purchase eligibility.

## What still requires live evidence

After an authorized deployment, inspect HTTP status and redirects, the deployed
canonical/hreflang/schema, `robots.txt`, `sitemap.xml`, and the text export. Test a
nonexistent URL returns HTTP 404, rather than a success page. A local pass cannot
prove the CDN is serving the intended commit or that a crawler can reach it.

Search Console/Bing Webmaster Tools verification, sitemap submission, indexed-page
counts, ranking, search clicks, AI citations and affiliate conversion have **not**
been established by these code checks. Use the owner's connected accounts to check
them before claiming success. Do not add invented verification tokens, site traffic
or conversion statistics. Adding analytics or account integrations is separate work.

Prioritize useful original comparisons, current vendor evidence, accurate offer
conditions and working product destinations before adding new landing pages. Review
high-value pages when vendor terms change. Do not refresh a date without a real
source review, mass-produce location variants, or promise search placement or revenue.

## Primary guidance reviewed for this implementation

- [Google localized-version guidance](https://developers.google.com/search/docs/specialty/international/localized-versions):
  reciprocal language annotations and self-references.
- [Google AI-feature guidance](https://developers.google.com/search/docs/appearance/ai-features):
  standard search requirements apply; no special AI file or schema is required,
  and crawling, indexing and serving are not guaranteed.
- [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots):
  OAI-SearchBot, GPTBot and user-triggered retrieval have different purposes.

The plain-text export is a convenience for readers and retrieval systems, not a
claim that `llms.txt` causes indexing, rankings or AI citations.
