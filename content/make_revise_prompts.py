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
    "bun-vs-node": """Edits I require on top of the review:
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
6. Verdict: the first clause names the buyer, not a condition stack.""",

    "prisma-vs-drizzle": """Edits I require on top of the review:
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
   and runtime around them.""",

    "docker-vs-podman": """Edits I require on top of the review:
1. Never print a Docker Business per-seat price. The pricing page says "Contact us for pricing"; if the
   review demands a number, the answer is that none is published, and the article says so.
2. The free-use test is an AND: fewer than 250 employees AND less than $10 million annual revenue, and
   government entities pay regardless. Do not let it become an OR in either direction.
3. Keep the `podman system service` man-page warning as a direct quotation, in quotation marks: the API
   "allows arbitrary code execution as the user running the API, with no ability to limit or audit this
   access". It is the strongest fact in the piece.
4. Do not add a 25-seat minimum, a reseller price, or any Docker Business figure: none is on the
   vendor's page.
5. Do not assert that Podman "has no SOC 2 report" or "lacks SCIM" as a fact about the project. Say
   instead that Docker Business includes SOC 2, SSO and SCIM, and that Podman's own pages sell no
   central admin controls — support arrives as a Red Hat build.
6. Keep the arithmetic that shows the cliff (200 developers x $15 = $3,000/month) and the Podman
   counter-bill ($0 in licence fees plus the port).""",

    "clerk-vs-auth0": """Edits I require on top of the review:
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
   arithmetic evidence for the whole article.""",

    "planetscale-vs-neon": """Edits I require on top of the review:
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
   only 2026 PlanetScale story this piece needs.""",

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
