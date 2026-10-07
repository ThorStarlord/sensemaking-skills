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

The current post-RC4 source is `1.0.0rc5.dev0` and the active release
target is `1.0.0rc5` with status `development` on integrated RC4 `main`. Integrated RC4
`d26521005f7ab6696e050844510ff0e3298f002b` remains immutable predecessor
provenance and its qualification does not transfer to these development bytes.
Historical `1.0.0rc1` and qualified `1.0.0rc2` also remain immutable provenance.

`pyproject.toml` `[project].version` is the literal source/build version.
`release-v1.0.yaml` declares the release target and phase.

## Candidate phase

While `release.status: candidate`:

- the source version equals the release target exactly;
- Product Validation, Lab Validation where applicable, and Release Candidate Distribution may qualify the exact branch head;
- passing checks qualifies only that exact source/tree for the claims those checks establish;
- candidate qualification does **not** authorize merge, PyPI publication, tagging, or final `1.0.0`.

## Candidate freeze

RC4 was integrated through PR #520 as `main@9ab42ee1248358bc9bf04d9f68fb49bbf1b2d776` with the exact frozen candidate tree. Current RC5 development is not a freeze proposal; a future RC5 candidate requires a new exact-source freeze and qualification after development converges.

Candidate qualification requires:

1. one exact freeze head qualified by Product Validation and Release Candidate Distribution;
2. integration without changing the candidate Git tree;
3. Product Validation and Release Candidate Distribution on the exact integrated `main` commit;
4. durable recording of the integrated commit, Git tree, workflow runs, and distribution SHA-256 digests.

Candidate qualification is an exact-source warrant. It does not automatically
authorize PyPI publication or final `1.0.0`.

### Hosted-CI availability boundary

Ordinary development does not stop merely because GitHub-hosted qualification is
temporarily unavailable. Continue with applicable local tests, validators, builds,
and repository work, and record the hosted check as pending/unavailable.

However, the current candidate/release contract deliberately requires hosted
exact-source qualification for the stronger candidate, merge, and publication
claims described below. Local reproduction may support development confidence but
does not substitute for that evidence.

```text
hosted Actions unavailable
-> continue ordinary development locally
-> preserve hosted qualification as pending

local PASS
!= exact-head hosted qualification

qualification unavailable
!= qualification failed
!= permission to weaken the gate
```

If the external blocker is quota/billing, do not spend money, change billing, or
bypass repository policy without explicit owner authority. Once hosted
qualification is available and materially needed, run only the required
qualification rather than rerunning it as routine ceremony.

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
identity such as a `.dev0` predecessor of its target.

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
