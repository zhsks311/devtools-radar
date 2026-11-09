#!/usr/bin/env python3
"""Revision prompt: the reviser implements the review without adding facts."""

import os

BASE = "/workspace/devtools-radar"
OUT = os.path.join(BASE, "content", "prompts")

TEMPLATE = """You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/{slug}.md
  @content/draft/{slug}.json
  @content/review/{slug}.md

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

{extra}

Write the revised article to: content/final/{slug}.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/{slug}.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
"""

EXTRA = {
    "supabase-vs-firebase": """Edits I require on top of the review:
1. Section 1 says the pool tier "tops out" — false, the ladder continues. Use the full ladder from the
   fact sheet: pooled connections run 200 on $10 Micro to 12,000 on $3,730 16XL. Keep 5-6 rows in the
   compute table, ending with one high tier, and state that the ceiling is purchasable, not absolute.
2. Keep the derived $1,296/month figure but label it once as a gross read-charge model at the us-central1
   rate before free-quota adjustments. Do not repeat the label in every section.
3. Do not describe Supabase Realtime subscriber capacity — no figure exists for it. Its ceiling is the
   compute instance and its connection/pooler limits.
4. Keep the sentence that reads the price list as a penalty table, but rewrite the surrounding prose so
   it never says "read the price list as a penalty table" — show, don't announce.""",

    "vercel-vs-cloudflare-pages": """There is no separate review file for this article; the brief below is the review.
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
6. Verdict must name a buyer in the first clause of each sentence, not a condition stack.""",

    "cursor-vs-github-copilot": """Edits I require on top of the review:
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
   price point is gone. Awkward-case rows should still resolve.""",

    "notion-vs-obsidian": """Edits I require on top of the review:
1. Distinguish Notion Agent (included in Business, $20/member) from Custom Agents (metered, "Free to try,
   then $10 per 1,000 monthly Notion credits"). Never imply Custom Agents need Business.
2. Every annual figure stays tied to 10 people with its formula in the same sentence.
3. The Bases section keeps its specific version facts (Table and Cards in 1.9, List and Map in 1.10,
   Kanban in 1.14, Map needs the Maps plugin) and the .base view definition. It must also say plainly
   what Bases does not replace: permissions, server-side computed properties, multi-user editing.
4. The Friday-afternoon recovery framing is stronger than "history tax": make the reader test whether
   the version they need still exists under their plan.
5. Remove any unsupported claim about Notion exports converting perfectly, and any claim that plugins or
   scripts are an equivalent to a server-side agent.""",
}

for slug, extra in EXTRA.items():
    prompt = TEMPLATE.format(slug=slug, extra=extra)
    with open(os.path.join(OUT, "revise-" + slug + ".md"), "w", encoding="utf-8") as f:
        f.write(prompt)
print("ok")
