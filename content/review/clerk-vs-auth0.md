# Clerk vs Auth0 — review

1. **FACT — The B2B comparison prices an Auth0 plan that cannot hold the stated organizations, and leaves Clerk's units implicit.** Location: section “Pick by who you are billed for, then check the next boundary”; repeated in decision_matrix row 4 and verdict_summary.

   **Quote:** “A 10-person SaaS with 5,000 users and 200 organisations on Clerk Business pays $300 + $100 + (200 − 100) × $1 = $500/month; Auth0 B2B Essentials at 5,000 MAU is $1,300.”

   Auth0 Essentials and Professional each allow only 10 organizations; $1,300 is not a usable quote for 200 organizations. Clerk's calculation assumes 5,000 MRU and 200 MRO, not merely 200 created organizations. An MRO needs at least 2 members, including an MRU that month. Business's included seats are dashboard seats, not SaaS end users. Facts: lines 12, 22–23, 28–31, 94, 109–112.

   **Replacement:** “For a team needing 10 dashboard seats, Clerk Business with 5,000 MRU and 200 qualifying MRO costs $300 + $100 + (200 − 100) × $1 = $500/month; Auth0 B2B Essentials costs $1,300/month at 5,000 MAU but allows only 10 organizations, so it cannot serve this 200-organization scenario.”

2. **FACT — Quote-only pricing does not establish HIPAA eligibility.** Location: decision_matrix row 8.

   **Quote:** “Clerk lists HIPAA with BAA only on its annual Enterprise plan, and Auth0 Enterprise pricing is quote-only too, so no self-serve tier settles it.”

   The sheet establishes Clerk's HIPAA-with-BAA gate, but supplies no Auth0 HIPAA or BAA claim. Do not use Auth0's pricing model as compliance evidence. Facts: lines 24–25, 58.

   **Replacement:** “For a HIPAA-with-BAA requirement, request Clerk Enterprise's custom annual quote; confirm Auth0's HIPAA and BAA eligibility separately before treating it as an alternative.”

3. **FACT — Counting an MAU is not an immediate charge.** Location: first section.

   **Quote:** “A user who signs up and never returns is never billed; Auth0 bills that same user the moment they log in.”

   Auth0 meters qualifying non-internal users monthly and has a Free plan covering up to 25,000 MAU. Neither an immediate charge nor a charge for every counted user is established. Facts: lines 10–11, 48, 53–55.

   **Replacement:** “A user who signs up and never returns does not count as a Clerk MRU, but a non-internal user who authenticates counts as an Auth0 MAU for that tenant and month, including within Free's 25,000-MAU allowance.”

4. **FACT — The blanket B2C enterprise-SSO prohibition erases Free's included connection.** Location: second section.

   **Quote:** “Auth0 forbids self-serve B2C enterprise SSO.”

   Free includes 1 enterprise connection; B2C Essentials and Professional list enterprise connections as unavailable. The following sentence does not repair the blanket prohibition. Facts: lines 53–55, 96–97.

   **Replacement:** “Auth0 B2C Free includes 1 enterprise connection, but paid B2C Essentials and Professional list enterprise connections as unavailable; custom SSO tiers require Enterprise.”

5. **LOGIC — A user-count ratio is not the share of a price gap caused by definitions.** Location: final section's checklist.

   **Quote:** “That ratio is the definitional share of the gap.”

   No such relationship follows: Clerk includes 50,000 MRU, Auth0 rounds usage to tiers, and feature requirements and add-ons also affect the bill. The preceding instruction also says “logins,” which can mean events rather than distinct qualifying users. Facts: lines 10–11, 18–21, 48–50.

   **Replacement:** “Count distinct non-internal users who authenticated during the month for each Auth0 tenant, and users who visited on a later day after signup for each Clerk app, then price those separate MAU and MRU totals under the required plans and add-ons.”

6. **LOGIC — The annual total is paired with the wrong monthly equivalent.** Location: cost_math row 1, result.

   **Quote:** “$38,500/year ($3,500/month)”

   $3,500 is the monthly-billing list price, not the monthly equivalent of the annual total. The displayed annual formula is correct. Facts: lines 49, 70.

   **Replacement:** “Annual billing costs 11 × $3,500 = $38,500/year, equivalent to $38,500 / 12 = $3,208.33/month rounded to cents; monthly billing remains $3,500/month.”

