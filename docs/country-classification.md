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
