# Repository Sensemaking Brief: sensemaking-skills dogfood

## 1. Repository goal

The repository is an agent-native framework for diagnosing repository uncertainty, producing validated sensemaking artifacts, and routing those artifacts to governed workflows. The repository's existing owner-intent artifact frames the current work as closing structural gaps before production deployment (`00-user-intent.md:5-21`). This run is a dogfood diagnosis of the framework itself; the current user request does not add a separate product or UI requirement.

## 2. Current shape

The repo contains the Python package under `src/sensemaking_skills/`, a broad `skills/` tree, workflow and artifact registries under `skills/workflow-planner/references/`, deterministic probes and validators under `scripts/`, tests and fixtures under `tests/`, and extensive live, historical, generated, and candidate documentation. The probe measured 3,815 tracked files, 132 test files, and a 0.0 context-entropy score at `63350d4` before this dogfood artifact and probe report were written (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:5-45`).

The target skill explicitly requires a probe before synthesis, evidence-backed weakest-boundary classification, and registry-verified workflow IDs (`skills/repo-sensemaker/SKILL.md:88-144`).

## 3. Strong signals

- The repository has a dedicated, deterministic probe engine and a validated probe-report contract. The dogfood probe completed successfully and recorded git state, verification gap, test collection, fixture coverage, churn, and relationship findings.
- The skill's producer guidance is unusually explicit about state currency: measured probe values outrank documentation, relationship findings are evidence candidates rather than diagnoses, and the final brief must distinguish observed evidence from documented claims and inference (`skills/repo-sensemaker/SKILL.md:101-144`).
- The checked-out tree was on `main` at commit `63350d4` with zero untracked files and zero dirty files when the probe ran (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:5-13`). This is a time-bounded verified observation, not a claim about the tree after this artifact was generated.
- The workflow registry contains an exact `docs-contract-reconciliation` workflow with `repo-sensemaker` as its first step and an explicit `plan_only` mode (`skills/workflow-planner/references/workflow-registry.yaml:127-153`).
- The artifact itself passes the direct `validate-brief.py --json` contract validator. This proves the brief grammar is acceptable even though the higher-level wrapper path below is not portable in this environment.

## 4. Missing pieces

- The probe measured a verification gap of `0.67`: the repository declares six checks, but only two of those declared checks appear directly in CI while other checks are enforced through different entry points (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:14-36`). This is a measured alignment gap, not proof that every indirectly exercised validator is unused.
- Validator fixture coverage is `0.74` (14 of 19), with five named gaps: `validate-mode-coverage`, `validate-output`, `validate-repo`, `validate-run-log`, and `validate-skill-hygiene` (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:47-56`). The missing fixture list identifies coverage or orphan candidates; it does not by itself prove that each validator lacks meaningful tests.
- Package metadata and documentation do not present one unambiguous version authority. The probe recorded a relationship finding containing `4.1.0` in `package.json` and `0.2.2` in the Python package declarations (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:77-105`).
- ADR relationship findings also require semantic review: the probe found three status-claim mismatches involving ADRs 0018, 0019, and 0020 (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:373-410`).
- The documented wrapper path is not portable in this Windows environment: `GETTING_STARTED.md:111-114` tells users to run the wrapper with `python`, while `scripts/validate-and-report.py:379-386` hardcodes `python3` for the child validator. The direct validator passed, but the wrapper returned an execution error because the `python3` command was unavailable.

## 5. Improvement opportunities

- Add a small authority matrix that names the authoritative source for product version, Python dependencies, JavaScript/tooling metadata, validator entry points, and CI enforcement.
- Reconcile the broad README claim `No external dependencies` with the package's declared Python dependencies, or narrow the wording explicitly to external services and credentials (`README.md:21-46`, `pyproject.toml:11-15`).
- Add or explicitly justify fixtures for the five validators in the probe's missing-fixture list, then rerun the probe so the coverage value reflects the decision.
- Review the three ADR status findings and label stale statements as historical or update them only after the owner confirms the authoritative status.
- Keep the generated probe report outside the tracked artifact set in normal CI, as the workflow itself requires a temporary report and a clean tree after probing (`.github/workflows/validation.yml:692-736`).

## 6. Weakest boundary

