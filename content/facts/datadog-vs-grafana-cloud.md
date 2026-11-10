# FACT SHEET — datadog-vs-grafana-cloud (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Datadog Infrastructure Pro** — $15 per host per month billed annually, $18 month-to-month  
  source: https://www.datadoghq.com/pricing/list/
- **Datadog custom metrics** — $5 per 100 custom metrics per month; 100 per host allotted on Pro, 200 on Enterprise  
  source: https://www.datadoghq.com/pricing/list/
- **Datadog ingested metrics** — $0.10 per 100 ingested custom metrics per month with Metrics without Limits  
  source: https://www.datadoghq.com/pricing/list/
- **Datadog logs** — $0.10 per ingested GB; indexed events $1.70 per 1M at 15 days, $2.50 at 30 days  
  source: https://www.datadoghq.com/pricing/list/
- **Datadog APM** — $31 per host per month billed annually, $36 month-to-month  
  source: https://www.datadoghq.com/pricing/list/
- **Datadog retention** — 15 months of full-resolution metrics on Pro; 15-day log and trace search  
  source: https://www.datadoghq.com/pricing/
- **Grafana Cloud Pro** — $19 per month platform fee plus usage; 10,000 active series and 50 GB logs included; 13-month metric retention  
  source: https://grafana.com/pricing/
- **Grafana series tiers** — $6.50 per 1,000 from 10,001 to 100,000; $5.90 to 200,000; $5.50 above; enterprise from $25,000 a year  
  source: https://grafana.com/pricing/
- **Grafana logs** — $0.05/GB process, $0.40/GB write, $0.10/GB retain; 50 GB included, 30-day retention  
  source: https://grafana.com/pricing/
- **Grafana Adaptive Metrics** — Vendor claim: optimise metrics by up to 80% through aggregation and cardinality work  
  source: https://grafana.com/pricing/

## Derived arithmetic used in the article (formula printed in the text)

- **20 hosts, 5,000 custom series** — Datadog: 20 × $15 = $300, plus (5,000 − 20 × 100) = 3,000 series ÷ 100 × $5 = $150. Grafana: $19 platform fee, 5,000 under the 10,000 allowance ⇒ $450 on Datadog against $19 on Grafana Cloud Pro
- **20 hosts, 200,000 custom series** — Datadog: $300 + (200,000 − 2,000) ÷ 100 × $5 = $9,900. Grafana: $19 + 90,000 × $6.50/1,000 = $585 + 100,000 × $5.90/1,000 = $590 ⇒ $10,200 on Datadog against $1,194 on Grafana Cloud Pro
- **500 GB of logs a month, 200M events, 30-day retention** — Datadog: 500 × $0.10 = $50 ingest, plus 200M ÷ 1M × $2.50 = $500 indexed. Grafana: 450 GB over the 50 GB allowance × ($0.05 + $0.40 + $0.10) = $247.50 ⇒ $550 on Datadog against $247.50 on Grafana Cloud Pro
- **30 hosts with APM on Datadog** — 30 × ($15 infrastructure + $31 APM) = 30 × $46 = $1,380 per month at annual rates ⇒ $1,380 before logs, traces or RUM; Grafana Cloud Pro has no per-host infrastructure line

## Sources

- https://www.datadoghq.com/pricing/
- https://www.datadoghq.com/pricing/list/
- https://docs.datadoghq.com/account_management/billing/custom_metrics/
- https://grafana.com/pricing/
- https://grafana.com/docs/grafana-cloud/adaptive-telemetry/adaptive-metrics/
