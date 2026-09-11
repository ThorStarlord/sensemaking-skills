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

The `test_campaign_*.py` family now covers preflight, resume v1/v2, uncertainty history/relations, operability, bundle inspection, inventory/archive, strategy ergonomics, multi-target identity/drift/rebinding/relations, completion receipts, static workflow navigation, and shared companion IO.

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

```bash
python scripts/validate-strategic-state.py --repo-root .
python scripts/validate-candidate-directions.py --repo-root .

sensemaking-skills campaign strategy inspect --repo-root /path/to/repository --json
sensemaking-skills campaign strategy diff \
  --from-status /path/to/before-STATUS.md \
  --to-status /path/to/after-STATUS.md \
  --json
```

Only after an agent/owner has already selected an exact current frontier item and responsibility should `campaign strategy handoff` transport that explicit decision into Campaign v2.

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

```text
strategy inspect != correct strategy
strategy diff != better strategy
frontier membership != warranted responsibility
strategy handoff != responsibility selection
```

## 5. Campaign operating flow

### 5.1 Static golden-path navigation

Use the static navigation surface when the CLI has become too large to remember. It does not choose a flow or run steps.

```bash
sensemaking-skills campaign workflow list
sensemaking-skills campaign workflow show single-repository
sensemaking-skills campaign workflow show fresh-context
sensemaking-skills campaign workflow show transferred-campaign
sensemaking-skills campaign workflow show multi-repository
```

The same guidance ships in `skills/using-sensemaking/references/golden-paths-v1.md`.

```text
flow shown != flow recommended
step listed != step authorized
golden path != workflow engine
```

### 5.2 Initialize, admit evidence, and preflight

A target-bound Campaign workspace must be outside the target repository tree.

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaigns/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Determine and execute the next warranted repository step" \
  --target-repo /path/to/target-repository

sensemaking-skills campaign status --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign ingest --workspace /path/to/campaigns/CMP-0001 --artifact /path/to/repository_sensemaking_brief.md
sensemaking-skills campaign preflight --workspace /path/to/campaigns/CMP-0001
```

Admission/validator/preflight success does not authorize a semantic transition.

### 5.3 Observe, diagnose, and reconstruct

```bash
sensemaking-skills campaign inspect --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign semantic-state --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign explain --workspace /path/to/campaigns/CMP-0001 --ref <exact-ref>
sensemaking-skills campaign graph --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign graph-integrity --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign doctor --workspace /path/to/campaigns/CMP-0001 --json
sensemaking-skills campaign resume-profile --workspace /path/to/campaigns/CMP-0001 --profile working --json
```

Backward-compatible `campaign resume-context` remains available. `resume-profile` supports `minimal|working|audit`, deterministic tail-preserving `--max-items`, and optional preflight inclusion.

When responsibility type is already explicitly selected:

```bash
sensemaking-skills campaign capability-context \
  --workspace /path/to/campaigns/CMP-0001 \
  --responsibility-type repository_diagnosis \
  --json
```

```text
preflight PASS != should proceed
capability compatibility != capability selection
doctor finding != repair decision
progressive disclosure != semantic summarization
```

### 5.4 Uncertainty lifecycle and explicit relationships

```bash
sensemaking-skills campaign uncertainty-record --help
sensemaking-skills campaign uncertainty-history --help
sensemaking-skills campaign uncertainty-relate --help
sensemaking-skills campaign uncertainty-show --help
sensemaking-skills campaign uncertainty-graph --help
```

`CampaignState.active_uncertainty` remains current authority. History/relationship companions preserve authored context; they do not rank uncertainties.

### 5.5 Bundle inspection, import, and portable target rebinding

Inspect transported bytes before durable import:

```bash
sensemaking-skills campaign bundle-inspect --bundle /tmp/CMP-0001.zip --json
sensemaking-skills campaign bundle-resume-context --bundle /tmp/CMP-0001.zip --profile working --json
sensemaking-skills campaign bundle-graph --bundle /tmp/CMP-0001.zip --json
sensemaking-skills campaign bundle-verify --bundle /tmp/CMP-0001.zip --json
sensemaking-skills campaign bundle-import --bundle /tmp/CMP-0001.zip --workspace /path/to/imported/CMP-0001
```

After relocation/import, supply the target path explicitly. Sensemaking does not search for a repository.

```bash
sensemaking-skills campaign target rebind \
  --workspace /path/to/imported/CMP-0001 \
  --target-repo /new/path/to/repository \
  --json

sensemaking-skills campaign target verify-rebind \
  --workspace /path/to/imported/CMP-0001 \
  --json
