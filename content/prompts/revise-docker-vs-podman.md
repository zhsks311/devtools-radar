You are revising one DevTools Radar article after fact-check review. You are not starting over:
keep every sentence that survived review.

Read:
  @content/facts/docker-vs-podman.md
  @content/draft/docker-vs-podman.json
  @content/review/docker-vs-podman.md

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
   counter-bill ($0 in licence fees plus the port).

Write the revised article to: content/final/docker-vs-podman.json  (same keys as the draft; do not change the schema)
Then verify with:
  python3 -c "import json;d=json.load(open('content/final/docker-vs-podman.json'));print(len(''.join(s['content'] for s in d['sections'])))"
That number must be 3,200-4,800. Report it, plus a 3-line summary of what you changed and what you
deliberately did not change.
