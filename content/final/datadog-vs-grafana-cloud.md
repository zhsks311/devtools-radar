# Datadog vs Grafana Cloud — a 2026 cost teardown

> Twenty hosts and 5,000 custom series bill $450 a month on Datadog and $19 on Grafana Cloud's Pro plan. The difference is not the per-series rate. It is that only one of them puts the hosts on the invoice.

*Prices verified 2026-11-14. Category: Monitoring & Observability. Author: DevTeardown Team.*

## Verdict

The modeled metrics bills favor Grafana Cloud, especially at high cardinality. That is not a complete migration cost: collector configuration, dashboards, alerts and non-metric signals need validation. Datadog may fit a team that relies on its integrated workflows; compare actual usage and transition work rather than assuming a fixed payback period.

## 1. One sells a host, the other sells a series

Datadog's infrastructure line is a licence: $15 per host per month billed annually, $18 month-to-month, and every licence carries 100 custom metrics. Grafana Cloud's Pro plan is a $19 platform fee for the whole account, with 10,000 active series and 50 GB of logs inside it.

That is the whole philosophical difference, and it decides the invoice shape:

- **Datadog:** cost grows with machines first, then with the cardinality of what you send from them.
- **Grafana Cloud:** cost is flat until you pass the account-level allowances, then grows with data volume only.

Neither page hides this. It is written in the billing unit, which is the one line worth reading before the price.

## 2. The custom metrics line is the one that grows without a deploy

Per unit, Datadog's custom metrics cost $5 per 100 per month, which is $50 per 1,000. Grafana Cloud's first paid band is $6.50 per 1,000, then $5.90 above 100,000 and $5.50 above 200,000.

| Meter | Datadog Infrastructure Pro | Grafana Cloud Pro |
|---|---|---|
| Base | $15 per host per month, annual | $19 per account per month |
| Included series | 100 per host | 10,000 per account |
| Series beyond that | $5 per 100 | $6.50 per 1,000 |
| Effective per 1,000 | $50.00 | $6.50 |

Datadog's rate is 7.7 times Grafana's, and the allotment it ships with is 100 times smaller. Those two numbers pull in opposite directions, so the bill depends on whether your cardinality scales with hosts or with users.

## 3. Two shops, and the same four numbers

Shop one: 20 hosts, 5,000 custom series.

| Line | Datadog | Grafana Cloud |
|---|---|---|
| Platform or hosts | 20 × $15 = $300 | $19 |
| Billable series | 5,000 − 2,000 = 3,000 | 0 (5,000 under 10,000) |
| Series cost | 30 × $5 = $150 | $0 |
| **Total** | **$450** | **$19** |

Shop two: 20 hosts, 200,000 custom series, which is what a `user_id` tag does to a counter.

| Line | Datadog | Grafana Cloud |
|---|---|---|
| Platform or hosts | $300 | $19 |
| Billable series | 198,000 | 190,000 |
| Series cost | 1,980 × $5 = $9,900 | 90,000 × $6.50/1k + 100,000 × $5.90/1k = $1,175 |
| **Total** | **$10,200** | **$1,194** |

The second table is the one that arrives without a deploy, a migration or a new service. It arrives the week someone adds a tag.

## 4. Logs: one vendor counts bytes, the other counts events

This is where the two sheets stop being directly comparable. Datadog charges $0.10 per ingested GB, then $1.70 per million indexed events at 15-day retention or $2.50 at 30-day. Grafana charges three meters per GB: $0.05 to process, $0.40 to write and $0.10 to retain, with 50 GB included.

Take 500 GB a month at roughly 2.5 KB per event, or 200 million events, indexed for 30 days.

| Meter | Datadog | Grafana Cloud |
|---|---|---|
| Ingest | 500 GB × $0.10 = $50 | 450 GB × $0.05 = $22.50 |
| Index and retain | 200M × $2.50/M = $500 | 450 GB × $0.40 = $180 |
| Retention | included in the index rate | 450 GB × $0.10 = $45 |
| **Total** | **$550** | **$247.50** |

