# Anthropic vs OpenAI — a 2026 cost teardown

> Claude Sonnet 5.5 and GPT-6.1 Sol list the same standard rate: $2 per million input tokens and $10 per million output. Equal rates do not establish equal costs for the same documents. Count each model separately; there is no measured Claude-versus-GPT token ratio established here.

*Prices verified 2026-11-10. Category: AI & LLM APIs. Author: DevTeardown Team.*

## Verdict

The named standard rows match: $2 input, $10 output and $0.10 cached input per million tokens. That does not make the same task equally expensive. Measure token usage, output quality, cache hits and retries on a representative sample. Apply the selected model, context and service-tier rates to those measurements; do not multiply a vendor bill by an assumed tokenizer premium.

## 1. Two sheets, one identical sticker

The flagship rows of both price sheets match to the cent, and so do the cache reads.

| Per million tokens | Claude Sonnet 5.5 | GPT-6.1 Sol |
|---|---|---|
| Input | $2.00 | $2.00 |
| Output | $10.00 | $10.00 |
| Cached input (hit) | $0.10 | $0.10 |
| 5m or 30m cache write | $2.50 (1.25x) | $2.50 (1.25x) |
| Batch input / output | $1.00 / $5.00 | $1.00 / $5.00 |

Anthropic's Opus 5.5 sits one rung up at $4 and $20, with cache reads at $0.20. OpenAI's GPT-6 Astra sits at $10 and $50. On the flagship row there is nothing to choose, which is the first sign that the model price is not the decision.

## 2. The tokenizer note is not a cross-vendor benchmark

Anthropic describes a tokenizer change between newer and earlier Claude models, not between Claude and GPT. Its approximate 30% increase depends on the text and workload. That note cannot establish a fixed Claude-versus-OpenAI price premium.

There is no universal source-token unit shared by the two vendors. Count the same representative input with each target model, then record actual output usage separately. Generated answers may differ in length, reasoning usage and quality; an input-token ratio does not predict output tokens.

The $1,844 example below assumes equal billed token counts in each category. It is arithmetic, not a measured identical-text benchmark. The separate input-only sensitivity case deliberately leaves the $500 output line unchanged and is not a prediction for either vendor.

Correction, 13 November 2026: removed the unsupported cross-vendor 30% claim and the whole-bill multiplier. Cache controls, hit rates and reuse arithmetic were also corrected on this date; other rates retain their original verification date.

## 3. Caching is a break-even test, not a discount

For standard short-context Sonnet 5.5 and GPT-6.1 Sol, the hit rate is $0.10 / $2.00 = 0.05x; other models differ.

| Cache operation | Sonnet 5.5 | GPT-6.1 Sol |
|---|---|---|
| Short write | 1.25x, 5m | 1.25x, 30m |
| Long write | 2x, 1h | 2.5x, 12h |
| Hit | 0.05x | 0.05x |

Let n be total requests, including the cold first request. One write and n-1 successful full-prefix reads cost w + r(n-1), not w + rn. This excludes fresh input and output and assumes no intervening expiry, prefix change or rewrite.

Short writes: 1.25 + 0.05(n-1) < n means n > 1.2632. At ten requests, 1.25 + 0.05 × 9 = 1.70 versus 10 uncached: 83% less for this prefix alone. With a 0.1x model the corresponding total is 2.15, a 78.5% reduction.

Long writes at 0.05x reads need three total requests (one write, two hits): Sonnet costs 2.10 and Sol costs 2.60 versus 3 uncached. Never count an expired entry as a hit.

## 4. Batch is the one line where both sheets agree

Both vendors halve input and output for asynchronous work. Anthropic publishes the batch rows separately; OpenAI prints a Batch table and a separate Flex table at the same numbers.

| Batch, per million | Claude Sonnet 5.5 | Claude Opus 5.5 | GPT-6.1 Sol |
|---|---|---|---|
| Input | $1.00 | $2.00 | $1.00 |
| Output | $5.00 | $10.00 | $5.00 |

