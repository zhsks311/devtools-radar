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
