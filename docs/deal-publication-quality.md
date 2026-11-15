# Deal publication quality controls

## 2026-11-15: price-unverified discoveries mixed with offers

Five AliExpress candidates had only third-party product-ID evidence and null current
prices. Rendering them at the front of the ordinary product grid made research
leads look like incomplete verified offers. A seller-page recheck did not yield
usable price/variant/stock evidence; no prices or review dates were fabricated.

- Keep discoveries outside the ordinary product grid in a separately labelled,
  collapsed research section. Search may reveal that section without counting it
  as a verified offer. Preserve country/category filters and independent counts.
- Null prices must not be replaced with zero, a scraped search snippet, reference
  price, or an old observation. No percentage/strike-through without comparable
  evidence. URL identity is not price or country-eligibility verification.
- Keep original observations and blocked attempts distinct. Source retrieval time
  is not publication time and a failed attempt cannot refresh successful review.
- Regression tests exercise all six languages, DOM section separation, search,
  country/category combinations, reset and browser history.

## DEAL20 follow-up

The seller campaign states 2026-11-09 through 2026-11-15, without an exact end time
or timezone. In the existing next scheduled product review after that date,
recheck all five affected seller pages and the campaign before describing this
code as current. Preserve historical coupon evidence; do not roll its dates
forward or infer a new campaign. Base product availability and base price require
separate checks. Remove or mark lapsed coupon prose across six languages when
expiry is established; this file does not itself schedule or execute a review.

## Revenue readiness, 2026-11-15

`python -m tools.audit_monetization` separates active ordinary destinations from
published commission destinations and held tracking links. On this audit: 22
active ordinary links, zero published commission links, 13 held tracking links.
A programme approval is not a product tracking URL or evidence of attributable
sales. Never restore a held search/mismatched destination merely to earn fees.
Obtain owner-issued product-specific links, verify exact destination and programme
ownership, then apply existing disclosure/rel=sponsored safeguards. Revenue and
attribution remain unverified until the programme reports actual results.

Product-specific catalogue anchors now provide a shareable return path in six
languages without sending visitor data, adding trackers or inventing Product
schema. They are not independent search-indexed product landing pages. Next
content work should add substantiated buying comparisons and useful conditions,
not duplicate thin pages or unsupported reviews. Conversion improvements are
hypotheses until measured; no traffic or revenue uplift is claimed.
