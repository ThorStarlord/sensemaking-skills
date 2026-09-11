# Sensemaking Skills Operations and Qualification Runbook

**Status:** current operator-facing operations/qualification runbook  
**Updated:** 2026-09-11  
**Audience:** maintainers, coding agents, and human qualification/release operators  
**Executable authority:** checked-in GitHub Actions workflows and current repository code  
**Strategic authority:** `docs/product-strategy.md` + `STATUS.md`

## 1. Purpose and authority

This is the single current operator-facing runbook for repository validation, Campaign operation, qualification, and release-candidate checks.

```text
this runbook != semantic truth
this runbook != strategy authority
this runbook != merge/release authorization
local reproduction != hosted cross-platform CI proof
```

When prose and executable behavior disagree, current checked-in code/workflows govern what the software actually enforces. Reconcile this runbook rather than using prose to override code.

Current CI authorities:

```text
.github/workflows/validation.yml          Product Validation
.github/workflows/lab-validation.yml      retained Lab Validation
.github/workflows/release-candidate.yml   Release Candidate Distribution
```

Current strategic representation guards:

```text
scripts/validate-strategic-state.py
scripts/validate-candidate-directions.py
```

Neither strategic validator decides strategy quality or priority.

## 2. Development setup

```bash
python -m venv .venv
# activate the environment
python -m pip install --upgrade pip
python -m pip install -e . pytest pytest-subtests
sensemaking-skills --version
```

Current package version: `0.3.0`.

For retained lab compatibility checks only:

```bash
python -m pip install -e . --no-deps
python -m pip install "click>=8.1.0" "PyYAML>=6.0,<7.0" -r requirements-lab.txt
```

Do not add source-only lab dependencies to shipped core merely to simplify testing.

## 3. Product Validation

`.github/workflows/validation.yml` is executable authority. Closest local reproduction follows.

### 3.1 Product/lab boundary

```bash
python scripts/validate-product-boundary.py
```

### 3.2 Campaign product suite

Run on Python 3.11 and 3.12 when reproducing the matrix:

```bash
python -m pytest \
  tests/test_campaign_contract_roundtrip.py \
  tests/test_product_lab_boundary.py \
  tests/campaign_validation/test_artifact_admission.py \
  tests/campaign_validation/test_campaign_*.py \
  tests/campaign_validation/test_harness_adapters.py \
  tests/campaign_validation/test_release_candidate_contract.py \
  tests/campaign_validation/test_repo_sensemaker_connector_probe_contract.py \
  tests/campaign_validation/test_workflow_liveness_contract.py \
  tests/integration/test_external_golden_path_qualification.py \
  -q
```

The `test_campaign_*.py` family includes repository/hermetic coverage for preflight, Resume Capsule v1/v2, uncertainty history/relations, operability, bundle inspection, inventory, strategy ergonomics, and multi-target identity/drift behavior.

### 3.3 Installed-core-wheel regressions

```bash
python -m pytest tests/campaign_validation/test_installed_wheel_smoke.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p9.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p10.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p11.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_setup_skills.py -q -rs
```

### 3.4 Repository, strategic-state, candidate, and Skill contracts

```bash
python scripts/validate-repo.py
python scripts/validate-strategic-state.py --repo-root .
python scripts/validate-candidate-directions.py --repo-root .

python scripts/probe-repo.py --repo-root . --output /tmp/probe-report.yaml
python scripts/validate-probe-report.py /tmp/probe-report.yaml --repo-root .
python scripts/gate_relationship_findings.py --report /tmp/probe-report.yaml

sensemaking-skills semantic conformance \
  --manifests-dir skill-manifests \
  --domain-packs-dir domain-packs \
  --repo-root . \
  --json
```

Use an OS-appropriate temporary path instead of `/tmp` on Windows.

Read-only manifest/Domain Pack discovery:

```bash
sensemaking-skills semantic catalog \
  --manifests-dir skill-manifests \
  --domain-packs-dir domain-packs \
  --repo-root . \
  --json
```

`semantic catalog` does not replace conformance and does not select/rank a Skill.

Stable repository assertion set:

```bash
python -m pytest \
  tests/test_repo_probes.py \
  tests/test_probe_report_cli.py \
  tests/test_probe_relationships.py \
  tests/test_skill_distribution_probe.py \
  tests/test_gate_relationship_findings.py \
  tests/test_path_drift.py \
  tests/test_cli.py \
  tests/test_operations_runbook_authority.py \
  tests/test_candidate_directions_validation.py \
  tests/test_semantic_reasoning_profile.py \
  tests/test_skill_registry_liveness.py \
  tests/test_strategic_state_validation.py \
  tests/test_semantic_substrate.py \
  tests/test_semantic_reference_audit.py \
  tests/test_semantic_conformance.py \
  tests/test_semantic_cli.py \
  tests/test_semantic_catalog.py \
  -q
```

