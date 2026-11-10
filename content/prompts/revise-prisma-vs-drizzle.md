You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/prisma-vs-drizzle.md
  @content/draft/prisma-vs-drizzle.json
  @content/review/prisma-vs-drizzle.md

Apply the REVISION BRIEF and the FACT / META / SLOP / LOGIC items. Rules for applying:
- META defects: always remove. The finished article must never mention the fact sheet, the brief,
  the review, "this comparison", "the table below shows", evidence labels, or a writing process.
- FACT defects: always fix when the review is right. EXCEPTION — do not delete these true, well-known
  product facts if the article uses them: Firestore is a NoSQL document store with no JOIN query;
  Supabase is hosted PostgreSQL with SQL/JOINs/ACID; Notion is a cloud workspace; Obsidian stores plain
  Markdown on disk. These may stay unsourced.
- Do not add any number, price, product name or feature that is not in the fact sheet. If a fix would
  need a number you do not have, rewrite the sentence without a number.
- Keep: hook 2 sentences; 5-6 sections; 3,200-4,800 characters of body; max 4 sentences per paragraph;
  a visual anchor (table, code, list, blockquote) at least every 300 characters; runnable code under
  20 lines; banned words (game-changer, seamless, robust, leverage, delve, landscape, realm, unlock,
  empower, "in conclusion", "it's worth noting") absent.
- Keep both sections that name who should NOT pick a product. Conditional verdict, no "it depends".

Edits I require on top of the review:
1. Keep both sides of the cold-start evidence in one paragraph: Prisma's own 90% / 3x claim and the
   third-party test (6.19.3 vs 7.10.1, SQLite, local machine, ~69 ms vs ~236 ms, 254.1 MiB vs
   333.3 MiB). Do not average them or drop one.
2. Keep the plan crossover with its formula visible: $10 + $8(n - 1) = $49 at n = 5.875M operations.
3. "PlanetScale hired the entire Drizzle core team" stays a hire, dated March 2026. Never write
   "acquired".
4. Keep the Accelerate retirement date, 1 December 2026 — a meter being switched off is a decision
   input.
5. If the review argues that Drizzle's 1.0.0-rc.5 status is "not a cost", keep it anyway: dependency
   risk is this article's second meter, and the rc.5 date is the evidence.
6. Do not introduce any fee for Prisma ORM or Drizzle ORM. Both are free; the money is in the database
   and runtime around them.

Write the revised article to: content/final/prisma-vs-drizzle.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/prisma-vs-drizzle.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
