# Fact-check review — cursor-vs-github-copilot

Reviewed: `content/draft/cursor-vs-github-copilot.json` against `content/facts/cursor-vs-github-copilot.md`.
Standard applied: `docs/tech-blog-writing-standard.md` is not in the repo. I used the restatement of that standard in
`content/prompts/cursor-vs-github-copilot.md` (STEP 2 and the structured-field rules). I could not check section 8.

Measured: section content totals 4,796 chars (ceiling 4,800). There are 6 sections, each 708–945 chars. No paragraph has more than
3 sentences. The longest prose run without a visual anchor is 198 chars. Hook: 3 lines, 2 sentences. The matrix has 7 rows; there are 4 FAQs.
No RHYTHM violations. Every addition below must be paid for with cuts.

---

1. **META** (§2, last paragraph)
   Quote: "Start with what each contract refuses to bundle; the feature checklist comes later."
   Defect: This describes the article's structure. It also promises a feature checklist that the article never delivers.
   Replace: "Cursor's $8 Plus has no Claude or GPT; Copilot Free has no PR review."

2. **META** (§1, blockquote)
   Quote: "> Evidence: vendor pricing and acquisition documents, verified 10 November 2026; no independent performance measurements."
   Defect: This is the fact sheet's header turned into reader copy, with a methodology disclaimer used as a visual anchor.
   Replace: "> Cursor told Reuters it runs at about $2.6B annualised revenue; SpaceX bought it in an all-stock deal at a $60B valuation."

3. **META** (§4, blockquote)
   Quote: "> Default routing is a renewal risk to inspect, not an observed routing result in this comparison."
   Defect: This talks about "this comparison" and what the writer did or did not observe.
   Replace: "> Cursor states that Grok 4.6, the first joint model, scores between 69.9% and 70.8% on CursorBench and 61 on the Artificial Analysis Intelligence Index."

