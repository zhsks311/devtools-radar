# Resend vs SendGrid — a 2026 cost teardown

> Resend and SendGrid offer similar entry prices, but trial expiry and overage billing change the bill. Resend’s paid overages need opt-in and round up in 1,000-email buckets. A standard SendGrid trial ends with sending paused, not an automatic paid subscription.

*Prices verified 2026-11-14. Category: Email Infrastructure. Author: DevTeardown Team.*

## Verdict

For a small service within 3,000 emails a month and 100 a day, Resend offers an ongoing free option. A standard new direct SendGrid account has a 60-day trial, not automatic paid conversion: sending stops unless you upgrade. Paid-plan selection needs both volume and features. Resend overages require opt-in and round up in 1,000-email buckets; do not budget them as a per-email charge.

## 1. At 100,000 emails, the feature tiers cost more

The listed 100,000-email tiers have a $55 feature-tier step, not an increase in included volume. This does not make the feature bundles equivalent or establish why either vendor set its prices.

| At 100,000 emails | Entry tier | Feature tier | Difference |
|---|---|---|---|
| Resend | Pro $35 | Scale $90 | $55 |
| SendGrid | Essentials $34.95 | Pro $89.95 | $55 |

All figures here are USD monthly estimates before taxes and add-ons. Check your actual account quote, especially for reseller or custom-contract plans.

## 2. The ladder is not monotonic, and overage is sometimes the cheaper rung

Resend paid transactional plans can opt into Transactional Overages in Settings; Free cannot. Without opt-in, quota limits apply rather than this paid continuation.

Formula: base + ceil(max(0, usage − quota) / 1,000) × plan bucket rate. At $20 for 50,000 and $0.90 per extra bucket:

| Monthly usage | Rounded extra buckets | Total |
|---|---|---|
| 50,003 | 1 | $20.90 |
| 51,415 | 2 | $21.80 |
| 66,000 | 16 | $34.40 |
| 66,001 | 17 | $35.30 |

The $35/100,000 tier first becomes cheaper at 66,001 emails, not 66,666. Count all usage charged to the quota, not just outbound messages; taxes and other fees are extra.

With opt-in, the listed $35/100,000 plan plus 100 extra buckets totals $125 for 200,000 emails, below the $160 Scale tier but without its features. Do not apply Resend’s rounding or activation rule to SendGrid.

## 3. Dedicated IP: $30 plus a $55 step, or included at $89.95

A dedicated IP may matter for a sustained high-volume sender, but it does not by itself guarantee better delivery. Choose it based on sending patterns and operational needs.

Resend sells it as a $30 per month add-on, and only on Scale, to accounts sending more than 3,000 emails a day. At 100,000 emails that is $90 + $30 = $120, or $1.20 per 1,000.

SendGrid includes one dedicated IP in Pro, which is $89.95 at the same volume, or $0.90 per 1,000.

| 100,000 emails with a dedicated IP | Monthly | Per 1,000 |
|---|---|---|
| Resend Scale + IP add-on | $120.00 | $1.20 |
| SendGrid Pro | $89.95 | $0.90 |

There is no Resend Pro path to an IP in the listed self-service tiers. That is not a worse deal; it is a missing SKU, and it decides the vendor for anyone whose deliverability depends on one.

## 4. Domain authentication is table stakes; the domain count is not

Both authenticate sending with DKIM, SPF and DMARC, and both include a REST API, SMTP relay and official SDKs on every paid plan. The differences are in the quantities.

| Quantity | Resend | SendGrid |
|---|---|---|
| Custom domains | 3 Free, 10 Pro, 1,000 Scale | Domain authentication included |
| Extra domains | $20/mo adds 100 | Not a listed line item |
| Teammates | Not metered | 1 on Essentials, 1,000 on Pro |
| Event webhooks | 5 on Pro, 10 on Scale | 2 on Essentials, 5 on Pro |
| SSO | $150/mo add-on on Scale | Included in Pro |

Resend retains idempotency keys for 24 hours only. Same-key retries require the identical payload. A 409 payload conflict needs correction; a concurrent request needs bounded backoff. Keep durable send state and reconcile ambiguous outcomes after long outages, not blind resends.

