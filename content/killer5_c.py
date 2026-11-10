"""Killer comparison batch C: transactional email."""

RESEND = {
    "slug": "resend-vs-sendgrid",
    "category": "Email Infrastructure",
    "last_verified": "2026-11-10",
    "published": "2026-11-10",
    "hook": (
        "At 100,000 emails a month, Resend's Pro plan is $35 and SendGrid's Essentials plan is "
        "$34.95. Both vendors then charge exactly $55 more for the next rung, and none of that $55 "
        "buys an extra email: it buys the tier where a dedicated IP becomes possible."
    ),
    "sections": [
        {
            "title": "At 100,000 emails, both vendors charge $55 for the same feature",
            "content": (
                "Resend splits its ladder at 100,000 emails, where the plan name changes: Pro is $20 "
                "for 50,000 and $35 for 100,000, while Scale starts at $90 for that same 100,000. The "
                "$55 difference buys no volume at all.\n\n"
                "SendGrid splits the same way: Essentials is $19.95 for 50,000 emails and $34.95 for "
                "100,000, and Pro is $89.95 for the identical 100,000. The difference is $55.00, to "
                "the cent.\n\n"
                "| At 100,000 emails | Cheap tier | Feature tier | Difference |\n|---|---|---|---|\n"
                "| Resend | Pro $35.00 | Scale $90.00 | $55.00 |\n"
                "| SendGrid | Essentials $34.95 | Pro $89.95 | $55.00 |\n\n"
                "Two vendors that share no code and no pricing page arrived at the same step, at the "
                "same volume, for the same reason: at 100,000 emails the feature gates are what the "
                "plan is priced on, not the sending."
            ),
        },
        {
            "title": "The ladder is not monotonic, and overage is sometimes the cheaper rung",
            "content": (
                "Read each ladder as cost per 1,000, not as a monthly price.\n\n"
                "| Volume needed | Resend | Per 1,000 | SendGrid | Per 1,000 |\n|---|---|---|---|---|\n"
                "| 50,000 | $20.00 (50k) | $0.40 | $19.95 (50k) | $0.40 |\n"
                "| 100,000 | $35.00 (100k Pro) | $0.35 | $34.95 (100k Essentials) | $0.35 |\n"
                "| 200,000 | $160.00 (200k) | $0.80 | $249.00 (300k) | $1.25 |\n"
                "| 500,000 | $350.00 (500k) | $0.70 | $499.00 (700k) | $1.00 |\n"
                "| 1,000,000 | $650.00 (1M) | $0.65 | $799.00 (1.5M) | $0.80 |\n"
                "| 2,500,000 | $1,150.00 (2.5M) | $0.46 | $1,099.00 (2.5M) | $0.44 |\n\n"
                "Where one vendor has no rung at that volume, the column shows the cheapest rung that "
                "covers it, which is why SendGrid's 200,000 row is its 300,000 plan.\n\n"
                "Resend's 200,000 rung costs $0.80 per 1,000, more than twice its 100,000 rung. That "
                "is not a discount curve; it is a plan boundary, and the cheaper block stops at "
                "100,000.\n\n"
                "Overage repairs it. Resend charges $0.90 per 1,000 beyond the included volume, so "
                "100,000 on Pro plus 100,000 of overage is $35 + $90 = $125, not $160. SendGrid's "
                "same move on Pro is $89.95 + 100,000 × $1.10/1,000 = $199.95, not $249."
            ),
        },
        {
            "title": "Dedicated IP: $30 plus a $55 step, or included at $89.95",
            "content": (
                "A dedicated IP is the feature that decides most of these purchases, because shared "
                "IP reputation is the thing a growing sender cannot control.\n\n"
                "Resend sells it as a $30 per month add-on, and only on Scale, to accounts sending "
                "more than 3,000 emails a day. At 100,000 emails that is $90 + $30 = $120, or $1.20 "
                "per 1,000.\n\n"
                "SendGrid includes one dedicated IP in Pro, which is $89.95 at the same volume, or "
                "$0.90 per 1,000.\n\n"
                "| 100,000 emails with a dedicated IP | Monthly | Per 1,000 |\n|---|---|---|\n"
                "| Resend Scale + IP add-on | $120.00 | $1.20 |\n"
                "| SendGrid Pro | $89.95 | $0.90 |\n\n"
                "There is no Resend Pro path to an IP at any price. That is not a worse deal; it is a "
                "missing SKU, and it decides the vendor for anyone whose deliverability depends on "
                "one."
            ),
        },
        {
            "title": "Domain authentication is table stakes; the domain count is not",
            "content": (
                "Both authenticate sending with DKIM, SPF and DMARC, and both include a REST API, "
                "SMTP relay and official SDKs on every paid plan. The differences are in the "
                "quantities.\n\n"
                "| Quantity | Resend | SendGrid |\n|---|---|---|\n"
                "| Custom domains | 3 Free, 10 Pro, 1,000 Scale | Domain authentication included |\n"
                "| Extra domains | $20/mo adds 100 | Not a listed line item |\n"
                "| Teammates | Not metered | 1 on Essentials, 1,000 on Pro |\n"
                "| Event webhooks | 5 on Pro, 10 on Scale | 2 on Essentials, 5 on Pro |\n"
                "| SSO | $150/mo add-on on Scale | Included in Pro |\n\n"
                "An agency managing dozens of client domains should price the domain line before the "
                "email line: Resend's add-on covers 100 extra domains for $20, and SendGrid's "
                "inclusion has no printed ceiling."
            ),
        },
        {
            "title": "The bottom of the market is where they stop competing",
            "content": (
                "Resend keeps a free plan: 3,000 emails a month, 100 a day, three domains, 30 days of "
                "data retention. SendGrid's free option is a 60-day trial at 100 emails a day, after "
                "which the account converts to a paid plan starting at $19.95.\n\n"
                "That single difference moves a whole segment. A side project, a staging environment "
                "or a low-volume notification service runs at $0 on Resend and at $19.95 on SendGrid, "
                "and the gap is $239.40 a year before either vendor has been compared on anything "
                "else.\n\n"
                "It also sets the frame for the first paid tier: $20 on Resend buys 50,000 emails, "
                "more than sixteen times what its own free plan allowed, and the same 50,000 that "
                "SendGrid now sells as its smallest paid plan."
            ),
        },
        {
            "title": "Where each one breaks",
            "content": (
                "Resend breaks on the feature boundary. The dedicated IP, SSO and 1,000 domains all "
                "sit on Scale, so the 100,000-email customer who outgrows Pro pays a $55 step and then "
                "$30 more for the IP. Marketing email moves to a separate contact-priced plan, and "
                "broadcasts only reach existing contacts.\n\n"
                "SendGrid breaks on the tier edge and on history. The 50,000 Essentials tier charges "
                "$1.33 per 1,000 beyond its volume, so 80,000 emails bills $19.95 + $39.90 = $59.85 "
                "against $34.95 for the next tier up. Searchable activity is 3 days on Essentials "
                "against 7 on Pro, so a deliverability investigation can outlast the evidence.\n\n"
                "Check three numbers before choosing: your monthly volume rounded up to the rung that "
                "covers it, whether you need an IP this quarter, and how many domains you will "
                "authenticate in a year."
            ),
        },
    ],
    "cost_math": [
        {
            "label": "100,000 emails a month, no dedicated IP",
            "formula": "Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000",
            "result": "$35.00 against $34.95, a five-cent gap at the bottom of the ladder",
        },
        {
            "label": "200,000 emails a month, the rung against the overage",
            "formula": "Resend: 100,000 Pro at $35 + 100,000 × $0.90/1,000 = $125, against the Scale 200,000 rung at $160. SendGrid: $89.95 + 100,000 × $1.10/1,000 = $199.95, against the Pro 300,000 rung at $249",
            "result": "$125 on Resend and $199.95 on SendGrid, both cheaper than buying the next rung",
        },
        {
            "label": "Overage break-even on the 50,000 tiers",
            "formula": "Resend: $20 + $0.90 per 1,000 over 50,000 equals $35 at 16,666 extra emails, so 66,666. SendGrid: $19.95 + $1.33 per 1,000 equals $34.95 at 11,278 extra, so 61,278",
            "result": "Past roughly 61,000 to 67,000 sends the next tier is cheaper than the overage",
        },
        {
            "label": "The same feature at the same volume",
            "formula": "Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 including one dedicated IP",
            "result": "$120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 monthly difference",
        },
    ],
    "decision_matrix": [
        {
            "situation": "Transactional email only, under 50,000 a month",
            "pick": "Either",
            "why": "$20 on Resend and $19.95 on SendGrid buy the same volume, and the five-cent gap is not a reason to migrate.",
        },
        {
            "situation": "You need a dedicated IP at 100,000 emails",
            "pick": "SendGrid Pro",
            "why": "$89.95 includes one IP, against $90 for Resend Scale plus $30 for the add-on, and Resend Pro cannot buy an IP at all.",
        },
        {
            "situation": "A free tier is mandatory for staging",
            "pick": "Resend",
            "why": "Resend's free plan sends 3,000 a month, while SendGrid's free option is a 60-day trial and then $19.95.",
        },
        {
            "situation": "Agencies authenticating dozens of client domains",
            "pick": "Resend Scale, with the domain add-on",
            "why": "1,000 domains are included on Scale and $20 adds 100 more, against a domain line SendGrid does not print.",
        },
        {
            "situation": "SSO and an IP at 500,000 emails",
            "pick": "SendGrid Pro",
            "why": "SSO is included in Pro and so is one IP, while Resend puts SSO at $150 a month and the IP at $30 on top of Scale.",
        },
        {
            "situation": "2,500,000 emails a month and nothing exotic",
            "pick": "SendGrid Pro",
            "why": "$1,099 against $1,150 on Resend, and the gap widens with the IP add-on that Resend needs for the same setup.",
        },
        {
            "situation": "Marketing broadcasts to a contact list",
            "pick": "Resend marketing plans",
            "why": "Marketing is priced per contact rather than per email, so an unlimited number of sends to 10,000 contacts is $80.",
        },
        {
            "situation": "Volume swings month to month",
            "pick": "Either, with an alert at 60,000",
            "why": "Both overage rates are more expensive than the next rung: the break-even is about 61,000 on SendGrid and 67,000 on Resend.",
        },
    ],
    "verdict_summary": (
        "Under 50,000 emails the two vendors are the same product at the same price, and the free "
        "tier is the only real difference. Past 100,000 the choice is decided by one feature: SendGrid "
        "includes a dedicated IP at $89.95, Resend sells it for $30 on a plan that already costs $90. "
        "If you need an IP, SendGrid; if you need a free tier and a clean API, Resend; if you need "
        "volume, check the rung and the overage before either."
    ),
    "migration_guide": (
        "Both vendors authenticate a domain with DKIM, SPF and DMARC records, so moving means adding "
        "new DNS records while the old ones still answer. Keep both authenticated for a week, warm "
        "the new domain or IP, then flip the sending domain in code.\n\n"
        "The parts that do not travel are templates and reputation. React Email templates are code "
        "and move with the repository; SendGrid's dynamic templates are vendor objects. A dedicated "
        "IP starts cold on either side, so a sender who relies on one should plan the warm-up as a "
        "week of projected volume rather than a switch."
    ),
    "faqs": [
        {
            "q": "Does Resend sell a dedicated IP on Pro?",
            "a": "No. The $30 per month add-on is listed for Scale plans, to accounts sending more than 3,000 emails a day. Pro has no IP option.",
        },
        {
            "q": "What does SendGrid's free plan include now?",
            "a": "A 60-day trial at 100 emails a day, with no credit card. After it ends the account moves to a paid plan, and Essentials starts at $19.95 for 50,000 emails.",
        },
        {
            "q": "Is overage cheaper than buying the next tier?",
            "a": "Usually not. Overage on the 50,000 tiers is $1.33 per 1,000 on SendGrid and $0.90 on Resend, both far above the next tier's per-1,000 rate, so the break-even arrives at 61,000 to 67,000 sends.",
        },
        {
            "q": "Do both include inbound email parsing?",
            "a": "Resend lists inbound email with webhooks on every plan, and SendGrid lists an Inbound Parse webhook as part of the Email API feature set.",
        },
    ],
    "sources": [
        "https://resend.com/pricing",
        "https://www.twilio.com/en-us/products/email-api/pricing",
        "https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai",
        "https://resend.com/docs",
        "https://www.twilio.com/docs/sendgrid",
    ],
    "related": [
        {"slug": "stripe-vs-lemonsqueezy-vs-paddle", "name": "Stripe vs Lemon Squeezy / Paddle", "why": "The same $55-style feature step, one decimal place larger."},
        {"slug": "datadog-vs-grafana-cloud", "name": "Datadog vs Grafana Cloud", "why": "What happens when a vendor meters the thing your code does by accident."},
    ],
    "tool_a": {
        "name": "Resend",
        "tagline": "Per-block email pricing with a free tier and a Scale step",
        "db": "Transactional email API with React Email templates and inbound parsing",
        "pricing": "Free 3,000/mo · Pro $20 for 50k, $35 for 100k · Scale $90 for 100k to $1,150 for 2.5M",
        "self_host": "No (managed sending infrastructure and shared IPs)",
        "realtime": "Batch sending and webhooks on every plan; 5 endpoints on Pro, 10 on Scale",
        "ai_readiness": "100 AI credits a month on Pro, 500 on Scale; 10,000 automation runs included",
        "lock_in": "Low: SMTP and REST, and domain reputation travels with your DNS",
        "badge": "Free tier",
        "cta_url": "https://resend.com/?utm_source=devteardown",
        "pros": [
            "A free plan that sends 3,000 emails a month, so staging and side projects cost nothing",
            "Monthly billing only, with no annual contract to sign before the first send",
            "10 domains on Pro and 1,000 on Scale, with 100 more for $20 a month",
            "React Email templates are code, so they live in the repository rather than a dashboard",
        ],
        "cons": [
            "The dedicated IP is a $30 add-on on Scale only, so Pro customers cannot buy one at any price",
            "SSO is $150 a month on Scale and unavailable below it",
            "Scale at 100,000 emails is $90 against $35 on Pro, a $55 step for features rather than volume",
            "The 200,000 rung costs $0.80 per 1,000, more than twice the 100,000 rung's rate",
        ],
        "code_example": (
            "// Resend: the idempotency key is what stops a retry from sending twice.\n"
            "import { Resend } from \"resend\";\n"
            "const resend = new Resend(process.env.RESEND_API_KEY);\n\n"
            "const { data, error } = await resend.emails.send(\n"
            "  {\n"
            "    from: \"billing@example.com\",\n"
            "    to: order.email,\n"
            "    subject: `Receipt for ${order.id}`,\n"
            "    react: Receipt({ order }),\n"
            "  },\n"
            "  { idempotencyKey: `receipt-${order.id}` },\n"
            ");\n"
            "// Breaks when: the key is built from Date.now(). A retry after a 429 is then a\n"
            "// second email, and there is no deduplication on the receiving side."
        ),
    },
    "tool_b": {
        "name": "SendGrid",
        "tagline": "Per-block pricing where Pro includes the dedicated IP",
        "db": "Email API with dynamic templates, subusers and dedicated IPs",
        "pricing": "60-day trial · Essentials $19.95 for 50k, $34.95 for 100k · Pro $89.95 for 100k to $1,099 for 2.5M",
        "self_host": "No (Twilio-managed sending infrastructure)",
        "realtime": "Event webhook on every plan: 1 endpoint on trial, 2 on Essentials, 5 on Pro",
        "ai_readiness": "Address validation included with Pro: 2,500 checks, 5,000 on Premier",
        "lock_in": "Medium: templates, subusers and IP warm-up history live in the product",
        "badge": "IP included",
        "cta_url": "https://www.twilio.com/en-us/products/email-api/pricing?utm_source=devteardown",
        "pros": [
            "One dedicated IP is included in Pro, which is the cheapest published way to get one at 100,000 emails",
            "SSO and 1,000 teammates arrive with Pro rather than as add-ons",
            "Subuser management makes it a fit for agencies and multi-brand senders",
            "The ladder keeps falling to $0.44 per 1,000 at 2,500,000, undercutting Resend at the top",
        ],
        "cons": [
            "No free plan: the trial runs 60 days and then the account is on a paid tier",
            "The 50,000 tier charges $1.33 per 1,000 beyond its volume, so 80,000 emails bills $59.85 against $34.95 for the next tier",
            "Essentials keeps 3 days of searchable activity against 7 on Pro, which can outlast a deliverability investigation",
            "Email validation and content testing are gated to Pro and above",
        ],
        "code_example": (
            "// SendGrid: categories are the only cheap way to separate streams in the event webhook.\n"
            "import sgMail from \"@sendgrid/mail\";\n"
            "sgMail.setApiKey(process.env.SENDGRID_API_KEY);\n\n"
            "await sgMail.send({\n"
            "  to: order.email,\n"
            "  from: \"billing@example.com\",\n"
            "  templateId: \"d-receipt-v3\",\n"
            "  dynamicTemplateData: { orderId: order.id, total: order.total },\n"
            "  categories: [\"receipt\", `region-${order.region}`],\n"
            "  customArgs: { order_id: order.id }, // echoed in the event webhook\n"
            "});\n"
            "// Breaks when: the template renders a total without a currency. The API accepts it,\n"
            "// the receipt is wrong, and the event webhook reports a delivered message."
        ),
    },
}
