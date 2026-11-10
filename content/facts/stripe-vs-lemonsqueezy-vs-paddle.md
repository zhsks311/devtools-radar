# FACT SHEET — stripe-vs-lemonsqueezy-vs-paddle (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Stripe Payments** — 2.9% + 30¢ per successful domestic card charge; +0.5% manually entered; +1.5% international; 1.5% if currency conversion is required  
  source: https://stripe.com/pricing
- **Stripe disputes** — $15.00 per dispute received, $15.00 countered, $15.00 appealed  
  source: https://stripe.com/pricing
- **Stripe ACH** — 0.8% of the amount, $5.00 cap  
  source: https://stripe.com/pricing
- **Stripe Billing** — 0.7% of Billing volume, including transactions processed off Stripe; excludes one-off invoices  
  source: https://stripe.com/billing/pricing
- **Stripe Tax Basic** — 50¢ per transaction where you are registered to collect; each transaction includes 10 calculation API calls, 5¢ each above that  
  source: https://stripe.com/tax/pricing
- **Stripe Tax Complete** — Tiered by registrations, transactions and filings, up to 10+ registrations and 5,000+ transactions; price not printed (quote)  
  source: https://stripe.com/tax/pricing
- **Stripe Tax coverage** — Obligation monitoring, registrations in 90+ countries, calculation on 700+ product types, filings in 90+ countries  
  source: https://stripe.com/tax/pricing
- **Lemon Squeezy** — 5% + 50¢ per transaction, $0/month; ecommerce features free; email marketing free to 500 subscribers  
  source: https://www.lemonsqueezy.com/pricing
- **Lemon Squeezy as MoR** — Takes on the liability of tax collection and calculation and pays the taxes on your behalf  
  source: https://www.lemonsqueezy.com/pricing
- **Paddle** — 5% + 50¢ per Checkout transaction, no monthly fee; custom pricing for products under $10; no lock-in period  
  source: https://www.paddle.com/pricing
- **Paddle inclusions** — Payments, subscriptions, tax and compliance, fraud protection, buyer support and migration inside the 5%  
  source: https://www.paddle.com/pricing

## Derived arithmetic used in the article (formula printed in the text)

- **1,000 subscribers at $20, domestic cards** — Stripe: 2.9% × $20,000 = $580; 1,000 × 30¢ = $300; Billing 0.7% × $20,000 = $140; Tax Basic 1,000 × 50¢ = $500. MoR: 5% × $20,000 = $1,000; 1,000 × 50¢ = $500 ⇒ $1,520 assembled Stripe stack against $1,500 on either merchant of record
- **200 subscribers at $100, same $20,000 of volume** — Stripe: 2.9% × $20,000 = $580; 200 × 30¢ = $60; 0.7% × $20,000 = $140; 200 × 50¢ = $100. MoR: 5% × $20,000 = $1,000; 200 × 50¢ = $100 ⇒ $880 on Stripe against $1,100 on a merchant of record, a $220 monthly premium
- **Break-even price per charge** — 3.6% × P + $0.80 = 5% × P + $0.50, so 1.4% × P = $0.30 and P = $21.43 ⇒ Above $21.43 a charge the assembled stack is cheaper; below it the merchant of record is
- **A $9 product on a merchant of record** — 5% × $9 = $0.45, plus $0.50 fixed = $0.95 per sale; $0.95 ÷ $9 = 10.6% ⇒ $0.95 of a $9 sale, with half of it coming from the fixed fee alone

## Sources

- https://stripe.com/pricing
- https://stripe.com/billing/pricing
- https://stripe.com/tax/pricing
- https://www.lemonsqueezy.com/pricing
- https://www.paddle.com/pricing
