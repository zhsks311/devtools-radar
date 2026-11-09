#!/usr/bin/env python3
"""Merge reviewed article content + refreshed 2026 product metadata into data/tools.json."""

import json
import os

BASE = "/workspace/devtools-radar"
VERIFIED = "2026-11-10"

META = {
    "supabase-vs-firebase": {
        "category": "Backend & Database",
        "tool_a": {
            "name": "Supabase",
            "tagline": "Postgres with the batteries, priced as a machine",
            "db": "PostgreSQL (relational + pgvector)",
            "pricing": "Free: 500 MB, 2 projects · Pro $25 + $10/project compute",
            "self_host": "Yes (Docker stack)",
            "realtime": "Postgres Changes (CDC, row-level-security aware)",
            "ai_readiness": "pgvector in the same database as your app data",
            "lock_in": "Low: standard Postgres, dump and leave",
            "badge": "Open source",
            "cta_url": "https://supabase.com/?utm_source=devtoolsradar",
            "pros": [
                "One invoice for compute, disk and connections — reads inside the instance are not metered",
                "pgvector lives in the same Postgres as your rows, so RAG needs no second system",
                "Standard Postgres: SQL, JOINs, transactions, triggers, and pg_dump as an exit door",
                "The connection ceiling is purchasable: 200 pooled connections on $10 Micro up to 12,000 on $3,730",
            ],
            "cons": [
                "You buy headroom, not usage: peak connections decide the tier, and idle capacity still bills",
                "Every extra project adds its own compute line ($10 for a Micro) even on one Pro plan",
                "Free projects are paused after a week of inactivity, which kills demo and staging projects",
                "Realtime subscriber capacity is not on the price sheet; you size by connection and compute limits",
            ],
            "code_example": (
                "// Relational read in one round trip. Free-tier note:\n"
                "// the nested select is a JOIN, so 50 comments cost 0 extra reads.\n"
                "const { data, error } = await supabase\n"
                "  .from('posts')\n"
                "  .select('id, title, comments(id, body, user_id)')\n"
                "  .eq('published', true)\n"
                "  .order('created_at', { ascending: false })\n"
                "  .limit(20);\n"
                "// Here it breaks: anon key + missing RLS policy = empty array, not an error.\n"
                "if (error) throw error;"
            ),
        },
        "tool_b": {
            "name": "Firebase",
            "tagline": "Firestore: offline-first sync, metered per event",
            "db": "Firestore (NoSQL document store)",
            "pricing": "Daily free quota · reads $0.03 / writes $0.09 per 100k",
            "self_host": "No (proprietary GCP)",
            "realtime": "Snapshot listeners — a read per changed document",
            "ai_readiness": "kNN vector search, billed per 100-entry index batch",
            "lock_in": "High: rules, SDKs, and no SQL export path",
            "badge": "Managed Google",
            "cta_url": "https://firebase.google.com/?utm_source=devtoolsradar",
            "pros": [
                "Offline persistence and multi-platform SDKs that work when the network does not",
                "No connection pool to size: events are metered, not sockets",
                "A daily free quota of 50,000 reads and 20,000 writes per project",
                "Listeners bill only for documents that change in the result set, not for every poll",
            ],
            "cons": [
                "A dashboard left open all day is a recurring read charge: 50 users can pass $1,296/month",
                "Reconnects are billed like brand-new queries — with persistence off, every one of them",
                "Index entry reads are a second meter: a second range field starts billing",
                "No JOIN, and the export tool flattens one collection to one table, so schema design lands on you",
            ],
            "code_example": (
                "// N+1 by design: comments are a second query per post.\n"
                "const q = query(collection(db, 'posts'), where('published', '==', true));\n"
                "const snap = await getDocs(q);           // 20 reads\n"
                "for (const doc of snap.docs) {\n"
                "  // Denormalise, or pay: 20 more queries = 20 more billed reads\n"
                "  const comments = await getDocs(collection(doc.ref, 'comments'));\n"
                "}\n"
                "// Here it breaks: a live listener on this collection bills a read on\n"
                "// every document update, for every listener, for as long as the tab is open."
            ),
        },
        "migration_guide": (
            "`supabase-community/firebase-to-supabase` is community tooling, not an official CLI. "
            "`firestore2json.js` exports one collection, `json2supabase.js` loads it into one table, and fields "
            "are flattened to text, numeric, boolean or jsonb — splitting nested JSON into related tables is a "
            "hook you write. Auth is the harder half: `firestoreusers2json` and `import_users` carry passwords "
            "over as SCRYPT hash parameters, and verifying a user's existing Firebase password on first login "
            "needs middleware the repo still marks work in progress. Budget the schema work, not the script."
        ),
        "related": [],
    },

    "vercel-vs-cloudflare-pages": {
        "category": "Hosting & Edge",
        "tool_a": {
            "name": "Vercel",
            "tagline": "The framework vendor that runs your framework",
            "db": "Serverless functions on Fluid compute",
            "pricing": "Hobby $0 · Pro $20/seat: 1 TB transfer, 10M requests",
            "self_host": "No (Vercel infrastructure)",
            "realtime": "Streaming responses and ISR revalidation",
            "ai_readiness": "Fluid compute targets inference and agent workloads",
            "lock_in": "Medium: framework and platform coupling",
            "badge": "Framework-native",
            "cta_url": "https://vercel.com/?utm_source=devtoolsradar",
            "pros": [
                "Your framework deploys as written; no runtime port to a different JS environment",
                "Fluid compute bills execution time, so an idle await on an external API costs no CPU",
                "In-function concurrency shares one instance across concurrent requests",
                "Per-project previews and ISR in the same product as the build pipeline",
            ],
            "cons": [
                "Transfer is metered: 2 TB over the Pro allowance is 2,048 GB × $0.15 = $307.20",
                "CDN requests bill past 10M/month at $2 per million — fan-out is expensive",
                "Price is per seat, so a growing team raises the floor before traffic does",
                "Active CPU is a separate metered line on top of the seat price",
            ],
            "code_example": (
                "// Vercel: the framework's own handler, deployed unchanged.\n"
                "export const maxDuration = 60; // seconds; the platform caps it\n"
                "export async function POST(req: Request) {\n"
                "  const { prompt } = await req.json();\n"
                "  // Active CPU bills while this code runs, not while it waits:\n"
                "  const upstream = await fetch('https://api.example.com/v1/chat', {\n"
                "    method: 'POST',\n"
                "    body: JSON.stringify({ prompt }),\n"
                "    headers: { 'content-type': 'application/json' },\n"
                "  });\n"
                "  // Here it breaks: default duration limits kill long streams. Set maxDuration\n"
                "  // and check the platform ceiling before shipping a 5-minute job.\n"
                "  return new Response(upstream.body, { headers: { 'content-type': 'text/event-stream' } });\n"
                "}"
            ),
        },
        "tool_b": {
            "name": "Cloudflare Pages",
            "tagline": "The network vendor that runs your requests",
            "db": "Workers runtime + Pages static assets",
            "pricing": "Pages free · Workers Paid from $5/account, $0 egress",
            "self_host": "No (Cloudflare network)",
            "realtime": "WebSocket upgrade bills one request; messages bill nothing",
            "ai_readiness": "CPU-metered runtime; 30M CPU-ms included per month",
            "lock_in": "Medium-high: Workers runtime, per-product line items",
            "badge": "Zero egress",
            "cta_url": "https://pages.cloudflare.com/?utm_source=devtoolsradar",
            "pros": [
                "Egress is free by policy: 3 TB a month costs $0 where Vercel adds $307.20",
                "Requests after 10M cost $0.30/million, against $2/million on Vercel Pro",
                "Static asset requests are free and unlimited; cache hits cost a request but no CPU",
                "WebSocket messages are not billed as requests — only the upgrade is",
            ],
            "cons": [
                "Your handlers run on the Workers runtime, so the port is real work, not a config change",
                "Hard ceilings that stop a deployment instead of billing you: 25 MiB per asset, 20-minute builds",
                "Pages Free allows 500 builds a month and 20,000 files per site",
                "CPU time is capped per invocation: 30 seconds default, 5 minutes maximum",
            ],
            "code_example": (
                "// Cloudflare: the Worker handler, not the framework's.\n"
                "export default {\n"
                "  async fetch(request, env, ctx) {\n"
                "    const { prompt } = await request.json();\n"
                "    // CPU-ms bills only while this isolate executes.\n"
                "    const upstream = await fetch('https://api.example.com/v1/chat', {\n"
                "      method: 'POST',\n"
                "      body: JSON.stringify({ prompt }),\n"
                "      headers: { 'content-type': 'application/json' },\n"
                "    });\n"
                "    // Here it breaks: no Node APIs by default. Anything importing fs, net or\n"
                "    // a native addon needs nodejs_compat, and some libraries never port.\n"
                "    return new Response(upstream.body, { headers: { 'content-type': 'text/event-stream' } });\n"
                "  },\n"
                "};"
            ),
        },
        "migration_guide": (
            "Moving from Vercel to Pages means rewriting handlers for the Workers runtime, not flipping a "
            "setting: no Node defaults, and anything importing fs or net needs the compatibility flag. Move "
            "the static build first (it costs nothing to serve), measure the handlers' CPU per request against "
            "the 30-second default and 5-minute cap, then check your largest asset against 25 MiB and your "
            "build against the 20-minute timeout. Going the other way, port back to Node and expect the "
            "transfer line to reappear the first month traffic passes 1 TB."
        ),
        "related": [],
    },

    "cursor-vs-github-copilot": {
        "category": "AI Coding",
        "tool_a": {
            "name": "Cursor",
            "tagline": "The editor that owns the model — now a SpaceX subsidiary",
            "db": "Full-repo index + agent (Composer, Grok 4.6)",
            "pricing": "Plus $8 (Grok only) · Premium $30 + third-party tokens",
            "self_host": "No (SpaceXAI-hosted models)",
            "realtime": "Cloud agents and automations from Premium",
            "ai_readiness": "Own models trained on SpaceX compute",
            "lock_in": "High: Grok-first routing after the acquisition",
            "badge": "Grok-native",
            "cta_url": "https://cursor.com/?utm_source=devtoolsradar",
            "pros": [
                "Owns its models, so it optimises the whole loop rather than renting someone's API",
                "One editor, one bill for indexing, completion, agent and cloud automation",
                "Premium bundles cloud agents, code hosting via Origin and review via Bugbot",
                "$8 Plus is the cheapest agentic editor entry point if Grok is enough for you",
            ],
            "cons": [
                "Every third-party model token bills at API list price on top of the subscription",
                "Plus ($8) cannot run Claude or GPT at all",
                "Model neutrality ended with the $60B acquisition; Grok is the default",
                "Published benchmark numbers are the vendor's own (69.9–70.8% CursorBench)",
            ],
            "code_example": (
                "// Cursor's agent works on the open repository, so the unit of work\n"
                "// is a task, not a suggestion. The bill follows the model you route to.\n"
                "// .cursor/rules/backend.mdc — project rules apply to every agent run\n"
                "---\n"
                "description: Backend conventions\n"
                "globs: services/**/*.py\n"
                "---\n"
                "Never edit migrations by hand; generate them and review the diff.\n"
                "// Here it breaks: on Premium, requests routed to Claude or GPT are billed\n"
                "// at API list price separately from the $30 subscription — watch the invoice,\n"
                "// not just the seat count."
            ),
        },
        "tool_b": {
            "name": "GitHub Copilot",
            "tagline": "The repository vendor that puts AI where review happens",
            "db": "Repository context + GitHub PR surface",
            "pricing": "Free · Pro $10 ($15 credits) · Pro+ $39 ($70 credits)",
            "self_host": "No (GitHub-hosted)",
            "realtime": "Copilot in the cloud: assign work, get a PR (Pro+)",
            "ai_readiness": "Premium models incl. Opus on Pro+",
            "lock_in": "Medium: one credit pool inside GitHub",
            "badge": "Repo-native",
            "cta_url": "https://github.com/features/copilot?utm_source=devtoolsradar",
            "pros": [
                "Runs in VS Code, Visual Studio, JetBrains, Xcode, Eclipse, Neovim, Zed and on github.com",
                "Free already includes agent mode and the CLI — the entry tier is usable, not a demo",
                "One credit meter covers agent, review, cloud and CLI, so spend is predictable per seat",
                "Review lands where the team already reviews: PRs, file diffs, assigned work",
            ],
            "cons": [
                "PR review, file diff review, custom instructions and cloud assignment all start at $10 Pro",
                "Pro's $15 of credits is a budget, not an allowance you can ignore",
                "Agent quality tracks whatever model GitHub routes you to; Opus is Pro+",
                "You are buying into GitHub's surface — fine in GitHub, awkward outside it",
            ],
            "code_example": (
                "// Copilot's advantage is the review surface, not the cursor.\n"
                "// .github/instructions/backend.instructions.md — applied to agent work\n"
                "---\n"
                "applyTo: \"**/*.py\"\n"
                "---\n"
                "- Generate migrations, never hand-edit them.\n"
                "- Every new endpoint needs an integration test.\n"
                "// Then assign an issue to Copilot: it opens a PR you review like any other.\n"
                "// Here it breaks: on Free, PR review, diff review and custom instructions\n"
                "// are unavailable — the agent runs, the review handoff does not."
            ),
        },
        "migration_guide": (
            "Switching editors is cheap; switching billing models is not. From Cursor to Copilot: export your "
            "rules to `.github/instructions/*.instructions.md`, check that the workflows you rely on (PR review, "
            "assigned work, cloud) sit at Pro or above, and price the Claude/GPT usage you actually run against "
            "Pro+ ($39 with $70 of credits). From Copilot to Cursor: budget Premium ($30) plus the list-price "
            "third-party tokens, because nothing in the subscription covers them — and confirm that Grok is "
            "acceptable for the default path before you renew a team licence."
        ),
        "related": [],
    },

    "notion-vs-obsidian": {
        "category": "Knowledge & Notes",
        "tool_a": {
            "name": "Notion",
            "tagline": "A server with a meter: shared state, permissions, agents",
            "db": "Relational databases, formulas, rollups (server-side)",
            "pricing": "Free · Plus $10 · Business $20 per member",
            "self_host": "No (Notion cloud)",
            "realtime": "Multiplayer editing and live cursors",
            "ai_readiness": "Notion Agent in Business; Custom Agents metered",
            "lock_in": "Medium-high: export is a conversion, history is a plan tier",
            "badge": "Team workspace",
            "cta_url": "https://www.notion.com/?utm_source=devtoolsradar",
            "pros": [
                "Permissions, private teamspaces and SSO in the same place as the content",
                "Databases with relations, rollups and formulas computed server-side",
                "Notion Agent and AI Meeting Notes included from Business",
                "Multiplayer editing with no sync service to run yourself",
            ],
            "cons": [
                "Page history is a plan feature: 7 days Free, 30 Plus, 90 Business",
                "The API is metered: 180 requests/minute per connection, 600 only on Business and up",
                "Free caps uploads at 5 MB and guests at 10",
                "Custom Agents bill per 1,000 Notion credits on top of the seat price",
            ],
            "code_example": (
                "// The API budget is the real constraint: 180 req/min per connection\n"
                "// (600 on Business+), plus a shared per-workspace budget.\n"
                "async function queryAll(dbId, cursor) {\n"
                "  const res = await fetch(`https://api.notion.com/v1/databases/${dbId}/query`, {\n"
                "    method: 'POST',\n"
                "    headers: { Authorization: `Bearer ${process.env.NOTION_TOKEN}`,\n"
                "               'Notion-Version': '2022-06-28', 'content-type': 'application/json' },\n"
                "    body: JSON.stringify({ start_cursor: cursor, page_size: 100 }),\n"
                "  });\n"
                "  // Here it breaks: bursts are allowed, sustained rate is not.\n"
                "  if (res.status === 429 || res.status === 529) {\n"
                "    const wait = Number(res.headers.get('Retry-After') || 60);\n"
                "    await new Promise(r => setTimeout(r, wait * 1000));\n"
                "  }\n"
                "  return res.json();\n"
                "}"
            ),
        },
        "tool_b": {
            "name": "Obsidian",
            "tagline": "A folder with a pipe: local files, no meter",
            "db": "Local Markdown + frontmatter; Bases views as a core plugin",
            "pricing": "Free · Sync $4/user · Publish $8/site",
            "self_host": "Yes — it is your disk",
            "realtime": "No built-in co-editing; shared vaults via Sync",
            "ai_readiness": "No server-side agent; bring your own script or plugin",
            "lock_in": "None: plain files, git history you own",
            "badge": "Local-first",
            "cta_url": "https://obsidian.md/?utm_source=devtoolsradar",
            "pros": [
                "Free without limits, no sign-up, no telemetry, data on your own disk",
                "Bases is a core plugin: table, cards, list, kanban and map views over frontmatter",
                "History is git history — no plan-imposed cutoff on how far back you can go",
                "Sync costs $4/user/month with AES-256 end-to-end encryption, and is optional",
            ],
            "cons": [
                "No permission model and no built-in multi-user editing",
                "No server-side agent, no computed properties on a server, no API",
                "Collaboration arrives only through Sync shared vaults or third-party tooling",
                "You own the backups, the indexing and the failure modes of your own machine",
            ],
            "code_example": (
                "# A .base file is a saved query. It holds the view, not the data:\n"
                "# delete it and your notes are untouched.\n"
                "filters:\n"
                "  and:\n"
                "    - file.inFolder(\"Projects\")\n"
                "    - file.hasTag(\"active\")\n"
                "formulas:\n"
                "  ratio: '(price / age).toFixed(2)'\n"
                "views:\n"
                "  - type: table\n"
                "    order:\n"
                "      - file.name\n"
                "      - formula.ratio\n"
                "# Here it breaks: there is no permission layer. Anyone who has the vault\n"
                "# sees every note, including the ones you would have restricted in Notion."
            ),
        },
        "migration_guide": (
            "Notion to Obsidian is a conversion, not a move: export to Markdown and CSV, then rebuild what "
            "the export cannot carry — relations become links or frontmatter, rollups become formulas, and "
            "permissions disappear entirely. Obsidian to Notion is worse in the other direction: plain files "
            "become blocks, the API becomes a 180-request-per-minute budget, and your git history stops being "
            "your history. Decide by which of those two losses you can actually live with."
        ),
        "related": [],
    },
}

