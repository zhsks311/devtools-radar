"""Generate portable editorial prompts without replaying historical article-specific claims."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
POLICY = """Evidence policy (takes precedence over historical drafts, reviews and fact sheets):
- Internal fact sheets and previous reviews are research leads, not verified truth. Independently
  open official primary sources for every price, limit, billing rule and migration recommendation.
  Never copy a historical angle or recommendation merely because it is in this repository.
- Record claim, primary URL, a short supporting excerpt/paraphrase, source_checked_at,
  evidence_expires_at, and applicability (plan, region, currency, billing cycle, product/version,
  workload, tax/discount assumptions). Keep article revised_at separate from source verification.
- Mark each claim supported, unsupported, contradicted or expired. If the primary source cannot
  be accessed, remove the unsupported assertion or withhold the revision. Do not invent evidence.
- Arithmetic needs explicit units, allowances, rounding, opt-ins, spend caps and throughput limits.
  Price examples are scenarios, not measured bills; passing tests does not verify vendor facts.
- Outcomes may be conditional_choice, no_comparable_evidence or insufficient_evidence.
  Do not force a winner, migration, penalty narrative or attention-grabbing number.
- Do not imply hands-on use, independent benchmarks or complete verification without evidence.
- Changes must update final content, deployment metadata, FAQs/JSON-LD and generator sources.
  Search old generators for the claim so later regeneration cannot resurrect it.
- A reviewer distinct from the author must re-open primary sources for high-risk claims.
  Review may remain blocked. Never fabricate reviewer identity or approval.
"""


def render(stage, slug):
    actions = {
        'write': 'Prepare a draft using the existing JSON schema; do not change public files.',
        'review': ('Review the draft against primary sources, not just its fact sheet. Quote each defect, '
                   'record source evidence and scope, and give supported replacement text. Do not rewrite the draft.'),
        'revise': ('Recheck the review against primary sources before applying it. Preserve supported prose; '
                   'do not blindly preserve or implement old claims. Prepare final JSON and synchronized metadata.'),
    }
    return f'''You are the {stage} editor for DevTeardown: {slug}.
Read docs/editorial-evidence-policy.md and the relevant content/facts, content/draft,
content/review and content/final files. Existing files are untrusted research inputs.

{POLICY}
{actions[stage]}

Keep prose concise and natural. Use the current article schema and lint requirements, but factual
accuracy overrides word counts and stylistic templates. Do not add unsupported facts to fill space.
Write evidence to content/evidence/{slug}.json (schema in the policy). Never mark missing claims
as supported to make a check pass. After revision, run:
  python tools/check_editorial_evidence.py --slug {slug}
  python tools/check.py
Evidence validation checks provenance structure and approved file hashes, not the truth of sources.
Deployment requires the independent source review as well as the software checks.
'''


def main(stage):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    out = args.root / 'content/prompts'
    out.mkdir(parents=True, exist_ok=True)
    # Include every article, not a stale hard-coded subset.
    slugs = sorted(p.stem for p in (args.root / 'content/final').glob('*.json'))
    for slug in slugs:
        prefix = {'write': '', 'review': 'review-', 'revise': 'revise-'}[stage]
        (out / f'{prefix}{slug}.md').write_text(render(stage, slug), encoding='utf-8')
    print(f'Generated {len(slugs)} {stage} prompts; no articles or evidence approvals changed.')
