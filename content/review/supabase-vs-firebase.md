# Supabase vs Firebase — editorial review

Locations use zero-based JSON array indices.

1. **FACT** — `hook, first sentence`

   **Quote:** “A 50-user dashboard watching 100 live documents costs about $1,296 a month in Firestore reads and a flat $25 on Supabase Pro.”

   **Defect:** The price requires 20 changes per document per minute and continuous listening throughout the modeled month; the Supabase comparison is valid only inside its quotas. This is arithmetic, not an observed bill (fact sheet, worked arithmetic and Pro allowances).

   **Replacement:** At us-central1 rates, 50 users continuously watching 100 documents that each change 20 times/minute produce a modeled read charge of 50 × 100 × 20 × 60 × 24 × 30 ÷ 100,000 × $0.03 ≈ $1,296/month before free-quota adjustments, versus $25/month for one Supabase Pro Micro project within its quotas.

2. **FACT** — `verdict_summary, first sentence`

   **Quote:** “Supabase wins if your app keeps live listeners open on frequently changing data: that dashboard shape costs ≈ $1,296/month in Firestore reads against a flat $25 on Supabase Pro.”

   **Defect:** Repeats the unqualified price guarantee and extends one hypothetical workload to every frequently changing app; neither capacity nor quota fit has been established.

   **Replacement:** Before switching, compare your modeled Firestore listener reads with Supabase Pro’s quotas and Micro’s 60 direct / 200 pooler connection limits; the $25/month comparison assumes one Micro project within those quotas.

3. **FACT** — `cost_math[1].result`

   **Quote:** “$25/month flat”

   **Defect:** The plan-plus-credit equation is correct, but this result suppresses usage overages and any additional compute; Pro includes 250 GB egress, then charges $0.09/GB, for example.

   **Replacement:** One Pro project on Micro costs $25/month within the included quotas; egress beyond 250 GB costs $0.09/GB.

4. **FACT** — `sections[1].content, after the Python block`

   **Quote:** “The same shape on Supabase Pro with Micro compute is a flat $25/month.”

   **Defect:** The worked comparison explicitly says inside the quota; it does not prove that this workload fits every quota or Micro’s capacity.

   **Replacement:** The same modeled shape costs $25/month on one Supabase Pro Micro project within the included quotas; check capacity separately.

5. **META** — `cost_math[0].label`

   **Quote:** “Firestore: 50-user live dashboard (derived from fact-sheet rates)”

   **Defect:** Fact-sheet rates exposes the editorial input rather than identifying reader-facing assumptions or rate provenance.

   **Replacement:** Firestore: modeled continuous dashboard with 50 users, 100 documents each and 20 changes per document per minute, priced at us-central1 read rates.

6. **FACT** — `sections[0].content, opening paragraph`

   **Quote:** “Every document read, write, index batch and listener update is a line on the invoice.”

   **Defect:** Free operations exist, queries with up to one range field are exempt from index-entry charges, and listener updates are billed as reads rather than as a separate meter.

   **Replacement:** Firestore has free daily quotas of 50,000 reads and 20,000 writes; billable reads cost $0.03 per 100,000 in us-central1, listener updates count as reads, and queries with up to one range field incur no index-entry charge.

7. **FACT** — `sections[0].content, first bullet`

   **Quote:** “**Firestore forbids JOINs.**”

   **Defect:** The fact sheet contains no JOIN-support claim; the writing standard is not an additional product-fact source.

   **Replacement:** The migration scripts copy a single Firestore collection into a single Postgres table.

8. **FACT** — `sections[0].content, first bullet`

   **Quote:** “Related data gets duplicated into documents or fetched with extra reads, and every extra read is billed.”

   **Defect:** Neither the forced data-model alternatives nor universal billing is supported; free read quota directly defeats the latter claim.

   **Replacement:** Splitting nested JSON into related tables requires custom hooks, and Firestore provides 50,000 free document reads per day.

