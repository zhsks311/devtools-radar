#!/usr/bin/env python3
"""Assemble the five commercial-intent teardowns into content/, data/ and dist/ inputs.

Run:  python3 content/build_killer5.py
Writes content/facts/{slug}.md, content/final/{slug}.json, content/final/{slug}.md
and merges the full items into data/tools.json (idempotent by slug).
"""

import json
import os
import sys

BASE = "/workspace/devtools-radar"
sys.path.insert(0, os.path.join(BASE, "content"))

from killer5_a import STRIPE, ANTHROPIC  # noqa: E402
from killer5_b import DATADOG, WORKERS  # noqa: E402
from killer5_c import RESEND  # noqa: E402

ITEMS = [STRIPE, ANTHROPIC, DATADOG, WORKERS, RESEND]

ARTICLE_KEYS = [
    "slug", "category", "last_verified", "published", "hook", "sections",
    "cost_math", "decision_matrix", "verdict_summary", "migration_guide",
    "faqs", "sources", "related",
]

# Published numbers each article is allowed to use, kept next to the article so the
# chain from price sheet to prose stays readable.
FACTS = {
    "stripe-vs-lemonsqueezy-vs-paddle": [('Stripe Payments US',
  'Domestic cards 2.9% + 30¢; international cards +1.5%; required currency conversion +1%. These '
  'are not Korean eligibility or account-specific quotes.',
  'https://stripe.com/pricing'),
 ('Stripe Billing', 'Pay-as-you-go 0.7% of Billing volume.', 'https://stripe.com/billing/pricing'),
 ('Stripe Tax Basic US',
  'No-code 0.5% for applicable registered transactions; API integration 50¢. Alternative '
  'integration paths. Tax Complete is separately priced with plan limits.',
  'https://stripe.com/pricing'),
 ('Lemon Squeezy',
  'Base 5% + 50¢; subscription +0.5 percentage points; applicable non-US transactions +1.5 and '
  'PayPal +1.5. Fee base includes tax. Region-dependent payout fees are separate.',
  'https://docs.lemonsqueezy.com/help/getting-started/fees'),
 ('Paddle',
  'Published standard 5% + 50¢ per Checkout transaction, subscriptions included; custom pricing '
  'may apply. Do not apply Lemon Squeezy surcharges.',
  'https://www.paddle.com/pricing'),
 ('Model assumptions',
  'US standard rates; tax-free total order value; every Stripe charge incurs the selected Tax '
  'path; no FX, international, PayPal, refund, dispute or payout fees unless explicitly modeled.',
  'https://stripe.com/pricing')],
    "anthropic-vs-openai-api-pricing": [
        ("Claude Sonnet 5.5", "$2 input / $10 output per MTok; 5m cache write $2.50; 1h write $4; cache hit $0.10; batch $1 / $5", "https://docs.anthropic.com/en/docs/about-claude/pricing"),
        ("Claude Opus 5.5", "$4 / $20 per MTok; writes $5 and $8; cache hit $0.20; batch $2 / $10", "https://docs.anthropic.com/en/docs/about-claude/pricing"),
        ("Claude Haiku 5.5", "$0.10 / $0.50 per MTok for prompts up to 100,000 tokens; $0.50 / $2.50 for prompts over it", "https://docs.anthropic.com/en/docs/about-claude/pricing"),
        ("Claude cache multipliers", "5m write 1.25x, 1h write 2x, read 0.1x (0.05x on Opus 5.5 and Sonnet 5.5); multipliers stack with batch", "https://platform.claude.com/docs/en/build-with-claude/prompt-caching"),
        ("Cache control correction, 2026-11-13", "Anthropic Messages opts in with top-level automatic or block-level explicit cache_control; n requests are one write plus n-1 hits; expiry requires a new write", "https://platform.claude.com/docs/en/build-with-claude/prompt-caching"),
        ("Claude tokenizer", "Newer Claude tokenizers count approximately 30% more than earlier Claude tokenizers, depending on content; this is not a comparison with GPT", "https://docs.anthropic.com/en/docs/about-claude/pricing"),
        ("Claude modifiers", "Fast mode doubles the rate and is unavailable with Batch; US-only inference applies 1.1x to every token category", "https://docs.anthropic.com/en/docs/about-claude/pricing"),
        ("GPT-6.1 Sol", "$2 input / $10 output per MTok; cached input $0.10; 30m write $2.50; 12h write $5.00; batch and flex $1 / $5", "https://platform.openai.com/docs/pricing"),
        ("GPT-6.1 Sol long context", "$4 input / $15 output; cached $0.20; 30m write $5.00; 12h write $10.00", "https://platform.openai.com/docs/pricing"),
        ("GPT-6 Astra", "$10 / $50 per MTok, batch $5 / $25", "https://platform.openai.com/docs/pricing"),
        ("GPT-6 Luna", "$0.10 / $0.50 per MTok, batch $0.05 / $0.25", "https://platform.openai.com/docs/pricing"),
        ("OpenAI rate cards", "Standard, Batch, Flex and Fast are separate tables; Batch and Flex share the same numbers", "https://platform.openai.com/docs/pricing"),
    ],
    "datadog-vs-grafana-cloud": [('Datadog Infrastructure Pro',
  '$15 per host per month billed annually, $18 month-to-month',
  'https://www.datadoghq.com/pricing/list/'),
 ('Datadog custom metrics',
  '$5 per 100 custom metrics per month; 100 per host allotted on Pro, 200 on Enterprise',
  'https://www.datadoghq.com/pricing/list/'),
 ('Datadog ingested metrics',
  '$0.10 per 100 ingested custom metrics per month with Metrics without Limits',
  'https://www.datadoghq.com/pricing/list/'),
 ('Datadog logs',
  '$0.10 per ingested GB; indexed events $1.70 per 1M at 15 days, $2.50 at 30 days',
  'https://www.datadoghq.com/pricing/list/'),
 ('Datadog APM',
  '$31 per host per month billed annually, $36 month-to-month',
  'https://www.datadoghq.com/pricing/list/'),
 ('Datadog retention',
  '15 months of full-resolution metrics on Pro; 15-day log and trace search',
  'https://www.datadoghq.com/pricing/'),
 ('Grafana Cloud Pro',
  '$19 per month platform fee plus usage; 10,000 active series and 50 GB logs included; 13-month '
  'metric retention',
  'https://grafana.com/pricing/'),
 ('Grafana series tiers',
  '$6.50 per 1,000 from 10,001 to 100,000; $5.90 to 200,000; $5.50 above; enterprise from $25,000 '
  'a year',
  'https://grafana.com/pricing/'),
 ('Grafana logs',
  '$0.05/GB process, $0.40/GB write, $0.10/GB retain; 50 GB included, 30-day retention',
  'https://grafana.com/pricing/'),
 ('Grafana Adaptive Metrics',
  'Vendor claim: optimise metrics by up to 80% through aggregation and cardinality work',
  'https://grafana.com/pricing/'),
 ('Technical correction 2026-11-14; pricing remains checked 2026-11-10',
  'Client exposes metrics; Prometheus or Alloy scrapes and remote-writes. No generic Datadog Agent '
  'forwarding or automatic dashboard/alert migration assumed.',
  'https://grafana.com/docs/alloy/latest/collect/prometheus-metrics/')],
    "aws-lambda-vs-cloudflare-workers": [('Lambda Event Functions',
  '$0.20 per million requests; $0.0000133334 per GB-s on Arm, $0.0000166667 on x86; free tier 1M '
  'requests and 400,000 GB-s',
  'https://aws.amazon.com/lambda/pricing/'),
 ('Lambda memory',
  '128 MB to 10,240 MB in 1 MB increments',
  'https://aws.amazon.com/lambda/pricing/'),
 ('Lambda Web Functions',
  '$0.30 per million requests; $0.0000276944 per active vCPU-second; $0.0000036667 per GB-second '
  "of memory for the environment's life",
  'https://aws.amazon.com/lambda/pricing/'),
 ('Lambda Web example',
  'LLM streaming endpoint, 5M requests of 3,000 ms with 200 ms active CPU, $33.94; the same page '
  'prices SSR at $25.78 and an authorizer at $64.56',
  'https://aws.amazon.com/lambda/pricing/'),
 ('Lambda durable functions',
  '$8.00 per million operations, $0.25 per GB written, $0.15 per GB-month retained',
  'https://aws.amazon.com/lambda/pricing/'),
 ('Workers paid',
  '$5 per month minimum; 10M requests included then $0.30/M; 30M CPU-ms included then $0.02/M',
  'https://developers.cloudflare.com/workers/platform/pricing/'),
 ('Workers free',
  '100,000 requests per day, 10 ms CPU per invocation, no charge for duration',
  'https://developers.cloudflare.com/workers/platform/pricing/'),
 ('Workers limits',
  'No charge for duration, egress or bandwidth; 5 minutes of CPU per invocation, 30 seconds by '
  'default; static asset requests free and unlimited',
  'https://developers.cloudflare.com/workers/platform/pricing/'),
 ('Workers worked examples',
  '15M at 7 ms = $8.00; 100M at 7 ms = $45.40; 100M with 80% cache hits = $34.20; 720 cron runs at '
  '180,000 ms = $6.99',
  'https://developers.cloudflare.com/workers/platform/pricing/'),
 ('CPU arithmetic and trigger correction 2026-11-14',
  '10M requests × 10ms CPU yields $6.40 including $5 floor, irrespective of 200ms versus 1s wall '
  'time. Paid Cron >=1h CPU 15min; Queue CPU default30s/max5min, wall15min. Other AWS prices '
  'retain November10 verification.',
  'https://developers.cloudflare.com/queues/platform/limits/')],
    "resend-vs-sendgrid": [('Resend plans',
  'Free 3,000/mo (100/day); Pro $20 for 50k and $35 for 100k; Scale $90 for 100k to $1,150 for '
  '2.5M',
  'https://resend.com/pricing'),
 ('Resend overage',
  '$0.90 per 1,000 beyond the included volume; $0.80, $0.70, $0.65, $0.52, $0.46 on higher Scale '
  'rungs',
  'https://resend.com/pricing'),
 ('Resend dedicated IP',
  '$30 per month add-on, Scale only, for accounts sending more than 3,000 emails a day',
  'https://resend.com/pricing'),
 ('Resend add-ons',
  'Domains $20/mo for 100 more; SSO $150/mo on Scale; 3 inboxes included, $1 per extra inbox',
  'https://resend.com/pricing'),
 ('Resend marketing',
  'Priced per contact: free to 1,000, $40 for 5,000, $80 for 10,000, up to $650 for 150,000',
  'https://resend.com/pricing'),
 ('SendGrid plans',
  '60-day trial at 100 emails/day; Essentials from $19.95 (50k) and $34.95 (100k); Pro from $89.95 '
  '(100k)',
  'https://www.twilio.com/en-us/products/email-api/pricing'),
 ('SendGrid ladder',
  'Pro $249 for 300k, $499 for 700k, $799 for 1.5M, $1,099 for 2.5M; Premier custom',
  'https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai'),
 ('SendGrid overage',
  '$1.33 per 1,000 on the 50k Essentials tier, $0.88 on 100k Essentials, $1.10 on 100k Pro',
  'https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai'),
 ('SendGrid features',
  'Pro includes 1 dedicated IP, SSO, 1,000 teammates, 2,500 validations and 7 days of searchable '
  'activity; Essentials keeps 1 teammate, 2 webhooks and 3 days',
  'https://www.twilio.com/en-us/products/email-api/pricing'),
 ('Resend bucket billing correction',
  'Paid transactional plans opt in using Transactional Overages. Round excess usage up in '
  '1,000-email buckets; 51,415 on 50k/$20 gives $21.80 at $0.90/bucket. Taxes/fees extra.',
  'https://resend.com/changelog/pay-as-you-go-pricing'),
 ('SendGrid trial correction',
  'Standard new direct trial stops sending after 60 days unless upgraded; no automatic paid '
  'conversion. Partner/reseller terms and account notices must be checked.',
  'https://www.twilio.com/docs/sendgrid/ui/account-and-settings/upgrading-your-plan')],
}


