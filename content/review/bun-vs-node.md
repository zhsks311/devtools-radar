# Bun vs Node.js — review

1. **Quote:** “Bun bills you in the 3% of Node tests it still fails”

   **FACT — `sections[3].title`.** The percentage describes only `node:http`, not the Node test suite. The sheet supplies no overall failure percentage; the other module counts differ substantially.

   **Replacement:** “Bun's own node:http count leaves 415 − 403 = 12 tests failing.”

2. **Quote:** “If your service is your own code plus I/O, Bun wins: by its own count node:http passes 403 of 415 tests, and its documented gaps sit in native addons, the inspector, TLS introspection and async_hooks.”

   **LOGIC — `verdict_summary`, first sentence.** A partial module pass count does not establish suitability for arbitrary I/O or dependencies. The exclusion of ordinary HTTP from the gap list also ignores documented `http.Server`, server-option and `listen(handle)` differences.

   **Replacement:** “If your HTTP service depends on the `keepAlive` server option, do not switch it unchanged to Bun: Bun documents that option as a no-op.”

3. **Quote:** “Bun's own count puts node:http at 403 of 415 tests, and its documented gaps sit in addons, TLS introspection and async_hooks rather than plain request handling.”

   **LOGIC — `decision_matrix[0].why`.** The reason contradicts the documented HTTP gaps and cannot justify the unconditional Bun pick for this situation.

   **Replacement:** “Bun's own node:http count is 403 / 415; consider it only after checking whether your service depends on the unsupported server options, `http.Server` inheritance or `listen(handle)`.”

4. **Quote:** “If the service is your own code plus I/O, Bun wins.”

   **LOGIC — `sections[5].content`, bold verdict.** Ownership of the code says nothing about which HTTP, TLS, crypto or async-context APIs it uses. No evidence here establishes this broad winner.

   **Replacement:** “For an HTTP service, check Bun's documented server-option and API gaps before choosing it.”

5. **Quote:** “No reading client certs, no cert per hostname.”

   **FACT — `sections[4].content`, TLS bullet.** The sheet establishes missing `getPeerCertificate()` and unsupported `SNICallback`, not the impossibility of every way to implement either capability.

   **Replacement:** “If your gateway requires `getPeerCertificate()` or `SNICallback`, Bun's node:https does not provide those APIs.”

6. **Quote:** “The binary forbids partial upgrades; 1.4.0 (20 August 2026) moved the Rust rewrite, the Node compatibility target and the native ABI in a single release.”

   **FACT — `sections[0].content`, Bun bullet.** The release changes are sourced; the claim that the binary forbids partial upgrades is not. The sheet provides no upgrade-component policy.

   **Replacement:** “Bun 1.4.0, released on 20 August 2026, combined the Rust rewrite with a compatibility-target change from 24.3.0 to 26.3.0 and `NODE_MODULE_VERSION` 147.”

7. **Quote:** “a standards body ships a runtime on a published clock.”

   **FACT — `sections[0].content`, Node bullet.** The sheet documents Node's release calendar, not governance by a standards body.

   **Replacement:** “Node publishes a release calendar; v26 Lithium, v24 Krypton and v22 Jod are LTS.”

8. **Quote:** “If the repo ships native addons, instruments through the inspector, or needs an EOL date it can put in a roadmap, Node wins.”

   **LOGIC — `sections[5].content` and `verdict_summary`.** Native addons are not a categorical Bun exclusion: the sheet requires rebuilding Node 24 addons for ABI 147. The inspector count does not identify which instrumentation works, and the sheet supplies no EOL dates for the active LTS majors.

   **Replacement:** “Retain Node if your service requires APIs Bun lacks; if its native addons were built for Node 24, a Bun 1.4 migration requires rebuilding them for `NODE_MODULE_VERSION` 147.”

9. **Quote:** “In Bun, createHook is a stub and async ids are always 0, so the agent cannot correlate work.”

   **LOGIC — `decision_matrix[2].why`.** The premise establishes failure of correlation through those hooks and IDs, not every correlation mechanism an unspecified agent might use. Scope the situation to an agent that requires these APIs as well.

   **Replacement:** “Keep Node if your tracing agent requires `createHook` or distinct async IDs: Bun documents the hook as a stub and async IDs as always 0.”

10. **Quote:** “17 Apr 2023 → 24 Mar 2026 ≈ 35 months from first release to EOL, against a documented 30-month fix guarantee”

    **LOGIC — `cost_math[2].formula`.** The arithmetic is allowed, but the comparison mixes total release lifetime with the LTS fix window. It cannot establish an excess over, or shortfall against, the LTS promise. The result also stops at elapsed time rather than the upgrade decision.

    **Replacement:** “Node 20's first-release-to-EOL interval is 17 April 2023 → 24 March 2026 ≈ 35 months, not a measurement of its LTS fix window; it is now EOL, while Node 24 and 26 are LTS.”

11. **Quote:** “It deletes a build step.”

    **LOGIC — `sections[2].content`.** Default type stripping does not eliminate the build step for every TypeScript codebase. The same section lists syntax and configuration that it cannot handle, and the sheet explicitly retains separate type checking.

    **Replacement:** “Node can execute erasable TypeScript syntax, but code needing enums or tsconfig paths still needs separate tooling.”

12. **Quote:** “It does not make Node a compiler.”

    **FACT — `sections[2].content`.** The sheet does not make this categorical compiler claim; its precise limitation is that Node performs no type checking.

    **Replacement:** “Node performs no type checking; that remains a separate tool's job.”