7. **LOGIC — The hook assigns most of the price difference to definitions without calculating that contribution.** Location: hook, first sentence.

   **Quote:** “At 50,000 users, Auth0 B2C Essentials bills $3,500 a month and Clerk Pro bills $25, a 140x gap that is mostly a units error.”

   Different units make the comparison conditional; they do not prove that definitions explain most of the gap. A population could satisfy both meters. Name both units at the comparison and show the division. Facts: lines 102–104.

   **Replacement:** “At 50,000 MAU, Auth0 B2C Essentials costs $3,500/month, while Clerk Pro at 50,000 MRU costs $25/month: $3,500 / $25 = 140, but MAU counts non-internal users who authenticated during the month for a tenant and MRU counts users who returned on a later day after signup, so these are not equivalent populations.”

8. **FACT — The claim about most comparisons has no source.** Location: hook, second sentence.

   **Quote:** “Clerk counts users who came back on a later day, Auth0 counts everyone who logged in, and most head-to-heads divide one by the other as if they were the same people.”

   The sheet contains no survey of head-to-head articles. “Everyone” also drops Auth0's non-internal-user qualification and tenant/month scope. Facts: lines 10–11, 48.

   **Replacement:** “A user who signs up and never returns is excluded from Clerk's MRU count, but a non-internal user who authenticates that month counts toward the Auth0 tenant's MAU total.”

9. **FACT — The Clerk philosophy invents a UI feature and product intent.** Location: second section's Clerk blockquote.

   **Quote:** “**Clerk:** authentication is a product surface, so it ships prebuilt UI, organisations and billing, and prices retained attention.”

   The sheet supports organizations, Clerk Billing and MRU billing, not prebuilt UI or a causal product philosophy. The section title repeats this unsupported positioning. Facts: lines 10–11, 28–31, 36–37.

   **Replacement:** “**Clerk:** the billing meter is a user who returns on a later day after signup; a signup that never returns is not billed.”

10. **FACT — The Auth0 philosophy adds an unsupported feature and causal positioning.** Location: second section's Auth0 blockquote.

    **Quote:** “**Auth0:** identity is infrastructure, so it sells connections, tenants and actions, and prices authenticated humans in tiers.”

    “Actions” is absent from the sheet; “identity is infrastructure” is not a documented reason for its pricing. Use the actual meter and consequence instead. Facts: lines 48–50.

    **Replacement:** “**Auth0:** the billing meter is a non-internal user who authenticates during the month for a tenant, and usage between published tiers is billed at the next tier up.”

11. **FACT — The Clerk recommendation rests partly on an unverified feature.** Location: final section, opening sentence.

    **Quote:** “**Clerk wins if** most sign-ups never return, or you sell B2B where organisations and prebuilt UI are the product.”

    Prebuilt UI is absent from the sheet. Nonreturning signups alone also do not establish a paid-plan winner when both products have free allowances. Use a documented requirement that actually selects Pro. Facts: lines 16–21, 53–55.

    **Replacement:** “**Choose Clerk Pro if** you need MFA, passkeys or branding removal below 50,000 MRU per app: those features are excluded from Hobby and included in Pro's $25/month plan.”

12. **FACT — “Identity programme” and procurement do not establish an Auth0 advantage.** Location: final section, second paragraph.

    **Quote:** “Auth0 wins for an identity programme: enterprise SSO, 12 tenants on Professional, custom database connections, procurement.”

    Procurement suitability is not in the sheet, and Clerk also offers SSO connections on Pro. The Auth0 SSO claim must distinguish B2B connections from B2C's paid-plan restriction. Facts: lines 18–20, 85–86, 93, 95–97.

    **Replacement:** “Choose Auth0 Professional if you need custom database connections or cross-app SSO, both gated to Professional and above; Professional includes 12 tenants, but paid B2C enterprise connections require Enterprise.”

13. **FACT — Protect is presented as an uncapped per-check tariff.** Location: Clerk add-ons table.

    **Quote:** “| Protect | 10,000 checks free, then $0.002 each | bot-heavy sign-up forms |”

    The sheet bounds the printed rate and makes 1,000,000+ checks quote-only; it does not establish that bot-heavy signup forms generate billable protection checks. Brute-force prevention explicitly does not count. Facts: lines 32–34.

    **Replacement:** “Protect includes 10,000 checks free per month, then lists $0.002 per check below the quote-only 1,000,000+ range; brute-force prevention does not count toward checks.”

