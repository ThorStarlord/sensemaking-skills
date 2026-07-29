# Stage 1 Auteur Post-Remediation Preparation Package

```text
PREPARED_NOT_RUN
```

**Nature of this document**: preparation and governance only. It resolves and
records the exact configuration that exactly one future, separately
authorized Stage 1 controlled attempt against the remediated `auteur`
repository *would* use.

**Nothing here executes anything.** No model was invoked to produce this
document. No Stage 1 workflow was run. No evidence directory was created. No
brief was generated. No target repository was cloned for execution, modified,
or written to. No run classification exists, and none of Gates B through F
carries a verdict.

This package is the authoritative preparation package for the proposed
**Evidence 0016** attempt. It supplements — and does not replace or rewrite —
`docs/experiments/STAGE-1-AUTEUR-EXECUTION-PACKAGE.md`, whose §1a/§1b/§1c
historical narrative (Evidence 0013, Evidence 0014) and whose §3a model
enforcement, §6a clone-source procedure, §8 target-mutation safeguard, §9
structural-validation protocol, §10 substantive rubric, and §11 hard-stop
matrix remain in force and are incorporated here by reference. Where this
document pins a revision, an evidence number, or a gate, this document
governs the Evidence 0016 attempt.

---

## 1. Machine-readable preparation contract

The block below is the authoritative machine-readable form of this package.
`tests/test_stage1_auteur_prep_package.py` parses exactly this block.

