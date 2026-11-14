#!/usr/bin/env python3
"""Merge reviewed article content + refreshed 2026 product metadata into data/tools.json."""

import json
import os
import sys
import copy
import argparse
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
from tools.validate_data import validate_items, SLUG
from tools.lint_content import lint_article
VERIFIED = "2026-11-10"

META = {
    "supabase-vs-firebase": {
        "category": "Backend & Database",
        "tool_a": {
            "name": "Supabase",
            "tagline": "Postgres with compute and metered Realtime",
            "db": "PostgreSQL (relational + pgvector)",
            "pricing": "Free: 500 MB, 2 projects · Pro $25 + $10/project compute",
            "self_host": "Yes (Docker stack)",
            "realtime": "Postgres Changes: recipient-level messages; 5M included on Pro then $2.50/M",
            "ai_readiness": "pgvector in the same database as your app data",
            "lock_in": "Low: standard Postgres, dump and leave",
            "badge": "Open source",
            "cta_url": "https://supabase.com/?utm_source=devtoolsradar",
            "pros": [
                "SQL queries do not have a per-read charge; Realtime delivery and other usage are separately metered",
                "pgvector lives in the same Postgres as your rows, so RAG needs no second system",
                "Standard Postgres: SQL, JOINs, transactions, triggers, and pg_dump as an exit door",
                "The connection ceiling is purchasable: 200 pooled connections on $10 Micro up to 12,000 on $3,730",
            ],
            "cons": [
                "Compute capacity and metered usage both matter; Realtime quotas and throughput limits are separate",
                "Every extra project adds its own compute line ($10 for a Micro) even on one Pro plan",
                "Free projects are paused after a week of inactivity, which kills demo and staging projects",
                "Realtime has published message-rate and connection limits; database pooler capacity is separate",
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
            "pricing": "Standard us-central1: reads $0.03 / writes $0.09 per 100k; daily allowances",
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
                "Listeners meter additions, updates and change-driven removals; initial queries and reconnects can add reads",
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

    "vercel-vs-cloudflare-pages": {'category': 'Hosting & Edge',
 'tool_a': {'name': 'Vercel',
            'tagline': 'The framework vendor that runs your framework',
            'db': 'Serverless functions on Fluid compute',
            'pricing': 'Verify Pro CDN billing mode; Flat Rate includes 1M requests/1 TB with '
                       'capacity tiers',
            'self_host': 'No (Vercel infrastructure)',
            'realtime': 'Streaming responses and ISR revalidation',
            'ai_readiness': 'Fluid compute targets inference and agent workloads',
            'lock_in': 'Medium: framework and platform coupling',
            'badge': 'Framework-native',
            'cta_url': 'https://vercel.com/?utm_source=devtoolsradar',
            'pros': ['Your framework deploys as written; no runtime port to a different JS '
                     'environment',
                     'Fluid compute bills execution time, so an idle await on an external API '
                     'costs no CPU',
                     'In-function concurrency shares one instance across concurrent requests',
                     'Per-project previews and ISR in the same product as the build pipeline'],
            'cons': ['Flat Rate CDN and usage-based billing require different cost models',
                     'Function duration depends on runtime, plan and deployed configuration',
                     'Price is per seat, so a growing team raises the floor before traffic does',
                     'Active CPU is a separate metered line on top of the seat price'],
            'code_example': "// Vercel: the framework's own handler, deployed unchanged.\n"
                            'export const maxDuration = 60; // seconds; the platform caps it\n'
                            'export async function POST(req: Request) {\n'
                            '  const { prompt } = await req.json();\n'
                            '  // Active CPU bills while this code runs, not while it waits:\n'
                            "  const upstream = await fetch('https://api.example.com/v1/chat', {\n"
                            "    method: 'POST',\n"
                            '    body: JSON.stringify({ prompt }),\n'
                            "    headers: { 'content-type': 'application/json' },\n"
                            '  });\n'
                            '  // Here it breaks: default duration limits kill long streams. Set '
                            'maxDuration\n'
                            '  // and check the platform ceiling before shipping a 5-minute job.\n'
                            "  return new Response(upstream.body, { headers: { 'content-type': "
                            "'text/event-stream' } });\n"
                            '}'},
 'tool_b': {'name': 'Cloudflare Pages',
            'tagline': 'The network vendor that runs your requests',
            'db': 'Workers runtime + Pages static assets',
            'pricing': 'Pages free · Workers Paid from $5/account, $0 egress',
            'self_host': 'No (Cloudflare network)',
            'realtime': 'WebSocket upgrade bills one request; messages bill nothing',
            'ai_readiness': 'CPU-metered runtime; 30M CPU-ms included per month',
            'lock_in': 'Medium-high: Workers runtime, per-product line items',
            'badge': 'Zero egress',
            'cta_url': 'https://pages.cloudflare.com/?utm_source=devtoolsradar',
            'pros': ['Workers Standard has no egress charge; other products meter separately',
                     'Workers Standard request overage is $0.30/M beyond 10M included',
                     'Static delivery and cache behavior can change invocation counts; measure '
                     'actual execution',
                     'WebSocket messages are not billed as requests — only the upgrade is'],
            'cons': ['Your handlers run on the Workers runtime, so the port is real work, not a '
                     'config change',
                     'Hard ceilings that stop a deployment instead of billing you: 25 MiB per '
                     'asset, 20-minute builds',
                     'Pages Free allows 500 builds a month and 20,000 files per site',
                     'Paid HTTP CPU up to 5 min; Cron and Queue limits differ, with separate '
                     'wall-time limits'],
            'code_example': "// Cloudflare: the Worker handler, not the framework's.\n"
                            'export default {\n'
                            '  async fetch(request, env, ctx) {\n'
                            '    const { prompt } = await request.json();\n'
                            '    // CPU-ms bills only while this isolate executes.\n'
                            "    const upstream = await fetch('https://api.example.com/v1/chat', "
                            '{\n'
                            "      method: 'POST',\n"
                            '      body: JSON.stringify({ prompt }),\n'
                            "      headers: { 'content-type': 'application/json' },\n"
                            '    });\n'
                            '    // Here it breaks: no Node APIs by default. Anything importing '
                            'fs, net or\n'
                            '    // a native addon needs nodejs_compat, and some libraries never '
                            'port.\n'
                            "    return new Response(upstream.body, { headers: { 'content-type': "
                            "'text/event-stream' } });\n"
                            '  },\n'
                            '};'},
 'migration_guide': 'Test the framework adapter, runtime APIs, state bindings and cache behavior '
                    'before moving. Compare actual account billing modes and measured usage; '
                    'validate deployed function duration, Worker trigger limits, Pages build '
                    'timeout and asset sizes. Do not assume traffic above 1 TB creates the same '
                    'bill on every Vercel team.',
 'related': []},

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
    "bun-vs-node": {
        "category": "Runtimes & Tooling",
        "tool_a": {
            "name": "Bun",
            "tagline": "One binary: runtime, package manager, test runner, bundler",
            "db": "JavaScriptCore runtime, rewritten in Rust for 1.4",
            "pricing": "Free · MIT · no paid tier",
            "self_host": "Yes — a single executable",
            "realtime": "Bun.serve HTTP and WebSocket server built in",
            "ai_readiness": "Claude Code ships as a Bun executable (Bun's statement)",
            "lock_in": "Low: MIT, npm-compatible, runs Node projects",
            "badge": "All-in-one",
            "cta_url": "https://bun.com/?utm_source=devtoolsradar",
            "pros": [
                "JavaScript, TypeScript, JSX and bundling from one executable, so no separate tsc, test runner or bundler",
                "1,517 more Node test-suite tests pass in 1.4, and node:sqlite passes 18 of 18 by Bun's own count",
                "Bun's own hello.js benchmark: 5.1 ms vs 27.2 ms start-up on Linux, 14.6 MB vs 44.5 MB peak memory",
                "MIT licensed after the Anthropic acquisition, with the Node compatibility target moved to 26.3.0",
            ],
            "cons": [
                "node:http passes 403 of 415 of Node's own tests, and http.Server does not extend net.Server",
                "node:https lacks getPeerCertificate() and getCipher(), and SNICallback is unsupported",
                "NODE_MODULE_VERSION 147 means addons built for Node 24 must be rebuilt",
                "Bun's own memory table shows the Vite dev server at 233 MB vs 214 MB on Node",
            ],
            "code_example": (
                "// One binary replaces four dev dependencies:\n"
                "// bun install, bun test, bun lint and bun fmt are the same executable.\n"
                "import { Database } from \"bun:sqlite\";   // built in, no addon to compile\n"
                "const db = new Database(\":memory:\");\n"
                "db.run(\"create table t (id integer primary key, name text)\");\n"
                "// Here it breaks: a native addon built for Node 24 will not load,\n"
                "// because Bun 1.4 reports NODE_MODULE_VERSION 147."
            ),
        },
        "tool_b": {
            "name": "Node.js",
            "tagline": "The runtime with a published release calendar",
            "db": "Node core plus the npm ecosystem",
            "pricing": "Free · MIT · support past Maintenance LTS via OpenJS partners",
            "self_host": "Yes — your own machines",
            "realtime": "node:http servers, cluster workers, inspector for tracing",
            "ai_readiness": "Type stripping on by default; no type checking",
            "lock_in": "None: MIT, runs on every platform",
            "badge": "Standards runtime",
            "cta_url": "https://nodejs.org/?utm_source=devtoolsradar",
            "pros": [
                "A dated calendar: v26 Lithium and v24 Krypton are LTS, and LTS typically guarantees fixes for 30 months",
                "Native addons are the default path, and ABI builds target the runtime you actually run",
                "TypeScript type stripping runs with no build step for erasable syntax",
                "Nothing to license, and commercial support exists through OpenJS partners after LTS ends",
            ],
            "cons": [
                "Type stripping refuses enum, .tsx, parameter properties, import aliases and tsconfig paths",
                "TypeScript inside node_modules is refused outright",
                "Parsing requires WebAssembly, or the parser throws ERR_WEBASSEMBLY_NOT_SUPPORTED",
                "v20 and v25 both reached end of life in 2026, so the calendar forces migrations",
            ],
            "code_example": (
                "// Node 26 strips types; it does not check them or transform them.\n"
                "type Host = string;\n"
                "const host: Host = process.env.HOST ?? \"localhost\";\n"
                "console.log(`binding ${host}`);\n"
                "// Here it breaks: an enum is not erasable, so Node throws\n"
                "// ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX before your code runs.\n"
                "enum Mode { Dev, Prod }"
            ),
        },
        "migration_guide": (
            "Moving to Bun starts with `bun install` reading the same package.json, but every native addon "
            "needs a build for NODE_MODULE_VERSION 147 before it loads, so the hook stampede is the first "
            "thing to schedule. Moving back is not automatic either: Bun's compatibility docs list the API "
            "gaps you will meet — getPeerCertificate(), SNICallback, async_hooks — and there is no tool that "
            "rewrites handlers around them. Run the service test suite under both runtimes before either "
            "direction, then keep the loser's addon builds around for a release or two."
        ),
        "related": [],
    },

    "prisma-vs-drizzle": {
        "category": "Data & ORM",
        "tool_a": {
            "name": "Prisma",
            "tagline": "Schema-first ORM with a generated client, sold beside a database",
            "db": "Any SQL database through driver adapters; Prisma Postgres is managed",
            "pricing": "ORM free · Prisma Postgres Free / $10 / $49 / $129 · Compute metered",
            "self_host": "Yes for the ORM; Prisma Postgres is managed",
            "realtime": "Compute and Postgres scale to zero; the Accelerate cache retires 1 Dec 2026",
            "ai_readiness": "Generated typed client over a schema contract",
            "lock_in": "Medium: schema DSL, generated client, optional platform",
            "badge": "Code generation",
            "cta_url": "https://www.prisma.io/?utm_source=devtoolsradar",
            "pros": [
                "One schema artefact drives migrations, types and the generated client",
                "Rust-free client in 7.x: Prisma's figures are 90% smaller output and 3x faster queries",
                "Prisma Postgres bills operations with no per-seat charge and a hard spend limit on paid plans",
                "Raw queries bypass the compiler from 7.3.0, and compilerBuild chooses fast or small",
            ],
            "cons": [
                "output is now required on the generator, so the client no longer lands in node_modules",
                "A third-party test measured cold start worse than the Rust engine: about 69 ms vs 236 ms",
                "The same test saw node_modules grow from 254.1 MiB to 333.3 MiB with WASM compilers per database",
                "Starter's $10 stops being cheaper at 5.875M operations, where Pro's $49 takes over",
            ],
            "code_example": (
                "// Prisma: the schema is a separate artefact, and the client is generated from it.\n"
                "generator client {\n"
                "  provider = \"prisma-client\"\n"
                "  output   = \"../src/generated/prisma\"   // required since 7.x\n"
                "  compilerBuild = \"fast\"                   // or \"small\"\n"
                "}\n"
                "// Here it breaks: the old datasource url style is gone in 7 —\n"
                "// connection details move to prisma.config.ts."
            ),
        },
        "tool_b": {
            "name": "Drizzle",
            "tagline": "The schema is a TypeScript file; nothing is generated",
            "db": "Postgres, MySQL, SQLite, SingleStore, MSSQL, CockroachDB",
            "pricing": "Free: ORM, Kit, local Studio, Gateway · paid: embeddable Studio Component",
            "self_host": "Yes — a library, not a service",
            "realtime": "Queries run through your driver as SQL you can read",
            "ai_readiness": "Zero dependencies and SQL-shaped output (vendor claim)",
            "lock_in": "Low: no engine, no runtime, plain SQL",
            "badge": "Open source",
            "cta_url": "https://orm.drizzle.team/?utm_source=devtoolsradar",
            "pros": [
                "No generate step and no engine to load: the TypeScript schema is the source of truth",
                "ORM, Kit, Studio for local development and Gateway are all free",
                "Six dialects through standard drivers, from Postgres to CockroachDB",
                "The relational query API emits one SQL statement (vendor claim), which suits serverless databases",
            ],
            "cons": [
                "No stable 1.0: 1.0.0-rc.5 shipped 21 October 2026 with a dozen-plus breaking changes",
                "Drizzle Studio is not open source, and the embeddable Studio Component is the paid product",
                "PlanetScale hired the entire core team in March 2026, so maintenance sits with a database vendor",
                "Relations are declared, not inferred: the SQL is yours to get right",
            ],
            "code_example": (
                "// Drizzle: this file is the schema. No generate step, no engine to load.\n"
                "import { pgTable, serial, varchar } from \"drizzle-orm/pg-core\";\n"
                "export const countries = pgTable(\"countries\", {\n"
                "  id: serial().primaryKey(),\n"
                "  name: varchar({ length: 256 }),\n"
                "});\n"
                "// Here it breaks: relations are declared explicitly, so a missing join\n"
                "// is a query you wrote — not a bug the ORM hides from you."
            ),
        },
        "migration_guide": (
            "Prisma to Drizzle rewrites the data layer: every model becomes a table definition, the "
            "`prisma migrate` history becomes drizzle-kit migrations, and there is no client to generate. "
            "Drizzle to Prisma means writing one schema file that becomes the truth again, and deciding "
            "whether the generated client is committed or ignored. In both directions, the migration tooling "
            "writes SQL you review — neither one replays the other's history."
        ),
        "related": [],
    },

    "docker-vs-podman": {
        "category": "Containers & Runtime",
        "tool_a": {
            "name": "Docker",
            "tagline": "An open-source engine under a licensed desktop",
            "db": "Docker Engine (Moby) plus the Docker Desktop app",
            "pricing": "Personal $0 · Pro $9 · Team $15 per user/month · Business quote-only",
            "self_host": "Yes for Engine and Moby; Desktop carries the subscription agreement",
            "realtime": "Build Cloud minutes per plan; Testcontainers Cloud at $3-4 per 100 minutes",
            "ai_readiness": "Hardened Images free for developers, from $5k/repo in production",
            "lock_in": "Medium: Compose and image tooling are standard, the desktop is licensed",
            "badge": "Licensed desktop",
            "cta_url": "https://www.docker.com/?utm_source=devtoolsradar",
            "pros": [
                "Desktop stays free under 250 employees AND $10M revenue, plus personal, education and non-commercial OSS",
                "A flat per-user rate with monthly or annual billing, and seats can be removed when people leave",
                "Team adds audit logs and RBAC; Business adds SSO, SCIM, Hardened Desktop and Image Access Management",
                "Build Cloud minutes and Testcontainers Cloud arrive on the same contract",
            ],
            "cons": [
                "Free use is a company-size test: cross either limit and every commercial seat is paid at once",
                "Government entities pay for Docker Desktop regardless of size",
                "Production Hardened Images start at $5k per repository, which dwarfs seat revenue for a small team",
                "Business pricing is quote-only, so the biggest line item is the one you cannot see",
            ],
            "code_example": (
                "# The engine is open source; Docker Desktop is the licensed surface.\n"
                "$ docker run --rm -v \"$PWD\":/app -w /app node:24 npm ci\n"
                "# Here it breaks: past 250 employees or $10M revenue, every\n"
                "# commercial Desktop seat must be on Pro, Team or Business.\n"
                "$ docker buildx bake --set \"*.cache-from=type=registry\""
            ),
        },
        "tool_b": {
            "name": "Podman",
            "tagline": "Daemonless rootless containers under Apache 2.0",
            "db": "Podman 6.1.4 runtime with Podman Desktop 1.30.5",
            "pricing": "Free · Apache 2.0 · enterprise support through the Red Hat build",
            "self_host": "Yes — a local process, not a service",
            "realtime": "Socket-activated API with one listening socket (--time default 5 s)",
            "ai_readiness": "GPU acceleration in Podman Desktop (vendor claim)",
            "lock_in": "Low: Apache 2.0, OCI and Compose compatible",
            "badge": "No paid tier",
            "cta_url": "https://podman.io/?utm_source=devtoolsradar",
            "pros": [
                "No daemon and no seat: containers run as the invoking user and nothing idles in the background",
                "Docker v1.40 compatibility layer, so DOCKER_HOST moves most CLI and Compose tooling",
                "Podman Desktop is CNCF-hosted, Apache 2.0 and vendor-neutral, with Kubernetes and Compose extensions",
                "Enterprise support exists without a licence tier: Red Hat sells a supported build",
            ],
            "cons": [
                "The API socket is arbitrary code execution as that user, with no way to limit or audit it (Podman's man page)",
                "Docker-only API surface still needs rewriting, and the compatibility layer is Docker v1.40",
                "The service command is unavailable where Podman runs directly on a Windows or macOS host",
                "There is no vendor to call unless you buy the Red Hat build",
            ],
            "code_example": (
                "# No daemon to start: each command is a process that runs and exits.\n"
                "$ podman run --rm -v \"$PWD\":/app -w /app node:24 npm ci\n"
                "# Docker tooling can use the compatibility socket:\n"
                "$ systemctl --user start podman.socket\n"
                "$ export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock\n"
                "# Here it breaks: that socket is full access as your user, so\n"
                "# never bind it to TCP without mutual TLS."
            ),
        },
        "migration_guide": (
            "Moving to Podman is one environment variable for CLI and Compose tooling plus two work items: "
            "handlers that use Docker-only API surface, and a decision about who may open the socket on each "
            "build host. Moving back is the same variable unset, which is why teams often keep both — Docker "
            "for the licensed platform services, Podman on machines that only need a runtime."
        ),
        "related": [],
    },

    "clerk-vs-auth0": {
        "category": "Identity & Auth",
        "tool_a": {
            "name": "Clerk",
            "tagline": "Authentication as a product surface, billed on retained users",
            "db": "Hosted auth with prebuilt UI, organisations and billing",
            "pricing": "Hobby $0 · Pro $25/mo ($20 annual) · Business $300/mo ($250 annual)",
            "self_host": "No (hosted service)",
            "realtime": "50,000 MRU included per app; sessions from 5 minutes to 10 years on paid",
            "ai_readiness": "M2M tokens and API keys with monthly verification limits",
            "lock_in": "Medium: hosted users, full data exports on every plan",
            "badge": "Retained users",
            "cta_url": "https://clerk.com/?utm_source=devtoolsradar",
            "pros": [
                "50,000 MRU included on Pro, then $0.02 each — a user who never returns is never billed",
                "Unlimited applications on every plan, including Hobby",
                "Organisations and B2B authentication are in the same product, with 100 MRO included",
                "Full data exports on every plan, so leaving is a data move rather than a negotiation",
            ],
            "cons": [
                "The bill hides in add-ons: SSO $75/mo each, Directory Sync $75/mo each from 1 January 2027",
                "Hobby stops at 50,000 MRU after a one-month grace period",
                "Protect checks meter at $0.002 after 10,000 free, so attack traffic is a billable event",
                "Business is a $300/mo step mostly for SOC 2, seats and 30-day logs",
            ],
            "code_example": (
                "// Clerk bills a retained user, not a session: the first day is free.\n"
                "const { totalCount } = await clerkClient.users.getUserList({ limit: 1 });\n"
                "// Here it breaks: past 50,000 MRU on Pro each extra user is $0.02/month,\n"
                "// and Hobby gives one grace month before requests stop being served.\n"
                "if (totalCount > 50_000) console.warn(totalCount, \"MRU — check the plan\");"
            ),
        },
        "tool_b": {
            "name": "Auth0",
            "tagline": "Identity infrastructure priced in tiers of monthly active users",
            "db": "Hosted identity platform: connections, tenants, rules",
            "pricing": "Free 25,000 MAU · Essentials from $35 · Professional from $240 · Enterprise quote",
            "self_host": "No (hosted); private deployment is an Enterprise add-on",
            "realtime": "Tenants 1/3/12/unlimited by plan; 3 enterprise connections on B2B Essentials",
            "ai_readiness": "AI Agents add-on adds 50% to the base price",
            "lock_in": "High: tenants, connections and rules live inside the product",
            "badge": "Tiered MAU",
            "cta_url": "https://auth0.com/?utm_source=devtoolsradar",
            "pros": [
                "25,000 MAU free, with 5 organisations, self-service SSO and SCIM included",
                "B2B Essentials is $150/month for 500 MAU with unlimited organisations",
                "Enterprise SSO connections included — 3 on Essentials, 5 on Professional — then $100/month each",
                "Professional adds custom database connections, cross-app SSO and 12 tenants",
            ],
            "cons": [
                "Price is a step function: 501 B2C users bill at the 1,000 tier, $70 instead of $35",
                "The B2C Professional sheet ends at 20,000 MAU; past that it is a quote or not available",
                "Custom enterprise SSO on B2C requires Enterprise — not available on Essentials or Professional",
                "The AI Agents add-on adds 50% to whichever tier it is applied to",
            ],
            "code_example": (
                "# Auth0 prices the tier, not the user: 501 MAU bills as 1,000.\n"
                "TIERS = [(500, 35), (1_000, 70), (2_500, 175), (5_000, 350)]\n"
                "def essentials(mau):\n"
                "    return next(p for cap, p in TIERS if mau <= cap)\n"
                "print(essentials(501))  # 70, not 35\n"
                "# Here it breaks: above 50,000 B2C MAU the printed sheet ends."
            ),
        },
        "migration_guide": (
            "Clerk to Auth0 means exporting users, recreating connections and mapping organisations onto a "
            "plan that includes 5 on Free and 10 on paid tiers — well short of 200 without a higher tier. "
            "Auth0 to Clerk changes the unit: MAU becomes MRU, so the population you migrate is not the "
            "population you are billed for, and users who never return after day one vanish from the invoice."
        ),
        "related": [],
    },

    "planetscale-vs-neon": {
        "category": "Backend & Database",
        "tool_a": {
            "name": "PlanetScale",
            "tagline": "Dedicated clusters billed whether or not they are awake",
            "db": "Postgres (single node, HA, Neki sharding) and Vitess for MySQL",
            "pricing": "No free plan · Postgres $5/mo single node, $15/mo HA, Neki from $30/shard",
            "self_host": "No (managed on AWS, GCP and Azure)",
            "realtime": "3-node HA clusters; Neki shards run 1 primary and 2 replicas each",
            "ai_readiness": "MCP and Insights in the platform (vendor description)",
            "lock_in": "Medium: Postgres or MySQL underneath, managed control plane on top",
            "badge": "Clusters",
            "cta_url": "https://planetscale.com/?utm_source=devtoolsradar",
            "pros": [
                "A fixed cluster charge: PS-5 HA is $15/month whether the database sleeps or not",
                "Every branch is its own cluster, so a schema change never touches production",
                "Postgres, Neki's sharded Postgres and Vitess for MySQL on one platform",
                "Backups included up to 2x disk size and run automatically every 12 hours",
            ],
            "cons": [
                "No free plan anywhere: the cheapest database is $5/month single node",
                "A branch is a second cluster, so 20 PS-5 HA branches bill $300/month",
                "Storage past 10 GB per instance bills at a region rate the docs expose only through an endpoint",
                "Neki is a platform preview, and PlanetScale says not to run production on it",
            ],
            "code_example": (
                "# PlanetScale bills the cluster, prorated to the millisecond.\n"
                "# PS-5 HA = 1 primary + 2 replicas, $15/month per branch, awake or not.\n"
                "# 20 branches for pull requests: 20 x $15 = $300/month.\n"
                "# Here it breaks: a branch is not metadata, it is a second cluster,\n"
                "# so preview environments get priced like production ones."
            ),
        },
        "tool_b": {
            "name": "Neon",
            "tagline": "Postgres billed by the CU-hour it is awake, from Databricks",
            "db": "Lakebase Postgres with branching, Data API, Functions and Object Storage",
            "pricing": "Free plan · Launch $0.106/CU-hour · Scale $0.222/CU-hour",
            "self_host": "No (managed, Databricks)",
            "realtime": "Up to 10,000 pooled connections per compute; scale to zero after 5 minutes",
            "ai_readiness": "Managed Better Auth and an AI Gateway with prepaid credits",
            "lock_in": "Medium: Postgres underneath, but branches and services are Neon's",
            "badge": "CU-hours",
            "cta_url": "https://neon.com/?utm_source=devtoolsradar",
            "pros": [
                "Suspended compute costs $0, so a database that sleeps most of the day costs almost nothing",
                "A permanent free plan: 100 CU-hours, 1 GB storage and 100 projects",
                "Branches cost $1.50 a month after 10 included, which makes a preview per pull request affordable",
                "Storage at $0.35/GB-month and 500 GB egress included per project on Launch",
            ],
            "cons": [
                "An always-on 0.25 CU costs 0.25 x 730 x $0.106 = $19.35/month, above a $15 cluster",
                "One CU running all month is $77.38 on Launch and $162.06 on Scale",
                "Storage, instant restore, extra branches and egress are separate lines on the same invoice",
                "Scale doubles the CU rate for the same compute shape",
            ],
            "code_example": (
                "# Neon bills compute size x hours awake; suspended compute is $0.\n"
                "# Launch: $0.106 per CU-hour. 0.25 CU awake all month:\n"
                "0.25 * 730 * 0.106   # 19.35, before storage\n"
                "# Here it breaks: a health check every few minutes keeps leaving\n"
                "# the compute awake, so the invoice tracks uptime, not traffic."
            ),
        },
        "migration_guide": (
            "Neon to PlanetScale gives up brevity: branches become clusters, scale-to-zero disappears and the "
            "cheapest HA Postgres is $15/month. PlanetScale to Neon restarts the clock — CU-hours accrue while "
            "the database is awake, so the setting to watch is the suspension timer rather than a cluster size, "
            "and storage plus egress move onto the same invoice. Dump and restore with pg_dump in both "
            "directions; both are Postgres underneath."
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
    "bun-vs-node": [
        {"slug": "docker-vs-podman", "name": "Docker vs Podman",
         "why": "Another open-source runtime where the licence sits on the developer tool, not the engine."},
        {"slug": "prisma-vs-drizzle", "name": "Prisma vs Drizzle",
         "why": "Two free libraries whose maintenance now depends on a vendor with a bill attached."},
    ],
    "prisma-vs-drizzle": [
        {"slug": "planetscale-vs-neon", "name": "PlanetScale vs Neon",
         "why": "Where the Drizzle team went to work, and what that database actually costs."},
        {"slug": "bun-vs-node", "name": "Bun vs Node.js",
         "why": "Prisma Compute runs on Bun's Rust port — the runtime invoice, told the same way."},
    ],
    "docker-vs-podman": [
        {"slug": "bun-vs-node", "name": "Bun vs Node.js",
         "why": "Open-source engine, licensed surface, and two bills measured in labour."},
        {"slug": "clerk-vs-auth0", "name": "Clerk vs Auth0",
         "why": "The other per-seat bill: identity, priced by the people who show up."},
    ],
    "clerk-vs-auth0": [
        {"slug": "docker-vs-podman", "name": "Docker vs Podman",
         "why": "Headcount decides both bills: seats at Docker, retained users at Clerk."},
        {"slug": "supabase-vs-firebase", "name": "Supabase vs Firebase",
         "why": "The same lesson in a database: the unit you are billed on is the architecture."},
    ],
    "planetscale-vs-neon": [
        {"slug": "prisma-vs-drizzle", "name": "Prisma vs Drizzle",
         "why": "The ORM that now shares a payroll with one side of this comparison."},
        {"slug": "supabase-vs-firebase", "name": "Supabase vs Firebase",
         "why": "Metered reads against a flat instance: the ancestor of this arithmetic."},
    ],
}


def merge_articles(base=BASE, output=None):
    """Refresh reviewed content without dropping articles or inventing verification dates.

    Existing deployment metadata is preserved. A new article must supply its dates
    and complete metadata (legacy META may fill tool metadata only).
    """
    base = Path(base)
    path = Path(output) if output is not None else base / "data" / "tools.json"
    source = base / "data" / "tools.json"
    existing = json.loads(source.read_text(encoding="utf-8")) if source.exists() else []
    if not isinstance(existing, list):
        raise ValueError("existing data/tools.json must be a list")
    if existing:
        errors = validate_items(existing)
        if errors:
            raise ValueError("Invalid existing deployment data: " + "; ".join(errors))
    by_slug = {item["slug"]: copy.deepcopy(item) for item in existing}
    finals = sorted((base / "content" / "final").glob("*.json"))
    if not finals:
        raise ValueError("No reviewed final articles found")
    seen = set()
    for final_path in finals:
        final = json.loads(final_path.read_text(encoding="utf-8"))
        slug, errors, _ = lint_article(final, str(final_path))
        if errors:
            raise ValueError(f"{final_path}: " + "; ".join(errors))
        if slug != final_path.stem or slug in seen:
            raise ValueError(f"Duplicate or filename-mismatched slug: {slug}")
        seen.add(slug)
        item = by_slug.get(slug, copy.deepcopy(META.get(slug, {})))
        # Explicit reviewed metadata overrides previous values; absent dates stay
        # unchanged. Never stamp today's date merely because content was merged.
        item.update(final)
        if "related" not in item:
            item["related"] = copy.deepcopy(RELATED.get(slug, []))
        by_slug[slug] = item
    items = list(by_slug.values())
    errors = validate_items(items)
    if errors:
        raise ValueError("Invalid merged deployment data: " + "; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement only after every article validates.
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".tools-", suffix=".json", delete=False) as f:
            tmp = Path(f.name)
            json.dump(items, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--output", type=Path, help="Write merged data elsewhere without replacing deployment input")
    args = parser.parse_args()
    try:
        items = merge_articles(args.base, args.output)
    except (OSError, ValueError) as exc:
        print(f"Merge failed: {exc}", file=sys.stderr)
        return 1
    print(f"Merged {len(items)} articles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
