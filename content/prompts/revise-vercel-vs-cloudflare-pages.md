You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/vercel-vs-cloudflare-pages.md
  @content/draft/vercel-vs-cloudflare-pages.json
  @content/review/vercel-vs-cloudflare-pages.md

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

There is no separate review file for this article; the brief below is the review.
This draft's worst problem is that it sounds like a legal disclaimer instead of a teardown. Fix in this order:
1. Delete every meta sentence: "These are vendor-published rates verified on 2026-11-10, not benchmarks",
   "These are monthly line items at listed starting rates, not complete invoices", "the fact sheet does not
   establish", "in this comparison", "not a measured cache-hit promise". Keep exactly ONE evidence note,
   in the third paragraph after the hook, phrased as information for the reader.
2. Rewrite the first section so it opens with the two philosophies as concrete claims about who runs what:
   Vercel runs your framework, Cloudflare runs your requests. Then the single most useful consequence of
   each, in one sentence each. Drop the generic "compare the workload's bill, not its function count".
3. Section titles must be claims, not categories. Replace "The philosophy still constrains the app" and
   "Choose the bill your workload can control" with something a reader would argue with.
4. The hook's second sentence is flabby ("so the deciding bill moves to..."). Rewrite the hook around the
   concrete shift: both vendors now meter CPU time, so the line item that decides your invoice is transfer
   and requests on Vercel versus CPU milliseconds on Cloudflare. Keep it to two sentences.
5. Keep all the arithmetic and the 25 MiB / 20-minute / 500-build findings — they are the best part. Make
   sure each is attached to a decision, not just listed.
6. Verdict must name a buyer in the first clause of each sentence, not a condition stack.

Write the revised article to: content/final/vercel-vs-cloudflare-pages.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/vercel-vs-cloudflare-pages.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
