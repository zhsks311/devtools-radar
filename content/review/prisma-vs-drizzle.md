# Prisma vs Drizzle — editorial review

1. **FACT — Storage charges are incorrectly excluded.** `sections[4].content`

   > Prisma Postgres bills one query as one operation, a unit that punishes N+1 loops and polling, not storage or seats.

   The operation meter does not eliminate the storage meter: Starter, Pro and Business charge storage overage. There is no per-seat charge. Evidence: fact sheet, “Prisma Postgres price sheet.”

   **Replacement:** “Prisma Postgres bills each query as an operation and charges separately for storage overage, but has no per-seat charge.”

2. **LOGIC — A Prisma upgrade comparison cannot select Prisma over Drizzle.** `decision_matrix[1].why`

   > The same test reproduced the vendor's 3x on warm lookups, about 0.60 ms against 0.19 ms per findUnique.

   The row picks Prisma for a long-running API, but the test compares Prisma 6.19.3 with 7.10.1, not Prisma with Drizzle. It measures sequential SQLite lookups, not general API throughput. The workload-based winner also appears in the last section and verdict.

   **Replacement:** “Alex Georgiev's local SQLite test found about 0.60 ms versus 0.19 ms per lookup across 2,000 sequential warm `findUnique` calls on Prisma 6.19.3 and 7.10.1 respectively, which informs a Prisma upgrade rather than a choice against Drizzle.”

3. **FACT — A single invoice is not established.** `sections[5].content`

   > Pick **Prisma** when one bill for database plus runtime beats an RC branch, and your workload is many warm queries rather than many cold starts.

   The sheet says Prisma sells Postgres and Compute; it does not promise one invoice or make either a requirement for its ORM. The same unsupported billing promise drives `decision_matrix[5]` and `verdict_summary`; remove it there too. The warm-query conclusion is separately addressed above.

   **Replacement:** “Evaluate Prisma Postgres and Prisma Compute as paid services separately from the free Prisma ORM, which does not require Prisma Postgres.”

4. **LOGIC — Hiring maintainers does not route the reader's invoice.** `sections[5].title`

   > Drizzle's meter reads $0, so the bill moves to whoever employs its team

   PlanetScale employs the team, but Drizzle users pay whatever database and runtime they choose. The following paragraph's juxtaposition sustains the same implication. Evidence: fact sheet, “Derived arithmetic” and “Ownership.”

   **Replacement:** “Drizzle's ORM is free; your database and runtime determine the infrastructure bill.”

5. **LOGIC — Vendor affiliation does not establish control over the reader's data layer.** `hook`

   > The choice is no longer generated client versus SQL builder; it is who ends up holding your data layer.

   Selling a database or hiring maintainers does not show that either vendor must hold the reader's data. The first section's title repeats this unsupported premise. Keep affiliation as a governance fact, not a replacement for the architecture comparison.

   **Replacement:** “Prisma generates its client, while Drizzle keeps the schema in TypeScript without a code-generation step; neither ORM has a per-seat price.”

6. **FACT — Client generation does not establish runtime ownership.** `sections[0].content`

   > - **Prisma:** the schema is a separate artefact compiled into a client, which is what lets Prisma own the query plan and now the runtime.

   The sheet establishes a generated client, a query compiler and an adapter; it does not establish this causal ownership claim. Prisma Compute is a separate product, not the inevitable runtime of a generated client.

   **Replacement:** “Prisma 7 generates its Rust-free client with `prisma-client`, and queries pass through a TypeScript/WebAssembly compiler and a JS driver adapter.”

7. **FACT — No client codegen is expanded into unsupported absolutes.** `sections[0].content`

   > - **Drizzle:** the TypeScript file is the schema, so there is nothing to generate and no engine to load.

   The sheet supports no code-generation step and no separate schema DSL, not the blanket engine claim; it explicitly says `drizzle-kit` generates migrations. Remove the matching engine assertion in the code comment too.

   **Replacement:** “Drizzle uses the TypeScript file as its schema without a client code-generation step or separate schema DSL, while `drizzle-kit` generates migrations.”

