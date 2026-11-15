# Country classification

The shopping-country filter describes the buyer audience, not an address-level
shipping guarantee. Korean community deals target Korea by default. Preserve the
original community URL in `source.url`; do not replace it with an aggregator.
`country_targeting` stores reviewed countries, basis and fulfilment separately
from `purchase_eligibility.countries_confirmed`, which still needs seller evidence.

- Domestic goods and Korean mobile vouchers belong under Korea.
- Overseas storefronts can still target Korean buyers. Keep cross-border freight,
  forwarding, customs, local-payment and activation restrictions in conditions.
- Overseas-only/local-pickup leads must set `fulfilment: overseas_only`; they do
  not inherit Korea from a Korean community. Review the destination separately.
- Language, currency, a generic `global` label and digital delivery alone are not
  sufficient evidence of a target or activation country.
- Country classification never upgrades a held link, stale price or unverified
  discount. Archived records remain separate from active offers.

RSS ingestion is only source discovery, not automatic publication. Current
collector archives DealNews; no Korean community feed has yet passed access and
reuse review. Do not claim Korean collection is enabled until tested. Review
robots/official feed availability, keep original timestamps and exact product
links, and do not bypass denied endpoints.

## Community-source operating scope (2026-11-15)

- Quasarzone: public posts can supply product leads; automated access/reuse is not
  established. Do not mirror post bodies, comments, handles or community images.
- FM Korea: robots request returned 429; further direct requests stopped.
- Ppomppu: source access failed with 403; discovery is not collector activation.
- A community price is a lead, not the current seller price. Capture seller URL,
  option, coupon requirements and actual observation separately. Sold-out or
  conflicting latest observations stay out of the active catalogue.
- Example exclusions this pass: Xbox KR100k card seller2186872881 displayed95k
  instead of reported89.9k; Mega KR10k card4885499854 was later SOLD OUT. Neither
  was published using the earlier community price.

Potential licensed sources, not enabled:
- LinkPrice official affiliate guide documents hot-deal APIs:
  https://www.linkprice.com/views/affiliateguide/guide02.html
  Existing account/API entitlement, advertiser permissions, quotas and storage or
  translation rights must be checked before using it. No account/key was created.
- Consumer Agency open data may help with dated price context, not live stock or
  purchase links: https://www.data.go.kr/data/15158701/openapi.do
- An unverified robots response is not a confirmed Disallow rule. Current disabled
  status records the actual access/reuse uncertainty, not a legal conclusion.