def write_fact_sheet(item):
    rows = FACTS[item["slug"]]
    lines = [
        "# FACT SHEET — %s (verified %s)" % (item["slug"], item["last_verified"]),
        "",
        "Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.",
        "Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as",
        "the vendor's claim.",
        "",
        "## Published unit prices and limits",
        "",
    ]
    for name, text, url in rows:
        lines.append("- **%s** — %s  \n  source: %s" % (name, text, url))
    lines += ["", "## Derived arithmetic used in the article (formula printed in the text)", ""]
    for c in item["cost_math"]:
        lines.append("- **%s** — %s ⇒ %s" % (c["label"], c["formula"], c["result"]))
    lines += ["", "## Sources", ""] + ["- " + s for s in item["sources"]] + [""]
    path = os.path.join(BASE, "content/facts", item["slug"] + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def write_article_md(item):
    a, b = item["tool_a"]["name"], item["tool_b"]["name"]
    out = [
        "# %s vs %s — a 2026 cost teardown" % (a, b),
        "",
        "> %s" % item["hook"],
        "",
        "*Prices verified %s. Category: %s. Author: DevTeardown Team.*" % (
            item["last_verified"], item["category"]),
        "",
        "## Verdict",
        "",
        item["verdict_summary"],
        "",
    ]
    for idx, sec in enumerate(item["sections"], 1):
        out += ["## %d. %s" % (idx, sec["title"]), "", sec["content"], ""]
    out += ["## Cost arithmetic at volume", "",
            "| Label | Formula | Result |", "|---|---|---|"]
    for c in item["cost_math"]:
        out.append("| %s | %s | %s |" % (c["label"], c["formula"], c["result"]))
    out += ["", "## Decision matrix", "",
            "| If this is you | Take | Because |", "|---|---|---|"]
    for r in item["decision_matrix"]:
        out.append("| %s | %s | %s |" % (r["situation"], r["pick"], r["why"]))
    out += ["", "## Migration path", "", item["migration_guide"], "",
            "## Questions that change the decision", ""]
    for f in item["faqs"]:
        out += ["**%s**  " % f["q"], f["a"], ""]
    out += ["## Sources", ""] + ["- " + s for s in item["sources"]]
    out += ["", "## Same task, two SDKs", "",
            "**%s**" % a, "", "```", item["tool_a"]["code_example"], "```", "",
            "**%s**" % b, "", "```", item["tool_b"]["code_example"], "```", ""]
    path = os.path.join(BASE, "content/final", item["slug"] + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return path


def main():
    data_path = os.path.join(BASE, "data/tools.json")
    with open(data_path, encoding="utf-8") as f:
        tools = json.load(f)

    by_slug = {t["slug"]: t for t in tools}
    new_items = []
    for item in ITEMS:
        article = {k: item[k] for k in ARTICLE_KEYS}
        full = dict(article)
        full["tool_a"] = item["tool_a"]
        full["tool_b"] = item["tool_b"]
        new_items.append(full)

        write_fact_sheet(item)
        write_article_md(item)
        with open(os.path.join(BASE, "content/final", item["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=2)

    # The five new teardowns lead the index; existing items keep their order.
    kept = [t for t in tools if t["slug"] not in {i["slug"] for i in new_items}]
    merged = new_items + kept

    # One UTM source for every outbound CTA.
    for t in merged:
        for key in ("tool_a", "tool_b"):
            url = t[key].get("cta_url", "")
            if "utm_source=" in url:
                head, _, _ = url.partition("utm_source=")
                t[key]["cta_url"] = head + "utm_source=devteardown"

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = 0
    for item in new_items:
        body = "\n\n".join(s["content"] for s in item["sections"])
        total += len(body)
        print("%-34s body=%5d sections=%d matrix=%d cost=%d" % (
            item["slug"], len(body), len(item["sections"]),
            len(item["decision_matrix"]), len(item["cost_math"])))
    print("items=%d total_body=%d" % (len(new_items), total))


if __name__ == "__main__":
    main()