8. **FACT — Main-thread execution is not in the sheet.** `sections[1].content`

   > The compiler runs on the JS main thread, and Prisma's own AMA of 13 February 2026 concedes "cases where throughput is similar or slightly worse".

   The AMA explanation in the sheet contrasts JavaScript database access with a multi-threaded Rust runtime; it does not specify the compiler's thread placement.

   **Replacement:** “Prisma's AMA of 13 February 2026 attributes ‘cases where throughput is similar or slightly worse’ to database access from JavaScript instead of a multi-threaded Rust runtime.”

9. **LOGIC — A qualified throughput concession becomes an absolute parallelism penalty.** `sections[1].content`

   > Peak parallelism is the price.

   The preceding AMA quote reports some similar or slightly worse throughput, not a measured peak-parallelism limit.

   **Replacement:** “Prisma's throughput concession is a reason to measure your workload, not evidence of a universal parallelism penalty.”

10. **FACT — Release status, licensing and employment are presented as prohibitions.** `sections[2].title`

    > Drizzle forbids a stable 1.0, Studio source and a neutral owner

    The sheet says the newest release is an RC, Studio is not open source, and PlanetScale hired the team; it does not say Drizzle forbids a stable release or identify PlanetScale as its owner. Evidence: “Release status,” “Pricing,” “Ownership,” and “Do not claim.”

    **Replacement:** “Drizzle's newest release is 1.0.0-rc.5, with breaking changes to review before adoption.”

11. **FACT — A free licence is not zero runtime cost.** `sections[2].content`

    > Drizzle's philosophy costs nothing at runtime.

    The sheet gives a $0 tooling price, not a runtime-resource measurement; the database and runtime still have their own bills.

    **Replacement:** “Drizzle ORM and Kit are free and open source; database and runtime charges depend on the services you choose.”

12. **LOGIC — The newest RC does not establish the status of every selectable release.** `decision_matrix[2].why`

    > Drizzle's newest release on 10 November 2026 is 1.0.0-rc.5, not a stable 1.0.

    This is true, but the row jumps from the newest version's status to a product-wide winner for every team that bans RCs. The sheet does not inventory earlier versions or their suitability.

    **Replacement:** “A policy that forbids release candidates rules out adopting Drizzle 1.0.0-rc.5, its newest published release as of 10 November 2026.”

13. **FACT — Version-range update behaviour is invented.** `sections[2].content`

    > Pin the exact RC, because a version range on a candidate lets the next BREAKING list in unannounced.

    The sheet documents breaking changes, not package-manager range semantics or automatic update behaviour. The last checklist item also substitutes an exact pin for reviewing the release's compatibility risk.

    **Replacement:** “Before adopting 1.0.0-rc.5, review its breaking changes, including postgres-js parsers, `withReplicas` default routing and the `sqlite-proxy` rework.”

14. **LOGIC — The crossover formula changes the meaning of its variable.** `cost_math[0].formula`

    > $10 + $8 × (n − 1M) = $49 → n − 1 = 39 ÷ 8 = 4.875 → n = 5.875M operations/month

    The first expression treats `n` as operations, then the next treats it as millions of operations. Define the unit once; apply the same definition to the crossover formula in the body.

    **Replacement:** “For n measured in millions of operations per month, $10 + $8 × (n − 1) = $49 gives n = 1 + ($49 − $10) ÷ $8 = 5.875, or 5.875M operations/month.”

15. **FACT — Pro is not a flat $49 above the crossover.** `cost_math[0].result`

    > Above 5.875M operations a month, Pro at $49 is cheaper than Starter

    Pro includes 10M operations, then charges $2 per million; the draft's own 20M example totals $69. Distinguish its base fee from its total, including in the body phrase “the $49 plan.”

    **Replacement:** “Above 5.875M operations/month, Pro is cheaper than Starter on operation charges, with a $49 base covering 10M operations and $2 per million thereafter.”

16. **LOGIC — Always-on time is silently equated with active CPU time.** `cost_math[3].formula`

    > 0.5 vCPU × 730 h × $0.064 = $23.36; 1 GB × 730 h × $0.006 = $4.38; $23.36 + $4.38

    The supplied scenario's arithmetic is permitted, but the paid CPU unit is active vCPU-hours, not merely hours that a service exists. State continuous CPU activity as an assumption; the result also excludes outbound bandwidth, not just requests.

    **Replacement:** “Assuming 0.5 active vCPU continuously and 1 GB provisioned memory for 730 hours at paid rates, (0.5 × 730 × $0.064) + (1 × 730 × $0.006) = $23.36 + $4.38 = $27.74/month before request and outbound-bandwidth charges.”

