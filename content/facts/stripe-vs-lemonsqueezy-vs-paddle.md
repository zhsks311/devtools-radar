# FACT SHEET — stripe-vs-lemonsqueezy-vs-paddle (verified 2026-11-14)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Stripe Payments US** — Domestic cards 2.9% + 30¢; international cards +1.5%; required currency conversion +1%. These are not Korean eligibility or account-specific quotes.  
  source: https://stripe.com/pricing
- **Stripe Billing** — Pay-as-you-go 0.7% of Billing volume.  
  source: https://stripe.com/billing/pricing
- **Stripe Tax Basic US** — No-code 0.5% for applicable registered transactions; API integration 50¢. Alternative integration paths. Tax Complete is separately priced with plan limits.  
  source: https://stripe.com/pricing
- **Lemon Squeezy** — Base 5% + 50¢; subscription +0.5 percentage points; applicable non-US transactions +1.5 and PayPal +1.5. Fee base includes tax. Region-dependent payout fees are separate.  
  source: https://docs.lemonsqueezy.com/help/getting-started/fees
- **Paddle** — Published standard 5% + 50¢ per Checkout transaction, subscriptions included; custom pricing may apply. Do not apply Lemon Squeezy surcharges.  
  source: https://www.paddle.com/pricing
- **Model assumptions** — US standard rates; tax-free total order value; every Stripe charge incurs the selected Tax path; no FX, international, PayPal, refund, dispute or payout fees unless explicitly modeled.  
  source: https://stripe.com/pricing

## Derived arithmetic used in the article (formula printed in the text)

- **1,000 monthly $20 renewals, defined US base model** — Stripe no-code: $580 + $300 + $140 + $100. Stripe API: $580 + $300 + $140 + $500. Lemon Squeezy: 0.055 × $20,000 + $500. Paddle: 0.05 × $20,000 + $500. ⇒ $1,120 / $1,520 / $1,600 / $1,500 respectively; excludes taxes added to the price and other fees.
- **200 monthly $100 renewals, same $20,000 total** — Stripe no-code: $580 + $60 + $140 + $100 = $880. Stripe API: $580 + $60 + $140 + $100 = $880. Lemon Squeezy: $1,100 + $100. Paddle: $1,000 + $100. ⇒ $880 Stripe on either Tax path; $1,200 Lemon Squeezy; $1,100 Paddle under the same assumptions.
- **Tax API path crossover only** — Stripe 0.036P + $0.80. Paddle 0.05P + $0.50: P = $0.30 / 0.014. Lemon Squeezy subscription 0.055P + $0.50: P = $0.30 / 0.019. ⇒ $21.43 versus Paddle, $15.79 versus Lemon Squeezy; neither is a universal crossover.
- **Hypothetical non-US taxed subscription on Lemon Squeezy** — $20 + 20% tax = $24 total; (5% + 0.5% subscription + 1.5% international) × $24 + $0.50 = $2.18. ⇒ $2.18 fee before payout costs; with an additional 1.5-point PayPal fee, $2.54.

## Sources

- https://stripe.com/pricing
- https://stripe.com/billing/pricing
- https://stripe.com/tax/pricing
- https://docs.lemonsqueezy.com/help/getting-started/fees
- https://www.paddle.com/pricing
