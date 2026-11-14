# Hosting correction — 2026-11-14

Canonical article: content/final/vercel-vs-cloudflare-pages.json. Old unconditional transfer-overage comparison withdrawn.

Identify the CDN billing mode before doing arithmetic
Correction, November 14, 2026: the previous fixed transfer surcharge and migration recommendation are withdrawn. They treated legacy usage-based CDN assumptions as universal and mixed transfer units without verifying the account’s billing mode.

Vercel’s September 2026 Flat Rate CDN announcement says new Pro teams default to that mode; existing teams can switch. Its included tier is 1M CDN requests and 1 TB transfer, not a universal 10M-request allowance.

The announced additional $20/month tier includes 10M requests and 50 TB; $100/month includes 50M and 50 TB. These are CDN capacity tiers, not full hosting invoices.

Usage-based teams have a different regional bill. Read the actual team subscription, capacity, spike-protection and fair-use terms before quoting a total; Cloudflare’s Workers request meter is not interchangeable with Vercel CDN requests.

Waiting uses no active CPU, but it is not a free deployment
Fluid compute separates active CPU, provisioned memory and invocation charges. Network waiting need not consume active CPU, but memory, delivery and other services can still cost money.

Workers Standard charges a $5 monthly minimum with 10M requests and 30M CPU-ms included, then $0.30 per million requests and $0.02 per million CPU-ms. Other Cloudflare products have their own meters.

Do not compare a CDN-only price with an application total. Classify static delivery, dynamic invocations, CPU, memory, storage, database access and logs separately; apply only the allowances available to that account.

Neither a normalized CPU rate nor a low average response time proves the same code performs equivalently on both runtimes. Measure the deployed handler and include retries and background work.

Vercel duration is not a universal five-minute maximum
On Fluid compute, the documented baseline is 300 seconds by default, with Hobby capped at 300 and Pro/Enterprise ordinarily up to 800 seconds. The extended-duration beta allows up to 1,800 seconds for supported Node.js, Bun and Python versions on Pro/Enterprise.

Above 800 seconds, configure each function in code or vercel.json; the project-level default does not enable that duration. Current docs support Secure Compute and Static IPs, but exclude BYOC above 800 seconds during beta.

A duration limit measures elapsed execution, not just active CPU. Non-Fluid projects, other runtimes and upstream/client connection timeouts need separate checks. Inspect the deployed function’s configuration rather than assuming an advertised maximum applies.

Cloudflare CPU and wall time depend on the trigger
Workers Paid HTTP CPU defaults to 30 seconds and can be configured up to 5 minutes. Paid Cron has 30 seconds CPU below a one-hour schedule interval, or 15 minutes CPU at intervals of at least one hour.

Queue consumers default to 30 seconds CPU, configurable to 5 minutes; their separate wall-clock limit is 15 minutes. A 15-minute elapsed-time allowance does not authorize 15 minutes of CPU.

These execution limits are separate from Pages deployment limits. Pages documents a 25 MiB asset limit and a 20-minute build timeout; a build or static asset is not a Worker invocation.

Check Free, legacy and account-specific settings separately. A long background job should be assessed for runtime, retry and queue behavior, not selected from a single maximum-duration number.

Cache location changes which meter runs
Static asset delivery, a cache hit before Worker execution and a cache lookup inside a Worker can have different invocation counts. Do not assume every cache hit bills exactly the same request and CPU lines.

For a simple uncached hypothetical workload, 50M metered Worker requests with 7 ms CPU each cost $5 + $12 request overage + $6.40 CPU overage = $23.40. This excludes other services and assumes all included usage remains available.

If a cache prevents invocation, recalculate both request count and CPU from actual executions. If code still runs, measure its CPU rather than setting it to zero. Validate cache safety for authentication and personalized responses before crediting savings.

Choose with a complete bill and a deployment test
Do not migrate merely because traffic passes an old request or transfer threshold. Existing Vercel subscriptions and newer Flat Rate CDN teams can have materially different delivery bills.

Compare the same workload and period, using explicit units and the account’s actual rates. Add seats, compute, storage and database costs, plus migration and maintenance effort.

For Pages, test framework compatibility, large assets and build duration. For Vercel, verify function runtime, Fluid compute, configured duration and CDN mode; for Workers, separate HTTP, Cron and Queue limits.

Keep the current platform when its measured total and operational fit are better. The public figures here are reference conditions, not a quote for an inspected customer account.

Sources
https://vercel.com/pricing
https://vercel.com/blog/introducing-active-cpu-pricing-for-fluid-compute
https://developers.cloudflare.com/workers/platform/pricing/
https://developers.cloudflare.com/pages/platform/limits/
https://vercel.com/changelog/flat-rate-cdn-is-now-ga-for-pro-teams
https://vercel.com/docs/functions/configuring-functions/duration
https://vercel.com/changelog/vercel-functions-can-now-run-up-to-30-minutes
https://developers.cloudflare.com/queues/platform/limits/
https://developers.cloudflare.com/workers/platform/limits/
