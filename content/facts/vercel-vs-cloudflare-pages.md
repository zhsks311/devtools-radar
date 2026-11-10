# FACT SHEET — Vercel vs Cloudflare (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Vercel (source: https://vercel.com/pricing, https://vercel.com/blog/introducing-active-cpu-pricing-for-fluid-compute)

Hobby — $0
- 100 GB Fast Data Transfer / month included
- 1 M CDN requests / month included
- temporary deployments without an account (`vercel deploy --temporary`)

Pro — $20/month (per seat)
- 1 TB Fast Data Transfer / month included, then starting at $0.15 per GB
- 10 M CDN requests / month included, then starting at $2 per 1 M
- additional line items that exist on the price sheet: ISR reads/writes, Blob storage ($0.023/GB),
  image optimization, log drains, firewall rate-limit requests ($0.50 per 1 M allowed requests)

Compute model — Fluid compute (default for new projects; vendor says it powers over one trillion invocations)
- active CPU pricing: $0.128 per vCPU-hour, "starting at"
- provisioned memory billed in GB-hours "at a much lower rate (less than 10% of Active CPU)"
- bills **execution time, not wall time**: a function waiting on an external API does not burn CPU meter
- in-function concurrency: concurrent requests share one instance, so idle waits are reused
- vendor claim, label it as such: "up to 85%" and "up to 90%" cost savings from in-function concurrency
  and active CPU respectively
- max function duration listed at 5 minutes (Vercel changelog: "Serverless Functions can now run up to 5 minutes")

## Cloudflare (source: https://developers.cloudflare.com/workers/platform/pricing/, .../pages/platform/limits/)

Workers Free
- 100,000 requests/day, 10 ms CPU time per invocation, no charge for duration

Workers Paid — $5/month minimum per account
- 10 M requests included, then $0.30 per additional million
- 30 M CPU-milliseconds included / month, then $0.02 per additional million CPU-ms
- max 5 minutes of CPU time per invocation (default limit 30 seconds); 15 minutes for Cron Trigger /
  Queue consumer invocations
- **no charge for data transfer (egress) or bandwidth** — stated explicitly on the pricing page
- static asset requests are free and unlimited
- Pages Functions are billed as Workers; Pages supports the Standard usage model

Cloudflare's own worked examples (cite as Cloudflare's numbers):
- 15 M requests/month at 7 ms CPU each ⇒ $5.00 sub + $1.50 requests + $1.50 CPU = $8.00
- 100 M requests/month at 7 ms CPU each ⇒ $5.00 + $27.00 + $13.40 = $45.40
- same 100 M with Workers Caching at 80% hit rate ⇒ $5.00 + $27.00 + $2.20 (cache hits cost a request, no CPU)
- 720 cron invocations at 180,000 ms CPU each ⇒ $5.00 + $1.99 = $6.99

Cloudflare Pages limits (Free / Pro / Business)
- builds per month: 500 / 5,000 / 20,000; concurrent builds 1 / 5 / 20
- build timeout 20 minutes
- 20,000 files per site on Free (100,000 on paid with PAGES_WRANGLER_MAJOR_VERSION=4)
- max single asset 25 MiB
- 100 projects per account

## Derived arithmetic you may use (show the formula in the text)

- 3 TB/month transfer: Vercel Pro includes 1 TB; 2 TB over = 2,048 GB × $0.15 = $307.20/month extra.
  Cloudflare: $0 by policy.
- 50 M requests/month: Vercel Pro 40 M over × $2/M = $80.00; Cloudflare Paid 40 M over × $0.30/M = $12.00
  + $5 base = $17.00.
- CPU price comparison: Vercel $0.128 per vCPU-hour = $0.128 / 3,600 / 1,000 seconds... compute it as
  $0.128 per 3.6 M CPU-ms ≈ $0.0356 per million CPU-ms, versus Cloudflare $0.02 per million CPU-ms.
- Cloudflare's 30 M included CPU-ms versus a Vercel Pro seat that has no free CPU allowance.

## Do not claim
- Do not state Workers memory limits or isolate-vs-container details you were not given beyond what is above.
- Do not claim Cloudflare "includes everything"; D1/R2/KV/Queues have their own line items and were not verified here.
- Do not attribute a benchmark of build times, TTFB or cold starts to either platform.
- Do not call Vercel Pro pricing per user; the price sheet says per seat and the 2026 sheet is per user/seat $20.
