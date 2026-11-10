# Docker vs Podman — defect review

1. **FACT — `sections[3].content`.**

   > That variable is the whole migration for CLI and Compose tooling; handlers using Docker-only API get rewritten.

   The environment variable selects an endpoint; it does not prove CLI or Compose compatibility. The sheet explicitly forbids a no-work drop-in claim and distinguishes the Docker v1.40 compatibility layer from the different runtime (facts: 58–71, 85–93).

   Replacement: “Point Docker tooling at the Podman socket with `DOCKER_HOST`, then check the required API calls and rewrite handlers that depend on Docker-only API surface.”

2. **FACT — `sections[0].title; repeated in the Podman blockquote`.**

   > Docker licenses the desktop; Podman has no licence to enforce

   No paid tier does not mean no licence: both Podman products use Apache License 2.0 (facts: 48–55). The blockquote repeats the error as “**Podman:** the runtime has no daemon; the desktop has no licence.” Replace that assertion too.

   Replacement: “Docker Desktop uses the Docker Subscription Service Agreement; Podman and Podman Desktop use Apache License 2.0 with no paid tier.”

3. **FACT — `sections[4].content and title`.**

   > Docker Business exists to sell that list.

   The preceding list asserts that Podman lacks SCIM and an image-access equivalent, introduces an unsupported “SOC 2 report,” and denies a support contact unless the reader buys a build. None of those negative capability claims or support entitlements is established. The sheet lists specific Business gates and separately identifies Red Hat enterprise support; it does not establish a SOC 2 report for either product (facts: 18, 41–43, 55–56). The title “Vendor-neutral also means nobody sells you control” has the same unsupported premise. Remove the negative list, not just this concluding sentence.

   Replacement: “Docker Business adds SSO, SCIM, Hardened Docker Desktop and Image Access Management; Red Hat separately offers enterprise support through Red Hat Build of Podman Desktop.”

4. **FACT — `decision_matrix[4].why`.**

   > SSO, SCIM and Image Access Management are gated at Business and Podman Desktop has no equivalent.

   The Business gates are documented; the categorical absence of Podman equivalents is not (facts: 41–56). Lack of a feature in this sheet is not evidence that a product lacks it.

   Replacement: “Choose Docker Business when SSO, SCIM and Image Access Management are required: those are documented Business plan gates.”

5. **LOGIC — `decision_matrix[6].why and pick`.**

   > Paying $3–$4 per 100 minutes is cheaper than an unowned socket that grants arbitrary code execution.

   There is no cost for staffing or securing a socket to compare with the runtime rate. Nor does the sheet establish that Testcontainers Cloud removes the stated CI-host responsibility or requires Docker Team (facts: 36–37, 66–69, 82–83). Replace this row with the supported pre-purchase decision: use the 4,000-minute scenario, not an invented security-cost comparison.

   Replacement: “For 4,000 Testcontainers Cloud runtime minutes per month, choose pre-purchase when that usage is committed: 4,000 ÷ 100 = 40 blocks, and 40 × $3 = $120/month versus 40 × $4 = $160/month on demand.”

6. **FACT — `hook, first sentence`.**

   > At 249 employees Docker Desktop costs your company $0; at employee 250, a 200-developer team owes 200 × $15 = $3,000 a month for the same binary.

   The free case also requires revenue below $10 million and the relevant small-business use case. The paid case silently chooses Team even though Pro and Business also include commercial Desktop use (facts: 20–25, 76–81). State both the revenue assumption and the selected plan.

   Replacement: “For a commercial company with annual revenue below $10 million, Docker Desktop is free at 249 employees; at 250 employees, choosing Docker Team for 200 developers costs 200 × $15 = $3,000/month for the same binary.”

7. **FACT — `hook, second sentence`.**

   > Docker's free tier is a headcount test, not a usage tier, and Podman has no seat to count.

   The small-business rule tests revenue as well as headcount; government eligibility also differs. The opening cannot reduce the rule to headcount (facts: 20–24).

   Replacement: “Docker Desktop’s small-business free tier requires both fewer than 250 employees and less than $10 million in annual revenue; Podman has no paid tier.”

