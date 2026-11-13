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

Correction, 13 November 2026: removed the unsupported cross-vendor 30% claim and the whole-bill multiplier. The other rate examples retain their original verification date.

## 3. Caching is a break-even test, not a discount

Both vendors sell the same shape: pay more to write a prefix, pay less to read it. The multipliers are where they part.

| Cache operation | Anthropic | OpenAI |
|---|---|---|
| Write, short | 1.25x, 5 minutes | 1.25x, 30 minutes |
| Write, long | 2x, 1 hour | 2.5x, 12 hours |
| Read (hit) | 0.1x, or 0.05x on 5.5 models | 0.05x |

A cached prefix costs 1.25 + 0.1n to serve n requests, against n uncached. The break-even is n = 1.39, so the second request already wins, and ten requests cost 2.25 instead of 10, a 77.5% cut on the input line. The long windows are worse deals for short runs: 2x + 0.1n beats n only from the third request, and OpenAI's 2.5x write needs three reads before it pays.

## 4. Batch is the one line where both sheets agree

Both vendors halve input and output for asynchronous work. Anthropic publishes the batch rows separately; OpenAI prints a Batch table and a separate Flex table at the same numbers.

| Batch, per million | Claude Sonnet 5.5 | Claude Opus 5.5 | GPT-6.1 Sol |
|---|---|---|---|
| Input | $1.00 | $2.00 | $1.00 |
| Output | $5.00 | $10.00 | $5.00 |

Anthropic's page says its cache multipliers stack with the batch discount. That combination is the cheapest published way to process a large, stable corpus: a cached prefix at 0.1x inside a batch, on a job that can wait. The trap is that a nightly single-run job has nothing to read from, and a cold cache write just adds 25% to a batch you could have submitted uncached.

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

The third is the cache window, and it is easy to lose money on. A 12-hour write costs 2.5x, so a job that runs twice a day should skip caching entirely rather than pay 2.5x for a prefix it reads once. Check the read count before enabling it: three reads is where the long window starts to earn.

## Cost arithmetic at volume

| Label | Formula | Result |
|---|---|---|
| 100k requests, 16k cached prefix, 4k fresh input, 500 output | Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits 90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = $800; output 100,000 × 500 = 50M × $10 = $500 | $1,844 with the stated equal billed token counts and rates; not a measured same-text comparison |
| Hypothetical sensitivity: 30% more input-category tokens, output unchanged | Input categories: ($400 writes + $144 hits + $800 fresh input) × 1.30 = $1,747.20; unchanged output $500; total $2,247.20 | $403.20 above the $1,844 baseline (21.87%). Assumed input change only, not an observed Claude-versus-GPT difference. |
| Cache break-even on a shared prefix | 1.25 + 0.10n < n, so n > 1.39; at n = 10 the cost is 1.25 + 1.00 = 2.25 against 10 uncached | Profitable from the second request; 77.5% off the input line by the tenth |
| Long window write on a twice-daily job | OpenAI 12h: 2.5 write + 0.10 read = 2.60, against 2 × 1.00 = 2.00 uncached. Anthropic 1h: 2.0 write + 0.10 read = 2.10, against 2.00 | 2.6 against 2.0: caching a prefix read twice costs more than not caching it under either vendor's long window |

## Decision matrix

| If this is you | Take | Because |
|---|---|---|
| A long, stable system prompt at high volume | Measure both on your workload | Compare measured input, cache-write, cache-hit and output usage at the applicable rates. The Claude tokenizer note does not supply a GPT comparison ratio. |
| Prompts that regularly pass 100,000 tokens | Weigh the long-context row first | OpenAI doubles input and multiplies output by 1.5 past the boundary; Haiku 5.5 lists a rate five times higher for prompts over 100,000 tokens. |
| Nightly batch of a few hundred thousand jobs | Batch API on either | Both halve input and output, and a single nightly pass has no cache to read from, so a cold write only adds 25%. |
| A job that runs every 12 hours over one corpus | No cache at all | The 12-hour write costs 2.5x and the 1-hour write has expired by the next run; two uncached passes cost 2.0 against 2.6. |
| Output-heavy generation, 500+ tokens per call | GPT-6.1 Sol over Opus 5.5 | Output is 5x input on both sheets, so the $10 against $20 output rate dominates the bill long before the input line does. |
| Streaming that a user is watching | Fast mode, at 2x | Opus 5.5 moves to $8 and $40 and GPT-6.1 Sol to $4 and $20, and fast mode cannot be combined with batch. |
| Data must stay in the US | Price the 1.1x before comparing | US-only inference multiplies every Claude token category by 1.1, cache writes and reads included, which changes a close comparison. |
| A prototype with prompts under 100,000 tokens | Claude Haiku 5.5 | $0.10 input and $0.50 output per million is a twentieth of the flagship rows, and the over-100k rate only applies when the prompt crosses the line. |

## Migration path

Moving between the two APIs is mostly a prompt rewrite, because the cache is the part that does not travel: Anthropic takes an explicit breakpoint marker, OpenAI caches a stable prefix automatically. Re-measure your token counts on the new tokenizer before you migrate pricing assumptions, since the same text will not bill the same number of tokens.

Everything asynchronous needs resubmission. Batch jobs, files and fine-tuned endpoints are per-vendor objects with no portable format, and model deprecations retire a SKU you may still be calling, so keep the model name in configuration rather than in code.

## Questions that change the decision

**Is prompt caching automatic on both?**  
No. Anthropic takes a cache_control marker on the block you want cached, and OpenAI caches a stable prefix automatically with no marker to place.

**Do the batch discount and the cache discount combine?**  
On Anthropic the page says cache multipliers stack with the batch discount. OpenAI publishes separate Batch and Flex tables at the same rates, and fast mode is excluded from batch on Anthropic.

**Does the 30% tokenizer note mean Claude costs 30% more than GPT?**  
No. Anthropic compares newer and earlier Claude tokenizers, not Claude with GPT. The difference depends on content. Measure each target model on the same input and account for generated output separately; this article provides no measured cross-vendor ratio.

**Is a cache write ever a loss?**  
Yes. The 1.25x short write needs a read to pay for itself and the 2x or 2.5x long write needs two or three, so a job that reads the prefix once bills more with caching than without.

## Sources

- https://platform.claude.com/docs/en/about-claude/pricing
- https://developers.openai.com/api/docs/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://claude.com/pricing

## Same task, two SDKs

**Anthropic**

```
// Anthropic bills the prefix once: the breakpoint is a marker, not a hint.
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-sonnet-5-5",
  max_tokens: 512,
  system: [{
    type: "text",
    text: SYSTEM_PROMPT,
    cache_control: { type: "ephemeral" }, // 1.25x write, then 0.10x reads
  }],
  messages: [{ role: "user", content: question }],
});
// Breaks when: the breakpoint sits after a timestamp or a user id. Every request
// then writes a new prefix and pays 1.25x instead of reading at 0.10x.
console.log(msg.usage);
```

**OpenAI**

```
// OpenAI caches automatically: there is no marker, only a prefix to keep stable.
import OpenAI from "openai";
const client = new OpenAI();

const res = await client.responses.create({
  model: "gpt-6.1-sol",
  input: [
    { role: "system", content: SYSTEM_PROMPT }, // byte-identical every call
    { role: "user", content: question },
  ],
});
// Breaks when: the system prompt is assembled with a date or a request id.
// A changed prefix is a cache miss billed at the full $2 per million.
console.log(res.usage?.input_tokens_details);
```
