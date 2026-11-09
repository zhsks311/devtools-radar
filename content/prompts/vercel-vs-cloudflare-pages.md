You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/vercel-vs-cloudflare-pages.md
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

The editorial angle: THEY CONVERGED, AND THE BILL MOVED TO A DIFFERENT LINE.

Both platforms now meter CPU time instead of wall time — Vercel calls it Active CPU under Fluid
compute ($0.128/vCPU-hour, memory in GB-hours at under 10% of that rate), Cloudflare includes 30M
CPU-ms then $0.02 per million and charges nothing for egress. That convergence is the story: the
question is no longer "who is cheaper per function call", it is "which line item does my workload
inflate", and the answer is transfer and requests on Vercel, CPU milliseconds on Cloudflare.

Required beats, in this order:
1. Philosophy in one sentence each (Vercel: the framework vendor runs your framework; Cloudflare:
   the network vendor runs your requests) and what each forbids.
2. The convergence: explain both meters with the fact-sheet numbers, including that Vercel bills
   execution time not wall time so an idle await is free on both now.
3. The arithmetic table: 3 TB of transfer (Vercel 2,048 GB over x $0.15 = $307.20 vs $0), 50M
   requests (Vercel 40M over x $2/M = $80 vs Cloudflare 40M over x $0.30/M = $12 + $5 base), and
   CPU at ~$0.0356 per million CPU-ms on Vercel versus $0.02 on Cloudflare. Show each formula.
4. The non-price ceilings that decide real projects: Cloudflare Pages Free = 500 builds/month,
   20-minute build timeout, 20,000 files, 25 MiB per asset; Vercel Pro = 10M requests, 1 TB, a
    5-minute function limit. Pick the one that breaks a real deployment and say which.
5. Where the "free egress" claim costs you: building the app for the platform (Workers runtime,
   D1/R2 line items exist too, cache-hit design to keep CPU low — Cloudflare's own example shows
   100M requests at 80% cache hit costing $2.20 of CPU instead of $13.40).
6. Verdict: conditional winner, condition in the first clause. The condition is what the workload
   spends: bytes and seats, or CPU milliseconds and build minutes.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/vercel-vs-cloudflare-pages.json

with exactly these keys:

{
  "slug": "vercel-vs-cloudflare-pages",
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
  python3 -c "import json;d=json.load(open('content/draft/vercel-vs-cloudflare-pages.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
