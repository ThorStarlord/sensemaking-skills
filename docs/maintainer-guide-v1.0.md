# Maintainer Guide for Version 1.0

This guide is the short operational entry point for maintainers. The exact
support and claim ceiling is defined in [`release-v1.0-contract.md`](release-v1.0-contract.md)
and validated by `scripts/validate-release-contract.py`.

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
- Treat `validator passed != semantic truth` as a release invariant.

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

## Release changes

The repository currently carries frozen candidate source version `1.0.0rc2`
with release target `1.0.0rc2` and status `candidate`. Qualify one exact
source tree, record the integrated commit/tree plus distribution digests in
durable GitHub evidence, and preserve that candidate identity immutably.
Publication, tagging, and final `1.0.0` remain explicit release-owner transitions.
