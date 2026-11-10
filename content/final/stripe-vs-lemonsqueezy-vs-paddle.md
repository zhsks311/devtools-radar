# Stripe vs Lemon Squeezy / Paddle — a 2026 cost teardown

> A thousand subscribers at $20 a month pay $1,520 on an assembled Stripe stack and $1,500 on a merchant of record. The vendor everyone calls expensive is the cheaper one at the price point most SaaS products actually charge.

*Prices verified 2026-11-10. Category: Payments & Billing. Author: DevTeardown Team.*

## Verdict

Below roughly $21 per charge, or on any card that is not domestic, the merchant of record is the cheaper invoice, not the expensive one. Above it, the assembled Stripe stack wins on price and only on price: the moment you are not doing the registrations and filings yourself, the two points you saved are paying for work you still owe.

## 1. The sticker price is one of four meters you will pay

Stripe's pricing page prints one number: 2.9% + 30¢ for a domestic card. A subscription business pays that plus three more.

| Meter | Price | Applied when |
|---|---|---|
| Domestic card | 2.9% + 30¢ | every successful charge |
| International card | +1.5% | the card is issued outside your country |
| Currency conversion | +1.5% | the charge is not in your settlement currency |
| Billing | 0.7% of Billing volume | subscriptions, processed on or off Stripe |
| Tax Basic | 50¢ per transaction | you are registered to collect there |
| ACH direct debit | 0.8%, $5 cap | bank debits |
| Dispute | $15.00 | each chargeback received |

None of those lines is hidden. Each one has its own page, which is how a 2.9% product becomes a 3.6% + 80¢ product by the end of the month.

## 2. A merchant of record sells a different invoice, not a cheaper one

Lemon Squeezy and Paddle both publish 5% + 50¢ per transaction and $0 per month. They also publish the same sentence in different words: they are the seller.

That moves who owns the tax question. On Stripe you are the merchant, so the VAT number, the filing deadline and the penalty for missing it are yours. On either merchant of record the receipt carries their name and you receive a net payout.

- **Lemon Squeezy:** 5% + 50¢ per transaction, $0 monthly, and sales tax or VAT collection where it is the merchant of record, with the liability taken on.
- **Paddle:** 5% + 50¢ per Checkout transaction, no monthly fee, and custom pricing for products under $10.
- Neither fee moves when you add a country to your tax map. That is the product.

The question is not which percentage is smaller. It is whether the extra points cost less than the paperwork you would otherwise do yourself.

## 3. At $20 a month the assembled stack loses by $20

Take 1,000 subscribers at $20, all domestic cards, $20,000 of volume, and assume you are registered to collect tax everywhere you sell. If you are not, the Tax line is smaller and the Stripe stack cheaper.

| Line | Assembled Stripe stack | Merchant of record |
|---|---|---|
| Payments | 2.9% × $20,000 = $580, plus 1,000 × 30¢ = $300 | — |
| Billing | 0.7% × $20,000 = $140 | — |
| Tax Basic | 1,000 × 50¢ = $500 | — |
| Single fee | — | 5% × $20,000 = $1,000, plus 1,000 × 50¢ = $500 |
| **Total** | **$1,520** | **$1,500** |

Move the price to $100 and keep the same $20,000: Stripe bills $580 + $140 + $160 = $880, the merchant of record bills $1,000 + $100 = $1,100. The crossover is one equation: 3.6% × P + 80¢ = 5% × P + 50¢, so 1.4% × P = 30¢, and P = $21.43.

## 4. International-card fees remove this modeled crossover

1.5% for an international card turns 3.6% + 80¢ into 5.1% + 80¢. The modeled gap against 5% + 50¢ is 0.1% × P + 30¢, always positive. Correction: the earlier $300 crossover used the wrong sign.

| Card | Stripe stack | Merchant of record | Cheaper |
|---|---|---|---|
| Domestic | 3.6% + 80¢ | 5% + 50¢ | Stripe above $21.43 |
| International | 5.1% + 80¢ | 5% + 50¢ | MoR at every positive price in this model |
| International, non-USD | 6.6% + 80¢ | 5% + 50¢ | MoR at every price |

The third row is the one people miss. A euro customer paying with a euro card costs 6.6% + 80¢, which is more than the fee that supposedly includes filing for thirty countries. Currency conversion is charged on top of the international card fee, so both can land on one charge.

## 5. What the extra points buy, and what they take

For the fee you get fraud screening, chargeback handling, buyer support and the remittance itself. Paddle lists payments, subscriptions, tax, fraud protection and billing support inside the 5%. Lemon Squeezy lists the same set and states the liability plainly: it takes on tax collection and pays the taxes on your behalf.

The cost is control:

- You do not hold the merchant account, so the acquirer relationship and the risk decision are theirs.
- Refund and chargeback conversations belong to their support queue, not yours.
- Leaving means moving subscribers, and Paddle sells that as a migration service rather than a button.

Stripe's answer is Tax Complete, which monitors thresholds, registers in 90+ countries and files returns. It is priced in tiers by registrations, transactions and filings, and the tiers are a quote rather than a number on the page.

## 6. Where each one breaks

Stripe breaks at the first country you sell into without registering. Tax Basic tells you the tax is due and meters 50¢ once you are registered; it does not register you, and back taxes plus penalties appear on no price sheet.

The merchant of record breaks on the fixed fee. 50¢ is 5.6% of a $9 product, so a $9 sale keeps $8.05 before hosting. Paddle's own FAQ routes products under $10 to custom pricing, which is the same admission in a politer sentence.

It breaks again at the top, because 5% never thins out. A $200,000 month split into 1,000 charges of $200 pays $10,000 + $500 on a merchant of record and $7,200 + $800 on the assembled stack, a $30,000 gap across a year.

