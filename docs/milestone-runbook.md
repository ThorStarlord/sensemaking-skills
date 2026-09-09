# Milestone Operations Runbook — CI Authority, v0.3 Release, and Target Snapshots

**Status:** post-milestone operational source of truth  
**Applies to:** Features 1–3 merged by PRs #298, #299, and #300  
**Product version:** 0.3.0  
**Feature-3 product baseline:** `24a88bf6311122dae1257999f5a7379cb0b095d5`  
**Audience:** maintainers, coding agents, and human release/qualification operators

This runbook consolidates the operational consequences of the completed three-feature milestone:

1. **CI Authority Reconciliation** — product, lab, version, and worktree boundaries are mechanically explicit.
2. **v0.3 Release Baseline Rebuild** — the installed wheel/sdist carry the Campaign product, Skill trees, and canonical validator runtime and are qualified on the exact PR head.
3. **Durable Target Snapshot Binding** — a Campaign can prove which exact Git repository identity and working-tree state its durable state concerns.

The architecture remains agent-native. Deterministic machinery preserves representation, provenance, validation, integrity, and reconstruction; it does not decide what evidence means or what work should happen next.

---

## 1. Milestone ledger

| Feature | PR | Operational result |
|---|---:|---|
| CI Authority Reconciliation | #298 | `pyproject.toml` is the sole literal version authority; Product Validation and Lab Validation have distinct claim boundaries; installed-wheel tests belong to product validation; stray `.claude/worktrees/*` gitlinks are rejected/removed. |
| v0.3 Release Baseline Rebuild | #299 | Version 0.3.0; installed canonical validator runtime; wheel + sdist release-candidate qualification; `twine check`; fresh-install proofs; stale PR #294 superseded rather than reused as release authority. |
| Durable Target Snapshot Binding | #300 | First-class target repository snapshot in Campaign state; transition source/destination target digests; live drift detection; target-aware lineage and handoff/resume; historical target-unbound schema-v2 records remain honest and compatible. |

The Feature-3 merge commit is the product-code milestone boundary. Documentation-only follow-up commits may move `main` without changing that product baseline.

---

## 2. Core invariants

Keep these inequalities explicit when operating or extending the system:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
lineage != semantic warrant
handoff != semantic recommendation
Skill copied to discovery root != harness observed or invoked Skill
external verifier PASS != semantic truth

target snapshot bound != repository correct
repository changed != repair succeeded
target identity != warranted responsibility
target drift != automatic transition
target provenance != capability selection or execution authority
```

The Campaign Controller is not a semantic router.

---

## 3. Development setup

From a clean source checkout:

```bash
python -m venv .venv
# activate the environment
python -m pip install --upgrade pip
python -m pip install -e . pytest pytest-subtests
sensemaking-skills --version
```

Expected product version:

```text
0.3.0
```

For retained research/lab work, install lab dependencies separately:

```bash
python -m pip install -e . --no-deps
python -m pip install "click>=8.1.0" "PyYAML>=6.0,<7.0" -r requirements-lab.txt
```

Do not add retained-lab dependencies to the shipped core merely to make source-only tests convenient.

---

## 4. Target-bound Campaign operating flow

### 4.1 Initialize outside the target repository

A Campaign workspace must live outside its target repository.

```bash
sensemaking-skills campaign init \
  --workspace /path/to/campaigns/CMP-0001 \
  --campaign-id CMP-0001 \
  --mission "Determine and execute the next warranted repository step" \
  --target-repo /path/to/target-repository
```

With `--target-repo`, initialization performs **mechanical target inspection only**. It records repository identity, Git HEAD/tree, and a deterministic working-tree digest. It does not diagnose the repository, infer uncertainty, choose responsibility, select a capability, or grant authority.

Immediately verify reconstruction:

```bash
sensemaking-skills campaign status --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign validate --workspace /path/to/campaigns/CMP-0001
```

### 4.2 Admit validated evidence

Normal installed use relies on the packaged canonical validator runtime:

```bash
sensemaking-skills campaign ingest \
  --workspace /path/to/campaigns/CMP-0001 \
  --artifact /path/to/repository_sensemaking_brief.md
