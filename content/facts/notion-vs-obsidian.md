# FACT SHEET — Notion vs Obsidian (verified 2026-11-10)

Rules: use ONLY facts from this sheet. No invented benchmarks, no invented API endpoints, no plugin counts.

## Notion (source: https://www.notion.com/pricing)
- Free — $0/member: databases incl. subtasks, dependencies, custom properties; basic forms; basic sites;
  Notion Calendar; file uploads **up to 5 MB**; page history **7 days**; **10 external guests**;
  1 notion.site domain; Notion AI trial only
- Plus — $10/member/month: file uploads up to 5 GB, page history 30 days, custom forms and sites, charts,
  collaborative blocks, basic connections, Notion AI trial only
- Business — $20/member/month: **Notion Agent**, **AI Meeting Notes**, Enterprise Search (beta), SAML SSO,
  granular database permissions, private teamspaces, page history 90 days
- Enterprise — custom: zero data retention with LLM providers, SCIM, audit log, security/compliance
  connections (DLP, SIEM)
- **Custom Agents — "Free to try, then $10 per 1,000 monthly Notion credits"**; agents handle repetitive
  tasks autonomously
- **Workers (beta)** — "Extend Notion with custom code to build agent tools, sync external data, and
  trigger Notion workflows from anywhere"
- Page history detail: only Business gets 90 days; Free is 7 days — this is the silent tax on version
  history.

## Notion API (source: https://developers.notion.com/reference/request-limits)
- Per-connection limit: **180 requests per 60-second window (average 3/second)** on all plans except
  Business/Enterprise, which get **600 per minute (average 10/second)**. The budget can be spent as a burst.
- A separate **per-workspace** budget is shared across all connections and scaled by plan; `Retry-After`
  for it can exceed a minute.
- Querying a data source has its own limit of about 3 requests/second per connection.
- Failures are HTTP 429 (or 529 for `service_overload`) with a `Retry-After` header you must obey; the JS
  SDK retries for you.
- A Free-plan workspace block limit takes effect 2026-09-08 (mentioned by Notion; do not detail it).

## Obsidian (source: https://obsidian.md/pricing)
- **Free without limits. No sign-up required.** No telemetry, no data collection; "we never sell user data";
  data stored locally on the device, "making it inaccessible to us".
- Sync — **$4/user/month billed annually**: sync across devices, AES-256 end-to-end encryption, version
  history, shared vaults, priority support
- Publish — **$8/site/month billed annually**
- Catalyst — $25 one-time: early access to beta versions, badges, exclusive channels
- Commercial license — $50/user/year, and it is explicitly **optional**: "You are not required to pay for a
  commercial license", encouraged if used at work
- 7-day no-questions refund on Sync and Publish; Catalyst/Commercial/Obsidian Credit non-refundable
- 40% education/nonprofit discount on Sync and Publish

## Obsidian Bases (source: https://obsidian.md/help/bases, https://obsidian.md/help/bases/views)
- Bases is a **core plugin** (no community plugin needed) that creates database-like views of notes.
- Data stays in local Markdown files and their frontmatter properties; the `.base` file holds only the view
  definition (filters, formulas, properties, views) — "Delete a base and your notes are untouched."
- View types and the app version that introduced them: Table (1.9), Cards (1.9), List (1.10),
  Map (1.10, needs the Maps plugin), **Kanban (1.14)**. Community plugins can add more layouts.
- `.base` syntax is YAML: `filters` (and / or / not, `file.hasTag()`, `file.inFolder()`, `file.hasLink()`),
  `formulas` (e.g. `'(price / age).toFixed(2)'`), `properties`, `views[]` with `type`, `limit`, `groupBy`
  (property + direction), `order`, `summaries`.
- Bases embeds in Markdown: a `.base` file or a `base` code block inside a note.

## Derived arithmetic you may use (show the formula)
- A 10-person team: Notion Business 10 × $20 = $200/month = $2,400/year. Notion Plus 10 × $10 = $100/month.
- Same 10 people on Obsidian: app $0, Sync 10 × $4 × 12 = $480/year; commercial licence optional
  10 × $50 = $500/year; total worst case $980/year, and $0 if they use git/iCloud instead of Sync.
- So the honest framing is not "Notion expensive vs Obsidian free". Notion sells a server, an agent and a
  permission model; Obsidian sells a folder and an optional pipe. Those are different bills for different
  failure modes.

## The trade-off the article must make explicit
- Notion: shared state, permissions, agents, automations — and a metered API (180/min), page-history tiers,
  block limits on Free, and a vendor that now sells agent credits on top.
- Obsidian: local truth, unlimited history by virtue of plain files + git, zero metering — and no
  permissions model, no server-side agent, no built-in multi-user editing; collaboration arrives only
  through Sync shared vaults or third-party tooling.

## Do not claim
- Do not state a community-plugin count.
- Do not invent Notion block limits, prices per credit, or an Obsidian "official API".
- Do not claim Obsidian Sync costs $4 for teams of any size — it is per user per month billed annually.
