# Publishing Sensemaking Skills Version 1.0

This document defines the publication boundary for the current Version 1.0 line.
The machine-readable support and claim ceiling is [`release-v1.0-contract.md`](release-v1.0-contract.md).

## Release identity

Three identities must not be conflated:

```text
repository development source
!= frozen release candidate
!= publicly published distribution
```

The current repository source and active frozen release target are both
`1.0.0rc2`. Historical `1.0.0rc1` remains qualified provenance for exact
commit `70542d47412d98ee6dfae5de6df29bf271304568`; continued development
superseded it as the identity of `main`.

`pyproject.toml` `[project].version` is the literal source/build version.
`release-v1.0.yaml` declares the release target and phase.

## Development phase

While `release.status: development`:

- the source version is the development predecessor of the target (currently `1.0.0rc2.dev0`);
- Product Validation and distribution validation may run;
- passing those checks does **not** qualify a frozen release candidate;
- current source must not present itself as `1.0.0rc2`.

## Candidate freeze

The current source is frozen as `1.0.0rc2` with release status `candidate`.

Candidate qualification requires:

1. one exact freeze head qualified by Product Validation and Release Candidate Distribution;
2. integration without changing the candidate Git tree;
3. Product Validation and Release Candidate Distribution on the exact integrated `main` commit;
4. durable recording of the integrated commit, Git tree, workflow runs, and distribution SHA-256 digests.

Candidate qualification is an exact-source warrant. It does not automatically
authorize PyPI publication or final `1.0.0`.

## Distribution gate

`.github/workflows/release-candidate.yml` derives distribution identity from
`pyproject.toml` instead of hardcoding a historical candidate version. It:

- checks out the exact PR/workflow head;
- validates the release contract and current documentation;
- validates the product/lab boundary;
- builds wheel and sdist;
- runs `python -m twine check dist/*`;
- verifies artifact names against the current source version;
- records SHA-256 digests;
- clean-installs both distributions;
- verifies CLI version, Campaign surface, schema v2, package boundaries, Skills, and validator runtime;
- uploads the exact validated distributions as workflow artifacts.

During `development`, this is distribution validation rather than candidate qualification. For a frozen `candidate`, the same workflow is candidate qualification and also runs on `main` pushes so the exact integrated source is qualified.

## Merge and integration

Merge only a qualified exact PR head. If the PR head moves, rerun qualification.

A qualified PR head does not prove that the eventual integrated candidate is the
same combined source state if the base advances. Preserve PR head, qualification
base, actual integration base, integrated commit, and post-integration validation
when the closure claim depends on the integrated result.

## Tag and PyPI publication

Tagging and PyPI publication are explicit release-owner actions and remain
separate from candidate qualification. Do not tag or publish an unqualified or stale candidate.

`.github/workflows/publish.yml` triggers on `v*` tags, builds distributions,
runs `twine check`, and uploads only after metadata validation succeeds.

After public publication, verify from a clean environment:

```bash
python -m venv /tmp/sensemaking-release-check
# activate it
python -m pip install --upgrade pip
python -m pip install sensemaking-skills
sensemaking-skills --version
sensemaking-skills campaign --help
```

## Post-candidate development

Once a candidate is frozen, any material continued development must leave that
frozen identity before ordinary development proceeds. For example, after a frozen
`1.0.0rc2`, development toward another candidate should use a new development
identity such as `1.0.0rc3.dev0`.

```text
candidate version
+ exact source
+ qualification
+ artifact hashes
= immutable release-candidate identity
```

## Evidence ceiling

The reduced-scope Version 1.0 contract excludes native-harness compatibility,
cross-harness portability, and semantic usefulness from the required support
promise unless they are separately promoted with the required evidence.

Validator PASS does not establish semantic truth or release-owner authorization.
