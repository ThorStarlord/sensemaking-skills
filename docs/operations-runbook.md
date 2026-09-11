# Sensemaking Skills Operations and Qualification Runbook

**Status:** current operator-facing operations/qualification runbook  
**Updated:** 2026-09-11  
**Audience:** maintainers, coding agents, and human qualification/release operators  
**Executable authority:** checked-in GitHub Actions workflows and current repository code  
**Strategic authority:** `docs/product-strategy.md` + `STATUS.md`

## 1. Purpose and authority

This document is the single current operator-facing runbook for ordinary repository validation, qualification, release-candidate checks, Campaign operation, and human gates.

It is a **navigation and reproduction surface**, not an authority above executable CI.

```text
this runbook != semantic truth
this runbook != strategy authority
this runbook != merge/release authorization
local reproduction != hosted cross-platform CI proof
```

When this runbook and checked-in workflow code disagree, the workflow/code is authority for what the repository currently executes. Reconcile this document rather than using prose to override executable behavior.

Current CI authorities:

```text
.github/workflows/validation.yml          Product Validation
.github/workflows/lab-validation.yml      retained Lab Validation
.github/workflows/release-candidate.yml   Release Candidate Distribution
```

Current strategic-state integrity authority:

```text
scripts/validate-strategic-state.py
```

Historical milestone runbooks are retained as milestone evidence only. They are not current operational authorities.

## 2. Development setup

From a clean source checkout:

```bash
python -m venv .venv
# activate the environment
python -m pip install --upgrade pip
python -m pip install -e . pytest pytest-subtests
sensemaking-skills --version
```

Current package version:

```text
0.3.0
```

For retained lab work, install lab dependencies separately:

```bash
python -m pip install -e . --no-deps
python -m pip install "click>=8.1.0" "PyYAML>=6.0,<7.0" -r requirements-lab.txt
```

Do not add source-only lab dependencies to the shipped core merely to simplify local testing.

## 3. Product Validation

`.github/workflows/validation.yml` is the exact executable authority. The commands below are the closest documented local reproduction of its current categories.

### 3.1 Product/lab boundary

```bash
python scripts/validate-product-boundary.py
```

This protects the shipped-product/lab boundary, release-version authority, installed-wheel ownership, and repository worktree/gitlink constraints.

### 3.2 Campaign product suite

Run on Python 3.11 and 3.12 when reproducing the CI matrix:

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

### 3.3 Installed-core-wheel regressions

```bash
python -m pytest tests/campaign_validation/test_installed_wheel_smoke.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p9.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p10.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p11.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_setup_skills.py -q -rs
```

Installed-wheel tests belong to Product Validation, not the retained research lab.

### 3.4 Repository and Skill contracts

Run the current deterministic repository-level gates:

```bash
python scripts/validate-repo.py
python scripts/validate-strategic-state.py --repo-root .

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

Then run the current stable repository assertion set:

```bash
python -m pytest \
  tests/test_repo_probes.py \
  tests/test_probe_report_cli.py \
  tests/test_probe_relationships.py \
  tests/test_skill_distribution_probe.py \
  tests/test_gate_relationship_findings.py \
  tests/test_path_drift.py \
  tests/test_cli.py \
  tests/test_semantic_reasoning_profile.py \
  tests/test_skill_registry_liveness.py \
  tests/test_strategic_state_validation.py \
  tests/test_semantic_substrate.py \
  tests/test_semantic_reference_audit.py \
  tests/test_semantic_conformance.py \
  tests/test_semantic_cli.py \
  -q
```

Important claim limits:

```text
strategic-state validator PASS != strategy correct
semantic conformance PASS != Skill should run
reference audit PASS != semantic truth
repository tests PASS != native-harness qualification
```

### 3.5 Filesystem-security contracts

Linux/macOS-style local reproduction:

```bash
python -m pytest tests/test_gate_a_authorization_consumer.py -q
python -m pytest tests/test_gate_a_path_canonicalization.py -q
python -m pytest tests/test_gate_a_physical_containment.py -q -rs
```

The same contract family runs on a Windows CI runner. A local Unix run does not establish the hosted Windows result.

### 3.6 Clean-tree rule

After validation:

```bash
git status --porcelain
```

Expected: validation did not create tracked repository changes.

## 4. Strategic Repository Evolution integrity

`STATUS.md` is the current Level-3 operational projection. `docs/product-strategy.md` remains Level-4 product-thesis authority.

Validate only the mechanically ratified representation contract with:

```bash
python scripts/validate-strategic-state.py --repo-root .
```

The validator checks required Level-3 anchors, canonical authority pointers, thesis-review marker shape, and duplicate Strategic Frontier identities.

It does **not** determine:

- whether the strategy is good;
- whether the active frontier is highest leverage;
- whether a strategic disposition is semantically correct;
- whether a PR/issue is current in GitHub;
- what repository responsibility should be selected next.

Outer Loop v0 remains agent-controlled. See:

```text
docs/strategic-outer-loop.md
docs/strategic-state-contract.md
docs/product-thesis-revision.md
```

## 5. Campaign operating flow

### 5.1 Initialize a target-bound Campaign

The Campaign workspace must live outside its target repository.

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaigns/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Determine and execute the next warranted repository step" \
  --target-repo /path/to/target-repository
```

