# Editorial evidence policy

Internal fact sheets, generated review prompts and historical reviews are research leads, not
certification. A software check can establish arithmetic or structural consistency, but cannot
establish that a vendor statement is current, applicable or true. Never describe all article
claims as verified merely because one defect was corrected or tests passed.

## Revision workflow

1. Inspect official primary sources independently of the existing fact sheet. For each high-risk
   price, limit, API, migration or purchasing recommendation, record the exact claim and applicability:
   plan, version, region, currency, billing cycle, included allowance, taxes, discounts and workload.
2. Label unsupported, contradicted or expired claims. Correct/remove them or withhold the revision.
   Source access failure is not evidence of truth. Quotations must stay short; do not archive full
   copyrighted pages in evidence records. No credentials or private customer data in records.
3. Calculate with explicit units, rounding, meter exclusions, opt-ins, spend caps and capacity.
   Throughput below a documented limit does not prove capacity. An example is not an observed bill.
4. Allow a conditional choice, no comparable evidence, or insufficient evidence. Do not force
   a winner, migration or invented loss-number hook. Factual uncertainty overrides style targets.
5. An independent reviewer reopens primary sources and checks the published high-risk claims in
   both final JSON and deployment metadata. Do not invent reviewer identities or approvals.
6. Update generator sources and search legacy generators for the old claim. Run merge before
   recording deployment hash. Run the evidence check and aggregate software checks before publication.
   Compare generated HTML/FAQ JSON-LD and the live deployed revision, not just a local draft.

## Machine-readable review record

`content/evidence/<slug>.json` is **not auto-generated approval**. Create it only after the review.
`article_sha256` and `deployment_sha256` use `tools.check_editorial_evidence.digest` on parsed
final JSON and its matching `data/tools.json` item. Any changed reviewed bytes invalidate approval.
Date fields use YYYY-MM-DD. `revised_at` is editing time; each `source_checked_at` is actual source
inspection time; `evidence_expires_at` is a deliberate recheck deadline, not vendor publication time.
No evidence records have been backfilled for existing articles. They remain legacy/unassessed.

```
{
  "schema_version": 1,
  "slug": "example-vs-example",
  "article_sha256": "<digest of final article>",
  "deployment_sha256": "<digest of deployment item>",
  "author": "<actual author>",
  "reviewer": "<actual distinct reviewer>",
  "review_status": "approved",
  "coverage": "all_published_high_risk_claims",
  "decision": "conditional_choice",
  "revised_at": "YYYY-MM-DD",
  "reviewed_at": "YYYY-MM-DD",
  "claims": [{
    "id": "unique-claim-id",
    "claim": "Exact scoped published claim",
    "status": "supported",
    "source_kind": "official_primary",
    "source_url": "https://vendor.example/pricing",
    "support": "Short excerpt or precise paraphrase supporting this claim",
    "scope": "Plan/version/region/billing cycle and all relevant conditions",
    "source_checked_at": "YYYY-MM-DD",
    "evidence_expires_at": "YYYY-MM-DD"
  }]
}
```

Run `python tools/check_editorial_evidence.py --slug <slug>`. Missing, stale, contradicted,
self-reviewed or hash-mismatched records fail. A syntactically valid false attestation can still
pass: independent editorial review remains mandatory. Claim completeness and URL authenticity
cannot be inferred by this script.

## Rollout limitations

This is a revision gate, not automatic certification or an automatic site-wide takedown.
The legacy site's general build does not require these new records yet. Existing articles are
preserved; the release coordinator must invoke the selected-article gate for each new revision.
Do not claim this change blocks all direct pushes or eliminates factual mistakes. Integrating
mandatory changed-article checks into CI requires a separately coordinated baseline/migration so
parallel factual corrections do not receive fabricated approvals just to unblock publication.
Historical `content/prompts`/`content/review` files may still contain bad directions: regenerate
prompts and follow this policy rather than replaying those files. Old hard-coded article writers
(`killer5*`, `polish*`, merge metadata) also require case-by-case review until consolidated.
