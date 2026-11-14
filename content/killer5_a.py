"""Killer comparison batch A: payments and LLM API pricing.

Numbers come from the fact sheets written alongside each item; every figure below is either
a published unit price or arithmetic printed with its formula.
"""

STRIPE = {'slug': 'stripe-vs-lemonsqueezy-vs-paddle',
 'category': 'Payments & Billing',
 'last_verified': '2026-11-14',
 'published': '2026-11-10',
 'hook': 'For 1,000 monthly $20 subscriptions, the modeled fees are $1,120 on Stripe with no-code '
         'Tax, $1,520 with Tax API, $1,600 on Lemon Squeezy and $1,500 on Paddle. The integration '
         'path and subscription surcharge change the ranking.',
 'sections': [{'title': 'Start with a defined account and checkout',
               'content': 'These are standard US Stripe card rates, not a quote for a Korean '
                          'business. Eligibility, negotiated contracts, tax treatment and '
                          'settlement currency must be checked before choosing a provider.\n'
                          '\n'
                          '| Stripe component | Published rate | Scope |\n'
                          '|---|---|---|\n'
                          '| Domestic cards | 2.9% + 30¢ | successful charge |\n'
                          '| International cards | +1.5% | applicable international cards |\n'
                          '| Currency conversion | +1% | when conversion is required |\n'
                          '| Billing pay-as-you-go | 0.7% | Billing volume |\n'
                          '| Tax Basic no-code | 0.5% | registered transactions |\n'
                          '| Tax Basic API | 50¢ | registered transactions |\n'
                          '\n'
                          'No-code Tax applies to integrations such as Checkout and Billing. The '
                          'API price is a different integration path, not a fee to add to the '
                          'no-code rate. Registration, filing and optional services need their own '
                          'budget.'},
              {'title': 'The two merchants have different fee rules',
               'content': 'Lemon Squeezy and Paddle advertise a base 5% + 50¢, but that does not '
                          'make their subscription invoices identical.\n'
                          '\n'
                          '- Lemon Squeezy adds 0.5 percentage points for subscriptions, 1.5 for '
                          'applicable non-US transactions and 1.5 for PayPal. Its fee uses the '
                          'total order value, including tax.\n'
                          '- Paddle advertises 5% + 50¢ per Checkout transaction with '
                          'subscriptions included. Do not copy Lemon Squeezy surcharges onto '
                          'Paddle.\n'
                          '- Account-specific pricing, payouts and optional services can change '
                          'either result.\n'
                          '\n'
                          'A merchant of record handles covered transaction tax obligations as the '
                          'seller. That is not a promise that your business has no income-tax, '
                          'reporting or other legal obligations. Compare the service scope as well '
                          'as the checkout fee.'},
              {'title': 'Four invoices for the same subscription volume',
               'content': 'Assume 1,000 successful $20 renewals: $20,000 charged, no added tax, '
                          'refunds, disputes, FX or payout fees. Use US domestic cards for Stripe '
                          'and no international or PayPal surcharge for Lemon Squeezy; assume '
                          'every transaction incurs the chosen Tax Basic fee.\n'
                          '\n'
                          '| Provider / path | Arithmetic | Total |\n'
                          '|---|---|---|\n'
                          '| Stripe + no-code Tax | $580 + $300 Payments + $140 Billing + $100 Tax '
                          '| $1,120 |\n'
                          '| Stripe + Tax API | $580 + $300 + $140 + $500 | $1,520 |\n'
                          '| Lemon Squeezy subscription | 5.5% × $20,000 + 1,000 × $0.50 | $1,600 '
                          '|\n'
                          '| Paddle standard | 5% × $20,000 + 1,000 × $0.50 | $1,500 |\n'
                          '\n'
                          'Correction, November 14: the earlier $1,500 Lemon Squeezy subscription '
                          'example omitted its surcharge. The old universal $21.43 crossover also '
                          "assumed the Tax API path and Paddle's base rate, not every subscription "
                          'setup.'},
              {'title': 'Country and tax change the denominator',
               'content': 'Use the actual checkout total, not just the advertised product price. A '
                          'hypothetical $20 subscription with 20% tax creates a $24 order; if '
                          "Lemon Squeezy's non-US surcharge applies, its fee is 7% × $24 + $0.50 = "
                          '$2.18, before payout costs.\n'
                          '\n'
                          '| Change from the base model | Consequence |\n'
                          '|---|---|\n'
                          '| Lemon Squeezy non-US subscription | 7% + 50¢; PayPal can add another '
                          '1.5 points |\n'
                          '| Stripe international card | add 1.5 points to its applicable stack |\n'
                          '| Stripe FX conversion | add 1 point when required |\n'
                          '| Tax-inclusive versus tax-exclusive price | calculate from the actual '
                          'fee base |\n'
                          '\n'
                          'Lemon Squeezy also documents region-dependent payout fees. These are '
                          'separate from checkout fees and excluded from the worked totals. '
                          "Paddle's own contract and payout terms must be evaluated separately; a "
                          'foreign buyer alone does not establish which provider wins.'},
              {'title': 'The crossover belongs to one set of assumptions',
               'content': 'With the same tax-free US model, Stripe plus no-code Tax is 4.1% × P + '
                          '$0.30 per charge, lower than both modeled MoR fees at every positive P. '
                          'With Tax API it is 3.6% × P + $0.80.\n'
                          '\n'
                          '- Against Paddle: $0.30 / (5% − 3.6%) = $21.43.\n'
                          '- Against a Lemon Squeezy subscription: $0.30 / (5.5% − 3.6%) = '
                          '$15.79.\n'
                          '- A $9 Lemon Squeezy subscription costs $0.995 before other fees, not '
                          'the $0.95 base one-time illustration.\n'
                          '\n'
                          'Those are processing comparisons, not total operating costs. Neither '
                          'result prices engineering, tax registration, filing, buyer support or '
                          'risk. A cheaper fee model can still be the more expensive business '
                          'process.'},
              {'title': 'Choose the service before trusting the headline',
               'content': 'For Stripe Payments with Billing, you remain the seller. Tax Basic is '
                          'calculation and collection tooling; Tax Complete offers a separate '
                          'registration and filing service with its own plans and limits. Stripe '
                          'also markets Managed Payments as a distinct MoR product, which is '
                          'outside these calculations.\n'
                          '\n'
                          'For a covered Paddle or Lemon Squeezy sale, the provider is the '
                          'merchant of record. Approval, product eligibility, refunds, '
                          'chargebacks, payout timing and reserves still matter.\n'
                          '\n'
                          '- Confirm the business and bank country are supported.\n'
                          '- Obtain the applicable rate card and test a representative receipt.\n'
                          '- Model the real card mix, tax totals and average charge.\n'
                          '- Check migration and data portability with both providers before '
                          'committing.\n'
                          '\n'
                          'A checkout demo is not proof of live eligibility or settlement. None of '
                          'the examples establishes that a Korean account will be approved or '
                          'receive the modeled net amount.'}],
 'cost_math': [{'label': '1,000 monthly $20 renewals, defined US base model',
                'formula': 'Stripe no-code: $580 + $300 + $140 + $100. Stripe API: $580 + $300 + '
                           '$140 + $500. Lemon Squeezy: 0.055 × $20,000 + $500. Paddle: 0.05 × '
                           '$20,000 + $500.',
                'result': '$1,120 / $1,520 / $1,600 / $1,500 respectively; excludes taxes added to '
                          'the price and other fees.'},
               {'label': '200 monthly $100 renewals, same $20,000 total',
                'formula': 'Stripe no-code: $580 + $60 + $140 + $100 = $880. Stripe API: $580 + '
                           '$60 + $140 + $100 = $880. Lemon Squeezy: $1,100 + $100. Paddle: $1,000 '
                           '+ $100.',
                'result': '$880 Stripe on either Tax path; $1,200 Lemon Squeezy; $1,100 Paddle '
                          'under the same assumptions.'},
               {'label': 'Tax API path crossover only',
                'formula': 'Stripe 0.036P + $0.80. Paddle 0.05P + $0.50: P = $0.30 / 0.014. Lemon '
                           'Squeezy subscription 0.055P + $0.50: P = $0.30 / 0.019.',
                'result': '$21.43 versus Paddle, $15.79 versus Lemon Squeezy; neither is a '
                          'universal crossover.'},
               {'label': 'Hypothetical non-US taxed subscription on Lemon Squeezy',
                'formula': '$20 + 20% tax = $24 total; (5% + 0.5% subscription + 1.5% '
                           'international) × $24 + $0.50 = $2.18.',
                'result': '$2.18 fee before payout costs; with an additional 1.5-point PayPal fee, '
                          '$2.54.'}],
 'decision_matrix': [{'situation': 'US domestic subscriptions with Checkout Tax',
                      'pick': 'Model Stripe no-code Tax separately',
                      'why': 'The 0.5% path produces $1,120 here, not the $1,520 Tax API total.'},
                     {'situation': 'A custom Tax API integration',
                      'pick': 'Compare all three invoices',
                      'why': 'At $20, Stripe is $1,520, Paddle $1,500 and Lemon Squeezy $1,600 '
                             'under the base assumptions.'},
                     {'situation': 'Non-US buyers or PayPal subscriptions',
                      'pick': 'Use the applicable surcharges',
                      'why': 'Lemon Squeezy lists additional fees; do not reuse the US base total '
                             'or transfer its rules to Paddle.'},
                     {'situation': 'A team without transaction-tax operations',
                      'pick': 'Evaluate an approved MoR',
                      'why': 'Covered tax handling can justify a higher fee, but business '
                             'reporting and eligibility still require review.'},
                     {'situation': 'Very small average charges',
                      'pick': 'Request applicable low-value pricing',
                      'why': 'The fixed 50¢ component weighs heavily; custom rates must be '
                             'confirmed, not assumed.'},
                     {'situation': 'A Korean business seeking payouts',
                      'pick': 'Verify eligibility and settlement first',
                      'why': 'US rate arithmetic does not establish Korean onboarding, payout '
                             'currency, timing or buyer-visible details.'}],
 'verdict_summary': 'There is no single merchant-of-record invoice. In the defined $20 '
                    'subscription model, Stripe no-code Tax costs $1,120, Stripe Tax API $1,520, '
                    'Lemon Squeezy $1,600 and Paddle $1,500. Choose using the actual integration, '
                    'country, tax base and service scope, not the shared 5% headline.',
 'migration_guide': 'Ask both providers to confirm supported subscription and payment-data '
                    'migration, required customer consent, settlement reconciliation and '
                    'historical tax-record handling before scheduling a move. Do not assume either '
                    'automatic portability or that every customer must re-enter a card. Run a '
                    'small approved migration test before moving active renewals; retaining access '
                    'to old records does not transfer earlier obligations.',
 'faqs': [{'q': 'Is 5% + 50¢ the full subscription fee on both MoRs?',
           'a': 'No. Lemon Squeezy adds 0.5 percentage points for subscriptions and may add '
                'international and PayPal fees. Paddle advertises subscriptions within its '
                'standard 5% + 50¢ rate. Check each account contract and payout costs separately.'},
          {'q': 'Does Stripe Tax always cost 50¢ per transaction?',
           'a': 'No. The US Tax Basic page distinguishes 0.5% no-code integrations from a 50¢ API '
                'integration charge for applicable registered transactions. They are alternative '
                'paths, not two fees to add together.'},
          {'q': 'What changes the international comparison?',
           'a': 'Stripe lists +1.5% for international cards and +1% when currency conversion is '
                'required. Lemon Squeezy lists +1.5% for applicable non-US transactions and +1.5% '
                'for PayPal. Tax-inclusive order totals and payout costs also matter.'},
          {'q': 'Do these calculations prove Korean eligibility or remove all tax duties?',
           'a': 'No. Verify supported business and bank countries, account approval, settlement '
                'and legal obligations. MoR transaction-tax handling is not a blanket exemption '
                'from the seller business’s own taxes or reporting.'}],
 'sources': ['https://stripe.com/pricing',
             'https://stripe.com/billing/pricing',
             'https://stripe.com/tax/pricing',
             'https://docs.lemonsqueezy.com/help/getting-started/fees',
             'https://www.paddle.com/pricing'],
 'related': [{'slug': 'resend-vs-sendgrid',
              'name': 'Resend vs SendGrid',
              'why': 'The same fixed-fee trap, one decimal place smaller: 50¢ on a $9 sale is '
                     '5.6%.'},
             {'slug': 'datadog-vs-grafana-cloud',
              'name': 'Datadog vs Grafana Cloud',
              'why': 'Another invoice built from meters the pricing page lists one at a time.'}],
 'tool_a': {'name': 'Stripe',
            'tagline': 'Separate payment, subscription and tax integration meters',
            'db': 'Payments, Billing and Tax as separate line items',
            'pricing': 'US cards 2.9% + 30¢ · Billing 0.7% · Tax no-code 0.5% or API 50¢',
            'self_host': 'No (Stripe-hosted checkout and portal)',
            'realtime': 'Payments + Billing keeps you as seller; Managed Payments is a separate '
                        'product',
            'ai_readiness': 'Optional fraud, tax and billing services have separate scopes',
            'lock_in': 'Confirm supported migration and retain historical records',
            'badge': 'Choose the Tax path',
            'cta_url': 'https://stripe.com/?utm_source=devteardown',
            'pros': ['Choose components to match the integration',
                     'No-code and API Tax paths have different pricing',
                     'Published US card and Billing rates support explicit modeling',
                     'Tax Complete is available separately for broader tax operations'],
            'cons': ['US pricing does not prove Korean account eligibility',
                     'Tax Basic does not by itself cover registrations and filings',
                     'International cards and currency conversion can add fees',
                     'Refunds, disputes, optional services and settlement need their own model'],
            'code_example': '// Pricing illustration only; not a live account configuration.\n'
                            'const gross = 20000;\n'
                            'const charges = 1000;\n'
                            'const payments = gross * 0.029 + charges * 0.30;\n'
                            'const billing = gross * 0.007;\n'
                            'const noCodeTax = gross * 0.005;\n'
                            'const apiTax = charges * 0.50;\n'
                            'console.log(payments + billing + noCodeTax); // 1120\n'
                            'console.log(payments + billing + apiTax); // 1520\n'
                            '// Assumes every charge incurs Tax; do not add both Tax paths.'},
 'tool_b': {'name': 'Lemon Squeezy / Paddle',
            'tagline': 'Separate rate cards, shared merchant-of-record model',
            'db': 'Checkout, subscriptions and tax remittance as a single fee',
            'pricing': 'Lemon subscription 5.5% + 50¢ base · Paddle standard 5% + 50¢',
            'self_host': 'No (both act as the merchant of record)',
            'realtime': 'MoR handles covered transaction tax; own business obligations remain',
            'ai_readiness': 'Compare product approval, buyer support and payout conditions',
            'lock_in': 'Confirm migration support with the providers',
            'badge': 'Check surcharges',
            'cta_url': 'https://www.paddle.com/?utm_source=devteardown',
            'pros': ['MoR transaction-tax handling differs from a payment processor',
                     'Paddle advertises subscriptions within its standard price',
                     'Lemon Squeezy publishes subscription and regional surcharges',
                     'Model each contract before choosing a checkout'],
            'cons': ['Lemon fees use total order value including tax',
                     'International, PayPal and payout fees can affect Lemon costs',
                     'Fixed fees weigh more on low-value purchases',
                     'Eligibility and net settlement are not guaranteed by a price sheet'],
            'code_example': '// Same tax-free US base model, no added international/PayPal fees.\n'
                            'const gross = 20000;\n'
                            'const charges = 1000;\n'
                            'const lemon = gross * (0.05 + 0.005) + charges * 0.50;\n'
                            'const paddle = gross * 0.05 + charges * 0.50;\n'
                            'console.log(lemon, paddle); // 1600, 1500\n'
                            '// Not interchangeable rate cards. Payout and other costs excluded.'}}