9. **FACT** — `decision_matrix[2].why`

   **Quote:** “Firestore has no JOINs, so every relation becomes duplicated data or extra billed reads.”

   **Defect:** The sheet does not establish JOIN support or these mandatory consequences. Reframe this row around the documented migration requirement rather than using outside product knowledge.

   **Replacement:** Choose Supabase only if you are prepared to design the related tables and write the custom hooks that split nested JSON during migration.

10. **FACT** — `verdict_summary, second sentence`

   **Quote:** “Firestore wins if your app is quiet enough to live inside its daily free quota and never needs a JOIN, because leaving means hand-written schema hooks and an unfinished password-verification middleware.”

   **Defect:** JOIN support is absent from the sheet, custom hooks are specifically for splitting nested JSON, and the unfinished middleware concerns first-login verification of existing Firebase passwords—not every migration.

   **Replacement:** Stay on Firestore when the workload fits all relevant free allowances and migration offers no cost saving; before moving, check whether nested JSON needs custom hooks or existing-password verification needs the work-in-progress middleware.

11. **FACT** — `sections[2].content, before the compute table`

   **Quote:** “The ceiling is the instance: its connection limits and its compute tier.”

   **Defect:** The sheet lists database direct/pooler connections, not a Realtime subscriber ceiling or a complete capacity model; it also lists usage quotas.

   **Replacement:** Micro allows 60 direct database connections or 200 pooler connections; these figures do not establish a Realtime subscriber limit.

12. **FACT** — `sections[2].content, last paragraph`

   **Quote:** “Supabase fails as a refused connection in your busiest hour, and the fix is a tier upgrade, not a config flag.”

   **Defect:** The failure scenario and exclusive remedy are invented; the sheet provides connection limits, not failure behavior or a troubleshooting prescription.

   **Replacement:** Micro provides 60 direct / 200 pooler connections for $10/month compute, while Small provides 90 / 400 for $15/month compute.

13. **FACT** — `sections[2].content, SQL comment`

   **Quote:** “-- opt-in per table: unlisted tables never stream”

   **Defect:** The publication requirement applies to Postgres Changes; the sheet also documents Broadcast, so this cannot be a universal streaming prohibition.

   **Replacement:** -- Add this table to the Postgres Changes publication.

14. **FACT** — `decision_matrix[4].why`

   **Quote:** “Supabase's pooled ceiling runs from 200 on Micro to 1,000 on XL at $210 compute, while Firestore meters events, not connections.”

   **Defect:** The Supabase numbers are listed, but no Firestore concurrency limits or capacity guarantee appear in the sheet; the Firestore pick is unsupported.

   **Replacement:** Compare the listed Supabase tiers—Micro has 200 pooler connections at $10/month compute and XL has 1,000 at $210/month compute—but do not select Firestore for concurrency without verified capacity information.

15. **LOGIC** — `decision_matrix[3].pick`

   **Quote:** “Supabase, or Firestore with offline persistence on”

   **Defect:** This is an unresolved alternative rather than a conditional winner, assumes undocumented Supabase offline behavior, and omits Firestore’s persistence-on reconnect charge after more than 30 minutes disconnected.

   **Replacement:** Keep Firestore with offline persistence on only if its reconnect charges fit your budget, including brand-new-query billing after disconnections longer than 30 minutes.

16. **LOGIC** — `sections[5].content, opening sentence`

   **Quote:** “**If your product keeps live listeners open on documents that change every minute, Supabase wins**: its bill tracks the machine, not the watching.”

   **Defect:** Update frequency alone does not establish a cost winner: listener count, document count, duration, free quota and Supabase capacity still matter.

   **Replacement:** Choose Supabase for a listener-heavy workload only when its modeled Firestore charges exceed the Supabase plan and compute cost and the workload fits the selected tier and included quotas.

17. **FACT** — `decision_matrix[0].why`

   **Quote:** “Firestore bills a read per listener update, so cost scales with users × documents × changes, while Supabase bills a flat compute tier.”

   **Defect:** A flat compute charge is not the entire Supabase bill; Pro also has a plan charge, credits and usage overages.

   **Replacement:** Choose Supabase for the modeled dashboard only within its quotas: one Pro Micro project costs $25/month after the compute credit, while Firestore listener updates are billed as reads.