14. **FACT — The Clerk Directory Sync row assumes a protocol not established by the sheet.** Location: Clerk add-ons table.

    **Quote:** “| Directory Sync | 1 included, then $75/mo from 1 January 2027 | SCIM-heavy B2B |”

    SCIM is documented for Auth0 Free, not for Clerk Directory Sync. Do not transfer a feature between vendors. Facts: lines 19–20, 55.

    **Replacement:** “On Clerk Pro, Directory Sync includes 1 connection, then costs $75/month per additional connection from 1 January 2027, so the bill increases with connection count.”

15. **FACT — The add-on table creates a product name.** Location: Clerk add-ons table.

    **Quote:** “| B2B Enhanced | $100/mo, 100 MRO included, then $1 each | many small organisations |”

    The sheet names B2B Authentication and describes an Enhanced add-on; it does not name a product “B2B Enhanced.” Also make clear that 100 MRO per app are included on all plans rather than a new allowance purchased with the add-on. Facts: lines 28–31.

    **Replacement:** “B2B Authentication includes 100 MRO per app on all plans; its Enhanced add-on costs $100/month, removes the 20-member organization limit and charges $1/month per MRO beyond the included 100.”

16. **FACT — An unprinted price is turned into a specific plan requirement.** Location: decision_matrix row 3, pick.

    **Quote:** “Clerk Pro, or an Auth0 Enterprise quote”

    The sheet says Auth0 B2C has no printed tier at 100,000 MAU and becomes contact-us pricing; it does not say crossing 50,000 MAU necessarily requires the Enterprise plan. The situation's “monthly users” also fails to distinguish MRU from MAU. Facts: lines 105–106.

    **Replacement:** “For usage beyond Clerk's 50,000 included MRU per app or Auth0's last printed 50,000-MAU B2C tier, price Clerk Pro's MRU overage and request an Auth0 quote for the actual MAU count.”

17. **FACT — The growth row drops Clerk's volume-discount qualification.** Location: decision_matrix row 3, why.

    **Quote:** “Clerk keeps charging $0.02 per MRU past 50,000; Auth0's B2C price sheet ends at 50,000 MAU and turns into "contact us".”

    The sheet explicitly says “with volume discounts”; the row presents a fixed marginal rate indefinitely. Facts: lines 18–19, 105–106.

    **Replacement:** “Clerk Pro lists $0.02/month per MRU beyond 50,000 included per app, with volume discounts; Auth0's printed B2C tiers end at 50,000 MAU, so higher usage needs a quote.”

18. **FACT — The AI add-on shorthand loses dollar rounding.** Location: decision_matrix row 7, pick.

    **Quote:** “Auth0, budgeted at 1.5x”

    The surcharge is 50% of base price rounded up to the dollar, not an unconditional exact multiplier. The row's $1,950 example also needs its formula, rather than a bare before/after total. Facts: lines 83–84, 111–112.

    **Replacement:** “For Token Vault and CIBA on Auth0, budget the base price plus a 50% surcharge rounded up to the dollar: at 5,000 B2B MAU on Essentials, $1,300 + ($1,300 × 50%) = $1,950/month.”

19. **FACT — The Business annual price is missing its monthly unit.** Location: FAQ “Do I need Clerk Business to offer SSO?”

    **Quote:** “SSO connections are a Pro add-on; Business ($300/month, $250 annual) adds a SOC 2 report, 10 dashboard seats and 30-day application and admin logs.”

    $250 is the monthly rate when billed annually, not an annual total. Facts: lines 18–23.

    **Replacement:** “Pro includes 1 SSO connection and charges $75/month for each additional connection; Business costs $300/month or $250/month billed annually and adds a SOC 2 report, 10 dashboard seats and 30-day application and admin logs.”

20. **WEAK — The consumer row supplies no reason to pay for Pro rather than use Hobby.** Location: decision_matrix row 1, why.

    **Quote:** “Users who never return after day one are never billed, and the first 50,000 MRU are inside the $25/month.”

    Both statements leave the same scenario eligible for Hobby's $0, 50,000-MRU-per-app allowance. Change the situation to require a documented paid feature, not just low retention. Facts: lines 16–21.

    **Replacement:** “Choose Clerk Pro below 50,000 MRU per app when you need MFA, passkeys or branding removal; without a paid-feature requirement, Hobby covers that MRU allowance for $0.”

