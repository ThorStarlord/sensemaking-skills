# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-09-09

### Added
- **Sensemaking Campaign control layer** — durable typed Campaign state, append-only transitions/trace, validated artifact admission, explicit agent-authored decisions, capability inspection, handoff/resume, evidence lineage, reconciliation reconstruction, and harness setup adapters.
- **Self-contained installed validation runtime** — wheel/sdist builds derive the canonical validator runtime from repository `scripts/`, `skills/`, and `docs/canonical-vocabulary.yaml`, so normal `campaign ingest` no longer requires a second Sensemaking source checkout.
- **Campaign schema v2 compatibility** — current artifacts emit schema v2; historical v1 Campaign artifacts can be deterministically migrated in memory and qualified through append-only migration receipts without rewriting historical bytes.
- **Durable target snapshot binding** — target-bound Campaigns persist sanitized repository identity, Git HEAD/tree, deterministic tracked/untracked worktree state, and transition source/destination snapshot digests; status/validation, lineage, and fresh-context handoff/resume fail closed on unrecorded target drift without turning provenance into semantic routing.
- **Real-harness qualification verifier** — `sensemaking_skills.external_qualification` verifies frozen real-harness evidence packages with exact candidate/target/runtime identity, SHA-256 binding, lifecycle checkpoints, fresh-context handoff/resume integrity, and explicit PASS/FAIL/INVALID dispositions.
- **Release-candidate distribution gate** — exact-head CI builds wheel and sdist, runs `twine check`, verifies exact artifact identities, clean-installs both distributions, checks schema-v2/core-lab boundaries, and uploads SHA-256-bound candidate artifacts.

### Changed
- **Product/lab split** — the shipped wheel contains only the Campaign product/runtime surface; retained research/experiment packages and their dependencies remain source-only lab infrastructure.
- **Release-version authority** — `[project].version` in `pyproject.toml` is the single literal release authority; runtime `sensemaking_skills.__version__` derives from installed distribution metadata.
- **CI authority** — Product Validation owns shipped-package, installed-wheel, repository-contract, and filesystem-security claims; Lab Validation owns retained source-only research claims.
- **Publishing workflow** — tagged builds use current GitHub Actions and run `twine check` before PyPI upload.
- **Version** — release authority advances from `0.2.2` to `0.3.0`.

### Claim ceiling
- `validator passed != semantic truth`
- `admitted evidence != warranted responsibility`
- `available capability != selected or authorized capability`
- `reconciliation evidence != semantic disposition`
- `lineage != semantic warrant`
- `handoff != semantic recommendation`
- `target snapshot bound != repository correct`
- `repository changed != repair succeeded`
- `target drift != automatic transition`
- `Skill copied to discovery root != harness observed/invoked Skill`
- `external qualification verifier PASS != semantic truth`

The repository contains the deterministic real-harness evidence verifier and its contract tests. A real-harness PASS result remains empirical evidence from a frozen external attempt; synthetic fixtures prove the verifier contract, not that such an empirical run has occurred.

## [0.2.2] - 2026-08-07

### Added
- **Skill trees shipped in the wheel** — the built wheel contains canonical `SKILL.md` trees under `sensemaking_skills/skill_trees/`, derived at build time from the authoritative repository-root `skills/` directory.
- **Drift detection in `setup-skills`** — installed skills are classified as `current`, `missing`, or `different`; divergent installed bytes are not overwritten without explicit `--force`.
- **Packaged-resource resolution** — `setup-skills` resolves source trees from installed package resources with a repository-root fallback for editable/source installs.
- **Installed-wheel distribution regression test** — fresh-wheel tests verify setup surface, packaged Skill bytes, and fail-closed drift behavior.

### Changed
- **Version bumped** from 0.2.1 to 0.2.2.

## [0.2.1] - 2026-05-25

### Added
- **CLI interface** with Click
  - `sensemaking-skills analyze`
  - `sensemaking-skills validate`
  - `sensemaking-skills test`
- **Source layout** under `src/sensemaking_skills/`.
- **CLI tests and documentation**.

### Changed
- Documentation was corrected to emphasize agent-native architecture and honest CLI boundaries.
- Packaging was reorganized for PyPI publication readiness.
- Version advanced from 0.2.0 to 0.2.1.

## [0.2.0] - 2026-05-25

### Added
- Honest documentation and packaging files.
- `setup.py`, `pyproject.toml`, `INSTALLATION.md`, and `GETTING_STARTED.md`.

### Changed
- Documentation was aligned with the actually implemented agent-native system.

## [0.1.0] - 2026-05-20

### Initial Release
- Agent-native diagnostic framework.
- Scenario 5 budget-exhaustion testing.
- Week 1 shadow-mode execution across 10 repositories.
- Repository sensemaking brief and workflow orchestration artifacts.
- Validation, bounded retry, and escalation behavior.

---

## Release posture

- **0.3.0** — first Campaign-based release baseline: shipped Campaign control layer, schema-v2 compatibility, durable target snapshot provenance, product/lab packaging separation, deterministic harness setup, installed validator runtime, and exact-head release qualification.
- **0.2.2** — wheel Skill-tree distribution repair.
- **0.2.1** — CLI/src-layout packaging.
- **0.2.0** — packaging/documentation foundation.
- **0.1.0** — initial agent-native framework.
- **Future 1.0.0** — stable release after broader runtime dogfood and compatibility evidence warrant stronger stability claims.
