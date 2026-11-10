#!/usr/bin/env python3
"""Build the writing prompt for each article from a shared contract + per-article angle."""

import os

BASE = "/workspace/devtools-radar"

CONTRACT = """You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/{slug}.md
  @docs/tech-blog-writing-standard.md

The fact sheet is your ONLY source of numbers, prices, product names, feature claims and version
facts. If a number is not in the fact sheet, do not write a number. If a product name or tool is not
there, do not invent one. Do not add benchmarks. Do not add "typically" figures. Do not add prices
from memory — the market changed in 2026 and your memory is stale.

STEP 2 — Obey the writing standard (sections 3 through 7) exactly:
- First 3 lines = a hook of the "loss number", "counter-intuitive claim" or "disappeared thing" type.
  Banned openings: "In today's...", "It's important to note", "In this article we will", rhetorical
  questions, "X is very important".
- Before any comparison table, establish each product's philosophy in one sentence, then show what
  that philosophy forbids.
- Read every price table as a penalty table: name which usage pattern this vendor punishes and why.
- Every derived cost shows its formula (unit price x volume), never a bare total.
- Mark vendor claims as vendor claims ("Cloudflare's own example", "Cursor states").
- Sentences must vary in length. Max 4 sentences per paragraph. A visual anchor (table, code block,
  bullet list, blockquote) at least every 300 characters.
- Banned words: game-changer, seamless, robust, leverage, delve, landscape, realm, unlock, empower,
  "in conclusion", "it's worth noting", "when it comes to", "the world of".
- End with what the reader should check or decide today — not a summary of what they just read.
- Each section 600-1,100 characters. Total across sections 3,200-4,800 characters.
- 5 or 6 sections. Section titles are claims or questions, never bare nouns like "Pricing".
- No HTML. Markdown subset only: **bold**, `inline code`, - bullets, 1. numbered, ```fenced code```,
  | pipe tables |, > blockquote. Do NOT use ## headings inside section content (the builder adds the
  heading from the title).
- Code fences: runnable, under 20 lines, comments only explaining "why" or "here it breaks".

STEP 3 — Write the article:

{angle}

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/{slug}.json

with exactly these keys:

{{
  "slug": "{slug}",
  "hook": "2 sentences, no more. The hook described above.",
  "sections": [ {{ "title": "...", "content": "markdown" }} ],
  "decision_matrix": [ {{ "situation": "...", "pick": "...", "why": "one sentence" }} ],
  "cost_math": [ {{ "label": "...", "formula": "...", "result": "..." }} ],
  "verdict_summary": "2-3 sentences, must name a conditional winner. No 'it depends' ending.",
  "faqs": [ {{ "q": "...", "a": "..." }} ],
  "sources": [ "https://..." ]
}}

Rules for the structured fields:
- decision_matrix: 6-8 rows. "pick" is a product name or a short conditional ("Neither — stay put").
  Cover the awkward cases, not only the obvious ones.
- cost_math: 2-4 rows. formula must be readable arithmetic with real unit prices from the fact sheet.
- faqs: exactly 4. Each answer must add a fact NOT already stated in the sections, max 2 sentences.
- sources: 3-6 URLs taken from the fact sheet's source links.
- reading_time is NOT yours to write; the builder computes it.

STEP 5 — After writing the file, run this check and fix anything it reports:
  python3 -c "import json;d=json.load(open('content/draft/{slug}.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
"""

