# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- **0.2.1** — CLI interface added, local testing complete, PyPI-ready (not yet published)
- **0.2.0** — Documentation and packaging foundation
- **0.1.0** — Initial agent-native framework (proven with Scenario 5)
- **Future 0.3.0** — Full CLI with agent integration (after real-world CLI usage testing)
- **Future 1.0.0** — Stable release with proven CLI and PyPI availability

## Deployment Timeline

**Phase 2.2** (Current): CLI development and local testing ✅
**Phase 2.3**: PyPI publication readiness (distribution built, awaiting real-world CLI usage)
**Phase 3**: Real-world CLI testing with users
**Phase 4**: Production PyPI publication and full GA
