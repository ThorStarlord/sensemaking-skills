# Maintainer Guide for Version 1.0

This guide is the short operational entry point for maintainers. The exact
support and claim ceiling is defined in [`release-v1.0-contract.md`](release-v1.0-contract.md)
and validated by `scripts/validate-release-contract.py`.

The canonical assurance vocabulary is defined in
[`verification-and-qualification-model.md`](verification-and-qualification-model.md).
Use that model to distinguish test class, mechanical validation stage,
Four-Level Control scope, and qualification state.

## Authority order

1. Accepted ADRs and executable contracts define current behavior.
2. `release-v1.0.yaml` defines the 1.0 support and claim surface.
3. `STATUS.md` records current qualification state.
4. Historical reports under `docs/archive/` and `experiments/` preserve evidence
   but do not override current authority.

When prose and executable behavior disagree, preserve the evidence, report the
disagreement, and reconcile the current document. Do not silently expand the
public surface.

## Change discipline

- Choose responsibility before Skill or workflow.
- Keep semantic judgment with the active coding agent.
- Add a failing test before changing production behavior.
- Preserve exact artifact and target-repository provenance.
- Use the product/lab boundary to decide which validation lane owns a test.
- Classify new assurance checks independently by test class, validation stage,
  control level, and qualification effect.
- Reserve `Level 1`-`Level 4` for the current Four-Level Control Model; do not
  introduce new `Level-N validator` terminology.
- Treat `validator passed != semantic truth` as a release invariant.
- Treat `test passed != qualification` as a release invariant.

## Verification lanes

```text
python scripts/validate-release-contract.py --repo-root .
python scripts/validate-contract-authority.py --repo-root .
python scripts/validate-docs-currentness.py --repo-root .
python scripts/validate-product-boundary.py
python scripts/validate-skill-hygiene.py
python -m pytest tests/ -q
python -m twine check dist/*
```

Product tests own shipped behavior. Lab tests own retained research machinery.
External qualification tests own frozen real-harness evidence. No lane may
upgrade a semantic or native-harness claim without its required evidence.

The lane and the test class are different axes. For example, an external
qualification lane may contain a qualification verifier plus preserved external
evidence; an integration test remains an integration test whether it exercises
product or retained lab machinery.

## Claim discipline

Use the smallest claim supported by the evidence:

```text
unit/contract/integration/acceptance result
!= qualification state

mechanical validation V0-V5
!= semantic judgment

repository qualified
!= native-harness qualified
!= portability qualified
!= promoted
```

Historical documents may retain older phrases such as `Level-3 validators` for
provenance. Treat those uses as legacy execution-validation terminology, not as
references to the current Level-3 repository-strategy control scope.

## Release changes

The repository currently carries development source version `1.0.0rc3.dev0`
targeting `1.0.0rc3` with release status `development`. The previously
qualified `1.0.0rc2` candidate remains immutable at integrated commit
`c9b86138d3919c4fce87040f14161364a0c1c3a0`. Future RC3 qualification must
bind a new exact source/tree and artifact evidence. Publication, tagging, and
final `1.0.0` remain explicit release-owner transitions.
