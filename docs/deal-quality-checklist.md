# Deal publication gate and incident register

## 2026-11-10: false discount correction
- Coupang 10,000 KRW gift card had sale=reference=10,000 and discount_pct=0. This is NOT a discount. The old renderer checked only whether original_price existed and struck it out unconditionally. Registration had no comparable-price evidence gate. An editorial score did not prove savings.
- All 17 Korean reference prices/percentages lacked verified comparison evidence. Moved them to rejected historical_claims, never silently destroyed. No new merchant price checks were performed for this correction. Existing price-review timestamps remain unchanged.
- The unified six-language renderer already avoided strike-through; the legacy renderer still had the defect. Both now fail closed. The exact equal-price record explicitly says no discount in all six languages.
- data/discount_corrections.json is the correction audit. data/price_audit.json is the prior source-price review, not a fresh result.

## Before publishing each product
1. Direct exact seller product detail page, final redirect and model/variant match. Never search/category/home/short links. HTTP 200 or a search snippet alone is insufficient. Preserve original links and hold unverified CTAs.
2. Record seller source URL, currency, numeric displayed price, actual check timestamp and observed evidence. Keep capture time separate from publication time. Check stock separately; purchase UI does not guarantee inventory.
3. Separate seller price from checkout: coupon, membership, new-customer, tax, delivery, region and payment conditions. Do not claim a coupon's final price without checkout evidence.
4. Discount comparison must be same variant, currency, quantity, license version/devices, billing period, eligibility and cost basis. Recurring vs lifetime, old version vs new, 1 vs 3 devices and USD vs PLN/EUR are NOT comparable discounts.
5. Former seller price is distinct from official RRP. A current price below RRP is not historical-low proof. Never label unverified market minima or inflate list prices.
6. Equal/reversed prices, missing evidence and amounts that round to 0%: no strike-through or discount badge. Preserve rejected claims as history, use ordinary price/held status. Derive percentage from amounts, do not trust scraped percentages.
7. Do not refresh a check timestamp because a build/RSS ran. Feeds stage candidates only. Changed price/URL/currency invalidates matching evidence. Recheck aging offers; never imply a dated observation is a live guarantee.
8. Run python tools/check.py before deployment. CI calls the same build and rejects unsupported active discount fields, price-review mismatch, unreviewed product links and regression failures. Verify all six outputs and live deployed revision.

## Follow-up examples to prevent recurrence
- Slidepad: version/device counts differ; no like-for-like discount.
- PDF Expert/Koofr: currency or subscription period differs; no discount percentage.
- TextSniper/Action: conflicting reference price or license scope; no exact discount assertion.
- Korean listings: unavailable exact seller identity/current price; keep held, not advertised as current hot deals.
- Stock or regional eligibility unknown: explicitly unknown, not inferred from language/currency.

## 2026-11-11: country and related catalogue corrections
- The former single market field mixed source country (KR), storefront country (CN), and delivery evidence (AU). The new independent storefront and destination selectors never infer delivery from currency, category or language. Existing country evidence is unchanged: only the Switch 2 record has AU evidence; all other destinations remain unverified.
- Explicit storefront classifications use the retained Korean Coupang records, reviewed DJI CN/Lenovo CN product URLs and EB Games Australia product URL. StackSocial remains unclassified rather than assuming US/global eligibility. No checkout, shipping or activation was newly certified by this correction.
- Lenovo GK10 and LOQ were hidden from their real categories because all China records were forced into hardware. They now appear under keyboards/mice and monitors/desks respectively, including China storefront + category intersections.
- Linked Lenovo records with unverified current prices keep their product descriptions, not a false claim that product identity is unverified. Current price caveats and historical-price labels remain visible.
- Koofr’s limit corrected in six translations and source briefing: one code redemption per person in their lifetime, not one per account. Source: https://www.stacksocial.com/sales/koofr-cloud-storage-plans-lifetime-subscription-1tb. Coupon prices remain advertised/unverified, and source price timestamps were not refreshed.
- All five localized report pages no longer redeclare the language-menu JavaScript; their lower catalogue link keeps the chosen language.
- Regression gate covers ISO/evidence validation, multiple destinations, all 3,240 current filter combinations, unknown versus unavailable, held/active counts, URL restore/reset, language switching, report scripts and category assignments.
