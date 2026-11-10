You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/cursor-vs-github-copilot.md
  @content/draft/cursor-vs-github-copilot.json
  @content/review/cursor-vs-github-copilot.md

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
1. Rebuild cost_math with real arithmetic, not "subscription floor" phrasing:
   - 10 seats: Copilot Pro 10 × $10 = $100/month versus Cursor Teams 10 × $30 = $300/month.
   - One Claude-dependent developer: Cursor Premium $30/month plus third-party tokens billed at API list
     price (unbounded, so state it as "plus metered tokens") versus Copilot Pro+ $39/month with $70 of
     included credits.
   - Heavy user: Cursor Super $100 (15× Plus) versus Copilot Max $100 ($200 credits).
2. The penalty paragraph must state that Cursor's meter punishes third-party model use specifically,
   because those tokens are unbilled inside the subscription and pass through at list price, while
   Copilot's meter is a single credit pool per user.
3. Keep the SpaceX timeline; it is the article's spine. Make sure Grok 4.6 and the CursorBench figures
   are attributed to Cursor with "Cursor states".
4. Replace any "stay put" recommendation in the matrix with a real pick, since the hook says the old
   price point is gone. Awkward-case rows should still resolve.

Write the revised article to: content/final/cursor-vs-github-copilot.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/cursor-vs-github-copilot.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