18. **LOGIC** — `sections[5].content, second sentence`

   **Quote:** “If your app fits Firestore's daily free quota of 50,000 reads and 20,000 writes, moving buys schema work, not savings.”

   **Defect:** Read/write fit alone cannot establish a free bill: the sheet also limits deletes, stored data, outbound transfer and the number of free databases.

   **Replacement:** Stay on Firestore for cost reasons if the app fits all relevant free allowances: 50,000 reads, 20,000 writes and 20,000 deletes per day, 1 GiB stored and 10 GiB/month outbound transfer, with one free database per project.

19. **LOGIC** — `decision_matrix[1].why`

   **Quote:** “At 50,000 free reads a day there is no bill to cut, and migration adds schema work.”

   **Defect:** The reason treats one allowance as sufficient to establish a zero bill; make the row’s all-allowances condition explicit.

   **Replacement:** Stay on Firestore when reads, writes, deletes, storage and outbound transfer all fit the free allowances for the project’s single free database; a read count alone does not establish a free workload.

20. **LOGIC** — `decision_matrix[5].pick`

   **Quote:** “Firestore, unless each client pays for compute”

   **Defect:** A Supabase per-project charge does not demonstrate that Firestore is cheaper for the agency’s workloads, and who pays the charge does not change its amount.

   **Replacement:** Keep the cheaper verified setup after comparing each client’s Firestore usage charges with Supabase’s $35/month Pro total for two Micro projects and the compute charge for every additional project.

21. **LOGIC** — `decision_matrix[6].pick`

   **Quote:** “Neither — stay put until the auth middleware ships”

   **Defect:** Staying on Firebase is a choice, not neither; work in progress does not establish a future release or justify a recommendation keyed to one.

   **Replacement:** Stay on Firebase if preserving existing-password verification at first login is a migration requirement you cannot currently meet with the work-in-progress middleware.

22. **LOGIC** — `sections[4].content, final sentence`

   **Quote:** “Budget a forced password reset as the fallback.”

   **Defect:** Unfinished verification middleware does not establish that a forced-reset migration path is available, required or sufficient; no such path is documented in the authorized facts.

   **Replacement:** Treat existing-password verification at first login as an unresolved migration dependency because its middleware is marked work in progress.

23. **LOGIC** — `sections[5].content, checklist item 4`

   **Quote:** “Decide whether your users can survive a password reset.”

   **Defect:** Repeats the unestablished reset fallback instead of checking the documented migration blocker.

   **Replacement:** Decide whether migration can proceed while first-login verification of existing Firebase passwords depends on work-in-progress middleware.

24. **FACT** — `sections[1].title`

   **Quote:** “Firestore bills you for every minute a tab stays open”

   **Defect:** Firestore bills document read events, not elapsed tab-open minutes; an unchanged result set does not generate the modeled stream of update reads.

   **Replacement:** Firestore bills listener document changes, not tab-open minutes.

25. **FACT** — `sections[1].content, final sentence`

   **Quote:** “A laptop closed over lunch pays for its whole result set again at 13:00.”

   **Defect:** 13:00 is invented, and neither the disconnect duration nor persistence setting is established; closing a laptop alone is not the documented billing condition.

   **Replacement:** With persistence on, reconnecting after more than 30 minutes disconnected is billed like a brand-new query; with persistence off, every reconnect is billed that way.

26. **FACT** — `sections[3].content, after the count example`

   **Quote:** “Now put that count in a page header that every open listener refreshes.”

   **Defect:** The sheet documents aggregation-query billing, not automatic aggregate refreshes driven by listeners.

   **Replacement:** If your application repeatedly calls count() for a page header, each call bills index reads, with a 1-document-read minimum even when it reads no index entries.

27. **FACT** — `sections[3].content, blockquote`

   **Quote:** “> Every filter you add is a pricing decision, not just a schema decision.”

   **Defect:** Every filter overstates the rule: queries with up to one range field are exempt from index-entry charges.

   **Replacement:** Queries with up to one range field incur no index-entry charge; adding a second range field starts that billing.

