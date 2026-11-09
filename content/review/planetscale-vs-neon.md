# PlanetScale vs Neon — review

1. **FACT — Invented hiring and sponsorship story.** Section 5.
   > In March 2026 PlanetScale hired Drizzle's entire core team; Drizzle's own page calls PlanetScale its "biggest sponsor".

   The sheet contains neither Drizzle nor this date, hiring claim or sponsorship claim. The title's “Drizzle's maintainers” and the surrounding sentences “The second bet is quieter.” and “If you write Drizzle, your ORM's maintainers work for one of these two vendors.” depend on the same unsupported story; remove them too.

   **Replacement:** “Neki's platform preview is explicitly not for production workloads because some changes will be breaking.”
   **Replacement title:** “Neki adds sharded Postgres, but its preview excludes production”.

2. **FACT — Fixed compute is misrepresented as a fixed total bill.** Section 1.
   > **PlanetScale forbids a bill that moves with traffic.**

   PlanetScale also bills storage, backups and egress; dedicated clusters do not eliminate metered charges. The next sentence, “A quiet Sunday costs the same as launch day, and a branch is a second cluster.” repeats the misleading total-bill promise.

   **Replacement:** “PlanetScale charges for dedicated cluster capacity even when it is idle, while storage, backups and egress can add charges.”
   **Replacement for the next sentence:** “Each branch runs on its own separately billed dedicated cluster.”

3. **FACT — Decision row promises budget certainty the sheet does not offer.** Decision matrix, steady-production row.
   > Steady production awake 24/7 with a budget that must not move

   This is a situation label rather than a sentence. Its reason compares only compute, not a stable total bill. The sheet does not establish that PlanetScale can meet the stated requirement.

   **Replacement situation:** “Always-on database comparing compute charges only”.
   **Replacement reason:** “For compute only, 0.25 CU × 730 h × $0.106 = $19.35 on Neon Launch, versus $15 for PlanetScale PS-5 HA; storage and other charges remain separate.”

4. **FACT — Recommendation repeats the fixed-total-bill fiction.** Section 6.
   > If production must stay awake on a bill that does not move with the clock, or you run a Vitess-shaped MySQL estate, pick PlanetScale.

   The verdict repeats it: “PlanetScale wins if production must stay awake on a bill that does not move with the clock, or if you already run Vitess-shaped MySQL.” Both need the same qualification.

   **Replacement:** “For always-on compute, compare PlanetScale's fixed cluster charge with Neon CU-hours, then add storage and transfer charges; for Vitess-based MySQL, PlanetScale is the MySQL option in this comparison.”

5. **LOGIC — Shared Postgres support does not erase engine requirements.** Section 1.
   > Both vendors sell Postgres in November 2026, so MySQL versus Postgres no longer decides anything.

   The sheet identifies Vitess as PlanetScale's MySQL product; the draft later recommends it for existing MySQL users. The sentence contradicts that decision branch.

   **Replacement:** “For a Postgres deployment, compare cluster charges with CU-hours; an existing Vitess-based MySQL deployment still has an engine constraint.”

6. **FACT — Invented probe-to-billing causal rule.** Section 2 code comment and section 6 checklist.
   > # Here it breaks: a probe every <5 min blocks suspend, so you bill 730.

   The corresponding checklist says: “Find whatever pings your database more often than every five minutes.” and “That probe, not your traffic, decides which vendor is cheaper.” The sheet specifies suspension intervals, not which probes prevent suspension or that a probe determines the cheaper vendor.

   **Replacement code comment:** `# This comparison assumes 0.25 CU runs for all 730 hours.`
   **Replacement checklist sentence:** “Check the compute's suspension configuration and billed CU-hours before comparing its compute charge with a PlanetScale cluster.”

7. **FACT — Invented pull-request lifetime.** Section 4.
   > A preview per pull request lives for days, though, and that meter runs whether anyone opens it or not.

   The sheet provides billing granularity, not a normal lifetime for previews.

   **Replacement:** “PlanetScale bills each branch's dedicated cluster separately, prorated to the millisecond, so use your branch's actual lifetime in the estimate.”

8. **FACT — Suspension and branch fees asserted without plan or configuration conditions.** Section 4.
   > Neon branch compute bills CU-hours and suspends after five idle minutes, so an unreviewed PR costs a branch fee and storage, not a cluster.

   Launch suspension can be disabled; Scale is configurable from one minute to always on. Included branches do not all incur an extra branch fee, and compute used before suspension still costs money.

   **Replacement:** “On Neon Launch, suspension after five minutes can be disabled; extra branches beyond the included 10 cost $1.50 per branch-month, with running compute and storage billed separately.”

9. **FACT — Paid-plan metering presented as universal.** Section 1.
   > **Neon forbids a flat bill for an awake database.**

   Free includes 100 CU-hours per project. An awake database within that allowance does not establish a paid CU-hour bill. The following “Every running hour meters; suspended compute is $0.” needs a paid-plan scope too.

   **Replacement:** “Neon's paid plans charge for CU-hours used, while suspended compute costs $0.”

