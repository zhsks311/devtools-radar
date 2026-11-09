You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/clerk-vs-auth0.md
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

The editorial angle: BOTH VENDORS BILL PEOPLE, BUT THEY COUNT DIFFERENT PEOPLE.

Clerk bills Monthly Retained Users — a user who comes back at least one day after signing up — and
counts the first day free. Auth0 bills Monthly Active Users — anyone who authenticated this month — in
tiers where 501 users cost the same as 1,000. Every comparison you have read between them compared a
two different quantities, and the 140x gap at 50,000 users is what that mistake looks like.

Required beats, in this order:
1. Put the unit difference first, before any price. Define MRU and MAU from the vendors' own wording,
   and say plainly that a consumer app with heavy sign-up churn will look cheap on Clerk for reasons
   that are partly definitional.
2. Philosophy in one sentence each, then what each forbids. Clerk: authentication is a product surface,
   so it ships prebuilt UI, organisations and billing and prices retained attention; Auth0: identity
   is infrastructure, so it sells connections, tenants and actions and prices authenticated humans in
   tiers.
3. Auth0's tier structure as a penalty table. B2C Essentials $35 at 500 MAU, $70 at 1,000 — so the
   501st user costs $35 and the price is a step function, not a curve. B2C Professional runs $240 to
   $3,200 and then stops: at 30,000 MAU it becomes "contact us" and at 40,000 it is not available.
   At the top of the sheet, 50,000 B2C Essentials is $3,500/month. Note that yearly billing is 11x
   monthly, i.e. one month free.
4. Clerk's meter and where the bill hides. Pro is $25/month ($20 annual) with 50,000 MRU included per
   app then $0.02 each, and every application is unlimited on every plan. Then the add-on stack:
   $75/month per extra SSO connection, $75/month per Directory Sync connection starting 1 January 2027,
   the B2B add-on at $100/month with 100 MRO included then $1 each, and Protect at $0.002 per check
   after 10,000 free.
5. The honest head-to-head, with formulas and the caveat: 50,000 B2C users at Auth0 Essentials is
   $3,500/month; the same 50,000 MRU on Clerk Pro is $25/month because they are included. Show the
   multiplication and then say what the ratio is and is not. Then Clerk at 100,000 MRU = 50,000 x
   $0.02 + $25 = $1,025/month, against an Auth0 B2C price sheet that ends at 50,000.
6. Verdict: conditional winner with the condition in the first clause — consumer app where most
   sign-ups never return, or B2B where organisations and prebuilt UI are the product, goes to Clerk;
   an identity programme with enterprise SSO, many tenants and procurement goes to Auth0, after
   checking which side of the next tier boundary you sit on.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/clerk-vs-auth0.json

with exactly these keys:

{
  "slug": "clerk-vs-auth0",
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
  python3 -c "import json;d=json.load(open('content/draft/clerk-vs-auth0.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