Price three things before you choose: your average charge, the share of cards that are not domestic, and whether anyone on the team has filed a VAT return.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 1,000 subscribers at $20, domestic cards | Stripe: 2.9% × $20,000 = $580; 1,000 × 30¢ = $300; Billing 0.7% × $20,000 = $140; Tax Basic 1,000 × 50¢ = $500. MoR: 5% × $20,000 = $1,000; 1,000 × 50¢ = $500 | $1,520 assembled Stripe stack against $1,500 on either merchant of record |
| 200 subscribers at $100, same $20,000 of volume | Stripe: 2.9% × $20,000 = $580; 200 × 30¢ = $60; 0.7% × $20,000 = $140; 200 × 50¢ = $100. MoR: 5% × $20,000 = $1,000; 200 × 50¢ = $100 | $880 on Stripe against $1,100 on a merchant of record, a $220 monthly premium |
| Break-even price per charge | 3.6% × P + $0.80 = 5% × P + $0.50, so 1.4% × P = $0.30 and P = $21.43 | Above $21.43 a charge the assembled stack is cheaper; below it the merchant of record is |
| A $9 product on a merchant of record | 5% × $9 = $0.45, plus $0.50 fixed = $0.95 per sale; $0.95 ÷ $9 = 10.6% | $0.95 of a $9 sale, with half of it coming from the fixed fee alone |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| Average charge under $21 and a team of one | Lemon Squeezy or Paddle | At $20 the single 5% + 50¢ meter bills $1,500 against $1,520 for the assembled Stripe stack, and nobody has to register for VAT. |
| Average charge over $21, mostly domestic cards | Stripe | The crossover is 1.4% × P = 30¢, so from $21.43 upward the four Stripe meters total less than one merchant-of-record fee. |
| Selling into the EU and UK from day one | Lemon Squeezy or Paddle | An international non-USD card costs the Stripe stack 6.6% + 80¢, which is more than the merchant-of-record fee that includes the filings. |
| Enterprise buyers who want invoices, POs and net terms | Stripe | Invoicing and Billing sit on the same account, and the 0.7% Billing rate excludes one-off invoices. |
| A marketplace that pays out to sellers | Stripe | Neither merchant-of-record price sheet covers paying out to third-party sellers; the 5% + 50¢ is a single-seller fee. |
| Products priced under $10 | Paddle, at custom pricing | The 50¢ fixed fee is 5.6% of a $9 sale, and Paddle's FAQ sends sub-$10 products to a bespoke rate instead of the public one. |
| $200,000 months with $200 charges | Stripe | The percentage never falls on a merchant of record: that month pays $10,500 there against $8,000 on the assembled stack. |
| Nobody on the team has ever filed a VAT return | A merchant of record | Tax Basic meters 50¢ per registered transaction but does not register you; the registrations and filings are the part you are buying. |

## Migration path

Leaving a merchant of record means moving subscribers, and there is no card-data path between the two: cards stored with the merchant of record do not transfer, so each customer either re-enters payment details or you run both systems until the next renewal. Product and price objects are recreated on the other side, and historical tax filings stay with whoever made them. Paddle sells this as a migration service; on Stripe the same move is exports plus a dunning sequence you write.

Going the other way, from Stripe to a merchant of record, the tax history is the part that does not travel. You keep the records, the new merchant registers where it needs to, and the previous filings remain your responsibility for the periods you owned them.

## Questions that change the decision

**Does the 5% + 50¢ include payment processing?**  
Yes. Both pages describe one all-in fee covering payments, checkout, subscriptions, tax collection, fraud screening and buyer support, with no monthly fee on top.

**Is Stripe Tax the same thing as a merchant of record?**  
No. Tax Basic calculates and collects tax where you are registered and meters 50¢ per transaction. Registration and filing are yours unless you buy Tax Complete, which is tiered and quoted.

**What does an international card add on Stripe?**  
1.5% on top of 2.9% + 30¢, and currency conversion is a separate 1.5% when the charge is not in your settlement currency.

**Can a merchant of record refuse a product?**  
It is the seller named on the receipt, so what it will and will not sell is its decision to make. That approval is part of what the 5% covers.

## Sources

- https://stripe.com/pricing
- https://stripe.com/billing/pricing
- https://stripe.com/tax/pricing
- https://www.lemonsqueezy.com/pricing
- https://www.paddle.com/pricing

## Same task, two SDKs

**Stripe**

```
// Stripe: you are the seller, so the tax switch is yours to get wrong.
import Stripe from "stripe";
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  line_items: [{ price: process.env.PRICE_20_MONTHLY, quantity: 1 }],
  automatic_tax: { enabled: true }, // 50¢ per transaction once registered
  customer_update: { address: "auto" },
  success_url: "https://app.example.com/ok?session={CHECKOUT_SESSION_ID}",
  cancel_url: "https://app.example.com/pricing",
});
// Breaks when: automatic_tax is on and you never registered in the buyer's country.
// No tax is collected, the liability stays yours, and the invoice still looks right.
```

**Lemon Squeezy / Paddle**

```
// Paddle: the tax never becomes your line item, but the webhook is the billable event.
import { Paddle, Environment } from "@paddle/paddle-node-sdk";
const paddle = new Paddle(process.env.PADDLE_API_KEY, {
  environment: Environment.production,
});

const transaction = await paddle.transactions.create({
  items: [{ priceId: process.env.PRICE_20_MONTHLY, quantity: 1 }],
  customData: { account_id: "acc_123" },
});
// Breaks when: you grant access from this response. The transaction is not the
// subscription; only the subscription webhook says the 5% + 50¢ was collected.
return transaction.id;
```
