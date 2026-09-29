# scripts/

Operator and CI tooling. The product CLI is `sensemaking-skills`
(see `docs/cli-reference.md`); these scripts are run directly with
`python scripts/<name>`. Console output is ASCII-only.

## Validators (`validate-*.py`)

Deterministic checks; a PASS makes an artifact eligible for semantic use, it
does not prove the conclusion.

| Group | Scripts |
| --- | --- |
| Generic artifact/plan | `validate-artifact.py`, `validate-output.py`, `validate-plan.py`, `validate-and-report.py`, `validate-and-record.py`, `record-validation.py` |
| Repository sensemaking | `validate-brief.py`, `validate-repo.py`, `validate-alignment.py` (problem frame vs brief boundary), `validate-probe-report.py`, `validate-unknowns-map.py`, `validate-prompt-handoff.py`, `validate-run-log.py` |
| Strategic / architectural | `validate-strategic-state.py`, `validate-strategic-companion.py`, `validate-strategic-repository-analysis.py`, `validate-multi-repository-strategic-analysis.py`, `validate-candidate-directions.py`, `validate-architectural-review-recommendation.py`, `validate-change-impact-analysis.py`, `validate-semantic-reasoning-profile.py` |
| Intent / PRD | `validate-user-intent.py`, `validate-user-intent-amendment.py`, `validate-prd.py` |
| Product management | `validate-pm-artifact.py`, `validate-pm-customer-model.py`, `validate-pm-feature-definition.py`, `validate-pm-launch-communication.py`, `validate-pm-measurement.py`, `validate-pm-strategy.py` |
| Skill maintenance | `validate-skill-hygiene.py`, `validate-skill-improvement-plan.py`, `validate-skill-registry-liveness.py`, `validate-usage-research-report.py` |
| Repository/docs governance | `validate-docs-currentness.py`, `validate-product-boundary.py`, `validate-contract-authority.py`, `validate-mode-coverage.py`, `validate-fog-type-normalization.py`, `validate-error-boundaries.py` (rejects silent broad exception handlers in the shipped product surface) |
| Release | `validate-release-contract.py`, `validate-release-readiness.py` (see `docs/release-authority-audit.md`) |

## Workflow and orchestration

- `workflow-planner.py`, `workflow_liveness.py`, `_orchestrator.py` - plan
  construction and registry liveness (ADR 0025-0027).
- `workflow-runtime.py`, `workflow-runner-agent.py` - retained compatibility
  runtime; the coding-agent-mode runner delegates skills to the active agent.
  The programmatic runner was retired (see
  `docs/2026-08-programmatic-runner-retirement-plan.md`); the agent-native path
  is primary (ADR 0013).
- `skill_executor.py`, `portfolio-orchestrator.py` (see
  `docs/PORTFOLIO_OPERATIONS.md`), `shadow-mode-runner.py`,
  `shadow-mode-metrics.py` - compatibility / measurement tooling.

## Probes and evidence tooling

- `probe-repo.py`, `probe_relationships.py`, `repo_probes.py`,
  `probe_skill_distribution.py`, `gate_relationship_findings.py`,
  `brief_skeleton.py`.
- `evidence_quote_extractor.py` - deterministic extraction of verbatim
  `evidence_excerpts[].quote` text so the model is not the copy boundary
  (issue #89).
- `weakness_type_safeguard.py` - section-aware, duplicate-key-safe
  `weakness_type` check (issue #90).

## Ledgers, logs, and contracts

`run-ledger.py` (`docs/run-ledger-guide.md`), `analyze-run-failures.py`,
`create-artifact.py`, `campaign-contract-roundtrip.py` (loads historical
campaign fixtures and every shipped template and checks round-trip equality),
`gate_a_authorization.py`.

## Execution infrastructure

`execution_infra/` - governed campaign execution and the agent-native campaign
bookkeeping commands. See `scripts/execution_infra/README.md` and
`docs/coding-agent-native-campaign.md`.

## Legacy / phase-era scripts

`run-day3-tests.py`, `test-phase2-redesign.py`,
`test-phase3-product-workflow.py`, `test-controlled-failures.py`,
`test-validators.py`, `mock_brief.md`, `deploy.sh` are phase-era test or
deployment helpers kept for reproducibility. They are not part of the current
operating path; prefer `pytest` and the validators above.
