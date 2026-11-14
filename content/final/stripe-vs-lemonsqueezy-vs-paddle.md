# Stripe vs Lemon Squeezy / Paddle — a 2026 cost teardown

> For 1,000 monthly $20 subscriptions, the modeled fees are $1,120 on Stripe with no-code Tax, $1,520 with Tax API, $1,600 on Lemon Squeezy and $1,500 on Paddle. The integration path and subscription surcharge change the ranking.

*Prices verified 2026-11-14. Category: Payments & Billing. Author: DevTeardown Team.*

## Verdict

There is no single merchant-of-record invoice. In the defined $20 subscription model, Stripe no-code Tax costs $1,120, Stripe Tax API $1,520, Lemon Squeezy $1,600 and Paddle $1,500. Choose using the actual integration, country, tax base and service scope, not the shared 5% headline.

## 1. Start with a defined account and checkout

These are standard US Stripe card rates, not a quote for a Korean business. Eligibility, negotiated contracts, tax treatment and settlement currency must be checked before choosing a provider.

| Stripe component | Published rate | Scope |
|---|---|---|
| Domestic cards | 2.9% + 30¢ | successful charge |
| International cards | +1.5% | applicable international cards |
| Currency conversion | +1% | when conversion is required |
| Billing pay-as-you-go | 0.7% | Billing volume |
| Tax Basic no-code | 0.5% | registered transactions |
| Tax Basic API | 50¢ | registered transactions |

No-code Tax applies to integrations such as Checkout and Billing. The API price is a different integration path, not a fee to add to the no-code rate. Registration, filing and optional services need their own budget.

## 2. The two merchants have different fee rules

Lemon Squeezy and Paddle advertise a base 5% + 50¢, but that does not make their subscription invoices identical.

- Lemon Squeezy adds 0.5 percentage points for subscriptions, 1.5 for applicable non-US transactions and 1.5 for PayPal. Its fee uses the total order value, including tax.
- Paddle advertises 5% + 50¢ per Checkout transaction with subscriptions included. Do not copy Lemon Squeezy surcharges onto Paddle.
- Account-specific pricing, payouts and optional services can change either result.

A merchant of record handles covered transaction tax obligations as the seller. That is not a promise that your business has no income-tax, reporting or other legal obligations. Compare the service scope as well as the checkout fee.

## 3. Four invoices for the same subscription volume

Assume 1,000 successful $20 renewals: $20,000 charged, no added tax, refunds, disputes, FX or payout fees. Use US domestic cards for Stripe and no international or PayPal surcharge for Lemon Squeezy; assume every transaction incurs the chosen Tax Basic fee.

| Provider / path | Arithmetic | Total |
|---|---|---|
| Stripe + no-code Tax | $580 + $300 Payments + $140 Billing + $100 Tax | $1,120 |
| Stripe + Tax API | $580 + $300 + $140 + $500 | $1,520 |
| Lemon Squeezy subscription | 5.5% × $20,000 + 1,000 × $0.50 | $1,600 |
| Paddle standard | 5% × $20,000 + 1,000 × $0.50 | $1,500 |

Correction, November 14: the earlier $1,500 Lemon Squeezy subscription example omitted its surcharge. The old universal $21.43 crossover also assumed the Tax API path and Paddle's base rate, not every subscription setup.

## 4. Country and tax change the denominator

Use the actual checkout total, not just the advertised product price. A hypothetical $20 subscription with 20% tax creates a $24 order; if Lemon Squeezy's non-US surcharge applies, its fee is 7% × $24 + $0.50 = $2.18, before payout costs.

| Change from the base model | Consequence |
|---|---|
| Lemon Squeezy non-US subscription | 7% + 50¢; PayPal can add another 1.5 points |
| Stripe international card | add 1.5 points to its applicable stack |
| Stripe FX conversion | add 1 point when required |
| Tax-inclusive versus tax-exclusive price | calculate from the actual fee base |

Lemon Squeezy also documents region-dependent payout fees. These are separate from checkout fees and excluded from the worked totals. Paddle's own contract and payout terms must be evaluated separately; a foreign buyer alone does not establish which provider wins.

## 5. The crossover belongs to one set of assumptions

With the same tax-free US model, Stripe plus no-code Tax is 4.1% × P + $0.30 per charge, lower than both modeled MoR fees at every positive P. With Tax API it is 3.6% × P + $0.80.

- Against Paddle: $0.30 / (5% − 3.6%) = $21.43.
- Against a Lemon Squeezy subscription: $0.30 / (5.5% − 3.6%) = $15.79.
- A $9 Lemon Squeezy subscription costs $0.995 before other fees, not the $0.95 base one-time illustration.

Those are processing comparisons, not total operating costs. Neither result prices engineering, tax registration, filing, buyer support or risk. A cheaper fee model can still be the more expensive business process.

## 6. Choose the service before trusting the headline

For Stripe Payments with Billing, you remain the seller. Tax Basic is calculation and collection tooling; Tax Complete offers a separate registration and filing service with its own plans and limits. Stripe also markets Managed Payments as a distinct MoR product, which is outside these calculations.

For a covered Paddle or Lemon Squeezy sale, the provider is the merchant of record. Approval, product eligibility, refunds, chargebacks, payout timing and reserves still matter.