8. **LOGIC — `sections[1].content, company table`.**

   > | 250 employees, or $10M+ revenue | 200 devs × $15 = $3,000/month = $36,000/year |

   Threshold crossing requires a paid subscription, not necessarily 200 seats of Team. The table must state its chosen seat count and plan, and expose the annualization rather than presenting the example as the universal bill (facts: 25, 76–81; standard §4 and §6).

   Replacement: “| 250 employees, or $10M+ revenue; 200 commercial Desktop users choosing Team | 200 × $15 = $3,000/month; $3,000 × 12 = $36,000/year |”

9. **FACT — `verdict_summary, first sentence`.**

   > A company already past 250 employees or $10M revenue that wants SSO, SCIM, image policy and CI minutes from one vendor should pay for Docker.

   “Past” excludes the exact boundary: the free tier already ends at 250 employees or $10 million revenue. The stated identity and image controls specifically select Business, whose price is quote-only (facts: 14, 20–25, 41–43).

   Replacement: “A commercial company with at least 250 employees or at least $10 million in annual revenue must pay for Docker Desktop; if it requires SSO, SCIM and Image Access Management, request Docker Business pricing.”

10. **FACT — `sections[0].content, Docker bullet`.**

   > Docker Engine and Moby stay open source; the desktop binary sits under the Docker Subscription Service Agreement, so SSO, SCIM and hardened builds live behind it.

   The binary’s licence does not explain individual plan entitlements. The sheet gates SSO, SCIM and Hardened Docker Desktop specifically at Business; “hardened builds” is not the listed feature name and can be confused with Hardened Images (facts: 15–18, 26–29, 41–43).

   Replacement: “Docker Engine and Moby stay open source; Docker Desktop uses the Docker Subscription Service Agreement, and Business adds SSO, SCIM and Hardened Docker Desktop.”

11. **FACT — `sections[2].content, Hardened Images table row; carry correction into cost_math[3]`.**

   > | Hardened Images | free for developers; "starting at $5k/repo" in production | How many repos ship? |

   The production offer includes compliance support, while enterprise DHI is separately quote-only and required for end-of-life software security. The unqualified row and production-repository example obscure a decision-changing exception (facts: 15–17, 84). Preserve the approved 12 × $5,000 = $60,000/year example, but identify the offer being calculated.

   Replacement: “| Docker Hardened Images | free for developers; production with compliance support starts at $5k/repo; enterprise pricing is quote-only | Does end-of-life software require enterprise DHI? |”

12. **LOGIC — `sections[5].content, opening recommendation`.**

   > **A company already past the threshold that wants central control and CI minutes should pay Docker.**

   “Central control” does not distinguish Team’s audit logs and RBAC from Business’s identity and image gates. Build Cloud minutes alone do not pick either plan; every plan includes a base allocation (facts: 34–35, 41–43). Make the conditional winner a specific plan.

   Replacement: “Choose Docker Business if you require SSO, SCIM or Image Access Management; choose Team if audit logs and role-based access control meet your governance requirements.”

13. **LOGIC — `sections[5].content, small-team recommendation`.**

   > A small team under the threshold should pick Podman while the port is cheap.

   Being small proves neither that the port is cheap nor that migration beats keeping free Desktop. The sheet gives no migration-time or labour-price estimate and explicitly requires Docker-only handler work and a socket-security decision (facts: 20–22, 85–93).

   Replacement: “Choose Podman below the free-tier limits if you can fund the Docker-only API changes and assign responsibility for socket access before crossing either limit.”

14. **WEAK — `decision_matrix[0].why`.**

   > Both cost $0 today, and the port is cheapest before 200 developers depend on Desktop.

   The row offers neither a supported migration-cost comparison nor a requirement that makes Podman the winner. The sheet’s 200 developers belong to a licence-cost example, not a migration-cost model (facts: 79–86). Add ability to fund the port and own socket access to the situation, then make the recommendation conditional on those requirements.

   Replacement: “Choose Podman below both free-tier limits if the team can fund Docker-only API changes and own socket security before growth triggers paid Desktop seats.”

15. **LOGIC — `decision_matrix[7].pick`.**

   > Neither — stay put until renewal

   Non-refundable assigned seats establish sunk spend, not a reason to defer migration work. The row’s own reason says to plan against renewal; paid access continues until the cycle ends (facts: 33, 39–40).

   Replacement: “Prepare the Podman port before renewal; cancelling Docker will not refund the unused paid period.”

