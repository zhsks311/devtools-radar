"""Killer comparison batch A: payments and LLM API pricing.

Numbers come from the fact sheets written alongside each item; every figure below is either
a published unit price or arithmetic printed with its formula.
"""

STRIPE = {
    "slug": "stripe-vs-lemonsqueezy-vs-paddle",
    "category": "Payments & Billing",
    "last_verified": "2026-11-10",
    "published": "2026-11-10",
    "hook": (
        "A thousand subscribers at $20 a month pay $1,520 on an assembled Stripe stack and "
        "$1,500 on a merchant of record. The vendor everyone calls expensive is the cheaper one "
        "at the price point most SaaS products actually charge."
    ),
    "sections": [
        {
            "title": "The sticker price is one of four meters you will pay",
            "content": (
                "Stripe's pricing page prints one number: 2.9% + 30¢ for a domestic card. A "
                "subscription business pays that plus three more.\n\n"
                "| Meter | Price | Applied when |\n|---|---|---|\n"
                "| Domestic card | 2.9% + 30¢ | every successful charge |\n"
                "| International card | +1.5% | the card is issued outside your country |\n"
                "| Currency conversion | +1.5% | the charge is not in your settlement currency |\n"
                "| Billing | 0.7% of Billing volume | subscriptions, processed on or off Stripe |\n"
                "| Tax Basic | 50¢ per transaction | you are registered to collect there |\n"
                "| ACH direct debit | 0.8%, $5 cap | bank debits |\n"
                "| Dispute | $15.00 | each chargeback received |\n\n"
                "None of those lines is hidden. Each one has its own page, which is how a 2.9% "
                "product becomes a 3.6% + 80¢ product by the end of the month."
            ),
        },
        {
            "title": "A merchant of record sells a different invoice, not a cheaper one",
            "content": (
                "Lemon Squeezy and Paddle both publish 5% + 50¢ per transaction and $0 per month. "
                "They also publish the same sentence in different words: they are the seller.\n\n"
                "That moves who owns the tax question. On Stripe you are the merchant, so the VAT "
                "number, the filing deadline and the penalty for missing it are yours. On either "
                "merchant of record the receipt carries their name and you receive a net payout.\n\n"
                "- **Lemon Squeezy:** 5% + 50¢ per transaction, $0 monthly, and sales tax or VAT "
                "collection where it is the merchant of record, with the liability taken on.\n"
                "- **Paddle:** 5% + 50¢ per Checkout transaction, no monthly fee, and custom "
                "pricing for products under $10.\n"
                "- Neither fee moves when you add a country to your tax map. That is the product.\n\n"
                "The question is not which percentage is smaller. It is whether the extra points "
                "cost less than the paperwork you would otherwise do yourself."
            ),
        },
        {
            "title": "At $20 a month the assembled stack loses by $20",
            "content": (
                "Take 1,000 subscribers at $20, all domestic cards, $20,000 of volume, and assume you "
                "are registered to collect tax everywhere you sell. If you are not, the Tax line is "
                "smaller and the Stripe stack cheaper.\n\n"
                "| Line | Assembled Stripe stack | Merchant of record |\n|---|---|---|\n"
                "| Payments | 2.9% × $20,000 = $580, plus 1,000 × 30¢ = $300 | — |\n"
                "| Billing | 0.7% × $20,000 = $140 | — |\n"
                "| Tax Basic | 1,000 × 50¢ = $500 | — |\n"
                "| Single fee | — | 5% × $20,000 = $1,000, plus 1,000 × 50¢ = $500 |\n"
                "| **Total** | **$1,520** | **$1,500** |\n\n"
                "Move the price to $100 and keep the same $20,000: Stripe bills $580 + $140 + "
                "$160 = $880, the merchant of record bills $1,000 + $100 = $1,100. The crossover "
                "is one equation: 3.6% × P + 80¢ = 5% × P + 50¢, so 1.4% × P = 30¢, and P = $21.43."
            ),
        },
        {
            "title": "Every foreign card multiplies the crossover by fourteen",
            "content": (
                "1.5% for an international card turns 3.6% + 80¢ into 5.1% + 80¢. Against 5% + "
                "50¢ the gap becomes 0.1% × P − 30¢, so the merchant of record wins until a single "
                "charge passes $300.\n\n"
                "| Card | Stripe stack | Merchant of record | Cheaper |\n|---|---|---|---|\n"
                "| Domestic | 3.6% + 80¢ | 5% + 50¢ | Stripe above $21.43 |\n"
                "| International | 5.1% + 80¢ | 5% + 50¢ | MoR below $300 |\n"
                "| International, non-USD | 6.6% + 80¢ | 5% + 50¢ | MoR at every price |\n\n"
                "The third row is the one people miss. A euro customer paying with a euro card "
                "costs 6.6% + 80¢, which is more than the fee that supposedly includes filing for "
                "thirty countries. Currency conversion is charged on top of the international card "
                "fee, so both can land on one charge."
            ),
        },
        {
            "title": "What the extra points buy, and what they take",
            "content": (
                "For the fee you get fraud screening, chargeback handling, buyer support and the "
                "remittance itself. Paddle lists payments, subscriptions, tax, fraud protection and "
                "billing support inside the 5%. Lemon Squeezy lists the same set and states the "
                "liability plainly: it takes on tax collection and pays the taxes on your behalf.\n\n"
                "The cost is control:\n\n"
                "- You do not hold the merchant account, so the acquirer relationship and the risk "
                "decision are theirs.\n"
                "- Refund and chargeback conversations belong to their support queue, not yours.\n"
                "- Leaving means moving subscribers, and Paddle sells that as a migration service "
                "rather than a button.\n\n"
                "Stripe's answer is Tax Complete, which monitors thresholds, registers in 90+ "
                "countries and files returns. It is priced in tiers by registrations, transactions "
                "and filings, and the tiers are a quote rather than a number on the page."
            ),
        },
        {
            "title": "Where each one breaks",
            "content": (
                "Stripe breaks at the first country you sell into without registering. Tax Basic "
                "tells you the tax is due and meters 50¢ once you are registered; it does not "
                "register you, and back taxes plus penalties appear on no price sheet.\n\n"
                "The merchant of record breaks on the fixed fee. 50¢ is 5.6% of a $9 product, so a "
                "$9 sale keeps $8.05 before hosting. Paddle's own FAQ routes products under $10 to "
                "custom pricing, which is the same admission in a politer sentence.\n\n"
                "It breaks again at the top, because 5% never thins out. A $200,000 month split into "
                "1,000 charges of $200 pays $10,000 + $500 on a merchant of record and $7,200 + $800 "
                "on the assembled stack, a $30,000 gap across a year.\n\n"
                "Price three things before you choose: your average charge, the share of cards that "
                "are not domestic, and whether anyone on the team has filed a VAT return."
            ),
        },
    ],
    "cost_math": [
        {
            "label": "1,000 subscribers at $20, domestic cards",
            "formula": (
                "Stripe: 2.9% × $20,000 = $580; 1,000 × 30¢ = $300; Billing 0.7% × $20,000 = $140; "
                "Tax Basic 1,000 × 50¢ = $500. MoR: 5% × $20,000 = $1,000; 1,000 × 50¢ = $500"
            ),
            "result": "$1,520 assembled Stripe stack against $1,500 on either merchant of record",
        },
        {
            "label": "200 subscribers at $100, same $20,000 of volume",
            "formula": (
                "Stripe: 2.9% × $20,000 = $580; 200 × 30¢ = $60; 0.7% × $20,000 = $140; 200 × 50¢ "
                "= $100. MoR: 5% × $20,000 = $1,000; 200 × 50¢ = $100"
            ),
            "result": "$880 on Stripe against $1,100 on a merchant of record, a $220 monthly premium",
        },
        {
            "label": "Break-even price per charge",
            "formula": "3.6% × P + $0.80 = 5% × P + $0.50, so 1.4% × P = $0.30 and P = $21.43",
            "result": "Above $21.43 a charge the assembled stack is cheaper; below it the merchant of record is",
        },
        {
            "label": "A $9 product on a merchant of record",
            "formula": "5% × $9 = $0.45, plus $0.50 fixed = $0.95 per sale; $0.95 ÷ $9 = 10.6%",
            "result": "$0.95 of a $9 sale, with half of it coming from the fixed fee alone",
        },
    ],
    "decision_matrix": [
        {
            "situation": "Average charge under $21 and a team of one",
            "pick": "Lemon Squeezy or Paddle",
            "why": "At $20 the single 5% + 50¢ meter bills $1,500 against $1,520 for the assembled Stripe stack, and nobody has to register for VAT.",
        },
        {
            "situation": "Average charge over $21, mostly domestic cards",
            "pick": "Stripe",
            "why": "The crossover is 1.4% × P = 30¢, so from $21.43 upward the four Stripe meters total less than one merchant-of-record fee.",
        },
        {
            "situation": "Selling into the EU and UK from day one",
            "pick": "Lemon Squeezy or Paddle",
            "why": "An international non-USD card costs the Stripe stack 6.6% + 80¢, which is more than the merchant-of-record fee that includes the filings.",
        },
        {
            "situation": "Enterprise buyers who want invoices, POs and net terms",
            "pick": "Stripe",
            "why": "Invoicing and Billing sit on the same account, and the 0.7% Billing rate excludes one-off invoices.",
        },
        {
            "situation": "A marketplace that pays out to sellers",
            "pick": "Stripe",
            "why": "Neither merchant-of-record price sheet covers paying out to third-party sellers; the 5% + 50¢ is a single-seller fee.",
        },
        {
            "situation": "Products priced under $10",
            "pick": "Paddle, at custom pricing",
            "why": "The 50¢ fixed fee is 5.6% of a $9 sale, and Paddle's FAQ sends sub-$10 products to a bespoke rate instead of the public one.",
        },
        {
            "situation": "$200,000 months with $200 charges",
            "pick": "Stripe",
            "why": "The percentage never falls on a merchant of record: that month pays $10,500 there against $8,000 on the assembled stack.",
        },
        {
            "situation": "Nobody on the team has ever filed a VAT return",
            "pick": "A merchant of record",
            "why": "Tax Basic meters 50¢ per registered transaction but does not register you; the registrations and filings are the part you are buying.",
        },
    ],
    "verdict_summary": (
        "Below roughly $21 per charge, or on any card that is not domestic, the merchant of record "
        "is the cheaper invoice, not the expensive one. Above it, the assembled Stripe stack wins on "
        "price and only on price: the moment you are not doing the registrations and filings yourself, "
        "the two points you saved are paying for work you still owe."
    ),
    "migration_guide": (
        "Leaving a merchant of record means moving subscribers, and there is no card-data path "
        "between the two: cards stored with the merchant of record do not transfer, so each customer "
        "either re-enters payment details or you run both systems until the next renewal. Product "
        "and price objects are recreated on the other side, and historical tax filings stay with "
        "whoever made them. Paddle sells this as a migration service; on Stripe the same move is "
        "exports plus a dunning sequence you write.\n\n"
        "Going the other way, from Stripe to a merchant of record, the tax history is the part that "
        "does not travel. You keep the records, the new merchant registers where it needs to, and "
        "the previous filings remain your responsibility for the periods you owned them."
    ),
    "faqs": [
        {
            "q": "Does the 5% + 50¢ include payment processing?",
            "a": "Yes. Both pages describe one all-in fee covering payments, checkout, subscriptions, tax collection, fraud screening and buyer support, with no monthly fee on top.",
        },
        {
            "q": "Is Stripe Tax the same thing as a merchant of record?",
            "a": "No. Tax Basic calculates and collects tax where you are registered and meters 50¢ per transaction. Registration and filing are yours unless you buy Tax Complete, which is tiered and quoted.",
        },
        {
            "q": "What does an international card add on Stripe?",
            "a": "1.5% on top of 2.9% + 30¢, and currency conversion is a separate 1.5% when the charge is not in your settlement currency.",
        },
        {
            "q": "Can a merchant of record refuse a product?",
            "a": "It is the seller named on the receipt, so what it will and will not sell is its decision to make. That approval is part of what the 5% covers.",
        },
    ],
    "sources": [
        "https://stripe.com/pricing",
        "https://stripe.com/billing/pricing",
        "https://stripe.com/tax/pricing",
        "https://www.lemonsqueezy.com/pricing",
        "https://www.paddle.com/pricing",
    ],
    "related": [
        {"slug": "resend-vs-sendgrid", "name": "Resend vs SendGrid", "why": "The same fixed-fee trap, one decimal place smaller: 50¢ on a $9 sale is 5.6%."},
        {"slug": "datadog-vs-grafana-cloud", "name": "Datadog vs Grafana Cloud", "why": "Another invoice built from meters the pricing page lists one at a time."},
    ],
    "tool_a": {
        "name": "Stripe",
        "tagline": "Four meters, one invoice, and you are the seller",
        "db": "Payments, Billing and Tax as separate line items",
        "pricing": "2.9% + 30¢ domestic · +1.5% international · Billing 0.7% · Tax 50¢ per transaction",
        "self_host": "No (Stripe-hosted checkout and portal)",
        "realtime": "You are the seller of record: registrations, filings and penalties are yours",
        "ai_readiness": "Radar fraud screening included; Smart Disputes takes 30% of a recovered dispute",
        "lock_in": "Low on card data, high on tax history: filings stay in your name",
        "badge": "3.6% + 80¢ assembled",
        "cta_url": "https://stripe.com/?utm_source=devteardown",
        "pros": [
            "Four meters you can turn off: Tax Basic and Billing are opt-in, so the fee follows the feature",
            "Payments, Billing and Invoicing share one customer record, so a one-off invoice skips the 0.7%",
            "Disputes cost $15 flat, which is cheaper than losing the dispute and the goods",
            "The exit is real: card tokens export and the API is documented, so a PSP swap is a project rather than a rewrite",
        ],
        "cons": [
            "The 2.9% + 30¢ on the pricing page is not the rate a subscription business pays",
            "Tax Basic meters 50¢ per registered transaction and still leaves registration and filing to you",
            "An international non-USD card carries 1.5% twice, before anyone mentions VAT",
            "Tax Complete, the part that would replace a merchant of record, is a quoted tier",
        ],
        "code_example": (
            "// Stripe: you are the seller, so the tax switch is yours to get wrong.\n"
            "import Stripe from \"stripe\";\n"
            "const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);\n\n"
            "const session = await stripe.checkout.sessions.create({\n"
            "  mode: \"subscription\",\n"
            "  line_items: [{ price: process.env.PRICE_20_MONTHLY, quantity: 1 }],\n"
            "  automatic_tax: { enabled: true }, // 50¢ per transaction once registered\n"
            "  customer_update: { address: \"auto\" },\n"
            "  success_url: \"https://app.example.com/ok?session={CHECKOUT_SESSION_ID}\",\n"
            "  cancel_url: \"https://app.example.com/pricing\",\n"
            "});\n"
            "// Breaks when: automatic_tax is on and you never registered in the buyer's country.\n"
            "// No tax is collected, the liability stays yours, and the invoice still looks right."
        ),
    },
    "tool_b": {
        "name": "Lemon Squeezy / Paddle",
        "tagline": "One meter for payments, tax and the seller's name on the receipt",
        "db": "Checkout, subscriptions and tax remittance as a single fee",
        "pricing": "5% + 50¢ per transaction on both · $0 per month · custom pricing under $10",
        "self_host": "No (both act as the merchant of record)",
        "realtime": "They are the seller: tax collection and remittance sit with them, not you",
        "ai_readiness": "Fraud screening and buyer support are inside the 5%, not priced separately",
        "lock_in": "Medium: subscriptions move through a paid migration, and cards do not transfer",
        "badge": "5% + 50¢",
        "cta_url": "https://www.paddle.com/?utm_source=devteardown",
        "pros": [
            "One percentage and one fixed fee cover payments, tax, fraud and buyer support",
            "No monthly fee on either, so the cost is zero until the first sale",
            "Tax collection follows the merchant's registrations, so a new country does not add a filing",
            "Both publish no lock-in period, and both sell a migration service for the exit",
        ],
        "cons": [
            "The percentage never thins out: a $200,000 month pays $10,500 where Stripe pays $8,000",
            "50¢ per transaction is 5.6% of a $9 product and 11% of a $4.50 one",
            "You do not hold the merchant account, so the risk decision and support queue are theirs",
            "Subscription data moves through a migration rather than an export you run yourself",
        ],
        "code_example": (
            "// Paddle: the tax never becomes your line item, but the webhook is the billable event.\n"
            "import { Paddle, Environment } from \"@paddle/paddle-node-sdk\";\n"
            "const paddle = new Paddle(process.env.PADDLE_API_KEY, {\n"
            "  environment: Environment.production,\n"
            "});\n\n"
            "const transaction = await paddle.transactions.create({\n"
            "  items: [{ priceId: process.env.PRICE_20_MONTHLY, quantity: 1 }],\n"
            "  customData: { account_id: \"acc_123\" },\n"
            "});\n"
            "// Breaks when: you grant access from this response. The transaction is not the\n"
            "// subscription; only the subscription webhook says the 5% + 50¢ was collected.\n"
            "return transaction.id;"
        ),
    },
}


