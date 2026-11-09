# Vercel vs Cloudflare Pages — editorial review

Locations use zero-based JSON array indices. Arithmetic in the draft was rechecked: $307.20, $80, $12/$17, ≈ $0.0356, $13.40 and $2.20 are all correct. The defects below come from claims around those numbers. All sections are 712–956 characters, the body is 4,677 characters and no paragraph exceeds 4 sentences, so no RHYTHM defects were found.

1. **FACT** — `hook, both sentences`

   **Quote:** “The idle-wait CPU advantage has disappeared. Vercel and Cloudflare now meter active execution, so the deciding bill moves to transfer, requests and the work your code actually does.”

   **Defect:** The sheet does not record when either vendor changed its billing model, so “has disappeared” and “now” describe a history the sheet doesn't contain. Fluid compute is only the default for *new* Vercel projects, and Vercel also bills provisioned memory in GB-hours, so “meter active execution” is incomplete. The hook also lacks the loss number recommended by standard §3-2, and it ends on a filler triad.

   **Replacement:** At 3 TB a month, Vercel Pro bills 2,048 GB × $0.15/GB = $307.20 in transfer overage while Cloudflare bills $0 for egress. CPU no longer separates them: Vercel's Fluid compute (the default for new projects) bills active CPU rather than wall time, and Workers bills CPU-ms.

2. **FACT** — `sections[1].content, first sentence`

   **Quote:** “Both now meter CPU execution rather than wall time.”

   **Defect:** The sheet says Fluid compute is the default for new projects, not for every Vercel deployment. The sentence is addressed to readers who already run a deployed app, so it may not describe their project.

   **Replacement:** Fluid compute, the default for new Vercel projects, bills active CPU rather than wall time, and Workers bills CPU-ms; check that an existing Vercel project actually runs on Fluid compute.

3. **LOGIC** — `cost_math[1].result (same skew in sections[2] table, request row)`

   **Quote:** “$80 Vercel request overage versus $17 Cloudflare requests plus base; Vercel seats excluded”

   **Defect:** This compares unlike figures. The Cloudflare figure includes the $5 plan floor, but the Vercel figure leaves out the $20 seat. Compare either overage against overage or overage plus floor on both sides.

   **Replacement:** Request overage: $80 on Vercel versus $12 on Cloudflare; with plan floors, $20 × seats + $80 (= $100 for one seat) on Vercel versus $5 + $12 = $17 on Cloudflare, before CPU.

4. **META** — `decision_matrix[4].why`

   **Quote:** “Pages has a hard per-asset ceiling, and the fact sheet does not establish Vercel's equivalent limit.”

   **Defect:** This refers to the editorial fact sheet, which readers never see.

   **Replacement:** Pages caps every asset at 25 MiB; Vercel's per-asset limit is not covered in this comparison, so check it before moving the file there.

5. **META** — `faqs[3].a`

   **Quote:** “The fact sheet lists `vercel deploy --temporary` under Hobby for temporary deployments without an account.”

   **Defect:** Mentions the writing input instead of answering the reader's question.

   **Replacement:** Yes: on the Hobby tier, `vercel deploy --temporary` creates a temporary deployment without an account.

6. **FACT** — `sections[0].content, last paragraph`

   **Quote:** “Build for the Workers runtime rather than assuming the app moves unchanged; keep the runtime-specific work identifiable if you may move back.”

   **Defect:** The sheet does not establish that moving requires runtime adaptation, and it forbids isolate-vs-container claims. Still, the draft's whole decision frame depends on undefined phrases such as “fits Workers”, “runtime adaptation” and “handlers already suited to Workers” (also in sections[4], sections[5], decision_matrix[0], [1], [2] and [6]). “Fit” must be defined using the listed limits.

   **Replacement:** Before moving, check each handler against Workers' listed limits: 10 ms CPU per invocation on Free, and a 30-second default with a 5-minute maximum of CPU time on Paid.

7. **FACT** — `sections[0].content, philosophy bullets`

   **Quote:** “- Vercel: the framework vendor runs your framework.”

   **Defect:** The sheet does not say Vercel is a framework vendor and names no framework. The same unsupported premise drives “framework fit” in the next paragraph and “framework deployment” in sections[5], decision_matrix[1] and verdict_summary. The Cloudflare bullet is a generic slogan.

   **Replacement:** - Vercel meters delivery: Pro includes 1 TB Fast Data Transfer and 10 M CDN requests, then charges starting at $0.15/GB and $2 per 1 M.
   - Cloudflare meters execution: egress is free, and Workers Paid charges $0.30 per additional 1 M requests and $0.02 per additional 1 M CPU-ms.

