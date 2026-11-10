You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/cursor-vs-github-copilot.md
  @docs/tech-blog-writing-standard.md

The fact sheet is your ONLY source of numbers, prices, product names, feature claims and version
facts. If a number is not in the fact sheet, do not write a number. If a product name or tool is not
there, do not invent one. Do not add benchmarks. Do not add "typically" figures. Do not add prices
from memory — the market changed in 2026 and your memory is stale.

STEP 2 — Obey the writing standard (sections 3 through 7) exactly:
- First 3 lines = a hook of the "loss number", "counter-intuitive claim" or "disappeared thing" type.
  Banned openings: "In today's...", "It's important to note", "In this article we will", rhetorical
  questions, "X is very important".
- Before any comparison table, establish each product's philosophy in one sentence, then show what
  that philosophy forbids.
- Read every price table as a penalty table: name which usage pattern this vendor punishes and why.
- Every derived cost shows its formula (unit price x volume), never a bare total.
- Mark vendor claims as vendor claims ("Cloudflare's own example", "Cursor states").
- Sentences must vary in length. Max 4 sentences per paragraph. A visual anchor (table, code block,
  bullet list, blockquote) at least every 300 characters.
- Banned words: game-changer, seamless, robust, leverage, delve, landscape, realm, unlock, empower,
  "in conclusion", "it's worth noting", "when it comes to", "the world of".
- End with what the reader should check or decide today — not a summary of what they just read.
- Each section 600-1,100 characters. Total across sections 3,200-4,800 characters.
- 5 or 6 sections. Section titles are claims or questions, never bare nouns like "Pricing".
- No HTML. Markdown subset only: **bold**, `inline code`, - bullets, 1. numbered, ```fenced code```,
  | pipe tables |, > blockquote. Do NOT use ## headings inside section content (the builder adds the
  heading from the title).
- Code fences: runnable, under 20 lines, comments only explaining "why" or "here it breaks".

STEP 3 — Write the article:

The editorial angle: THE $20 AI EDITOR IS GONE. WHAT YOU ARE BUYING CHANGED.

This is the article's whole reason to exist. In 2026 Cursor is part of SpaceX: the partnership was
announced 21 April 2026 with a $10B payment and a $60B option, the all-stock deal was signed 16 June
2026 through X67 Inc., and it closed on 14 August 2026 with Cursor joining SpaceXAI to work on Grok,
Grok Build, Grok Bot and Cursor. Cursor's stated reason was compute. The pricing followed: $8 Plus
is Grok-only, $30 Premium is the first tier with third-party models and those are billed at API list
price on top, third-party usage is explicitly not included in the monthly price. Copilot went the
other way — $10 Pro with $15 of GitHub AI Credits, $39 Pro+, $100 Max, and one credit meter for
agent mode, code review, Copilot in the cloud, CLI and the app.

Required beats, in this order:
1. Open with the disappearance, not with a feature comparison. Then state what both products are
   now: agent-first, credit-metered, with a deliberately restricted entry tier.
2. Philosophy in one sentence each (Cursor: the model is the product, so the editor must own the
   model and the inference bill; GitHub: the repository is the product, so AI must land in review,
   PRs and issues) and what each forbids.
3. The penalty table: what does each meter punish? Cursor punishes heavy third-party model use
   (list price, unbundled) and rewards Grok loyalty; Copilot punishes breadth of agent use across
   seats and rewards keeping everything inside one vendor's surface.
4. The neutrality question, stated plainly: teams that chose Cursor partly to stay model-agnostic
   now buy from a company whose model is Grok; name the check a team should run before renewing.
5. The distribution counter-argument: Copilot's Free tier already runs agent mode and the CLI, so
   the free tier is not a demo — but PR review, file diff review, custom instructions and "assign
   work to Copilot and it creates a pull request" start at Pro.
6. Verdict: two different buyers, named in the first clause. Do not hedge into "both are great".

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/cursor-vs-github-copilot.json

with exactly these keys:

{
  "slug": "cursor-vs-github-copilot",
  "hook": "2 sentences, no more. The hook described above.",
  "sections": [ { "title": "...", "content": "markdown" } ],
  "decision_matrix": [ { "situation": "...", "pick": "...", "why": "one sentence" } ],
  "cost_math": [ { "label": "...", "formula": "...", "result": "..." } ],
  "verdict_summary": "2-3 sentences, must name a conditional winner. No 'it depends' ending.",
  "faqs": [ { "q": "...", "a": "..." } ],
  "sources": [ "https://..." ]
}

Rules for the structured fields:
- decision_matrix: 6-8 rows. "pick" is a product name or a short conditional ("Neither — stay put").
  Cover the awkward cases, not only the obvious ones.
- cost_math: 2-4 rows. formula must be readable arithmetic with real unit prices from the fact sheet.
- faqs: exactly 4. Each answer must add a fact NOT already stated in the sections, max 2 sentences.
- sources: 3-6 URLs taken from the fact sheet's source links.
- reading_time is NOT yours to write; the builder computes it.

STEP 5 — After writing the file, run this check and fix anything it reports:
  python3 -c "import json;d=json.load(open('content/draft/cursor-vs-github-copilot.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
