# FACT SHEET — Clerk vs Auth0 (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Both vendors meter people, but they count different people: Clerk bills Monthly Retained Users
(MRU), Auth0 bills Monthly Active Users (MAU). State that difference wherever you compare a number.

## Clerk (source: https://clerk.com/pricing)

The unit
- MRU = a user who visits at least one day after signing up. The first day is free, so a user who
  signs up and never returns is never billed.
- MRO = a monthly retained organization: at least 2 members, at least one of them an MRU that month.
- Every plan supports unlimited applications.

Plans (monthly price; annual price in brackets)
- Hobby — $0. 50,000 MRU limit per app, up to 3 dashboard seats, 3 social connections, fixed 7-day
  session lifetime, 1-day application logs, no MFA, no passkeys, no branding removal.
- Pro — $25/mo ($20/mo billed annually). 50,000 MRU included per app, then $0.02/month each with
  volume discounts; 1 SSO connection included then $75/mo each; 1 Directory Sync connection included
  then $75/mo each **from 1 January 2027**; satellite domains $10/mo each; MFA; passkeys; branding
  removal; 7-day logs; SMS authentication (US/Canada $0.01 per SMS, international at market rate).
- Business — $300/mo ($250/mo billed annually). 10 dashboard seats included ($20/mo each additional);
  SOC 2 report; 30-day application and admin logs; advanced protections; priority (not SLA) support.
- Enterprise — custom, annual only: 99.99% uptime SLA, dedicated TAM, HIPAA with BAA, log sink
  destinations, custom security questionnaires.

Add-ons that change the bill
- B2B Authentication (organizations). Included free on all plans: 100 MRO per app, up to 20 members
  per organization, Admin/Member roles, custom permissions, invitations. Enhanced add-on $100/mo
  ($85/mo annual): unlimited members per organization, custom roles and role-sets, verified domains,
  enterprise connections linked to organizations, then $1/month per MRO beyond the 100 included.
- Protect: 10,000 protection checks free per month, then $0.002 per check up to 1,000,000. The table
  runs 50,000 checks = $80, 100,000 = $180, 500,000 = $980; 1,000,000+ is quote-only. Brute-force
  prevention does not count toward checks.
- Administration: 5 impersonations free, unlimited for $100/mo ($85 annual).
- Clerk Billing (their Stripe-based subscription product): 0.7% of billing volume on top of
  Stripe's 2.9% + $0.30 per transaction.
- Machine authentication: API keys 1,000 creations and 100,000 verifications included per month;
  M2M tokens 2,500 creations and 100,000 verifications included per month, then volume pricing.

Grace and enforcement
- Exceeding 50,000 MRU on Hobby, or 100 MRO without the B2B add-on, gives a one-month grace period to
  upgrade before the application stops working.

## Auth0 (source: https://auth0.com/pricing)

The unit
- MAU = any non-internal (non-employee) user that authenticated during the month for a given tenant.
- Yearly billing is 11x the monthly price (one month free).
- Between tiers, you are billed at the next tier up.

Plans at the starting tier (B2C / B2B, 500 MAU)
- Free — $0 for both. Up to 25,000 MAU, 1 custom domain, 5 organizations, 1 enterprise connection,
  unlimited social connections, 1-day log retention, 1 tenant, 3 admin users, 1,000 M2M tokens,
  self-service SSO and SCIM included.
- Essentials — $35/mo B2C, $150/mo B2B.
- Professional — $240/mo B2C, $800/mo B2B.
- Enterprise — contact sales.

B2C base price by MAU (monthly, Essentials / Professional)
- 500: $35 / $240
- 1,000: $70 / $240
- 2,500: $175 / $545
- 5,000: $350 / $1,000
- 7,500: $525 / $1,200
- 10,000: $700 / $1,600
- 20,000: $1,400 / $3,200
- 30,000: $2,100 / contact
- 40,000: $2,800 / not available
- 50,000: $3,500 / not available

B2B base price by MAU (monthly, Essentials / Professional)
- 500: $150 / $800
- 1,000: $300 / $800
- 2,500: $700 / $1,200
- 5,000: $1,300 / $1,500
- 7,500: $1,725 / $1,800
- 10,000: $2,100 / $2,400
- 20,000: $3,800 / contact
- 30,000+: contact for both

Add-ons (Auth0)
- Auth0 for AI Agents: adds 50% to the base price, rounded up to the dollar (unlimited Token Vault,
  all forms of CIBA).
- Enterprise SSO connections: Essentials includes 3, Professional includes 5; each additional costs
  $100/month ($1,100/year), maximum 30 in total.
- Enterprise MFA: $100/month on Essentials, included on Professional.
- M2M tokens: 1,000 included on Free and Essentials, 5,000 on Professional; add-on tiers run
  $10/month for 2,500 (B2B) up to $1,200/month for 300,000.

Feature cliffs worth naming
- Log retention: 1 day Free, 5 days Essentials, 10 days Professional, 30 days Enterprise.
- Tenants: 1 / 3 / 12 / unlimited.
- Organizations: 5 on Free, 10 on Essentials and Professional, custom on Enterprise.
- Custom database connections (bring your own user store) and cross-app SSO: Professional and up only.
- B2C enterprise connections: 1 on Free, "not available" on Essentials and Professional — custom SSO
  tiers require Enterprise.
- Admin users: 3 on Free, unlimited on paid.

## Derived arithmetic you may use (show the formula in the text)

- B2C at 50,000 users: Auth0 Essentials $3,500/month. Clerk Pro at 50,000 MRU is $25/month because
  the first 50,000 are included. That is 140x — but Auth0 counts every user who authenticated, and
  Clerk counts only users who returned at least 24 hours after signup, so the two numbers are not the same quantity.
- Clerk at 100,000 MRU: 50,000 over × $0.02 = $1,000 + $25 = $1,025/month. Auth0 B2C at 100,000 MAU
  has no printed tier — the price sheet ends at 50,000 and becomes "contact us".
- Auth0's step function: 501 B2C users on Essentials bills at the 1,000 tier, $70/month, double the
  $35 for 500. 500 users cost $0.07 each; the 501st user costs $35.
- Clerk B2B for a 10-person SaaS at 5,000 users with 200 organizations: Business $300 + B2B add-on
  $100 + 100 MRO over × $1 = $500/month (all 5,000 MRU inside the 50,000 included).
- Auth0 B2B at 5,000 MAU: Essentials $1,300/month, Professional $1,500/month — before the AI Agents
  add-on, which is 50% more again ($1,950 and $2,250).
- Clerk Protect at 200,000 checks/month: (200,000 − 10,000) × $0.002 = $380, matching the published
  table row.

## Do not claim
- Do not treat MAU and MRU as the same number; say which vendor counts what.
- Do not claim Clerk's free tier has unlimited users — Hobby stops at 50,000 MRU per app.
- Do not claim Auth0 is "enterprise only" or has no free tier: it includes 25,000 MAU free.
- Do not claim Clerk Business is required for SSO — SSO connections are a Pro add-on; Business adds
  workspace SSO, SOC 2 and seat count.
- Do not quote an Auth0 Enterprise price; it is quote-only.
- Do not present the 140x comparison without the unit caveat above.
- Do not claim either vendor stores passwords in plaintext or makes migration effortless; that is not
  on either price sheet.


## Targeted correction review — 2026-11-14
Auth0 B2B Essentials includes unlimited organizations; Professional inherits it. B2C organization limits must not be applied to B2B. Source: https://auth0.com/pricing.md . Clerk retention means return at least 24 hours after signup: https://clerk.com/pricing .
Other claims retain their original review date; this is not a full re-verification.
