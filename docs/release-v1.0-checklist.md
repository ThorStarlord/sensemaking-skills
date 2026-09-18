# Version 1.0 Release Checklist

Use this checklist with [`release-v1.0-contract.md`](release-v1.0-contract.md).
It is a gate record, not evidence that the gates have already passed.

The current contract is a reduced-scope Version 1.0 target. Repository source
is `1.0.0rc2.dev0` in `development` toward `1.0.0rc2`; RC2 is not yet a
frozen candidate. External harness, portability, and semantic-usefulness
evidence is intentionally excluded from the support promise and remains
deferred research evidence.

## Architecture and contracts

- [x] Stable public CLI and Python modules are documented.
- [x] Legacy runner behavior is explicitly compatibility-only, supported, or removed.
- [x] Every canonical Skill is classified exactly once.
- [x] Every supported Skill has a manifest and artifact contract.
- [x] Skill inventory is frozen in the release contract.
- [x] Product/lab boundary validation passes.
- [x] Contract authority graph is resolved.
- [x] `validate-contract-authority.py` passes.
- [x] Source-only lab modules are absent from the wheel.
- [x] Stable Python exports are explicit and hash-pinned in `docs/public-api-v1.0.yaml`.

## Tests and packaging

- [x] Test collection is isolated from nested repositories and generated trees.
- [x] Isolated collection is reproducible from a clean checkout.
- [ ] Product suite passes on Python 3.11 and 3.12 on the exact release head.
- [x] Lab suite passes in its independent lane.
- [x] Filesystem and Gate A security suites pass on supported systems.
- [x] Campaign golden path passes from a clean wheel install.
- [x] Campaign golden path passes from a clean sdist install.
- [x] Campaign schema v1 migration to v2 is verified without semantic reinterpretation.
- [x] Schema migration evidence is recorded.
- [x] Wheel and sdist metadata pass `twine check`.
- [ ] Wheel and sdist build completes from the exact release head.

## Evidence and claims

- [x] Engineering native-harness evidence is frozen, or engineering native support is excluded from 1.0. Current reduced-scope contract excludes it.
- [x] Product Management native-harness evidence is frozen, or PM native support is excluded from 1.0.
- [x] Second-harness portability evidence is frozen, or portability is excluded from 1.0.
- [x] Semantic usefulness evaluation protocol is frozen; usefulness remains deferred unless its study passes.
- [x] Semantic Architecture usefulness claims remain deferred unless behavioral evidence exists.
- [x] `release-v1.0.yaml` contains no unsupported positive claim.
- [x] Qualification claims are either independently evidenced or excluded from 1.0.

## Publication

- [x] Current documentation and ADR statuses are reconciled.
- [x] Documentation currentness validation passes.
- [x] Changelog, migration notes, support matrix, and rollback instructions are complete.
- [ ] Exact release head is checked out and CI passes.
- [ ] Artifact SHA-256 digests are recorded.
- [ ] The release owner explicitly authorizes publication.

The final publication gate is executable with
`python scripts/validate-release-readiness.py --repo-root .`. It must return
`READY` from a clean exact release head; a `BLOCKED` result is authoritative
and must not be bypassed by changing documentation alone.

Until every required item is checked, the repository remains development/candidate Beta rather than final Version 1.0. Passing mechanical checks does not establish semantic
truth or user usefulness; semantic truth is never inferred from a validator.
