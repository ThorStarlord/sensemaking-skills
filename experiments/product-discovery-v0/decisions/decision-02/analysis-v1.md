# Decision 02 — active agent or delegated model

## 1. Decision
Should the coding agent that holds task context perform repository sensemaking directly, should a runtime delegate reasoning to a separate model, or should the execution surface remain selectable?

## 2. Known
- **OBSERVED:** ADR 0013 proposes skill-led orchestration and says agents read artifacts and validation results to decide next steps (`docs/adr/0013-agent-native-orchestration-primary.md:6-48`). Its status is Proposed, so it is direction evidence, not conclusive validation.
- **OBSERVED:** all reviewed external runs used the same executor/model configuration; provider/platform coverage was not evaluated (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:303`).
- **OBSERVED:** EXP-0002 is designed for the current coding agent, explicitly without an external provider; it is not executed.
- **DERIVED:** repository evidence establishes two implementable surfaces but no controlled comparative outcome.

## 3–4. Uncertainty and type
Dominant: **solution validation**. Unknowns: diagnosis quality, context loss, latency/cost, independence benefits, tool access, privacy, and whether a delegated model catches active-agent blind spots. Construction feasibility is already evidenced enough not to dominate.

## 5. Alternatives
1. Active coding agent executes the skill directly.
2. Runtime delegates every diagnosis to a pinned external model.
3. Selectable surface: direct by default, delegation only for independence or missing capability.
4. Use ordinary repository inspection without invoking a named skill.

## 6. Highest-value uncertainty
Does delegation create better **actionable and substantively supported** diagnoses after accounting for context-transfer errors and cost—not merely different prose?

## 7–9. Cheapest credible experiment
**Hypothesis:** direct execution is sufficient for normal use; blind delegation adds value only as an independent check on consequential ambiguity.

Run 6 matched cases across at least two repository shapes. Freeze repo/intent/evidence access. Have direct and delegated executors produce briefs blind. Human maintainers rate factual support and actionability without knowing executor; record cost, latency, context omissions, and preferred action.

- **Observations:** matched artifacts, validator outcomes, human review, cost/latency, omitted context.
- **Success:** one surface reliably produces more supported/actionable decisions or the combination exposes consequential errors.
- **Failure:** no meaningful difference after cost/context transfer.
- **Kill:** do not build mandatory delegation if it lacks repeated decision value or creates material context/privacy burden.
- **Ambiguous:** preferences differ but action and correctness do not.

Repository-only simulation can compare architecture claims, not executor outcomes. **REQUIRES_REAL_WORLD_EVIDENCE.**

## 10. Synthesis
- **Original hypothesis:** active-agent execution avoids unnecessary delegation.
- **Evidence:** ADR 0013, product review, EXP-0002 preparation.
- **Observations:** direction favors active agents; comparative coverage is absent.
- **Surprise:** provider choice is mostly a test gap, not an evidenced product deficiency.
- **Contradiction:** architectural confidence exceeds outcome evidence.
- **Changed understanding:** provider abstraction should not precede evidence that provider choice changes decisions.
- **Current preferred:** direct execution as the cheapest experiment/default, preserving manual delegated comparison—not building a general selector.
- **Confidence:** low-medium on experiment choice, low on final product choice.
- **Unresolved:** matched human-rated performance.
- **Next experiment:** concierge blind paired comparison.
- **Disposition:** **CONTINUE** direct-agent testing; **DISCARD** premature delegation infrastructure.