The event meter rewards fat logs and the byte meter rewards few of them. The same 500 GB is $550 or $247.50 depending on which unit your logging happens to satisfy.

## 5. Both vendors now discount you for deleting tags

Datadog sells Metrics without Limits, which splits one number into two: ingested custom metrics at $0.10 per 100, and indexed ones at $5 per 100. Grafana ships Adaptive Metrics, which aggregates and drops unused series, and the page states the claim as the vendor's own: up to 80%.

Read that as an admission. When a vendor builds a product whose only job is to delete time series before they reach the meter, the meter is cardinality, and the vendor knows the cardinality is often junk.

The practical move costs nothing:

1. Sort your metrics by tag value count, not by metric name.
2. Drop any tag whose values scale with users, carts or request ids.
3. Re-count before you negotiate a discount, because the discount is priced on the number you can already fix.

## 6. What the switch actually costs

Correction, November 14, 2026: a standard Prometheus client exposes metrics for scraping; it does not directly send to a remote_write endpoint. Pricing figures retain their November 10 check and were not re-quoted in this technical correction.

Typical metrics path: application /metrics → Prometheus scrape + remote_write → Grafana Cloud Metrics. With Alloy: application /metrics → prometheus.scrape → prometheus.remote_write → the destination. Configure the collector’s targets, endpoint and authentication; changing application instrumentation alone is insufficient.

Metrics compatibility does not migrate Datadog dashboards, monitor semantics, logs or traces automatically. Inventory each signal and verify the required collector/exporter path before cutover.

Retention also needs review: the listed Datadog Pro metrics window is 15 months, while Grafana Pro lists 13 months for metrics and 30 days for logs and traces. Compare query results and alerts, not only whether samples arrive.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 20 hosts, 5,000 custom series | Datadog: 20 × $15 = $300, plus (5,000 − 20 × 100) = 3,000 series ÷ 100 × $5 = $150. Grafana: $19 platform fee, 5,000 under the 10,000 allowance | $450 on Datadog against $19 on Grafana Cloud Pro |
| 20 hosts, 200,000 custom series | Datadog: $300 + (200,000 − 2,000) ÷ 100 × $5 = $9,900. Grafana: $19 + 90,000 × $6.50/1,000 = $585 + 100,000 × $5.90/1,000 = $590 | $10,200 on Datadog against $1,194 on Grafana Cloud Pro |
| 500 GB of logs a month, 200M events, 30-day retention | Datadog: 500 × $0.10 = $50 ingest, plus 200M ÷ 1M × $2.50 = $500 indexed. Grafana: 450 GB over the 50 GB allowance × ($0.05 + $0.40 + $0.10) = $247.50 | $550 on Datadog against $247.50 on Grafana Cloud Pro |
| 30 hosts with APM on Datadog | 30 × ($15 infrastructure + $31 APM) = 30 × $46 = $1,380 per month at annual rates | $1,380 before logs, traces or RUM; Grafana Cloud Pro has no per-host infrastructure line |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| Series count scales with users, not hosts | Grafana Cloud | At 200,000 series the series meter bills $9,900 on Datadog against $1,175 on Grafana, and the 10,000-series allowance is account-wide. |
| A team already living in Datadog APM and security | Datadog | At 30 hosts the infrastructure plus APM licence is $1,380, and rebuilding dashboards and monitors is the hidden cost of leaving. |
| Five hosts and one person on call | Grafana Cloud | Datadog's licence starts at $75 for five hosts before any custom metrics; Grafana's platform fee is $19 for the account. |
| You need 15 months of full-resolution metrics | Datadog | Datadog keeps 15 months on Pro; Grafana Cloud Pro lists 13 months for metrics and 30 days for logs and traces. |
| The custom metrics line is already over $500 | Grafana Cloud | That line is $500 per 10,000 series on Datadog and $65 per 10,000 on Grafana, so the same data crosses a factor of 7.7. |
| Logs are verbose JSON from a dozen services | Compute both before choosing | Datadog's index rate is per event and Grafana's is per GB, so 500 GB at 2.5 KB per event bills $550 against $247.50, and the same 500 GB at 250 bytes per event is 2 billion events, or $5,000 on the index line. |
| Security, SIEM and audit on one invoice | Datadog | Cloud SIEM, workload protection and audit trail are on the same price list; Grafana Cloud prices observability and leaves security elsewhere. |
| Everything is already Prometheus and you self-host Grafana | Grafana Cloud, or keep self-hosting | Existing instrumentation may be reusable, but configure Prometheus or Alloy scraping and remote_write, then verify labels, queries, alerts and destination limits before switching. |

