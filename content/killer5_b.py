"""Killer comparison batch B: monitoring, serverless and email pricing."""

DATADOG = {
    "slug": "datadog-vs-grafana-cloud",
    "category": "Monitoring & Observability",
    "last_verified": "2026-11-10",
    "published": "2026-11-10",
    "hook": (
        "Twenty hosts and 5,000 custom series bill $450 a month on Datadog and $19 on Grafana "
        "Cloud's Pro plan. The difference is not the per-series rate. It is that only one of them "
        "puts the hosts on the invoice."
    ),
    "sections": [
        {
            "title": "One sells a host, the other sells a series",
            "content": (
                "Datadog's infrastructure line is a licence: $15 per host per month billed annually, "
                "$18 month-to-month, and every licence carries 100 custom metrics. Grafana Cloud's "
                "Pro plan is a $19 platform fee for the whole account, with 10,000 active series and "
                "50 GB of logs inside it.\n\n"
                "That is the whole philosophical difference, and it decides the invoice shape:\n\n"
                "- **Datadog:** cost grows with machines first, then with the cardinality of what "
                "you send from them.\n"
                "- **Grafana Cloud:** cost is flat until you pass the account-level allowances, then "
                "grows with data volume only.\n\n"
                "Neither page hides this. It is written in the billing unit, which is the one line "
                "worth reading before the price."
            ),
        },
        {
            "title": "The custom metrics line is the one that grows without a deploy",
            "content": (
                "Per unit, Datadog's custom metrics cost $5 per 100 per month, which is $50 per "
                "1,000. Grafana Cloud's first paid band is $6.50 per 1,000, then $5.90 above 100,000 "
                "and $5.50 above 200,000.\n\n"
                "| Meter | Datadog Infrastructure Pro | Grafana Cloud Pro |\n|---|---|---|\n"
                "| Base | $15 per host per month, annual | $19 per account per month |\n"
                "| Included series | 100 per host | 10,000 per account |\n"
                "| Series beyond that | $5 per 100 | $6.50 per 1,000 |\n"
                "| Effective per 1,000 | $50.00 | $6.50 |\n\n"
                "Datadog's rate is 7.7 times Grafana's, and the allotment it ships with is 100 times "
                "smaller. Those two numbers pull in opposite directions, so the bill depends on "
                "whether your cardinality scales with hosts or with users."
            ),
        },
        {
            "title": "Two shops, and the same four numbers",
            "content": (
                "Shop one: 20 hosts, 5,000 custom series.\n\n"
                "| Line | Datadog | Grafana Cloud |\n|---|---|---|\n"
                "| Platform or hosts | 20 × $15 = $300 | $19 |\n"
                "| Billable series | 5,000 − 2,000 = 3,000 | 0 (5,000 under 10,000) |\n"
                "| Series cost | 30 × $5 = $150 | $0 |\n"
                "| **Total** | **$450** | **$19** |\n\n"
                "Shop two: 20 hosts, 200,000 custom series, which is what a `user_id` tag does to a "
                "counter.\n\n"
                "| Line | Datadog | Grafana Cloud |\n|---|---|---|\n"
                "| Platform or hosts | $300 | $19 |\n"
                "| Billable series | 198,000 | 190,000 |\n"
                "| Series cost | 1,980 × $5 = $9,900 | 90,000 × $6.50/1k + 100,000 × $5.90/1k = $1,175 |\n"
                "| **Total** | **$10,200** | **$1,194** |\n\n"
                "The second table is the one that arrives without a deploy, a migration or a new "
                "service. It arrives the week someone adds a tag."
            ),
        },
        {
            "title": "Logs: one vendor counts bytes, the other counts events",
            "content": (
                "This is where the two sheets stop being directly comparable. Datadog charges $0.10 "
                "per ingested GB, then $1.70 per million indexed events at 15-day retention or $2.50 "
                "at 30-day. Grafana charges three meters per GB: $0.05 to process, $0.40 to write and "
                "$0.10 to retain, with 50 GB included.\n\n"
                "Take 500 GB a month at roughly 2.5 KB per event, or 200 million events, indexed for "
                "30 days.\n\n"
                "| Meter | Datadog | Grafana Cloud |\n|---|---|---|\n"
                "| Ingest | 500 GB × $0.10 = $50 | 450 GB × $0.05 = $22.50 |\n"
                "| Index and retain | 200M × $2.50/M = $500 | 450 GB × $0.40 = $180 |\n"
                "| Retention | included in the index rate | 450 GB × $0.10 = $45 |\n"
                "| **Total** | **$550** | **$247.50** |\n\n"
                "The event meter rewards fat logs and the byte meter rewards few of them. The same "
                "500 GB is $550 or $247.50 depending on which unit your logging happens to satisfy."
            ),
        },
        {
            "title": "Both vendors now discount you for deleting tags",
            "content": (
                "Datadog sells Metrics without Limits, which splits one number into two: ingested "
                "custom metrics at $0.10 per 100, and indexed ones at $5 per 100. Grafana ships "
                "Adaptive Metrics, which aggregates and drops unused series, and the page states the "
                "claim as the vendor's own: up to 80%.\n\n"
                "Read that as an admission. When a vendor builds a product whose only job is to delete "
                "time series before they reach the meter, the meter is cardinality, and the vendor "
                "knows the cardinality is often junk.\n\n"
                "The practical move costs nothing:\n\n"
                "1. Sort your metrics by tag value count, not by metric name.\n"
                "2. Drop any tag whose values scale with users, carts or request ids.\n"
                "3. Re-count before you negotiate a discount, because the discount is priced on the "
                "number you can already fix."
            ),
        },
        {
            "title": "What the switch actually costs",
            "content": (
                "Grafana Cloud speaks Prometheus for metrics, Loki for logs and Tempo for traces, so "
                "an application already instrumented with a Prometheus client can point at a remote "
                "write endpoint and stop. Datadog's agent, dashboards, monitors and APM traces do not "
                "translate: every dashboard is a rebuild, and every monitor needs a PromQL "
                "equivalent.\n\n"
                "Retention also moves. Datadog keeps full-resolution metrics for 15 months on Pro; "
                "Grafana's Pro plan lists 13 months for metrics and 30 days for logs, traces, profiles "
                "and k6 tests.\n\n"
                "The reverse move is the expensive direction for a small team: going to Datadog means "
                "adopting a per-host licence where Grafana charged per account, so the same twenty "
                "hosts start at $300 before a single custom metric."
            ),
        },
    ],
    "cost_math": [
        {
            "label": "20 hosts, 5,000 custom series",
            "formula": "Datadog: 20 × $15 = $300, plus (5,000 − 20 × 100) = 3,000 series ÷ 100 × $5 = $150. Grafana: $19 platform fee, 5,000 under the 10,000 allowance",
            "result": "$450 on Datadog against $19 on Grafana Cloud Pro",
        },
        {
            "label": "20 hosts, 200,000 custom series",
            "formula": "Datadog: $300 + (200,000 − 2,000) ÷ 100 × $5 = $9,900. Grafana: $19 + 90,000 × $6.50/1,000 = $585 + 100,000 × $5.90/1,000 = $590",
            "result": "$10,200 on Datadog against $1,194 on Grafana Cloud Pro",
        },
        {
            "label": "500 GB of logs a month, 200M events, 30-day retention",
            "formula": "Datadog: 500 × $0.10 = $50 ingest, plus 200M ÷ 1M × $2.50 = $500 indexed. Grafana: 450 GB over the 50 GB allowance × ($0.05 + $0.40 + $0.10) = $247.50",
            "result": "$550 on Datadog against $247.50 on Grafana Cloud Pro",
        },
        {
            "label": "30 hosts with APM on Datadog",
            "formula": "30 × ($15 infrastructure + $31 APM) = 30 × $46 = $1,380 per month at annual rates",
            "result": "$1,380 before logs, traces or RUM; Grafana Cloud Pro has no per-host infrastructure line",
        },
    ],
    "decision_matrix": [
        {
            "situation": "Series count scales with users, not hosts",
            "pick": "Grafana Cloud",
            "why": "At 200,000 series the series meter bills $9,900 on Datadog against $1,175 on Grafana, and the 10,000-series allowance is account-wide.",
        },
        {
            "situation": "A team already living in Datadog APM and security",
            "pick": "Datadog",
            "why": "At 30 hosts the infrastructure plus APM licence is $1,380, and rebuilding dashboards and monitors is the hidden cost of leaving.",
        },
        {
            "situation": "Five hosts and one person on call",
            "pick": "Grafana Cloud",
            "why": "Datadog's licence starts at $75 for five hosts before any custom metrics; Grafana's platform fee is $19 for the account.",
        },
        {
            "situation": "You need 15 months of full-resolution metrics",
            "pick": "Datadog",
            "why": "Datadog keeps 15 months on Pro; Grafana Cloud Pro lists 13 months for metrics and 30 days for logs and traces.",
        },
        {
            "situation": "The custom metrics line is already over $500",
            "pick": "Grafana Cloud",
            "why": "That line is $500 per 10,000 series on Datadog and $65 per 10,000 on Grafana, so the same data crosses a factor of 7.7.",
        },
        {
            "situation": "Logs are verbose JSON from a dozen services",
            "pick": "Compute both before choosing",
            "why": "Datadog's index rate is per event and Grafana's is per GB, so 500 GB at 2.5 KB per event bills $550 against $247.50, and the same 500 GB at 250 bytes per event is 2 billion events, or $5,000 on the index line.",
        },
        {
            "situation": "Security, SIEM and audit on one invoice",
            "pick": "Datadog",
            "why": "Cloud SIEM, workload protection and audit trail are on the same price list; Grafana Cloud prices observability and leaves security elsewhere.",
        },
        {
            "situation": "Everything is already Prometheus and you self-host Grafana",
            "pick": "Grafana Cloud, or keep self-hosting",
            "why": "The remote-write path means no re-instrumentation, and the open-source stack is the same software the paid plan runs.",
        },
    ],
    "verdict_summary": (
        "Grafana Cloud wins every version of this bill where the data is the problem, and the margin "
        "is an order of magnitude once cardinality passes the 10,000-series allowance. Datadog wins "
        "where the workflow is the product: one agent, one APM trace, one security screen, and a team "
        "that already knows where to click. If your custom metrics line is a typo away from $10,000, "
        "the migration pays for itself in a quarter."
    ),
    "migration_guide": (
        "Self-hosted or Grafana Cloud, the instrumentation is the portable part: a Prometheus client "
        "library pushes to a remote-write endpoint, and the same client keeps working on either. "
        "Datadog's agent can also forward to a Prometheus-compatible backend, so the first phase is "
        "usually dual-writing while you rebuild dashboards.\n\n"
        "The rebuild is the cost. Datadog dashboards, monitors and APM traces have no export format "
        "for Grafana, and every alert needs a PromQL translation with its own threshold review. Plan "
        "the monitor rewrite as its own project; the metrics are the easy half, which is why teams "
        "that switch usually run both systems for a quarter."
    ),
    "faqs": [
        {
            "q": "Are Grafana Cloud's tier prices marginal or flat?",
            "a": "Marginal. Each new band bills at a lower rate for the usage inside it, so the blended rate falls as the account grows: $6.50 per 1,000 to 100,000, then $5.90, then $5.50.",
        },
        {
            "q": "What exactly is a custom metric on Datadog?",
            "a": "A unique metric name plus tag combination, averaged hourly across the month. Adding a tag with many values multiplies the count even if the metric name never changes.",
        },
        {
            "q": "Does Grafana Cloud charge per host?",
            "a": "The Pro plan is a $19 platform fee per account. Host hours appear for Kubernetes monitoring at $0.01 per host hour, which is a separate product from infrastructure metrics.",
        },
        {
            "q": "Can I keep 30-day logs on Grafana Cloud?",
            "a": "Yes. Pro includes 30 days of log retention inside the platform fee, with 50 GB of ingest included and $0.55 per GB across the process, write and retain meters after that.",
        },
    ],
    "sources": [
        "https://www.datadoghq.com/pricing/",
        "https://www.datadoghq.com/pricing/list/",
        "https://docs.datadoghq.com/account_management/billing/custom_metrics/",
        "https://grafana.com/pricing/",
        "https://grafana.com/docs/grafana-cloud/adaptive-telemetry/adaptive-metrics/",
    ],
    "related": [
        {"slug": "aws-lambda-vs-cloudflare-workers", "name": "AWS Lambda vs Cloudflare Workers", "why": "Another invoice where the billing unit, not the price, decides the total."},
        {"slug": "stripe-vs-lemonsqueezy-vs-paddle", "name": "Stripe vs Lemon Squeezy / Paddle", "why": "Four meters on one invoice, and the sticker price covers one of them."},
    ],
    "tool_a": {
        "name": "Datadog",
        "tagline": "Per-host licences with a custom-metric meter on top",
        "db": "SaaS telemetry: infrastructure, APM, logs, security and RUM",
        "pricing": "Infrastructure Pro $15/host/mo annual ($18 monthly) · custom metrics $5 per 100 · logs $0.10/GB + $1.70 per 1M at 15 days",
        "self_host": "No (hosted SaaS, agent-based collection)",
        "realtime": "15 months of full-resolution metrics; 15-day log and trace search",
        "ai_readiness": "Bits AI credits from $500, with per-action credit estimates",
        "lock_in": "High: dashboards, monitors and APM traces have no export to another backend",
        "badge": "Per host",
        "cta_url": "https://www.datadoghq.com/?utm_source=devteardown",
        "pros": [
            "One agent covers infrastructure, APM, logs and security, so the product surface is the reason teams stay",
            "100 custom metrics ride along with every host licence, which covers a well-behaved service",
            "Metrics without Limits decouples ingest from index, so you can keep sending and stop paying full price",
            "15 months of full-resolution retention on Pro is the longest on either price sheet",
        ],
        "cons": [
            "The host licence bills machines you did not grow, so a fleet of small instances pays per instance",
            "Custom metrics at $5 per 100 is $50 per 1,000, after an allowance of just 100 per host",
            "Logs are metered twice, on ingest and on indexed events, and the event count follows log size",
            "APM is a second per-host licence at $31, so a monitored host is $46 before logs",
        ],
        "code_example": (
            "# Every tag value pair is its own billable series on Datadog.\n"
            "from datadog import statsd\n\n"
            "def checkout(cart_id: str, user_id: str, items: int) -> None:\n"
            "    statsd.increment(\"checkout.completed\", tags=[f\"user_id:{user_id}\"])\n"
            "    statsd.gauge(\"checkout.items\", items, tags=[f\"cart_id:{cart_id}\"])\n"
            "# Breaks when: user_id has 50,000 values. That is 50,000 custom series,\n"
            "# against an allowance of 100 per host — 500 hosts' worth of licence for one tag."
        ),
    },
    "tool_b": {
        "name": "Grafana Cloud",
        "tagline": "One platform fee, then per-series and per-GB meters",
        "db": "Managed Prometheus, Loki, Tempo and Mimir behind Grafana dashboards",
        "pricing": "Pro $19/mo platform fee · 10,000 series and 50 GB logs included · $6.50 per 1k series after",
        "self_host": "Yes (Grafana, Loki, Mimir and Tempo are open source)",
        "realtime": "13 months of metrics on Pro; 30 days for logs, traces, profiles and k6 tests",
        "ai_readiness": "AI Assistant and Adaptive Telemetry included on Free and Pro",
        "lock_in": "Low: Prometheus remote write in, dashboards and data out",
        "badge": "Per series",
        "cta_url": "https://grafana.com/?utm_source=devteardown",
        "pros": [
            "The account-level fee means machines are free: twenty hosts cost the same as two",
            "10,000 included series cover most small deployments with no custom-metric line at all",
            "Tiered marginal rates mean the effective price falls as volume grows, to $5.50 per 1,000",
            "Prometheus, Loki and Tempo are open source, so the paid plan runs software you can also host",
        ],
        "cons": [
            "The series rate is cheaper but the 10,000-series allowance is shared by every metric in the account",
            "Traces, profiles and logs all meter GB, so a verbose log line is a billable byte",
            "There is no Datadog-equivalent APM product on the Pro sheet, so trace-based debugging is a rebuild",
            "Metrics retention is 13 months against Datadog's 15, which matters for year-over-year comparisons",
        ],
        "code_example": (
            "# Same job, same mistake: cardinality is the meter, not the vendor.\n"
            "from prometheus_client import Counter, Gauge, start_http_server\n\n"
            "checkout = Counter(\"checkout_completed_total\", \"Checkouts\", [\"user_id\"])\n"
            "items = Gauge(\"checkout_items\", \"Items per cart\", [\"cart_id\"])\n"
            "start_http_server(9100)\n\n"
            "checkout.labels(user_id=\"u_123\").inc()  # one time series per label value\n"
            "# Breaks first here: 50,000 user_id values are 50,000 series on Grafana Cloud too,\n"
            "# and the 10,000-series allowance ends long before the first page of users."
        ),
    },
}