Anthropic's page says its cache multipliers stack with the batch discount. For Sonnet 5.5, apply the 0.05x hit multiplier to the applicable batch input rate only for an actual cache hit; a batch does not guarantee reuse. The trap is that a nightly single-run job has nothing to read from, and a cold cache write just adds 25% to a batch you could have submitted uncached.

## 5. Long prompts are where the sheets stop being comparable

Both vendors reprice the prompt once it gets long, and they do it in different shapes.

| Prompt size | GPT-6.1 Sol | Claude Haiku 5.5 |
|---|---|---|
| Short context, input | $2.00 | $0.10 up to 100,000 tokens |
| Long context, input | $4.00 | $0.50 over 100,000 tokens |
| Long context, output | $15.00 | $2.50 over 100,000 tokens |

OpenAI's long-context row doubles input and multiplies output by 1.5. Anthropic's Haiku sheet lists two rows, one for prompts up to 100,000 tokens and one for prompts over it, at five times the rate, and it does not print a marginal split.

A 200,000-token prompt therefore bills at 0.2 × $0.50 = $0.10 on the over-100k row against $0.02 if the same prompt fit under the line. That cliff, not the per-token sticker, is what a document pipeline hits when someone pastes a whole contract set.

## 6. Three add-ons that quietly change the unit

Fast mode on both sides doubles the sticker: Opus 5.5 goes to $8 input and $40 output, GPT-6.1 Sol to $4 and $20. Anthropic notes that fast mode is not available with the Batch API, so the two savings cannot be stacked.

Data residency is a multiplier rather than a tier. Sending Claude 4.6 or later to US-only inference applies 1.1x to every token category, cache writes and reads included.

For exactly two requests 12 hours apart, with no intervening reuse: Anthropic's 1-hour entry has expired: two cold writes cost 2 + 2 = 4 prefix units, not 2 + a cache read. 

For GPT-6.1 Sol, a successful 12-hour-cache hit would cost 2.5 + 0.05 = 2.55 across the pair; two cold writes cost 5. Both exceed two uncached passes at 2. 

This is not a long-run forecast: measure hits, writes and refreshes before extrapolating.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 100k requests, 16k cached prefix, 4k fresh input, 500 output | Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits 90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = $800; output 100,000 × 500 = 50M × $10 = $500 | $1,844 with the stated equal billed token counts and rates; not a measured same-text comparison; assumes fresh input lies after the explicit cache breakpoint and is not written |
| Hypothetical sensitivity: 30% more input-category tokens, output unchanged | Input categories: ($400 writes + $144 hits + $800 fresh input) × 1.30 = $1,747.20; unchanged output $500; total $2,247.20 | $403.20 above the $1,844 baseline (21.87%). Assumed input change only, not an observed Claude-versus-GPT difference. |
| One write plus n-1 reads of one unchanged prefix | Sonnet 5.5 / GPT-6.1 Sol short write: 1.25 + 0.05(n-1) < n; n > 1.2632. At n=10: 1.25 + 9 × 0.05 = 1.70 versus 10. Long write at n=3: Sonnet 2 + 2 × 0.05 = 2.10; Sol 2.5 + 2 × 0.05 = 2.60 versus 3. | Short window saves 83% on the cached prefix over ten requests. Long windows break even at three total requests, assuming two successful hits. |
| Exactly two requests 12 hours apart, no intervening reuse | Sonnet 1h: two expired/cold writes, 2 + 2 = 4. Sol 12h if hit: 2.5 + 0.05 = 2.55; if miss and rewritten: 2.5 + 2.5 = 5. Uncached: 1 + 1 = 2. | A 1-hour entry cannot be assumed to hit after 12 hours. Even the illustrative Sol hit costs more than two uncached passes; not a long-run schedule forecast. |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| A long, stable system prompt at high volume | Measure both on your workload | Compare measured input, cache-write, cache-hit and output usage at the applicable rates. The Claude tokenizer note does not supply a GPT comparison ratio. |
| Prompts that regularly pass 100,000 tokens | Weigh the long-context row first | OpenAI doubles input and multiplies output by 1.5 past the boundary; Haiku 5.5 lists a rate five times higher for prompts over 100,000 tokens. |
| Nightly batch of a few hundred thousand jobs | Batch API on either | Both halve input and output, and a single nightly pass has no cache to read from, so a cold write only adds 25%. |
| Only two requests, 12 hours apart, no intervening reuse | Compare against uncached input | Sonnet 1h writes cost 4 prefix units after expiry; Sol 12h costs 2.55 with one hit or 5 with a rewrite, versus 2 uncached. A recurring workload needs its own observed hit/write history. |
| Output-heavy generation, 500+ tokens per call | GPT-6.1 Sol over Opus 5.5 | Output is 5x input on both sheets, so the $10 against $20 output rate dominates the bill long before the input line does. |
| Streaming that a user is watching | Fast mode, at 2x | Opus 5.5 moves to $8 and $40 and GPT-6.1 Sol to $4 and $20, and fast mode cannot be combined with batch. |
| Data must stay in the US | Price the 1.1x before comparing | US-only inference multiplies every Claude token category by 1.1, cache writes and reads included, which changes a close comparison. |
| A prototype with prompts under 100,000 tokens | Claude Haiku 5.5 | $0.10 input and $0.50 output per million is a twentieth of the flagship rows, and the over-100k rate only applies when the prompt crosses the line. |