13. **Quote:** “None of these shows up in a hello-world. All of them show up in production.”

    **FACT — `sections[4].content`, closing paragraph.** Neither universal workload claim is in the sheet. The gaps matter when a service uses the affected APIs, not merely because it runs in production.

    **Replacement:** “Also check async-context boundaries: Bun documents that `AsyncLocalStorage` context does not propagate into Worker/BroadcastChannel events.”

14. **Quote:** “Who pays for Bun's roadmap matters more than its start-up time”

    **LOGIC — `sections[5].title`.** The acquisition and executable-distribution facts do not establish this ranking of operational risks. No funding commitment or roadmap guarantee appears in the sheet.

    **Replacement:** “Bun stays MIT after Anthropic's acquisition; check compatibility before migrating.”

15. **Quote:** “The platform-team check is not speed. It is: who pays for this binary's roadmap, and does their product depend on my runtime?”

    **LOGIC — `sections[5].content`, blockquote.** This repeats the unsupported priority from the heading and leaves the proposed funding question unanswered. Claude Code shipping as a Bun executable does not establish a support commitment to the reader's service.

    **Replacement:** “Anthropic acquired Bun on 2 December 2025; Bun remains MIT and has no paid tier.”

16. **Quote:** “Neither Bun nor Node.js has a price, so neither bill ever reaches procurement.”

    **FACT — `hook`, first sentence.** Free runtimes do not establish how an organisation procures upgrade work or support. The sheet also explicitly permits commercial post-Maintenance-LTS Node support from partners.

    **Replacement:** “Both runtimes are free; for teams maintaining a Node service, the migration bill is compatibility work and native-addon rebuilds.”

17. **Quote:** “Two rules decide every upgrade:”

    **LOGIC — `sections[1].content`.** The following support-window and release-cycle rules do not decide compatibility work or whether TypeScript and native addons need changes. “Every” overstates what the evidence can settle.

    **Replacement:** “Starting with Node 27, the release cycle becomes annual: every major gets six months of Alpha, six months of Current, then LTS.”

18. **Quote:** “141 tests not passing across the two modules a debugger and test runner touch”

    **WEAK — `cost_math[1].result`.** Adding the module gaps hides which dependency should block the migration. The total is not a count of broken workflows or a labour estimate; keep the module-specific arithmetic and state its decision boundary.

    **Replacement:** “If your debugger or test runner depends on these modules, check the required APIs before migrating: Bun's counts leave node:inspector at 110 − 22 = 88 tests unpassed and node:test_runner at 81 − 28 = 53.”

19. **Quote:** “The same vendor load test shows the Vite dev server peaking at 233 MB on Bun versus 214 MB on Node, so Bun is not lighter everywhere.”

    **LOGIC — `faqs[1].a`, second sentence.** The preceding sentence describes the `hello.js` start-up benchmark, not a load test. The sheet lists the memory-under-load figures separately and gives their conditions.

    **Replacement:** “Separately, Bun's peak-memory figures under load, with 1,000,000 requests and 64 connections, put the Vite dev server at 233 MB on Bun versus 214 MB on Node.”

20. **Quote:** “Node charges you on someone else's schedule. Bun charges you on the tests it does not pass yet.”

    **SLOP — `sections[0].content`, closing paragraph.** The symmetric closer restates the invoice metaphor without adding a concrete constraint or action.

    **Replacement:** “For Bun 1.4, check whether your native addons have builds for `NODE_MODULE_VERSION` 147.”

21. **Quote:** “You keep a Node major for years, and you leave it on the project's date.”

    **SLOP — `sections[1].content`, closing blockquote.** This repeats the section heading and calendar metaphor after the dates have already supplied the evidence.

    **Replacement:** “If production still runs Node 20, plan a move to Node 24 or 26 LTS: Node 20 reached EOL on 24 March 2026.”

## REVISION BRIEF

- Replace the headline's overall “3% of Node tests” claim with the module-specific calculation `415 − 403 = 12`; attribute every Bun pass count to Bun and never treat it as application coverage.
- Remove the unconditional Bun recommendation for “own code plus I/O” from the section verdict, decision matrix and final verdict. Make the HTTP decision depend on the service's use of the documented `http.Server`, server-option and `listen(handle)` gaps; update both the matrix situation and its pick so they match the conditional reason.
- Remove the invented Node standards-body governance and Bun partial-upgrade prohibition. State the published Node release cycle and Bun 1.4's documented target/ABI changes instead; retain the verification date and vendor attribution, and identify the intended reader as a team maintaining a Node service.
- Scope TLS and tracing exclusions to required APIs: `getPeerCertificate()`, `SNICallback`, `createHook` and distinct async IDs. Remove the universal hello-world/production closer; add the documented `AsyncLocalStorage` Worker/BroadcastChannel boundary instead.
- Replace blanket native-addon rejection with the Node 24-to-ABI-147 rebuild condition. Make the migration checklist identify required addon builds and unsupported API dependencies before switching, and describe returning to Node as retaining the Node runtime and its required addon builds—not as a measured or guaranteed-cost rollback.
- Keep total Node 20 lifetime separate from the LTS fix guarantee; turn that cost row into the actionable EOL-to-LTS decision. Replace the combined debugger/test-runner total with the separate module gaps and an API-check decision; do not convert test counts into labour estimates.
- State that Node runs erasable TypeScript without type checking, not that it universally removes a build step or is categorically “not a compiler.” In the performance FAQ, separate the start-up benchmark from the memory-under-load figures and include the documented load conditions.
- Remove the unsupported roadmap-funding priority, procurement universal and repeated billing/calendar closers. Keep acquisition, licence and paid-tier facts distinct from compatibility advice; end with specific addon/API and production-version checks rather than another winner recap.

DEFECTS: FACT=7 META=0 SLOP=2 LOGIC=11 RHYTHM=0 BORING=0 WEAK=1