17. **LOGIC — Different metrics are described as contradictory evidence.** `sections[3].content`

    > Two kinds of evidence disagree here.

    Smaller vendor-reported bundle output and a larger third-party `node_modules` directory measure different things; faster warm queries and slower cold starts can also coexist. Standard §6 requires comparable metrics, not a manufactured contradiction.

    **Replacement:** “Prisma's bundle-output claim and Alex Georgiev's local `node_modules` measurement describe different quantities, while his warm-query and cold-start measurements describe different execution phases.”

18. **LOGIC — Observed directory growth becomes an unproved causal attribution, with missing derivations.** `sections[3].content`

    > Both hold at once: the compiler shrank, yet per-database WASM builds in two sizes grew `node_modules` 31%.

    The sheet reports shipped compiler variants and directory totals; it does not isolate how much growth those variants caused. Keep Prisma's compiler-size comparison attributed to Prisma, and show formulas for both the 31% directory growth and the headline's 3.4x cold-start slowdown.

    **Replacement:** “In Georgiev's local SQLite comparison of Prisma 6.19.3 with 7.10.1, `node_modules` grew by (333.3 − 254.1) ÷ 254.1 × 100 ≈ 31%, while process start to first query slowed by 236 ÷ 69 ≈ 3.4x.”

19. **FACT — The Drizzle snippet asserts APIs absent from the only permitted source.** `sections[0].content`, code

    > import { sqliteTable, integer, text } from "drizzle-orm/sqlite-core";

    This is the offending code line rather than a prose sentence: the sheet does not document this import path, these APIs or their chained methods. The Drizzle schema declaration and Prisma generator configuration also do different jobs, contrary to standard §5's equivalent-example rule; neither supplies a complete equivalent query example. Do not invent more API details to make them runnable.

    **Replacement:** “Drizzle defines its schema in TypeScript and generates migrations with `drizzle-kit`; Prisma 7 generates its client with `prisma-client`.”

20. **FACT — A changed default is described as an absolute destination ban.** `sections[1].content`, code comment

    > // required since 7.10.1: the client no longer lands in node_modules

    The sheet says `output` is required and generation no longer targets `node_modules` by default, not that this destination is impossible.

    **Replacement:** “Since Prisma 7.10.1, the generator requires an explicit `output` field instead of generating the client into `node_modules` by default.”

21. **FACT — The historical framing invents a year and a causal transition.** `sections[0].content`

    > Neither ORM has a seat price, so the 2023 question of generated client versus SQL builder has become a supply-chain question.

    The fact sheet does not contain 2023 or this history; the absence of seat charges does not explain a shift to supply-chain risk. This opening also fails standard §3-3's requirement to identify a reader with a concrete condition.

    **Replacement:** “If you are choosing between Prisma's generated client and Drizzle's TypeScript schema, separate the free ORM decision from database pricing and release-candidate risk.”

22. **LOGIC — Pinning cannot satisfy an employer-independence requirement.** `decision_matrix[6].pick`

    > Neither — pin a version and keep the exit path documented

    The situation requires maintainers whom no database vendor pays. A pinned release does not change who employs its maintainers, and the sheet supplies no documented exit procedure.

    **Replacement:** “Neither meets the stated requirement: Prisma sells its own database, and PlanetScale employs Drizzle's core team.”

23. **WEAK — Shared sponsorship supplies no concrete tooling criterion.** `decision_matrix[4].why`

    > PlanetScale employs the core team, so the ORM's sponsor and your database vendor are the same company.

    The row repeats the situation's desire to deepen a relationship without identifying a capability or constraint. Replace the whole situation/pick/reason row with a tooling requirement supported by the sheet: free self-hosted Studio, with closed-source Studio acceptable; pick Drizzle. The exact supporting fact is Gateway's free Docker image or binary, alongside Studio's non-open-source licence.

    **Replacement:** “Choose Drizzle if you need free self-hosted Studio and accept that Studio is not open source, because Drizzle Gateway is available free as a Docker image or binary.”