8. **FACT** — `sections[5].content, blockquote`

   **Quote:** “> Neither CPU milliseconds nor build minutes disappear with free egress.”

   **Defect:** The sheet has no “build minutes” meter for either vendor. Pages lists builds per month (500 / 5,000 / 20,000), concurrent builds (1 / 5 / 20) and a 20-minute build timeout.

   **Replacement:** > Pages allows 500 builds a month on Free, and each build must finish within 20 minutes.

9. **FACT** — `verdict_summary, second sentence`

   **Quote:** “Check CPU milliseconds, build minutes and generated assets today before committing to either bill.”

   **Defect:** “Build minutes” is invented, as in item 8, and the sentence is a filler triad.

   **Replacement:** Today, compare your monthly builds with Pages' 500 / 5,000 / 20,000 limits and your largest asset with its 25 MiB ceiling.

10. **FACT** — `sections[5].content, checklist item 2`

    **Quote:** “- Count seats, inspect build minutes and check the largest generated asset.”

    **Defect:** “Build minutes” is invented, as in item 8.

    **Replacement:** - Count seats at $20 each, check your longest build against Pages' 20-minute timeout and check your largest asset against 25 MiB.

11. **LOGIC** — `decision_matrix[3].why`

    **Quote:** “Idle waits consume neither platform's CPU meter, so waiting alone does not justify a migration.”

    **Defect:** The conclusion does not follow. Vercel still bills provisioned memory in GB-hours while an instance waits, and only new projects are guaranteed to be on Fluid compute. The “Neither — stay put” pick also breaks the standard's no-tie rule (§4).

    **Replacement:** On Fluid compute an idle wait burns no Active CPU, but Vercel still bills provisioned memory in GB-hours; confirm the project runs on Fluid compute and price that memory line before deciding a wait-heavy app should stay.

12. **LOGIC** — `decision_matrix[2].why`

    **Quote:** “Workers Paid has a per-account minimum while Vercel Pro charges per seat.”

    **Defect:** A $5 minimum is a floor, not a full price. The sheet lists Pages Free/Pro/Business tiers without prices, so it does not show that Cloudflare's cost stays flat as seats grow. The same leap appears in “If bytes and seats dominate…” in sections[5] and verdict_summary.

    **Replacement:** Each Vercel Pro seat adds $20/month before traffic changes, while Workers Paid lists a $5/month minimum per account; Pages Pro and Business plan prices are not covered here, so confirm them before moving for seats.

13. **LOGIC** — `sections[5].content, second sentence`

    **Quote:** “If preserving the framework deployment matters more and transfer stays inside its allowance, Vercel wins on that condition—not on idle-wait CPU billing.”

    **Defect:** Keeping transfer inside 1 TB does not make Vercel the cheaper option. The article's own 50 M-request row shows $80 against $12 in request overage. Seats, CPU and memory still bill.

    **Replacement:** If your Vercel deployment already works and stays within Pro's 1 TB transfer and 10 M CDN requests, its delivery overages are $0 and the bill to beat is $20 per seat plus Active CPU and provisioned memory.

14. **LOGIC** — `decision_matrix[7].why`

    **Quote:** “Vercel's listed duration ceiling rules it out while a switch requires checking Workers CPU limits rather than assuming longer execution.”

    **Defect:** “Neither” does not follow. Workers' limits are CPU time, not duration, and Cron Trigger and Queue consumer invocations get 15 minutes. A long job may therefore fit Workers. The row is also a tie, which §4 forbids.

    **Replacement:** Vercel lists a 5-minute function duration; Workers Paid allows 5 minutes of CPU time per invocation (15 for Cron Trigger and Queue consumers), so move a long Cron or Queue job to Workers if its CPU time fits, and redesign anything else.

15. **LOGIC** — `sections[2].content, after the table`

    **Quote:** “The request row assumes billable requests, not free static assets.”

    **Defect:** The row places two different meters side by side as if they were one 50 M figure: Vercel counts CDN requests and Cloudflare counts Workers requests. The sheet says Cloudflare static asset requests are free and unlimited. The caveat hides that difference instead of naming it (§6: compare only like numbers).

    **Replacement:** The row applies only to requests that run a Worker; Vercel's line counts CDN requests, while Cloudflare static asset requests are free and unlimited.

