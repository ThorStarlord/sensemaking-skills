# Project learning map v1

## Scope and evidence discipline

This map reads repository artifacts as historical claims, not as ground truth about user value. Labels mean: **OBSERVED** = directly present in an artifact; **DERIVED** = follows from multiple observations; **INFERRED** = plausible interpretation; **UNKNOWN** = repository evidence cannot answer it.

## Trajectory

1. **OBSERVED — broad stated product.** The README calls the project an agent-native framework for repository diagnosis and workflow orchestration (`README.md:6`).
2. **OBSERVED — architecture moved toward agent-owned control.** ADR 0013 records a proposed shift from runner-led control to skill-led orchestration (`docs/adr/0013-agent-native-orchestration-primary.md:6-29`) and says the agent reads artifacts and validation results to choose a next step (`:48`).
3. **OBSERVED — repo-sensemaker has a deliberately diagnostic boundary.** Its canonical instructions forbid implementation and require a brief (`skills/repo-sensemaker/SKILL.md:98`).
4. **OBSERVED — evidence narrowed the credible boundary.** The July product-contract review reports four external Auteur attempts, three framework bugs, and no successful external end-to-end golden path (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:18-19`). It says the brief is the only stage ever to pass live externally (`:43-44`), routing accuracy lacks external evidence (`:70-71`), and the highest justified readiness is “Externally exercised” (`:311`).
5. **OBSERVED — repetition is now an explicit experimental variable.** EXP-0002 freezes three serialized attempts (`experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot/README.md:26`) specifically to study reproducibility across identical attempts (`scientific-questions.md:3-15`). The package is preparation-only, so it is a planned test rather than result evidence.
6. **OBSERVED — provider/executor coverage remains absent.** The product review says all live runs used one executor/model configuration (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:303`). EXP-0002 deliberately tests the current coding agent with no external provider.
7. **OBSERVED — governance became explicit and bounded.** ADR 0023 proposes two authorization lanes; EXP-0002 uses a frozen envelope plus a standalone conversational `approve`, while treating the file as an audit receipt rather than independent identity proof (`README.md:50-67`).
8. **OBSERVED — transition semantics have conflicting historical signals.** ADR 0013 favors agent judgment, while Stage 2 preserves Diagnosis → Recommendation → Selection and defaults escalation to recommendation rather than action (`docs/STAGE-2-COMPLETE.md:92,259`).
9. **UNKNOWN — current hardening result.** No `experiments/repository-sensemaking-skill-hardening-v1/**` artifacts exist in this checkout. This workstream therefore does not claim or reconstruct its candidate, scorer, corpus, baseline, ground truth, or results.

## Positive knowledge

- A brief can be structurally checked, and external attempts found real prompt/validator defects.
- Target immutability held across the four external attempts according to the product review.
- A direct agent-native attempt is concrete enough to freeze and govern without an external provider.
- Separating diagnosis, recommendation, and selection is already represented in project artifacts.

## Negative knowledge (what has been falsified or remains unsupported)

- Structural validity is not substantive correctness: the review records a structurally passing brief with an unsupported absence claim.
- A successful internal path does not prove external routing or end-to-end usefulness.
- Multiple attempts are not yet proven better; EXP-0002 asks the question but contains no outcome.
- No repository evidence compares active-agent reasoning with delegated-model reasoning on matched tasks.
- No evidence shows an external maintainer acted on a brief, so usefulness and willingness-to-adopt remain unknown.
- Existing campaign machinery proves controls can be expressed; it does not prove that all of that ceremony is proportionate for every exploratory session.

## Derived tension map

| Tension | What is supported | What remains unknown |
|---|---|---|
| one vs many | variability is plausible and a three-run test is frozen | incremental decision value per extra attempt |
| agent vs delegation | agent-owned control is a documented architectural direction | matched quality/cost comparison |
| governance | bounded approvals and durable accounting exist | minimum safe controls by consequence |
| routing | recommendation/selection separation exists | whether auto-transition improves user outcomes |
| product layer | product fog exists in vocabulary | whether a dedicated layer creates more value than a careful prompt |

## Recon conclusion

**DERIVED:** the repository has repeatedly invested in mechanics before external usefulness was established. That makes the proposed discovery discipline relevant as a guard against another infrastructure-first cycle. **INFERRED:** a useful method would focus on decision-changing uncertainty and evidence boundaries, not add another lifecycle. **UNKNOWN:** whether users experience these decisions as problems at all.
