You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/planetscale-vs-neon.md
  @content/draft/planetscale-vs-neon.json
  @content/review/planetscale-vs-neon.md

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
1. Keep the always-on inversion: 0.25 CU x 730 h = 182.5 CU-hours x $0.106 = $19.35/month on Neon
   Launch against $15/month for a PlanetScale PS-5 HA cluster. It is the spine of the piece.
2. Do not use the 1 TB egress example. If egress appears at all, it is 1,024 - 500 = 524 GB x $0.10 =
   $52.40/month, and PlanetScale's rate is region-dependent and not printed.
3. Neki is a platform preview, not production. Keep that sentence next to any Neki number, and keep
   the router formula (production router compute = router rate x observed routers / 3).
4. Keep the branch-cost contrast: 20 branches on Neon Launch = 10 included + 10 x $1.50 = $15/month,
   against 20 PS-5 HA branches on PlanetScale = 20 x $15 = $300/month prorated to the millisecond.
5. Neon "from Databricks" is the pricing page's own phrase. Do not add an acquisition date or a
   purchase price.
6. Drop the Drizzle core-team hire from this article. It is true and verified, but this sheet does not
   source it; the Prisma vs Drizzle page carries it with its own source. Neki's preview status is the
   only 2026 PlanetScale story this piece needs.

Write the revised article to: content/final/planetscale-vs-neon.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/planetscale-vs-neon.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