16. **FACT** — `sections[3].content, third bullet`

    **Quote:** “- Vercel Pro: 10M requests and 1 TB included, then overages; functions have a 5-minute limit.”

    **Defect:** The allowance is 10 M *CDN* requests of 1 TB *Fast Data Transfer*. Bare “requests” blurs it with the Workers request meter in the same section.

    **Replacement:** - Vercel Pro: 10 M CDN requests and 1 TB Fast Data Transfer included; functions run up to 5 minutes.

17. **LOGIC** — `cost_math[2].result`

    **Quote:** “Approximately $0.0356 versus $0.02 per million CPU-ms; Cloudflare includes 30M CPU-ms/month”

    **Defect:** The Vercel figure is a starting rate that excludes provisioned memory GB-hours, while sections[1] says memory is a separate bill. Presenting the two CPU rates as a full compute comparison overstates their equivalence.

    **Replacement:** ≈ $0.0356 (Vercel starting rate, before provisioned-memory GB-hours) versus $0.02 per million CPU-ms after Cloudflare's 30 M included; Vercel Pro includes no CPU.

18. **LOGIC** — `decision_matrix[0].why`

    **Quote:** “Cloudflare's no-egress-charge policy removes the transfer penalty without requiring an assumed runtime fit.”

    **Defect:** The situation column already assumes runtime fit, so “without requiring an assumed runtime fit” contradicts the row. The row also leaves out the number that drives the pick.

    **Replacement:** At 3 TB/month, Vercel Pro's transfer overage is 2,048 GB × $0.15/GB = $307.20; Cloudflare charges $0 for egress.

19. **LOGIC** — `sections[4].title`

    **Quote:** “Free egress makes cache design your problem”

    **Defect:** The section shows caching lowering Cloudflare's CPU line. Egress has nothing to do with it, so the title claims a cause that the section does not show.

    **Replacement:** Caching cuts Cloudflare's CPU line; requests still bill

20. **SLOP** — `sections[0].content, first blockquote`

    **Quote:** “> The winner follows the inflated line item, not the cheapest invocation headline.”

    **Defect:** This is an aphorism with no number, and it uses the “not X” construction. That construction appears more than 10 times in the body (“not its function count”, “not benchmarks”, “not invoice convergence”, “not complete invoices”, “not interchangeable”, “not nothing for the app”, “not just the transfer savings”, “not a measured cache-hit promise”, “not on idle-wait CPU billing”).

    **Replacement:** > At 3 TB a month the gap is $307.20 of Vercel transfer overage; at 50 M requests it is $80 versus $12 of request overage.

21. **SLOP** — `sections[0].content, first sentence`

    **Quote:** “If you operate a deployed app and are weighing a move, compare the workload's bill, not its function count.”

    **Defect:** “Function count” is a strawman that the article never discusses. Standard §3-3 requires the opening paragraph to state, with a condition, who the article is for.

    **Replacement:** This is for teams running on Vercel Pro or Cloudflare Pages whose transfer is near 1 TB a month or whose requests exceed 10 M.

22. **SLOP** — `sections[0].content, second blockquote`

    **Quote:** “> Cloudflare's bargain forbids treating free delivery as free execution.”

    **Defect:** This slogan mirrors the preceding “The Vercel bargain forbids…” sentence. The pair is a symmetric construction with no figures.

    **Replacement:** > Free egress does not cover execution: Workers Paid still bills $0.30 per additional 1 M requests and $0.02 per additional 1 M CPU-ms.

23. **SLOP** — `sections[1].content, blockquote`

    **Quote:** “> CPU convergence is not invoice convergence.”

    **Defect:** A hollow aphorism, and another “not X” sentence.

    **Replacement:** > Vercel Pro includes no CPU; Workers Paid includes 30 M CPU-ms a month.

24. **SLOP** — `sections[4].content, first sentence`

    **Quote:** “Cloudflare charges nothing for egress, not nothing for the app.”

    **Defect:** Wordplay instead of a fact.

    **Replacement:** Cloudflare charges $0 for egress, but Pages Functions still bill as Workers requests and CPU-ms.

