# Resend vs SendGrid — a 2026 cost teardown

> At 100,000 emails a month, Resend's Pro plan is $35 and SendGrid's Essentials plan is $34.95. Both vendors then charge exactly $55 more for the next rung, and none of that $55 buys an extra email: it buys the tier where a dedicated IP becomes possible.

*Prices verified 2026-11-10. Category: Email Infrastructure. Author: DevTeardown Team.*

## Verdict

Under 50,000 emails the two vendors are the same product at the same price, and the free tier is the only real difference. Past 100,000 the choice is decided by one feature: SendGrid includes a dedicated IP at $89.95, Resend sells it for $30 on a plan that already costs $90. If you need an IP, SendGrid; if you need a free tier and a clean API, Resend; if you need volume, check the rung and the overage before either.

## 1. At 100,000 emails, both vendors charge $55 for the same feature

Resend splits its ladder at 100,000 emails, where the plan name changes: Pro is $20 for 50,000 and $35 for 100,000, while Scale starts at $90 for that same 100,000. The $55 difference buys no volume at all.

SendGrid splits the same way: Essentials is $19.95 for 50,000 emails and $34.95 for 100,000, and Pro is $89.95 for the identical 100,000. The difference is $55.00, to the cent.

| At 100,000 emails | Cheap tier | Feature tier | Difference |
|---|---|---|---|
| Resend | Pro $35.00 | Scale $90.00 | $55.00 |
| SendGrid | Essentials $34.95 | Pro $89.95 | $55.00 |

Two vendors that share no code and no pricing page arrived at the same step, at the same volume, for the same reason: at 100,000 emails the feature gates are what the plan is priced on, not the sending.

## 2. The ladder is not monotonic, and overage is sometimes the cheaper rung

Read each ladder as cost per 1,000, not as a monthly price.

| Volume needed | Resend | Per 1,000 | SendGrid | Per 1,000 |
|---|---|---|---|---|
| 50,000 | $20.00 (50k) | $0.40 | $19.95 (50k) | $0.40 |
| 100,000 | $35.00 (100k Pro) | $0.35 | $34.95 (100k Essentials) | $0.35 |
| 200,000 | $160.00 (200k) | $0.80 | $249.00 (300k) | $1.25 |
| 500,000 | $350.00 (500k) | $0.70 | $499.00 (700k) | $1.00 |
| 1,000,000 | $650.00 (1M) | $0.65 | $799.00 (1.5M) | $0.80 |
| 2,500,000 | $1,150.00 (2.5M) | $0.46 | $1,099.00 (2.5M) | $0.44 |

Where one vendor has no rung at that volume, the column shows the cheapest rung that covers it, which is why SendGrid's 200,000 row is its 300,000 plan.

Resend's 200,000 rung costs $0.80 per 1,000, more than twice its 100,000 rung. That is not a discount curve; it is a plan boundary, and the cheaper block stops at 100,000.

Overage repairs it. Resend charges $0.90 per 1,000 beyond the included volume, so 100,000 on Pro plus 100,000 of overage is $35 + $90 = $125, not $160. SendGrid's same move on Pro is $89.95 + 100,000 × $1.10/1,000 = $199.95, not $249.

## 3. Dedicated IP: $30 plus a $55 step, or included at $89.95

A dedicated IP is the feature that decides most of these purchases, because shared IP reputation is the thing a growing sender cannot control.

Resend sells it as a $30 per month add-on, and only on Scale, to accounts sending more than 3,000 emails a day. At 100,000 emails that is $90 + $30 = $120, or $1.20 per 1,000.

SendGrid includes one dedicated IP in Pro, which is $89.95 at the same volume, or $0.90 per 1,000.

| 100,000 emails with a dedicated IP | Monthly | Per 1,000 |
|---|---|---|
| Resend Scale + IP add-on | $120.00 | $1.20 |
| SendGrid Pro | $89.95 | $0.90 |

There is no Resend Pro path to an IP at any price. That is not a worse deal; it is a missing SKU, and it decides the vendor for anyone whose deliverability depends on one.

## 4. Domain authentication is table stakes; the domain count is not

Both authenticate sending with DKIM, SPF and DMARC, and both include a REST API, SMTP relay and official SDKs on every paid plan. The differences are in the quantities.

| Quantity | Resend | SendGrid |
|---|---|---|
| Custom domains | 3 Free, 10 Pro, 1,000 Scale | Domain authentication included |
| Extra domains | $20/mo adds 100 | Not a listed line item |
| Teammates | Not metered | 1 on Essentials, 1,000 on Pro |
| Event webhooks | 5 on Pro, 10 on Scale | 2 on Essentials, 5 on Pro |
| SSO | $150/mo add-on on Scale | Included in Pro |

An agency managing dozens of client domains should price the domain line before the email line: Resend's add-on covers 100 extra domains for $20, and SendGrid's inclusion has no printed ceiling.

## 5. The bottom of the market is where they stop competing

Resend keeps a free plan: 3,000 emails a month, 100 a day, three domains, 30 days of data retention. SendGrid's free option is a 60-day trial at 100 emails a day, after which the account converts to a paid plan starting at $19.95.

That single difference moves a whole segment. A side project, a staging environment or a low-volume notification service runs at $0 on Resend and at $19.95 on SendGrid, and the gap is $239.40 a year before either vendor has been compared on anything else.

It also sets the frame for the first paid tier: $20 on Resend buys 50,000 emails, more than sixteen times what its own free plan allowed, and the same 50,000 that SendGrid now sells as its smallest paid plan.

## 6. Where each one breaks