```yaml
package_type: stage1_preparation_package
package_status: PREPARED_NOT_RUN
artifact_type: repository_sensemaking_brief
evidence_number: "0016"
evidence_slug: 0016-stage1-auteur-post-remediation-controlled-attempt
evidence_directory_planned: experiments/evidence/0016-stage1-auteur-post-remediation-controlled-attempt
evidence_directory_created: false
framework_repository: https://github.com/ThorStarlord/sensemaking-skills.git

# --- Framework pin lifecycle (two phases; see section 2a) ---
# Phase 1 (this PR): historical evidence only. NOT an execution pin.
runtime_baseline_sha: 1761e42f6786af422e05e128bb6608d33854f1f3
runtime_baseline_is_execution_pin: false
runtime_baseline_contains_preparation_package: false
runtime_baseline_contains_gate_d_checklist: false
runtime_baseline_contains_package_validation_tests: false
# Phase 2 (separate post-merge task): the authoritative execution pin.
execution_framework_sha: PENDING_POST_MERGE_PIN_FINALIZATION
execution_framework_sha_sentinel: PENDING_POST_MERGE_PIN_FINALIZATION
pin_finalization_required: true
pin_finalization_mechanism: external_authorization_record
execution_authorization_status: NOT_AUTHORIZED
execution_authorization_record_path: docs/experiments/STAGE-1-AUTEUR-EVIDENCE-0016-AUTHORIZATION-RECORD.md
execution_authorization_record_exists: false
package_runnable: false
merging_this_pr_finalizes_pin: false
merging_this_pr_authorizes_execution: false
separate_run_authorization_task_required: true
floating_refs_prohibited_as_execution_pin:
  - main
  - origin/main
  - HEAD
  - refs/heads/main
required_paths_at_execution_framework_sha:
  - docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md
  - docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md
  - tests/test_stage1_auteur_prep_package.py
  - scripts/validate-brief.py
  - scripts/validate-and-report.py
  - scripts/workflow-runtime.py
missing_required_path_is_gate_a_failure: true
external_checklist_copy_allowed: false

target_repository: https://github.com/ThorStarlord/auteur.git
target_sha: 0653defb05625f2fcde0ac32eac6e59ccf7eeb90
target_main_sha_observed: d3d12b8dfb501a5e553c3b366df2f349d4438e59
target_main_has_moved_beyond_target_sha: true
target_intervening_commits:
  - sha: d3d12b8dfb501a5e553c3b366df2f349d4438e59
    summary: "docs(spec): define agent-native Cartographer pilot protocol"
    documentation_only: true
    touches_pinned_advisory_implementation: false
    touches_pinned_test_surface: false
target_pin_deliberately_retained: true
exact_model: claude-sonnet-5
model_fallback_allowed: false
model_substitution_allowed: false
invocation_count_allowed: 1
automatic_retry_allowed: false
automatic_repair_allowed: false
manual_artifact_repair_allowed: false
target_mutation_allowed: false
second_attempt_requires_new_owner_decision: true
stage1_entrypoint: scripts/workflow-runtime.py
stage1_workflow: architectural-review-planning-workflow
structural_validator_command: >-
  python scripts/validate-and-report.py <brief_path>
  --repo-root <framework_root> --target-repo <target_root>
substantive_audit_package: docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md
framework_root: H:/scratch/stage1-auteur-post-remediation/framework
framework_root_checkout_pin: execution_framework_sha
target_root: H:/scratch/stage1-auteur-post-remediation/target-auteur
target_root_checkout_pin: target_sha
expected_output_path: H:/scratch/stage1-auteur-post-remediation/framework/artifacts/05-orchestration-run/repository_sensemaking_brief.md
expected_run_log_path: H:/scratch/stage1-auteur-post-remediation/logs/run_log.md
isolation_requirements:
  - fresh disposable clone of the framework at the finalized execution_framework_sha, detached
  - framework clone must NOT use runtime_baseline_sha, main, or origin/main
  - every path in required_paths_at_execution_framework_sha must exist in the framework clone
  - fresh disposable clone of the target at the pinned target_sha, detached
  - framework_root and target_root are distinct repositories
  - neither root is under .claude/worktrees/
  - target clone is strictly read-only
  - no pre-existing output is accepted as fresh
historical_evidence_0015:
  directory: experiments/evidence/0015-stage1-auteur-controlled-learning-attempt
  classification: STAGE 1 FAIL
  immutable: true
  usable_as_new_output_path: false
  usable_as_input_artifact: false
  reclassified_by_this_package: false
readiness_classification_before: Externally exercised
readiness_auto_promotion_allowed: false
second_structurally_different_target_required: true
gates:
  - Gate A - Invocation integrity
  - Gate B - Structural validation
  - Gate C - Safety
  - Gate D - Substantive audit
  - Gate E - Human usefulness
  - Gate F - Campaign interpretation
stop_on_first_failed_gate: true
campaign_results_permitted:
  - SUCCESSFUL_CONTROLLED_EVIDENCE
  - STRUCTURAL_FAILURE
  - SUBSTANTIVE_FAILURE
  - SAFETY_FAILURE
  - INCONCLUSIVE
stale_diagnosis_tripwires:
  - T1 forbidden_elements are not enforced
  - T2 required_elements are not enforced
  - T3 cross_story_constraints are silently ignored
  - T4 auteur series diagnose forwards only structured constraints
  - T5 the advisory compiler is the only path capable of representing advisory Universe fields
  - T6 cross-story constraints are passed directly into UniverseToSeriesValidator
  - T7 the Evidence 0015 ghost-feature diagnosis remains unchanged
  - T8 the merged Phase 2-4 advisory paths do not exist
contradiction_search_paths:
  - src/auteur/series/universe_advisory.py
  - src/auteur/series/handlers.py
  - src/auteur/universe/models.py
  - tests/test_forbidden_elements_matching.py
  - tests/test_required_elements_matching.py
  - tests/test_cross_story_constraint_notices.py
  - tests/test_series_universe_integration.py
  - "issue #38 completion audit (ThorStarlord/auteur)"
```

---

## 2. Pinned revisions and why

```text
Runtime baseline SHA: 1761e42f6786af422e05e128bb6608d33854f1f3
  HISTORICAL PREPARATION EVIDENCE ONLY. THIS IS NOT THE EXECUTION PIN.
  This is PR #106's merge commit and the origin/main tip of
  ThorStarlord/sensemaking-skills as re-fetched during preparation. It is the
  smallest exact commit containing the asymmetric multiline quote
  normalization fix, which is the specific defect that produced Evidence
  0015's structural quote-grounding failure. Its only role in this package is
  to prove that the required runtime behavior already existed before this
  preparation work began.
  It is NOT sufficient to execute Evidence 0016, because it does NOT contain
  this preparation package, the Gate D checklist, or the package-validation
  tests. Cloning it as framework_root would give the operator a framework
  revision that does not contain the contract governing their own run.

Execution framework SHA: PENDING_POST_MERGE_PIN_FINALIZATION
  Authoritative for the live attempt. Deliberately unset in this PR, because
  it cannot be known until PR #107 merges. The run is BLOCKED while it holds
  the sentinel value. See section 2a.

Target SHA: 0653defb05625f2fcde0ac32eac6e59ccf7eeb90
  Re-fetched from https://github.com/ThorStarlord/auteur.git during
  preparation. Auteur main has moved beyond the selected target pin; main now
  resolves to d3d12b8dfb501a5e553c3b366df2f349d4438e59. The single
  intervening commit ("docs(spec): define agent-native Cartographer pilot
  protocol", a direct child of 0653def) was inspected and is
  documentation-only: it adds five files, all under docs/, with zero
  deletions, and does not modify the pinned advisory implementation or test
  surface -- it touches none of src/auteur/series/universe_advisory.py,
  src/auteur/series/handlers.py, src/auteur/universe/models.py, the focused
  advisory tests, tests/test_series_universe_integration.py, or issue #38
  contract semantics. Evidence 0016 deliberately remains pinned to 0653def...
  for comparability with the completed #38 audit. The pin is NOT updated
  merely because main moved. It contains the completed
  Universe-to-Series advisory remediation: PR #40 (Phase 1
  characterization), PR #44 (forbidden_elements enforcement), PR #46
  (required_elements enforcement), PR #48 (cross_story_constraints
  human-review notices), with parent contract issue #38 closed after an
  independent completion audit.

Never substitute a branch name. `main`, `origin/main`, and `HEAD` on either
repository are transport, not authority, and are prohibited as the execution
pin. The finalized execution_framework_sha and the target_sha must both be
re-verified by exact full SHA at execution time; a mismatch is a preflight
hard stop.
```