## 5. A trial ending is not an automatic subscription

Correction, November 14, 2026: the earlier article wrongly described automatic SendGrid paid conversion and continuous per-email Resend overage billing. The calculations and FAQ are corrected.

A standard new direct SendGrid/Twilio Email API account gets a 60-day trial at 100 emails/day. After expiry, sending stops unless you choose a paid upgrade; the trial does not itself trigger a $19.95 charge. Email API and Marketing Campaigns are separate plans.

Partner/reseller accounts such as Azure can differ: check actual terms and notices. Older direct free accounts are not a guaranteed exemption; Twilio announced their retirement in May 2025 with a transition to paused sending absent upgrade. Already-paid subscriptions follow their own terms.

Resend’s free tier allows 3,000 emails/month and 100/day. $19.95 × 12 = $239.40 represents twelve voluntarily purchased SendGrid months, not a trial-expiry bill or a first year including the trial.

## 6. Where each one breaks

Resend breaks on the feature boundary. The dedicated IP, SSO and 1,000 domains all sit on Scale, so the 100,000-email customer who outgrows Pro pays a $55 step and then $30 more for the IP. Marketing email moves to a separate contact-priced plan, and broadcasts only reach existing contacts.

SendGrid breaks on the tier edge and on history. The 50,000 Essentials tier charges $1.33 per 1,000 beyond its volume, so 80,000 emails bills $19.95 + $39.90 = $59.85 against $34.95 for the next tier up. Searchable activity is 3 days on Essentials against 7 on Pro, so a deliverability investigation can outlast the evidence.

Check three numbers before choosing: your monthly volume rounded up to the rung that covers it, whether you need an IP this quarter, and how many domains you will authenticate in a year.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 100,000 emails a month, no dedicated IP | Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000 | $35.00 against $34.95, a five-cent gap at the bottom of the ladder |
| 200,000 emails a month, the rung against the overage | Eligible Resend paid plan with Transactional Overages enabled: $35 + ceil(100,000/1,000) × $0.90 = $125. SendGrid published Pro scenario: $89.95 + 100,000 × $1.10/1,000 = $199.95; confirm the account-specific overage schedule. | Conditional estimates before taxes/add-ons, not automatic access to unlimited sending. |
| Resend 50,000 tier: first cheaper upgrade point | $20 + ceil(max(0, volume − 50,000)/1,000) × $0.90. At 66,000: $34.40. At 66,001: $35.30, compared with $35 for 100,000. | Upgrade first costs less at 66,001 quota-counted emails, with overages enabled; no exact equality. Do not apply this rounding to SendGrid. |
| The same feature at the same volume | Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 including one dedicated IP | $120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 monthly difference |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| Transactional email only, under 50,000 a month | Either | $20 on Resend and $19.95 on SendGrid buy the same volume, and the five-cent gap is not a reason to migrate. |
| You need a dedicated IP at 100,000 emails | SendGrid Pro | $89.95 includes one IP, against $90 for Resend Scale plus $30 for the add-on, and Resend Pro cannot buy an IP at all. |
| A free tier is mandatory for staging | Resend | Resend offers ongoing free usage within both limits. Standard direct SendGrid trials expire after 60 days; sending requires an explicit paid upgrade, not automatic billing. |
| Agencies authenticating dozens of client domains | Resend Scale, with the domain add-on | 1,000 domains are included on Scale and $20 adds 100 more, against a domain line SendGrid does not print. |
| SSO and an IP at 500,000 emails | SendGrid Pro | SSO is included in Pro and so is one IP, while Resend puts SSO at $150 a month and the IP at $30 on top of Scale. |
| 2,500,000 emails a month and nothing exotic | SendGrid Pro | $1,099 against $1,150 on Resend, and the gap widens with the IP add-on that Resend needs for the same setup. |
| Marketing broadcasts to a contact list | Resend marketing plans | Marketing is priced per contact rather than per email, so an unlimited number of sends to 10,000 contacts is $80. |
| Volume swings month to month | Either, with an alert at 60,000 | For Resend, enable eligible paid-plan overages before relying on them and compare rounded buckets: the $35 tier wins from 66,001 emails. SendGrid has its own account-specific rates and limits; check those separately. |

## Migration path