16. **WEAK — `decision_matrix[2].pick`.**

   > Docker Team, or fund the port

   This offers both choices without a deciding requirement; revenue alone establishes payment eligibility, not Team rather than Pro. Add a need for audit logs and RBAC to the situation and name the conditional winner (facts: 25, 41–43; standard §4 forbids ties).

   Replacement: “Choose Docker Team if the company requires audit logs and role-based access control.”

17. **LOGIC — `decision_matrix[5].why`.**

   > Per-seat × headcount goes to $0 and the team can absorb the Docker v1.40 gap and the socket decision.

   The situation says the platform team owns CI sockets; that does not establish capacity to rewrite Docker-only handlers. Zero licence fees do not prove the migration is staffed (facts: 85–86). Add that capacity as an explicit condition rather than asserting it.

   Replacement: “Choose Podman if the platform team can also fund Docker-only API rewrites; licence fees become $0, but socket access remains its responsibility.”

18. **LOGIC — `sections[2].content, closing sentence`.**

   > Build Cloud punishes bursty CI: base minutes reset each cycle without accumulating, and bought extras expire.

   Expiry proves a risk from unused minutes, not that bursty CI is penalized. There is no workload distribution, allocation size or overage price supporting that conclusion (facts: 34–35).

   Replacement: “Build Cloud base minutes do not accumulate, and purchased extras expire at the end of the period; buy extras only for work you expect to consume within that period.”

19. **LOGIC — `sections[3].content, snippet comment`.**

   > # --time 0: no idle exit, so long CI jobs keep the socket

   The documented timeout measures inactivity, not job duration. A long job alone does not establish that the service needs a disabled inactivity timeout (facts: 61–62, 72).

   Replacement: “# --time 0 disables the inactivity timeout.”

20. **FACT — `sections[3].content, snippet`.**

   > sleep 1  # let the listener bind first

   The sheet supplies no one-second listener-startup guarantee. A fixed sleep also does not establish readiness, so the block cannot promise copy-paste execution on that basis (facts: 61–65; standard §5). Remove the background-start-and-sleep recipe and retain only the documented export with an already-listening rootless service as an explicit precondition.

   Replacement: “With a rootless Podman API service already listening, point Docker tooling at it with `export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock`.”

21. **FACT — `sections[3].content, snippet comment; repeated in sections[5]`.**

   > # Breaks next: anything needing Docker API newer than v1.40

   The sheet specifies a Docker v1.40 compatibility layer, not a demonstrated failure result for every newer API request. The later sentence “Skip Podman if your toolchain needs Docker API above v1.40, or nobody owns socket permissions.” repeats that absolute version-only exclusion (facts: 58–60, 92–93). Replace the comment and make the exclusion about required unsupported calls or unowned access.

   Replacement: “# Compatibility is Docker v1.40; check the API calls your tooling requires.”

22. **FACT — `sections[0].content, Podman bullet`.**

   > **Podman forbids** a sales motion.

   No paid Podman tier does not prohibit commercial support. The bullet’s later “nothing to sell you when you grow” repeats the error; Red Hat sells enterprise support (facts: 49, 55–56). Remove both sales prohibitions.

   Replacement: “Podman and Podman Desktop have no paid tier; Red Hat offers enterprise support through Red Hat Build of Podman Desktop.”

23. **FACT — `sections[1].title`.**

   > The bill arrives at employee 250, not at build 10,000

   10,000 builds is an invented number, and the title again omits the revenue trigger. The sheet permits the employee and revenue thresholds, not a build-count contrast (facts: 20–24, 79–81).

   Replacement: “Commercial Docker Desktop seats become paid at 250 employees or $10 million annual revenue.”

24. **FACT — `sections[1].content, last sentence`.**

   > Seat pricing punishes hiring, not usage: one container a week costs the same $15 as a thousand.

   The container counts and weekly scenario are absent from the sheet. $15 is Team’s rate, not a universal Desktop price (facts: 10–14, 32).

   Replacement: “Docker Team charges a flat $15 per user per month, so adding a user adds a seat charge rather than a container-usage charge.”

25. **FACT — `decision_matrix[1].situation`.**

   > 240 employees and hiring

   240 is not an approved scenario. The row also needs revenue below $10 million if it is describing a company that has not already crossed the free-tier limits (facts: 20–24, 79–81).

   Replacement: “A company at 249 employees, with annual revenue below $10 million, is hiring toward 250 employees.”