```

Primary rebinding writes `target-rebind.json` and does not rewrite canonical `CampaignState.target_snapshot` provenance. The candidate repository must have the same recorded identity and exact recorded Git/worktree state.

```text
rebind valid != repository selected
rebind != target refresh
rebind != work authorized
```

### 5.6 Multi-repository target sets, rebinding, and dependencies

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

Inspect/verify and explicitly record a changed target snapshot when authorized work changes it:

```bash
sensemaking-skills campaign multi-target inspect --workspace /path/to/campaigns/CMP-0001 --json
sensemaking-skills campaign multi-target verify --workspace /path/to/campaigns/CMP-0001 --json
sensemaking-skills campaign multi-target refresh --workspace /path/to/campaigns/CMP-0001 --alias frontend --json
```

For an equivalent repository relocated to a new filesystem path:

```bash
sensemaking-skills campaign multi-target rebind \
  --workspace /path/to/campaigns/CMP-0001 \
  --alias backend \
  --target-repo /new/path/to/backend \
  --json
```

Declare cross-repository relationships only after the agent/human has authored them:

```bash
sensemaking-skills campaign multi-target relate \
  --workspace /path/to/campaigns/CMP-0001 \
  --relation-id REL-17 \
  --source-alias frontend \
  --target-alias backend \
  --relation-type depends_on \
  --json

sensemaking-skills campaign multi-target dependency-check \
  --workspace /path/to/campaigns/CMP-0001 \
  --json

sensemaking-skills campaign multi-target graph \
  --workspace /path/to/campaigns/CMP-0001 \
  --format mermaid
```

Supported relation classes are `depends_on`, `provides_interface_to`, `consumes_interface_from`, `must_change_with`, and `release_after`. Only `depends_on` and `release_after` participate in deterministic ordering-cycle rejection.

When the relation companion is present, Campaign Preflight validates its aliases/evidence/hash chain/ordering constraints as another mechanical check.

```text
repository supplied != repository discovered by tool
relationship recorded != architectural truth
dependency graph valid != execution plan correct
release_after != deployment authorized
same Campaign != atomic deployment unit
```

### 5.7 Campaign completion, archival, and inventory

`campaign close` remains the semantic terminal decision. Only afterward create a mechanical receipt:

```bash
sensemaking-skills campaign closeout \
  --workspace /path/to/campaigns/CMP-0001 \
  --json

sensemaking-skills campaign completion-receipt \
  --workspace /path/to/campaigns/CMP-0001 \
  --json
```

The receipt binds terminal state, transitions/evidence, mechanical preflight/provenance status, and a SHA-256 manifest of durable workspace files. If durable bytes later change, the old receipt becomes stale until closeout is explicitly regenerated.

Optional archive marker:

```bash
sensemaking-skills campaign archive \
  --workspace /path/to/campaigns/CMP-0001 \
  --json
```

Archive does not move or delete the workspace and does not mean success.

Inventory hides valid archived workspaces by default:

```bash
sensemaking-skills campaign inventory --root /path/to/campaigns --json
sensemaking-skills campaign inventory --root /path/to/campaigns --include-archived --json
```

```text
completion receipt valid != terminal decision correct
archive != success
inventory != prioritization
```

### 5.8 Local provenance and explicit semantic decisions

```bash
sensemaking-skills campaign provenance --workspace /path/to/campaigns/CMP-0001 --format markdown
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
sensemaking-skills campaign handoff --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/campaigns/CMP-0001
```

Actual GitHub publication/mutation remains separately authorized.

```text
generate provenance != publish provenance
validator/drift/dependency status != semantic transition
```

### 5.9 Relevant implementation contracts

```text
docs/sensemaking-campaign.md
docs/campaign-target-snapshot.md
docs/campaign-observability-and-portability.md
docs/campaign-preflight.md
docs/campaign-usability-composition-v1.md
docs/strategic-outer-loop-ergonomics-v1.md
docs/multi-repository-campaigns-v1.md
docs/portable-target-rebinding-v1.md
docs/cross-repository-dependency-declarations-v1.md
docs/campaign-completion-and-archival-v1.md
docs/agent-workflow-golden-path-v1.md
docs/surface-simplification-and-contract-consolidation-v1.md
```

## 6. Retained Lab Validation

`.github/workflows/lab-validation.yml` owns retained source-only research/lab compatibility claims.

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
6. campaign workflow show ...        — optional static navigation, not routing
7. branch/code/tests                 — Level 1 execution
8. terminal decision + closeout      — semantic close first; receipt second
9. this operations runbook           — current mechanical qualification path
```

After integration, reconcile Level-3 state and reassess. Do not automatically select another package merely because one appears next in an old phase, historical milestone, golden path, or candidate reservoir.