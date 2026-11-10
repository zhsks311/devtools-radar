# Notion vs Obsidian — defect review

1. **LOGIC — `decision_matrix[2].why`: conflates Notion Agent with Custom Agents.**
   > Notion Agent ships on Business and Custom Agents run server-side, metered at $10 per 1,000 credits.

   Business includes Notion Agent; the sheet separately prices Custom Agents and does not establish that Business is required for them (facts: 11–16). The row's repetitive-task requirement does not justify its plan recommendation.

   Replacement: “Choose Business if you need its included Notion Agent; price autonomous repetitive tasks separately with Custom Agents, which are free to try, then $10 per 1,000 monthly Notion credits.”

2. **LOGIC — `decision_matrix[5].pick`: recommends an unverified guest capacity.**
   > Neither Free tier — pay for Notion

   The sheet gives Free's 10-external-guest cap but no paid-plan guest allowance; it also does not call Obsidian a Free tier (facts: 6–12, 32–40).

   Replacement: “Notion Free's 10-external-guest cap rules it out; do not choose a paid plan until its guest capacity meets your client requirement.”

3. **LOGIC — `decision_matrix[6].why`: view layouts do not establish database equivalence.**
   > Table, Cards, List, Map and Kanban views over frontmatter cover the database use case without a server.

   Bases provides database-like views, not a demonstrated substitute for every database workflow; Map also requires the Maps plugin (facts: 44–53). The situation does not establish that the team only needs views.

   Replacement: “Choose Bases if the requirement is views over local Markdown properties rather than shared editing or permissions; Map additionally requires the Maps plugin.”

4. **LOGIC — `decision_matrix[4].why`: edit frequency does not determine recovery needs.**
   > A 7-day page history cannot be a system of record for documents edited rarely.

   A rarely edited document need not require an older version; Plus's 30 days is not automatically sufficient either (facts: 7–12).

   Replacement: “Choose Plus only if 30 days of recovery is enough, Business if you need 90 days, or plain files under git if you need history without a plan-imposed cutoff.”

5. **LOGIC — `decision_matrix[3].why`: the stated bottleneck does not establish that Business fixes it.**
   > Below Business each connection gets 180 requests/minute and all connections share one workspace budget.

   Business raises the connection allowance, but the separate workspace budget remains and data-source queries retain their own limit (facts: 23–29).

   Replacement: “Business raises the per-connection allowance from 180 to 600 requests per minute, but a separate plan-scaled workspace budget and the roughly 3-per-second data-source query limit still constrain the pipeline.”

6. **LOGIC — `faqs[3].a`: retention is not transmission.**
   > Zero data retention with LLM providers is listed as an Enterprise feature, alongside SCIM and audit log.

   This does not answer whether workspace content is sent to providers; the sheet establishes only the Enterprise retention feature (facts: 13–14). Change the question to ask which plan lists zero data retention.

   Replacement: “Notion Enterprise lists zero data retention with LLM providers; that retention policy does not establish whether workspace content is sent to them.”

7. **LOGIC — section 5: the zero-cost conclusion drops the optional licence assumption.**
   > Replace Sync with git or iCloud and their bill is $0.

   Removing Sync leaves the optional $500/year licence payment in the preceding calculation unless the team declines it (facts: 39–40, 57–58).

   Replacement: “For 10 people using git or iCloud instead of Sync, the app costs $0; choosing the optional commercial licences adds 10 × $50 = $500/year.”

8. **FACT — `verdict_summary`: invents an exclusive cause of history expiry and leaves Sync's team size implicit.**
   > If your notes are private thinking, Obsidian wins: $0 for the app, $480/year if you want Sync, and history that only git can expire.

   The sheet supports no plan-imposed history cutoff for plain files plus git, not a claim that only git can remove history; $480/year is for 10 users (facts: 55–58, 66–68).

   Replacement: “For private notes, Obsidian's app costs $0; Sync for 10 people costs 10 × $4 × 12 = $480/year billed annually, while plain files under git avoid a plan-imposed history cutoff.”