25. **SLOP** — `sections[4].content, first blockquote`

    **Quote:** “> Budget the runtime adaptation, not just the transfer savings.”

    **Defect:** This repeats the unsupported adaptation claim (item 6), sits in a section about caching CPU, and is another “not X” slogan.

    **Replacement:** > In Cloudflare's 100 M-request example, requests cost $27.00 and uncached CPU $13.40.

26. **SLOP** — `verdict_summary, first sentence`

    **Quote:** “If bytes and seats dominate and Workers fits the app, Cloudflare Pages wins; if preserving a working framework deployment matters more and transfer stays within its allowance, Vercel wins.”

    **Defect:** This repeats the opening of sections[5] almost word for word. Standard §8-2 requires the conclusion to take a new angle rather than restate earlier text.

    **Replacement:** Pick Cloudflare Pages when transfer above 1 TB or requests above 10 M drive your Vercel bill (3 TB means $307.20 of overage against $0) and every asset fits 25 MiB; stay on Vercel when traffic stays inside Pro's 1 TB and 10 M CDN requests.

27. **SLOP** — `sections[2].content, last sentence`

    **Quote:** “Adding seats raises Vercel's floor before traffic changes; multiplying bytes raises its transfer line without adding useful CPU work.”

    **Defect:** “Without adding useful CPU work” adds no information, and the sentence pairs two clauses for symmetry.

    **Replacement:** Each Vercel seat adds $20/month before any traffic; Cloudflare's $5 minimum is per account.

28. **SLOP** — `sections[3].content, after the bullets`

    **Quote:** “Those limits are not interchangeable.”

    **Defect:** This sentence says nothing, and the next sentence already makes the point.

    **Replacement:** (Delete; begin the paragraph with “Exceeding an included traffic allowance raises a bill; exceeding an asset ceiling breaks the deployment plan.”)

29. **SLOP** — `sections[3].content, closing blockquote + paragraph`

    **Quote:** “> Do not choose Pages for that oversized asset unchanged.”

    **Defect:** It is paired with “Do not choose Vercel for a function that must run beyond its duration limit unchanged, either” as mirror-image prohibitions. That is a symmetric construction, and the second prohibition ignores Workers' CPU-time limit.

    **Replacement:** > Shrink or remove every asset over 25 MiB before targeting Pages; a Vercel function that needs more than 5 minutes must be split, or checked against Workers' 5-minute CPU-time cap.

30. **BORING** — `sections[4].content, after the bullets`

    **Quote:** “The request line therefore survives.”

    **Defect:** It names a line without giving its amount. Missing facts from the sheet: the request line is $27.00, and the totals are $45.40 uncached and $5.00 + $27.00 + $2.20 cached.

    **Replacement:** The request line stays at (100 M − 10 M) × $0.30/M = $27.00, so the cached total is $5.00 + $27.00 + $2.20 = $34.20 against $45.40 uncached.

31. **BORING** — `sections[3].content, first bullet`

    **Quote:** “- Pages Free: 500 builds/month, 20,000 files per site.”

    **Defect:** It gives only the Free tier. Missing facts: builds of 5,000 Pro / 20,000 Business, concurrent builds of 1 / 5 / 20, and 100 projects per account. The 20,000-file cap is a more common deployment blocker than the 25 MiB example and should not be buried.

    **Replacement:** - Pages builds per month: 500 Free / 5,000 Pro / 20,000 Business, with 1 / 5 / 20 concurrent; 20,000 files per site on Free; 100 projects per account.

32. **BORING** — `sections[1].content, after the bullets`

    **Quote:** “Vercel also reuses idle waits through in-function concurrency: concurrent requests share an instance.”

    **Defect:** It states the mechanism without the vendor's figures. Missing: Vercel claims “up to 85%” savings from in-function concurrency and “up to 90%” from Active CPU, and both must be labelled as Vercel's claims.

    **Replacement:** In-function concurrency lets concurrent requests share one instance; Vercel claims up to 85% savings from it and up to 90% from Active CPU pricing, and neither is a measurement.

33. **WEAK** — `decision_matrix[1]`

    **Quote:** “Keeping the working deployment avoids runtime adaptation when transfer overages are not the problem.”

    **Defect:** The condition leaves out the 10 M CDN-request allowance, and $80 versus $12 at 50 M can reverse the pick. The reason rests on unsupported adaptation cost instead of a number.

    **Replacement:** situation “Vercel deployment works, transfer ≤ 1 TB and CDN requests ≤ 10 M/month”; why “Inside both Pro allowances Vercel's delivery overages are $0, so the bill to beat is $20 per seat plus Active CPU and memory.”