The weakest boundary is the executable validation handoff. The public usage path tells a user to invoke `validate-and-report.py` with `python` (`GETTING_STARTED.md:107-114`), but the wrapper launches the selected validator with a hardcoded `python3` executable (`scripts/validate-and-report.py:378-399`). In this dogfood run, the direct validator passed while the wrapper failed because that executable was unavailable in the Windows environment. The probe also measured `vg=0.67`, incomplete fixture coverage, and conflicting version declarations, showing that this is part of a broader authority/enforcement alignment problem rather than an isolated command typo.

**Weakness type:** Implicit Dependencies

## 6.5. Problem classification (fog type)

**Primary fog type:** `docs_fog`

The existing owner intent implies `architecture_fog` because it asks for structural framework fixes (`00-user-intent.md:5-10`). The current diagnosis is `docs_fog` because the demonstrated failure is in the documented validation contract and executable handoff rather than unclear user value, UI behavior, or module structure. This is a conflict between the existing implied intent and the current repository diagnosis, so escalation is recommended for owner review of authority decisions.

## 7. Evidence

<!-- mode: investigative -->

Verified current state: the probe report generated at `2026-08-12T04:38:22Z` measured a clean `main` checkout at `63350d4`, `vg=0.67`, fixture coverage `0.74`, and one version relationship finding (`artifacts/repo-sensemaker-dogfood-probe-report.yaml:3-13`, `:35-56`, `:77-105`). The clean-tree observation predates creation of this dogfood report and therefore is not being presented as the final working-tree state.

Observed execution evidence: the direct `validate-brief.py --json` command passed for this artifact, but the documented `validate-and-report.py` wrapper failed because its child command was hardcoded to `python3`, which is not available in the current Windows environment. The source contract is visible at `GETTING_STARTED.md:111-114` and `scripts/validate-and-report.py:379-386`. This is an environment observation with a repository-level cause, not a claim that every supported runner fails.

Additional source evidence: `package.json:3` declares `4.1.0`, while `pyproject.toml:7` and `setup.py:42` declare `0.2.2`. Documented state claims reconciliation in `STATUS.md:11-14`, but that claim is not treated as proof that all declarations are current. The README says `No external dependencies` at `README.md:29`, while the Python package declares runtime dependencies at `pyproject.toml:11-15`; the surrounding README text narrows the claim to no external API calls and no credentials, so the wording needs semantic reconciliation rather than an automatic bug verdict.

Documented owner context: `00-user-intent.md:5-21` asks for structural fixes and integrated validation. That is owner-supplied context, not an independently verified repository fact.

Logic trace: the dogfood run first proves that the brief and direct validator contract work, then fails at the wrapper boundary because the wrapper assumes a `python3` executable that the documented Windows invocation does not establish. The probe adds measured evidence that declared checks and fixture coverage do not line up cleanly, and its relationship scanner identifies conflicting version declarations. Because the public command and the wrapper disagree about the interpreter boundary, the immediate weakness is an `Implicit Dependencies` failure; the broader version and enforcement drift makes it a documentation/contract reconciliation problem. The owner-intent conflict remains explicit rather than silently resolved.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: artifacts/repo-sensemaker-dogfood-probe-report.yaml
    lines: L35-L36
    quote: "vg: 0.67"
    supports_claim: "The mandatory probe measured a non-zero verification gap and explicitly reported declared-but-unenforced checks."
  - file: artifacts/repo-sensemaker-dogfood-probe-report.yaml
    lines: L47-L56
    quote: "coverage: 0.74"
    supports_claim: "The probe measured incomplete validator fixture coverage and listed five missing fixtures."
  - file: artifacts/repo-sensemaker-dogfood-probe-report.yaml
    lines: L77-L99
    quote: "value: 4.1.0"
    supports_claim: "The relationship probe recorded a product-version declaration of 4.1.0 before the 0.2.2 declarations."
  - file: GETTING_STARTED.md
    lines: L111-L114
    quote: "python scripts/validate-and-report.py artifacts/repository_sensemaking_brief.md"
    supports_claim: "The documented wrapper invocation uses the generic python command."
  - file: scripts/validate-and-report.py
    lines: L379-L385
    quote: '"python3",'
    supports_claim: "The wrapper introduces an implicit dependency on a python3 executable for the child validator."
  - file: package.json
    lines: L3
    quote: '"version": "4.1.0",'
    supports_claim: "The JavaScript/tooling metadata declares a different version from the Python package."
  - file: pyproject.toml
    lines: L7
    quote: 'version = "0.2.2"'
    supports_claim: "The Python project metadata declares version 0.2.2."
  - file: setup.py
    lines: L42
    quote: 'version="0.2.2",'
    supports_claim: "The legacy Python packaging metadata agrees with pyproject.toml rather than package.json."
  - file: STATUS.md
    lines: L11-L12
    quote: "Documentation reconciled: README version/API claims match the codebase"
    supports_claim: "A living status document claims that version/API documentation was already reconciled."
  - file: 00-user-intent.md
    lines: L5-L10
    quote: "Fix four structural gaps in the sensemaking skills system to stabilize the framework for production deployment:"
    supports_claim: "The existing owner-intent artifact implies a structural/architecture-oriented concern."
