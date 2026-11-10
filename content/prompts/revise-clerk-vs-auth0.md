You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/clerk-vs-auth0.md
  @content/draft/clerk-vs-auth0.json
  @content/review/clerk-vs-auth0.md

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
1. The MRU-versus-MAU caveat must sit in the same paragraph as any ratio between the two vendors. If
   the review calls the 140x comparison misleading, fix it by keeping the caveat sentence, not by
   deleting the comparison.
2. Sources: the fact sheet lists exactly two URLs, the two vendor pricing pages. Two sources is
   acceptable here; do not invent a third.
3. Keep the step-function fact (501 B2C users on Essentials bills at $70, double the $35 for 500) and
   the fact that the printed Professional sheet ends at 20,000 MAU for B2C and at 10,000 for B2B.
4. Do not add product capabilities the fact sheet does not carry — no MFA factor lists, no "Actions",
   no compliance certifications beyond SOC 2 on Business and HIPAA on Enterprise. If the philosophy
   sentence says Auth0 sells connections, tenants and rules, either keep the word "rules" out or cut
   it; do not introduce "actions" as a named product.
5. Keep the small code block that prints 501 / 70, 50,000 / 3,500 / 25 and 100,000 / 1,025. It is the
   arithmetic evidence for the whole article.

Write the revised article to: content/final/clerk-vs-auth0.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/clerk-vs-auth0.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
