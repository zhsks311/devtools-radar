"""Monitoring and serverless comparisons."""

DATADOG = {'slug': 'datadog-vs-grafana-cloud',
 'category': 'Monitoring & Observability',
 'last_verified': '2026-11-14',
 'published': '2026-11-10',
 'hook': 'Twenty hosts and 5,000 custom series bill $450 a month on Datadog and $19 on Grafana '
         "Cloud's Pro plan. The difference is not the per-series rate. It is that only one of them "
         'puts the hosts on the invoice.',
 'sections': [{'title': 'One sells a host, the other sells a series',
               'content': "Datadog's infrastructure line is a licence: $15 per host per month "
                          'billed annually, $18 month-to-month, and every licence carries 100 '
                          "custom metrics. Grafana Cloud's Pro plan is a $19 platform fee for the "
                          'whole account, with 10,000 active series and 50 GB of logs inside it.\n'
                          '\n'
                          'That is the whole philosophical difference, and it decides the invoice '
                          'shape:\n'
                          '\n'
                          '- **Datadog:** cost grows with machines first, then with the '
                          'cardinality of what you send from them.\n'
                          '- **Grafana Cloud:** cost is flat until you pass the account-level '
                          'allowances, then grows with data volume only.\n'
                          '\n'
                          'Neither page hides this. It is written in the billing unit, which is '
                          'the one line worth reading before the price.'},
              {'title': 'The custom metrics line is the one that grows without a deploy',
               'content': "Per unit, Datadog's custom metrics cost $5 per 100 per month, which is "
                          "$50 per 1,000. Grafana Cloud's first paid band is $6.50 per 1,000, then "
                          '$5.90 above 100,000 and $5.50 above 200,000.\n'
                          '\n'
                          '| Meter | Datadog Infrastructure Pro | Grafana Cloud Pro |\n'
                          '|---|---|---|\n'
                          '| Base | $15 per host per month, annual | $19 per account per month |\n'
                          '| Included series | 100 per host | 10,000 per account |\n'
                          '| Series beyond that | $5 per 100 | $6.50 per 1,000 |\n'
                          '| Effective per 1,000 | $50.00 | $6.50 |\n'
                          '\n'
                          "Datadog's rate is 7.7 times Grafana's, and the allotment it ships with "
                          'is 100 times smaller. Those two numbers pull in opposite directions, so '
                          'the bill depends on whether your cardinality scales with hosts or with '
                          'users.'},
              {'title': 'Two shops, and the same four numbers',
               'content': 'Shop one: 20 hosts, 5,000 custom series.\n'
                          '\n'
                          '| Line | Datadog | Grafana Cloud |\n'
                          '|---|---|---|\n'
                          '| Platform or hosts | 20 × $15 = $300 | $19 |\n'
                          '| Billable series | 5,000 − 2,000 = 3,000 | 0 (5,000 under 10,000) |\n'
                          '| Series cost | 30 × $5 = $150 | $0 |\n'
                          '| **Total** | **$450** | **$19** |\n'
                          '\n'
                          'Shop two: 20 hosts, 200,000 custom series, which is what a `user_id` '
                          'tag does to a counter.\n'
                          '\n'
                          '| Line | Datadog | Grafana Cloud |\n'
                          '|---|---|---|\n'
                          '| Platform or hosts | $300 | $19 |\n'
                          '| Billable series | 198,000 | 190,000 |\n'
                          '| Series cost | 1,980 × $5 = $9,900 | 90,000 × $6.50/1k + 100,000 × '
                          '$5.90/1k = $1,175 |\n'
                          '| **Total** | **$10,200** | **$1,194** |\n'
                          '\n'
                          'The second table is the one that arrives without a deploy, a migration '
                          'or a new service. It arrives the week someone adds a tag.'},
              {'title': 'Logs: one vendor counts bytes, the other counts events',
               'content': 'This is where the two sheets stop being directly comparable. Datadog '
                          'charges $0.10 per ingested GB, then $1.70 per million indexed events at '
                          '15-day retention or $2.50 at 30-day. Grafana charges three meters per '
                          'GB: $0.05 to process, $0.40 to write and $0.10 to retain, with 50 GB '
                          'included.\n'
                          '\n'
                          'Take 500 GB a month at roughly 2.5 KB per event, or 200 million events, '
                          'indexed for 30 days.\n'
                          '\n'
                          '| Meter | Datadog | Grafana Cloud |\n'
                          '|---|---|---|\n'
                          '| Ingest | 500 GB × $0.10 = $50 | 450 GB × $0.05 = $22.50 |\n'
                          '| Index and retain | 200M × $2.50/M = $500 | 450 GB × $0.40 = $180 |\n'
                          '| Retention | included in the index rate | 450 GB × $0.10 = $45 |\n'
                          '| **Total** | **$550** | **$247.50** |\n'
                          '\n'
                          'The event meter rewards fat logs and the byte meter rewards few of '
                          'them. The same 500 GB is $550 or $247.50 depending on which unit your '
                          'logging happens to satisfy.'},
              {'title': 'Both vendors now discount you for deleting tags',
               'content': 'Datadog sells Metrics without Limits, which splits one number into two: '
                          'ingested custom metrics at $0.10 per 100, and indexed ones at $5 per '
                          '100. Grafana ships Adaptive Metrics, which aggregates and drops unused '
                          "series, and the page states the claim as the vendor's own: up to 80%.\n"
                          '\n'
                          'Read that as an admission. When a vendor builds a product whose only '
                          'job is to delete time series before they reach the meter, the meter is '
                          'cardinality, and the vendor knows the cardinality is often junk.\n'
                          '\n'
                          'The practical move costs nothing:\n'
                          '\n'
                          '1. Sort your metrics by tag value count, not by metric name.\n'
                          '2. Drop any tag whose values scale with users, carts or request ids.\n'
                          '3. Re-count before you negotiate a discount, because the discount is '
                          'priced on the number you can already fix.'},
              {'title': 'What the switch actually costs',
               'content': 'Correction, November 14, 2026: a standard Prometheus client exposes '
                          'metrics for scraping; it does not directly send to a remote_write '
                          'endpoint. Pricing figures retain their November 10 check and were not '
                          're-quoted in this technical correction.\n'
                          '\n'
                          'Typical metrics path: application /metrics → Prometheus scrape + '
                          'remote_write → Grafana Cloud Metrics. With Alloy: application /metrics '
                          '→ prometheus.scrape → prometheus.remote_write → the destination. '
                          'Configure the collector’s targets, endpoint and authentication; '
                          'changing application instrumentation alone is insufficient.\n'
                          '\n'
                          'Metrics compatibility does not migrate Datadog dashboards, monitor '
                          'semantics, logs or traces automatically. Inventory each signal and '
                          'verify the required collector/exporter path before cutover.\n'
                          '\n'
                          'Retention also needs review: the listed Datadog Pro metrics window is '
                          '15 months, while Grafana Pro lists 13 months for metrics and 30 days '
                          'for logs and traces. Compare query results and alerts, not only whether '
                          'samples arrive.'}],
 'cost_math': [{'label': '20 hosts, 5,000 custom series',
                'formula': 'Datadog: 20 × $15 = $300, plus (5,000 − 20 × 100) = 3,000 series ÷ 100 '
                           '× $5 = $150. Grafana: $19 platform fee, 5,000 under the 10,000 '
                           'allowance',
                'result': '$450 on Datadog against $19 on Grafana Cloud Pro'},
               {'label': '20 hosts, 200,000 custom series',
                'formula': 'Datadog: $300 + (200,000 − 2,000) ÷ 100 × $5 = $9,900. Grafana: $19 + '
                           '90,000 × $6.50/1,000 = $585 + 100,000 × $5.90/1,000 = $590',
                'result': '$10,200 on Datadog against $1,194 on Grafana Cloud Pro'},
               {'label': '500 GB of logs a month, 200M events, 30-day retention',
                'formula': 'Datadog: 500 × $0.10 = $50 ingest, plus 200M ÷ 1M × $2.50 = $500 '
                           'indexed. Grafana: 450 GB over the 50 GB allowance × ($0.05 + $0.40 + '
                           '$0.10) = $247.50',
                'result': '$550 on Datadog against $247.50 on Grafana Cloud Pro'},
               {'label': '30 hosts with APM on Datadog',
                'formula': '30 × ($15 infrastructure + $31 APM) = 30 × $46 = $1,380 per month at '
                           'annual rates',
                'result': '$1,380 before logs, traces or RUM; Grafana Cloud Pro has no per-host '
                          'infrastructure line'}],
 'decision_matrix': [{'situation': 'Series count scales with users, not hosts',
                      'pick': 'Grafana Cloud',
                      'why': 'At 200,000 series the series meter bills $9,900 on Datadog against '
                             '$1,175 on Grafana, and the 10,000-series allowance is account-wide.'},
                     {'situation': 'A team already living in Datadog APM and security',
                      'pick': 'Datadog',
                      'why': 'At 30 hosts the infrastructure plus APM licence is $1,380, and '
                             'rebuilding dashboards and monitors is the hidden cost of leaving.'},
                     {'situation': 'Five hosts and one person on call',
                      'pick': 'Grafana Cloud',
                      'why': "Datadog's licence starts at $75 for five hosts before any custom "
                             "metrics; Grafana's platform fee is $19 for the account."},
                     {'situation': 'You need 15 months of full-resolution metrics',
                      'pick': 'Datadog',
                      'why': 'Datadog keeps 15 months on Pro; Grafana Cloud Pro lists 13 months '
                             'for metrics and 30 days for logs and traces.'},
                     {'situation': 'The custom metrics line is already over $500',
                      'pick': 'Grafana Cloud',
                      'why': 'That line is $500 per 10,000 series on Datadog and $65 per 10,000 on '
                             'Grafana, so the same data crosses a factor of 7.7.'},
                     {'situation': 'Logs are verbose JSON from a dozen services',
                      'pick': 'Compute both before choosing',
                      'why': "Datadog's index rate is per event and Grafana's is per GB, so 500 GB "
                             'at 2.5 KB per event bills $550 against $247.50, and the same 500 GB '
                             'at 250 bytes per event is 2 billion events, or $5,000 on the index '
                             'line.'},
                     {'situation': 'Security, SIEM and audit on one invoice',
                      'pick': 'Datadog',
                      'why': 'Cloud SIEM, workload protection and audit trail are on the same '
                             'price list; Grafana Cloud prices observability and leaves security '
                             'elsewhere.'},
                     {'situation': 'Everything is already Prometheus and you self-host Grafana',
                      'pick': 'Grafana Cloud, or keep self-hosting',
                      'why': 'Existing instrumentation may be reusable, but configure Prometheus '
                             'or Alloy scraping and remote_write, then verify labels, queries, '
                             'alerts and destination limits before switching.'}],
 'verdict_summary': 'The modeled metrics bills favor Grafana Cloud, especially at high '
                    'cardinality. That is not a complete migration cost: collector configuration, '
                    'dashboards, alerts and non-metric signals need validation. Datadog may fit a '
                    'team that relies on its integrated workflows; compare actual usage and '
                    'transition work rather than assuming a fixed payback period.',
 'migration_guide': 'Keep compatible instrumentation, then build and test the collection pipeline. '
                    'The Python client example below exposes a scrape target on port 9100; it is a '
                    'cardinality anti-pattern demonstration, not a complete remote_write setup. '
                    'Prometheus scrapes that target and forwards via remote_write, or Alloy '
                    'connects prometheus.scrape to prometheus.remote_write.\n'
                    '\n'
                    'Use the destination’s documented endpoint, tenant/account identifier and '
                    'scoped authentication. Verify metric names, label mapping, histogram '
                    'compatibility, scrape interval, sample timestamps, cardinality and ingestion '
                    'limits. Watch failed sends, queue/WAL health, gaps and duplicate series '
                    'during a limited parallel run.\n'
                    '\n'
                    'Do not assume the Datadog Agent is a generic Prometheus remote_write '
                    'forwarder. Confirm supported collection/export for each actual integration; '
                    'logs and traces require their own paths. Review dashboards, alert queries and '
                    'thresholds against observed results, establish rollback criteria, and retire '
                    'the old path only after validation. No fixed quarter-long overlap or payback '
                    'period is established here.',
 'faqs': [{'q': "Are Grafana Cloud's tier prices marginal or flat?",
           'a': 'Marginal. Each new band bills at a lower rate for the usage inside it, so the '
                'blended rate falls as the account grows: $6.50 per 1,000 to 100,000, then $5.90, '
                'then $5.50.'},
          {'q': 'What exactly is a custom metric on Datadog?',
           'a': 'A unique metric name plus tag combination, averaged hourly across the month. '
                'Adding a tag with many values multiplies the count even if the metric name never '
                'changes.'},
          {'q': 'Does Grafana Cloud charge per host?',
           'a': 'The Pro plan is a $19 platform fee per account. Host hours appear for Kubernetes '
                'monitoring at $0.01 per host hour, which is a separate product from '
                'infrastructure metrics.'},
          {'q': 'Does a Prometheus client push directly to Grafana Cloud remote_write?',
           'a': 'Not in the standard scrape-based setup. The client exposes /metrics; Prometheus '
                'scrapes it and forwards with remote_write, or Alloy uses prometheus.scrape '
                'feeding prometheus.remote_write. Configure the collector’s destination and '
                'authentication, then validate labels, gaps, duplicates, queries and alerts. The '
                'application example alone is not a complete pipeline.'}],
 'sources': ['https://www.datadoghq.com/pricing/',
             'https://www.datadoghq.com/pricing/list/',
             'https://docs.datadoghq.com/account_management/billing/custom_metrics/',
             'https://grafana.com/pricing/',
             'https://grafana.com/docs/grafana-cloud/adaptive-telemetry/adaptive-metrics/',
             'https://prometheus.io/docs/guides/go-application/',
             'https://prometheus.io/docs/prometheus/latest/prometheus_agent/',
             'https://grafana.com/docs/alloy/latest/collect/prometheus-metrics/',
             'https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/'],
 'related': [{'slug': 'aws-lambda-vs-cloudflare-workers',
              'name': 'AWS Lambda vs Cloudflare Workers',
              'why': 'Another invoice where the billing unit, not the price, decides the total.'},
             {'slug': 'stripe-vs-lemonsqueezy-vs-paddle',
              'name': 'Stripe vs Lemon Squeezy / Paddle',
              'why': 'Four meters on one invoice, and the sticker price covers one of them.'}],
 'tool_a': {'name': 'Datadog',
            'tagline': 'Per-host licences with a custom-metric meter on top',
            'db': 'SaaS telemetry: infrastructure, APM, logs, security and RUM',
            'pricing': 'Infrastructure Pro $15/host/mo annual ($18 monthly) · custom metrics $5 '
                       'per 100 · logs $0.10/GB + $1.70 per 1M at 15 days',
            'self_host': 'No (hosted SaaS, agent-based collection)',
            'realtime': '15 months of full-resolution metrics; 15-day log and trace search',
            'ai_readiness': 'Bits AI credits from $500, with per-action credit estimates',
            'lock_in': 'High: dashboards, monitors and APM traces have no export to another '
                       'backend',
            'badge': 'Per host',
            'cta_url': 'https://www.datadoghq.com/?utm_source=devteardown',
            'pros': ['One agent covers infrastructure, APM, logs and security, so the product '
                     'surface is the reason teams stay',
                     '100 custom metrics ride along with every host licence, which covers a '
                     'well-behaved service',
                     'Metrics without Limits decouples ingest from index, so you can keep sending '
                     'and stop paying full price',
                     '15 months of full-resolution retention on Pro is the longest on either price '
                     'sheet'],
            'cons': ['The host licence bills machines you did not grow, so a fleet of small '
                     'instances pays per instance',
                     'Custom metrics at $5 per 100 is $50 per 1,000, after an allowance of just '
                     '100 per host',
                     'Logs are metered twice, on ingest and on indexed events, and the event count '
                     'follows log size',
                     'APM is a second per-host licence at $31, so a monitored host is $46 before '
                     'logs'],
            'code_example': '# Every tag value pair is its own billable series on Datadog.\n'
                            'from datadog import statsd\n'
                            '\n'
                            'def checkout(cart_id: str, user_id: str, items: int) -> None:\n'
                            '    statsd.increment("checkout.completed", '
                            'tags=[f"user_id:{user_id}"])\n'
                            '    statsd.gauge("checkout.items", items, '
                            'tags=[f"cart_id:{cart_id}"])\n'
                            '# Breaks when: user_id has 50,000 values. That is 50,000 custom '
                            'series,\n'
                            "# against an allowance of 100 per host — 500 hosts' worth of licence "
                            'for one tag.'},
 'tool_b': {'name': 'Grafana Cloud',
            'tagline': 'One platform fee, then per-series and per-GB meters',
            'db': 'Managed Prometheus, Loki, Tempo and Mimir behind Grafana dashboards',
            'pricing': 'Pro $19/mo platform fee · 10,000 series and 50 GB logs included · $6.50 '
                       'per 1k series after',
            'self_host': 'Yes (Grafana, Loki, Mimir and Tempo are open source)',
            'realtime': '13 months of metrics on Pro; 30 days for logs, traces, profiles and k6 '
                        'tests',
            'ai_readiness': 'AI Assistant and Adaptive Telemetry included on Free and Pro',
            'lock_in': 'Prometheus-compatible ingestion; collector setup, dashboards and alert '
                       'semantics still need validation',
            'badge': 'Per series',
            'cta_url': 'https://grafana.com/?utm_source=devteardown',
            'pros': ['The account-level fee means machines are free: twenty hosts cost the same as '
                     'two',
                     '10,000 included series cover most small deployments with no custom-metric '
                     'line at all',
                     'Tiered marginal rates mean the effective price falls as volume grows, to '
                     '$5.50 per 1,000',
                     'Prometheus, Loki and Tempo are open source, so the paid plan runs software '
                     'you can also host'],
            'cons': ['The series rate is cheaper but the 10,000-series allowance is shared by '
                     'every metric in the account',
                     'Traces, profiles and logs all meter GB, so a verbose log line is a billable '
                     'byte',
                     'There is no Datadog-equivalent APM product on the Pro sheet, so trace-based '
                     'debugging is a rebuild',
                     "Metrics retention is 13 months against Datadog's 15, which matters for "
                     'year-over-year comparisons'],
            'code_example': '# Same job, same mistake: cardinality is the meter, not the vendor.\n'
                            'from prometheus_client import Counter, Gauge, start_http_server\n'
                            '\n'
                            'checkout = Counter("checkout_completed_total", "Checkouts", '
                            '["user_id"])\n'
                            'items = Gauge("checkout_items", "Items per cart", ["cart_id"])\n'
                            'start_http_server(9100)\n'
                            '\n'
                            'checkout.labels(user_id="u_123").inc()  # one time series per label '
                            'value\n'
                            '# Breaks first here: 50,000 user_id values are 50,000 series on '
                            'Grafana Cloud too,\n'
                            '# and the 10,000-series allowance ends long before the first page of '
                            'users.'}}