4. **META** (§3, first sentence)
   Quote: "Read these prices as penalties."
   Defect: This instruction leaked from the brief ("Read every price table as a penalty table"). It speaks to the writer, not the reader.
   Replace: (delete; open the paragraph with item 6's replacement.)

5. **FACT** (§3, blockquote)
   Quote: "> Subscription arithmetic only. Extra Copilot credits cost more; neither seat count predicts agent consumption."
   Defect: The sheet says only that extra credits are "purchasable on Pro and above". It gives no price and no comparison, so "cost more" is invented. "Subscription arithmetic only" is a disclaimer.
   Replace: "> Each Pro seat includes $15 of credits ($10 base + $5 flex); usage past that is bought as extra credits, so $100 and $300 are the least these teams pay."

6. **LOGIC** (§3, paragraph 1)
   Quote: "Cursor punishes heavy third-party use and rewards Grok loyalty; Copilot punishes agent breadth across seats and rewards staying inside GitHub's surfaces."
   Defect: Two sentences later the draft says "changing surfaces does not escape it". If every surface drains the same meter, staying inside GitHub's surfaces rewards nothing. "Across seats" implies pooled credits, but the sheet prices credits per user.
   Replace: "Cursor punishes Claude or GPT use, billed at API list price on top of the plan; Copilot punishes heavy agent use per seat, because agent mode, review, cloud and CLI all drain one per-user credit balance."

7. **LOGIC** (§6, blockquote)
   Quote: "> If your hard requirement is a fixed fee covering heavy third-party use, neither published offer establishes that contract. Stay put rather than assume it."
   Defect: The hook says the $20 all-you-can-eat tier no longer exists, so a reader has nowhere to "stay put". The sentence also ignores Copilot Pro+, which includes premium models including Opus inside a fixed $70 credit allotment.
   Replace: "> If you need Claude inside a known monthly allotment, Copilot Pro+ at $39 includes Opus within $70 of credits; Cursor bills third-party tokens at API list price on top of $30 Premium."

8. **LOGIC** (decision_matrix row 5)
   Quote: "Cursor excludes those tokens from the subscription and Copilot's credits remain metered." (pick: "Neither — stay put")
   Defect: The same "stay put" problem as item 7. Metered credits with a fixed allotment are the closest thing to the requirement, so "neither" is wrong.
   Replace: situation "Claude-class models must fit a known monthly allotment" · pick "GitHub Copilot Pro+" · why "Pro+ includes premium models including Opus inside $70 of monthly credits for $39, while Cursor bills third-party tokens at API list price on top."

9. **LOGIC** (§4, bullet 1)
   Quote: "- Compare the model you requested with the model actually used."
   Defect: Nothing in the article or the sheet shows that Cursor reports which model served a request. The check depends on data the reader may not have. The paragraph's "record the selected model, any routing changes" has the same problem. The observable signal is the separately billed third-party usage.
   Replace: "- On Premium, compare the separate third-party token charge with the Claude or GPT work your team believes it ran; a near-zero charge means that work did not run on third-party models."

10. **LOGIC** (decision_matrix row 3)
    Quote: "Free supports both surfaces with limited usage."
    Defect: Cursor Free also lists "limited agent and chat requests". The "why" does not rule Cursor out, so the pick does not follow. The CLI is the only claimed difference, and the sheet says nothing about a Cursor CLI.
    Replace: situation "A free trial must run inside JetBrains, Xcode or Neovim" · pick "GitHub Copilot" · why "Copilot Free includes agent mode, and GitHub lists those editors among its supported surfaces."

11. **BORING** (§3, penalty table, Copilot row)
    Quote: "| GitHub Copilot: $10 Pro with $15 GitHub AI Credits; $39 Pro+; $100 Max |"
    Defect: The cell drops the decision-changing numbers. The sheet gives Pro+ $70 credits plus "premium models including Opus" and Max $200 credits. The Opus fact sits in FAQ 4, but it is the main counterweight to Cursor's list-price third-party billing.
    Replace: "| GitHub Copilot: $10 Pro ($15 credits); $39 Pro+ ($70 credits, Opus included); $100 Max ($200 credits) |"

12. **WEAK** (cost_math row 1)
    Quote: "$10/user/month × 10 users = $100/month"
    Defect: This is Copilot against Copilot, with no Cursor figure, so it changes no choice. It also duplicates the §3 table word for word.
    Replace: label "10-seat team floor" · formula "Copilot Pro $10/user/month × 10 = $100/month vs Cursor Teams $30+/user/month × 10 = $300+/month" · result "Cursor's team floor is at least 3× Copilot Pro's, before any third-party tokens."

13. **WEAK** (cost_math row 2)
    Quote: "$10/user/month × 30 users = $300/month"
    Defect: This is the same multiplication with a bigger number. Linear scaling teaches the reader nothing.
    Replace: label "One Claude-dependent developer" · formula "Cursor Premium $30 + third-party tokens × API list price vs Copilot Pro+ $39 with $70 of credits" · result "Copilot's cost is fixed at $39 until the $70 of credits run out; Cursor's third-party cost has no published ceiling."

14. **BORING** (§1, first sentence)
    Quote: "If your renewal approval still assumes bundled model choice, the old editor budget is misleading."
    Defect: It has no numbers. The sheet has the replacement tiers.
    Replace: "A renewal priced on the old $20 tier now buys either $8 Plus, which is Grok-only, or $30 Premium, where Claude and GPT tokens bill at API list price on top."

15. **BORING** (§1, timeline bullet 3)
    Quote: "- 14 August 2026: the deal closed; Cursor joined SpaceXAI to work on Grok, Grok Build, Grok Bot and Cursor."
    Defect: "SpaceXAI" is never explained. Without the xAI absorption, §4's "a company whose model is Grok" has no support. The bullet also drops Grok API from the sheet's list.
    Replace: "- 14 August 2026: the deal closed; Cursor joined the SpaceXAI team (SpaceX absorbed xAI in February 2026) to work on Grok, Grok Build, Grok Bot, Grok API and Cursor."

16. **BORING** (§5, first sentence)
    Quote: "GitHub's counter-argument is distribution, not model neutrality."
    Defect: The article never says what "distribution" means. The surfaces list in the sheet appears only in FAQ 1.
    Replace: "GitHub's counter-argument is reach: Copilot runs in VS Code, Visual Studio, JetBrains, Xcode, Eclipse, Neovim, Zed and on github.com."

17. **BORING** (verdict_summary)
    Quote: "Grok-committed editor buyers should choose Cursor; GitHub review-centric teams should choose GitHub Copilot Pro or above."
    Defect: It has no prices and does not name the Claude-dependent buyer. Its "inspect model routing" advice repeats the unobservable check from item 9.
    Replace: "Teams content with Grok should choose Cursor, from $8 Plus; teams whose review runs through GitHub PRs should choose Copilot Pro at $10/user/month or above. Teams that need Claude should price Cursor Premium's $30 plus list-price tokens against Copilot Pro+'s $39 with $70 of credits."

18. **SLOP** (whole article: "not X" / "rather than" overuse, at least 10 instances)
    Quotes: "Choose by model dependence and review workflow, not completion quality." · "The acquisition is complete, not an option still awaiting exercise." · "Premium opens third-party access, not an included third-party allowance." · "GitHub's counter-argument is distribution, not model neutrality." · "It is not a no-agent demo." · "Pro buys access to repository-side work, not an unlimited agent budget." · "a subscription change is not a workflow migration." · "Plus's Grok-only restriction matches the requirement rather than obstructing it." · title "Copilot Free is a working entry point, not the review tier"
    Defect: The counterpunch construction is the article's default sentence shape.
    Replace (examples): title → "Copilot Free runs the agent; PR review costs $10". "The acquisition is complete, not an option still awaiting exercise." → "Cursor is now a wholly owned SpaceX subsidiary."

19. **SLOP** (§2, symmetric paragraphs)
    Quote: "GitHub's philosophy: the repository is the product, so AI must land in review, PRs and issues. That rules out treating the editor as an isolated purchase."
    Defect: This mirrors the Cursor paragraph clause for clause ("X's philosophy: … That rules out treating …"), so both read as a template. "Isolated purchase" says nothing a buyer can act on.
    Replace: "GitHub sells the repository, so Copilot's AI lands in PRs and reviews. That forbids giving review away: Free gets agent mode and the CLI, but PR review waits for the $10 Pro tier."

20. **SLOP** (§3, paragraph 2)
    Quote: "Third-party usage is outside Cursor's monthly price. GitHub's meter spans activities; changing surfaces does not escape it."
    Defect: This restates the table directly above it.
    Replace: "Cursor gives third-party tokens no allotment at all; Copilot's allotment runs out, and Pro and above then buy extra credits."

21. **SLOP** (§6, first sentence)
    Quote: "Grok-committed editor buyers and GitHub review-centric teams should choose Cursor and GitHub Copilot, respectively."
    Defect: It nearly duplicates verdict_summary. "Respectively" makes the reader map buyers to products backwards.
    Replace: "Teams happy on Grok should buy Cursor; teams whose review lives in GitHub PRs should buy Copilot Pro."

22. **SLOP** (§6, paragraph 1)
    Quote: "Buy the constraint you can accept."
    Defect: This is a hollow aphorism.
    Replace: "Cursor's $8 Plus undercuts Copilot Pro by $2, but only if Grok is enough."

23. **SLOP** (§6, paragraph 2)
    Quote: "Switching changes more than the invoice. Inventory model assumptions and review handoffs before moving; a subscription change is not a workflow migration."
    Defect: Three ways of saying "switching is work", none of them concrete.
    Replace: "Moving to Copilot puts custom instructions (`.instructions.md`) and PR review behind Pro; moving to Cursor puts Claude and GPT behind list-price billing."

24. **SLOP** (§1, paragraph 2)
    Quote: "Choose by model dependence and review workflow, not completion quality. The bill follows that choice."
    Defect: "The bill follows that choice" says nothing.
    Replace: "Two questions decide it: do you need non-Grok models, and does your review happen in GitHub PRs?"

25. **SLOP** (§2, last paragraph)
    Quote: "These are business constraints, not claims that either tool cannot edit code."
    Defect: This is a defensive hedge aimed at no claim the reader made.
    Replace: (delete; item 1's replacement carries the paragraph.)

26. **SLOP** (§5, paragraph 2)
    Quote: "The boundary is concrete."
    Defect: The sentence says nothing.
    Replace: (delete.)

27. **SLOP** (§4, bullet 2)
    Quote: "- Have reviewers judge the resulting changes, not the subscription label."
    Defect: No reader judges code by its subscription label, so the advice is empty.
    Replace: (delete.)

28. **SLOP** (§5, last paragraph)
    Quote: "Do not choose Free for a process that requires those paid gates."
    Defect: It restates the bullets two lines up.
    Replace: (delete; keep "Try the actual handoff from assigned work to reviewed PR before migrating the team.")

29. **SLOP** (§4, paragraph 2)
    Quote: "Keep the outputs for review."
    Defect: This is filler that ends a triad.
    Replace: (delete.)

30. **WEAK** (decision_matrix row 4)
    Quote: "The budget must include PR review without a paid subscription" → "Neither — stay put"
    Defect: No real buyer has this requirement, and "stay put" has no meaning now that the old tiers are gone.
    Replace: situation "Cheapest paid tier with AI PR review" · pick "GitHub Copilot Pro" · why "PR review starts at $10/user/month on Copilot; Cursor lists Bugbot code review on the $30 Premium tier."

31. **WEAK** (decision_matrix row 7)
    Quote: "Seat arithmetic establishes only the subscription floor, not consumption across the shared meter."
    Defect: The situation already presumes Copilot, so the row cannot change a choice.
    Replace: situation "One heavy agent user with a $100/month budget" · pick "Copilot Max if non-Grok models matter; Cursor Super if Grok suffices" · why "Max includes $200 of credits for $100; Super gives 15× Plus usage, and any third-party tokens still bill at API list price on top."

32. **WEAK** (faqs, Q3)
    Quote: "Cursor lists Super at $100/month with 15× Plus usage and priority model access at peak times."
    Defect: The answer is a bare price list with no cross-vendor anchor, so it changes no decision.
    Replace: "Super is $100/month for 15× Plus usage and priority model access at peak times, the same price as Copilot Max with $200 of credits. Ultra is $200/month for 50× Plus usage and earliest access to all products and models."

33. **BORING** (§2, GitHub bullet)
    Quote: "- GitHub's paid review and cloud-assignment gates make repository work part of the buying decision."
    Defect: It is abstract and repeats §5. The sheet has a sharper fact: Cursor Premium now sells code hosting (Origin) and code review (Bugbot), which moves Cursor onto GitHub's ground.
    Replace: "- Cursor is contesting that ground: Premium lists code hosting via Origin and AI code review via Bugbot."

34. **BORING** (§5, blockquote)
    Quote: "> Pro buys access to repository-side work, not an unlimited agent budget."
    Defect: It has no number. The sheet gives the credit allotment.
    Replace: "> Pro's $15 of monthly credits per user ($10 base + $5 flex) funds agent mode, code review and cloud work alike."

35. **BORING** (§6, closing line)
    Quote: "Today, bring a representative change to review and inspect its model choice and billed usage before approving renewal."
    Defect: It is vague and relies on the unobservable model check from item 9.
    Replace: "Today, list the workflows that need Claude or GPT, then price them on Cursor Premium at $30 plus API list-price tokens and on Copilot Pro+ at $39 with $70 of credits."

36. **BORING** (faqs, Q2)
    Quote: "Cursor lists code hosting through Origin and AI code reviews through Bugbot, alongside cloud agents and automations."
    Defect: After item 33, Origin and Bugbot are in the body. The answer also omits Premium's only quantitative fact.
    Replace: "Premium gives 4× the usage of Plus, the latest Grok models, cloud agents and automations, and Grok Bot."

37. **FACT** (§5, bullet 1)
    Quote: "- Free can exercise the local agent workflow before a subscription decision."
    Defect: The sheet says Free has "agent mode and CLI". It never says "local". The bullet also leaves out the Copilot-in-the-cloud gate the sheet lists.
    Replace: "- Free runs agent mode and the CLI; Copilot in the cloud starts at Pro."

---

## REVISION BRIEF

1. Delete every sentence that refers to evidence, verification, "this comparison", a later checklist, or how to read a table. Specifically: §1 "> Evidence: …", §2 "…the feature checklist comes later.", §3 "Read these prices as penalties.", and §4 "> Default routing is … in this comparison." In their place put the Reuters $2.6B / $60B all-stock blockquote (§1) and the Grok 4.6 blockquote (§4). Introduce the scores with "Cursor states": 69.9%–70.8% on CursorBench and 61 on the Artificial Analysis Intelligence Index. Say nothing about CursorBench methodology.
2. Use only numbers and claims from the fact sheet. Remove "Extra Copilot credits cost more" and "local agent workflow". In the §1 timeline, add "SpaceX absorbed xAI in February 2026" and "Grok API" so that §4's "a company whose model is Grok" is supported.
3. Rebuild the penalty argument in §3. The Copilot table cell must show $10 Pro ($15 credits), $39 Pro+ ($70 credits, Opus included) and $100 Max ($200 credits). Rewrite the punish/reward sentence around a per-user credit meter, and drop "rewards staying inside GitHub's surfaces". Move the Pro+/Opus fact into the body and use it in §6 and the verdict.
4. Remove all "stay put" advice from §6 and the decision matrix, because the hook says the old tiers are gone. Replace matrix rows 3, 4, 5 and 7 with: free trial in JetBrains/Xcode/Neovim → Copilot; cheapest AI PR review → Copilot Pro ($10 vs Cursor Premium $30 with Bugbot); Claude inside a known allotment → Copilot Pro+; $100 heavy user → Copilot Max ($200 credits) vs Cursor Super (15× Plus).
5. Replace both cost_math rows. Row 1: 10-seat floor, Copilot Pro $10 × 10 = $100 vs Cursor Teams $30+ × 10 = $300+. Row 2: one Claude-dependent developer, Cursor Premium $30 + list-price tokens vs Copilot Pro+ $39 with $70 credits. Make the §3 seat table match these rows or delete it so the numbers are not duplicated.
6. Base the §4 neutrality check on billing data, not on reporting of "model actually used". On Premium, the reader compares the separate third-party token charge with the Claude/GPT work the team believes it ran. Delete "Keep the outputs for review." and "Have reviewers judge…".
7. Cut the slop. Allow at most two "not X" / "rather than" constructions in the whole article. Delete "Buy the constraint you can accept.", "The boundary is concrete.", "These are business constraints…", "Do not choose Free for a process…" and "Switching changes more than the invoice…". Break the mirrored "X's philosophy: … That rules out treating …" pair in §2. In §2, use the Origin/Bugbot fact to show Cursor moving onto GitHub's ground.
8. Rebalance §5 and the FAQs. §5 opens with the surfaces list (VS Code, Visual Studio, JetBrains, Xcode, Eclipse, Neovim, Zed, github.com), adds the Copilot-in-the-cloud gate and gives Pro's $15 credits ($10 + $5 flex). FAQ 1 then covers only facts not already in the body: Raycast, SQL Server Management Studio and GitHub Mobile. FAQ 2 becomes Premium's 4× Plus usage, latest Grok models, cloud agents and Grok Bot. FAQ 3 anchors Super's $100 to Copilot Max's $100 with $200 credits. Re-run the length check: the total must be 3,200–4,800 (currently 4,796), so additions must be paid for with cuts. Each section must be 600–1,100 chars.

DEFECTS: FACT=2 META=4 SLOP=12 LOGIC=5 RHYTHM=0 BORING=9 WEAK=5