10. **FACT — Idle and suspended treated as synonyms.** Hook.
    > An idle Postgres database bills $0 in compute on Neon and $15 a month on PlanetScale's smallest HA cluster.

    Only suspended Neon compute is specified as $0. The article itself calculates the cost of quiet compute that remains awake.

    **Replacement:** “Suspended compute costs $0 on Neon; PlanetScale's smallest HA Postgres cluster has a $15 monthly compute charge even when idle.”

11. **FACT — Unsupported competitive intent.** Hook.
    > Keep that Neon database awake all month at 0.25 CU and it costs 0.25 × 730 h × $0.106 = $19.35 before storage, more than the cluster it was meant to undercut.

    The formula is supported; the sheet does not say Neon was meant to undercut this cluster.

    **Replacement:** “Keep 0.25 CU awake for 730 hours on Neon Launch and compute costs 0.25 × 730 h × $0.106 = $19.35 before storage, versus $15 for PlanetScale PS-5 HA.”

12. **LOGIC — A price crossover becomes a capacity recommendation.** Decision matrix, one-CU row.
    > Past $148 ÷ $0.222 = 667 hours, the flat $148 cluster is the cheaper meter.

    The selected PS-80 HA is not demonstrated to replace the workload on one CU. The body acknowledges about 4 GB RAM per CU versus 8 GiB and replicas on PS-80, but the standalone matrix drops that qualification. It also presents a rounded threshold as an exact equality.

    **Replacement situation:** “Comparing one always-on Neon Scale CU with PS-80 HA compute prices”.
    **Replacement pick:** “PlanetScale PS-80 HA, only if its capacity suits the workload”.
    **Replacement reason:** “Compute charges cross at $148 ÷ (1 CU × $0.222/CU-hour) ≈ 666.67 h; this is a price comparison, not evidence of equivalent workload capacity.”
    Apply the same capacity caveat and approximate sign to the section 3 crossover sentence and the one-CU cost_math row.

13. **LOGIC — Rounding changes the checklist's decision boundary.** Section 6.
    > A 0.25 CU compute above 566 hours already costs more than PS-5 HA.

    The crossover is approximately 566.04 hours, not exactly 566; a duration just above 566 can still be below it. The snippet's rounded output should not become an exact rule.

    **Replacement:** “For compute only, compare awake hours with $15 ÷ (0.25 CU × $0.106/CU-hour) ≈ 566.04 h on Neon Launch.”
    Display the same precision in the snippet output, and label it approximate.

14. **LOGIC — Neki's restriction does not prove neither vendor can meet the requirement.** Decision matrix, production-sharding row.
    > Neki is a platform preview and PlanetScale says not to run production on it.

    That supports rejecting Neki for production, not the row's pick, “Neither — not Neki yet”; the sheet does not establish a Neon production-sharding capability or prohibition.

    **Replacement situation:** “Considering Neki for production sharding”.
    **Replacement pick:** “Do not use Neki”.
    **Replacement reason:** “PlanetScale explicitly excludes production workloads from Neki's platform preview.”

15. **LOGIC — Nightly suspension alone does not prove migration is uneconomic.** Decision matrix, final row.
    > Every suspended hour is $0 on Neon that a PlanetScale cluster would bill at its flat rate.

    This does not support “Neither — stay put”: total CU-hours, compute size, storage and transfer can change the result despite nightly suspension. This row also duplicates the idle-development scenario without adding a measured decision threshold.

    **Replacement situation:** “Need Launch's compute ceiling exceeded by a fixed-size deployment”.
    **Replacement pick:** “Neon Scale”.
    **Replacement reason:** “Launch autoscaling stops at 16 CU, while Scale offers fixed sizes up to 56 CU (224 GB RAM).”

16. **LOGIC — Branch totals hide different cost components.** Section 4 and branch cost_math row.
    > $15 plus CU-hours vs $300/month

    This result string compares Neon branch fees plus compute with PlanetScale cluster compute, omitting separately billed data storage and other charges. The body's “$15 + CU-hours” table cell has the same problem. The sheet supports these component estimates, not complete branch bills.

    **Replacement:** “Neon extra-branch fees: (20 − 10) × $1.50 = $15/month, plus compute and data storage; PlanetScale cluster compute: 20 × $15 = $300/month, plus separately billed charges.”

17. **LOGIC — Cost formula uses a slash as an ambiguous separator.** One-CU cost_math row.
    > 730 × $0.106 / 730 × $0.222 vs $148 flat

    In a formula field, the slash reads as division rather than two independent calculations; CU-hours and the workload-size caveat are absent.

    **Replacement:** “Neon Launch: 1 CU × 730 h × $0.106/CU-hour = $77.38; Neon Scale: 1 CU × 730 h × $0.222/CU-hour = $162.06; PlanetScale PS-80 HA arm64: $148/month for different capacity, compute only.”