ANGLES = {
    "supabase-vs-firebase": """The editorial angle: THE BILLING UNIT IS THE ARCHITECTURE.

The 2024 version of this comparison was "Postgres vs NoSQL". The 2026 version is harder and more
useful: Supabase sells compute (a machine, a disk, a connection ceiling) and Firebase sells events
(document reads, writes, index entry reads, and a read per change on every live listener). Those two
meters punish different code. Supabase punishes connections and disk; Firestore punishes watching.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids (JOINs absent on Firestore; a hard
   connection ceiling of 60 direct / 200 pooled on Supabase's $10 Micro and no way to buy an
   infinite pool).
2. The Firestore realtime trap, with the arithmetic from the fact sheet: a 50-user dashboard
   watching 100 documents that change 20 times a minute is ~4.32B read events/month, about
   $1,296/month, while the same shape on Supabase Pro is a flat $25. Show the multiplication.
   Also note reconnects are billed like new queries.
3. The counter-trap: on Supabase, a Postgres Changes subscription is a database event stream that
   you opt into per table (alter publication ... add table), and the ceiling you hit is the
   connection/pooler ceiling and the compute tier, not a per-read meter. Say plainly that this
   swaps a metered risk for a capacity risk.
4. Index entry reads on Firestore — the line item nobody quotes: 1 read per 1,000 index entries,
   a second range field starts billing, count() bills index reads.
5. The migration section must be honest: firebase-to-supabase copies one collection to one table,
   flattens to text/numeric/boolean/jsonb, you write the hooks that split nested data, and the
   password path needs a middleware the repo itself marks work in progress.
6. Verdict: a conditional winner with the deciding condition named in the first clause.""",

    "vercel-vs-cloudflare-pages": """The editorial angle: THEY CONVERGED, AND THE BILL MOVED TO A DIFFERENT LINE.

Both platforms now meter CPU time instead of wall time — Vercel calls it Active CPU under Fluid
compute ($0.128/vCPU-hour, memory in GB-hours at under 10% of that rate), Cloudflare includes 30M
CPU-ms then $0.02 per million and charges nothing for egress. That convergence is the story: the
question is no longer "who is cheaper per function call", it is "which line item does my workload
inflate", and the answer is transfer and requests on Vercel, CPU milliseconds on Cloudflare.

Required beats, in this order:
1. Philosophy in one sentence each (Vercel: the framework vendor runs your framework; Cloudflare:
   the network vendor runs your requests) and what each forbids.
2. The convergence: explain both meters with the fact-sheet numbers, including that Vercel bills
   execution time not wall time so an idle await is free on both now.
3. The arithmetic table: 3 TB of transfer (Vercel 2,048 GB over x $0.15 = $307.20 vs $0), 50M
   requests (Vercel 40M over x $2/M = $80 vs Cloudflare 40M over x $0.30/M = $12 + $5 base), and
   CPU at ~$0.0356 per million CPU-ms on Vercel versus $0.02 on Cloudflare. Show each formula.
4. The non-price ceilings that decide real projects: Cloudflare Pages Free = 500 builds/month,
   20-minute build timeout, 20,000 files, 25 MiB per asset; Vercel Pro = 10M requests, 1 TB, a
    5-minute function limit. Pick the one that breaks a real deployment and say which.
5. Where the "free egress" claim costs you: building the app for the platform (Workers runtime,
   D1/R2 line items exist too, cache-hit design to keep CPU low — Cloudflare's own example shows
   100M requests at 80% cache hit costing $2.20 of CPU instead of $13.40).
6. Verdict: conditional winner, condition in the first clause. The condition is what the workload
   spends: bytes and seats, or CPU milliseconds and build minutes.""",

    "cursor-vs-github-copilot": """The editorial angle: THE $20 AI EDITOR IS GONE. WHAT YOU ARE BUYING CHANGED.

This is the article's whole reason to exist. In 2026 Cursor is part of SpaceX: the partnership was
announced 21 April 2026 with a $10B payment and a $60B option, the all-stock deal was signed 16 June
2026 through X67 Inc., and it closed on 14 August 2026 with Cursor joining SpaceXAI to work on Grok,
Grok Build, Grok Bot and Cursor. Cursor's stated reason was compute. The pricing followed: $8 Plus
is Grok-only, $30 Premium is the first tier with third-party models and those are billed at API list
price on top, third-party usage is explicitly not included in the monthly price. Copilot went the
other way — $10 Pro with $15 of GitHub AI Credits, $39 Pro+, $100 Max, and one credit meter for
agent mode, code review, Copilot in the cloud, CLI and the app.

Required beats, in this order:
1. Open with the disappearance, not with a feature comparison. Then state what both products are
   now: agent-first, credit-metered, with a deliberately restricted entry tier.
2. Philosophy in one sentence each (Cursor: the model is the product, so the editor must own the
   model and the inference bill; GitHub: the repository is the product, so AI must land in review,
   PRs and issues) and what each forbids.
3. The penalty table: what does each meter punish? Cursor punishes heavy third-party model use
   (list price, unbundled) and rewards Grok loyalty; Copilot punishes breadth of agent use across
   seats and rewards keeping everything inside one vendor's surface.
4. The neutrality question, stated plainly: teams that chose Cursor partly to stay model-agnostic
   now buy from a company whose model is Grok; name the check a team should run before renewing.
5. The distribution counter-argument: Copilot's Free tier already runs agent mode and the CLI, so
   the free tier is not a demo — but PR review, file diff review, custom instructions and "assign
   work to Copilot and it creates a pull request" start at Pro.
6. Verdict: two different buyers, named in the first clause. Do not hedge into "both are great".""",

    "notion-vs-obsidian": """The editorial angle: ONE SELLS A SERVER WITH A METER, THE OTHER SELLS A FOLDER WITH A PIPE.

The naive comparison is free vs $10. The real one: Notion sells shared state — permissions,
databases, an agent, automations — and meters everything around it (180 API requests/minute per
connection on all plans except Business/Enterprise's 600, 7-day page history on Free, 5 MB uploads,
10 guests, Custom Agents at $10 per 1,000 Notion credits, Workers in beta). Obsidian sells nothing
and meters nothing: the app is free without limits, no telemetry, data local, and the optional
pieces are Sync at $4/user/month and Publish at $8/site/month, with the commercial licence
explicitly not required.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids (Obsidian has no server-side permission
   model and no built-in agent; Notion has no plain-file truth, so your export is a conversion, and
   your history is a plan feature).
2. The history/upload tiers as the hidden tax — 7 days on Free, 30 on Plus, 90 on Business. This is
   the most under-reported constraint and it decides whether Notion can be a system of record.
3. Bases: Obsidian shipped a core plugin that makes database views over frontmatter — Table and
   Cards in 1.9, List and Map in 1.10, Kanban in 1.14 — stored as a .base YAML file that holds only
   the view definition. This is the moment "Notion has databases, Obsidian has notes" stopped being
   true. Say what Bases still does not give you (permissions, server-side computed properties,
   multi-user edit).
4. The agent argument, factually: Notion's agents live in Business at $20/member and Custom Agents
   are metered at $10 per 1,000 credits; Obsidian's equivalent is you, a script, or a plugin. Then
   the honest counter: an API at 180 requests/minute is a queue you have to build, and every
   integration is a vendor relationship.
5. The real math: a 10-person team on Notion Business is $200/month = $2,400/year; the same team on
   Obsidian with Sync is $480/year on Sync plus an optional $500/year in commercial licences.
   Then say what the extra $1,900 buys and who should not pay it.
6. Verdict: conditional winner with the condition in the first clause — decide by whether the notes
   are shared state or private thinking.""",
    "bun-vs-node": """The editorial angle: NEITHER RUNTIME HAS A PRICE, SO THE BILL IS PAID IN SOMETHING ELSE.

Bun is MIT, Node is MIT, and neither has a paid tier. That is exactly why this comparison is worth
writing: with money out of the picture, the real meters are the release calendar, the compatibility
surface, and the native-module ABI. Node bills you on someone else's schedule. Bun bills you on the
tests it does not pass yet.

Required beats, in this order:
1. Open by taking the price question off the table: both runtimes are free and MIT-licensed, so the
   invoice is labour. Then the philosophy in one sentence each (Node: a standards body ships a
   runtime on a published clock; Bun: one binary ships the whole toolkit) and what each forbids.
2. Node's meter is the calendar. Show the table: v27 Alpha 29 Oct 2026, v26 Lithium LTS from 5 May
   2026, v25 EOL 31 Mar 2026, v24 Krypton LTS from 6 May 2025, v22 Jod LTS from 24 Apr 2024, v20 Iron
   EOL 24 Mar 2026. State the two rules that decide upgrades: LTS typically guarantees fixes for a
   total of 30 months, and starting with v27 every major gets six months of Alpha, six of Current,
   then LTS. This is a runtime you keep for years and must move on a date you did not choose.
3. Node's 2026 own goal and its limit: TypeScript type stripping is on by default and stable
   (stable at v25.2.0/v24.12.0), but it is only erasure. `enum`, `namespace` with runtime code,
   parameter properties and import aliases throw ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX, `.tsx` is
   unsupported, `tsconfig.json` is ignored so `paths` do not work, TypeScript inside node_modules is
   refused, and the parser needs WebAssembly. Show a four-line code block that works on Node 26 and
   the enum that does not.
4. Bun's meter is the failing 3%. Use Bun's own per-module pass counts: node:http 403/415,
   node:inspector 22/110, node:module 68/93, node:test_runner 28/81, node:fs 349/358, node:sqlite
   18/18. State the 1,517 newly passing tests in 1.4 as progress, then state the ABI tax: the Node
   compatibility target moved from 24.3.0 to 26.3.0, `NODE_MODULE_VERSION` is now 147, and native
   addons built for 24 must be rebuilt.
5. The gaps that decide real services, named from Bun's own compatibility docs: `http.Server` does not
   extend `net.Server` and the keepAlive options are no-ops; node:https is missing
   getPeerCertificate() and getCipher() and does not support SNICallback; node:crypto lacks
   ed448/x448/rsa-pss/dsa, has no secp256k1 curve and no chacha20-poly1305; async_hooks createHook is
   a stub with async ids always 0; cluster load-balancing of HTTP only works on Linux via SO_REUSEPORT.
   Attach each to the kind of service it breaks, not to a checklist.
6. The ownership paragraph, stated plainly: Anthropic acquired Bun on 2 December 2025, Claude Code
   ships as a Bun executable, and Bun's founder wrote that Bun made $0 in revenue at the time. Bun
   stays MIT. Name the check a platform team runs before standardising: not "is it fast" but "who
   pays for this binary's roadmap, and does their product depend on my runtime".
7. Verdict: a conditional winner whose condition is in the first clause. Bun for a service that is
   your own code plus I/O; Node for a repo that ships native addons, instruments with the inspector,
   or needs an EOL date it can put in a roadmap.""",

    "prisma-vs-drizzle": """The editorial angle: BOTH ORMS ARE FREE, AND EACH NOW ARRIVES WITH A DATABASE VENDOR ATTACHED.

The 2023 version of this comparison was generated client vs SQL builder. The 2026 version is a
supply-chain question: Prisma sells Prisma Postgres and Prisma Compute next to its free ORM, and in
March 2026 PlanetScale hired Drizzle's entire core team. Neither ORM has a seat price, so read this as
who ends up holding your data layer.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids. Prisma: the schema is a separate artefact
   compiled into a client, which is what lets Prisma own the query plan and now the runtime; Drizzle:
   the TypeScript file IS the schema, so there is nothing to generate and no engine to load.
2. What Prisma 7 forbids, with facts: `output` is now required on the generator so the client is no
   longer written into node_modules; the old `url` datasource style gives way to `prisma.config.ts`;
   and the query compiler runs on the JS main thread, which Prisma's own AMA says costs peak
   parallelism ("cases where throughput is similar or slightly worse").
3. What Drizzle forbids, with facts: no stable 1.0 — 1.0.0-rc.5 shipped 21 October 2026 and its notes
   carry a dozen-plus BREAKING changes; no Studio source (ORM and Kit are open source, Studio is not);
   and no neutral owner, because its sponsor hired the team.
4. The cold-start honesty beat, and the best part of the article. Prisma's claim is 90% smaller output
   and 3x faster queries, from a 14 MB (7 MB gzipped) Rust engine to a ~1.6 MB (600 KB gzipped)
   compiler. A third-party test published 6 November 2026 measured the opposite for cold start: about
   69 ms to first query on Prisma 6 vs about 236 ms on 7.10.1, and node_modules 254.1 MiB vs 333.3 MiB.
   Label both: vendor claim versus one developer's SQLite test.
5. Read Prisma Postgres as a penalty table: one query = one operation, Starter $10 with 1M included
   then $8/million, Pro $49 with 10M then $2/million, Business $129 with 50M then $1/million. Show the
   crossover: $10 + 8(n-1) = $49 at n = 5.875M operations, so the cheap plan stops being cheap below
   six million queries. Then note the retiring line item: the Accelerate cache ends 1 December 2026.
6. Drizzle's meter is not money at all: $0 for ORM, Kit, Studio for local development and Gateway. Say
   where the cost actually lands — you pay the database vendor directly, and that vendor now employs
   the maintainers.
7. Verdict: conditional winner with the condition in the first clause. Drizzle when you want no codegen
   and can pin a release candidate; Prisma when one bill for database plus runtime beats an RC branch,
   and your workload is many warm queries rather than many cold starts.""",

    "docker-vs-podman": """The editorial angle: DOCKER'S FREE TIER IS A HEADCOUNT TEST, NOT A USAGE TIER.

Docker Desktop is free until your company has 250 employees or $10 million in revenue — both limits
must hold — and then every commercial seat is paid at once. Government entities pay regardless. Podman
is Apache 2.0 with no seat at all. So the comparison is not daemon vs daemonless first; it is which
organisation is legally allowed to run the free thing.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids. Docker: the runtime is open source and the
   desktop is a licensed product, so the product is allowed to gate SSO, SCIM and hardened builds;
   Podman: the runtime has no daemon and the desktop has no licence, so there is nothing to gate and
   nothing to sell you at the moment you grow.
2. The cliff, with the arithmetic. 249 employees and $0 for Docker Desktop; 250 employees, or $10M
   revenue, and 200 developers x $15 = $3,000/month = $36,000/year with no change to the software.
   Show the plan ladder (Personal $0, Pro $9, Team $15, Business quote-only) and what is gated where:
   audit logs and RBAC at Team, SSO, SCIM, Hardened Docker Desktop and Image Access Management at
   Business. Note that Docker Engine and Moby licensing did not change — the desktop is the gate.
3. What Docker's money buys, factually: Build Cloud minutes allocated per plan that reset and do not
   accumulate, Testcontainers Cloud at $3 per 100 minutes prepaid or $4 per 100 on demand, Docker
   Hardened Images free for developers and "starting at $5k/repo" in production, Docker Offload
   licences on Team and Business. Attach each to a decision.
4. Podman's real bill is the port, and name it exactly. `podman system service` exposes a Docker v1.40
   compatibility layer plus a native Libpod API, socket-activated through systemd with a default
   5-second inactivity timeout, and `DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock` is the
   whole migration for CLI and Compose tooling. Then quote the man page's own warning: the API grants
   full access and allows arbitrary code execution as the user running it, with no ability to limit or
   audit that access — so the rootless story ends at a socket you must still protect.
5. The vendor-neutral argument and its limit: Podman Desktop is free, part of CNCF, Apache 2.0, with
   enterprise support sold by Red Hat as a build rather than a licence tier. Then say what that does
   not buy: no SOC 2 report, no SCIM provisioning, no image access policy, nobody to call.
6. Verdict: conditional winner with the buyer named in the first clause. Docker for a company already
   past the threshold that wants central control and CI minutes; Podman for a small team under the
   threshold, or a large one where per-seat x headcount is the line item it wants to delete and it can
   fund the port.""",

    "clerk-vs-auth0": """The editorial angle: BOTH VENDORS BILL PEOPLE, BUT THEY COUNT DIFFERENT PEOPLE.

Clerk bills Monthly Retained Users — a user who comes back at least one day after signing up — and
counts the first day free. Auth0 bills Monthly Active Users — anyone who authenticated this month — in
tiers where 501 users cost the same as 1,000. Every comparison you have read between them compared a
two different quantities, and the 140x gap at 50,000 users is what that mistake looks like.

Required beats, in this order:
1. Put the unit difference first, before any price. Define MRU and MAU from the vendors' own wording,
   and say plainly that a consumer app with heavy sign-up churn will look cheap on Clerk for reasons
   that are partly definitional.
2. Philosophy in one sentence each, then what each forbids. Clerk: authentication is a product surface,
   so it ships prebuilt UI, organisations and billing and prices retained attention; Auth0: identity
   is infrastructure, so it sells connections, tenants and actions and prices authenticated humans in
   tiers.
3. Auth0's tier structure as a penalty table. B2C Essentials $35 at 500 MAU, $70 at 1,000 — so the
   501st user costs $35 and the price is a step function, not a curve. B2C Professional runs $240 to
   $3,200 and then stops: at 30,000 MAU it becomes "contact us" and at 40,000 it is not available.
   At the top of the sheet, 50,000 B2C Essentials is $3,500/month. Note that yearly billing is 11x
   monthly, i.e. one month free.
4. Clerk's meter and where the bill hides. Pro is $25/month ($20 annual) with 50,000 MRU included per
   app then $0.02 each, and every application is unlimited on every plan. Then the add-on stack:
   $75/month per extra SSO connection, $75/month per Directory Sync connection starting 1 January 2027,
   the B2B add-on at $100/month with 100 MRO included then $1 each, and Protect at $0.002 per check
   after 10,000 free.
5. The honest head-to-head, with formulas and the caveat: 50,000 B2C users at Auth0 Essentials is
   $3,500/month; the same 50,000 MRU on Clerk Pro is $25/month because they are included. Show the
   multiplication and then say what the ratio is and is not. Then Clerk at 100,000 MRU = 50,000 x
   $0.02 + $25 = $1,025/month, against an Auth0 B2C price sheet that ends at 50,000.
6. Verdict: conditional winner with the condition in the first clause — consumer app where most
   sign-ups never return, or B2B where organisations and prebuilt UI are the product, goes to Clerk;
   an identity programme with enterprise SSO, many tenants and procurement goes to Auth0, after
   checking which side of the next tier boundary you sit on.""",

    "planetscale-vs-neon": """The editorial angle: ONE SELLS YOU A MACHINE, THE OTHER SELLS YOU AWAKE HOURS.

PlanetScale prices a dedicated cluster per branch, prorated to the millisecond, and never sleeps.
Neon prices CU-hours on Lakebase Postgres, suspends after five idle minutes, and charges nothing while
suspended. Both are Postgres now — PlanetScale has sold Postgres for over a year and shipped Neki,
sharded Postgres, into platform preview on 10 September 2026 — so the old "MySQL vs Postgres" framing
is dead. The question is what your workload does with the clock.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids. PlanetScale: capacity is a cluster you rent,
   so the invoice cannot move when traffic does and a branch is a second cluster; Neon: compute is
   CU-hours (compute size x hours running), so the invoice tracks the clock and an idle database is
   free. State the price of each philosophy: no free plan on PlanetScale, and a bill that grows with
   uptime on Neon.
2. The bottom of the market, with arithmetic. PlanetScale Postgres starts at $5/month single node and
   $15/month for a 3-node HA PS-5; Neon starts at $0 on a permanent Free plan with 100 CU-hours and
   1 GB. An always-on 0.25 CU database on Neon Launch is 0.25 x 730 = 182.5 CU-hours x $0.106 =
   $19.35/month before storage — more than PlanetScale's $15 HA cluster. Show that inversion clearly:
   the vendor that charges for idle is cheaper for idle, until you stop being idle.
3. The scale-up arithmetic: one full CU all month on Launch is 730 x $0.106 = $77.38, on Scale
   730 x $0.222 = $162.06, while PlanetScale's PS-80 HA cluster is $148/month flat. Use Neon's own
   typical-cost rows ($15 intermittent, $353 high load on Launch; $701 high load on Scale) against
   PlanetScale's SKU ladder as the two ways to answer the same question.
4. Branching, where the models diverge most. Neon: 10 branches included, $1.50 per extra branch-month,
   copy-on-write so a child branch starts at $0. PlanetScale: every branch is its own cluster, billed
   separately and prorated to the millisecond, so 20 PS-5 HA branches is 20 x $15 = $300/month. Say
   what that decides: preview environment per pull request is a Neon habit, not a PlanetScale one.
5. The 2026 twist, stated flatly: Neki is sharded Postgres in platform preview, with no single-node
   configuration, $30/month for a PS-10 arm64 shard (1 primary, 2 replicas across 3 AZs), routers from
   $6 and a production three-router baseline billed as rate x observed routers / 3. And PlanetScale
   hired Drizzle's entire core team in March 2026, so the ORM you write against is maintained by the
   database vendor you are evaluating.
6. Verdict: conditional winner with the condition in the first clause — nightly-idle dev and test with
   a branch per pull request goes to Neon; steady production that must not move with the clock, or a
   Vitess-shaped MySQL estate, goes to PlanetScale, and Neki is not a decision yet because it is a
   preview.""",
}

for slug, angle in ANGLES.items():
    prompt = CONTRACT.format(slug=slug, angle=angle)
    path = os.path.join(BASE, "content", "prompts", slug + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print("wrote", path, len(prompt), "chars")