24. **BORING — An upgrade sentence omits the actual breaking requirement.** `sections[1].content`

    > By 7.10.1 (15 October 2026) the idea had hardened into rules.

    The exact detail that fixes it is the required generator `output` field and the move away from the old datasource URL style toward `prisma.config.ts`, both in the architecture timeline.

    **Replacement:** “Prisma 7.10.1 shipped on 15 October 2026 with a required generator `output` field, while the upgrade guide replaces the old datasource URL style with `prisma.config.ts`.”

25. **SLOP — A teaser replaces the constraint it should name.** `sections[1].content`

    > The third rule is invisible in config.

    This adds no actionable fact and dresses a performance qualification up as another configuration prohibition. Introduce the AMA directly instead.

    **Replacement:** “Prisma's February 2026 AMA also qualifies the performance gains: some workloads have similar or slightly worse throughput.”

26. **LOGIC — A database-plan crossover is assigned to all ORM readers.** `sections[5].content`

    > Count monthly queries and place yourself against the 5.875M crossover.

    That threshold compares Prisma Postgres Starter and Pro operation charges, not ORM choices, arbitrary database bills or total infrastructure costs. Storage overage remains separate.

    **Replacement:** “If you use Prisma Postgres, compare Starter and Pro operation charges at 5.875M monthly operations, then account separately for storage overage.”

27. **SLOP — The verdict repeats the section's winner formula instead of advancing the decision.** `verdict_summary`

    > Drizzle wins if you want no codegen step and can pin 1.0.0-rc.5 in production, accepting that PlanetScale now employs its maintainers.

    The first two verdict sentences repeat the last section's picks; the second also repeats the unsupported invoice and cross-ORM performance claims. Standard §8-2 requires a new angle, and §7 requires an action ending. Replace the repeated winner sentences with a concrete adoption gate while retaining a scoped measurement action for existing Prisma users.

    **Replacement:** “Before adopting Drizzle 1.0.0-rc.5 for its lack of client codegen, review the release's breaking changes; before upgrading Prisma 6.19.3 to 7.10.1, measure process start to first query on your deployment target.”

## REVISION BRIEF

- Separate ORM architecture, vendor employment and paid hosting throughout: neither free ORM requires its adjacent database vendor, PlanetScale hired rather than acquired the Drizzle team, and the sheet does not promise one Prisma invoice.
- Replace the invented 2023 history with a conditional reader statement and a concrete decision outcome; retain the dated evidence-level disclosure rather than treating source attribution as process chatter.
- Limit benchmark conclusions to Alex Georgiev's local SQLite comparison of Prisma 6.19.3 and 7.10.1, including the 2,000 sequential warm lookups; never use it to declare a winner over Drizzle, and distinguish vendor bundle figures from directory size and cold starts.
- Remove the unsupported main-thread claim, absolute parallelism penalty, zero-runtime-cost claim and version-range update prediction; describe Drizzle's current RC status without claiming stable releases are forbidden or that an exact pin removes compatibility risk.
- Fix the crossover's units by defining n in millions of monthly operations, distinguish Pro's $49 base from its $2-per-million overage after 10M, show the 31% and 3.4x derivations, and label the Compute scenario's continuous active-CPU assumption plus its request and outbound-bandwidth exclusions.
- Restore storage charges to the pricing explanation and scope the 5.875M crossover to Prisma Postgres Starter versus Pro operation charges; do not present it as the crossover for either ORM or for the complete infrastructure invoice.
- Replace unsupported API snippets with source-supported architecture prose unless equivalent runnable examples can be established from the permitted sheet; preserve the explicit `output` requirement and the distinction between a changed generation default and a forbidden destination.
- Rework the decision matrix around actual gates: no codegen, willingness to adopt the named RC, free self-hosted Gateway with closed-source Studio acceptable, and the raw-SQL compiler bypass; remove sponsorship-only reasoning and pinning as a remedy for employer independence, then end with compatibility review and target-specific upgrade measurement rather than repeated winner slogans.

DEFECTS: FACT=12 META=0 SLOP=2 LOGIC=11 RHYTHM=0 BORING=1 WEAK=1