ANTHROPIC = {
    "slug": "anthropic-vs-openai-api-pricing",
    "category": "AI & LLM APIs",
    "last_verified": "2026-11-10",
    "published": "2026-11-10",
    "hook": (
        "Claude Sonnet 5.5 and GPT-6.1 Sol list the same price: $2 per million input tokens and "
        "$10 per million output. The same thousand documents do not cost the same on both, because "
        "one tokenizer counts about 30% more tokens for the same text."
    ),
    "sections": [
        {
            "title": "Two sheets, one identical sticker",
            "content": (
                "The flagship rows of both price sheets match to the cent, and so do the cache reads.\n\n"
                "| Per million tokens | Claude Sonnet 5.5 | GPT-6.1 Sol |\n|---|---|---|\n"
                "| Input | $2.00 | $2.00 |\n"
                "| Output | $10.00 | $10.00 |\n"
                "| Cached input (hit) | $0.10 | $0.10 |\n"
                "| 5m or 30m cache write | $2.50 (1.25x) | $2.50 (1.25x) |\n"
                "| Batch input / output | $1.00 / $5.00 | $1.00 / $5.00 |\n\n"
                "Anthropic's Opus 5.5 sits one rung up at $4 and $20, with cache reads at $0.20. "
                "OpenAI's GPT-6 Astra sits at $10 and $50. On the flagship row there is nothing to "
                "choose, which is the first sign that the model price is not the decision."
            ),
        },
        {
            "title": "The tokenizer changes the invoice before your prompt does",
            "content": (
                "Anthropic's pricing page carries a note most price sheets would leave out: Claude "
                "4.7 and later use a newer tokenizer that produces approximately 30% more tokens for "
                "the same text.\n\n"
                "So the sticker is $2 per million tokens, and the bill is $2 per million tokens of "
                "Claude's counting. For text that costs $2.00 per million source tokens on a standard "
                "tokenizer, the same text costs $2.00 × 1.3 = $2.60.\n\n"
                "That is a 30% difference on the largest line of a RAG or agent bill, and it does not "
                "appear anywhere in a side-by-side table that compares per-token prices. The note also "
                "says the exact increase depends on the content, so treat 1.3 as a working multiplier, "
                "not a constant."
            ),
        },
        {
            "title": "Caching is a break-even test, not a discount",
            "content": (
                "Both vendors sell the same shape: pay more to write a prefix, pay less to read it. "
                "The multipliers are where they part.\n\n"
                "| Cache operation | Anthropic | OpenAI |\n|---|---|---|\n"
                "| Write, short | 1.25x, 5 minutes | 1.25x, 30 minutes |\n"
                "| Write, long | 2x, 1 hour | 2.5x, 12 hours |\n"
                "| Read (hit) | 0.1x, or 0.05x on 5.5 models | 0.05x |\n\n"
                "A cached prefix costs 1.25 + 0.1n to serve n requests, against n uncached. The "
                "break-even is n = 1.39, so the second request already wins, and ten requests cost "
                "2.25 instead of 10, a 77.5% cut on the input line. The long windows are worse "
                "deals for short runs: 2x + 0.1n beats n only from the third request, and OpenAI's "
                "2.5x write needs three reads before it pays."
            ),
        },
        {
            "title": "Batch is the one line where both sheets agree",
            "content": (
                "Both vendors halve input and output for asynchronous work. Anthropic publishes the "
                "batch rows separately; OpenAI prints a Batch table and a separate Flex table at the "
                "same numbers.\n\n"
                "| Batch, per million | Claude Sonnet 5.5 | Claude Opus 5.5 | GPT-6.1 Sol |\n|---|---|---|---|\n"
                "| Input | $1.00 | $2.00 | $1.00 |\n"
                "| Output | $5.00 | $10.00 | $5.00 |\n\n"
                "Anthropic's page says its cache multipliers stack with the batch discount. That "
                "combination is the cheapest published way to process a large, stable corpus: a "
                "cached prefix at 0.1x inside a batch, on a job that can wait. The trap is that a "
                "nightly single-run job has nothing to read from, and a cold cache write just adds "
                "25% to a batch you could have submitted uncached."
            ),
        },
        {
            "title": "Long prompts are where the sheets stop being comparable",
            "content": (
                "Both vendors reprice the prompt once it gets long, and they do it in different "
                "shapes.\n\n"
                "| Prompt size | GPT-6.1 Sol | Claude Haiku 5.5 |\n|---|---|---|\n"
                "| Short context, input | $2.00 | $0.10 up to 100,000 tokens |\n"
                "| Long context, input | $4.00 | $0.50 over 100,000 tokens |\n"
                "| Long context, output | $15.00 | $2.50 over 100,000 tokens |\n\n"
                "OpenAI's long-context row doubles input and multiplies output by 1.5. Anthropic's "
                "Haiku sheet lists two rows, one for prompts up to 100,000 tokens and one for prompts "
                "over it, at five times the rate, and it does not print a marginal split.\n\n"
                "A 200,000-token prompt therefore bills at 0.2 × $0.50 = $0.10 on the over-100k row "
                "against $0.02 if the same prompt fit under the line. That cliff, not the per-token "
                "sticker, is what a document pipeline hits when someone pastes a whole contract set."
            ),
        },
        {
            "title": "Three add-ons that quietly change the unit",
            "content": (
                "Fast mode on both sides doubles the sticker: Opus 5.5 goes to $8 input and $40 "
                "output, GPT-6.1 Sol to $4 and $20. Anthropic notes that fast mode is not available "
                "with the Batch API, so the two savings cannot be stacked.\n\n"
                "Data residency is a multiplier rather than a tier. Sending Claude 4.6 or later to "
                "US-only inference applies 1.1x to every token category, cache writes and reads "
                "included.\n\n"
                "The third is the cache window, and it is easy to lose money on. A 12-hour write "
                "costs 2.5x, so a job that runs twice a day should skip caching entirely rather than "
                "pay 2.5x for a prefix it reads once. Check the read count before enabling it: "
                "three reads is where the long window starts to earn."
            ),
        },
    ],
    "cost_math": [
        {
            "label": "100k requests, 16k cached prefix, 4k fresh input, 500 output",
            "formula": (
                "Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits "
                "90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = $800; "
                "output 100,000 × 500 = 50M × $10 = $500"
            ),
            "result": "$1,844 on either vendor at list price, before the tokenizer",
        },
        {
            "label": "The same workload through a tokenizer that counts 30% more",
            "formula": "$1,844 × 1.3 = $2,397.20, applying Anthropic's stated ~30% token increase",
            "result": "$2,397 against $1,844 for identical text, a 30% difference on a sheet whose per-token prices match",
        },
        {
            "label": "Cache break-even on a shared prefix",
            "formula": "1.25 + 0.10n < n, so n > 1.39; at n = 10 the cost is 1.25 + 1.00 = 2.25 against 10 uncached",
            "result": "Profitable from the second request; 77.5% off the input line by the tenth",
        },
        {
            "label": "Long window write on a twice-daily job",
            "formula": "OpenAI 12h: 2.5 write + 0.10 read = 2.60, against 2 × 1.00 = 2.00 uncached. Anthropic 1h: 2.0 write + 0.10 read = 2.10, against 2.00",
            "result": "2.6 against 2.0: caching a prefix read twice costs more than not caching it under either vendor's long window",
        },
    ],
    "decision_matrix": [
        {
            "situation": "A long, stable system prompt at high volume",
            "pick": "Either; decide on the tokenizer",
            "why": "Both bill the prefix at 1.25x to write and 0.10x or 0.05x to read, so a 30% token difference decides more than the cache terms do.",
        },
        {
            "situation": "Prompts that regularly pass 100,000 tokens",
            "pick": "Weigh the long-context row first",
            "why": "OpenAI doubles input and multiplies output by 1.5 past the boundary; Haiku 5.5 lists a rate five times higher for prompts over 100,000 tokens.",
        },
        {
            "situation": "Nightly batch of a few hundred thousand jobs",
            "pick": "Batch API on either",
            "why": "Both halve input and output, and a single nightly pass has no cache to read from, so a cold write only adds 25%.",
        },
        {
            "situation": "A job that runs every 12 hours over one corpus",
            "pick": "No cache at all",
            "why": "The 12-hour write costs 2.5x and the 1-hour write has expired by the next run; two uncached passes cost 2.0 against 2.6.",
        },
        {
            "situation": "Output-heavy generation, 500+ tokens per call",
            "pick": "GPT-6.1 Sol over Opus 5.5",
            "why": "Output is 5x input on both sheets, so the $10 against $20 output rate dominates the bill long before the input line does.",
        },
        {
            "situation": "Streaming that a user is watching",
            "pick": "Fast mode, at 2x",
            "why": "Opus 5.5 moves to $8 and $40 and GPT-6.1 Sol to $4 and $20, and fast mode cannot be combined with batch.",
        },
        {
            "situation": "Data must stay in the US",
            "pick": "Price the 1.1x before comparing",
            "why": "US-only inference multiplies every Claude token category by 1.1, cache writes and reads included, which changes a close comparison.",
        },
        {
            "situation": "A prototype with prompts under 100,000 tokens",
            "pick": "Claude Haiku 5.5",
            "why": "$0.10 input and $0.50 output per million is a twentieth of the flagship rows, and the over-100k rate only applies when the prompt crosses the line.",
        },
    ],
    "verdict_summary": (
        "On the flagship row the two sheets are the same page: $2 in, $10 out, $0.10 cached. The "
        "choice is decided by three things that are not on that row, the tokenizer's 30% count, the "
        "long-context shape, and how many times your prefix is actually read. If your prompts stay "
        "under 100,000 tokens and your cache is warm, you are choosing a vendor on arithmetic that "
        "differs by a few percent; if they cross the line, you are choosing on a cliff."
    ),
    "migration_guide": (
        "Moving between the two APIs is mostly a prompt rewrite, because the cache is the part that "
        "does not travel: Anthropic takes an explicit breakpoint marker, OpenAI caches a stable "
        "prefix automatically. Re-measure your token counts on the new tokenizer before you migrate "
        "pricing assumptions, since the same text will not bill the same number of tokens.\n\n"
        "Everything asynchronous needs resubmission. Batch jobs, files and fine-tuned endpoints are "
        "per-vendor objects with no portable format, and model deprecations retire a SKU you may "
        "still be calling, so keep the model name in configuration rather than in code."
    ),
    "faqs": [
        {
            "q": "Is prompt caching automatic on both?",
            "a": "No. Anthropic takes a cache_control marker on the block you want cached, and OpenAI caches a stable prefix automatically with no marker to place.",
        },
        {
            "q": "Do the batch discount and the cache discount combine?",
            "a": "On Anthropic the page says cache multipliers stack with the batch discount. OpenAI publishes separate Batch and Flex tables at the same rates, and fast mode is excluded from batch on Anthropic.",
        },
        {
            "q": "What does the 30% tokenizer note change?",
            "a": "It raises the effective price per unit of source text by about 30% on Claude 4.7 and later, against a sheet whose per-token rates are otherwise identical to the competitor's.",
        },
        {
            "q": "Is a cache write ever a loss?",
            "a": "Yes. The 1.25x short write needs a read to pay for itself and the 2x or 2.5x long write needs two or three, so a job that reads the prefix once bills more with caching than without.",
        },
    ],
    "sources": [
        "https://docs.anthropic.com/en/docs/about-claude/pricing",
        "https://platform.openai.com/docs/pricing",
        "https://platform.claude.com/docs/en/build-with-claude/prompt-caching",
        "https://platform.claude.com/docs/en/build-with-claude/batch-processing",
        "https://claude.com/pricing",
    ],
    "related": [
        {"slug": "datadog-vs-grafana-cloud", "name": "Datadog vs Grafana Cloud", "why": "The same discipline on a monitoring invoice: find the meter, then print the formula."},
        {"slug": "aws-lambda-vs-cloudflare-workers", "name": "AWS Lambda vs Cloudflare Workers", "why": "When the bill depends on whether you charge for waiting or for working."},
    ],
    "tool_a": {
        "name": "Anthropic",
        "tagline": "Per-token pricing with an explicit cache breakpoint",
        "db": "Claude API: messages, prompt caching and batch in one price sheet",
        "pricing": "Sonnet 5.5 $2 / $10 · Opus 5.5 $4 / $20 · Haiku 5.5 $0.10 / $0.50 per MTok",
        "self_host": "No (first-party API, Bedrock and Google Cloud endpoints)",
        "realtime": "Cache reads at 0.1x, or 0.05x on Opus 5.5 and Sonnet 5.5; writes 1.25x for 5m and 2x for 1h",
        "ai_readiness": "Batch halves both sides; fast mode doubles; US-only inference adds 1.1x",
        "lock_in": "Medium: model deprecations retire SKUs, and cache breakpoints are vendor-specific",
        "badge": "Cache breakpoints",
        "cta_url": "https://claude.com/pricing?utm_source=devteardown",
        "pros": [
            "Two cache windows on every model, 5 minutes and 1 hour, priced at 1.25x and 2x",
            "Cache reads cost 0.05x on Opus 5.5 and Sonnet 5.5, cheaper than the standard 0.1x row",
            "The batch and cache multipliers stack, which is the cheapest published path for a stable corpus",
            "Haiku 5.5 starts at $0.10 input for prompts under 100,000 tokens, with a documented higher row above it",
        ],
        "cons": [
            "The 4.7-and-later tokenizer produces about 30% more tokens for the same text, which the per-token price hides",
            "The over-100,000-token Haiku row is five times the rate and is printed as a whole-prompt rate",
            "Fast mode doubles the sheet and cannot be stacked with the batch discount",
            "US-only inference applies 1.1x to cache writes and reads, not just to fresh input",
        ],
        "code_example": (
            "// Anthropic bills the prefix once: the breakpoint is a marker, not a hint.\n"
            "import Anthropic from \"@anthropic-ai/sdk\";\n"
            "const client = new Anthropic();\n\n"
            "const msg = await client.messages.create({\n"
            "  model: \"claude-sonnet-5-5\",\n"
            "  max_tokens: 512,\n"
            "  system: [{\n"
            "    type: \"text\",\n"
            "    text: SYSTEM_PROMPT,\n"
            "    cache_control: { type: \"ephemeral\" }, // 1.25x write, then 0.10x reads\n"
            "  }],\n"
            "  messages: [{ role: \"user\", content: question }],\n"
            "});\n"
            "// Breaks when: the breakpoint sits after a timestamp or a user id. Every request\n"
            "// then writes a new prefix and pays 1.25x instead of reading at 0.10x.\n"
            "console.log(msg.usage);"
        ),
    },
    "tool_b": {
        "name": "OpenAI",
        "tagline": "Per-token pricing with automatic prefix caching and two windows",
        "db": "GPT API: tokens, cached input, Batch and Flex as separate rate cards",
        "pricing": "GPT-6.1 Sol $2 / $10 · GPT-6 Astra $10 / $50 · GPT-6 Luna $0.10 / $0.50 per MTok",
        "self_host": "No (first-party API and Azure-hosted deployments)",
        "realtime": "Cached input at 0.05x; writes 1.25x for 30 minutes and 2.5x for 12 hours",
        "ai_readiness": "Batch and Flex halve both sides; long context doubles input and multiplies output by 1.5",
        "lock_in": "Medium: batch files and assistants are per-vendor objects with no export",
        "badge": "Automatic caching",
        "cta_url": "https://openai.com/api/pricing/?utm_source=devteardown",
        "pros": [
            "Caching needs no marker: keep the prefix byte-identical and the discount applies",
            "A 12-hour cache window exists, which suits jobs spread over a working day",
            "Flex is priced at the batch rate, so the discount is available without the queue",
            "Long context is priced as a multiplier on the same row, so the jump is visible before you hit it",
        ],
        "cons": [
            "The 12-hour write costs 2.5x, so it needs three reads before it beats paying full price",
            "Long context doubles input and multiplies output by 1.5, which lands on the most expensive line",
            "A single changed byte in the prefix is a silent cache miss at full input price",
            "Fast mode doubles the sheet and is a separate rate card from the standard one",
        ],
        "code_example": (
            "// OpenAI caches automatically: there is no marker, only a prefix to keep stable.\n"
            "import OpenAI from \"openai\";\n"
            "const client = new OpenAI();\n\n"
            "const res = await client.responses.create({\n"
            "  model: \"gpt-6.1-sol\",\n"
            "  input: [\n"
            "    { role: \"system\", content: SYSTEM_PROMPT }, // byte-identical every call\n"
            "    { role: \"user\", content: question },\n"
            "  ],\n"
            "});\n"
            "// Breaks when: the system prompt is assembled with a date or a request id.\n"
            "// A changed prefix is a cache miss billed at the full $2 per million.\n"
            "console.log(res.usage?.input_tokens_details);"
        ),
    },
}
