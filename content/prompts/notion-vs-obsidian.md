You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/notion-vs-obsidian.md
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

The editorial angle: ONE SELLS A SERVER WITH A METER, THE OTHER SELLS A FOLDER WITH A PIPE.

The naive comparison is free vs $10. The real one: Notion sells shared state — permissions,
databases, an agent, automations — and meters everything around it (180 API requests/minute per
connection on all plans except Business/Enterprise's 600, 7-day page history on Free, 5 MB uploads,
10 guests, Custom Agents at $10 per 1,000 Notion credits, Workers in beta). Obsidian sells nothing
and meters nothing: the app is free without limits, no telemetry, data local, and the optional
pieces are Sync at $4/user/month and Publish at $8/site/month, with the commercial licence
explicitly not required.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids (Obsidian has no server-side permission
   model and no built-in agent; Notion has no plain-file truth, so your export is a conversion, and
   your history is a plan feature).
2. The history/upload tiers as the hidden tax — 7 days on Free, 30 on Plus, 90 on Business. This is
   the most under-reported constraint and it decides whether Notion can be a system of record.
3. Bases: Obsidian shipped a core plugin that makes database views over frontmatter — Table and
   Cards in 1.9, List and Map in 1.10, Kanban in 1.14 — stored as a .base YAML file that holds only
   the view definition. This is the moment "Notion has databases, Obsidian has notes" stopped being
   true. Say what Bases still does not give you (permissions, server-side computed properties,
   multi-user edit).
4. The agent argument, factually: Notion's agents live in Business at $20/member and Custom Agents
   are metered at $10 per 1,000 credits; Obsidian's equivalent is you, a script, or a plugin. Then
   the honest counter: an API at 180 requests/minute is a queue you have to build, and every
   integration is a vendor relationship.
5. The real math: a 10-person team on Notion Business is $200/month = $2,400/year; the same team on
   Obsidian with Sync is $480/year on Sync plus an optional $500/year in commercial licences.
   Then say what the extra $1,900 buys and who should not pay it.
6. Verdict: conditional winner with the condition in the first clause — decide by whether the notes
   are shared state or private thinking.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/notion-vs-obsidian.json

with exactly these keys:

{
  "slug": "notion-vs-obsidian",
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
  python3 -c "import json;d=json.load(open('content/draft/notion-vs-obsidian.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
