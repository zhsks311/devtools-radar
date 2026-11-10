You are writing ONE article for DevTools Radar, an independent comparison site read by
working engineers. The article must read like it was written by an engineer who has operated these
systems, not by a content marketer.

STEP 1 — Read these files before writing anything:
  @content/facts/docker-vs-podman.md
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

The editorial angle: DOCKER'S FREE TIER IS A HEADCOUNT TEST, NOT A USAGE TIER.

Docker Desktop is free until your company has 250 employees or $10 million in revenue — both limits
must hold — and then every commercial seat is paid at once. Government entities pay regardless. Podman
is Apache 2.0 with no seat at all. So the comparison is not daemon vs daemonless first; it is which
organisation is legally allowed to run the free thing.

Required beats, in this order:
1. Philosophy in one sentence each, then what each forbids. Docker: the runtime is open source and the
   desktop is a licensed product, so the product is allowed to gate SSO, SCIM and hardened builds;
   Podman: the runtime has no daemon and the desktop has no licence, so there is nothing to gate and
   nothing to sell you at the moment you grow.
2. The cliff, with the arithmetic. 249 employees and $0 for Docker Desktop; 250 employees, or $10M
   revenue, and 200 developers x $15 = $3,000/month = $36,000/year with no change to the software.
   Show the plan ladder (Personal $0, Pro $9, Team $15, Business quote-only) and what is gated where:
   audit logs and RBAC at Team, SSO, SCIM, Hardened Docker Desktop and Image Access Management at
   Business. Note that Docker Engine and Moby licensing did not change — the desktop is the gate.
3. What Docker's money buys, factually: Build Cloud minutes allocated per plan that reset and do not
   accumulate, Testcontainers Cloud at $3 per 100 minutes prepaid or $4 per 100 on demand, Docker
   Hardened Images free for developers and "starting at $5k/repo" in production, Docker Offload
   licences on Team and Business. Attach each to a decision.
4. Podman's real bill is the port, and name it exactly. `podman system service` exposes a Docker v1.40
   compatibility layer plus a native Libpod API, socket-activated through systemd with a default
   5-second inactivity timeout, and `DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock` is the
   whole migration for CLI and Compose tooling. Then quote the man page's own warning: the API grants
   full access and allows arbitrary code execution as the user running it, with no ability to limit or
   audit that access — so the rootless story ends at a socket you must still protect.
5. The vendor-neutral argument and its limit: Podman Desktop is free, part of CNCF, Apache 2.0, with
   enterprise support sold by Red Hat as a build rather than a licence tier. Then say what that does
   not buy: no SOC 2 report, no SCIM provisioning, no image access policy, nobody to call.
6. Verdict: conditional winner with the buyer named in the first clause. Docker for a company already
   past the threshold that wants central control and CI minutes; Podman for a small team under the
   threshold, or a large one where per-seat x headcount is the line item it wants to delete and it can
   fund the port.

STEP 4 — Write valid JSON (UTF-8, no trailing commas, no comments) to exactly this path:
  content/draft/docker-vs-podman.json

with exactly these keys:

{
  "slug": "docker-vs-podman",
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
  python3 -c "import json;d=json.load(open('content/draft/docker-vs-podman.json'));print(len(''.join(s['content'] for s in d['sections'])), len(d['sections']), len(d['decision_matrix']), len(d['faqs']))"
The first number must be between 3200 and 4800. Also count sentences per paragraph in your own
draft and split anything over 4. Report the final numbers in one line when done.
