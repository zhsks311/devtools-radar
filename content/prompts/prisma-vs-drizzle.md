You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/prisma-vs-drizzle.md
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

The editorial angle: BOTH ORMS ARE FREE, AND EACH NOW ARRIVES WITH A DATABASE VENDOR ATTACHED.

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
   and your workload is many warm queries rather than many cold starts.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/prisma-vs-drizzle.json

with exactly these keys:

{
  "slug": "prisma-vs-drizzle",
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
  python3 -c "import json;d=json.load(open('content/draft/prisma-vs-drizzle.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