28. **FACT** — `sections[0].content, opening paragraph`

   **Quote:** “You rent compute, a disk and a connection ceiling, and Postgres does whatever fits inside them.”

   **Defect:** This presents compute, disk and connections as the complete constraint set, omitting the listed metered usage allowances.

   **Replacement:** Supabase Pro combines plan and per-project compute charges with usage allowances, including 250 GB egress before $0.09/GB overages and 100,000 MAU before $0.00325/MAU overages.

29. **FACT** — `sections[4].content, after the numbered list`

   **Quote:** “The schema design Firestore let you skip lands on your desk now.”

   **Defect:** The sheet establishes custom migration hooks, not that Firestore eliminates schema design.

   **Replacement:** The import flattens a collection into text, numeric, boolean or jsonb columns; you write custom hooks if nested JSON must become related tables.

30. **LOGIC** — `hook, second sentence`

   **Quote:** “Same screen, same users: the only thing that changed is what the vendor counts.”

   **Defect:** The arithmetic does not demonstrate equivalent deployments, capacity, quotas or migration effort; only the hypothetical read-event volume is held constant.

   **Replacement:** This is a modeled billing comparison, not a measured deployment comparison or proof that Micro can serve the workload.

31. **LOGIC** — `cost_math[0].formula`

   **Quote:** “50 users × 100 docs × 20 changes/min × 60 × 24 × 30 = 4.32B reads; 4.32B ÷ 100,000 = 43,200 × $0.03”

   **Defect:** The last equality equates a batch count with a monetary amount. Separate events, billable batches and their price; identify the gross rate calculation rather than a final invoice.

   **Replacement:** For continuous listening: 50 × 100 × 20 × 60 × 24 × 30 = 4.32 billion read events/month; 4.32 billion ÷ 100,000 = 43,200 batches; 43,200 × $0.03 ≈ $1,296/month at us-central1 rates before free-quota adjustments.

32. **LOGIC** — `cost_math[3].formula`

   **Quote:** “10,000,000 ÷ 100,000 = 100 × $0.03”

   **Defect:** The equality similarly equates 100 batches with $3.00; the separate result field does not repair the false equality.

   **Replacement:** 10,000,000 reads ÷ 100,000 reads/batch = 100 batches; 100 × $0.03 = $3.00 at us-central1 rates before free-quota adjustments.

33. **LOGIC** — `sections[5].title`

   **Quote:** “Pick Supabase if users watch; keep Firestore if they mostly don't”

   **Defect:** Watching versus not watching is not a sufficient decision boundary: free allowances and total event volume can reverse the cost recommendation.

   **Replacement:** Choose by modeled read charges, quota fit and migration blockers—not watching alone.

34. **WEAK** — `decision_matrix[7].why`

   **Quote:** “Firestore's count() bills index reads on every call, with a 1-document-read minimum.”

   **Defect:** A billable minimum alone cannot justify choosing a $25/month plan; the row lacks call volume or a meaningful cost comparison.

   **Replacement:** Do not move for count() billing alone: a count over 1,500 index entries bills 2 document reads, so compare your aggregate-call volume at $0.03 per 100,000 reads with Supabase Pro’s $25/month base cost.

35. **BORING** — `sections[3].content, after the worked count example`

   **Quote:** “Cheap per call.”

   **Defect:** Cheap supplies no price scale. The exact useful sheet fact is 10,000,000 document reads = $3.00 at the listed read rate.

   **Replacement:** At the listed us-central1 rate, 10,000,000 document reads cost $3.00 before free-quota adjustments.

36. **SLOP** — `sections[2].content, blockquote`

   **Quote:** “> You stop paying for surprise. You start paying for headroom.”

   **Defect:** Symmetric slogan instead of a trade-off; it also distracts from the usage overages that can still change the bill.

   **Replacement:** Pro’s $10/month compute credit covers one Micro instance; an additional Micro project adds $10/month.

37. **SLOP** — `sections[2].content, last paragraph`

   **Quote:** “Firestore fails as a large invoice.”

   **Defect:** A billing metaphor substitutes for a concrete reader action and pretends to define the product’s failure mode.

   **Replacement:** Estimate Firestore listener charges from changed documents and reconnects before choosing a plan.