Then inspect/validate reconstruction:

```bash
sensemaking-skills campaign status --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/campaigns/CMP-0001
```

Target inspection records mechanical identity/current bytes. It does not diagnose the repository or select a responsibility.

### 5.2 Admit validated evidence

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/campaigns/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

Admission/validator success does not itself authorize a Campaign transition.

### 5.3 Inspect observability and semantic-reference state

```bash
sensemaking-skills campaign inspect --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign semantic-state --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign explain --workspace /path/to/campaigns/CMP-0001 --ref <exact-ref>
sensemaking-skills campaign graph --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume-context --workspace /path/to/campaigns/CMP-0001
```

B7 reference audit distinguishes occurrence from mechanical resolution.

```text
resolved != current
not_addressable != invalid
reference audit PASS != semantic support
```

### 5.4 Record semantic decisions explicitly

Use the Campaign lifecycle interfaces only after the active agent/human has made the semantic decision:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

Target drift, validator PASS, or capability availability never creates a semantic transition automatically.

### 5.5 Handoff and resume

After the latest durable transition and while the target is stable:

```bash
sensemaking-skills campaign handoff --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/campaigns/CMP-0001
```

For deeper Campaign contracts see:

```text
docs/sensemaking-campaign.md
docs/campaign-target-snapshot.md
docs/campaign-observability-and-portability.md
docs/campaign-handoff-resume.md
```

## 6. Retained Lab Validation

`.github/workflows/lab-validation.yml` owns source-only research/lab claims and is path-filtered for PR/push events.

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

If a claim explicitly depends on Lab Validation and path filters did not trigger it, invoke the workflow explicitly against the intended ref before making the claim.

Lab qualification does not substitute for native-harness product evidence.

## 7. Release Candidate Distribution

`.github/workflows/release-candidate.yml` is the exact-head distribution authority for v0.3.0.

### 7.1 Local baseline contracts

```bash
python scripts/validate-product-boundary.py
python -m pytest \
  tests/campaign_validation/test_release_candidate_contract.py \
  tests/campaign_validation/test_campaign_schema_evolution.py \
  tests/integration/test_external_golden_path_qualification.py \
  -q
```

### 7.2 Build and metadata checks

```bash
python -m pip install -e . pytest pytest-subtests build twine
rm -rf build dist
python -m build
python -m twine check dist/*
```

Current v0.3.0 artifact identities:

```text
sensemaking_skills-0.3.0-py3-none-any.whl
sensemaking_skills-0.3.0.tar.gz
```

The hosted workflow additionally proves fresh installation from both wheel and sdist and uploads the exact-head candidate artifacts.

### 7.3 Exact-head rule

Qualification applies only to the exact candidate head that passed it.

If the head moves:

1. treat older green runs as historical evidence;
2. rerun qualification against the new exact head;
3. do not borrow stale CI success for merge or publication claims.

## 8. Human/owner gates

Deterministic validation cannot decide whether work is strategically warranted.

Owner/human authority remains required where the repository contract reserves it, including:

- major Level-4 product-thesis changes;
- expansion of product/public claim ceilings;
- explicit merge/release/publication decisions when not already delegated;
- acceptance of external/subjective production QA;
- real credentials or destructive/live external actions;
- resumption of experiments when owner direction currently defers them.

`validator passed != authorization`.

## 9. Native-harness / empirical evidence ceiling

Repository qualification, Campaign admission, Domain Pack membership, installation, and connector-side reasoning do not prove native harness discovery/invocation or product-value superiority.

Current distinction:

```text
repository qualified
!= native-harness qualified
!= portability qualified
!= promoted / product-value established
```

Real-harness PASS claims require the canonical real external attempt protocol and its required provenance. Synthetic fixtures establish verifier behavior only.

Current owner direction continues to defer new empirical experiments. This runbook does not reopen them.

## 10. Historical milestone runbooks

The following documents are retained as historical milestone records, not current operational authorities:

```text
docs/milestone-runbook.md
docs/post-milestone-handoff-runbook.md
```

They preserve package ledgers, exact-head evidence, and milestone-specific interpretation. Current operators should begin here instead:

```text
docs/operations-runbook.md
```

Git history preserves the former detailed command reproductions when historical reconstruction requires them.

## 11. Normal repository-development entry sequence

For consequential repository work:

```text
1. docs/product-strategy.md          — Level 4: what/why
2. STATUS.md                         — Level 3: current state/frontier
3. relevant ADRs/contracts           — ratified boundaries
4. active Campaign/work package      — Level 2 responsibility
5. branch/code/tests                 — Level 1 execution
6. this operations runbook           — current mechanical qualification path
```

After integration, reconcile Level-3 state and reassess. Do not automatically select another package merely because one appears next in an old phase or milestone document.
