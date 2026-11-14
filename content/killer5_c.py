"""Transactional email comparison; corrected billing evidence."""

RESEND = {'slug': 'resend-vs-sendgrid',
 'category': 'Email Infrastructure',
 'last_verified': '2026-11-14',
 'published': '2026-11-10',
 'hook': 'Resend and SendGrid offer similar entry prices, but trial expiry and overage billing '
         'change the bill. Resend’s paid overages need opt-in and round up in 1,000-email buckets. '
         'A standard SendGrid trial ends with sending paused, not an automatic paid subscription.',
 'sections': [{'title': 'At 100,000 emails, the feature tiers cost more',
               'content': 'The listed 100,000-email tiers have a $55 feature-tier step, not an '
                          'increase in included volume. This does not make the feature bundles '
                          'equivalent or establish why either vendor set its prices.\n'
                          '\n'
                          '| At 100,000 emails | Entry tier | Feature tier | Difference |\n'
                          '|---|---|---|---|\n'
                          '| Resend | Pro $35 | Scale $90 | $55 |\n'
                          '| SendGrid | Essentials $34.95 | Pro $89.95 | $55 |\n'
                          '\n'
                          'All figures here are USD monthly estimates before taxes and add-ons. '
                          'Check your actual account quote, especially for reseller or '
                          'custom-contract plans.'},
              {'title': 'The ladder is not monotonic, and overage is sometimes the cheaper rung',
               'content': 'Resend paid transactional plans can opt into Transactional Overages in '
                          'Settings; Free cannot. Without opt-in, quota limits apply rather than '
                          'this paid continuation.\n'
                          '\n'
                          'Formula: base + ceil(max(0, usage − quota) / 1,000) × plan bucket rate. '
                          'At $20 for 50,000 and $0.90 per extra bucket:\n'
                          '\n'
                          '| Monthly usage | Rounded extra buckets | Total |\n'
                          '|---|---|---|\n'
                          '| 50,003 | 1 | $20.90 |\n'
                          '| 51,415 | 2 | $21.80 |\n'
                          '| 66,000 | 16 | $34.40 |\n'
                          '| 66,001 | 17 | $35.30 |\n'
                          '\n'
                          'The $35/100,000 tier first becomes cheaper at 66,001 emails, not '
                          '66,666. Count all usage charged to the quota, not just outbound '
                          'messages; taxes and other fees are extra.\n'
                          '\n'
                          'With opt-in, the listed $35/100,000 plan plus 100 extra buckets totals '
                          '$125 for 200,000 emails, below the $160 Scale tier but without its '
                          'features. Do not apply Resend’s rounding or activation rule to '
                          'SendGrid.'},
              {'title': 'Dedicated IP: $30 plus a $55 step, or included at $89.95',
               'content': 'A dedicated IP may matter for a sustained high-volume sender, but it '
                          'does not by itself guarantee better delivery. Choose it based on '
                          'sending patterns and operational needs.\n'
                          '\n'
                          'Resend sells it as a $30 per month add-on, and only on Scale, to '
                          'accounts sending more than 3,000 emails a day. At 100,000 emails that '
                          'is $90 + $30 = $120, or $1.20 per 1,000.\n'
                          '\n'
                          'SendGrid includes one dedicated IP in Pro, which is $89.95 at the same '
                          'volume, or $0.90 per 1,000.\n'
                          '\n'
                          '| 100,000 emails with a dedicated IP | Monthly | Per 1,000 |\n'
                          '|---|---|---|\n'
                          '| Resend Scale + IP add-on | $120.00 | $1.20 |\n'
                          '| SendGrid Pro | $89.95 | $0.90 |\n'
                          '\n'
                          'There is no Resend Pro path to an IP in the listed self-service tiers. '
                          'That is not a worse deal; it is a missing SKU, and it decides the '
                          'vendor for anyone whose deliverability depends on one.'},
              {'title': 'Domain authentication is table stakes; the domain count is not',
               'content': 'Both authenticate sending with DKIM, SPF and DMARC, and both include a '
                          'REST API, SMTP relay and official SDKs on every paid plan. The '
                          'differences are in the quantities.\n'
                          '\n'
                          '| Quantity | Resend | SendGrid |\n'
                          '|---|---|---|\n'
                          '| Custom domains | 3 Free, 10 Pro, 1,000 Scale | Domain authentication '
                          'included |\n'
                          '| Extra domains | $20/mo adds 100 | Not a listed line item |\n'
                          '| Teammates | Not metered | 1 on Essentials, 1,000 on Pro |\n'
                          '| Event webhooks | 5 on Pro, 10 on Scale | 2 on Essentials, 5 on Pro |\n'
                          '| SSO | $150/mo add-on on Scale | Included in Pro |\n'
                          '\n'
                          'Resend retains idempotency keys for 24 hours only. Same-key retries '
                          'require the identical payload. A 409 payload conflict needs correction; '
                          'a concurrent request needs bounded backoff. Keep durable send state and '
                          'reconcile ambiguous outcomes after long outages, not blind resends.'},
              {'title': 'A trial ending is not an automatic subscription',
               'content': 'Correction, November 14, 2026: the earlier article wrongly described '
                          'automatic SendGrid paid conversion and continuous per-email Resend '
                          'overage billing. The calculations and FAQ are corrected.\n'
                          '\n'
                          'A standard new direct SendGrid/Twilio Email API account gets a 60-day '
                          'trial at 100 emails/day. After expiry, sending stops unless you choose '
                          'a paid upgrade; the trial does not itself trigger a $19.95 charge. '
                          'Email API and Marketing Campaigns are separate plans.\n'
                          '\n'
                          'Partner/reseller accounts such as Azure can differ: check actual terms '
                          'and notices. Older direct free accounts are not a guaranteed exemption; '
                          'Twilio announced their retirement in May 2025 with a transition to '
                          'paused sending absent upgrade. Already-paid subscriptions follow their '
                          'own terms.\n'
                          '\n'
                          'Resend’s free tier allows 3,000 emails/month and 100/day. $19.95 × 12 = '
                          '$239.40 represents twelve voluntarily purchased SendGrid months, not a '
                          'trial-expiry bill or a first year including the trial.'},
              {'title': 'Where each one breaks',
               'content': 'Resend breaks on the feature boundary. The dedicated IP, SSO and 1,000 '
                          'domains all sit on Scale, so the 100,000-email customer who outgrows '
                          'Pro pays a $55 step and then $30 more for the IP. Marketing email moves '
                          'to a separate contact-priced plan, and broadcasts only reach existing '
                          'contacts.\n'
                          '\n'
                          'SendGrid breaks on the tier edge and on history. The 50,000 Essentials '
                          'tier charges $1.33 per 1,000 beyond its volume, so 80,000 emails bills '
                          '$19.95 + $39.90 = $59.85 against $34.95 for the next tier up. '
                          'Searchable activity is 3 days on Essentials against 7 on Pro, so a '
                          'deliverability investigation can outlast the evidence.\n'
                          '\n'
                          'Check three numbers before choosing: your monthly volume rounded up to '
                          'the rung that covers it, whether you need an IP this quarter, and how '
                          'many domains you will authenticate in a year.'}],
 'cost_math': [{'label': '100,000 emails a month, no dedicated IP',
                'formula': 'Resend Pro $35 ÷ 100,000 emails × 1,000 = $0.35 per 1,000. SendGrid '
                           'Essentials $34.95 ÷ 100,000 × 1,000 = $0.35 per 1,000',
                'result': '$35.00 against $34.95, a five-cent gap at the bottom of the ladder'},
               {'label': '200,000 emails a month, the rung against the overage',
                'formula': 'Eligible Resend paid plan with Transactional Overages enabled: $35 + '
                           'ceil(100,000/1,000) × $0.90 = $125. SendGrid published Pro scenario: '
                           '$89.95 + 100,000 × $1.10/1,000 = $199.95; confirm the account-specific '
                           'overage schedule.',
                'result': 'Conditional estimates before taxes/add-ons, not automatic access to '
                          'unlimited sending.'},
               {'label': 'Resend 50,000 tier: first cheaper upgrade point',
                'formula': '$20 + ceil(max(0, volume − 50,000)/1,000) × $0.90. At 66,000: $34.40. '
                           'At 66,001: $35.30, compared with $35 for 100,000.',
                'result': 'Upgrade first costs less at 66,001 quota-counted emails, with overages '
                          'enabled; no exact equality. Do not apply this rounding to SendGrid.'},
               {'label': 'The same feature at the same volume',
                'formula': 'Resend: Scale $90 + dedicated IP $30 = $120. SendGrid: Pro $89.95 '
                           'including one dedicated IP',
                'result': '$120 against $89.95 for 100,000 emails with a dedicated IP, a $30.05 '
                          'monthly difference'}],
 'decision_matrix': [{'situation': 'Transactional email only, under 50,000 a month',
                      'pick': 'Either',
                      'why': '$20 on Resend and $19.95 on SendGrid buy the same volume, and the '
                             'five-cent gap is not a reason to migrate.'},
                     {'situation': 'You need a dedicated IP at 100,000 emails',
                      'pick': 'SendGrid Pro',
                      'why': '$89.95 includes one IP, against $90 for Resend Scale plus $30 for '
                             'the add-on, and Resend Pro cannot buy an IP at all.'},
                     {'situation': 'A free tier is mandatory for staging',
                      'pick': 'Resend',
                      'why': 'Resend offers ongoing free usage within both limits. Standard direct '
                             'SendGrid trials expire after 60 days; sending requires an explicit '
                             'paid upgrade, not automatic billing.'},
                     {'situation': 'Agencies authenticating dozens of client domains',
                      'pick': 'Resend Scale, with the domain add-on',
                      'why': '1,000 domains are included on Scale and $20 adds 100 more, against a '
                             'domain line SendGrid does not print.'},
                     {'situation': 'SSO and an IP at 500,000 emails',
                      'pick': 'SendGrid Pro',
                      'why': 'SSO is included in Pro and so is one IP, while Resend puts SSO at '
                             '$150 a month and the IP at $30 on top of Scale.'},
                     {'situation': '2,500,000 emails a month and nothing exotic',
                      'pick': 'SendGrid Pro',
                      'why': '$1,099 against $1,150 on Resend, and the gap widens with the IP '
                             'add-on that Resend needs for the same setup.'},
                     {'situation': 'Marketing broadcasts to a contact list',
                      'pick': 'Resend marketing plans',
                      'why': 'Marketing is priced per contact rather than per email, so an '
                             'unlimited number of sends to 10,000 contacts is $80.'},
                     {'situation': 'Volume swings month to month',
                      'pick': 'Either, with an alert at 60,000',
                      'why': 'For Resend, enable eligible paid-plan overages before relying on '
                             'them and compare rounded buckets: the $35 tier wins from 66,001 '
                             'emails. SendGrid has its own account-specific rates and limits; '
                             'check those separately.'}],
 'verdict_summary': 'For a small service within 3,000 emails a month and 100 a day, Resend offers '
                    'an ongoing free option. A standard new direct SendGrid account has a 60-day '
                    'trial, not automatic paid conversion: sending stops unless you upgrade. '
                    'Paid-plan selection needs both volume and features. Resend overages require '
                    'opt-in and round up in 1,000-email buckets; do not budget them as a per-email '
                    'charge.',
 'migration_guide': 'Both vendors authenticate a domain with DKIM, SPF and DMARC records, so '
                    'moving means adding new DNS records while the old ones still answer. Keep '
                    'both authenticated for a week, warm the new domain or IP, then flip the '
                    'sending domain in code.\n'
                    '\n'
                    'The parts that do not travel are templates and reputation. React Email '
                    "templates are code and move with the repository; SendGrid's dynamic templates "
                    'are vendor objects. A dedicated IP starts cold on either side, so a sender '
                    'who relies on one should plan the warm-up as a week of projected volume '
                    'rather than a switch.',
 'faqs': [{'q': 'Does Resend sell a dedicated IP on Pro?',
           'a': 'No. The $30 per month add-on is listed for Scale plans, to accounts sending more '
                'than 3,000 emails a day. Pro has no IP option.'},
          {'q': 'Does SendGrid automatically charge after the free trial?',
           'a': 'No automatic paid conversion is described for the standard new direct-account '
                'trial. After 60 days, sending stops unless you choose a paid upgrade. '
                'Partner/reseller and already-paid accounts can have different terms; check the '
                'actual plan and notices. Older direct free plans were subject to the 2025 '
                'retirement transition.'},
          {'q': 'How do Resend overages work?',
           'a': 'On an eligible paid transactional plan, enable Transactional Overages in '
                'Settings. Additional usage rounds up in 1,000-email buckets at the plan rate. At '
                '$20 for 50,000 and $0.90 per bucket, 51,415 emails cost $21.80; 66,001 cost '
                '$35.30, above the $35/100,000 tier. Free plans are not eligible. Taxes and other '
                'fees are extra. This rounding rule does not establish SendGrid billing behavior.'},
          {'q': 'Do both include inbound email parsing?',
           'a': 'Resend lists inbound email with webhooks on every plan, and SendGrid lists an '
                'Inbound Parse webhook as part of the Email API feature set.'}],
 'sources': ['https://resend.com/pricing',
             'https://www.twilio.com/en-us/products/email-api/pricing',
             'https://aws.amazon.com/marketplace/pp/prodview-dp5xcsvbvixai',
             'https://resend.com/docs',
             'https://www.twilio.com/docs/sendgrid',
             'https://resend.com/changelog/pay-as-you-go-pricing',
             'https://www.twilio.com/docs/sendgrid/ui/account-and-settings/upgrading-your-plan',
             'https://help.twilio.com/articles/47846436523419',
             'https://www.twilio.com/en-us/changelog/changes-coming-to-sendgrid-s-free-plans',
             'https://resend.com/docs/dashboard/emails/idempotency-keys',
             'https://resend.com/docs/api-reference/errors'],
 'related': [{'slug': 'stripe-vs-lemonsqueezy-vs-paddle',
              'name': 'Stripe vs Lemon Squeezy / Paddle',
              'why': 'The same $55-style feature step, one decimal place larger.'},
             {'slug': 'datadog-vs-grafana-cloud',
              'name': 'Datadog vs Grafana Cloud',
              'why': 'What happens when a vendor meters the thing your code does by accident.'}],
 'tool_a': {'name': 'Resend',
            'tagline': 'Per-block email pricing with a free tier and a Scale step',
            'db': 'Transactional email API with React Email templates and inbound parsing',
            'pricing': 'Free 3,000/mo · Pro $20 for 50k, $35 for 100k · Scale $90 for 100k to '
                       '$1,150 for 2.5M',
            'self_host': 'No (managed sending infrastructure and shared IPs)',
            'realtime': 'Batch sending and webhooks on every plan; 5 endpoints on Pro, 10 on Scale',
            'ai_readiness': '100 AI credits a month on Pro, 500 on Scale; 10,000 automation runs '
                            'included',
            'lock_in': 'Low: SMTP and REST, and domain reputation travels with your DNS',
            'badge': 'Free tier',
            'cta_url': 'https://resend.com/?utm_source=devteardown',
            'pros': ['A free plan that sends 3,000 emails a month, so staging and side projects '
                     'cost nothing',
                     'Monthly billing only, with no annual contract to sign before the first send',
                     '10 domains on Pro and 1,000 on Scale, with 100 more for $20 a month',
                     'React Email templates are code, so they live in the repository rather than a '
                     'dashboard'],
            'cons': ['The dedicated IP is a $30 add-on on Scale only, so Pro customers cannot buy '
                     'one at any price',
                     'SSO is $150 a month on Scale and unavailable below it',
                     'Scale at 100,000 emails is $90 against $35 on Pro, a $55 step for features '
                     'rather than volume',
                     "The 200,000 rung costs $0.80 per 1,000, more than twice the 100,000 rung's "
                     'rate'],
            'code_example': '// One attempt, not an outbox implementation. Never call directly '
                            'from a browser.\n'
                            '// Caller must atomically claim a durable outbox row BEFORE the first '
                            'send and\n'
                            '// persist its immutable payload, key, firstAttemptAt and attempt '
                            'outcomes.\n'
                            '// Use one event/version key, not Date.now(); retries must reuse the '
                            'exact payload.\n'
                            '// Resend retains keys for 24 hours, not forever. Acceptance is not '
                            'delivery.\n'
                            'export async function attemptEmail(resend, row, now = Date.now()) {\n'
                            '  if (row.acceptedId) return { acceptedId: row.acceptedId, '
                            'alreadyRecorded: true };\n'
                            '  const age = now - row.firstAttemptAt;\n'
                            '  // Stop 5 minutes early to allow for clock skew / requests in '
                            'flight.\n'
                            '  if (!Number.isFinite(age) || age < 0 || age >= 23 * 3600000 + 55 * '
                            '60000) {\n'
                            "    throw new Error('reconcile_required: do not blindly resend after "
                            "the 24-hour window');\n"
                            '  }\n'
                            '  if (!row.key || row.key.length > 256 || !row.payload) throw new '
                            "Error('invalid_outbox_row');\n"
                            '  let response;\n'
                            '  try {\n'
                            '    response = await resend.emails.send(row.payload, { '
                            'idempotencyKey: row.key });\n'
                            '  } catch {\n'
                            "    throw new Error('unknown_outcome: reconcile; bounded same-key "
                            "retry only within the window');\n"
                            '  }\n'
                            '  const { data, error } = response;\n'
                            '  if (error) {\n'
                            "    if (error.name === 'invalid_idempotent_request') {\n"
                            "      throw new Error('payload_conflict: stop; do not mint a new key "
                            "to bypass this 409');\n"
                            '    }\n'
                            "    if (error.name === 'concurrent_idempotent_requests') {\n"
                            "      throw new Error('in_progress: defer with bounded backoff and "
                            "recheck the window');\n"
                            '    }\n'
                            '    throw new Error(`send_failed: ${error.name}; inspect before any '
                            'retry`);\n'
                            '  }\n'
                            "  if (!data?.id) throw new Error('unknown_outcome: missing acceptance "
                            "id; reconcile');\n"
                            '  return { acceptedId: data.id }; // Caller must durably save this '
                            'before acking its job.\n'
                            '}\n'
                            '// On long outages, check durable state plus provider logs/webhooks '
                            'before deciding\n'
                            '// whether to resend. A crash after acceptance but before saving the '
                            'id is ambiguous.\n'
                            '// If reconciliation cannot resolve it, hold for review; this is not '
                            'exactly-once delivery.'},
 'tool_b': {'name': 'SendGrid',
            'tagline': 'Per-block pricing where Pro includes the dedicated IP',
            'db': 'Email API with dynamic templates, subusers and dedicated IPs',
            'pricing': '60-day trial · Essentials $19.95 for 50k, $34.95 for 100k · Pro $89.95 for '
                       '100k to $1,099 for 2.5M',
            'self_host': 'No (Twilio-managed sending infrastructure)',
            'realtime': 'Event webhook on every plan: 1 endpoint on trial, 2 on Essentials, 5 on '
                        'Pro',
            'ai_readiness': 'Address validation included with Pro: 2,500 checks, 5,000 on Premier',
            'lock_in': 'Medium: templates, subusers and IP warm-up history live in the product',
            'badge': 'IP included',
            'cta_url': 'https://www.twilio.com/en-us/products/email-api/pricing?utm_source=devteardown',
            'pros': ['One dedicated IP is included in Pro, which is the cheapest published way to '
                     'get one at 100,000 emails',
                     'SSO and 1,000 teammates arrive with Pro rather than as add-ons',
                     'Subuser management makes it a fit for agencies and multi-brand senders',
                     'The ladder keeps falling to $0.44 per 1,000 at 2,500,000, undercutting '
                     'Resend at the top'],
            'cons': ['Standard direct-signup trial: sending stops after 60 days unless you '
                     'explicitly upgrade; partner or existing paid accounts can differ',
                     'The 50,000 tier charges $1.33 per 1,000 beyond its volume, so 80,000 emails '
                     'bills $59.85 against $34.95 for the next tier',
                     'Essentials keeps 3 days of searchable activity against 7 on Pro, which can '
                     'outlast a deliverability investigation',
                     'Email validation and content testing are gated to Pro and above'],
            'code_example': '// SendGrid: categories are the only cheap way to separate streams in '
                            'the event webhook.\n'
                            'import sgMail from "@sendgrid/mail";\n'
                            'sgMail.setApiKey(process.env.SENDGRID_API_KEY);\n'
                            '\n'
                            'await sgMail.send({\n'
                            '  to: order.email,\n'
                            '  from: "billing@example.com",\n'
                            '  templateId: "d-receipt-v3",\n'
                            '  dynamicTemplateData: { orderId: order.id, total: order.total },\n'
                            '  categories: ["receipt", `region-${order.region}`],\n'
                            '  customArgs: { order_id: order.id }, // echoed in the event webhook\n'
                            '});\n'
                            '// Breaks when: the template renders a total without a currency. The '
                            'API accepts it,\n'
                            '// the receipt is wrong, and the event webhook reports a delivered '
                            'message.'}}
