# Publishing Sensemaking Skills v0.3.0

This document describes the release process for the first Campaign-based Sensemaking Skills release.

## Current status

- Candidate version: **0.3.0**
- Release branch: `productization/v0.3-p11-release-qualification`
- Integrated baseline: P10 at `main@d833095ab9b37bd9a93d39d286b358061eb913e5`
- P11 release portability: mechanically qualified before final metadata freeze
- Final `0.3.0` source candidate: requires exact-head release qualification before merge
- Real external-harness dogfood: useful after release, **not a publication gate**

## Release claim

v0.3.0 may claim the mechanically qualified installed Campaign control layer:

- durable Campaign workspace/lifecycle;
- canonical artifact admission and validator provenance;
- explicit agent-authored decisions;
- deterministic capability inspection;
- reconciliation reconstruction;
- exact evidence lineage;
- integrity-bound handoff/resume;
- deterministic Skill installation adapters for declared coding-agent discovery roots.

v0.3.0 does **not** claim universal runtime Skill discovery, universal external-repository golden-path success, automatic semantic routing, or guaranteed fresh-agent reasoning quality.

## Release gates before merge

The P11 PR may become ready only when the same exact head satisfies both blocking CI families:

1. **Validator Ecosystem** — repository, Campaign, path-containment, installed-wheel, execution-boundary, and exact-head contracts.
2. **Release Candidate Distribution** — wheel+sdist build, `twine check`, SHA-256 reporting, fresh wheel install, fresh sdist install, `0.3.0` CLI identity, Campaign CLI presence, packaged Skill tree, and packaged validator runtime.

Record the exact candidate SHA and tree. CI success does not itself authorize merge or publication.

## Merge gate

Before integrating the qualified P11 PR:

```text
re-fetch PR
→ head unchanged
→ required CI still SUCCESS on exact head
→ late review threads/reviews/comments checked
→ main/base unchanged or reconciled
→ merge with expected-head protection
```

After merge, verify mechanically:

```text
merge parent 1 = previous main
merge parent 2 = exact qualified P11 head
merge tree = exact qualified P11 tree
main = merge commit
```

Do not squash/rebase the exact-qualified candidate when the release record depends on preserving its tree identity.

## Build and metadata checks

The release-candidate workflow already performs these checks on the PR head:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
sha256sum dist/*
```

Expected distribution identities for v0.3.0:

```text
sensemaking_skills-0.3.0-py3-none-any.whl
sensemaking_skills-0.3.0.tar.gz
```

The workflow also clean-installs both artifacts outside the source checkout.

## Tag and publish

Only after the exact qualified candidate is merged and the merge tree is verified:

```bash
git tag v0.3.0 <verified-main-merge-sha>
git push origin v0.3.0
```

The tag triggers `.github/workflows/publish.yml`:

```text
checkout tagged source
→ install build + twine
→ python -m build
→ python -m twine check dist/*
→ upload dist/* to PyPI
```

The workflow requires the `PYPI_API_TOKEN` repository secret.

## Optional TestPyPI safety check

If desired before production publication, build the exact integrated tree locally or in a controlled release job and upload to TestPyPI:

```bash
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
```

Then install the candidate in a fresh environment. This is a deployment-safety check, not a substitute for exact-head source qualification.

## Production verification

After PyPI publication, create a clean environment and install **from PyPI**, not from the repository or a local wheel:

```bash
python -m venv .verify-v0.3.0
# activate the environment
python -m pip install --upgrade pip
python -m pip install sensemaking-skills==0.3.0
sensemaking-skills --version
sensemaking-skills campaign --help
```

Expected:

```text
0.3.0
```

Also verify that ordinary installed artifact admission does not require a Sensemaking source checkout:

```text
fresh PyPI install
→ campaign init
→ campaign ingest without --framework-root
```

A small valid fixture may be used for this production-distribution smoke test; do not claim it is external semantic dogfood.

## Post-release dogfood

Real coding-agent harness + external repository execution remains valuable. Use [`v0.3-external-qualification-protocol.md`](v0.3-external-qualification-protocol.md) for disciplined post-release dogfood.

That protocol is explicitly **non-blocking** for v0.3.0 and may inform v0.3.1 or v0.4.

## Release checklist

Before tagging:

- [ ] package version is `0.3.0` in `pyproject.toml`, `setup.py`, and `src/sensemaking_skills/__init__.py`;
- [ ] CLI reports `0.3.0`;
- [ ] README, STATUS, CHANGELOG, productization plan, and publishing docs are reconciled;
- [ ] P11 PR exact head is frozen;
- [ ] Validator Ecosystem succeeds on that exact head;
- [ ] Release Candidate Distribution workflow succeeds on that exact head;
- [ ] wheel and sdist pass `twine check`;
- [ ] fresh wheel and sdist install proofs succeed;
- [ ] no unresolved late review findings remain;
- [ ] qualified head/tree are recorded;
- [ ] owner explicitly authorizes integration/release;
- [ ] merge tree is verified equal to the qualified candidate tree;
- [ ] `v0.3.0` tag points at the verified integrated commit.

After publication:

- [ ] `pip install sensemaking-skills==0.3.0` succeeds in a fresh environment;
- [ ] CLI reports `0.3.0`;
- [ ] Campaign CLI is available;
- [ ] installed `campaign ingest` works without `--framework-root` on a valid fixture;
- [ ] release notes preserve the v0.3.0 claim ceiling.

## Credentials and security

Never commit PyPI credentials.

For manual Twine use, prefer environment variables or a protected local configuration:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi_YOUR_API_TOKEN_HERE
python -m twine upload dist/*
```

The GitHub tag workflow uses the repository secret `PYPI_API_TOKEN`.

## Roll-forward policy

Published versions are immutable release identities.

If a genuine defect is discovered after publication:

```text
do not rewrite 0.3.0
→ fix the defect
→ add regression evidence
→ exact-head qualify
→ publish 0.3.1
```

Preserve the actual claim ceiling and failure history rather than retroactively rewriting release evidence.
