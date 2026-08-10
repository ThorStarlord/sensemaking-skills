# Archived Phase Reports

Historical phase/completion/deployment status documents, moved here from the
repo root during Work Stream 2 (docs & contract reconciliation, 2026-08-10).
The repo root now keeps a single living status document: `STATUS.md`.

## What was moved

97 files, including:

- `FINAL-*.md`, `PHASE-*.md`, `COMPLETION-*.md`, `PROJECT-STATUS-*.md`,
  `CURRENT-PROJECT-STATUS.md`, `NEXT-AGENT-HANDOFF.md`
- `DEPLOYMENT-*.md`, `PRODUCTION-*.md`, `SESSION-*.md`, `SHADOW-MODE-*.md`,
  `PILOT-ROLLOUT-*.md`, `WEEK1-*.md`, `GENERAL-AVAILABILITY-*.md`
- `SCENARIO-5-*.md`, `IMPLEMENTATION_*.md`, `PROCESS_*.md`,
  `validation_run_log*.md`, and other dated status/report/evidence files

All content is preserved; nothing was deleted. Relative links between files
that moved together remain valid within this directory.

## README updates (same stream)

- Version claim `0.2.1` -> `0.2.2` (matching `pyproject.toml`).
- Disclosed GitHub REST API usage in the `exploratory_execution` subsystem
  (issue/approval tracking, bearer-token auth, fail-closed).
- Repository structure diagram: corrected `docs/CONTEXT.md` -> root
  `CONTEXT.md` and added the `src/sensemaking_skills/` subsystems
  (`campaign_accounting/`, `campaign_validation/`, `exploratory_authorization/`,
  `exploratory_execution/`).
- Updated the two evidence links (Scenario 5, Week 1) to point at this
  archive directory.

## ADR restored

- `docs/adr/0011-canonical-vocabulary-enforcement.md` — the 0011 slot was
  missing (ADR numbering skipped from 0010 to 0012); restored per CONTEXT.md
  item 10 and `docs/HARDENING_STATUS.md`.
