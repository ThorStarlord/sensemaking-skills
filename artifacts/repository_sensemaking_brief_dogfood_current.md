# Repository Sensemaking Brief: sensemaking-skills dogfood (current state)

## 1. Repository goal

The repository is an agent-native framework for diagnosing repository uncertainty, producing validated sensemaking artifacts, and routing those artifacts to governed workflows. This is a current-state dogfood diagnosis after the validator portability and CI baseline fixes were merged.

## 2. Current shape

The repository contains the Python package under `src/sensemaking_skills/`, skills under `skills/`, workflow and artifact registries under `skills/workflow-planner/references/`, probes and validators under `scripts/`, and tests and fixtures under `tests/`. The current probe measured 3,817 tracked files, 134 test files, context entropy `0.01`, and `main` at commit `5c82e6b` (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:3-13`, `:20-26`).

## 3. Strong signals

- The wrapper now delegates validator execution through the current interpreter (`scripts/validate-and-report.py:370-376`), and a regression test exercises that cross-platform boundary (`tests/test_validate_and_report_interpreter.py:14-25`).
- The core assertion command is represented as one YAML scalar and has dedicated regression coverage (`.github/workflows/validation.yml:754-755`, `tests/test_validation_workflow_commands.py:9-23`).
- The probe engine remains deterministic and reports verification gap, fixture coverage, churn, and relationship findings in a machine-readable report.
- The workflow registry contains the exact `docs-contract-reconciliation` workflow, including `plan_only` mode (`skills/workflow-planner/references/workflow-registry.yaml:127-159`).

## 4. Missing pieces

- The current probe still measures a verification gap of `0.67`, meaning declared checks and directly declared CI checks do not fully align (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:35-43`).
- Fixture coverage remains `0.74` (14 of 19), with five missing fixture families: `validate-mode-coverage`, `validate-output`, `validate-repo`, `validate-run-log`, and `validate-skill-hygiene` (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:47-56`). This is a coverage signal, not an automatic requirement to add every fixture.
- The probe still finds competing version declarations: `package.json` declares `4.1.0`, while the Python metadata declares `0.2.2` (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:86-105`).
- ADRs 0018, 0019, and 0020 remain owner-review candidates because the relationship probe reports status-claim mismatches (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:373-410`).

## 5. Improvement opportunities

- Record an authority matrix for product version, Python packaging, JavaScript/tooling metadata, CI enforcement, and validator fixtures.
- Decide whether the five missing fixture families are required or intentionally waived, then encode the approved policy.
- Review ADRs 0018-0020 against current repository state and update their status only with owner approval.
- Keep baseline and post-fix dogfood artifacts clearly separated so historical observations are not mistaken for current claims.

## 6. Weakest boundary

The weakest boundary is the unresolved authority and enforcement contract. The portability and CI command failures are fixed and covered by regression tests, but the current probe still reports a non-zero verification gap, incomplete fixture coverage, a version conflict, and three ADR status candidates. Those findings require semantic or owner decisions that the probe cannot make.

**Weakness type:** Contract Mismatch

## 6.5. Problem classification (fog type)

**Primary fog type:** `docs_fog`

The current uncertainty is about which documentation, metadata, fixture policy, and ADR status statements are authoritative. It is not an unresolved product or UI requirement, and the implementation boundary that previously failed has now been repaired.

## 7. Evidence

<!-- mode: investigative -->

Verified current state: the fresh probe measured `main` at `5c82e6b`, `vg=0.67`, fixture coverage `0.74`, six untracked dogfood artifacts before this current probe was written, and no dirty tracked files (`artifacts/repo-sensemaker-current-dogfood-probe-report.yaml:3-13`, `:35-56`).

Verified implementation state: `scripts/validate-and-report.py:370-376` uses `sys.executable` for child validators, and `tests/test_validate_and_report_interpreter.py:14-25` asserts the wrapper succeeds through the active interpreter. The workflow command is now a single parsed command at `.github/workflows/validation.yml:755`, with a regression assertion in `tests/test_validation_workflow_commands.py:18-23`.

The remaining version and ADR findings are probe-generated evidence candidates, not decisions. The source files show the competing declarations and proposed ADR statuses, but neither the probe nor this brief assigns authority. Owner review remains required.

Logic trace: current source and regression tests show that the previously demonstrated interpreter and YAML parsing failures are repaired. The fresh probe still measures enforcement, fixture, version, and ADR disagreements. Because the remaining disagreements cross documentation, metadata, tests, and decision records, the weakest boundary is a contract mismatch requiring explicit authority decisions rather than another unscoped implementation pass.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: artifacts/repo-sensemaker-current-dogfood-probe-report.yaml
    lines: L7-L13
    quote: "head_sha: 5c82e6b"
    supports_claim: "The current probe measured the post-merge main checkout and its working-tree state."
  - file: artifacts/repo-sensemaker-current-dogfood-probe-report.yaml
    lines: L35-L35
    quote: "vg: 0.67"
    supports_claim: "The current probe measured a non-zero verification gap."
  - file: artifacts/repo-sensemaker-current-dogfood-probe-report.yaml
    lines: L50-L56
    quote: "  - validate-mode-coverage"
    supports_claim: "The current probe lists the five missing validator fixture families."
  - file: scripts/validate-and-report.py
    lines: L370-L376
    quote: "                sys.executable,"
    supports_claim: "The validator wrapper now uses the active Python interpreter."
  - file: tests/test_validate_and_report_interpreter.py
    lines: L14-L25
    quote: "def test_wrapper_uses_the_current_python_interpreter():"
    supports_claim: "The portability fix has direct regression coverage."
  - file: .github/workflows/validation.yml
    lines: L755
    quote: "        run: python -m pytest tests/test_repo_probes.py tests/test_probe_report_cli.py tests/test_probe_relationships.py tests/test_skill_distribution_probe.py tests/test_gate_relationship_findings.py tests/test_path_drift.py tests/test_cli.py -q"
    supports_claim: "The core CI assertion is represented as one shell command."
  - file: package.json
    lines: L3
    quote: "  \"version\": \"4.1.0\","
    supports_claim: "JavaScript/tooling metadata declares version 4.1.0."
  - file: pyproject.toml
    lines: L7
    quote: "version = \"0.2.2\""
    supports_claim: "Python project metadata declares version 0.2.2."
```

## 9. Why this boundary matters

If authority remains ambiguous, future contributors can choose the wrong release version, misread fixture coverage as either a defect or a waiver, or treat proposed ADR decisions as settled. That would undermine the repository's promise of durable, validated handoffs.

## 10. Candidate next steps

1. Commit the baseline and current dogfood artifacts as evidence-only history.
2. Decide whether the `package.json` and Python versions represent separate identities or one inconsistent version.
3. Decide whether the five missing validator fixture families are required or intentionally waived.
4. Review ADRs 0018-0020 and classify their status with owner approval.

## 11. Recommended next step

Commit the validated baseline and current dogfood artifacts separately from implementation changes. Then handle the version, fixture-policy, and ADR decisions as independent owner-gated follow-up tracks.

## 12. Recommended workflow

`docs-contract-reconciliation` in `plan_only` mode. This is a registry-verified workflow for reconciling documentation, registries, artifact contracts, templates, and validator rules (`skills/workflow-planner/references/workflow-registry.yaml:127-159`).

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: 00-user-intent.md
user_implied_fog_type: architecture_fog
primary_fog_type: docs_fog
diagnosis_conflict: true
escalation_recommended: true
evidence:
  - "artifacts/repo-sensemaker-current-dogfood-probe-report.yaml (lines L35-L56): current verification gap and fixture coverage"
  - "artifacts/repo-sensemaker-current-dogfood-probe-report.yaml (lines L86-L105): current version relationship finding"
  - "scripts/validate-and-report.py (lines L370-L376): current interpreter handoff"
  - "tests/test_validate_and_report_interpreter.py (lines L14-L25): portability regression coverage"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
weakest_boundary: "Contract Mismatch: unresolved authority and enforcement contract"
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-12T08:01:16Z"
immutable: true
```

## 14. Ready-to-copy prompt

Use `docs-contract-reconciliation` in `plan_only` mode on the current dogfood evidence. Treat `artifacts/repository_sensemaking_brief_dogfood.md` and `artifacts/repo-sensemaker-dogfood-probe-report.yaml` as the pre-fix baseline, and use the current-state brief and probe as post-merge evidence. Build an authority matrix for versions, fixture policy, CI enforcement, and ADR status. Do not mutate code or decision records until the owner approves each unresolved decision.