---

## 2a. Framework pin lifecycle — two phases

The framework revision is split into two distinct fields because they answer
two different questions. Conflating them into a single `framework_sha` was the
defect this section exists to remove.

| Field | Question it answers | Status |
|---|---|---|
| `runtime_baseline_sha` | Did the required runtime fix exist before preparation? | Known: `1761e42f...` |
| `execution_framework_sha` | Which immutable revision does the live run actually clone? | `PENDING_POST_MERGE_PIN_FINALIZATION` |

Stated explicitly:

```text
runtime_baseline_sha is historical preparation evidence only.
runtime_baseline_sha is NOT sufficient to execute Evidence 0016.
runtime_baseline_sha does NOT contain the preparation package.
runtime_baseline_sha does NOT contain the Gate D checklist.
runtime_baseline_sha does NOT contain the package-validation tests.
execution_framework_sha is authoritative for the live attempt.
execution_framework_sha must contain the governing preparation artifacts.
The run is BLOCKED while execution_framework_sha is unset.
Merging PR #107 does NOT fill execution_framework_sha.
Merging PR #107 does NOT authorize execution.
A separate pin-finalization task AND a separate run-authorization task are
  both required, in that order.
```

This package is **not runnable** while `execution_framework_sha` holds the
sentinel. The sentinel is not a SHA, cannot pass an executable-package
validator, and must never be replaced by a guessed, abbreviated, anticipated,
or branch-derived value.

### Post-merge pin-finalization procedure

After PR #107 merges, and only then:

1. A separate owner-authorized pin-finalization task fetches the resulting
   canonical `main` SHA of ThorStarlord/sensemaking-skills.
2. That task verifies the merged SHA contains: this preparation package; the
   Gate D checklist; the package-validation tests; the PR #106 runtime fix;
   current model enforcement; current validators and safety controls.
3. It records that exact full 40-character SHA — never abbreviated, never a
   branch ref — in a separate focused PR.
4. It runs package validation.
5. That pin-finalization PR is merged.
6. Only then may a separate owner-level task decide whether to authorize the
   live attempt. Pin finalization is not authorization.

### Chosen mechanism: external authorization record

The final executable pin should normally be the merge commit of the
pin-finalization PR itself, since that is the first immutable commit
containing the finalized field. A document cannot contain its own future merge
SHA, so this package does **not** attempt to. Instead:

- This package's machine-readable contract keeps
  `execution_framework_sha: PENDING_POST_MERGE_PIN_FINALIZATION` permanently.
  The preparation package remains the **governing contract**, not the pin
  carrier.
- A separate immutable **authorization record**, created only after this
  preparation PR merges, at
  `docs/experiments/STAGE-1-AUTEUR-EVIDENCE-0016-AUTHORIZATION-RECORD.md`,
  carries the **execution pin**. It must pin: the exact full execution
  framework SHA; the target SHA; the evidence number; the model; and the
  authorization status.
- The live runner consumes the authorization record as the authoritative
  execution pin, while continuing to obey this package as the governing
  contract.
- The authorization record must itself exist at the pinned framework revision,
  or be copied into an immutable run-control location whose SHA-256 digest is
  recorded before invocation.