Claim limits:

```text
strategic-state validator PASS != strategy correct
candidate-directions validator PASS != candidate prioritized
semantic conformance PASS != Skill should run
semantic catalog hit != Skill selected
repository tests PASS != native-harness qualification
```

### 3.5 Filesystem-security contracts

```bash
python -m pytest tests/test_gate_a_authorization_consumer.py -q
python -m pytest tests/test_gate_a_path_canonicalization.py -q
python -m pytest tests/test_gate_a_physical_containment.py -q -rs
```

The same family runs on hosted Windows. Local Unix proof is not hosted Windows proof.

### 3.6 Clean-tree rule

```bash
git status --porcelain
```

Expected: validation created no tracked repository changes.

## 4. Strategic Repository Evolution integrity and ergonomics

`STATUS.md` is current Level-3 state. `docs/product-strategy.md` is Level-4 product-thesis authority. `docs/strategic-candidate-directions.md` is non-authoritative idea memory.

Mechanical representation validation:

```bash
python scripts/validate-strategic-state.py --repo-root .
python scripts/validate-candidate-directions.py --repo-root .
```

Read current Level-3 representation without ranking it:

```bash
sensemaking-skills campaign strategy inspect \
  --repo-root /path/to/repository \
  --json
```

Compare two explicit status representations without deciding which is better:

```bash
sensemaking-skills campaign strategy diff \
  --from-status /path/to/before-STATUS.md \
  --to-status /path/to/after-STATUS.md \
  --json
```

After an agent/owner has **already** selected an exact current frontier item and responsibility, transport that explicit decision into Campaign v2:

```bash
sensemaking-skills campaign strategy handoff \
  --repo-root /path/to/repository \
  --workspace /path/to/campaigns/CMP-0002 \
  --campaign-id CMP-0002 \
  --mission "Execute the explicitly selected repository responsibility" \
  --frontier-item "<exact current Strategic Frontier item>" \
  --responsibility-id R-42 \
  --responsibility-type repository_diagnosis \
  --responsibility-statement "<explicit statement>" \
  --decision-blocked "<explicit blocked decision>" \
  --scope repository \
  --authority authorized_autonomously \
  --success-condition "<explicit success condition>" \
  --target-repo /path/to/target-repository \
  --json
```

The command verifies occurrence of the supplied frontier identity and records the exact source `STATUS.md` SHA-256. It does not select frontier/responsibility/authority.

```text
strategy inspect != correct strategy
strategy diff != better strategy
frontier membership != warranted responsibility
strategy handoff != responsibility selection
```

## 5. Campaign operating flow

### 5.1 Initialize and validate

A target-bound Campaign workspace must be outside the target repository tree.

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaigns/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Determine and execute the next warranted repository step" \
  --target-repo /path/to/target-repository

sensemaking-skills campaign status --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/campaigns/CMP-0001
```

### 5.2 Admit evidence

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/campaigns/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

Admission/validator success is not transition authorization.

### 5.3 Preflight, observability, and diagnostics

```bash
sensemaking-skills campaign preflight --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign inspect --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign semantic-state --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign explain --workspace /path/to/campaigns/CMP-0001 --ref <exact-ref>
sensemaking-skills campaign graph --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign graph-integrity --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign doctor --workspace /path/to/campaigns/CMP-0001 --json
```

When an explicit responsibility classification is already known:

```bash
sensemaking-skills campaign capability-context \
  --workspace /path/to/campaigns/CMP-0001 \
  --responsibility-type repository_diagnosis \
  --json
```

Preflight can use the same explicit classification via `--responsibility-type`. When a multi-target companion exists, preflight also verifies every declared target's current identity/snapshot.

```text
preflight PASS != should proceed
capability compatibility != capability selection
doctor finding != repair decision
graph integrity != semantic causality
```

### 5.4 Resume Capsule v1 and v2

Backward-compatible v1:

```bash
sensemaking-skills campaign resume-context \
  --workspace /path/to/campaigns/CMP-0001

sensemaking-skills campaign resume-context \
  --workspace /path/to/campaigns/CMP-0001 \
  --compact \
  --recent-transitions 3 \
  --include-preflight \
  --json
```

Progressive-disclosure v2:

```bash
sensemaking-skills campaign resume-profile \
  --workspace /path/to/campaigns/CMP-0001 \
  --profile minimal \
  --json

