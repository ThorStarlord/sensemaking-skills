# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-09-09

### Added
- **Sensemaking Campaign product model** — a durable engineering decision process that carries mission, uncertainty, responsibility, authority, evidence, transitions, deferred work, and terminal/continuation state across agent sessions.
- **Durable Campaign workspace and lifecycle service** — typed file-backed state, append-only transitions/trace, atomic/recoverable lifecycle commits, strict reconstruction, handoff invalidation, and fail-closed path containment.
- **Campaign CLI foundation** — `campaign init`, `status`, `validate`, and `history`.
- **Validated artifact admission** — `campaign ingest` validates exact artifact bytes through the canonical validator router, stores content-addressed artifacts, and appends admission receipts before treating artifacts as Campaign evidence.
- **Agent-authored Campaign decisions** — `campaign advance`, `defer`, and `close` persist explicit semantic decisions without introducing automatic routing.
- **Capability registry inspection** — `campaign capabilities` exposes deterministic, unranked capability metadata while keeping responsibility, availability, selection, and execution authority separate.
- **Durable handoff/resume** — `campaign handoff` and `campaign resume` provide integrity-bound reconstruction for fresh processes/agents without making the handoff a semantic recommendation.
- **Artifact/evidence lineage** — `campaign lineage` reconstructs exact consumed bytes, admission provenance, and explicit transition-consumption links while preserving historical claim ceilings.
- **Reconciliation lifecycle inspection** — `campaign reconciliation` distinguishes mechanically required/recorded/legacy-unbound disposition without interpreting report verdicts into automatic Campaign transitions.
- **Coding-agent harness adapters** — deterministic Skill installation targets for generic Agent Skills, Claude Code, Codex, and OpenCode user/project discovery roots, with drift detection and explicit replacement.
- **Self-contained installed artifact validation** — the built distribution now derives the canonical validator runtime from repository `scripts/`, `skills/`, and canonical vocabulary sources so normal `campaign ingest` no longer requires a separate Sensemaking source checkout.
- **Release-candidate distribution qualification** — PR CI builds both wheel and sdist, runs `twine check`, records artifact SHA-256 hashes, clean-installs both distributions, verifies CLI version/Campaign surface, and checks packaged Skill/validator resources.

### Changed
- **Product direction** — development moved from experiment-first work to implementation/productization-first Campaign delivery.
- **Version** — package authorities, CLI, and live release documentation advance from `0.2.2` to `0.3.0`.
- **Release claim** — v0.3.0 deliberately claims the mechanically qualified installed Campaign control layer and deterministic harness installation adapters. Real-harness Skill discovery, complete external-repository golden paths, and fresh-agent semantic quality remain useful post-release dogfood rather than blocking release claims.
- **Publishing workflow** — tagged builds now run `twine check` before PyPI upload.

### Claim ceiling
- `validator passed != semantic truth`
- `admitted evidence != warranted responsibility`
- `available capability != selected or authorized capability`
- `reconciliation evidence != semantic disposition`
- `lineage != semantic warrant`
- `handoff != semantic recommendation`
- `Skill copied to discovery root != harness observed/invoked Skill`

A real external-repository run through a real coding-agent harness is preserved as a disciplined **non-blocking post-release dogfood protocol**; it is not represented as evidence already possessed by v0.3.0.

## [0.2.2] - 2026-08-07

### Added
- **Skill trees shipped in the wheel** — the built wheel now contains the
  canonical SKILL.md trees under `sensemaking_skills/skill_trees/`, derived at
  build time from the single authoritative repository-root `skills/` directory
  (Task P1-F). The shipped 0.2.1 artifact contained no SKILL.md files, so the
  documented `setup-skills` flow could not deliver the canonical
  `repo-sensemaker` (Task P1-R: CONFIRMED).
- **Drift detection in `setup-skills`** — an existing installed skill is
  classified as `current` (matches packaged version, no action), `missing`
  (installed), or `different` (reported as drift, NOT overwritten). Explicit
  `--force` remains the deliberate-replacement mechanism.
- **Packaged-resource resolution** — `setup-skills` now resolves its source
  from installed package resources (`sensemaking_skills/skill_trees` via
  `importlib.resources`) with a repository-root `skills/` fallback for
  editable/source installs; no wheel-installed user needs a source-checkout
  layout assumption.
- **Installed-wheel distribution regression test** —
  `tests/campaign_validation/test_installed_wheel_setup_skills.py` builds the
  wheel, installs it into a fresh venv, runs the documented setup path into a
  temporary destination, and verifies the installed `repo-sensemaker/SKILL.md`
  and references match the release source byte-for-byte, that the CLI exposes
  `setup-skills`, and that divergent copies are reported (not silently
  overwritten) without `--force`.

### Changed
- **Version bumped** from 0.2.1 to 0.2.2 (0.2.1 remains the published broken
  artifact; a new version is required for the repair, per Task P1-F).

## [0.2.1] - 2026-05-25

### Added
- **CLI interface** with Click
  - `sensemaking-skills analyze` — Prepare repository for diagnosis
  - `sensemaking-skills validate` — Validate brief and plan artifacts
  - `sensemaking-skills test` — Run test automation
- **Source layout** — Package moved to `src/sensemaking_skills/` following Python best practices
- **CLI tests** — Integration tests for all CLI commands (8 tests, all passing)
- **CLI documentation** — Usage examples in README and GETTING_STARTED

### Changed
- **Documentation** — Corrected to emphasize agent-native architecture
  - Removed overpromising CLI syntax examples
  - Added explicit fallbacks for skill installation
  - Clarified Python scripts validate, don't diagnose
- **Package structure** — Reorganized for PyPI publication readiness
- **Version bumped** from 0.2.0 to 0.2.1

### Technical
- Added Click dependency (>=8.1.0)
- Updated setup.py with console_scripts entry point
- Added [project.scripts] to pyproject.toml
- Fixed package configuration in pyproject.toml for src layout
- Corrected setuptools config to avoid package discovery issues

## [0.2.0] - 2026-05-25

### Added
- Honest documentation and packaging files
- setup.py for development installation
- pyproject.toml for PEP 518 compliance
- INSTALLATION.md with real setup procedures
- GETTING_STARTED.md with working examples

### Changed
- README.md — Replaced aspirational content with honest state
- Removed promises about non-existent features
- Corrected documentation to match agent-native reality

## [0.1.0] - 2026-05-20

### Initial Release
- Agent-native diagnostic framework
- Scenario 5 budget exhaustion testing (proven)
- Week 1 shadow mode deployment (real execution with 10 actual repositories)
- Repository sensemaking brief artifact (14 sections)
- Workflow orchestration plan artifact (10 sections)
- Artifact validation with error recovery
- Bounded retry logic (3 attempts max)
- Graceful escalation on error budget exhaustion

---

## Notes on Versioning

- **0.3.0** — First Campaign-based release; mechanically qualified installed control layer with deterministic harness installation adapters.
- **0.2.2** — Wheel Skill-tree distribution repair.
- **0.2.1** — CLI interface and src-layout packaging.
- **0.2.0** — Documentation and packaging foundation.
- **0.1.0** — Initial agent-native framework.
- **Future 1.0.0** — Stable release after broader runtime dogfood and compatibility feedback warrant stronger stability claims.

## Current release posture

v0.3.0 is qualified by deterministic/exact-head repository and installed-distribution evidence. Real-harness external-repository dogfood remains valuable but is not a blocking release gate.