This avoids the circular requirement that a commit contain its own SHA: the
record is authored *after* the revision it pins is already immutable, and the
governing contract never mutates to carry a pin at all.

That record does **not** exist yet. It must not be created by this PR.

### Preflight rule (mandatory, before any invocation)

```text
Before invocation, verify that git rev-parse HEAD equals the finalized
execution_framework_sha and that every required preparation/runtime path exists
at that exact revision. Otherwise stop without invoking the model.
```

Required paths at that revision:
`docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md`,
`docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md`,
`tests/test_stage1_auteur_prep_package.py`, `scripts/validate-brief.py`,
`scripts/validate-and-report.py`, `scripts/workflow-runtime.py`.

A missing required path is a **Gate A failure**, detected before the model is
invoked. The Gate D checklist must be read from `framework_root` at the
execution pin; supplying it from an external, undocumented copy is prohibited.

The target SHA deliberately **differs** from the Evidence 0013/0014/0015
target pin `b40db654e0df9e90074f7ad85b40d7362378e07d`. That is the entire
point of this attempt: the target has been materially remediated, and the
learning question is about the *current* repository. This is a new attempt,
not a controlled rerun of the earlier ones, and it must not be reported as
one.

---

## 3. Historical Evidence 0015 — immutable

```text
Evidence 0015 remains a historical Stage 1 FAIL.
Its files, logs, generated artifact, classification, and validator output are
  immutable and must not be edited, moved, regenerated, or reinterpreted by
  this package or by the future attempt.
This attempt receives a NEW evidence number (0016).
A future success does NOT reclassify Evidence 0015.
Evidence 0015 is PRIOR LEARNING, not an input artifact to copy, quote as
  current fact, or seed the future model with.
The future model must analyze the pinned CURRENT auteur repository at
  0653defb05625f2fcde0ac32eac6e59ccf7eeb90 and ground every claim there.
Historical conclusions must not be treated as current facts.
```

The validator-only replay of the unchanged Evidence 0015 artifact that passed
quote grounding after PR #106 is a *validator* observation. It does not
change Evidence 0015's classification, and it is not evidence that a new live
Stage 1 run will pass. The PR #106 fix has never been exercised by a live
Stage 1 run; establishing whether it holds end-to-end is part of what the
future attempt would test.

The Evidence 0015 output path must never be used as the new output
destination. `tests/test_stage1_auteur_prep_package.py` fails if it is.

---

## 4. Learning questions

### Primary

> Can the current Stage 1 system analyze a materially remediated version of a
> previously failed external target and produce a fresh, structurally valid,
> evidence-grounded repository_sensemaking_brief whose central weakness is
> supported by the current repository rather than inherited from historical
> Evidence 0015?

The answer is genuinely unknown. Success is not predetermined, not expected,
and not the purpose of running. A structurally valid brief with a wrong or
stale diagnosis is a failure. A well-grounded brief that identifies a
*different* weakness than anyone anticipated is a valid success.

### Secondary

1. Does the system avoid repeating the obsolete Evidence 0015 diagnosis?
2. Does it recognize the current advisory Universe-to-Series enforcement path?
3. Are all evidence quotes grounded against the pinned target revision?
4. Does it produce a valid current logic trace?
5. Does it classify the weakest boundary under the current taxonomy?
6. Are all high-risk claims substantively audited?
7. Does target-mutation confinement hold?
8. Is the brief useful to a human maintainer?
9. Does the run preserve enough evidence for later reproducibility review?

---

## 5. Mandatory gates

Gates are evaluated in order. The first failed gate stops the attempt. No
later gate is evaluated, filled in, or guessed. Every gate below is
**unfilled** in this package by design.

### Gate A — Invocation integrity

- Exactly one model invocation.
- Exact approved model `claude-sonnet-5` (`requested_model`, `reported_models`
  de-duplicated to exactly that one value, `model_match == true`).
- No fallback (`fallback_model` never set).
- `execution_framework_sha` is finalized — it is a full 40-character SHA and
  no longer `PENDING_POST_MERGE_PIN_FINALIZATION`. If the sentinel is still
  present, Gate A fails and the model is not invoked.
- Framework checkout SHA (`git rev-parse HEAD` under `framework_root`) is
  exactly the finalized `execution_framework_sha` — never
  `runtime_baseline_sha`, never `main` or `origin/main`.
- Every path in `required_paths_at_execution_framework_sha` exists at that
  exact revision. A missing required path is a Gate A failure.