26. **FACT — `decision_matrix[2].situation`.**

   > 30 employees but $12M annual revenue

   Neither 30 employees nor $12M revenue is in the sheet. Use the approved revenue boundary and include the governance requirement needed by the corrected Team recommendation (facts: 20–24, 41–43).

   Replacement: “A company with fewer than 250 employees and annual revenue of $10 million or more requires audit logs and role-based access control.”

27. **FACT — `decision_matrix[4].situation`.**

   > 1,000+ engineers, identity team requires SSO, SCIM and registry policy

   1,000+ engineers is invented and contributes nothing to the documented Business gate. The requirements, not this headcount, select the plan (facts: 41–43).

   Replacement: “The identity team requires SSO, SCIM and Image Access Management.”

28. **LOGIC — `cost_math[0].result`.**

   > $36,000/year, previously $0

   The previous $0 assumes commercial use under both small-business limits before the threshold crossing, and the new amount assumes 200 users choosing Team. The row label names only headcount, so it omits essential assumptions (facts: 20–25, 79–81). Put those assumptions in the label or formula rather than implying every threshold crossing has this bill.

   Replacement: “For a commercial company below $10 million annual revenue moving from 249 to 250 employees, choosing Team for 200 Desktop users changes the licence bill from $0 to 200 × $15 = $3,000/month; $3,000 × 12 = $36,000/year.”

29. **LOGIC — `cost_math[1].formula`.**

   > 25 × $15 = $375/month vs 25 × $9 = $225/month

   The result gives annual totals without displaying the annualization. The sheet permits those totals but requires derived arithmetic to show its formula; the prose also must retain Pro’s lack of org audit logs and RBAC (facts: 3, 76–78; standard §6).

   Replacement: “For 25 developers, Team costs 25 × $15 = $375/month and $375 × 12 = $4,500/year; Pro costs 25 × $9 = $225/month and $225 × 12 = $2,700/year, but lacks org audit logs and role-based access control.”

30. **LOGIC — `sections[0].content, closing sentence`.**

   > So the question is not daemon vs daemonless; it is which organisation may legally run the free thing.

   The licence comparison does not eliminate runtime compatibility, migration work or socket security as deciding factors. It also never states the concrete reader outcome required before the comparison tables (facts: 20–29, 58–71, 85–93; standard §3-3).

   Replacement: “Choose paid Docker Desktop when its documented plan controls are required; choose Podman when eliminating licence fees justifies the Docker-only API port and socket-security responsibility.”

31. **WEAK — `faqs[0].a, first sentence`.**

   > Only unused seats can be removed on Team and Business, and cancelling has no pause and refunds no unused portion; access runs to the end of the paid cycle.

   The assigned-seat and no-refund rules already drive decision_matrix[7]; repeating them adds little to the decision. The new fact is the following sentence’s unpaid-invoice grace period. Change the question to “What happens if a Docker invoice is unpaid?” and keep that new fact instead of recapping cancellation (facts: 39–40; standard §8-2).

   Replacement: “An unpaid Docker invoice starts a 15-day grace period.”

32. **WEAK — `faqs[3].a, first sentence`.**

   > Podman Desktop lists VPN/proxy support and air-gapped installation options, plus multi-arch builds and GPU acceleration.

   Multi-arch builds and GPU acceleration do not answer the locked-down-network question. Keep the two network-relevant capabilities and attribute them to the vendor (facts: 52–54).

   Replacement: “Podman Desktop’s vendor lists VPN/proxy support and air-gapped installation options.”

33. **META — `faqs[3].a, last sentence`.**

   > Those are vendor descriptions, not tested here.

   “Not tested here” discusses the article’s production rather than helping the reader decide. Preserve evidence attribution in the preceding network-capability sentence, not this process aside; do not replace it with a claim of testing.

   Replacement: “Check which of those network and installation options matches your environment’s restrictions.”

34. **SLOP — `sections[0].content, standalone paragraph`.**

   > Each philosophy forbids something.

   This announces the structure without naming a constraint. The following matched “forbids” bullets then manufacture symmetry between a Desktop licence gate and a supposed ban on sales (standard §8). Replace the empty bridge and abandon the mirrored bullet premise.

   Replacement: “Docker Desktop’s commercial free tier has company-size limits; Podman has no paid tier but still requires a Docker API compatibility check.”