## Migration path

Caching controls are not interchangeable. Anthropic Messages is opt-in: top-level cache_control selects an automatic moving breakpoint; block-level cache_control selects explicit breakpoints. GPT-6.1 Sol supports implicit caching and explicit-only breakpoints. Re-measure token usage on migration, rather than transferring an assumed token ratio.

The worked bill uses explicit boundaries around the stable prefix, leaving fresh input outside the write. Batch jobs, files and model-specific configuration also need review when switching providers.

## Questions that change the decision

**Is prompt caching automatic on both?**  
Anthropic Messages requires opt-in: use top-level cache_control for automatic breakpoint placement, or block-level cache_control for explicit boundaries. GPT-6.1 Sol supports implicit caching by default and explicit-only controls. Automatic placement does not guarantee a hit.

**Do the batch discount and the cache discount combine?**  
On Anthropic the page says cache multipliers stack with the batch discount. OpenAI publishes separate Batch and Flex tables at the same rates, and fast mode is excluded from batch on Anthropic.

**Does the 30% tokenizer note mean Claude costs 30% more than GPT?**  
No. Anthropic compares newer and earlier Claude tokenizers, not Claude with GPT. The difference depends on content. Measure each target model on the same input and account for generated output separately; this article provides no measured cross-vendor ratio.

**Is a cache write ever a loss?**  
Yes. For Sonnet 5.5 and GPT-6.1 Sol, count one cold write plus n-1 hits across n requests, with a 0.05x hit rate. Short writes need two total requests; long writes need three. Expiry or changed prefixes add writes, not discounted reads.

## Sources

- https://platform.claude.com/docs/en/about-claude/pricing
- https://developers.openai.com/api/docs/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://claude.com/pricing
- https://developers.openai.com/api/docs/guides/prompt-caching

## Same task, two SDKs

**Anthropic**

```
// Explicit system-prefix caching; top-level cache_control is another opt-in option.
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-sonnet-5-5",
  max_tokens: 512,
  system: [{
    type: "text",
    text: SYSTEM_PROMPT,
    cache_control: { type: "ephemeral" }, // 1.25x write, then 0.05x reads
  }],
  messages: [{ role: "user", content: question }],
});
// Breaks when: the breakpoint sits after a timestamp or a user id. Every request
// then writes a new prefix and pays 1.25x instead of reading at 0.05x.
console.log(msg.usage);
```

**OpenAI**

```
// Explicit-only mode keeps the fresh question outside the cached prefix.
import OpenAI from "openai";
const client = new OpenAI();
const res = await client.responses.create({
  model: "gpt-6.1-sol",
  prompt_cache_options: { mode: "explicit", ttl: "30m" },
  input: [
    { role: "developer", content: [{ type: "input_text", text: SYSTEM_PROMPT,
      prompt_cache_breakpoint: { mode: "explicit" } }] },
    { role: "user", content: question },
  ],
});
// Without a reusable prefix, explicit mode with no breakpoints avoids writes.
console.log(res.usage?.input_tokens_details);
```