Both vendors authenticate a domain with DKIM, SPF and DMARC records, so moving means adding new DNS records while the old ones still answer. Keep both authenticated for a week, warm the new domain or IP, then flip the sending domain in code.

The parts that do not travel are templates and reputation. React Email templates are code and move with the repository; SendGrid's dynamic templates are vendor objects. A dedicated IP starts cold on either side, so a sender who relies on one should plan the warm-up as a week of projected volume rather than a switch.

## Questions that change the decision

**Does Resend sell a dedicated IP on Pro?**  
No. The $30 per month add-on is listed for Scale plans, to accounts sending more than 3,000 emails a day. Pro has no IP option.

**Does SendGrid automatically charge after the free trial?**  
No automatic paid conversion is described for the standard new direct-account trial. After 60 days, sending stops unless you choose a paid upgrade. Partner/reseller and already-paid accounts can have different terms; check the actual plan and notices. Older direct free plans were subject to the 2025 retirement transition.

**How do Resend overages work?**  
On an eligible paid transactional plan, enable Transactional Overages in Settings. Additional usage rounds up in 1,000-email buckets at the plan rate. At $20 for 50,000 and $0.90 per bucket, 51,415 emails cost $21.80; 66,001 cost $35.30, above the $35/100,000 tier. Free plans are not eligible. Taxes and other fees are extra. This rounding rule does not establish SendGrid billing behavior.

**Do both include inbound email parsing?**  
Resend lists inbound email with webhooks on every plan, and SendGrid lists an Inbound Parse webhook as part of the Email API feature set.

## Sources

- https://resend.com/pricing
- https://www.twilio.com/en-us/products/email-api/pricing
- https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
- https://resend.com/docs
- https://www.twilio.com/docs/sendgrid
- https://resend.com/changelog/pay-as-you-go-pricing
- https://www.twilio.com/docs/sendgrid/ui/account-and-settings/upgrading-your-plan
- https://help.twilio.com/articles/47846436523419
- https://www.twilio.com/en-us/changelog/changes-coming-to-sendgrid-s-free-plans
- https://resend.com/docs/dashboard/emails/idempotency-keys
- https://resend.com/docs/api-reference/errors

## Same task, two SDKs

**Resend**

```
// One attempt, not an outbox implementation. Never call directly from a browser.
// Caller must atomically claim a durable outbox row BEFORE the first send and
// persist its immutable payload, key, firstAttemptAt and attempt outcomes.
// Use one event/version key, not Date.now(); retries must reuse the exact payload.
// Resend retains keys for 24 hours, not forever. Acceptance is not delivery.
export async function attemptEmail(resend, row, now = Date.now()) {
  if (row.acceptedId) return { acceptedId: row.acceptedId, alreadyRecorded: true };
  const age = now - row.firstAttemptAt;
  // Stop 5 minutes early to allow for clock skew / requests in flight.
  if (!Number.isFinite(age) || age < 0 || age >= 23 * 3600000 + 55 * 60000) {
    throw new Error('reconcile_required: do not blindly resend after the 24-hour window');
  }
  if (!row.key || row.key.length > 256 || !row.payload) throw new Error('invalid_outbox_row');
  let response;
  try {
    response = await resend.emails.send(row.payload, { idempotencyKey: row.key });
  } catch {
    throw new Error('unknown_outcome: reconcile; bounded same-key retry only within the window');
  }
  const { data, error } = response;
  if (error) {
    if (error.name === 'invalid_idempotent_request') {
      throw new Error('payload_conflict: stop; do not mint a new key to bypass this 409');
    }
    if (error.name === 'concurrent_idempotent_requests') {
      throw new Error('in_progress: defer with bounded backoff and recheck the window');
    }
    throw new Error(`send_failed: ${error.name}; inspect before any retry`);
  }
  if (!data?.id) throw new Error('unknown_outcome: missing acceptance id; reconcile');
  return { acceptedId: data.id }; // Caller must durably save this before acking its job.
}
// On long outages, check durable state plus provider logs/webhooks before deciding
// whether to resend. A crash after acceptance but before saving the id is ambiguous.
// If reconciliation cannot resolve it, hold for review; this is not exactly-once delivery.
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