```

`--framework-root` is an explicit source-development/compatibility override. If a supplied override is invalid, the command fails closed; it does not silently fall back to another validator tree.

### 4.3 Record semantic decisions explicitly

Inspect the exact decision interfaces before authoring a transition:

```bash
sensemaking-skills campaign advance --help
sensemaking-skills campaign defer --help
sensemaking-skills campaign close --help
```

The active agent/human authors the decision. Validator success, target changes, or capability availability never create a semantic transition automatically.

### 4.4 Work may change the repository

A target snapshot is **not globally immutable**. Bounded implementation work may legitimately change the target repository between Campaign decisions.

The expected lifecycle is:

```text
current durable target snapshot
→ bounded repository work
→ live target changes
→ explicit agent-authored Campaign decision
→ deterministic destination snapshot capture
→ transition stores source target digest + destination target digest
```

Do not manually edit `campaign-state.yaml`, transition YAML, trace history, or target snapshot fields to make drift disappear.

If ordinary reconstruction detects unrecorded target drift, treat that as a provenance/precondition signal. Determine why the repository changed, then use the normal explicit lifecycle decision path when the Campaign is semantically ready to transition. Drift itself does not justify the transition.

### 4.5 Inspect target/evidence lineage

```bash
sensemaking-skills campaign lineage --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign history --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign reconciliation --workspace /path/to/campaigns/CMP-0001
```

Lineage exposes transition source/destination target snapshot digests and evidence consumption. Neither one proves the repository change was correct.

### 4.6 Handoff only from current durable state

After the latest lifecycle transition and while the target is stable:

```bash
sensemaking-skills campaign handoff --workspace /path/to/campaigns/CMP-0001
sensemaking-skills campaign resume --workspace /path/to/campaigns/CMP-0001
```

Fresh-context resume verifies the handoff reconstruction binding and, for target-bound Campaigns, the current live target snapshot. A changed/unavailable/wrong repository must fail closed rather than silently resuming against different bytes.

Historical target-unbound Campaigns remain target-unbound. Do not retroactively invent repository identity by editing old state.

For the full target contract, see `docs/campaign-target-snapshot.md`.

---

## 5. Product Validation runbook

`.github/workflows/validation.yml` is the authority for shipped-product validation. Run the following from the repository root for the closest local Linux equivalent.

### 5.1 Product/lab boundary

```bash
python scripts/validate-product-boundary.py
```

This protects the release-version authority, installed-wheel ownership, retained-lab exclusion, and worktree/gitlink boundary.

### 5.2 Campaign product suite

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

Run this on supported Python 3.11 and 3.12 when reproducing the CI matrix.

### 5.3 Installed-core-wheel regressions

```bash
python -m pytest tests/campaign_validation/test_installed_wheel_smoke.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p9.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p10.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_p11.py -q -rs
python -m pytest tests/campaign_validation/test_installed_wheel_setup_skills.py -q -rs
```

These tests belong to **Product Validation**, not the retained lab.

### 5.4 Repository and Skill contracts

```bash
python scripts/validate-repo.py
python scripts/probe-repo.py --repo-root . --output /tmp/probe-report.yaml
python scripts/validate-probe-report.py /tmp/probe-report.yaml --repo-root .
python scripts/gate_relationship_findings.py --report /tmp/probe-report.yaml

python -m pytest \
  tests/test_repo_probes.py \
  tests/test_probe_report_cli.py \
  tests/test_probe_relationships.py \
  tests/test_skill_distribution_probe.py \
  tests/test_gate_relationship_findings.py \
  tests/test_path_drift.py \
  tests/test_cli.py \
  -q
```

Use an OS-appropriate temporary path instead of `/tmp` on Windows.

### 5.5 Filesystem-security contracts

Linux/macOS-style local run:

```bash
python -m pytest tests/test_gate_a_authorization_consumer.py -q
python -m pytest tests/test_gate_a_path_canonicalization.py -q
python -m pytest tests/test_gate_a_physical_containment.py -q -rs
```

The same contracts are also authoritative on the Windows CI runner. Cross-platform containment claims require the CI matrix, not only a local Unix run.

### 5.6 Clean-tree check

After validation:

```bash
git status --porcelain
```

Expected: no tracked changes created by validation.

---

## 6. Retained Lab Validation runbook

`.github/workflows/lab-validation.yml` owns source-only research/lab claims. It deliberately ignores `test_installed_wheel_*.py` because those are product tests.

On Linux/macOS:

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

Windows confinement proofs:

```bash
python -m pytest tests/campaign_accounting/test_artifact_path_confinement.py -q
python -m pytest tests/campaign_accounting/test_artifact_path_confinement_windows.py -q
```

Lab tests must not create operative experiment state or dirty tracked repository files.

---

## 7. Release Candidate Distribution runbook

`.github/workflows/release-candidate.yml` is the exact-head distribution authority for v0.3.0.

### 7.1 Install release tooling

```bash
python -m pip install -e . pytest pytest-subtests build twine
```

### 7.2 Run release contracts

```bash
python scripts/validate-product-boundary.py
python -m pytest \
  tests/campaign_validation/test_release_candidate_contract.py \
  tests/campaign_validation/test_campaign_schema_evolution.py \
  tests/integration/test_external_golden_path_qualification.py \
  -q
