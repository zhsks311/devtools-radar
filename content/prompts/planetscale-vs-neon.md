You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/planetscale-vs-neon.md
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

The editorial angle: ONE SELLS YOU A MACHINE, THE OTHER SELLS YOU AWAKE HOURS.

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
   preview.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/planetscale-vs-neon.json

with exactly these keys:

{
  "slug": "planetscale-vs-neon",
  "hook": "2 sentences, no more. The hook described above.",
  "sections": [ { "title": "...", "content": "markdown" } ],
  "decision_matrix": [ { "situation": "...", "pick": "...", "why": "one sentence" } ],
  "cost_math": [ { "label": "...", "formula": "...", "result": "..." } ],
  "verdict_summary": "2-3 sentences, must name a conditional winner. No 'it depends' ending.",
  "faqs": [ { "q": "...", "a": "..." } ],
  "sources": [ "https://..." ]
}

Rules for the structured fields:
- decision_matrix: 6-8 rows. "pick" is a product name or a short conditional ("Neither — stay put").
  Cover the awkward cases, not only the obvious ones.
- cost_math: 2-4 rows. formula must be readable arithmetic with real unit prices from the fact sheet.
- faqs: exactly 4. Each answer must add a fact NOT already stated in the sections, max 2 sentences.
- sources: 3-6 URLs taken from the fact sheet's source links.
- reading_time is NOT yours to write; the builder computes it.

STEP 5 — After writing the file, run this check and fix anything it reports:
  python3 -c "import json;d=json.load(open('content/draft/planetscale-vs-neon.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
