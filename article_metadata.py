"""Editorial search summaries, not character-sliced article openings.

These describe the article's scope without promoting conditional examples as quotes.
New articles must supply a reviewed meta_description or add an explicit summary here.
"""
DESCRIPTIONS = {
    'stripe-vs-lemonsqueezy-vs-paddle': 'Compare Stripe, Lemon Squeezy and Paddle subscription fees, tax integration paths and merchant-of-record trade-offs with worked cost examples.',
    'anthropic-vs-openai-api-pricing': 'Compare Anthropic and OpenAI API pricing, token-count assumptions, caching and batch costs without assuming equal token usage or model quality.',
    'datadog-vs-grafana-cloud': 'Compare Datadog and Grafana Cloud billing units, host charges and custom metric costs using a worked monitoring workload.',
    'aws-lambda-vs-cloudflare-workers': 'Compare AWS Lambda and Cloudflare Workers request, duration and CPU billing with workload assumptions and separate storage costs.',
    'resend-vs-sendgrid': 'Compare Resend and SendGrid trial limits, paid overages and delivery operations, including retry safety and the limits of idempotency.',
    'supabase-vs-firebase': 'Compare Supabase and Firebase realtime fan-out charges, workload limits and migration trade-offs with explicitly hypothetical cost calculations.',
    'vercel-vs-cloudflare-pages': 'Compare Vercel and Cloudflare Pages billing modes, function limits and deployment trade-offs, with account-specific pricing caveats.',
    'cursor-vs-github-copilot': 'Compare Cursor and GitHub Copilot plan restrictions, metered AI usage and workflow trade-offs before choosing a coding assistant.',
    'notion-vs-obsidian': 'Compare Notion and Obsidian costs, history, permissions and migration trade-offs, including reliable Notion API pagination and retries.',
    'bun-vs-node': 'Compare Bun and Node.js runtime compatibility, native addon risks and migration costs, distinguishing vendor benchmarks from workload testing.',
    'prisma-vs-drizzle': 'Compare Prisma and Drizzle schema workflows, generated clients, database services and migration trade-offs without assuming ORM licence fees.',
    'docker-vs-podman': 'Compare Docker Desktop and Podman licensing, commercial eligibility, team limits and migration effort without assuming a universal seat price.',
    'clerk-vs-auth0': 'Compare Clerk and Auth0 pricing, active-user definitions and authentication trade-offs without treating their billed user populations as equivalent.',
    'planetscale-vs-neon': 'Compare PlanetScale and Neon Postgres compute, idle-time and storage costs using explicit uptime assumptions and migration trade-offs.',
}


def validate_description(value):
    if not isinstance(value, str) or value != value.strip() or not 60 <= len(value) <= 180:
        raise ValueError('article description must be reviewed plain text of 60–180 characters')
    if value[-1] not in '.!?' or value.endswith(('...', '…')) or any(c in value for c in '<>\n\r'):
        raise ValueError('article description must end as a complete sentence, not truncated text or markup')
    return value


def article_description(item):
    value = item.get('meta_description', DESCRIPTIONS.get(item['slug']))
    return validate_description(value)
