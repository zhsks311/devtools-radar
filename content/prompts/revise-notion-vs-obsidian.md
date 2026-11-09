You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/notion-vs-obsidian.md
  @content/draft/notion-vs-obsidian.json
  @content/review/notion-vs-obsidian.md

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
1. Distinguish Notion Agent (included in Business, $20/member) from Custom Agents (metered, "Free to try,
   then $10 per 1,000 monthly Notion credits"). Never imply Custom Agents need Business.
2. Every annual figure stays tied to 10 people with its formula in the same sentence.
3. The Bases section keeps its specific version facts (Table and Cards in 1.9, List and Map in 1.10,
   Kanban in 1.14, Map needs the Maps plugin) and the .base view definition. It must also say plainly
   what Bases does not replace: permissions, server-side computed properties, multi-user editing.
4. The Friday-afternoon recovery framing is stronger than "history tax": make the reader test whether
   the version they need still exists under their plan.
5. Remove any unsupported claim about Notion exports converting perfectly, and any claim that plugins or
   scripts are an equivalent to a server-side agent.

Write the revised article to: content/final/notion-vs-obsidian.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/notion-vs-obsidian.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