- Confirm the business and bank country are supported.
- Obtain the applicable rate card and test a representative receipt.
- Model the real card mix, tax totals and average charge.
- Check migration and data portability with both providers before committing.

A checkout demo is not proof of live eligibility or settlement. None of the examples establishes that a Korean account will be approved or receive the modeled net amount.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 1,000 monthly $20 renewals, defined US base model | Stripe no-code: $580 + $300 + $140 + $100. Stripe API: $580 + $300 + $140 + $500. Lemon Squeezy: 0.055 × $20,000 + $500. Paddle: 0.05 × $20,000 + $500. | $1,120 / $1,520 / $1,600 / $1,500 respectively; excludes taxes added to the price and other fees. |
| 200 monthly $100 renewals, same $20,000 total | Stripe no-code: $580 + $60 + $140 + $100 = $880. Stripe API: $580 + $60 + $140 + $100 = $880. Lemon Squeezy: $1,100 + $100. Paddle: $1,000 + $100. | $880 Stripe on either Tax path; $1,200 Lemon Squeezy; $1,100 Paddle under the same assumptions. |
| Tax API path crossover only | Stripe 0.036P + $0.80. Paddle 0.05P + $0.50: P = $0.30 / 0.014. Lemon Squeezy subscription 0.055P + $0.50: P = $0.30 / 0.019. | $21.43 versus Paddle, $15.79 versus Lemon Squeezy; neither is a universal crossover. |
| Hypothetical non-US taxed subscription on Lemon Squeezy | $20 + 20% tax = $24 total; (5% + 0.5% subscription + 1.5% international) × $24 + $0.50 = $2.18. | $2.18 fee before payout costs; with an additional 1.5-point PayPal fee, $2.54. |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| US domestic subscriptions with Checkout Tax | Model Stripe no-code Tax separately | The 0.5% path produces $1,120 here, not the $1,520 Tax API total. |
| A custom Tax API integration | Compare all three invoices | At $20, Stripe is $1,520, Paddle $1,500 and Lemon Squeezy $1,600 under the base assumptions. |
| Non-US buyers or PayPal subscriptions | Use the applicable surcharges | Lemon Squeezy lists additional fees; do not reuse the US base total or transfer its rules to Paddle. |
| A team without transaction-tax operations | Evaluate an approved MoR | Covered tax handling can justify a higher fee, but business reporting and eligibility still require review. |
| Very small average charges | Request applicable low-value pricing | The fixed 50¢ component weighs heavily; custom rates must be confirmed, not assumed. |
| A Korean business seeking payouts | Verify eligibility and settlement first | US rate arithmetic does not establish Korean onboarding, payout currency, timing or buyer-visible details. |

## Migration path

Ask both providers to confirm supported subscription and payment-data migration, required customer consent, settlement reconciliation and historical tax-record handling before scheduling a move. Do not assume either automatic portability or that every customer must re-enter a card. Run a small approved migration test before moving active renewals; retaining access to old records does not transfer earlier obligations.

## Questions that change the decision

**Is 5% + 50¢ the full subscription fee on both MoRs?**  
No. Lemon Squeezy adds 0.5 percentage points for subscriptions and may add international and PayPal fees. Paddle advertises subscriptions within its standard 5% + 50¢ rate. Check each account contract and payout costs separately.

**Does Stripe Tax always cost 50¢ per transaction?**  
No. The US Tax Basic page distinguishes 0.5% no-code integrations from a 50¢ API integration charge for applicable registered transactions. They are alternative paths, not two fees to add together.

**What changes the international comparison?**  
Stripe lists +1.5% for international cards and +1% when currency conversion is required. Lemon Squeezy lists +1.5% for applicable non-US transactions and +1.5% for PayPal. Tax-inclusive order totals and payout costs also matter.

**Do these calculations prove Korean eligibility or remove all tax duties?**  
No. Verify supported business and bank countries, account approval, settlement and legal obligations. MoR transaction-tax handling is not a blanket exemption from the seller business’s own taxes or reporting.

## Sources

- https://stripe.com/pricing
- https://stripe.com/billing/pricing
- https://stripe.com/tax/pricing
- https://docs.lemonsqueezy.com/help/getting-started/fees
- https://www.paddle.com/pricing

## Same task, two SDKs

**Stripe**

```
// Pricing illustration only; not a live account configuration.
const gross = 20000;
const charges = 1000;
const payments = gross * 0.029 + charges * 0.30;
const billing = gross * 0.007;
const noCodeTax = gross * 0.005;
const apiTax = charges * 0.50;
console.log(payments + billing + noCodeTax); // 1120
console.log(payments + billing + apiTax); // 1520
// Assumes every charge incurs Tax; do not add both Tax paths.
```

**Lemon Squeezy / Paddle**

```
// Same tax-free US base model, no added international/PayPal fees.
const gross = 20000;
const charges = 1000;
const lemon = gross * (0.05 + 0.005) + charges * 0.50;
const paddle = gross * 0.05 + charges * 0.50;
console.log(lemon, paddle); // 1600, 1500
// Not interchangeable rate cards. Payout and other costs excluded.
```
