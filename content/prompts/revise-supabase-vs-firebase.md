You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/supabase-vs-firebase.md
  @content/draft/supabase-vs-firebase.json
  @content/review/supabase-vs-firebase.md

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
1. Section 1 says the pool tier "tops out" — false, the ladder continues. Use the full ladder from the
   fact sheet: pooled connections run 200 on $10 Micro to 12,000 on $3,730 16XL. Keep 5-6 rows in the
   compute table, ending with one high tier, and state that the ceiling is purchasable, not absolute.
2. Keep the derived $1,296/month figure but label it once as a gross read-charge model at the us-central1
   rate before free-quota adjustments. Do not repeat the label in every section.
3. Do not describe Supabase Realtime subscriber capacity — no figure exists for it. Its ceiling is the
   compute instance and its connection/pooler limits.
4. Keep the sentence that reads the price list as a penalty table, but rewrite the surrounding prose so
   it never says "read the price list as a penalty table" — show, don't announce.

Write the revised article to: content/final/supabase-vs-firebase.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/supabase-vs-firebase.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