18. **LOGIC — A preview limitation becomes a ban on evaluating it.** Section 6.
    > Neki is not a decision yet, because it is a preview.

    The restriction is on production workloads, not preview evaluation. The verdict's “Neki is a platform preview, so sharded Postgres on PlanetScale is not a production decision yet.” should use the explicit prohibition too.

    **Replacement:** “Do not run production workloads on Neki's platform preview; evaluate it only outside production.”

19. **META — Exposes the writing scaffold.** Section 1.
    > Each sentence forbids something.

    This describes the preceding prose rather than giving the reader a constraint. It is not the useful pricing-method disclosure at the end of the section.

    **Replacement:** “PlanetScale bills each branch as a dedicated cluster; Neon paid compute bills size multiplied by running hours.”

20. **SLOP — Symmetric punishment slogan substitutes for the cost distinction.** Section 3.
    > Neon punishes uptime.
    > PlanetScale punishes the night you paid for and did not use.

    The paired closer repeats the section's thesis without a usable condition.

    **Replacement:** “Compare billed CU-hours with the cluster charge before attributing savings to suspension.”

21. **SLOP — Hollow bridge.** Section 1.
    > Each model has a price.

    No information survives removing this sentence.

    **Replacement:** “PlanetScale has no free plan; Neon Free includes 100 CU-hours and 1 GB of Postgres storage per project.”

22. **BORING — Short slogan omits the reader's decision conditions.** Section 1.
    > The clock does.

    It neither identifies the target reader required by standard §3-3 nor states the concrete choice. The exact sheet facts that fix it are dedicated, separately billed PlanetScale branch clusters and Neon's CU-hour definition, with suspended compute at $0.

    **Replacement:** “For a Postgres deployment with idle periods or many branches, compare billed CU-hours with the cost of keeping a dedicated cluster for each branch.”

23. **WEAK — FAQ repeats the Neki section instead of changing a decision.** Final FAQ.
    > Yes: PlanetScale lists resharding, schema changes, version upgrades and failovers as online workflows, so you can start unsharded and reshard later.

    The adjacent answer sentence repeats router compatibility already introduced in the body. Standard §8-2 requires FAQ information absent from the sections; the current answer also omits the production prohibition. Replace the question and answer, rather than expanding this recap.

    **Replacement question:** “When do PlanetScale backups add charges?”
    **Replacement answer:** “PlanetScale runs automated backups every 12 hours and includes backup and WAL storage up to twice disk size; overage costs $0.023 per GB-month on compressed size.”

24. **SLOP — Verdict restates the opening choice without a new action.** verdict_summary.
    > Neon wins if your dev and test databases sleep at night and every pull request gets a branch, because suspended compute bills $0 and branch fees replace whole clusters.

    This repeats the section 6 opening and turns a conditional component comparison into a broad winner. Preserve the required conditional verdict, but give the reader an action and its scope.

    **Replacement:** “Choose Neon Launch when measured CU-hours plus branch, storage and transfer charges beat the corresponding PlanetScale bill; price always-on cluster compute separately before choosing PlanetScale.”

## REVISION BRIEF

- Remove the entire Drizzle hiring/sponsorship narrative and its heading reference; keep Neki's preview status and explicit production prohibition, without inventing a second PlanetScale bet.
- Limit every “flat” PlanetScale claim to cluster compute, including bold bullets, decision rows and the verdict; account separately for storage, backups and egress, and never promise a fixed total production bill.
- Distinguish suspended from merely idle Neon compute; scope paid CU-hour claims to paid plans, state that Launch suspension can be disabled, and remove every claim that probes prevent suspension or determine the winning vendor.
- Rework the opening for Postgres readers with idle periods or multiple branches; preserve the Vitess/MySQL engine constraint, delete the writing-scaffold sentence and unsupported competitive intent, and retain the useful dated vendor-pricing disclosure.
- Make all crossover arithmetic explicit and approximate: $15 ÷ (0.25 × $0.106) ≈ 566.04 h and $148 ÷ (1 × $0.222) ≈ 666.67 h; fix the snippet/checklist precision, separate the two one-CU formulas, and label comparisons as compute-only with non-equivalent capacity where applicable.
- Remove the invented preview lifetime; make branch comparisons explicitly $15 in Neon extra-branch fees versus $300 in PlanetScale cluster compute for the stated 20-branch scenario, with other charges excluded on both sides and running compute added on Neon.
- Keep the matrix actionable: qualify the PS-80 capacity recommendation, replace the unsupported “neither vendor” sharding claim with “do not use Neki for production,” and replace the unsupported stay-put row with the 16-CU-versus-56-CU ceiling decision.
- Replace the repeated Neki FAQ with the backup allowance and compressed-overage answer; remove hollow pricing and punishment slogans, and make the verdict direct a measured total-cost comparison rather than repeat the opening slogan.

DEFECTS: FACT=10 META=1 SLOP=3 LOGIC=8 RHYTHM=0 BORING=1 WEAK=1
