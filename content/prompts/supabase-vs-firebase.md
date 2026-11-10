You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/supabase-vs-firebase.md
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

The editorial angle: THE BILLING UNIT IS THE ARCHITECTURE.

The 2024 version of this comparison was "Postgres vs NoSQL". The 2026 version is harder and more
useful: Supabase sells compute (a machine, a disk, a connection ceiling) and Firebase sells events
(document reads, writes, index entry reads, and a read per change on every live listener). Those two
meters punish different code. Supabase punishes connections and disk; Firestore punishes watching.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids (JOINs absent on Firestore; a hard
   connection ceiling of 60 direct / 200 pooled on Supabase's $10 Micro and no way to buy an
   infinite pool).
2. The Firestore realtime trap, with the arithmetic from the fact sheet: a 50-user dashboard
   watching 100 documents that change 20 times a minute is ~4.32B read events/month, about
   $1,296/month, while the same shape on Supabase Pro is a flat $25. Show the multiplication.
   Also note reconnects are billed like new queries.
3. The counter-trap: on Supabase, a Postgres Changes subscription is a database event stream that
   you opt into per table (alter publication ... add table), and the ceiling you hit is the
   connection/pooler ceiling and the compute tier, not a per-read meter. Say plainly that this
   swaps a metered risk for a capacity risk.
4. Index entry reads on Firestore — the line item nobody quotes: 1 read per 1,000 index entries,
   a second range field starts billing, count() bills index reads.
5. The migration section must be honest: firebase-to-supabase copies one collection to one table,
   flattens to text/numeric/boolean/jsonb, you write the hooks that split nested data, and the
   password path needs a middleware the repo itself marks work in progress.
6. Verdict: a conditional winner with the deciding condition named in the first clause.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/supabase-vs-firebase.json

with exactly these keys:

{
  "slug": "supabase-vs-firebase",
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
  python3 -c "import json;d=json.load(open('content/draft/supabase-vs-firebase.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