```

### 7.3 Build and validate distributions

```bash
rm -rf build dist
python -m build
python -m twine check dist/*
```

For v0.3.0 the candidate identities must be exactly:

```text
sensemaking_skills-0.3.0-py3-none-any.whl
sensemaking_skills-0.3.0.tar.gz
```

Record distribution digests:

```bash
sha256sum dist/*
```

The CI workflow additionally creates fresh environments from both the wheel and sdist and proves the Campaign CLI, schema-v2 contract, packaged Skill trees, packaged validator runtime, and exclusion of source-only lab packages.

### 7.4 Exact-head rule

A release qualification claim applies only to the exact candidate head that passed it.

If the PR head moves after qualification:

1. treat the old run as historical evidence only;
2. rerun qualification on the new exact head;
3. do not merge or publish by borrowing a green result from stale bytes.

This is why the obsolete PR #294 was superseded rather than reused as v0.3 release authority.

---

## 8. Human-only operational gates

CI and deterministic tooling cannot replace the following owner decisions.

### 8.1 Merge and release ownership

- A human/authorized repository operator decides whether a qualified PR should merge.
- Tagging/publication is a separate owner action after the intended exact-head qualification is accepted.
- The publishing workflow runs `twine check` before upload, but that does not decide whether publication is warranted.

### 8.2 Retained-lab qualification when path filters do not trigger it

Product Validation and Release Candidate Distribution run for PRs to `main`. Lab Validation is path-filtered.

If a release or milestone claim explicitly depends on retained-lab qualification and the lab workflow did not auto-trigger, a human operator must invoke **Lab Validation** manually with `workflow_dispatch` against the intended ref before making that claim.

### 8.3 Real-harness evidence

A synthetic external-qualification fixture proves the verifier contract only.

A real-harness PASS claim requires a real frozen external attempt with the required evidence package. Preserve the distinction:

```text
fixture verifier PASS != real harness PASS
```

Installing/copying Skills also does not prove the harness observed or natively invoked them. Real-harness qualification requires separate invocation evidence.

### 8.4 Harness setup and `--force`

Harness selection is explicit:

```bash
sensemaking-skills setup-skills --target generic --scope user
sensemaking-skills setup-skills --target claude --scope user
sensemaking-skills setup-skills --target codex --scope user
sensemaking-skills setup-skills --target opencode --scope user
```

Project scope requires an explicit project root, for example:

```bash
sensemaking-skills setup-skills \
  --target claude \
  --scope project \
  --project-root /path/to/repository
```

Divergent installed Skill trees are preserved by default. Use `--force` only as an explicit operator decision after inspecting the drift.

### 8.5 Worktrees

`.claude/worktrees/` is local-only and ignored. Do not commit nested worktrees or mode-160000 gitlinks as repository content. Run:

```bash
python scripts/validate-product-boundary.py
```

before qualification to catch violations of this boundary.

---

## 9. Failure interpretation

### `TARGET_SNAPSHOT_DRIFT`

The live target bytes no longer match the durable Campaign snapshot. Investigate the change. Do not hand-edit Campaign state to suppress the diagnostic.

### `TARGET_REPOSITORY_IDENTITY_MISMATCH`

The Campaign is resolving against a different repository identity. Restore/access the intended repository; do not reinterpret the Campaign as belonging to the new repository.

### `TARGET_REPOSITORY_UNAVAILABLE`

Fresh-context reconstruction cannot access the target locator. Re-establish access to the intended target before relying on target-bound reconstruction.

### artifact validator override failure

If `campaign ingest --framework-root ...` fails, fix the explicit override or omit it to use the packaged canonical validator runtime. Do not create fallback search logic.

### Product Validation failure

Treat it as a shipped-product/repository-contract problem. Do not make Lab Validation green and claim that substitutes for product qualification.

### Lab Validation failure

Treat it as a retained research/source-lab problem. Do not add lab packages/dependencies to the wheel merely to erase the boundary.

### Release Candidate Distribution failure

Do not publish. Fix the exact candidate, rerun the distribution workflow, and qualify the new exact head.

---

## 10. Version and packaging authority

The literal release version lives only in:

```text
pyproject.toml -> [project].version
```

Runtime `sensemaking_skills.__version__` derives from installed distribution metadata. `setup.py` is a build hook, not version authority. `package.json` is private repository tooling metadata and is not the Python release-version authority.

The shipped wheel contains the Campaign product/runtime surface. These remain source-only retained lab packages:

```text
sensemaking_skills.campaign_validation*
sensemaking_skills.campaign_accounting*
sensemaking_skills.exploratory_authorization*
sensemaking_skills.exploratory_execution*
```

---

## 11. Canonical references

- `README.md` — product entry point and quick start.
- `STATUS.md` — current milestone/product state.
- `docs/sensemaking-campaign.md` — Campaign product model.
- `docs/campaign-target-snapshot.md` — durable target provenance contract.
- `docs/campaign-cli.md` — base Campaign CLI semantics.
- `docs/campaign-schema-evolution.md` — schema compatibility and append-only migration qualification.
- `docs/product-lab-boundary.md` — shipped product vs retained lab.
- `docs/artifact-ingestion.md` — canonical artifact admission and installed validator runtime.
- `docs/external-golden-path-verifier.md` — real-harness evidence verifier.
- `docs/harness-adapters.md` — deterministic harness setup roots.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release-candidate distribution authority.
- `.github/workflows/publish.yml` — tagged publication mechanics.

When this runbook and a workflow disagree about exact test commands, the checked-in workflow is the executable authority; reconcile the documentation rather than silently diverging.
