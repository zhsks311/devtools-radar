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
- **Claude tokenizer** — Claude 4.7 and later use a tokenizer producing approximately 30% more tokens for the same text  
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

- **100k requests, 16k cached prefix, 4k fresh input, 500 output** — Sonnet 5.5 or GPT-6.1 Sol: writes 10,000 × 16,000 = 160M × $2.50 = $400; hits 90,000 × 16,000 = 1,440M × $0.10 = $144; fresh 100,000 × 4,000 = 400M × $2 = $800; output 100,000 × 500 = 50M × $10 = $500 ⇒ $1,844 on either vendor at list price, before the tokenizer
- **The same workload through a tokenizer that counts 30% more** — $1,844 × 1.3 = $2,397.20, applying Anthropic's stated ~30% token increase ⇒ $2,397 against $1,844 for identical text, a 30% difference on a sheet whose per-token prices match
- **Cache break-even on a shared prefix** — 1.25 + 0.10n < n, so n > 1.39; at n = 10 the cost is 1.25 + 1.00 = 2.25 against 10 uncached ⇒ Profitable from the second request; 77.5% off the input line by the tenth
- **Long window write on a twice-daily job** — OpenAI 12h: 2.5 write + 0.10 read = 2.60, against 2 × 1.00 = 2.00 uncached. Anthropic 1h: 2.0 write + 0.10 read = 2.10, against 2.00 ⇒ 2.6 against 2.0: caching a prefix read twice costs more than not caching it under either vendor's long window

## Sources

- https://docs.anthropic.com/en/docs/about-claude/pricing
- https://platform.openai.com/docs/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://claude.com/pricing