sensemaking-skills campaign resume-profile \
  --workspace /path/to/campaigns/CMP-0001 \
  --profile working \
  --max-items 10 \
  --include-preflight \
  --json

sensemaking-skills campaign resume-profile \
  --workspace /path/to/campaigns/CMP-0001 \
  --profile audit \
  --json
```

`--max-items` is deterministic tail-preserving bounding with omission counts.

```text
progressive disclosure != semantic summarization
bounded output != evidence ranking
```

### 5.5 Uncertainty lifecycle and explicit relationships

Lifecycle history:

```bash
sensemaking-skills campaign uncertainty-record \
  --workspace /path/to/campaigns/CMP-0001 \
  --event-id UE-12 \
  --uncertainty-id U-7 \
  --status resolved \
  --transition-id T-21

sensemaking-skills campaign uncertainty-history \
  --workspace /path/to/campaigns/CMP-0001 \
  --json
```

Explicit relations:

```bash
sensemaking-skills campaign uncertainty-relate \
  --workspace /path/to/campaigns/CMP-0001 \
  --relation-id UR-12 \
  --uncertainty-id U-7 \
  --relation depends_on \
  --target U-8 \
  --json

sensemaking-skills campaign uncertainty-show \
  --workspace /path/to/campaigns/CMP-0001 \
  U-7 \
  --json

sensemaking-skills campaign uncertainty-graph \
  --workspace /path/to/campaigns/CMP-0001 \
  --format json
```

Supported relation classes are explicit `depends_on`, `blocks_decision`, `introduced_by_transition`, `resolved_by_transition`, and `supersedes` records.

```text
CampaignState.active_uncertainty = current authority
history/relations = authored durable companions
uncertainty graph != uncertainty ranking
```

### 5.6 Bundle transport and pre-import inspection

Existing transport:

```bash
sensemaking-skills campaign bundle-export --workspace /path/to/campaigns/CMP-0001 --output /tmp/CMP-0001.zip
sensemaking-skills campaign bundle-verify --bundle /tmp/CMP-0001.zip --json
sensemaking-skills campaign bundle-import --bundle /tmp/CMP-0001.zip --workspace /path/to/imported/CMP-0001
```

Inspect before durable import:

```bash
sensemaking-skills campaign bundle-inspect --bundle /tmp/CMP-0001.zip --json
sensemaking-skills campaign bundle-resume-context --bundle /tmp/CMP-0001.zip --profile working --json
sensemaking-skills campaign bundle-graph --bundle /tmp/CMP-0001.zip --json
```

The projection uses an ephemeral internal workspace that is discarded after inspection.

```text
bundle verified != import authorized
bundle projection != durable import
```

### 5.7 Campaign inventory

```bash
sensemaking-skills campaign inventory \
  --root /path/to/campaigns \
  --json
```

Inventory enumerates direct child Campaign workspaces, state, target identity, active responsibility, last transition, and mechanical integrity.

```text
inventory != prioritization
```

### 5.8 Multi-repository target sets

Multi-repository responsibilities use an additive companion; Campaign schema remains v2 and the existing primary `target_snapshot` semantics remain unchanged.

Bind explicitly selected repositories:

```bash
sensemaking-skills campaign multi-target add \
  --workspace /path/to/campaigns/CMP-0001 \
  --alias frontend \
  --target-repo /path/to/frontend \
  --role "web client" \
  --authority authorized_autonomously \
  --json

sensemaking-skills campaign multi-target add \
  --workspace /path/to/campaigns/CMP-0001 \
  --alias backend \
  --target-repo /path/to/backend \
  --role "service API" \
  --authority authorized_autonomously \
  --json
```

Inspect and verify:

```bash
sensemaking-skills campaign multi-target inspect --workspace /path/to/campaigns/CMP-0001 --json
sensemaking-skills campaign multi-target verify --workspace /path/to/campaigns/CMP-0001 --json
sensemaking-skills campaign multi-target verify --workspace /path/to/campaigns/CMP-0001 --alias frontend --json
```

After authorized work changes one target and repository identity is still the same, explicitly record its new snapshot:

```bash
sensemaking-skills campaign multi-target refresh \
  --workspace /path/to/campaigns/CMP-0001 \
  --alias frontend \
  --json
```

`multi-targets.json` carries target-set identity; `multi-target-history.jsonl` records refresh edges.

```text
repository supplied != repository discovered by tool
multi-target verified != semantic correctness
same Campaign != atomic deployment unit
refresh != semantic approval
```

True cross-repository commit/deployment/rollback atomicity is not part of v1.

### 5.9 Local provenance

```bash
sensemaking-skills campaign provenance \
  --workspace /path/to/campaigns/CMP-0001 \
  --format markdown