9. **FACT — section 1: extends metering to everything.**
   > **Notion: notes are shared state on Notion's server**, and everything around it is metered.

   The sheet distinguishes membership pricing, API budgets, page-history tiers and agent credits; it does not say every surrounding feature is metered (facts: 5–29, 64–65).

   Replacement: “Notion sells shared state and permissions through membership plans, with separate API budgets, page-history tiers and Custom Agent credits.”

10. **FACT — section 1: invents an export/conversion claim.**
    > The canonical copy lives in Notion's database, so every export is a conversion.

    The sheet contains no Notion export behavior or conversion guarantee. The preceding “Notion forbids plain-file truth” heading must also lose that unsupported absolute.

    Replacement: “Obsidian keeps note data in local Markdown files and frontmatter, while Notion provides shared state and permissions.”

11. **FACT — `decision_matrix[7].why`: invents migration work.**
    > Migration turns every page into a conversion job and buys back nothing you are missing.

    Neither per-page conversion work nor a universal absence of migration benefits is established (facts: 63–68).

    Replacement: “Stay on Notion if its existing permissions and history meet your requirements; Obsidian has no permission model or built-in multi-user editing.”

12. **FACT — section 3: invents formula execution behavior.**
    > Formulas run in each user's app.

    The sheet documents YAML formula definitions, not where or when they execute (facts: 50–52). Remove the associated “Server-side computed properties” claim as well.

    Replacement: “A `.base` file stores view definitions, including formulas; note data remains in Markdown files and frontmatter.”

13. **FACT — section 4: turns the absence of a built-in agent into a claim about every server.**
    > Obsidian's equivalent is you, a script or a plugin. No server runs anything while your laptop sleeps.

    The sheet establishes no server-side Obsidian agent, not equivalence with arbitrary scripts/plugins or a restriction on third-party infrastructure (facts: 66–68).

    Replacement: “Obsidian has no server-side agent; collaboration comes through Sync shared vaults or third-party tooling.”

14. **FACT — section 3: invents a universal visibility rule.**
    > Anyone with the folder sees every row.

    Having no Obsidian permission model does not establish what every person sees in every filtered view (facts: 46–52, 66–68).

    Replacement: “Obsidian has no permission model, so Bases is not a substitute for Notion Business's granular database permissions.”

15. **FACT — section 1: omits the built-in qualification on editing.**
    > No permission model, no built-in agent, no multi-user editing.

    The sheet says no built-in multi-user editing and explicitly allows collaboration through shared vaults or third-party tooling (facts: 66–68). “Obsidian forbids server-side control” also overstates the documented absence.

    Replacement: “Obsidian has no permission model, no server-side agent and no built-in multi-user editing; collaboration requires Sync shared vaults or third-party tooling.”

16. **FACT — `decision_matrix[5].why`: invents a guest-model description.**
    > Free caps external guests at 10, and Obsidian has no guest model beyond shared vaults.

    The sheet establishes Obsidian's lack of permissions and its collaboration routes, not a guest model or guest-capacity comparison (facts: 7, 66–68).

    Replacement: “Notion Free allows 10 external guests; Obsidian offers collaboration through Sync shared vaults or third-party tooling, without a permission model.”

17. **FACT — section 4: invents mandatory queue implementation.**
    > The honest counter is that Notion's API is a queue you have to build:

    Request budgets and retry requirements do not establish that every consumer must build a queue; the JS SDK already retries (facts: 23–29).

    Replacement: “Notion integrations must respect connection and workspace budgets, plus `Retry-After` on HTTP 429 or 529; the JS SDK retries for you.”

18. **FACT — section 5: presents connection allowances as unqualified throughput.**
    > 600 API requests per minute instead of 180.

    Both figures are per connection; workspace and data-source query limits also apply (facts: 23–29).

    Replacement: “Business raises the per-connection budget from 180 to 600 requests per minute, while the separate workspace budget and roughly 3-per-second data-source query limit still apply.”

