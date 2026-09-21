# Strategic Hypothesis Admission v1 — Handoff

**Issue:** #446  
**Feature PR:** #447  
**Feature disposition:** COMPLETE / INTEGRATED  
**Normal-use disposition:** NORMAL_USE_HANDOFF  
**Feature head:** `1c4bb394b685f0ca4fc7fbe58edceb22e61ef9d7`  
**Feature merge:** `b9ae094f7946ab72653f02392c10e0f977fb3d47`

## Objective

Correct the remaining epistemic-conservatism failure mode in
`strategic-repository-analysis` without weakening evidence, authority, or
validation boundaries.

The change distinguishes three epistemic jobs:

```text
present-state claim
-> evidence or explicit owner-intent source

future-state possibility
-> strategic grounding + explicit assumptions

future success claim
-> returned evidence after construction/use
```

## Integrated changes

### Strategic Hypothesis Admission

Before converging on evidence sufficiency, the Skill now performs a generative
pass. A real strategic path may represent an unbuilt future when it is coherent
with governing intent, compatible with repository reality, materially distinct,
mechanistically plausible, explicit about material assumptions, and free of
known contradiction.

```text
real strategic path
!= empirically validated future

speculative path
!= manufactured path

strategic grounding
!= prior validation
```

### Opportunity-driven Strategic Frontier

The Strategic Frontier may now admit materially grounded opportunities and
unexploited leverage, not only deficiencies/tensions. Evidence grounds the
present basis of the opportunity; it does not need to prove the future outcome.

### Manufactured-alternative boundary

A path is manufactured when it exists to fill path-count symmetry, is not
materially distinct, contradicts governing intent/current reality, solves no
represented problem/opportunity, or depends on hidden/invented premises.

Unvalidated or ambitious no longer means manufactured by itself.

### Commission / omission symmetry

Path comparison now explicitly considers both:

- commission risk — downside of building toward a wrong future;
- omission risk — lost mission progress, leverage, learning rate, optionality,
  or adjacent opportunity from not acting.

The existing v2 qualitative lenses remain authoritative; no numeric
expected-value score or new schema field was added.

### Reversible build-as-learning at Level 3

Residual success uncertainty no longer automatically pushes the disposition to
`INVESTIGATE` or `DEFER`. A bounded, reversible, authorized, sufficiently
safe, information-producing build may be the cheapest sufficient way to learn.

```text
residual uncertainty
!= BUILD prohibited
```

## Files changed

- `skills/strategic-repository-analysis/SKILL.md`
- `skills/strategic-repository-analysis/references/construction-path-synthesis-v1.md`
- `docs/strategic-repository-sensemaking-v1.md`
- `tests/test_strategic_repository_analysis_integration.py`

Closeout reconciliation additionally updates `STATUS.md`, `CHANGELOG.md`,
and this handoff.

## Qualification

Exact feature head:

`1c4bb394b685f0ca4fc7fbe58edceb22e61ef9d7`

- Product Validation run `35642494009` / #1142: PASS
- Release Candidate Distribution run `35642494021` / #274: PASS

The feature was merged as:

`b9ae094f7946ab72653f02392c10e0f977fb3d47`

GitHub compare from the qualified feature head to the merge commit reports one
merge commit and **zero file differences**. The integrated feature bytes are
therefore content-identical to the qualified PR head.

No separate post-merge push-run identifier is asserted here because the
available connector exposes pull-request-triggered workflow runs, not a complete
push-run enumeration surface.

## Compatibility

No package introduces:

- schema v3;
- a new strategic disposition;
- a StrategicPlanner / OuterLoopEngine runtime;
- numeric strategy/path ranking;
- automatic path selection;
- automatic Campaign creation;
- automatic Level-4 revision;
- merge/release/deploy/publication authority;
- weaker evidence requirements for present-state claims.

Existing strategic artifact v2 remains canonical, and historical legacy v1
artifacts remain valid.

## Claim ceiling

Repository qualification establishes contract/integration coherence and the
presence of the new semantic guidance. It does not establish that every future
agent will surface every useful opportunity, that any admitted strategic
hypothesis will succeed, or that the selected path is objectively optimal.

```text
hypothesis admitted
!= future success established

path selected
!= implementation authorized

mechanically qualified
!= semantically optimal
```

## Terminal operating state

```text
ISSUE_446_STRATEGIC_HYPOTHESIS_ADMISSION_V1
= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF

CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
OPERATING MODE = NORMAL_USE_VALIDATION
```

Future refinement should reopen only from concrete normal-use evidence that the
Skill still collapses grounded opportunities into conservative no-path outcomes,
or that it has overcorrected into ungrounded speculation, or from explicit owner
direction.
