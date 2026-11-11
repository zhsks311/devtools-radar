# AliExpress affiliate integration

The renderer supports reviewed, publisher-issued AliExpress promotion links. No
AliExpress links or products are enabled by this change. Program approval alone
does not establish a working tracking link or API access. Never substitute a
documentation example, another publisher's link, or a made-up tracking ID.

## Activation without sharing secrets

1. In the owner's AliExpress Portals account, generate a normal product link for
   a product actually reviewed for this catalogue. A product-to-promotion-link
   export is sufficient. Do not request a password or app secret in chat.
2. Keep the exact canonical seller product URL in `link.url`. Complete the
   existing `link_review`, price evidence and country evidence independently.
   A commission link does not establish price, stock, discount or shipping.
3. Store `affiliate.network` as `aliexpress`, `affiliate.status` as `verified`,
   `affiliate.source_url` as the same canonical seller URL, and
   `affiliate.promotion_url` as the exact owner-issued HTTPS promotion link.
4. In `affiliate.review`, record that exact `promotion_url`, its observed final
   `resolved_product_url`, `owner_confirmed: true`, `product_match: true`, the
   timezone-aware `checked_at`, and a concrete `evidence` description. Confirm
   that the link belongs to this publisher and lands on the same product and
   variant. A URL shape or an HTTP 200 alone is not sufficient evidence.
5. Run `python3 tools/check.py`, inspect all six language versions, and verify
   the destination once. Do not create automated tracking clicks, test purchases
   or commission claims. Only AliExpress's own reports establish attribution.

If a promotion link is blocked, unverified, expired or unavailable, use
`affiliate.status: held` and a nonempty `reason`. Its promotion URL will not be
emitted. A separately verified canonical product link can remain visible without
the AliExpress commission claim. If the product itself is unverified, hold its
`link_review` too. Malformed or contradictory active affiliate metadata fails CI.

Approved link shapes are deliberately narrow. Adding another official hostname
or redirect family requires a reviewed example and regression tests; do not
loosen the allowlist to accept arbitrary shorteners. Keep promotion links intact
rather than appending guessed tracking parameters or wrapping them in a local
redirect. Canonical AliExpress product URLs accept only numeric SKU selectors
(`sku_id` or `skuId`), not hidden affiliate or redirect parameters.
Product title and purchase-button links both receive `rel="sponsored"`,
and an explicit, translated commission notice appears directly before the
purchase button. Existing tracked links receive the same disclosure treatment.

## API option

The official `aliexpress.affiliate.link.generate` documentation requires an app
key, a signed request, a publisher `tracking_id`, source values and a link type.
Normal product conversion uses type `0`. The response includes `promotion_link`
and `source_value`; keep that mapping. An approved affiliate account is not proof
that an API application is configured or approved. No API client, credentials,
new account, subscription or scheduled tracking requests are installed here.
If API access is later configured, app secrets belong only in approved server-side
secret storage, never Git, public JSON, generated HTML or browser JavaScript.

## Operational checks and claims

- Use material from the approved Portals/API channel with its actual permission
  basis. Affiliate membership does not authorize scraping or copying all images.
- Do not promise a commission rate, guaranteed income, a cookie duration, lowest
  price, free shipping or worldwide delivery without applicable source evidence.
- Recheck links when offers change. AliExpress's agreement allows short-key
  invalidation after one year, after six months without clicks, or for infringing
  content. A past review is not an ongoing validity guarantee.
- Keep useful comparison/selection content; a catalogue of copied descriptions
  with affiliate buttons alone is not an SEO strategy.

## Official references checked 2026-11-11

- [AliExpress Affiliate Program Service Agreement, effective April 1, 2025](https://cdn.contract.alibaba.com/terms/b_platform_service_agreement/20250305142526766/20250305142526766.html?lng=en)
- [Official affiliate link-generation API](https://developer.alibaba.com/docs/api.htm?apiId=45804)
- [Google: qualifying affiliate links](https://developers.google.com/search/blog/2021/07/link-tagging-and-link-spam-update)
- [FTC: endorsement and affiliate disclosure guidance](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)

Account-specific Portals rules, product participation and country-specific
advertising requirements must also be checked when activating real links.
