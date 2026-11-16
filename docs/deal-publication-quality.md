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

## Stock correction, 2026-11-15 18:41 UTC

The Anker P31i D1202 Gmarket offer (4620949305) now renders `SOLD OUT`
without a current item price. Its earlier KRW 24,440 coupon and colour quantities
are historical observations, not current purchase conditions. Keep the record and
prior review for audit, but hold the card and clear its verified current price.
A still-reachable product URL or a delivery estimate is not stock confirmation.
The regression test must prevent this item returning to the active catalogue
without a new seller availability/price review. Do not erase history to fix stock.

This pass inspected nine existing seller pages, not the whole catalogue. Seven
were readable; two Lenovo China pages timed out. The unchanged six were Belkin,
Ugreen, Mega HOT Americano, AdGuard, Otter A/B and Koofr. Preserve last-good
review timestamps for unrefreshed or inaccessible products. Displayed coupons
are conditional and do not establish completed checkout or a market-low price.

### 2026-11-16: expired stock must leave active offers
Gmarket 4885511021 (Mega HOT Americano) now explicitly displays SOLD OUT and no current price. The previous KRW1,320 remains only in historical evidence. The record and Korean audience classification are retained, but all six catalogues hide the purchase link and price in the held archive. This check does not infer stock from the stale daily purchase-limit field.

### 2026-11-16: buyer-facing cards, not internal audit dumps
Active cards now lead with a specific purpose, visual and purchase action. Raw source JSON stays in the repository and is never rendered into cards, even when expanded. Purchase limitations, renewal/refund terms and dated source links remain in closed, readable sections. Original category illustrations are explicitly labelled and never presented as product screenshots. Existing licensed images are retained. Proton's media-kit reuse terms were located, but asset requests returned 403: no blocked images were copied or hotlinked. Regression tests cover all six languages, illustration coverage and action-before-details order.

## Availability regression: Google Play code (2026-11-16)
The seller displayed SOLD OUT while still showing a one-per-day purchase limit.
Purchase limits must never be treated as remaining inventory. Preserve prior
price evidence as history, remove the current buying CTA when sold out, and
record the actual observation time without guessing when stock changed.
`tools.deal_availability.classify_visible_offer` accepts only reviewer-extracted
visible exact-offer text, not raw HTML containing hidden sold-out templates.
Access failures and unselected variants remain separate unknown states. A buy
button and displayed price only establish `purchase_ui_observed`, not successful
checkout, stock reservation, or eligibility. `publishable_link` blocks recorded
sold-out offers even if an older product-link review was positive.