19. **LOGIC — closing checklist: checks the last edit rather than the needed version.**
    > Is its last real edit inside your plan's 7, 30 or 90 days?

    The last edit's age does not establish whether a recoverable version predates a mistake. The history comparison concerns recovery windows (facts: 7–12).

    Replacement: “Can you still recover the version from before a mistaken edit within your plan's 7-, 30- or 90-day history window?”

20. **FACT — closing checklist: applies the lower connection budget without a plan condition.**
    > Do they share one connection's 180/min?

    Business and Enterprise get 600/minute per connection; all connections also share a separate workspace budget (facts: 23–26).

    Replacement: “Which integrations share a connection's 180-request-per-minute budget, or 600 on Business and Enterprise, and which compete for the separate workspace budget?”

21. **LOGIC — closing checklist: absence of hidden pages does not establish absence of permission requirements.**
    > None? Permissions are buying you nothing.

    The preceding question only asks about page visibility, whereas Business also includes granular database permissions and private teamspaces (facts: 11–12).

    Replacement: “Before paying for Business permissions, identify the granular database permissions or private teamspaces your team actually needs.”

22. **LOGIC — section 5: rules out Business based on only one feature need.**
    > Who should not pay it: a team whose notes are private drafts, where nobody needs to be locked out of anything.

    Private drafts do not rule out demand for Notion Agent, AI Meeting Notes or a longer recovery window (facts: 11–12).

    Replacement: “Do not pay for Business solely to store private drafts if you do not need its agent, AI Meeting Notes, SSO, permissions or 90-day page history.”

23. **LOGIC — section 2: makes the recovery window the sole test of a system of record.**
    > Notion's history window decides whether it can be a system of record.

    A history window must be compared with the reader's recovery requirement; the sheet establishes plan differences, not universal suitability (facts: 7–12).

    Replacement: “If you need to recover an edit older than 7 days, Notion Free's page history does not meet that requirement.”

24. **LOGIC — section 3 title: declares the database comparison settled.**
    > Obsidian Bases ended the 'Notion has databases' argument

    Database-like views do not erase the documented differences in permissions and built-in multi-user editing (facts: 45–53, 66–68).

    Replacement: “Bases adds database-like views, but Obsidian still lacks a permission model.”

25. **FACT — section 2 title: invents universal reader behavior.**
    > Page history is the tax nobody prices in

    The sheet calls history a silent tax but does not establish that nobody accounts for it (facts: 19–20).

    Replacement: “Notion Free keeps 7 days of page history; Business keeps 90.”

26. **FACT — section 2: invents a claim about other comparisons.**
    > Comparisons rarely mention it.

    The sheet contains no survey or frequency claim about comparison articles.

    Replacement: “Plus provides 30 days of page history at $10/member/month.”

27. **FACT — section 4 closer: invents a vendor relationship for every integration.**
    > And every integration is one more vendor relationship.

    The sheet does not establish that every integration introduces another vendor.

    Replacement: “All connections share a separate plan-scaled workspace budget, whose `Retry-After` can exceed a minute.”

28. **SLOP — closing section: symmetric slogans substitute for the decision boundary.**
    > **If your notes are shared state** that other people edit, permission and automate, Notion Business wins: those features need a server. **If they are private thinking** that occasionally gets shared, Obsidian wins: files outlive vendors.

    The matched “If … wins” sentences repeat the framing instead of identifying the next requirement to check; they also overreach with “those features need a server” and “files outlive vendors” (standard: §§7–8).

    Replacement: “Choose Notion Business when granular database permissions or private teamspaces are required; choose Obsidian for local Markdown notes only if you can forgo a permission model and built-in multi-user editing.”

29. **SLOP — final checklist sentence: hollow closer.**
    > It is optional, and that is a decision.

    The preceding sentence already establishes the licence price and tells the reader to decide; this adds nothing (standard: §§7–8).

    Replacement: “Exclude the commercial licence from required costs unless your team chooses to pay the optional $50/user/year.”