WORKERS = {'slug': 'aws-lambda-vs-cloudflare-workers',
 'category': 'Serverless & Edge',
 'last_verified': '2026-11-14',
 'published': '2026-11-10',
 'hook': 'One hundred million requests that each take 200 ms and use 10 ms of CPU cost $147.80 on '
         'AWS Lambda and $51.40 on Cloudflare Workers. Nothing about the code differs. One vendor '
         'bills the waiting.',
 'sections': [{'title': 'Two vendors, three meters, two definitions of work',
               'content': 'Lambda now publishes two price sheets. Event Functions bill requests '
                          'plus duration in GB-seconds: $0.0000133334 per GB-second on Arm, '
                          '$0.0000166667 on x86, and $0.20 per million requests. Web Functions '
                          'bill active CPU at $0.0000276944 per vCPU-second, memory at '
                          '$0.0000036667 per GB-second for as long as the environment exists, and '
                          '$0.30 per million requests.\n'
                          '\n'
                          'Workers bill one thing that matters: CPU milliseconds, $0.02 per '
                          'million after 30 million included, plus $0.30 per million requests '
                          'after 10 million on a $5 plan. No Workers duration/egress charge does '
                          'not make D1 free: database usage, storage and database-count overages '
                          'meter separately.\n'
                          '\n'
                          '| Meter | Lambda Event | Lambda Web | Workers |\n'
                          '|---|---|---|---|\n'
                          '| Requests | $0.20/M | $0.30/M | $0.30/M |\n'
                          '| Duration | GB-seconds | memory GB-s, whole life | none |\n'
                          '| CPU | inside duration | $0.0000276944/vCPU-s | $0.02/M CPU-ms |'},
              {'title': 'A GB-second is a memory meter wearing a clock',
               'content': 'Duration billing multiplies wall time by allocated memory, and both '
                          'factors are yours to set. A 512 MB function that takes 200 ms bills 0.5 '
                          'GB × 0.2 s = 0.1 GB-s per request. At 100 million requests that is 10 '
                          'million GB-seconds, or $133.34 on Arm at $0.0000133334.\n'
                          '\n'
                          'Workers bills the 10 ms of actual work instead: 100 million × 10 ms = '
                          '1,000 million CPU-milliseconds, which is 970 million after the 30 '
                          'million included, at $0.02 per million CPU-ms = $19.40.\n'
                          '\n'
                          'So the ratio between the two vendors is not a rate difference. It is '
                          'the fraction of the request that is CPU: 10 ms of 200 ms is 5%, and '
                          'that 5% is what Workers meters. Make the handler heavier and the gap '
                          'narrows; make it wait on a database and the gap widens.'},
              {'title': 'The bills cross at about 7.5 million requests',
               'content': 'Same shape everywhere below: 200 ms duration, 512 MB, 10 ms of CPU, one '
                          'function.\n'
                          '\n'
                          '| Requests/month | Lambda Event (Arm) | Workers | Cheaper |\n'
                          '|---|---|---|---|\n'
                          '| 5M | $0.80 + $1.33 = $2.13 | $5.00 + $0.40 = $5.40 | Lambda |\n'
                          '| 7.5M | $1.30 + $4.67 = $5.97 | $5.00 + $0.90 = $5.90 | Workers, by 7¢ '
                          '|\n'
                          '| 10M | $1.80 + $8.00 = $9.80 | $5.00 + $1.40 = $6.40 | Workers |\n'
                          '| 50M | $9.80 + $61.33 = $71.13 | $5.00 + $12.00 + $9.40 = $26.40 | '
                          'Workers |\n'
                          '| 100M | $19.80 + $128.00 = $147.80 | $5.00 + $27.00 + $19.40 = $51.40 '
                          '| Workers |\n'
                          '\n'
                          'The crossover is a free-tier artefact, not a policy: 1 million requests '
                          'and 400,000 GB-seconds are free on Lambda, and 30 million CPU-ms are '
                          'free on Workers. Below roughly 7.5 million requests the Lambda '
                          'allowance is worth more than the CPU savings. Above it, the $5 plan '
                          'floor disappears into the noise.'},
              {'title': "Lambda's second sheet splits the same request in two",
               'content': "Web Functions are AWS's answer to active-CPU billing, and they price "
                          'the same 100 million requests differently.\n'
                          '\n'
                          '| Line | Lambda Event | Lambda Web | Workers |\n'
                          '|---|---|---|---|\n'
                          '| Requests | $19.80 | $30.00 | $27.00 |\n'
                          '| Compute | 10M GB-s = $128.00 | 1M vCPU-s = $27.69, 1.296M GB-s = '
                          '$4.75 | 970M CPU-ms = $19.40 |\n'
                          '| Plan floor | — | — | $5.00 |\n'
                          '| **Total** | **$147.80** | **$62.45** | **$51.40** |\n'
                          '\n'
                          'Web Functions bill $62.45 for the same traffic, 42% of the Event price, '
                          'and still 21% above the Workers bill. The memory meter is why: it bills '
                          "the environment for its whole life, idle time included, and AWS's own "
                          'examples quietly assume exactly one environment stays up for the entire '
                          'month.'},
              {'title': 'Where Lambda wins on the same sheet',
               'content': 'The free allowance matters: in the stated 512 MB, 200 ms, 10 ms CPU '
                          'model, 5 million requests cost $2.13 on Lambda and $5.40 on Workers. '
                          'This assumes the allowances are not already consumed by other '
                          'workloads.\n'
                          '\n'
                          'Lambda supports up to 10,240 MB. Workers CPU limits vary by trigger; do '
                          'not treat the HTTP limit as universal:\n'
                          '\n'
                          '| Workers Paid invocation | CPU limit | Wall-clock limit |\n'
                          '|---|---|---|\n'
                          '| HTTP | 30 s default; configurable to 5 min | No hard limit while '
                          'client connected |\n'
                          '| Cron, interval under 1 hour | 30 s | 15 min |\n'
                          '| Cron, interval at least 1 hour | 15 min | 15 min |\n'
                          '| Queue consumer | 30 s default; configurable to 5 min | 15 min |\n'
                          '\n'
                          'Queue wall time is not CPU time. Free and legacy plans have different '
                          'limits; verify the deployed configuration. AWS integrations such as '
                          'VPC, IAM, SQS and Kinesis may also outweigh a small compute-price '
                          'difference.'},
              {'title': 'The exit door has a rewrite behind it',
               'content': 'Correction, November 14, 2026: the wait-only example accidentally '
                          'substituted 200 ms CPU for its stated 10 ms. At 10 million requests, '
                          'Workers remains $6.40, not $44.40; the extra wall time changes Lambda’s '
                          'duration bill only. Workers pricing and trigger limits were rechecked; '
                          'other AWS figures retain their November 10 source check.\n'
                          '\n'
                          'Moving runtimes still requires testing APIs, native dependencies, '
                          'filesystem behavior and state bindings. Check the actual HTTP, Cron or '
                          'Queue limit rather than assuming every invocation has a five-minute CPU '
                          'cap.\n'
                          '\n'
                          'The estimate covers one workload with available included usage, not a '
                          'complete application invoice. Storage, queues, databases, retries and '
                          'migration work can add costs; measure CPU and elapsed duration '
                          'separately before choosing.'}],
 'cost_math': [{'label': '100M requests at 200 ms, 512 MB, 10 ms CPU',
                'formula': 'Lambda Event Arm: 100M × 0.2 s × 0.5 GB = 10M GB-s, minus 400k free = '
                           '9.6M × $0.0000133334 = $128.00, plus 99M × $0.20/M = $19.80. Workers: '
                           '(100M − 10M) × $0.30/M = $27.00, plus (1,000M − 30M) CPU-ms × $0.02/M '
                           '= $19.40, plus $5.00',
                'result': '$147.80 on Lambda against $51.40 on Workers'},
               {'label': 'The same traffic on Lambda Web Functions',
                'formula': '100M × 10 ms = 1M vCPU-s × $0.0000276944 = $27.69; 0.5 GB × 2,592,000 '
                           's = 1,296,000 GB-s × $0.0000036667 = $4.75; 100M × $0.30/M = $30.00',
                'result': "$62.45, 58% below Lambda's own Event price for identical traffic"},
               {'label': "Cross-over against Lambda's free tier",
                'formula': 'Lambda: (R − 1M) × $0.20/M + (R × 0.1 − 400k) × $0.0000133334. '
                           'Workers: $5 + (R × 10 − 30M) × $0.02/M',
                'result': "Equal at about 7.5M requests a month; below that Lambda's free "
                          'allowance wins, above it the CPU meter does'},
               {'label': 'Wall time rises from 200 ms to 1 s; CPU remains 10 ms',
                'formula': 'At 10M requests, Lambda Event Arm: (10M × 1 s × 0.5 GB − 400k GB-s) × '
                           '$0.0000133334 + 9M × $0.20/M = $63.13. Workers: $5 + max(0, 10M − 10M) '
                           '× $0.30/M + max(0, 10M × 10 ms − 30M CPU-ms) × $0.02/M = $6.40.',
                'result': 'Lambda rises from $9.80 to $63.13 (+$53.33); Workers stays $6.40. All '
                          'stated allowances are assumed available; taxes and other services are '
                          'excluded.'}],
 'decision_matrix': [{'situation': 'Under about 5 million requests a month',
                      'pick': 'Lambda Event Functions',
                      'why': 'The 1M-request and 400,000 GB-second free allowances cover the whole '
                             'job: 5M requests at 200 ms and 512 MB price at $2.13 against $5.40 '
                             'on Workers.'},
                     {'situation': '100 million requests that mostly wait on I/O',
                      'pick': 'Workers',
                      'why': 'The same shape prices at $51.40 against $147.80, because 10 ms of '
                             'CPU out of a 200 ms request is all Workers meters.'},
                     {'situation': 'A function that needs 10 GB of memory',
                      'pick': 'Lambda',
                      'why': 'Lambda supports up to 10,240 MB; Workers uses a much smaller isolate '
                             'memory budget. CPU limits are separate and depend on the invocation '
                             'type.'},
                     {'situation': 'Long-lived streaming to a browser',
                      'pick': 'Lambda Web Functions',
                      'why': "Active-CPU billing ignores the wait: AWS's own LLM streaming example "
                             'prices 5M requests of 3 s at $33.94, against $101.00 as Event '
                             'Functions.'},
                     {'situation': 'Byte-heavy responses at the edge',
                      'pick': 'Workers',
                      'why': 'Workers charges nothing for egress or bandwidth, and static asset '
                             'requests are free and unlimited.'},
                     {'situation': 'SQS, Kinesis, VPC and IAM already wired into the app',
                      'pick': 'Lambda',
                      'why': 'The compute line is often the small one; rewriting event sources and '
                             'IAM to leave AWS costs more than the difference on the invoice.'},
                     {'situation': 'A cron job every hour, minutes of CPU each',
                      'pick': 'Workers',
                      'why': 'At an hourly interval, paid Cron permits up to 15 minutes CPU and 15 '
                             'minutes wall time. The 720-invocation × 180,000 ms example is $5 + '
                             '(129.6M − 30M) × $0.02/M = $6.992, about $6.99, assuming no other '
                             'usage or services.'},
                     {'situation': 'Traffic so spiky that one environment cannot serve it',
                      'pick': 'Lambda Event Functions',
                      'why': 'Web Functions bill memory for the life of every environment, and the '
                             'pricing examples quietly assume exactly one environment runs all '
                             'month.'}],
 'verdict_summary': 'For a request that waits, Workers is two to three times cheaper and the gap '
                    'grows with every millisecond you spend on a database call. For a request that '
                    "works, the two converge, and Lambda's free tier and memory ceiling win back "
                    "the low end. The bill is a statement about your code's shape, not about the "
                    "vendors' rates.",
 'migration_guide': 'Lambda to Workers is a runtime rewrite: the handler becomes a fetch listener, '
                    'environment variables become bindings, and anything that needs a native '
                    'module, a spawned process or a writable disk has no equivalent. State moves '
                    'to Durable Objects or KV, which bill separately.\n'
                    '\n'
                    'Workers to Lambda is smaller but not free: package the code, replace KV and '
                    'Durable Objects with a database, and accept that egress is metered again. In '
                    'both directions the traffic analysis comes first, because the arithmetic only '
                    'favours one vendor when you know the request duration and the CPU share of '
                    'it.',
 'faqs': [{'q': 'Does no duration charge mean Workers has no execution limit?',
           'a': 'No. Standard Workers bills CPU and requests rather than elapsed duration, but '
                'trigger limits still apply. Paid HTTP CPU defaults to 30 seconds and can be '
                'configured to 5 minutes. Paid Cron CPU is 30 seconds below a one-hour interval '
                'and 15 minutes at intervals of at least one hour. Queue CPU defaults to 30 '
                'seconds, configurable to 5 minutes; its separate wall-clock limit is 15 minutes.'},
          {'q': 'What are Lambda Web Functions?',
           'a': 'A second Lambda billing model that charges per request, per vCPU-second of active '
                'CPU and per GB-second of memory for as long as the execution environment exists.'},
          {'q': 'What happens if a request waits longer but still uses 10 ms CPU?',
           'a': 'In the stated 10M-request paid-plan model with available allowances, increasing '
                'wall time from 200 ms to 1 s leaves Workers at $6.40. Lambda Event Arm at 512 MB '
                'rises from $9.80 to $63.13. The old $44.40 Workers result incorrectly used 200 ms '
                'CPU. These are modeled costs, not measured performance or complete invoices.'},
          {'q': 'Is a cold start billed?',
           'a': 'On Event Functions the initialisation runs inside the billed duration, and '
                'SnapStart adds its own cache and restore charges. Workers does not bill duration '
                'at all.'}],
 'sources': ['https://aws.amazon.com/lambda/pricing/',
             'https://developers.cloudflare.com/workers/platform/pricing/',
             'https://developers.cloudflare.com/workers/platform/limits/',
             'https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html',
             'https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html',
             'https://developers.cloudflare.com/queues/platform/limits/',
             'https://developers.cloudflare.com/d1/platform/pricing/'],
 'related': [{'slug': 'datadog-vs-grafana-cloud',
              'name': 'Datadog vs Grafana Cloud',
              'why': 'The same reading exercise on a monitoring bill: find the unit, then the '
                     'formula.'},
             {'slug': 'anthropic-vs-openai-api-pricing',
              'name': 'Anthropic vs OpenAI API pricing',
              'why': 'Two vendors, identical stickers, and the invoice decided by a token count.'}],
 'tool_a': {'name': 'AWS Lambda',
            'tagline': 'Two bills in one product: duration and active CPU',
            'db': 'Event Functions bill duration in GB-seconds; Web Functions bill active CPU plus '
                  'memory',
            'pricing': 'Event: $0.20/M requests + $0.0000133334/GB-s Arm · Web: $0.30/M + '
                       '$0.0000276944/vCPU-s + $0.0000036667/GB-s',
            'self_host': 'No (AWS-managed, VPC and IAM integrated)',
            'realtime': 'Free tier 1M requests and 400,000 GB-s; 10,240 MB memory ceiling',
            'ai_readiness': 'Durable functions at $8 per million operations; streaming priced per '
                            'GB written',
            'lock_in': 'Medium: event sources, IAM and VPC wiring are AWS-shaped',
            'badge': 'GB-seconds',
            'cta_url': 'https://aws.amazon.com/lambda/?utm_source=devteardown',
            'pros': ['Free tier covers a small service outright: 1M requests and 400,000 '
                     'GB-seconds each month',
                     'Up to 10,240 MB of memory per function, which a V8 isolate cannot match',
                     'Event Functions, MicroVMs, Web Functions and durable functions are all one '
                     'integration',
                     'The event-source catalogue is the reason teams stay: SQS, Kinesis and Step '
                     'Functions in one IAM model'],
            'cons': ['GB-second billing multiplies wall time by memory, so a request that waits '
                     'still bills',
                     'Web Functions fix the wait but bill memory for the life of every '
                     'environment, idle included',
                     'Requests cost $0.20/M on Event Functions and $0.30/M on Web Functions, above '
                     "Workers' $0.30 after 10M included",
                     'Data transfer is metered, so a byte-heavy response is a billable event'],
            'code_example': '// Event Function: the meter starts at invocation and runs through '
                            'the wait.\n'
                            'export const handler = async (event) => {\n'
                            '  const user = await db.users.findUnique({ where: { id: event.userId '
                            '} }); // 180 ms here\n'
                            '  const digest = '
                            'render(user);                                            // 10 ms '
                            'here\n'
                            '  return { statusCode: 200, body: digest };\n'
                            '};\n'
                            '// If lookup takes 1 s, this Event Function runs about 1.01 s at '
                            'configured memory.\n'
                            '// The wait counts toward duration, not just the 10 ms render CPU; '
                            'requests cost extra.\n'
                            '// Web Functions instead bill active CPU PLUS environment-lifetime '
                            'memory,\n'
                            '// requests and data transfer. 10 ms CPU alone is not their total '
                            'bill.'},
 'tool_b': {'name': 'Cloudflare Workers',
            'tagline': 'A flat $5 and a CPU meter, with no duration line',
            'db': 'V8 isolates at the edge: CPU time is the only compute meter',
            'pricing': '$5/mo minimum · 10M requests included then $0.30/M · 30M CPU-ms included '
                       'then $0.02/M',
            'self_host': 'No managed equivalent; workerd is open source',
            'realtime': 'Paid HTTP: CPU 30 s default, up to 5 min; paid Cron at least hourly: 15 '
                        'min CPU; Queue CPU up to 5 min, wall time 15 min',
            'ai_readiness': 'D1, Durable Objects, KV, Queues and Workflows meter separately; '
                            'static assets are free',
            'lock_in': 'Low on compute, higher on state: Durable Objects hold data inside the '
                       'product',
            'badge': 'CPU-ms',
            'cta_url': 'https://workers.cloudflare.com/?utm_source=devteardown',
            'pros': ['No charge for duration, egress or bandwidth, which removes the line that '
                     'surprises AWS bills',
                     'The $5 plan includes 10M requests and 30M CPU-ms, enough for a real product '
                     'to start',
                     'Static asset requests are free and unlimited, so a Worker-fronted site pays '
                     'for the API only',
                     'Caching at the edge cuts CPU without cutting the request, and only the '
                     'request is billed'],
            'cons': ['CPU and wall-clock limits depend on trigger and plan; HTTP defaults to 30 s '
                     'CPU, configurable to 5 min on Paid',
                     'The runtime is not a container: native modules, spawned processes and '
                     'writable disks do not run',
                     'Memory is an isolate-sized budget rather than a configurable 10 GB',
                     "At very low volume the $5 floor is more than Lambda's free tier charges"],
            'code_example': '// Workers compute bills active CPU, plus request charges after '
                            'allowances.\n'
                            'export default {\n'
                            '  async fetch(request, env) {\n'
                            '    const userId = new URL(request.url).searchParams.get("id");\n'
                            '    const user = await env.DB.prepare("SELECT * FROM users WHERE id = '
                            '?")\n'
                            '      .bind(userId).first();            // I/O wait is not Workers '
                            'CPU time\n'
                            '    return new Response(render(user), {\n'
                            '      headers: { "content-type": "text/html" },\n'
                            '    });\n'
                            '  },\n'
                            '};\n'
                            '// D1 separately meters rows read/written, storage and database-count '
                            'overages.\n'
                            '// A query can scan many rows even when first() returns one; check '
                            'indexes.\n'
                            '// Rendering uses Workers CPU; database allowances are not the CPU '
                            'allowance.'}}