ANTHROPIC = {'slug': 'anthropic-vs-openai-api-pricing',
 'category': 'AI & LLM APIs',
 'last_verified': '2026-11-10',
 'published': '2026-11-10',
 'hook': 'Claude Sonnet 5.5 and GPT-6.1 Sol list the same standard rate: $2 per million input tokens and $10 '
         'per million output. Equal rates do not establish equal costs for the same documents. Count each '
         'model separately; there is no measured Claude-versus-GPT token ratio established here.',
 'sections': [{'title': 'Two sheets, one identical sticker',
               'content': 'The flagship rows of both price sheets match to the cent, and so do the cache '
                          'reads.\n'
                          '\n'
                          '| Per million tokens | Claude Sonnet 5.5 | GPT-6.1 Sol |\n'
                          '|---|---|---|\n'
                          '| Input | $2.00 | $2.00 |\n'
                          '| Output | $10.00 | $10.00 |\n'
                          '| Cached input (hit) | $0.10 | $0.10 |\n'
                          '| 5m or 30m cache write | $2.50 (1.25x) | $2.50 (1.25x) |\n'
                          '| Batch input / output | $1.00 / $5.00 | $1.00 / $5.00 |\n'
                          '\n'
                          "Anthropic's Opus 5.5 sits one rung up at $4 and $20, with cache reads at $0.20. "
                          "OpenAI's GPT-6 Astra sits at $10 and $50. On the flagship row there is nothing to "
                          'choose, which is the first sign that the model price is not the decision.'},
              {'title': 'The tokenizer note is not a cross-vendor benchmark',
               'content': 'Anthropic describes a tokenizer change between newer and earlier Claude models, '
                          'not between Claude and GPT. Its approximate 30% increase depends on the text and '
                          'workload. That note cannot establish a fixed Claude-versus-OpenAI price premium.\n'
                          '\n'
                          'There is no universal source-token unit shared by the two vendors. Count the same '
                          'representative input with each target model, then record actual output usage '
                          'separately. Generated answers may differ in length, reasoning usage and quality; '
                          'an input-token ratio does not predict output tokens.\n'
                          '\n'
                          'The $1,844 example below assumes equal billed token counts in each category. It '
                          'is arithmetic, not a measured identical-text benchmark. The separate input-only '
                          'sensitivity case deliberately leaves the $500 output line unchanged and is not a '
                          'prediction for either vendor.\n'
                          '\n'
                          'Correction, 13 November 2026: removed the unsupported cross-vendor 30% claim and '
                          'the whole-bill multiplier. Cache controls, hit rates and reuse arithmetic were '
                          'also corrected on this date; other rates retain their original verification '
                          'date.'},
              {'title': 'Caching is a break-even test, not a discount',
               'content': 'For standard short-context Sonnet 5.5 and GPT-6.1 Sol, the hit rate is $0.10 / '
                          '$2.00 = 0.05x; other models differ.\n'
                          '\n'
                          '| Cache operation | Sonnet 5.5 | GPT-6.1 Sol |\n'
                          '|---|---|---|\n'
                          '| Short write | 1.25x, 5m | 1.25x, 30m |\n'
                          '| Long write | 2x, 1h | 2.5x, 12h |\n'
                          '| Hit | 0.05x | 0.05x |\n'
                          '\n'
                          'Let n be total requests, including the cold first request. One write and n-1 '
                          'successful full-prefix reads cost w + r(n-1), not w + rn. This excludes fresh '
                          'input and output and assumes no intervening expiry, prefix change or rewrite.\n'
                          '\n'
                          'Short writes: 1.25 + 0.05(n-1) < n means n > 1.2632. At ten requests, 1.25 + 0.05 '
                          '× 9 = 1.70 versus 10 uncached: 83% less for this prefix alone. With a 0.1x model '
                          'the corresponding total is 2.15, a 78.5% reduction.\n'
                          '\n'
                          'Long writes at 0.05x reads need three total requests (one write, two hits): '
                          'Sonnet costs 2.10 and Sol costs 2.60 versus 3 uncached. Never count an expired '
                          'entry as a hit.'},
              {'title': 'Batch is the one line where both sheets agree',
               'content': 'Both vendors halve input and output for asynchronous work. Anthropic publishes '
                          'the batch rows separately; OpenAI prints a Batch table and a separate Flex table '
                          'at the same numbers.\n'
                          '\n'
                          '| Batch, per million | Claude Sonnet 5.5 | Claude Opus 5.5 | GPT-6.1 Sol |\n'
                          '|---|---|---|---|\n'
                          '| Input | $1.00 | $2.00 | $1.00 |\n'
                          '| Output | $5.00 | $10.00 | $5.00 |\n'
                          '\n'
                          "Anthropic's page says its cache multipliers stack with the batch discount. For "
                          'Sonnet 5.5, apply the 0.05x hit multiplier to the applicable batch input rate '
                          'only for an actual cache hit; a batch does not guarantee reuse. The trap is that '
                          'a nightly single-run job has nothing to read from, and a cold cache write just '
                          'adds 25% to a batch you could have submitted uncached.'},
              {'title': 'Long prompts are where the sheets stop being comparable',
               'content': 'Both vendors reprice the prompt once it gets long, and they do it in different '
                          'shapes.\n'
                          '\n'
                          '| Prompt size | GPT-6.1 Sol | Claude Haiku 5.5 |\n'
                          '|---|---|---|\n'
                          '| Short context, input | $2.00 | $0.10 up to 100,000 tokens |\n'
                          '| Long context, input | $4.00 | $0.50 over 100,000 tokens |\n'
                          '| Long context, output | $15.00 | $2.50 over 100,000 tokens |\n'
                          '\n'
                          "OpenAI's long-context row doubles input and multiplies output by 1.5. Anthropic's "
                          'Haiku sheet lists two rows, one for prompts up to 100,000 tokens and one for '
                          'prompts over it, at five times the rate, and it does not print a marginal split.\n'
                          '\n'
                          'A 200,000-token prompt therefore bills at 0.2 × $0.50 = $0.10 on the over-100k '
                          'row against $0.02 if the same prompt fit under the line. That cliff, not the '
                          'per-token sticker, is what a document pipeline hits when someone pastes a whole '
                          'contract set.'},
              {'title': 'Three add-ons that quietly change the unit',
               'content': 'Fast mode on both sides doubles the sticker: Opus 5.5 goes to $8 input and $40 '
                          'output, GPT-6.1 Sol to $4 and $20. Anthropic notes that fast mode is not '
                          'available with the Batch API, so the two savings cannot be stacked.\n'
                          '\n'
                          'Data residency is a multiplier rather than a tier. Sending Claude 4.6 or later to '
                          'US-only inference applies 1.1x to every token category, cache writes and reads '
                          'included.\n'
                          '\n'
                          "For exactly two requests 12 hours apart, with no intervening reuse: Anthropic's "
                          '1-hour entry has expired: two cold writes cost 2 + 2 = 4 prefix units, not 2 + a '
                          'cache read. \n'
                          '\n'
                          'For GPT-6.1 Sol, a successful 12-hour-cache hit would cost 2.5 + 0.05 = 2.55 '
                          'across the pair; two cold writes cost 5. Both exceed two uncached passes at 2. \n'
                          '\n'
                          'This is not a long-run forecast: measure hits, writes and refreshes before '
                          'extrapolating.'}],
 'cost_math': [{'label': '100k requests, 16k cached prefix, 4k fresh input, 500 output',
                'formula': 'Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits '
                           '90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = '
                           '$800; output 100,000 × 500 = 50M × $10 = $500',
                'result': '$1,844 with the stated equal billed token counts and rates; not a measured '
                          'same-text comparison; assumes fresh input lies after the explicit cache '
                          'breakpoint and is not written'},
               {'label': 'Hypothetical sensitivity: 30% more input-category tokens, output unchanged',
                'formula': 'Input categories: ($400 writes + $144 hits + $800 fresh input) × 1.30 = '
                           '$1,747.20; unchanged output $500; total $2,247.20',
                'result': '$403.20 above the $1,844 baseline (21.87%). Assumed input change only, not an '
                          'observed Claude-versus-GPT difference.'},
               {'label': 'One write plus n-1 reads of one unchanged prefix',
                'formula': 'Sonnet 5.5 / GPT-6.1 Sol short write: 1.25 + 0.05(n-1) < n; n > 1.2632. At n=10: '
                           '1.25 + 9 × 0.05 = 1.70 versus 10. Long write at n=3: Sonnet 2 + 2 × 0.05 = 2.10; '
                           'Sol 2.5 + 2 × 0.05 = 2.60 versus 3.',
                'result': 'Short window saves 83% on the cached prefix over ten requests. Long windows break '
                          'even at three total requests, assuming two successful hits.'},
               {'label': 'Exactly two requests 12 hours apart, no intervening reuse',
                'formula': 'Sonnet 1h: two expired/cold writes, 2 + 2 = 4. Sol 12h if hit: 2.5 + 0.05 = '
                           '2.55; if miss and rewritten: 2.5 + 2.5 = 5. Uncached: 1 + 1 = 2.',
                'result': 'A 1-hour entry cannot be assumed to hit after 12 hours. Even the illustrative Sol '
                          'hit costs more than two uncached passes; not a long-run schedule forecast.'}],
 'decision_matrix': [{'situation': 'A long, stable system prompt at high volume',
                      'pick': 'Measure both on your workload',
                      'why': 'Compare measured input, cache-write, cache-hit and output usage at the '
                             'applicable rates. The Claude tokenizer note does not supply a GPT comparison '
                             'ratio.'},
                     {'situation': 'Prompts that regularly pass 100,000 tokens',
                      'pick': 'Weigh the long-context row first',
                      'why': 'OpenAI doubles input and multiplies output by 1.5 past the boundary; Haiku 5.5 '
                             'lists a rate five times higher for prompts over 100,000 tokens.'},
                     {'situation': 'Nightly batch of a few hundred thousand jobs',
                      'pick': 'Batch API on either',
                      'why': 'Both halve input and output, and a single nightly pass has no cache to read '
                             'from, so a cold write only adds 25%.'},
                     {'situation': 'Only two requests, 12 hours apart, no intervening reuse',
                      'pick': 'Compare against uncached input',
                      'why': 'Sonnet 1h writes cost 4 prefix units after expiry; Sol 12h costs 2.55 with one '
                             'hit or 5 with a rewrite, versus 2 uncached. A recurring workload needs its own '
                             'observed hit/write history.'},
                     {'situation': 'Output-heavy generation, 500+ tokens per call',
                      'pick': 'GPT-6.1 Sol over Opus 5.5',
                      'why': 'Output is 5x input on both sheets, so the $10 against $20 output rate '
                             'dominates the bill long before the input line does.'},
                     {'situation': 'Streaming that a user is watching',
                      'pick': 'Fast mode, at 2x',
                      'why': 'Opus 5.5 moves to $8 and $40 and GPT-6.1 Sol to $4 and $20, and fast mode '
                             'cannot be combined with batch.'},
                     {'situation': 'Data must stay in the US',
                      'pick': 'Price the 1.1x before comparing',
                      'why': 'US-only inference multiplies every Claude token category by 1.1, cache writes '
                             'and reads included, which changes a close comparison.'},
                     {'situation': 'A prototype with prompts under 100,000 tokens',
                      'pick': 'Claude Haiku 5.5',
                      'why': '$0.10 input and $0.50 output per million is a twentieth of the flagship rows, '
                             'and the over-100k rate only applies when the prompt crosses the line.'}],
 'verdict_summary': 'The named standard rows match: $2 input, $10 output and $0.10 cached input per million '
                    'tokens. That does not make the same task equally expensive. Measure token usage, output '
                    'quality, cache hits and retries on a representative sample. Apply the selected model, '
                    'context and service-tier rates to those measurements; do not multiply a vendor bill by '
                    'an assumed tokenizer premium.',
 'migration_guide': 'Caching controls are not interchangeable. Anthropic Messages is opt-in: top-level '
                    'cache_control selects an automatic moving breakpoint; block-level cache_control selects '
                    'explicit breakpoints. GPT-6.1 Sol supports implicit caching and explicit-only '
                    'breakpoints. Re-measure token usage on migration, rather than transferring an assumed '
                    'token ratio.\n'
                    '\n'
                    'The worked bill uses explicit boundaries around the stable prefix, leaving fresh input '
                    'outside the write. Batch jobs, files and model-specific configuration also need review '
                    'when switching providers.',
 'faqs': [{'q': 'Is prompt caching automatic on both?',
           'a': 'Anthropic Messages requires opt-in: use top-level cache_control for automatic breakpoint '
                'placement, or block-level cache_control for explicit boundaries. GPT-6.1 Sol supports '
                'implicit caching by default and explicit-only controls. Automatic placement does not '
                'guarantee a hit.'},
          {'q': 'Do the batch discount and the cache discount combine?',
           'a': 'On Anthropic the page says cache multipliers stack with the batch discount. OpenAI '
                'publishes separate Batch and Flex tables at the same rates, and fast mode is excluded from '
                'batch on Anthropic.'},
          {'q': 'Does the 30% tokenizer note mean Claude costs 30% more than GPT?',
           'a': 'No. Anthropic compares newer and earlier Claude tokenizers, not Claude with GPT. The '
                'difference depends on content. Measure each target model on the same input and account for '
                'generated output separately; this article provides no measured cross-vendor ratio.'},
          {'q': 'Is a cache write ever a loss?',
           'a': 'Yes. For Sonnet 5.5 and GPT-6.1 Sol, count one cold write plus n-1 hits across n requests, '
                'with a 0.05x hit rate. Short writes need two total requests; long writes need three. Expiry '
                'or changed prefixes add writes, not discounted reads.'}],
 'sources': ['https://platform.claude.com/docs/en/about-claude/pricing',
             'https://developers.openai.com/api/docs/pricing',
             'https://platform.claude.com/docs/en/build-with-claude/prompt-caching',
             'https://platform.claude.com/docs/en/build-with-claude/batch-processing',
             'https://claude.com/pricing',
             'https://developers.openai.com/api/docs/guides/prompt-caching'],
 'related': [{'slug': 'datadog-vs-grafana-cloud',
              'name': 'Datadog vs Grafana Cloud',
              'why': 'The same discipline on a monitoring invoice: find the meter, then print the formula.'},
             {'slug': 'aws-lambda-vs-cloudflare-workers',
              'name': 'AWS Lambda vs Cloudflare Workers',
              'why': 'When the bill depends on whether you charge for waiting or for working.'}],
 'tool_a': {'name': 'Anthropic',
            'tagline': 'Opt-in caching with automatic or explicit breakpoints',
            'db': 'Claude API: messages, prompt caching and batch in one price sheet',
            'pricing': 'Sonnet 5.5 $2 / $10 · Opus 5.5 $4 / $20 · Haiku 5.5 $0.10 / $0.50 per MTok',
            'self_host': 'No (first-party API, Bedrock and Google Cloud endpoints)',
            'realtime': 'Cache reads at 0.1x, or 0.05x on Opus 5.5 and Sonnet 5.5; writes 1.25x for 5m and '
                        '2x for 1h',
            'ai_readiness': 'Batch halves both sides; fast mode doubles; US-only inference adds 1.1x',
            'lock_in': 'Medium: model deprecations retire SKUs, and cache breakpoints are vendor-specific',
            'badge': 'Cache breakpoints',
            'cta_url': 'https://claude.com/pricing?utm_source=devteardown',
            'pros': ['Two cache windows on every model, 5 minutes and 1 hour, priced at 1.25x and 2x',
                     'Cache reads cost 0.05x on Opus 5.5 and Sonnet 5.5, cheaper than the standard 0.1x row',
                     'The batch and cache multipliers stack, which is the cheapest published path for a '
                     'stable corpus',
                     'Haiku 5.5 starts at $0.10 input for prompts under 100,000 tokens, with a documented '
                     'higher row above it'],
            'cons': ['Input counts need measurement against the target model; the newer-versus-earlier '
                     'Claude tokenizer note is not a GPT comparison',
                     'The over-100,000-token Haiku row is five times the rate and is printed as a '
                     'whole-prompt rate',
                     'Fast mode doubles the sheet and cannot be stacked with the batch discount',
                     'US-only inference applies 1.1x to cache writes and reads, not just to fresh input'],
            'code_example': '// Explicit system-prefix caching; top-level cache_control is another opt-in '
                            'option.\n'
                            'import Anthropic from "@anthropic-ai/sdk";\n'
                            'const client = new Anthropic();\n'
                            '\n'
                            'const msg = await client.messages.create({\n'
                            '  model: "claude-sonnet-5-5",\n'
                            '  max_tokens: 512,\n'
                            '  system: [{\n'
                            '    type: "text",\n'
                            '    text: SYSTEM_PROMPT,\n'
                            '    cache_control: { type: "ephemeral" }, // 1.25x write, then 0.05x reads\n'
                            '  }],\n'
                            '  messages: [{ role: "user", content: question }],\n'
                            '});\n'
                            '// Breaks when: the breakpoint sits after a timestamp or a user id. Every '
                            'request\n'
                            '// then writes a new prefix and pays 1.25x instead of reading at 0.05x.\n'
                            'console.log(msg.usage);'},
 'tool_b': {'name': 'OpenAI',
            'tagline': 'Per-token pricing with automatic prefix caching and two windows',
            'db': 'GPT API: tokens, cached input, Batch and Flex as separate rate cards',
            'pricing': 'GPT-6.1 Sol $2 / $10 · GPT-6 Astra $10 / $50 · GPT-6 Luna $0.10 / $0.50 per MTok',
            'self_host': 'No (first-party API and Azure-hosted deployments)',
            'realtime': 'Cached input at 0.05x; writes 1.25x for 30 minutes and 2.5x for 12 hours',
            'ai_readiness': 'Batch and Flex halve both sides; long context doubles input and multiplies '
                            'output by 1.5',
            'lock_in': 'Medium: batch files and assistants are per-vendor objects with no export',
            'badge': 'Automatic caching',
            'cta_url': 'https://openai.com/api/pricing/?utm_source=devteardown',
            'pros': ['Caching needs no marker: keep the prefix byte-identical and the discount applies',
                     'A 12-hour cache window exists, which suits jobs spread over a working day',
                     'Flex is priced at the batch rate, so the discount is available without the queue',
                     'Long context is priced as a multiplier on the same row, so the jump is visible before '
                     'you hit it'],
            'cons': ['The 12-hour write needs two successful reads (three total requests) to beat uncached '
                     'input at the Sol 0.05x hit rate',
                     'The long-context tier raises both input and output rates',
                     'Changing the cached prefix can require a new write; inspect actual cache usage',
                     'Fast mode uses a separate, higher rate card'],
            'code_example': '// Explicit-only mode keeps the fresh question outside the cached prefix.\n'
                            'import OpenAI from "openai";\n'
                            'const client = new OpenAI();\n'
                            'const res = await client.responses.create({\n'
                            '  model: "gpt-6.1-sol",\n'
                            '  prompt_cache_options: { mode: "explicit", ttl: "30m" },\n'
                            '  input: [\n'
                            '    { role: "developer", content: [{ type: "input_text", text: SYSTEM_PROMPT,\n'
                            '      prompt_cache_breakpoint: { mode: "explicit" } }] },\n'
                            '    { role: "user", content: question },\n'
                            '  ],\n'
                            '});\n'
                            '// Without a reusable prefix, explicit mode with no breakpoints avoids writes.\n'
                            'console.log(res.usage?.input_tokens_details);'}}
