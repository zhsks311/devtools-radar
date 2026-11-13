# FACT SHEET — anthropic-vs-openai-api-pricing (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Never invent a benchmark, a cold-start figure, or a feature. Vendor marketing claims must be labelled as
the vendor's claim.

## Published unit prices and limits

- **Claude Sonnet 5.5** — $2 input / $10 output per MTok; 5m cache write $2.50; 1h write $4; cache hit $0.10; batch $1 / $5  
  source: https://docs.anthropic.com/en/docs/about-claude/pricing
- **Claude Opus 5.5** — $4 / $20 per MTok; writes $5 and $8; cache hit $0.20; batch $2 / $10  
  source: https://docs.anthropic.com/en/docs/about-claude/pricing
- **Claude Haiku 5.5** — $0.10 / $0.50 per MTok for prompts up to 100,000 tokens; $0.50 / $2.50 for prompts over it  
  source: https://docs.anthropic.com/en/docs/about-claude/pricing
- **Claude cache multipliers** — 5m write 1.25x, 1h write 2x, read 0.1x (0.05x on Opus 5.5 and Sonnet 5.5); multipliers stack with batch  
  source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- **Cache control correction, 2026-11-13** — Anthropic Messages opts in with top-level automatic or block-level explicit cache_control; n requests are one write plus n-1 hits; expiry requires a new write  
  source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- **Claude tokenizer** — Newer Claude tokenizers count approximately 30% more than earlier Claude tokenizers, depending on content; this is not a comparison with GPT  
  source: https://docs.anthropic.com/en/docs/about-claude/pricing
- **Claude modifiers** — Fast mode doubles the rate and is unavailable with Batch; US-only inference applies 1.1x to every token category  
  source: https://docs.anthropic.com/en/docs/about-claude/pricing
- **GPT-6.1 Sol** — $2 input / $10 output per MTok; cached input $0.10; 30m write $2.50; 12h write $5.00; batch and flex $1 / $5  
  source: https://platform.openai.com/docs/pricing
- **GPT-6.1 Sol long context** — $4 input / $15 output; cached $0.20; 30m write $5.00; 12h write $10.00  
  source: https://platform.openai.com/docs/pricing
- **GPT-6 Astra** — $10 / $50 per MTok, batch $5 / $25  
  source: https://platform.openai.com/docs/pricing
- **GPT-6 Luna** — $0.10 / $0.50 per MTok, batch $0.05 / $0.25  
  source: https://platform.openai.com/docs/pricing
- **OpenAI rate cards** — Standard, Batch, Flex and Fast are separate tables; Batch and Flex share the same numbers  
  source: https://platform.openai.com/docs/pricing

## Derived arithmetic used in the article (formula printed in the text)

- **100k requests, 16k cached prefix, 4k fresh input, 500 output** — Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits 90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = $800; output 100,000 × 500 = 50M × $10 = $500 ⇒ $1,844 with the stated equal billed token counts and rates; not a measured same-text comparison; assumes fresh input lies after the explicit cache breakpoint and is not written
- **Hypothetical sensitivity: 30% more input-category tokens, output unchanged** — Input categories: ($400 writes + $144 hits + $800 fresh input) × 1.30 = $1,747.20; unchanged output $500; total $2,247.20 ⇒ $403.20 above the $1,844 baseline (21.87%). Assumed input change only, not an observed Claude-versus-GPT difference.
- **One write plus n-1 reads of one unchanged prefix** — Sonnet 5.5 / GPT-6.1 Sol short write: 1.25 + 0.05(n-1) < n; n > 1.2632. At n=10: 1.25 + 9 × 0.05 = 1.70 versus 10. Long write at n=3: Sonnet 2 + 2 × 0.05 = 2.10; Sol 2.5 + 2 × 0.05 = 2.60 versus 3. ⇒ Short window saves 83% on the cached prefix over ten requests. Long windows break even at three total requests, assuming two successful hits.
- **Exactly two requests 12 hours apart, no intervening reuse** — Sonnet 1h: two expired/cold writes, 2 + 2 = 4. Sol 12h if hit: 2.5 + 0.05 = 2.55; if miss and rewritten: 2.5 + 2.5 = 5. Uncached: 1 + 1 = 2. ⇒ A 1-hour entry cannot be assumed to hit after 12 hours. Even the illustrative Sol hit costs more than two uncached passes; not a long-run schedule forecast.

## Sources

- https://platform.claude.com/docs/en/about-claude/pricing
- https://developers.openai.com/api/docs/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://claude.com/pricing
- https://developers.openai.com/api/docs/guides/prompt-caching
