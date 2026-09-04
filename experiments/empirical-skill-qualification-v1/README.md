# Empirical Skill Qualification v1

**Status:** `PREPARED_NOT_RUN`  
**Classification:** `EXPLORATORY_NOT_CANONICAL_EVIDENCE`  
**Baseline framework:** `969e8eb47144ffdeb27a8d9df02b6a292586e842`  
**Target Skill:** `skills/repo-sensemaker/SKILL.md`

## Purpose

Test whether held-out baseline-vs-candidate qualification adds consequential
information beyond the current Skill maintenance process (trigger rerun + neighboring
regression check) without changing Sensemaking's product-level control or authority
model.

This package is a research protocol and deterministic support surface. It is **not**
a Skill optimizer, a promotion mechanism, a new product artifact contract, or an
authorization to invoke a provider/model.

## Central research question

> Does held-out baseline-vs-candidate qualification detect useful improvements or
> regressions that the existing Skill-maintenance verification process would not?

## Pre-registered hypotheses

1. **Qualification value:** held-out comparison will reveal at least one materially
   relevant fact not established by trigger-rerun plus one neighboring regression
   case alone.
2. **Existing artifact sufficiency:** `usage_research_report` and
   `skill_improvement_plan` can drive candidate generation without a new product
   artifact contract.
3. **Bounded edits:** a small Skill candidate is easier to attribute and falsify than
   an unrestricted rewrite.
4. **Independent evaluation:** a blinded qualifier may disagree with the candidate
   author's predicted improvement.

A negative result is valid. `NO_SKILL_CHANGE`, candidate rejection, or a finding that
held-out qualification adds no material value all count as informative outcomes.

## Scope

V1 targets exactly one Skill: `repo-sensemaker`.

Candidate budget:

- max target Skills: 1
- max modified files in the candidate: 1 (`skills/repo-sensemaker/SKILL.md`)
- max instruction regions: 2
- full Skill rewrite: prohibited
- registry change: prohibited
- artifact-contract change: prohibited
- validator change: prohibited
- workflow change: prohibited
- automatic adoption/merge: prohibited

If diagnosis attributes the pressure to a fixture, validator, registry, executor lapse,
harness/tool failure, environment failure, or remains inconclusive, the correct Skill
candidate is `NO_SKILL_CHANGE`.

## Experimental split

The case corpus is frozen before candidate generation into three disjoint sets:

- **D — Diagnostic:** visible to `usage-researcher`, `skill-maintainer`, and candidate
  author. Used to expose pressure and motivate a bounded candidate.
- **Q — Qualification:** hidden from candidate generation. Used for blind
  baseline-vs-candidate selection.
- **T — Test:** untouched until after a candidate survives Q. Used to test
  generalization.

The deterministic helper `sensemaking_skills.skill_qualification` validates split
integrity and creates reproducible per-case blind assignments. It does not execute a
model or make an authorization decision.

## Qualification dimensions

No scalar overall score is used. Evaluators keep these dimensions separate:

- mechanical validity
- evidence grounding
- decision quality
- boundary/authority compliance
- original defect behavior
- correct-negative preservation
- regression materiality

Cost/latency/tool-count telemetry may be recorded, but is non-authoritative unless a
future experiment explicitly pre-registers it as a qualification criterion.

## Candidate survival rule

A candidate cannot survive Q if any of the following is observed:

1. a new mechanical failure;
2. a material regression;
3. a boundary/authority regression;
4. loss of correct-negative behavior;
5. no demonstrated improvement on the original failure pressure when that pressure is
   applicable.

A surviving comparison is classified qualitatively as `IMPROVED`, `EQUIVALENT`,
`MIXED`, `REGRESSED`, or `INCONCLUSIVE`. Only `IMPROVED` is eligible to proceed to T.
Eligibility is not promotion authority.

## Execution order

1. Freeze baseline identity.
2. Freeze D/Q/T case manifest and its digest.
3. Run baseline characterization only under valid existing experiment authorization.
4. Expose D only to `usage-researcher` and `skill-maintainer`.
5. Attribute defect before editing.
6. Freeze one bounded candidate (or `NO_SKILL_CHANGE`).
7. Run baseline and candidate on Q under equivalent execution conditions.
8. Commit blinded judgments before unblinding.
9. If and only if Q disposition is `IMPROVED`, open T and repeat blind comparison.
10. Compare the result against the current promotion-process counterfactual.
11. Produce one final disposition.
12. Do not merge or productize the Skill candidate from this experiment automatically.

## Final research dispositions

Exactly one of:

- `NO_FURTHER_WORK_WARRANTED`
- `REPLICATE`
- `NARROW_MECHANISM_WARRANTED`
- `PRODUCTIZATION_CANDIDATE`

V1 should normally end in one of the first two. A single successful candidate is not
sufficient evidence for generic optimization machinery.

## Authorization boundary

This repository already separates exploratory campaigns from canonical evidence.
Nothing in this package constitutes human campaign approval. No model/provider run,
Skill candidate execution, or external-target experiment is authorized merely because
this package exists or is merged.

If an exploratory provider/model campaign is prepared, it must use the repository's
existing two-lane authorization machinery and an available `EXP-NNNN` namespace. Its
outputs remain `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. Canonical evidence requires a new
canonical run; exploratory results are never relabeled.

## Stop conditions

Stop rather than repair toward a positive result when:

- the observed failure is not a Skill defect;
- the candidate exceeds the edit budget;
- Q leaks before candidate freeze;
- T leaks before Q selection;
- baseline/candidate execution conditions are materially incomparable;
- provenance cannot be pinned;
- evaluator blinding is materially compromised;
- required experiment authorization is absent;
- a material regression appears;
- evidence is already sufficient to answer the research question.

## Claim boundary

A successful v1 can support only a statement about the usefulness of this qualification
method for the tested `repo-sensemaker` candidate under the frozen cases and execution
conditions. It cannot establish automatic Skill optimization, cross-Skill generality,
real-world prevalence of the tested failures, or promotion authority.
