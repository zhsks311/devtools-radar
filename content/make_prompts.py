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
}

for slug, angle in ANGLES.items():
    prompt = CONTRACT.format(slug=slug, angle=angle)
    path = os.path.join(BASE, "content", "prompts", slug + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print("wrote", path, len(prompt), "chars")
