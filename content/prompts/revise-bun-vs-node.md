You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/bun-vs-node.md
  @content/draft/bun-vs-node.json
  @content/review/bun-vs-node.md

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
1. Keep the structural fact that both runtimes are MIT and neither has a paid tier. If the review asks
   for "the price", refuse in the text: there is no price, and the article is about the other two
   invoices.
2. Keep Bun's per-module pass counts attributed to Bun, and keep both headline gaps: node:http 12
   failing tests (415 - 403) and node:inspector 88 (110 - 22). They are the article's arithmetic.
3. Keep the Vite dev server memory line where Bun loses (233 MB vs 214 MB). Dropping the one row the
   vendor loses would make the piece read as a press release.
4. Node's TypeScript section must keep both limits that surprise people: the parser needs WebAssembly
   (ERR_WEBASSEMBLY_NOT_SUPPORTED otherwise) and TypeScript inside node_modules is refused.
5. Do not speculate about Anthropic's motives, "enshittification", or what the acquisition "really"
   means. State the date, that Claude Code ships as a Bun executable, that Bun stays MIT-licensed, and
   let the reader run the check.
6. Verdict: the first clause names the buyer, not a condition stack.

Write the revised article to: content/final/bun-vs-node.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/bun-vs-node.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