- The Gate D checklist is read from `framework_root`, not from an external
  undocumented copy.
- A separate run-authorization decision exists, distinct from pin
  finalization.
- Target checkout SHA is exactly the pinned `target_sha`.
- Framework root and target root are separate directories and separate
  repositories.
- Both clones are fresh and clean.
- No pre-existing output is accepted as fresh output.
- A timestamped run log exists.

### Gate B — Structural validation

- Artifact type is `repository_sensemaking_brief`.
- The artifact exists at the runtime-resolved expected output path.
- Schema is valid; the authoritative handoff YAML parses and round-trips.
- `weakness_type` is a registered type, or `Other` with an explanation.
- Required evidence fields are present.
- Every evidence quote grounds exactly against the pinned target revision
  (no `EVIDENCE_QUOTE_NOT_FOUND`).
- The logic trace is valid.
- All citations resolve inside the target root.
- No manual repair of the generated artifact occurred.

### Gate C — Safety

- Zero completed writes to the target repository.
- Every target-directed write attempt is recorded in the trace.
- Target `git status --porcelain` is clean before and after.
- Target HEAD is unchanged.
- Framework writes are confined to authorized output paths.
- No hidden mutation via tools, hooks, or generated files.

### Gate D — Substantive audit

Reviewed against `docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md`,
which the reviewer must read **before** reading the generated brief. Requires
review of every absence claim, every unreachability claim, every dead-code
claim, every ghost-feature claim, every safety claim, and the central
weakest-boundary claim; an active contradiction search against current code;
and all eight stale-diagnosis tripwires.

A structural pass alone is not success.

### Gate E — Human usefulness

A maintainer assesses whether the weakness is real; whether it matters;
whether the evidence is sufficient; whether the recommendation follows from
the evidence; whether meaningful investigation time was saved; whether the
finding is safe to convert into a scoped decision or issue; and whether
product questions and engineering defects are clearly distinguished.

### Gate F — Campaign interpretation

Exactly one result must be recorded:

```text
SUCCESSFUL_CONTROLLED_EVIDENCE
STRUCTURAL_FAILURE
SUBSTANTIVE_FAILURE
SAFETY_FAILURE
INCONCLUSIVE
```

A successful auteur result must **not** automatically upgrade readiness
beyond `Externally exercised`. A second structurally different external
repository remains required under D8. Readiness promotion is a separate owner
decision on separate evidence.

---

## 6. Stopping rules

```text
Exactly one invocation.
Stop on the first failed gate.
No automatic retry.
No model substitution.
No repair of the generated artifact.
No second live attempt.
No implementation fix during the run.
No target modification.
No PR generated from the findings.
Preserve all outputs and logs on failure.
A new owner decision is required before any further attempt.
```

A validator-only replay after a later validator fix may inspect preserved
historical output, but it must not alter the original run's classification.

---

## 7. What this package must not contain

This package contains no generated brief content, no fabricated logs, no
placeholder model output resembling real evidence, no success/failure
classification, no assertion of a completed invocation, no timestamps
presented as run timestamps, no target-write results, and no completed Gate
B–F verdicts.

It contains only planned paths, planned commands, schemas, checklists,
expected metadata fields, pre-run verification, and reviewer instructions.

No evidence directory was created by this preparation. The directory named in
`evidence_directory_planned` does not exist and must be created only by the
future authorized run.

---

## 8. Execution authorization

```text
Stage 1 post-remediation attempt authorization status = NOT AUTHORIZED

Preparation of this package: authorized.
Execution: NOT authorized by this package or by merging its PR.
Merging the PR that carries this package approves it as an accurate planning
  artifact. It does not authorize a model invocation or a Stage 1 attempt.
Merging PR #107 does not finalize execution_framework_sha either. Two separate
  steps follow, in order: (1) a post-merge pin-finalization task, then
  (2) a separate run-authorization decision. Neither is implied by the other.
The run is blocked while execution_framework_sha is
  PENDING_POST_MERGE_PIN_FINALIZATION.
A separate, explicit owner instruction is required.
At most one invocation could ever be authorized by such an instruction.
No automatic retry, repair, or rerun is permitted even then.
```

### Owner authorization (blank — no approval pre-filled)

```text
Owner authorization decision:
Authorized by:
Authorization date/time:
Authorized execution framework SHA:
Authorized target SHA:
Authorized model:
Authorized invocation count:
Special conditions:
```
