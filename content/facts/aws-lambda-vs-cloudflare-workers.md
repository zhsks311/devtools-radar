# FACT SHEET — aws-lambda-vs-cloudflare-workers (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Lambda Event Functions** — $0.20 per million requests; $0.0000133334 per GB-s on Arm, $0.0000166667 on x86; free tier 1M requests and 400,000 GB-s  
  source: https://aws.amazon.com/lambda/pricing/
- **Lambda memory** — 128 MB to 10,240 MB in 1 MB increments  
  source: https://aws.amazon.com/lambda/pricing/
- **Lambda Web Functions** — $0.30 per million requests; $0.0000276944 per active vCPU-second; $0.0000036667 per GB-second of memory for the environment's life  
  source: https://aws.amazon.com/lambda/pricing/
- **Lambda Web example** — LLM streaming endpoint, 5M requests of 3,000 ms with 200 ms active CPU, $33.94; the same page prices SSR at $25.78 and an authorizer at $64.56  
  source: https://aws.amazon.com/lambda/pricing/
- **Lambda durable functions** — $8.00 per million operations, $0.25 per GB written, $0.15 per GB-month retained  
  source: https://aws.amazon.com/lambda/pricing/
- **Workers paid** — $5 per month minimum; 10M requests included then $0.30/M; 30M CPU-ms included then $0.02/M  
  source: https://developers.cloudflare.com/workers/platform/pricing/
- **Workers free** — 100,000 requests per day, 10 ms CPU per invocation, no charge for duration  
  source: https://developers.cloudflare.com/workers/platform/pricing/
- **Workers limits** — No charge for duration, egress or bandwidth; 5 minutes of CPU per invocation, 30 seconds by default; static asset requests free and unlimited  
  source: https://developers.cloudflare.com/workers/platform/pricing/
- **Workers worked examples** — 15M at 7 ms = $8.00; 100M at 7 ms = $45.40; 100M with 80% cache hits = $34.20; 720 cron runs at 180,000 ms = $6.99  
  source: https://developers.cloudflare.com/workers/platform/pricing/

## Derived arithmetic used in the article (formula printed in the text)

- **100M requests at 200 ms, 512 MB, 10 ms CPU** — Lambda Event Arm: 100M × 0.2 s × 0.5 GB = 10M GB-s, minus 400k free = 9.6M × $0.0000133334 = $128.00, plus 99M × $0.20/M = $19.80. Workers: (100M − 10M) × $0.30/M = $27.00, plus (1,000M − 30M) CPU-ms × $0.02/M = $19.40, plus $5.00 ⇒ $147.80 on Lambda against $51.40 on Workers
- **The same traffic on Lambda Web Functions** — 100M × 10 ms = 1M vCPU-s × $0.0000276944 = $27.69; 0.5 GB × 2,592,000 s = 1,296,000 GB-s × $0.0000036667 = $4.75; 100M × $0.30/M = $30.00 ⇒ $62.45, 58% below Lambda's own Event price for identical traffic
- **Cross-over against Lambda's free tier** — Lambda: (R − 1M) × $0.20/M + (R × 0.1 − 400k) × $0.0000133334. Workers: $5 + (R × 10 − 30M) × $0.02/M ⇒ Equal at about 7.5M requests a month; below that Lambda's free allowance wins, above it the CPU meter does
- **Replacing a 200 ms wait with a 1 s wait** — At 10M requests: Lambda 10M × 1 s × 0.5 GB = 5M GB-s − 400k = 4.6M × $0.0000133334 = $61.33 + $1.80. Workers CPU is unchanged at 10M × 200 ms = 2,000M − 30M × $0.02/M = $39.40 + $5 ⇒ $63.13 against $44.40: the slower request costs Lambda $53 more and Workers nothing

## Sources

- https://aws.amazon.com/lambda/pricing/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://developers.cloudflare.com/workers/platform/limits/
- https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
- https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html