35. **SLOP — `verdict_summary, second sentence`.**

   > A small team under the threshold, or a large org that wants per-seat × headcount off the budget and can fund the port to a Docker v1.40 socket, should run Podman.

   This repeats the small-team and large-org recommendations from section 6 instead of giving the conclusion a new action or timing constraint (standard §8-2). It also calls the work a port “to a socket” rather than identifying the Docker-only API handlers.

   Replacement: “Before the next Docker renewal, identify Docker-only API handlers that need rewriting and assign responsibility for Podman socket access.”

## REVISION BRIEF

1. Qualify every free-to-paid example with commercial company use and both free-tier conditions: fewer than 250 employees AND less than $10 million annual revenue; payment starts at either boundary. Name Team whenever using $15 per user. Remove the invented 240-employee, 30-employee/$12M, 1,000-engineer, 10,000-build and container-count scenarios; use the approved 249-to-250 and revenue-boundary cases instead. Preserve the separate government payment rule.

2. State that Podman 6.1.4 and Podman Desktop 1.30.5 use Apache License 2.0 with no paid tier. Replace both “no licence” assertions and the sales-prohibition bullet. Keep Docker Engine and Moby’s open-source terms separate from Docker Desktop’s Subscription Service Agreement; describe Red Hat Build of Podman Desktop as enterprise support, not a paid Podman Desktop tier.

3. Delete the unsupported Podman capability-absence list, the SOC 2 assertion, the “nobody sells you control” title and the claim that Business sells that entire list. State only documented gates: Team adds audit logs and RBAC; Business adds SSO, SCIM, Hardened Docker Desktop and Image Access Management. Do not infer that Podman lacks equivalents because the sheet does not list them.

4. Replace the claimed one-variable migration with endpoint selection plus required-API checks, Docker-only handler rewrites and assigned socket ownership. Remove the background-start, fixed-sleep and unverified Compose-run recipe; retain the documented DOCKER_HOST export only with an already-listening rootless service as a precondition. Describe Docker v1.40 as the compatibility target, not proof that every newer call fails. Explain that --time 0 disables inactivity timeout, retain the direct Windows/macOS command limitation, and preserve the arbitrary-code-execution warning and mutual-TLS/SSH guidance.

5. Make every cost scenario identify its plan, seats, time unit and eligibility assumptions. Display 200 × $15 = $3,000/month and $3,000 × 12 = $36,000/year; display both monthly and annual formulas for the 25-developer Team/Pro comparison, retaining Pro’s org audit-log/RBAC gap. Keep the 4,000 ÷ 100 Testcontainers Cloud calculation. Qualify the 12 × $5,000 = $60,000/year DHI example as production with compliance support; state that enterprise DHI is quote-only and required for end-of-life software security. Keep Business quote-only and describe Build Cloud expiry as unused-minute risk, not a proven penalty for bursty CI.

6. Rebuild the eight matrix situations around explicit deciding requirements: a below-threshold team able to fund the port and own sockets; a 249-employee company below $10 million approaching 250; a below-250 company at $10 million or more needing audit logs/RBAC; government use with a feasible staffed port; required Business identity/image controls; a large platform team able to fund Docker-only rewrites as well as own sockets; committed 4,000-minute Testcontainers Cloud usage selecting pre-purchase; and assigned annual seats with migration prepared before renewal. Give each a conditional winner. Remove the unsupported Cloud-versus-socket cost comparison and the unsupported Docker Team requirement for Cloud; do not equate sunk subscription spend with a reason to delay migration preparation.

7. Refocus the cancellation FAQ on the new unpaid-invoice fact: ask what happens after non-payment and answer with the 15-day grace period, without duplicating that answer or the matrix’s seat/refund discussion. Limit the locked-down-network FAQ to vendor-listed VPN/proxy support and air-gapped installation options; remove unrelated GPU/multi-arch detail and the “not tested here” process aside. Preserve source attribution without inventing test results.

8. Replace “Each philosophy forbids something” and the mirrored forbids framing with concrete licence and compatibility constraints. State the conditional reader outcome before the comparison tables, retaining the verification date and vendor/document evidence level. End the verdict with a pre-renewal audit of Docker-only handlers and named socket-access responsibility rather than repeating the small-team/large-org recommendations. Keep paragraphs within four sentences and sections within 1,100 characters while revising.

DEFECTS: FACT=17 META=1 SLOP=2 LOGIC=11 RHYTHM=0 BORING=0 WEAK=4