RELATED = {
    "supabase-vs-firebase": [
        {"slug": "vercel-vs-cloudflare-pages", "name": "Vercel vs Cloudflare Pages",
         "why": "The same penalty-table reading, applied to hosting: which line your workload inflates."},
        {"slug": "notion-vs-obsidian", "name": "Notion vs Obsidian",
         "why": "Another free tier that is really a history and API budget."},
    ],
    "vercel-vs-cloudflare-pages": [
        {"slug": "supabase-vs-firebase", "name": "Supabase vs Firebase",
         "why": "Metered reads versus metered compute, with the arithmetic shown."},
        {"slug": "cursor-vs-github-copilot", "name": "Cursor vs GitHub Copilot",
         "why": "When a vendor moves the meter to credits, the entry tier is where the cost hides."},
    ],
    "cursor-vs-github-copilot": [
        {"slug": "vercel-vs-cloudflare-pages", "name": "Vercel vs Cloudflare Pages",
         "why": "Both articles start from the same question: what does this vendor count?"},
        {"slug": "notion-vs-obsidian", "name": "Notion vs Obsidian",
         "why": "Agents are now sold as credits — here is the same pattern in a notes app."},
    ],
    "notion-vs-obsidian": [
        {"slug": "cursor-vs-github-copilot", "name": "Cursor vs GitHub Copilot",
         "why": "Two vendors, two meters, same question about model and surface ownership."},
        {"slug": "supabase-vs-firebase", "name": "Supabase vs Firebase",
         "why": "The clearest case of a free tier that expires the moment your usage pattern changes."},
    ],
}

items = []
for slug, meta in META.items():
    final = json.load(open(os.path.join(BASE, "content", "final", slug + ".json"), encoding="utf-8"))
    item = {
        "slug": slug,
        "category": meta["category"],
        "last_verified": VERIFIED,
        "published": "2026-11-10",
        "hook": final["hook"],
        "tool_a": meta["tool_a"],
        "tool_b": meta["tool_b"],
        "sections": final["sections"],
        "cost_math": final["cost_math"],
        "decision_matrix": final["decision_matrix"],
        "verdict_summary": final["verdict_summary"],
        "migration_guide": meta["migration_guide"],
        "faqs": final["faqs"],
        "sources": final["sources"],
        "related": RELATED[slug],
    }
    items.append(item)

path = os.path.join(BASE, "data", "tools.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("wrote", path, os.path.getsize(path), "bytes")
for it in items:
    body = "".join(s["content"] for s in it["sections"])
    print("  %-28s body=%d  sections=%d  matrix=%d  cost=%d  faq=%d  src=%d" % (
        it["slug"], len(body), len(it["sections"]), len(it["decision_matrix"]),
        len(it["cost_math"]), len(it["faqs"]), len(it["sources"])))
