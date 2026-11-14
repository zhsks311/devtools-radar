# FACT SHEET — resend-vs-sendgrid (verified 2026-11-14)

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
- **Resend bucket billing correction** — Paid transactional plans opt in using Transactional Overages. Round excess usage up in 1,000-email buckets; 51,415 on 50k/$20 gives $21.80 at $0.90/bucket. Taxes/fees extra.  
  source: https://resend.com/changelog/pay-as-you-go-pricing
- **SendGrid trial correction** — Standard new direct trial stops sending after 60 days unless upgraded; no automatic paid conversion. Partner/reseller terms and account notices must be checked.  
  source: https://www.twilio.com/docs/sendgrid/ui/account-and-settings/upgrading-your-plan

## Derived arithmetic used in the article (formula printed in the text)

- **100,000 emails a month, no dedicated IP** — Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000 ⇒ $35.00 against $34.95, a five-cent gap at the bottom of the ladder
- **200,000 emails a month, the rung against the overage** — Eligible Resend paid plan with Transactional Overages enabled: $35 + ceil(100,000/1,000) × $0.90 = $125. SendGrid published Pro scenario: $89.95 + 100,000 × $1.10/1,000 = $199.95; confirm the account-specific overage schedule. ⇒ Conditional estimates before taxes/add-ons, not automatic access to unlimited sending.
- **Resend 50,000 tier: first cheaper upgrade point** — $20 + ceil(max(0, volume − 50,000)/1,000) × $0.90. At 66,000: $34.40. At 66,001: $35.30, compared with $35 for 100,000. ⇒ Upgrade first costs less at 66,001 quota-counted emails, with overages enabled; no exact equality. Do not apply this rounding to SendGrid.
- **The same feature at the same volume** — Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 including one dedicated IP ⇒ $120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 monthly difference

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
