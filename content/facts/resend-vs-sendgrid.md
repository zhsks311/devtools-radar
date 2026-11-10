# FACT SHEET — resend-vs-sendgrid (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Resend plans** — Free 3,000/mo (100/day); Pro $20 for 50k and $35 for 100k; Scale $90 for 100k to $1,150 for 2.5M  
  source: https://resend.com/pricing
- **Resend overage** — $0.90 per 1,000 beyond the included volume; $0.80, $0.70, $0.65, $0.52, $0.46 on higher Scale rungs  
  source: https://resend.com/pricing
- **Resend dedicated IP** — $30 per month add-on, Scale only, for accounts sending more than 3,000 emails a day  
  source: https://resend.com/pricing
- **Resend add-ons** — Domains $20/mo for 100 more; SSO $150/mo on Scale; 3 inboxes included, $1 per extra inbox  
  source: https://resend.com/pricing
- **Resend marketing** — Priced per contact: free to 1,000, $40 for 5,000, $80 for 10,000, up to $650 for 150,000  
  source: https://resend.com/pricing
- **SendGrid plans** — 60-day trial at 100 emails/day; Essentials from $19.95 (50k) and $34.95 (100k); Pro from $89.95 (100k)  
  source: https://www.twilio.com/en-us/products/email-api/pricing
- **SendGrid ladder** — Pro $249 for 300k, $499 for 700k, $799 for 1.5M, $1,099 for 2.5M; Premier custom  
  source: https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
- **SendGrid overage** — $1.33 per 1,000 on the 50k Essentials tier, $0.88 on 100k Essentials, $1.10 on 100k Pro  
  source: https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
- **SendGrid features** — Pro includes 1 dedicated IP, SSO, 1,000 teammates, 2,500 validations and 7 days of searchable activity; Essentials keeps 1 teammate, 2 webhooks and 3 days  
  source: https://www.twilio.com/en-us/products/email-api/pricing

## Derived arithmetic used in the article (formula printed in the text)

- **100,000 emails a month, no dedicated IP** — Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000 ⇒ $35.00 against $34.95, a five-cent gap at the bottom of the ladder
- **200,000 emails a month, the rung against the overage** — Resend: 100,000 Pro at $35 + 100,000 × $0.90/1,000 = $125, against the Scale 200,000 rung at $160. SendGrid: $89.95 + 100,000 × $1.10/1,000 = $199.95, against the Pro 300,000 rung at $249 ⇒ $125 on Resend and $199.95 on SendGrid, both cheaper than buying the next rung
- **Overage break-even on the 50,000 tiers** — Resend: $20 + $0.90 per 1,000 over 50,000 equals $35 at 16,666 extra emails, so 66,666. SendGrid: $19.95 + $1.33 per 1,000 equals $34.95 at 11,278 extra, so 61,278 ⇒ Past roughly 61,000 to 67,000 sends the next tier is cheaper than the overage
- **The same feature at the same volume** — Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 including one dedicated IP ⇒ $120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 monthly difference

## Sources

- https://resend.com/pricing
- https://www.twilio.com/en-us/products/email-api/pricing
- https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai
- https://resend.com/docs
- https://www.twilio.com/docs/sendgrid