```

## 9. Why this boundary matters

If authority remains ambiguous, a future agent or release process can select the wrong version, install an incomplete dependency set, believe a validator is enforced when it is only documented, or treat an unresolved ADR status as settled. That undermines the repository's central promise of durable, validated handoffs and makes later drift harder to distinguish from historical documentation.

## 10. Candidate next steps

1. Run `docs-contract-reconciliation` in `plan_only` mode to produce an authority matrix and a proposed reconciliation report.
2. Decide which version declaration is authoritative and classify `package.json` as product metadata, tooling metadata, or stale material.
3. Reconcile README dependency wording with `pyproject.toml` and `setup.py`, then verify install behavior in the supported Python versions.
4. Add or explicitly waive the five missing validator fixtures and rerun the probe.
5. Review the three ADR status findings with the owner before changing accepted/proposed labels.

## 11. Recommended next step

Use the registry-verified `docs-contract-reconciliation` workflow in `plan_only` mode to reconcile the validation entry point first: make the wrapper invoke the same interpreter as the parent process, then add a Windows smoke test for the documented command. Include the version, dependency, CI-enforcement, fixture, and ADR findings in the authority matrix; do not assume which declaration wins where repository evidence cannot decide. The workflow is defined at `skills/workflow-planner/references/workflow-registry.yaml:127-153` and permits `plan_only` at `:137-140`.

## 12. Recommended workflow

`docs-contract-reconciliation` — plan-only documentation and contract reconciliation. This is a verified registry ID, and its first step is `repo-sensemaker`; subsequent steps produce a reconciliation report and handoff (`skills/workflow-planner/references/workflow-registry.yaml:127-159`).

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
  - "artifacts/repo-sensemaker-dogfood-probe-report.yaml (lines L35-L56): measured vg=0.67 and fixture coverage=0.74 with five missing fixtures"
  - "artifacts/repo-sensemaker-dogfood-probe-report.yaml (lines L77-L105): measured version relationship finding across 4.1.0 and 0.2.2 declarations"
  - "package.json (line L3), pyproject.toml (line L7), setup.py (line L42): competing package-version declarations"
  - "STATUS.md (lines L11-L14): documented claim that README version/API claims match the codebase"
  - "GETTING_STARTED.md (lines L111-L114) and scripts/validate-and-report.py (lines L379-L386): documented python invocation versus hardcoded python3 child process"
  - "00-user-intent.md (lines L5-L10): owner-supplied structural-fix intent"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
weakest_boundary: "Implicit Dependencies: wrapper requires an undocumented python3 executable"
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-12T04:38:22Z"
immutable: true
```

## 14. Ready-to-copy prompt

Use `docs-contract-reconciliation` in `plan_only` mode on this repository. Start from the dogfood brief and probe report. First reconcile the documented `python scripts/validate-and-report.py` command with the wrapper's hardcoded `python3` child process and specify a cross-platform interpreter contract plus a Windows smoke test. Then build an authority matrix for package versions, Python dependencies, JavaScript/tooling metadata, CI enforcement, fixtures, and ADR status. Separate verified facts from documented claims and owner decisions. Do not mutate code, registries, contracts, or documentation until the competing authorities and required owner approvals are explicit. After the plan is ratified, rerun the probe and artifact validation to confirm the contract is coherent.