## Migration path

Keep compatible instrumentation, then build and test the collection pipeline. The Python client example below exposes a scrape target on port 9100; it is a cardinality anti-pattern demonstration, not a complete remote_write setup. Prometheus scrapes that target and forwards via remote_write, or Alloy connects prometheus.scrape to prometheus.remote_write.

Use the destination’s documented endpoint, tenant/account identifier and scoped authentication. Verify metric names, label mapping, histogram compatibility, scrape interval, sample timestamps, cardinality and ingestion limits. Watch failed sends, queue/WAL health, gaps and duplicate series during a limited parallel run.

Do not assume the Datadog Agent is a generic Prometheus remote_write forwarder. Confirm supported collection/export for each actual integration; logs and traces require their own paths. Review dashboards, alert queries and thresholds against observed results, establish rollback criteria, and retire the old path only after validation. No fixed quarter-long overlap or payback period is established here.

## Questions that change the decision

**Are Grafana Cloud's tier prices marginal or flat?**  
Marginal. Each new band bills at a lower rate for the usage inside it, so the blended rate falls as the account grows: $6.50 per 1,000 to 100,000, then $5.90, then $5.50.

**What exactly is a custom metric on Datadog?**  
A unique metric name plus tag combination, averaged hourly across the month. Adding a tag with many values multiplies the count even if the metric name never changes.

**Does Grafana Cloud charge per host?**  
The Pro plan is a $19 platform fee per account. Host hours appear for Kubernetes monitoring at $0.01 per host hour, which is a separate product from infrastructure metrics.

**Does a Prometheus client push directly to Grafana Cloud remote_write?**  
Not in the standard scrape-based setup. The client exposes /metrics; Prometheus scrapes it and forwards with remote_write, or Alloy uses prometheus.scrape feeding prometheus.remote_write. Configure the collector’s destination and authentication, then validate labels, gaps, duplicates, queries and alerts. The application example alone is not a complete pipeline.

## Sources

- https://www.datadoghq.com/pricing/
- https://www.datadoghq.com/pricing/list/
- https://docs.datadoghq.com/account_management/billing/custom_metrics/
- https://grafana.com/pricing/
- https://grafana.com/docs/grafana-cloud/adaptive-telemetry/adaptive-metrics/
- https://prometheus.io/docs/guides/go-application/
- https://prometheus.io/docs/prometheus/latest/prometheus_agent/
- https://grafana.com/docs/alloy/latest/collect/prometheus-metrics/
- https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/

## Same task, two SDKs

**Datadog**

```
# Every tag value pair is its own billable series on Datadog.
from datadog import statsd

def checkout(cart_id: str, user_id: str, items: int) -> None:
    statsd.increment("checkout.completed", tags=[f"user_id:{user_id}"])
    statsd.gauge("checkout.items", items, tags=[f"cart_id:{cart_id}"])
# Breaks when: user_id has 50,000 values. That is 50,000 custom series,
# against an allowance of 100 per host — 500 hosts' worth of licence for one tag.
```

**Grafana Cloud**

```
# Same job, same mistake: cardinality is the meter, not the vendor.
from prometheus_client import Counter, Gauge, start_http_server

checkout = Counter("checkout_completed_total", "Checkouts", ["user_id"])
items = Gauge("checkout_items", "Items per cart", ["cart_id"])
start_http_server(9100)

checkout.labels(user_id="u_123").inc()  # one time series per label value
# Breaks first here: 50,000 user_id values are 50,000 series on Grafana Cloud too,
# and the 10,000-series allowance ends long before the first page of users.
```