30. **WEAK — `faqs[1].a`: unrelated purchase terms dilute the discount answer.**
    > The commercial licence and the $25 one-time Catalyst tier are non-refundable.

    These terms do not help a school or nonprofit decide whether discounted Sync or Publish fits; use the refund terms for those purchases instead (facts: 41–42).

    Replacement: “Sync and Publish also have a 7-day no-questions refund.”

31. **BORING — hook's second sentence: repeats the metaphor without a purchasing condition.**
    > The sticker fight is $0 versus $10, but the real one is a server with a meter against a folder with a pipe.

    The prices lack their product and billing units, and the reader still has no team-level comparison. Use the sheet's 10-person Business-versus-Sync calculation (facts: 55–60); the following introduction also needs the audience, outcome and evidence level required by standard §3.3.

    Replacement: “For a 10-person team, Notion Business costs 10 × $20 × 12 = $2,400/year, while Obsidian Sync costs 10 × $4 × 12 = $480/year billed annually; the deciding requirement is whether you need Notion's shared permissions and agent.”

32. **BORING — section 1: names a tier distinction without its useful values.**
    > How far back you can roll a page depends on tier.

    Name the exact recovery windows from the sheet rather than making the reader wait for the next section (facts: 7–12).

    Replacement: “Notion page history is 7 days on Free, 30 on Plus and 90 on Business.”

## REVISION BRIEF

- Separate Business's included Notion Agent from separately priced Custom Agents everywhere, including the decision matrix; retain the exact Custom Agents terms, “Free to try, then $10 per 1,000 monthly Notion credits,” and do not infer a Business prerequisite for them.
- Rebuild matrix choices around explicit requirements: recovery duration rather than edit frequency; local property views rather than database equivalence; connection throughput rather than unspecified pipeline frequency. Preserve Map's Maps-plugin dependency, do not recommend an unverified paid guest capacity, and make the stay-put pick explicitly Notion rather than “Neither.”
- Delete unsupported Notion export/conversion claims, per-user formula execution claims, universal folder visibility, scripts/plugins as agent equivalents, the laptop-sleep server claim and the universal integration/vendor claim. Describe only local Markdown/frontmatter, view definitions, and the documented collaboration and permission limitations.
- Give API figures their scope everywhere: 180 requests per 60-second window per connection, or 600/minute on Business/Enterprise; a separate plan-scaled workspace budget; roughly 3 data-source queries/second per connection. Preserve burst capability and `Retry-After` handling, including SDK retries, without prescribing a mandatory queue.
- Keep every annual team price tied to 10 people and show its formula. Preserve $2,400/year Business, $1,200/year Plus, $480/year Sync and $980/year Sync plus optional licences; make $0 conditional on using git/iCloud instead of Sync and declining the optional licences. Describe git history as free of plan-imposed cutoffs, not impossible to lose.
- Replace categorical history and database headlines with their supported limits. Remove claims about what nobody prices in or what comparisons rarely mention; make the closing checklist test recovery of the needed version and actual Business feature requirements, then end with an action rather than a repeated slogan.
- Introduce the intended reader and purchasing outcome immediately after the hook; identify vendor pricing and official documentation as the evidence, verified 2026-11-10, without mentioning the fact sheet, brief or reviewer. Expose at least two buying scenarios with formulas, using the available single-user rates and 10-person team figures rather than inventing usage benchmarks; do not invent migration timings or export tooling to fill the standard's transition requirement.
- Change the LLM FAQ to ask which plan lists zero data retention, without equating retention with transmission; keep the education/nonprofit FAQ focused on its 40% Sync/Publish discount and those services' refund terms rather than unrelated Catalyst purchases.

DEFECTS: FACT=15 META=0 SLOP=2 LOGIC=12 RHYTHM=0 BORING=2 WEAK=1
