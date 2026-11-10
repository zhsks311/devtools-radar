# FACT SHEET — Cursor vs GitHub Copilot (verified 2026-11-10)

Rules: use ONLY facts from this sheet. This market changed hands in 2026; the article's whole point is that
the 2024–2025 advice is stale. Do not invent benchmark scores beyond the two figures below, and label them
as Cursor's own numbers.

## Cursor — corporate reality in 2026 (sources below)
- Apr 21, 2026: SpaceX and Cursor announce a partnership to "create the best coding and knowledge-work AI",
  including a $10B payment from SpaceXAI to Cursor and an option to acquire for $60B.
- Jun 16, 2026: SpaceX signs a binding all-stock deal to buy Anysphere (Cursor's company) at a $60B
  valuation; subsidiary X67 Inc. merges into Cursor, which survives as a wholly owned subsidiary.
- Aug 14, 2026: Cursor's blog post "Cursor is now a part of SpaceX" — acquisition complete. Cursor joins
  the SpaceXAI team (SpaceX absorbed xAI in February 2026) to improve Grok, Grok Build, Grok Bot,
  Grok API and Cursor. Cursor's reasons: compute. "We've wanted to push our training efforts much
  further, but we've been bottlenecked by compute."
- Cursor revenue stated to Reuters: ~$2.6B annualised. Founded 2022, CEO Michael Truell.
- Cursor models: Composer (first agentic coding model), Composer 1.5 "scaled reinforcement learning by over
  20x", Composer 2 "added continued pretraining". Grok 4.6 released the Wednesday before Aug 14, 2026 and
  is the first joint model: Cursor states scores between 69.9% and 70.8% on CursorBench and 61 on the
  Artificial Analysis Intelligence Index (as reported by AI/TLDR). Label these as Cursor's claims.
- Sources: https://cursor.com/blog/joining-spacex · https://9to5mac.com/2026/08/14/... ·
  https://thenextweb.com/news/spacex-cursor-acquisition-official-60-billion

## Cursor pricing (source: https://cursor.com/pricing)
- Free — $0, limited agent and chat requests
- Plus — $8/month: shared AI usage pool, "**Only Grok models are available on this plan**"
- Premium — $30/month, "most popular": 4× the usage of Plus, latest Grok models, cloud agents &
  automations, code hosting via Origin, AI code reviews via Bugbot, "third-party models at API list price"
  (billed separately), Grok Bot
- Super — $100/month: 15× Plus, priority model access at peak times
- Ultra — $200/month: 50× Plus, earliest access to all products and models
- Teams — $30+/user/month; Enterprise — custom
- Third-party (non-Grok) model usage in Cursor "is not included in the monthly prices shown and must be
  purchased separately" — i.e. Claude/GPT usage is metered at API list price on top of the subscription.
⇒ Derived: the tiers that used to be "$20 all-you-can-eat" no longer exist. $8 is Grok-only; $30 is the
first tier with third-party models, and those are pay-per-token on top.

## GitHub Copilot pricing (source: https://github.com/features/copilot/plans)
- Free — $0: limited chat and agent usage; CLI and agent mode supported
- Pro — $10/user/month: $15/month total GitHub AI Credits ($10 base + $5 flex allotment)
- Pro+ — $39/user/month: $70/month total credits, premium models including Opus, audit logs
- Max — $100/user/month: $200/month total credits
- Billing unit is now **GitHub AI Credits**: consumed by agent mode, code review, Copilot in the cloud,
  Copilot CLI and the Copilot app; extra credits purchasable on Pro and above
- Feature gates: PR reviews, file diff reviews, custom instructions (.instructions.md), Copilot in the
  cloud, "assign work to Copilot and it creates a pull request" — **Pro and above, not Free**
- Panels: prose explanation, Free is not "no agent"; Free gets agent mode and CLI, it lacks PR review,
  code review, cloud assignment and custom instructions.
- Supported surfaces: VS Code, Visual Studio, JetBrains, Xcode, Eclipse, Neovim, Raycast, Zed, SQL Server
  Management Studio, github.com and GitHub Mobile.

## Market context you may reference qualitatively
- Agentic coding CLI competitors named in the SpaceX coverage: Anthropic's Claude Code and OpenAI's Codex.
- Do not state their prices (not verified here).

## What the comparison must argue (this is the 2026-shaped thesis)
1. The axis moved from "single-file completion vs multi-file agent" to "who owns the model and who meters
   the tokens". Both products are now agent-first; both bill through metered credits; both have a cheap
   entry tier that is deliberately model-restricted or feature-restricted.
2. Cursor's neutrality ended with the acquisition: default routing to Grok is now a real risk for teams
   that picked Cursor partly to stay model-agnostic.
3. Copilot's distribution is the counter-argument: the editor you already have, the PR surface you already
   pay for, one vendor for identity + code + review.
4. Spend behaviour differs: Copilot sells a credit balance inside GitHub; Cursor sells Grok-heavy tiers and
   passes third-party tokens through at list price.

## Do not claim
- Do not cite the old $20 Pro / $10 all-inclusive numbers as current.
- Do not state CursorBench methodology you were not given.
- Do not claim Copilot Free includes PR review or custom instructions.