```

JSON is available with `--format json`.

```text
generate provenance != publish provenance
published provenance != semantic correctness
```

GitHub mutation remains separately authorized.

### 5.10 Semantic transitions, handoff, and resume

Only after the active agent/human has made the semantic decision:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

Then produce/reconsume durable handoff as appropriate:

```bash
sensemaking-skills campaign handoff --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/campaigns/CMP-0001
```

Validators, drift checks, capability availability, strategy representation, inventory, and graph state never create a semantic transition automatically.

Deeper contracts:

```text
docs/sensemaking-campaign.md
docs/campaign-target-snapshot.md
docs/campaign-observability-and-portability.md
docs/campaign-handoff-resume.md
docs/campaign-preflight.md
docs/resume-capsule-v1.md
docs/uncertainty-history.md
docs/campaign-operability-v1.md
docs/extensibility-and-simplification-v1.md
docs/campaign-usability-composition-v1.md
docs/strategic-outer-loop-ergonomics-v1.md
docs/multi-repository-campaigns-v1.md
```

## 6. Retained Lab Validation

`.github/workflows/lab-validation.yml` owns retained source-only research/lab compatibility claims.

Closest local Linux/macOS reproduction:

```bash
export PYTHONPATH=src
python -m pytest \
  tests/campaign_validation \
  --ignore-glob="tests/campaign_validation/test_installed_wheel_*.py" \
  tests/test_two_lane_schema_contracts.py \
  tests/test_exploratory_digests.py \
  tests/test_exploratory_lane_derivation.py \
  tests/test_exploratory_capability_lifecycle.py \
  tests/campaign_accounting \
  tests/campaign_preparation \
  tests/execution_infra_tests \
  -q
```

Windows historical confinement proofs:

```bash
python -m pytest tests/campaign_accounting/test_artifact_path_confinement.py -q
python -m pytest tests/campaign_accounting/test_artifact_path_confinement_windows.py -q
```

Running retained compatibility tests does not create a new operative experiment; the workflow explicitly checks that it does not create operative experiment state. Lab qualification is not native-harness evidence.

## 7. Release Candidate Distribution

`.github/workflows/release-candidate.yml` is exact-head distribution authority for v0.3.0.

```bash
python scripts/validate-product-boundary.py
python -m pytest \
  tests/campaign_validation/test_release_candidate_contract.py \
  tests/campaign_validation/test_campaign_schema_evolution.py \
  tests/integration/test_external_golden_path_qualification.py \
  -q

python -m pip install -e . pytest pytest-subtests build twine
rm -rf build dist
python -m build
python -m twine check dist/*
```

Current artifacts:

```text
sensemaking_skills-0.3.0-py3-none-any.whl
sensemaking_skills-0.3.0.tar.gz
```

Qualification applies only to the exact candidate head that passed. If the head changes, rerun rather than borrowing stale green evidence.

## 8. Human/owner gates

Owner/human authority remains required for matters reserved by current contracts, including major Level-4 thesis changes, public claim expansion, live/destructive external operations, and empirical/native-harness work when those stronger claims are pursued.

Explicit owner direction may authorize bounded repository-only/hermetic construction without a new experiment as a universal prerequisite.

```text
owner direction to build != empirical product-value proof
validator passed != authorization beyond its declared scope
```

## 9. Native-harness / empirical evidence ceiling

```text
repository qualified
!= native-harness qualified
!= portability qualified
!= promoted / product-value established
```

Real-harness PASS claims still require their canonical external-attempt evidence. Current owner direction defers such experiments; repository/hermetic development may continue without pretending those claims are proven.

## 10. Historical milestone runbooks

These are retained as historical evidence, **not current operational authority**:

```text
docs/milestone-runbook.md
docs/post-milestone-handoff-runbook.md
```

Current operators start with `docs/operations-runbook.md`.

## 11. Normal repository-development entry sequence

```text
1. docs/product-strategy.md          — Level 4: what/why
2. STATUS.md                         — Level 3: current state/frontier
3. relevant ADRs/contracts           — ratified boundaries
4. explicit strategy handoff if used — transport, not selection
5. active Campaign/work package      — Level 2 responsibility
6. branch/code/tests                 — Level 1 execution
7. this operations runbook           — current mechanical qualification path
```

After integration, reconcile Level-3 state and reassess. Do not automatically select another package merely because one appears next in an old phase, historical milestone, or candidate reservoir.