Resend breaks on the feature boundary. The dedicated IP, SSO and 1,000 domains all sit on Scale, so the 100,000-email customer who outgrows Pro pays a $55 step and then $30 more for the IP. Marketing email moves to a separate contact-priced plan, and broadcasts only reach existing contacts.

SendGrid breaks on the tier edge and on history. The 50,000 Essentials tier charges $1.33 per 1,000 beyond its volume, so 80,000 emails bills $19.95 + $39.90 = $59.85 against $34.95 for the next tier up. Searchable activity is 3 days on Essentials against 7 on Pro, so a deliverability investigation can outlast the evidence.

Check three numbers before choosing: your monthly volume rounded up to the rung that covers it, whether you need an IP this quarter, and how many domains you will authenticate in a year.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 100,000 emails a month, no dedicated IP | Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000 | $35.00 against $34.95, a five-cent gap at the bottom of the ladder |
| 200,000 emails a month, the rung against the overage | Resend: 100,000 Pro at $35 + 100,000 × $0.90/1,000 = $125, against the Scale 200,000 rung at $160. SendGrid: $89.95 + 100,000 × $1.10/1,000 = $199.95, against the Pro 300,000 rung at $249 | $125 on Resend and $199.95 on SendGrid, both cheaper than buying the next rung |
| Overage break-even on the 50,000 tiers | Resend: $20 + $0.90 per 1,000 over 50,000 equals $35 at 16,666 extra emails, so 66,666. SendGrid: $19.95 + $1.33 per 1,000 equals $34.95 at 11,278 extra, so 61,278 | Past roughly 61,000 to 67,000 sends the next tier is cheaper than the overage |
| The same feature at the same volume | Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 including one dedicated IP | $120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 monthly difference |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| Transactional email only, under 50,000 a month | Either | $20 on Resend and $19.95 on SendGrid buy the same volume, and the five-cent gap is not a reason to migrate. |
| You need a dedicated IP at 100,000 emails | SendGrid Pro | $89.95 includes one IP, against $90 for Resend Scale plus $30 for the add-on, and Resend Pro cannot buy an IP at all. |
| A free tier is mandatory for staging | Resend | Resend's free plan sends 3,000 a month, while SendGrid's free option is a 60-day trial and then $19.95. |
| Agencies authenticating dozens of client domains | Resend Scale, with the domain add-on | 1,000 domains are included on Scale and $20 adds 100 more, against a domain line SendGrid does not print. |
| SSO and an IP at 500,000 emails | SendGrid Pro | SSO is included in Pro and so is one IP, while Resend puts SSO at $150 a month and the IP at $30 on top of Scale. |
| 2,500,000 emails a month and nothing exotic | SendGrid Pro | $1,099 against $1,150 on Resend, and the gap widens with the IP add-on that Resend needs for the same setup. |
| Marketing broadcasts to a contact list | Resend marketing plans | Marketing is priced per contact rather than per email, so an unlimited number of sends to 10,000 contacts is $80. |
| Volume swings month to month | Either, with an alert at 60,000 | Both overage rates are more expensive than the next rung: the break-even is about 61,000 on SendGrid and 67,000 on Resend. |

## Migration path

Both vendors authenticate a domain with DKIM, SPF and DMARC records, so moving means adding new DNS records while the old ones still answer. Keep both authenticated for a week, warm the new domain or IP, then flip the sending domain in code.

The parts that do not travel are templates and reputation. React Email templates are code and move with the repository; SendGrid's dynamic templates are vendor objects. A dedicated IP starts cold on either side, so a sender who relies on one should plan the warm-up as a week of projected volume rather than a switch.

## Questions that change the decision

**Does Resend sell a dedicated IP on Pro?**  
No. The $30 per month add-on is listed for Scale plans, to accounts sending more than 3,000 emails a day. Pro has no IP option.

**What does SendGrid's free plan include now?**  
A 60-day trial at 100 emails a day, with no credit card. After it ends the account moves to a paid plan, and Essentials starts at $19.95 for 50,000 emails.

**Is overage cheaper than buying the next tier?**  
Usually not. Overage on the 50,000 tiers is $1.33 per 1,000 on SendGrid and $0.90 on Resend, both far above the next tier's per-1,000 rate, so the break-even arrives at 61,000 to 67,000 sends.

**Do both include inbound email parsing?**  
Resend lists inbound email with webhooks on every plan, and SendGrid lists an Inbound Parse webhook as part of the Email API feature set.

## Sources

- https://resend.com/pricing
- https://www.twilio.com/en-us/products/email-api/pricing
- https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
- https://resend.com/docs
- https://www.twilio.com/docs/sendgrid

## Same task, two SDKs

**Resend**

```
// Resend: the idempotency key is what stops a retry from sending twice.
import { Resend } from "resend";
const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send(
  {
    from: "billing@example.com",
    to: order.email,
    subject: `Receipt for ${order.id}`,
    react: Receipt({ order }),
  },
  { idempotencyKey: `receipt-${order.id}` },
);
// Breaks when: the key is built from Date.now(). A retry after a 429 is then a
// second email, and there is no deduplication on the receiving side.
```

**SendGrid**

```
// SendGrid: categories are the only cheap way to separate streams in the event webhook.
import sgMail from "@sendgrid/mail";
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

await sgMail.send({
  to: order.email,
  from: "billing@example.com",
  templateId: "d-receipt-v3",
  dynamicTemplateData: { orderId: order.id, total: order.total },
  categories: ["receipt", `region-${order.region}`],
  customArgs: { order_id: order.id }, // echoed in the event webhook
});
// Breaks when: the template renders a total without a currency. The API accepts it,
// the receipt is wrong, and the event webhook reports a delivered message.
```