21. **WEAK — Tier headroom does not justify staying with a vendor.** Location: decision_matrix row 6, why.

    **Quote:** “The step only costs you when you cross it, so measure your headroom to the next tier before pricing a migration.”

    This tells the reader to measure usage but supplies no decision-changing reason for “Neither — stay put,” and there is no migration-cost evidence. Replace the entire row with a missing Auth0 exclusion case, including a matching situation and pick. Facts: lines 96–97.

    **Replacement:** “If your B2C app requires enterprise connections on a paid plan, request Auth0 Enterprise pricing rather than choose Essentials or Professional, where those connections are unavailable.”

22. **META — The arithmetic introduction describes presentation rather than the reader's scenario.** Location: arithmetic section.

    **Quote:** “The quoted head-to-head, as code.”

    This announces the writing device without specifying the calculation. Replace it with the paid-plan scope and unit limitation; keep the verification date and vendor-pricing attribution elsewhere, since the standard explicitly requires those.

    **Replacement:** “This calculator prices Auth0 B2C Essentials in MAU and Clerk Pro in MRU at equal numeric inputs, not for an identical population.”

23. **SLOP — The verdict repeats the hook and recommendations instead of supplying a next decision.** Location: verdict_summary; the quoted second sentence follows another recap of Clerk's $25 and $500 examples.

    **Quote:** “Auth0 wins if you run an identity programme with enterprise SSO, multiple tenants and procurement, once you have checked which side of the next MAU tier boundary you sit on.”

    This repeats the final section's unsupported positioning and closes on a generic qualification. Sections 7–8 require an actionable ending rather than a recap. Replace the first verdict sentence's UI claim and mismatched B2B comparison as directed above, then end with a concrete feature/count check. Facts: lines 94–97.

    **Replacement:** “Before choosing Auth0 for B2B, check its 10-organization cap on Essentials and Professional against your customer count.”

## REVISION BRIEF

- Rebuild the hook around the explicit $3,500 / $25 = 140 calculation, naming 50,000 Auth0 MAU and 50,000 Clerk MRU in that sentence; delete “mostly a units error” and the unsourced claim about most head-to-heads.
- Distinguish monthly metering from charging: define Auth0's non-internal users per tenant and Clerk's later-day return rule per app, acknowledge both free allowances, and replace the alleged “definitional share” with separate MAU/MRU inputs priced under the required plans.
- Repair every 200-organization comparison, including the narrative, matrix, cost_math assumptions and verdict: specify 5,000 Clerk MRU, 200 qualifying MRO and the need for 10 dashboard seats; retain the $300 + $100 + (200 − 100) × $1 = $500 formula, but state that Auth0 Essentials and Professional stop at 10 organizations, so $1,300 at 5,000 MAU is not a compatible quote.
- Replace the invented product philosophies and their title with the documented MRU-versus-MAU and tier-rounding constraints; remove prebuilt UI, Auth0 actions, procurement suitability, Clerk SCIM assumptions and bot-signup check assumptions, and use “B2B Authentication” with its “Enhanced add-on” rather than “B2B Enhanced.”
- Restore pricing boundaries and units: keep Clerk's volume discounts, Protect's quote-only 1,000,000+ range and brute-force exclusion, the Directory Sync start date of 1 January 2027, the AI surcharge's dollar rounding and $1,300 + ($1,300 × 50%) = $1,950 formula, the $38,500 / 12 annual monthly-equivalent calculation, and Business's $250/month billed-annually unit.
- Rewrite the matrix's low-retention row around a Pro-only requirement such as MFA, passkeys or branding removal; replace the stay-put row with the paid B2C enterprise-connection exclusion, distinguish Free's 1 connection from the paid restriction, and request an Auth0 quote above printed MAU tiers without inventing an Enterprise requirement from usage alone.
- Ground conditional winners in documented gates such as Auth0 custom database connections/cross-app SSO and Clerk HIPAA with BAA on annual Enterprise; do not infer Auth0 HIPAA eligibility from quote-only pricing or invent migration effort, and end the verdict with the B2B organization-cap check rather than another positioning recap.

DEFECTS: FACT=16 META=1 SLOP=1 LOGIC=3 RHYTHM=0 BORING=0 WEAK=2
