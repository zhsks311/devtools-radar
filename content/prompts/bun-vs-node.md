You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/bun-vs-node.md
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

The editorial angle: NEITHER RUNTIME HAS A PRICE, SO THE BILL IS PAID IN SOMETHING ELSE.

Bun is MIT, Node is MIT, and neither has a paid tier. That is exactly why this comparison is worth
writing: with money out of the picture, the real meters are the release calendar, the compatibility
surface, and the native-module ABI. Node bills you on someone else's schedule. Bun bills you on the
tests it does not pass yet.

Required beats, in this order:
1. Open by taking the price question off the table: both runtimes are free and MIT-licensed, so the
   invoice is labour. Then the philosophy in one sentence each (Node: a standards body ships a
   runtime on a published clock; Bun: one binary ships the whole toolkit) and what each forbids.
2. Node's meter is the calendar. Show the table: v27 Alpha 29 Oct 2026, v26 Lithium LTS from 5 May
   2026, v25 EOL 31 Mar 2026, v24 Krypton LTS from 6 May 2025, v22 Jod LTS from 24 Apr 2024, v20 Iron
   EOL 24 Mar 2026. State the two rules that decide upgrades: LTS typically guarantees fixes for a
   total of 30 months, and starting with v27 every major gets six months of Alpha, six of Current,
   then LTS. This is a runtime you keep for years and must move on a date you did not choose.
3. Node's 2026 own goal and its limit: TypeScript type stripping is on by default and stable
   (stable at v25.2.0/v24.12.0), but it is only erasure. `enum`, `namespace` with runtime code,
   parameter properties and import aliases throw ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX, `.tsx` is
   unsupported, `tsconfig.json` is ignored so `paths` do not work, TypeScript inside node_modules is
   refused, and the parser needs WebAssembly. Show a four-line code block that works on Node 26 and
   the enum that does not.
4. Bun's meter is the failing 3%. Use Bun's own per-module pass counts: node:http 403/415,
   node:inspector 22/110, node:module 68/93, node:test_runner 28/81, node:fs 349/358, node:sqlite
   18/18. State the 1,517 newly passing tests in 1.4 as progress, then state the ABI tax: the Node
   compatibility target moved from 24.3.0 to 26.3.0, `NODE_MODULE_VERSION` is now 147, and native
   addons built for 24 must be rebuilt.
5. The gaps that decide real services, named from Bun's own compatibility docs: `http.Server` does not
   extend `net.Server` and the keepAlive options are no-ops; node:https is missing
   getPeerCertificate() and getCipher() and does not support SNICallback; node:crypto lacks
   ed448/x448/rsa-pss/dsa, has no secp256k1 curve and no chacha20-poly1305; async_hooks createHook is
   a stub with async ids always 0; cluster load-balancing of HTTP only works on Linux via SO_REUSEPORT.
   Attach each to the kind of service it breaks, not to a checklist.
6. The ownership paragraph, stated plainly: Anthropic acquired Bun on 2 December 2025, Claude Code
   ships as a Bun executable, and Bun's founder wrote that Bun made $0 in revenue at the time. Bun
   stays MIT. Name the check a platform team runs before standardising: not "is it fast" but "who
   pays for this binary's roadmap, and does their product depend on my runtime".
7. Verdict: a conditional winner whose condition is in the first clause. Bun for a service that is
   your own code plus I/O; Node for a repo that ships native addons, instruments with the inspector,
   or needs an EOL date it can put in a roadmap.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/bun-vs-node.json

with exactly these keys:

{
  "slug": "bun-vs-node",
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
  python3 -c "import json;d=json.load(open('content/draft/bun-vs-node.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
