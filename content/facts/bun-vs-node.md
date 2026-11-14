# FACT SHEET — Bun vs Node.js (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a version, or a feature. Vendor benchmark numbers must be labelled as the
vendor's own measurements. Nothing here is a price: both runtimes are free, so the "bill" in this
article is upgrade labour, compatibility surface, and native-module ABI.

## Bun (sources: https://bun.com/blog/bun-v1.4, https://bun.com/blog/bun-joins-anthropic,
https://bun.com/docs, https://bun.com/docs/runtime/nodejs-compat, https://github.com/oven-sh/bun/releases)

Licence and ownership
- MIT licensed. Statically links JavaScriptCore/WebKit under LGPL-2, which is why the licence file
  spells out relinking obligations.
- Anthropic acquired Bun; announcement dated 2 December 2025. Bun stays MIT and open source.
  Claude Code ships as a Bun executable (Bun's own statement). Bun's founder wrote at that time:
  "Today, Bun makes $0 in revenue." There is no paid Bun tier.
- Latest releases: 1.4.0 on 20 August 2026, 1.4.4 on 22 October 2026.

Version 1.4 (20 August 2026) — what changed
- Rewritten from Zig to Rust.
- Node.js compatibility target bumped from 24.3.0 to 26.3.0; `process.versions.node` reports 26.3.0
  and `NODE_MODULE_VERSION` is 147. That does not require every Node-API addon to be rebuilt.
- +1,517 tests from the Node.js test suite now pass (Bun calls it the largest compatibility jump
  since 1.0); over 2,900 issues fixed.
- Idle CPU down 5x, memory down up to 35%, Linux start-up 50% faster (vendor figures).
- New built-ins: `Bun.Image`, `Bun.WebView` (headless browser automation), `Bun.markdown`,
  `Bun.cron()`, `Bun.Terminal`, `Bun.JSON5`, `Bun.YAML`, `Bun.TOML`, `bun check` (type checker),
  `bun lint`, `bun fmt`, `bun run --parallel`, `bun test --parallel`.

Bun's own per-module pass counts against the Node 26.3.0 suite (Bun 1.4, vendor numbers)
- node:http 403 / 415 (rewritten)
- node:fs 349 / 358
- node:tls 191 / 224
- node:http2 261 / 280 (rewritten)
- node:stream 254 / 262
- node:worker 116 / 157
- node:process 160 / 190
- node:net 171 / 191
- node:module 68 / 93
- node:inspector 22 / 110
- node:repl 82 / 109
- node:test_runner 28 / 81
- node:sqlite 18 / 18 (100%), node:trace_events 30 / 30, node:quic 235 / 237, node:events 95%
- Bun states plainly: "Bun is not 100% compatible with Node.js yet."

Compatibility gaps named in Bun's own docs (https://bun.com/docs/runtime/nodejs-compat)
- node:http: `http.Server` does not extend `net.Server`; the `keepAlive` / `keepAliveInitialDelay`
  server options are no-ops; `listen(handle)` is ignored.
- node:https: `getPeerCertificate()` and `getCipher()` are missing; `setSecureContext()`,
  `addContext()`, `SNICallback` and `handshakeTimeout` are not supported.
- node:crypto: backed by BoringSSL, which lacks the `ed448`, `x448`, `rsa-pss`, `dsa`, `dh` and
  `ml-kem-512` key types, has no EC curve other than P-224/256/384/521 (no `secp256k1`) and lacks
  the CCM, OCB, XTS and `chacha20-poly1305` ciphers; `setEngine()` throws; `setFips()` is a no-op.
- node:async_hooks: `createHook`, `executionAsyncId`, `triggerAsyncId` are stubs and async ids are
  always 0; `AsyncLocalStorage` context does not propagate into Worker/BroadcastChannel events.
- node:cluster: HTTP servers in workers each bind their own socket, so HTTP request load-balancing
  across processes only works on Linux (via `SO_REUSEPORT`).
- node:module: `registerHooks`, `findPackageJSON`, `stripTypeScriptTypes` missing; `module.register`
  is a no-op.
- node:perf_hooks: never emits `gc`, `dns` or `resource` entries.

Vendor performance numbers (Bun's benchmarks, `hello.js`; label them as Bun's)
- Start-up on Linux: Bun 1.4 5.1 ms vs Node.js 26 27.2 ms; peak memory 14.6 MB vs 44.5 MB.
- Start-up on Windows: 15.5 ms vs 40.1 ms; peak memory 16.8 MB vs 32.5 MB.
- Peak memory under load (1,000,000 requests, 64 connections): fastify 120 MB vs Node 156 MB;
  Express 92 MB vs 145 MB; `node:http` 81 MB vs 107 MB; Next.js 285 MB vs 342 MB;
  **Vite dev server 233 MB vs Node 214 MB — Bun uses more here.**
- Binary size: Linux x64 77.0 MB, macOS arm64 61.2 MB (1.4.4 vintage).
- Package manager claim on the docs landing page: `bun install` "up to 30x faster than npm"
  (vendor marketing). 1.4.4 adds up to 3.2x faster hoisted installs from a warm cache on Linux.

## Node.js (sources: https://nodejs.org/en/about/previous-releases, https://nodejs.org/api/typescript.html)

Licence and support
- MIT licensed, no paid tier. Commercial support for releases past Maintenance LTS is sold by
  OpenJS Ecosystem Sustainability Program partners, not by the project.
- LTS status "typically guarantees that critical bugs will be fixed for a total of 30 months".

Release calendar (nodejs.org, as of 10 November 2026)
- v27 — Alpha, first released 29 October 2026.
- v26 "Lithium" — first released 5 May 2026, LTS.
- v25 — first released 15 October 2025, EOL 31 March 2026.
- v24 "Krypton" — first released 6 May 2025, LTS, last updated 27 October 2026.
- v22 "Jod" — first released 24 April 2024, LTS, last updated 20 October 2026.
- v20 "Iron" — first released 17 April 2023, EOL 24 March 2026.
- Odd-numbered majors become unsupported after six months. **Starting with Node.js 27 the cycle
  becomes annual: every major gets six months of Alpha, six months of Current, then LTS.**

TypeScript in Node (docs for v26.13.0)
- Type stripping is on by default (since v23.6.0 / v22.18.0) and stable since v25.2.0 / v24.12.0.
- `--experimental-transform-types` was removed in v26.0.0.
- Only erasable syntax runs: `enum`, `namespace` with runtime code, parameter properties and import
  aliases throw `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`; decorators are a parser error.
- `.tsx` is unsupported. `tsconfig.json` is ignored, so `paths` do not work.
- TypeScript inside `node_modules` is refused outright.
- Parsing needs WebAssembly; without it the parser throws `ERR_WEBASSEMBLY_NOT_SUPPORTED`.
- No type checking is performed — that is still a separate tool.

## Derived arithmetic you may use (show the formula in the text)

- node:http gap: 415 − 403 = 12 failing tests out of 415.
- node:inspector gap: 110 − 22 = 88 unimplemented tests; node:test_runner: 81 − 28 = 53.
- Distinguish stable Node-API from version-specific V8/native ABI. Test packages, OS, architecture and external dependencies; only affected packages need rebuilding or replacement.
- Node 20's life: 17 April 2023 → 24 March 2026 is about 35 months from first release, and the
  documented LTS guarantee is 30 months of fixes.

## Do not claim
- Do not call either runtime "paid", "enterprise", or "free tier" — neither has a price.
- Do not invent startup or memory numbers beyond the table above, and do not present Bun's
  benchmarks as independent.
- Do not claim Bun runs all npm packages, or that Node cannot run TypeScript at all: Node strips
  types, it just refuses non-erasable syntax and `.tsx`.
- Do not state Deno comparisons, V8 vs JavaScriptCore speed ratios, or "4x faster start" as a
  measured fact — Bun's docs phrase the 4x as a design goal.
- Do not claim Anthropic pays for Bun's development in exchange for a licence fee; the announced
  terms are ownership, not a price sheet.


## Targeted correction review — 2026-11-14
Node-API ABI stability differs from V8/version-specific ABI. Bun independently implements Node-API; test package compatibility, do not mandate a rebuild of every Node24 addon. Sources: https://nodejs.org/learn/modules/abi-stability and https://bun.com/docs/runtime/node-api .
Other claims retain their original review date; this is not a full re-verification.