34. **WEAK** — `decision_matrix[6].why`

    **Quote:** “Its listed CPU unit rate is lower, but requests and separate service line items still need costing.”

    **Defect:** It gives no figures, and the hedge cancels the pick.

    **Replacement:** Workers Paid charges $0.02 per million CPU-ms after 30 M included, against Vercel's starting ≈ $0.0356 per million CPU-ms with no included CPU.

35. **WEAK** — `cost_math[3].result`

    **Quote:** “$13.40 versus $2.20 CPU only in Cloudflare's example; request charges remain”

    **Defect:** Showing CPU alone overstates the saving from caching. A reader needs the totals to decide whether cache work is worth it.

    **Replacement:** In Cloudflare's example, $45.40 uncached ($5.00 + $27.00 + $13.40) versus $34.20 cached ($5.00 + $27.00 + $2.20); caching cuts only the CPU line.

## REVISION BRIEF

- Rewrite the hook as a loss number: “At 3 TB a month, Vercel Pro bills 2,048 GB × $0.15/GB = $307.20 in transfer overage; Cloudflare bills $0 for egress.” Wherever the article says both vendors meter CPU, state that Fluid compute is the default for *new* Vercel projects and that Vercel also bills provisioned memory in GB-hours (Vercel says it is under 10% of the Active CPU rate). Do not say anything “disappeared” or changed “now”.
- Delete every “framework vendor”, “framework fit”, “runtime adaptation” and undefined “fits Workers” phrase. Define fit only with listed limits: Workers Free allows 10 ms CPU per invocation; Paid has a 30 s default and a 5-minute maximum of CPU time (15 minutes for Cron Trigger and Queue consumers); Pages allows 25 MiB per asset, 20,000 files on Free, a 20-minute build timeout and 500 / 5,000 / 20,000 builds per month. Replace the philosophy bullets with “Vercel meters delivery” and “Cloudflare meters execution”, each backed by its included allowances and overage rates.
- Remove “build minutes” everywhere (sections[5] blockquote, checklist and verdict_summary); no such meter exists in the source. Replace it with builds per month and the 20-minute timeout. Remove both “fact sheet” mentions (decision_matrix[4].why and faqs[3].a) and answer the reader directly.
- Make every price comparison like-for-like: request overage $80 vs $12, or with floors $20 × seats + $80 vs $5 + $12 = $17. Label Vercel's line “CDN requests”, state that Cloudflare static asset requests are free and unlimited, mark Vercel CPU ≈ $0.0356/M as a starting rate before memory, and give Cloudflare's cache example as totals: $45.40 uncached vs $34.20 cached, with the $27.00 request line unchanged.
- Rebuild the decision matrix so that no row picks “Neither” or only “Not Pages”. Split the long-job row by trigger type (Cron and Queue jobs get 15 minutes of CPU on Workers). Base the seat row on $20 per seat vs a $5 per-account minimum, noting that Pages Pro and Business prices are not covered. Make the stay-on-Vercel row require transfer ≤ 1 TB *and* CDN requests ≤ 10 M. Put a number in every “why”.
- Cut the “not X” construction to at most two uses in the whole article. Replace the slogan blockquotes (“inflated line item”, “CPU convergence”, “bargain forbids…”, “Budget the runtime adaptation”, the mirrored “Do not choose…” pair) with blockquotes that each carry one sheet figure. Delete “Those limits are not interchangeable.”
- Open sections[0] with a condition-bearing audience sentence (transfer near 1 TB or requests above 10 M). Rename sections[4] “Caching cuts Cloudflare's CPU line; requests still bill”. Expand the Pages bullet to Free/Pro/Business builds, 1 / 5 / 20 concurrency and 100 projects per account. Add Vercel's “up to 85%” and “up to 90%” savings figures, labelled as Vercel's claims.
- Rewrite verdict_summary from a new angle rather than restating sections[5]: name the trigger thresholds (above 1 TB transfer or above 10 M requests means Cloudflare, provided assets are ≤ 25 MiB; otherwise Vercel), then give one check to run today. Keep the body within 3,200–4,800 characters and each section within 1,100.

DEFECTS: FACT=8 META=2 SLOP=10 LOGIC=9 RHYTHM=0 BORING=3 WEAK=3