WORKERS = {
    "slug": "aws-lambda-vs-cloudflare-workers",
    "category": "Serverless & Edge",
    "last_verified": "2026-11-10",
    "published": "2026-11-10",
    "hook": (
        "One hundred million requests that each take 200 ms and use 10 ms of CPU cost $147.80 on "
        "AWS Lambda and $51.40 on Cloudflare Workers. Nothing about the code differs. One vendor "
        "bills the waiting."
    ),
    "sections": [
        {
            "title": "Two vendors, three meters, two definitions of work",
            "content": (
                "Lambda now publishes two price sheets. Event Functions bill requests plus duration "
                "in GB-seconds: $0.0000133334 per GB-second on Arm, $0.0000166667 on x86, and $0.20 "
                "per million requests. Web Functions bill active CPU at $0.0000276944 per vCPU-second, "
                "memory at $0.0000036667 per GB-second for as long as the environment exists, and "
                "$0.30 per million requests.\n\n"
                "Workers bill one thing that matters: CPU milliseconds, $0.02 per million after 30 "
                "million included, plus $0.30 per million requests after 10 million on a $5 plan. "
                "The page is explicit that there is no charge for duration, for egress or for "
                "bandwidth.\n\n"
                "| Meter | Lambda Event | Lambda Web | Workers |\n|---|---|---|---|\n"
                "| Requests | $0.20/M | $0.30/M | $0.30/M |\n"
                "| Duration | GB-seconds | memory GB-s, whole life | none |\n"
                "| CPU | inside duration | $0.0000276944/vCPU-s | $0.02/M CPU-ms |"
            ),
        },
        {
            "title": "A GB-second is a memory meter wearing a clock",
            "content": (
                "Duration billing multiplies wall time by allocated memory, and both factors are "
                "yours to set. A 512 MB function that takes 200 ms bills 0.5 GB × 0.2 s = 0.1 GB-s "
                "per request. At 100 million requests that is 10 million GB-seconds, or $133.34 on Arm "
                "at $0.0000133334.\n\n"
                "Workers bills the 10 ms of actual work instead: 100 million × 10 ms = 1,000 million "
                "CPU-milliseconds, which is 970 million after the 30 million included, at $0.02 per "
                "million CPU-ms = $19.40.\n\n"
                "So the ratio between the two vendors is not a rate difference. It is the fraction of "
                "the request that is CPU: 10 ms of 200 ms is 5%, and that 5% is what Workers meters. "
                "Make the handler heavier and the gap narrows; make it wait on a database and the gap "
                "widens."
            ),
        },
        {
            "title": "The bills cross at about 7.5 million requests",
            "content": (
                "Same shape everywhere below: 200 ms duration, 512 MB, 10 ms of CPU, one function.\n\n"
                "| Requests/month | Lambda Event (Arm) | Workers | Cheaper |\n|---|---|---|---|\n"
                "| 5M | $0.80 + $1.33 = $2.13 | $5.00 + $0.40 = $5.40 | Lambda |\n"
                "| 7.5M | $1.30 + $4.67 = $5.97 | $5.00 + $0.90 = $5.90 | Workers, by 7¢ |\n"
                "| 10M | $1.80 + $8.00 = $9.80 | $5.00 + $1.40 = $6.40 | Workers |\n"
                "| 50M | $9.80 + $61.33 = $71.13 | $5.00 + $12.00 + $9.40 = $26.40 | Workers |\n"
                "| 100M | $19.80 + $128.00 = $147.80 | $5.00 + $27.00 + $19.40 = $51.40 | Workers |\n\n"
                "The crossover is a free-tier artefact, not a policy: 1 million requests and 400,000 "
                "GB-seconds are free on Lambda, and 30 million CPU-ms are free on Workers. Below "
                "roughly 7.5 million requests the Lambda allowance is worth more than the CPU "
                "savings. Above it, the $5 plan floor disappears into the noise."
            ),
        },
        {
            "title": "Lambda's second sheet splits the same request in two",
            "content": (
                "Web Functions are AWS's answer to active-CPU billing, and they price the same 100 "
                "million requests differently.\n\n"
                "| Line | Lambda Event | Lambda Web | Workers |\n|---|---|---|---|\n"
                "| Requests | $19.80 | $30.00 | $27.00 |\n"
                "| Compute | 10M GB-s = $128.00 | 1M vCPU-s = $27.69, 1.296M GB-s = $4.75 | 970M CPU-ms = $19.40 |\n"
                "| Plan floor | — | — | $5.00 |\n"
                "| **Total** | **$147.80** | **$62.45** | **$51.40** |\n\n"
                "Web Functions bill $62.45 for the same traffic, 42% of the Event price, and still "
                "21% above the Workers bill. The memory meter is why: it bills the "
                "environment for its whole life, idle time included, and AWS's own examples quietly "
                "assume exactly one environment stays up for the entire month."
            ),
        },
        {
            "title": "Where Lambda wins on the same sheet",
            "content": (
                "The free tier, for one. Five million requests a month cost $2.13 on Lambda and "
                "$5.40 on Workers, and a hobby project that sends three million costs $2.73 by AWS's "
                "own worked example.\n\n"
                "Memory ceiling is the second. Lambda allocates up to 10,240 MB per function, which "
                "covers a model that will not fit in a V8 isolate. Workers caps a single invocation "
                "at 5 minutes of CPU, 30 seconds by default.\n\n"
                "The third is everything around the function: VPC access, IAM, SQS, Kinesis, "
                "Step Functions and the rest of the event-source catalogue. On an AWS shop, the "
                "compute line is frequently cheaper than the integration you would rewrite to leave "
                "it."
            ),
        },
        {
            "title": "The exit door has a rewrite behind it",
            "content": (
                "Workers runs JavaScript on V8 with a fetch-shaped API. A Lambda handler that imports "
                "a native module, spawns a process or needs a writable filesystem does not run there, "
                "and the 5-minute CPU cap is not negotiable with a support ticket.\n\n"
                "The reverse move is easier and still not free: Workers' egress is $0 and Lambda's is "
                "not, so a byte-heavy service that moves back to Lambda picks up a data transfer line "
                "it never had.\n\n"
                "Price the traffic, not the platform. If your p50 request spends most of its time "
                "waiting on a database, the CPU meter is the cheaper meter and the rewrite is the only "
                "real cost. If your requests are heavy, synchronous and mostly compute, the two bills "
                "converge and the free tier decides."
            ),
        },
    ],
    "cost_math": [
        {
            "label": "100M requests at 200 ms, 512 MB, 10 ms CPU",
            "formula": "Lambda Event Arm: 100M × 0.2 s × 0.5 GB = 10M GB-s, minus 400k free = 9.6M × $0.0000133334 = $128.00, plus 99M × $0.20/M = $19.80. Workers: (100M − 10M) × $0.30/M = $27.00, plus (1,000M − 30M) CPU-ms × $0.02/M = $19.40, plus $5.00",
            "result": "$147.80 on Lambda against $51.40 on Workers",
        },
        {
            "label": "The same traffic on Lambda Web Functions",
            "formula": "100M × 10 ms = 1M vCPU-s × $0.0000276944 = $27.69; 0.5 GB × 2,592,000 s = 1,296,000 GB-s × $0.0000036667 = $4.75; 100M × $0.30/M = $30.00",
            "result": "$62.45, 58% below Lambda's own Event price for identical traffic",
        },
        {
            "label": "Cross-over against Lambda's free tier",
            "formula": "Lambda: (R − 1M) × $0.20/M + (R × 0.1 − 400k) × $0.0000133334. Workers: $5 + (R × 10 − 30M) × $0.02/M",
            "result": "Equal at about 7.5M requests a month; below that Lambda's free allowance wins, above it the CPU meter does",
        },
        {
            "label": "Replacing a 200 ms wait with a 1 s wait",
            "formula": "At 10M requests: Lambda 10M × 1 s × 0.5 GB = 5M GB-s − 400k = 4.6M × $0.0000133334 = $61.33 + $1.80. Workers CPU is unchanged at 10M × 200 ms = 2,000M − 30M × $0.02/M = $39.40 + $5",
            "result": "$63.13 against $44.40: the slower request costs Lambda $53 more and Workers nothing",
        },
    ],
    "decision_matrix": [
        {
            "situation": "Under about 5 million requests a month",
            "pick": "Lambda Event Functions",
            "why": "The 1M-request and 400,000 GB-second free allowances cover the whole job: 5M requests at 200 ms and 512 MB price at $2.13 against $5.40 on Workers.",
        },
        {
            "situation": "100 million requests that mostly wait on I/O",
            "pick": "Workers",
            "why": "The same shape prices at $51.40 against $147.80, because 10 ms of CPU out of a 200 ms request is all Workers meters.",
        },
        {
            "situation": "A function that needs 10 GB of memory",
            "pick": "Lambda",
            "why": "Lambda allocates up to 10,240 MB; Workers caps a single invocation at 5 minutes of CPU and runs in an isolate with a far smaller footprint.",
        },
        {
            "situation": "Long-lived streaming to a browser",
            "pick": "Lambda Web Functions",
            "why": "Active-CPU billing ignores the wait: AWS's own LLM streaming example prices 5M requests of 3 s at $33.94, against $101.00 as Event Functions.",
        },
        {
            "situation": "Byte-heavy responses at the edge",
            "pick": "Workers",
            "why": "Workers charges nothing for egress or bandwidth, and static asset requests are free and unlimited.",
        },
        {
            "situation": "SQS, Kinesis, VPC and IAM already wired into the app",
            "pick": "Lambda",
            "why": "The compute line is often the small one; rewriting event sources and IAM to leave AWS costs more than the difference on the invoice.",
        },
        {
            "situation": "A cron job every hour, minutes of CPU each",
            "pick": "Workers",
            "why": "Cloudflare's own example prices 720 invocations at 180,000 ms CPU each at $6.99, and duration is not a meter at all.",
        },
        {
            "situation": "Traffic so spiky that one environment cannot serve it",
            "pick": "Lambda Event Functions",
            "why": "Web Functions bill memory for the life of every environment, and the pricing examples quietly assume exactly one environment runs all month.",
        },
    ],
    "verdict_summary": (
        "For a request that waits, Workers is two to three times cheaper and the gap grows with every "
        "millisecond you spend on a database call. For a request that works, the two converge, and "
        "Lambda's free tier and memory ceiling win back the low end. The bill is a statement about "
        "your code's shape, not about the vendors' rates."
    ),
    "migration_guide": (
        "Lambda to Workers is a runtime rewrite: the handler becomes a fetch listener, environment "
        "variables become bindings, and anything that needs a native module, a spawned process or a "
        "writable disk has no equivalent. State moves to Durable Objects or KV, which bill separately.\n\n"
        "Workers to Lambda is smaller but not free: package the code, replace KV and Durable Objects "
        "with a database, and accept that egress is metered again. In both directions the traffic "
        "analysis comes first, because the arithmetic only favours one vendor when you know the "
        "request duration and the CPU share of it."
    ),
    "faqs": [
        {
            "q": "Does Workers really charge nothing for duration?",
            "a": "The pricing page states there is no charge or limit for duration and no charge for data transfer or bandwidth. Only CPU milliseconds and requests are metered.",
        },
        {
            "q": "What are Lambda Web Functions?",
            "a": "A second Lambda billing model that charges per request, per vCPU-second of active CPU and per GB-second of memory for as long as the execution environment exists.",
        },
        {
            "q": "Which free tier is bigger?",
            "a": "Lambda's, in dollar terms at low volume: 1 million requests and 400,000 GB-seconds against Workers' 10 million requests and 30 million CPU-milliseconds on the $5 plan.",
        },
        {
            "q": "Is a cold start billed?",
            "a": "On Event Functions the initialisation runs inside the billed duration, and SnapStart adds its own cache and restore charges. Workers does not bill duration at all.",
        },
    ],
    "sources": [
        "https://aws.amazon.com/lambda/pricing/",
        "https://developers.cloudflare.com/workers/platform/pricing/",
        "https://developers.cloudflare.com/workers/platform/limits/",
        "https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html",
        "https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html",
    ],
    "related": [
        {"slug": "datadog-vs-grafana-cloud", "name": "Datadog vs Grafana Cloud", "why": "The same reading exercise on a monitoring bill: find the unit, then the formula."},
        {"slug": "anthropic-vs-openai-api-pricing", "name": "Anthropic vs OpenAI API pricing", "why": "Two vendors, identical stickers, and the invoice decided by a token count."},
    ],
    "tool_a": {
        "name": "AWS Lambda",
        "tagline": "Two bills in one product: duration and active CPU",
        "db": "Event Functions bill duration in GB-seconds; Web Functions bill active CPU plus memory",
        "pricing": "Event: $0.20/M requests + $0.0000133334/GB-s Arm · Web: $0.30/M + $0.0000276944/vCPU-s + $0.0000036667/GB-s",
        "self_host": "No (AWS-managed, VPC and IAM integrated)",
        "realtime": "Free tier 1M requests and 400,000 GB-s; 10,240 MB memory ceiling",
        "ai_readiness": "Durable functions at $8 per million operations; streaming priced per GB written",
        "lock_in": "Medium: event sources, IAM and VPC wiring are AWS-shaped",
        "badge": "GB-seconds",
        "cta_url": "https://aws.amazon.com/lambda/?utm_source=devteardown",
        "pros": [
            "Free tier covers a small service outright: 1M requests and 400,000 GB-seconds each month",
            "Up to 10,240 MB of memory per function, which a V8 isolate cannot match",
            "Event Functions, MicroVMs, Web Functions and durable functions are all one integration",
            "The event-source catalogue is the reason teams stay: SQS, Kinesis and Step Functions in one IAM model",
        ],
        "cons": [
            "GB-second billing multiplies wall time by memory, so a request that waits still bills",
            "Web Functions fix the wait but bill memory for the life of every environment, idle included",
            "Requests cost $0.20/M on Event Functions and $0.30/M on Web Functions, above Workers' $0.30 after 10M included",
            "Data transfer is metered, so a byte-heavy response is a billable event",
        ],
        "code_example": (
            "// Event Function: the meter starts at invocation and runs through the wait.\n"
            "export const handler = async (event) => {\n"
            "  const user = await db.users.findUnique({ where: { id: event.userId } }); // 180 ms here\n"
            "  const digest = render(user);                                            // 10 ms here\n"
            "  return { statusCode: 200, body: digest };\n"
            "};\n"
            "// Breaks when: the lookup takes 1 s. You are billed 1.01 s of 512 MB, so the wait\n"
            "// is 99% of the invoice. Web Functions bill only the 10 ms of active CPU."
        ),
    },
    "tool_b": {
        "name": "Cloudflare Workers",
        "tagline": "A flat $5 and a CPU meter, with no duration line",
        "db": "V8 isolates at the edge: CPU time is the only compute meter",
        "pricing": "$5/mo minimum · 10M requests included then $0.30/M · 30M CPU-ms included then $0.02/M",
        "self_host": "No managed equivalent; workerd is open source",
        "realtime": "Free: 100,000 requests/day and 10 ms CPU per invocation; paid: 5-minute CPU ceiling",
        "ai_readiness": "Durable Objects, KV, Queues and Workflows meter separately; static assets are free",
        "lock_in": "Low on compute, higher on state: Durable Objects hold data inside the product",
        "badge": "CPU-ms",
        "cta_url": "https://workers.cloudflare.com/?utm_source=devteardown",
        "pros": [
            "No charge for duration, egress or bandwidth, which removes the line that surprises AWS bills",
            "The $5 plan includes 10M requests and 30M CPU-ms, enough for a real product to start",
            "Static asset requests are free and unlimited, so a Worker-fronted site pays for the API only",
            "Caching at the edge cuts CPU without cutting the request, and only the request is billed",
        ],
        "cons": [
            "A 5-minute CPU ceiling per invocation, 30 seconds by default, with no ticket that lifts it",
            "The runtime is not a container: native modules, spawned processes and writable disks do not run",
            "Memory is an isolate-sized budget rather than a configurable 10 GB",
            "At very low volume the $5 floor is more than Lambda's free tier charges",
        ],
        "code_example": (
            "// Workers: nothing here is billed by the clock, only the CPU this code burns.\n"
            "export default {\n"
            "  async fetch(request, env) {\n"
            "    const userId = new URL(request.url).searchParams.get(\"id\");\n"
            "    const user = await env.DB.prepare(\"SELECT * FROM users WHERE id = ?\")\n"
            "      .bind(userId).first();            // 180 ms of waiting, not billed\n"
            "    return new Response(render(user), {\n"
            "      headers: { \"content-type\": \"text/html\" },\n"
            "    });\n"
            "  },\n"
            "};\n"
            "// Breaks when: render() parses a 5 MB XML feed on every request. CPU is the meter,\n"
            "// and the 30M CPU-ms allowance is 30 million milliseconds of exactly that."
        ),
    },
}