38. **BORING** — `sections[2].content, final sentence`

   **Quote:** “Size for peak, not average.”

   **Defect:** Generic capacity advice supplies no decision input. The exact missing detail is Micro’s 60 direct / 200 pooler database-connection limits, not a Realtime subscriber count.

   **Replacement:** Compare peak database connections with Micro’s 60 direct / 200 pooler limits before selecting that compute tier.

39. **SLOP** — `sections[3].content, opening`

   **Quote:** “Document reads get the attention. Index entry reads sit underneath them:”

   **Defect:** The attention claim and spatial metaphor add no information before the actual billing rule.

   **Replacement:** Firestore bills one read per batch of up to 1,000 index entries, except that queries with up to one range field incur no index-entry charge.

40. **SLOP** — `sections[1].content, Python output line`

   **Quote:** “print(reads / 100_000 * 0.03)  # here it breaks: ~1296 dollars/month”

   **Defect:** Here it breaks invents a failure point in arithmetic that executes successfully; the comment should explain the calculation’s limit, not stage a failure (standard §5).

   **Replacement:** print(reads / 100_000 * 0.03)  # Gross us-central1 read charge; excludes free-quota adjustments.

## REVISION BRIEF

- Rebuild the hook and verdict around an explicitly hypothetical continuous workload: 50 users × 100 documents × 20 changes per document per minute × 60 × 24 × 30. Show the us-central1 rate conversion to ≈ $1,296/month as a gross read-charge model before free-quota adjustments, not a measured bill; remove claims of equivalent deployments and winners based on watching alone.

- Qualify every $25 Supabase claim—including cost_math results and matrix reasons—as one Pro Micro project within included quotas; show $25 plan + $10 compute − $10 credit. Separate monthly compute prices from total plan cost, state 250 GB egress then $0.09/GB as a concrete overage example, and distinguish direct/pooler database limits from unverified Realtime subscriber capacity. Remove the invented refused-connection scenario and mandatory-upgrade remedy.

- Remove every unsupported JOIN claim, mandatory duplication/extra-read claim, assertion that Firestore lets readers skip schema design, and Firestore concurrency or Supabase offline comparison. Ground the data-model discussion in the documented single-collection-to-single-table import and the custom hooks needed to split nested JSON.

- Make the decision matrix contain 6–8 supported conditional choices, not Neither or unresolved alternatives. Require all relevant Firestore free allowances for a no-bill conclusion: 50,000 reads, 20,000 writes and 20,000 deletes per day, 1 GiB stored, 10 GiB/month outbound and one free database per project. Include the persistence-on disconnect threshold of more than 30 minutes, compare agency workload charges rather than who pays, and do not recommend migration merely because count() has a read minimum.

- Keep migration advice within the documented tooling and limitations: firestore2json.js, json2supabase.js, firestoreusers2json and import_users; custom schema hooks when splitting nested JSON; hash-parameter import; first-login existing-password verification middleware marked work in progress and the AWS Lambda variant marked TBD. Remove the forced-reset fallback, the reset checklist item and any assumption that the middleware will ship.

- Repair both cost_math equality chains by separating event counts, 100,000-read batch counts and dollars. Replace the tab-open-minute headline with changed-document billing, remove the invented lunch clock time and automatic listener-driven count refresh, and state the up-to-one-range-field exemption instead of claiming every filter adds charges. Replace the Python here-it-breaks comment with the calculation’s free-quota limitation.

- Delete the fact-sheet reference and replace the symmetric surprise/headroom slogan, generic closers and attention metaphor with specific charges, limits or actions. Identify live-dashboard readers immediately after the hook, disclose vendor-rate arithmetic rather than measurement, and date the verified rates 2026-11-10. Preserve short paragraphs and existing visual anchors; do not add padding to manufacture a rhythm fix.

DEFECTS: FACT=20 META=1 SLOP=4 LOGIC=12 RHYTHM=0 BORING=2 WEAK=1
