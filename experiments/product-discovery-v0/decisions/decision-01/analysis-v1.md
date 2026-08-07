# Decision 01 — one or multiple sensemaking attempts

## 1. Decision
Should the normal invocation spend one attempt and expose uncertainty, run a fixed ensemble, or request another independent attempt only when the first result is decision-sensitive?

## 2. Known
- **OBSERVED:** EXP-0002 freezes three identical, serialized attempts and asks about reproducibility; it has not executed (`experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot/{README.md:26,scientific-questions.md:3-15}`).
- **OBSERVED:** four historical external attempts found different framework defects but yielded zero complete external golden paths (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:18-38`). These were sequential framework revisions, not independent same-condition samples.
- **DERIVED:** those four attempts demonstrate learning from repetition, but cannot estimate ensemble value because the system changed between attempts.

## 3–4. Uncertainty and type
Dominant: **solution validation**. Unknowns are disagreement frequency, whether disagreement exposes substantive risk, marginal time/cost, and whether synthesis is better than merely choosing a favored output. Reliability is secondary. Absence of a completed three-run campaign is not evidence that one run suffices.

## 5. Genuine alternatives
1. Single attempt by default; state uncertainty and let review catch errors.
2. Always run a fixed number of independent attempts and synthesize all results.
3. Run once, then trigger an independent attempt only for high-impact, weakly evidenced, contradictory, or low-confidence claims.
4. Do nothing beyond existing user-requested reruns.

## 6. Highest-value uncertainty
Does a second blind attempt reveal a **decision-changing** contradiction or unsupported claim often enough to justify its marginal cost? Output diversity alone would not justify multiplication.

## 7–9. Cheapest credible probe and evidence defined before running
**Hypothesis:** conditional second attempts improve consequential briefs more efficiently than either one or fixed-three defaults.

**Probe:** use 5–10 real future coding-agent sessions. Freeze the same repo, intent, prompt, and executor. Produce attempt A; before revealing it, produce B. Have a reviewer record claim-level agreement, contradictions, unsupported claims, recommended action, and whether seeing B changed the action. Retrospective comparison of current artifacts is invalid because prompts/framework revisions differ.

- **Observations required:** blind A/B outputs, elapsed effort, validation result, substantive-review findings, action before/after B.
- **Success evidence:** B repeatedly catches a consequential issue or changes the chosen next action, especially in predeclared trigger cases.
- **Failure evidence:** B mostly paraphrases A or adds noise without changing decisions.
- **Kill criterion:** stop fixed-multiple default if additional attempts add cost without decision-changing evidence across the bounded sample.
- **Ambiguous:** disagreement exists but reviewers cannot determine which claim is better.

**Available probe result:** artifact inspection found no matched independent outputs. **REQUIRES_REAL_WORLD_EVIDENCE.**

## 10. Evidence synthesis
- **Original hypothesis:** multiple independent attempts are normally better.
- **Evidence inspected:** EXP-0002 package/questions; four-attempt product review.
- **Observations:** repetition found defects; independence benefit is unmeasured.
- **Surprise:** most observed failures were contracts/prompts, not clearly model variance.
- **Contradiction:** a three-attempt plan exists, but no result supports adopting it as a default.
- **Changed understanding:** the choice is not “one vs many”; it is when marginal disagreement information is worth buying.
- **Current preferred alternative:** risk-triggered additional attempt, provisionally—not a fixed product policy.
- **Confidence:** low.
- **Unresolved:** trigger precision and incremental user value.
- **Next cheapest experiment:** matched blind two-attempt concierge study.
- **Disposition:** **REVISE** the original multiple-by-default hypothesis.
