# Stage 1 Auteur Post-Remediation Preparation Package

```text
PREPARED_NOT_RUN
```

> **READ THIS FIRST — the authorization contract in this document is SPECIFIED
> and is enforced by the merged Gate A consumer, but no Stage 1 run is
> authorized.**
>
> ```text
> Authorization contract:     specified
> Authorization consumer:     implemented
> Runtime enforcement:        active at provider boundaries
> Owner approval:             not yet meaningful
> Package runnable:           false
> Evidence 0016 execution:    prohibited
> ```
>
> A Gate A authorization consumer now exists at
> `scripts/gate_a_authorization.py` and is wired into the real invocation path:
> it loads the authorization record, validates the owner approval, recomputes
> the digests, and blocks a model invocation on authorization state. That the
> mechanism exists authorizes nothing. This package remains non-runnable
> while the pending sentinels stand, and authorization cannot succeed without
> an owner approval binding the exact current record digest; the consumer
> therefore denies every request. See section 1a.

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
pin_finalization_mechanism: owner_approved_external_immutable_authorization_record
execution_authorization_status: NOT_AUTHORIZED
package_runnable: false

# --- Gate A runtime consumer status (see section 2i) ---
# THE DECISIVE FIELDS. As of the Gate A consumer PR, the authorization contract
# below is SPECIFIED and ENFORCED: `scripts/gate_a_authorization.py` reads it,
# and `scripts/skill_executor.py` requires the typed capability it mints before
# any provider SDK call. Implementing the consumer does NOT authorize a run --
# see `execution_authorization_status` and `package_runnable`, both unchanged.
gate_a_authorization_consumer_status: IMPLEMENTED
gate_a_authorization_consumer_required: true
gate_a_authorization_consumer_path: scripts/gate_a_authorization.py
gate_a_authorization_consumer_wired_to_stage1: true
gate_a_authorization_consumer_tests_status: IMPLEMENTED
gate_a_consumer_integration_point: scripts/skill_executor.py::ClaudeAgentSdkSkillExecutor
gate_a_runtime_enforcement_exists: true
contract_tests_are_runtime_enforcement_tests: false
authorization_without_consumer_is_valid: false
owner_approval_without_consumer_is_valid: false
filling_sentinels_without_consumer_makes_package_runnable: false
creating_authorization_files_without_consumer_makes_package_runnable: false
pr_107_implements_runtime_enforcement: false
pr_107_tests_are_contract_consistency_tests: true
# Proof required before any future authorization may take effect (section 2k).
consumer_merge_required_before_authorization: true
consumer_integration_proof_required: true
negative_zero_invocation_test_required: true
positive_single_invocation_test_required: true
consumer_deterministic_preflight_output_required: true
consumer_stable_failure_codes_required: true
consumer_must_gate_model_invocation_path: true
consumer_absence_blocks_preflight: true
consumer_not_wired_blocks_preflight: true
gate_d_requires_gate_a_consumer_pass: true
# Ordering constraints (section 2d). Violating any of these voids authorization.
consumer_implementation_precedes_authorization_record_creation: true
consumer_merge_precedes_owner_approval: true
execution_framework_sha_selected_after_consumer_merge: true
# "this pr" means the PR that most recently updated this document. PR #107
# added no consumer; the Gate A consumer PR did.
consumer_implementation_file_added_by_this_pr: true

# --- Authorization-record integrity (single mandatory mechanism; sections 2b-2h) ---
# Exactly one mechanism is permitted. There is no fork, no alternative, and no
# optional branch. See section 2b.
authorization_mechanism: owner_approved_external_immutable_authorization_record
authorization_mechanism_alternatives_allowed: false
authorization_mechanism_count: 1
authorization_record_may_exist_at_pinned_framework_revision: false
authorization_record_location_type: immutable_run_control_commit
run_control_directory: experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt
execution_authorization_record_path: experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/authorization-record.yaml
execution_authorization_record_digest_path: experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/authorization-record.sha256
owner_approval_artifact_path: experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/owner-approval.md
# Existence is not authority. The draft record and its digest exist so the
# authorization proposal has stable, reviewable bytes; neither is operative.
# Authorization requires an owner approval binding the exact current record
# digest; its presence or absence is derived repository state, computed at
# validation time -- never pinned as a fact inside this digest-hashed
# document. See section 2d for why: this document's bytes (including any
# claim about approval existence) are hashed into preparation_package_sha256,
# which is hashed into authorization-record.sha256. A present-tense existence
# claim here would flip from false to true the moment a real approval is
# added, changing this file's bytes, changing the record digest, and voiding
# the very approval that was just granted for the old digest. Only a
# historical, timestamped observation about the moment this package was
# prepared can safely live here.
owner_approval_required: true
owner_approval_must_bind_current_record_digest: true
run_control_directory_exists: true
execution_authorization_record_exists: true
execution_authorization_record_digest_exists: true
owner_approval_present_at_preparation_time: false
# Pending sentinels. All three block execution while unset.
run_control_commit_sha: PENDING_AUTHORIZATION_RECORD_CREATION
run_control_commit_sha_sentinel: PENDING_AUTHORIZATION_RECORD_CREATION
authorization_record_sha256: PENDING_OWNER_APPROVAL
authorization_record_sha256_sentinel: PENDING_OWNER_APPROVAL
pending_sentinels_block_execution: true
pending_sentinels:
  - PENDING_POST_MERGE_PIN_FINALIZATION
  - PENDING_AUTHORIZATION_RECORD_CREATION
  - PENDING_OWNER_APPROVAL
# Provenance of authority.
authoritative_digest_source: owner_approval_artifact
digest_inside_authorization_record_is_informational: true
authorization_record_self_approval_allowed: false
approving_authority: repository_owner_or_explicitly_delegated_campaign_owner
operator_self_approval_allowed: false
approval_identity_verification_required: true
required_authorization_status_string: AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION
authorization_digest_algorithm: sha256
authorization_digest_format: 64_lowercase_hex
# Required fields of the authorization record. A draft record carrying these
# fields now exists; it is a proposal awaiting owner approval, not an
# authorization.
authorization_record_required_fields:
  - schema_version
  - authorization_status
  - authorization_scope
  - evidence_number
  - evidence_slug
  - execution_framework_sha
  - target_repository
  - target_sha
  - exact_model
  - artifact_type
  - preparation_package_path
  - preparation_package_sha256
  - gate_d_checklist_path
  - gate_d_checklist_sha256
  - authorization_record_created_at
  - authorization_record_created_by
  - owner_approval_reference
  - one_invocation_only
  - no_retry
  - no_fallback
  - no_model_substitution
  - no_artifact_repair
  - no_target_mutation
  - stop_on_first_failed_gate
authorization_record_boolean_fields_must_be_true:
  - one_invocation_only
  - no_retry
  - no_fallback
  - no_model_substitution
  - no_artifact_repair
  - no_target_mutation
  - stop_on_first_failed_gate
# Required fields of the FUTURE owner-approval artifact. It does not exist yet.
owner_approval_required_fields:
  - approver_github_identity
  - approval_timestamp
  - authorization_record_sha256
  - execution_framework_sha
  - target_sha
  - evidence_number
  - evidence_slug
  - exact_model
  - authorization_decision
  - no_retry_statement
  - owner_decision_reference
canonical_preparation_package_path: docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md
canonical_gate_d_checklist_path: docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md
package_and_checklist_loaded_from_framework_root: true
external_package_or_checklist_copy_allowed: false
# Required behavior of the Gate A authorization consumer, in order.
# Current runtime behavior: scripts/gate_a_authorization.py executes these
# steps (see section 2g).
gate_a_authorization_verification_steps_are_current_runtime_behavior: true
gate_a_authorization_verification_steps_are_future_contract: false
gate_a_authorization_verification_steps:
  - 1 authorization record exists at the exact planned run-control path
  - 2 owner approval artifact must exist at the exact planned run-control path
  - 3 authorization record SHA-256 must be recomputed over its exact bytes
  - 4 recomputed digest matches the owner-approved digest
  - 5 approval identity is valid
  - 6 approval status is exactly AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION
  - 7 authorization record required fields are complete
  - 8 authorization record framework SHA matches checked-out framework HEAD
  - 9 target SHA matches checked-out Auteur HEAD
  - 10 evidence number and slug match the planned attempt
  - 11 exact model matches the enforced model
  - 12 preparation-package path and digest match
  - 13 Gate D checklist path and digest match
  - 14 one-invocation/no-retry/no-fallback rules are true
  - 15 no existing Evidence 0016 output is present
gate_a_digest_verification_precedes_invocation: true
# Every condition below is a hard stop BEFORE model invocation. See section 2h.
authorization_hard_stop_conditions:
  - authorization record absent
  - approval artifact absent
  - owner-approved digest absent
  - digest malformed
  - digest mismatch
  - approval identity unauthorized
  - record changed after approval
  - execution framework SHA mismatch
  - target SHA mismatch
  - evidence number mismatch
  - evidence slug mismatch
  - model mismatch
  - package path mismatch
  - package digest mismatch
  - checklist path mismatch
  - checklist digest mismatch
  - authorization status not exact
  - one-invocation flag false or absent
  - no-retry flag false or absent
  - conflicting duplicate records
  - more than one approval artifact
  - pre-existing Evidence 0016 output
  - mutable or floating path used as authority
  - GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED
authorization_hard_stop_count: 24
# Hard stop 24 is RETIRED: the consumer exists, is wired ahead of the first
# model call, and is proven at the invocation boundary. Conditions 1-23 are now
# reachable and evaluated. The first hard stop that still fires is the pending
# execution pin -- and the missing record and approval fire immediately after.
# No hard stop was removed; one stopped firing because its condition was fixed.
first_evaluated_hard_stop: GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING
gate_a_authorization_consumer_not_implemented_is_active: false
gate_a_authorization_consumer_hard_stop_waivable: false
authorization_failure_is_gate_a_failure: true
authorization_failure_permits_retry: false
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

# --- Acceptance criteria for the Gate A consumer (section 2j) ---
# The merged consumer satisfies these criteria; they are restated here as its contract.
gate_a_consumer_acceptance_criteria:
  - accept the immutable run-control location or exact paths as input
  - load exactly one authorization record
  - load exactly one owner-approval artifact
  - parse the 24-field authorization record schema
  - reject missing or duplicate records
  - reject missing or duplicate approvals
  - recompute authorization-record SHA-256 from exact bytes
  - compare the recomputed digest to the owner-approved digest
  - verify approval identity
  - verify authorization status
  - verify framework HEAD
  - verify target HEAD
  - verify evidence number and slug
  - verify exact model
  - verify preparation-package path and digest
  - verify Gate D checklist path and digest
  - verify all safety booleans
  - verify no pre-existing Evidence 0016 output
  - emit a deterministic structured preflight result
  - include stable failure codes
  - stop the execution path before any model call on failure
  - leave an auditable preflight record
  - perform no target writes
  - permit no retry
  - be tested through the actual invocation boundary, not only as an isolated helper
gate_a_consumer_required_test_categories:
  - valid authorization accepted
  - missing record rejected
  - missing approval rejected
  - digest mismatch rejected
  - unauthorized approver rejected
  - framework mismatch rejected
  - target mismatch rejected
  - model mismatch rejected
  - package digest mismatch rejected
  - checklist digest mismatch rejected
  - false safety flag rejected
  - duplicate record rejected
  - duplicate approval rejected
  - pre-existing evidence output rejected
  - consumer absent blocks execution
  - consumer not wired into invocation path blocks execution
  - positive proof that the model invocation cannot occur before preflight success
gate_a_consumer_required_test_categories_implemented_in_this_pr: true
# Proof a LATER independent review must demonstrate before authorization (section 2k).
proof_required_before_authorization:
  - real consumer source code exists
  - consumer source is merged
  - consumer tests pass
  - actual invocation path calls the consumer
  - a negative integration test proves model invocation count remains zero when preflight fails
  - a positive integration test proves exactly one invocation can occur only after successful preflight
  - the selected execution framework SHA contains the consumer
  - all preparation artifacts remain present at that SHA
# Ordered authorization lifecycle (section 2d). Steps 3-7 are the new prerequisite.
authorization_lifecycle_order:
  - 1 PR #107 merges as preparation contract only
  - 2 select the immutable execution framework revision containing the preparation contract
  - 3 implement the real Gate A authorization consumer
  - 4 add positive and negative consumer tests
  - 5 wire the consumer into the actual Stage 1 invocation path before any model invocation
  - 6 independently review and merge the consumer
  - 7 select a new immutable execution framework SHA containing the consumer
  - 8 create the external authorization record against that SHA
  - 9 finalize its bytes and compute SHA-256
  - 10 create the separate owner-approval artifact
  - 11 owner approves the exact digest
  - 12 pin the immutable run-control commit
  - 13 perform a dry preflight with no model invocation
  - 14 only after preflight passes may a separate owner decision authorize exactly one live invocation
effective_authorization_before_consumer_steps_complete_allowed: false
owner_approval_created_before_consumer_implementation_is_valid: false

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
# scripts/workflow-runtime.py is named ONLY as the Stage 1 entrypoint. It does
# NOT perform authorization preflight, and this package does not claim it does.
stage1_entrypoint_performs_authorization_preflight: false
workflow_runtime_enforces_authorization: false
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
# What PR #107 does and does not prove (section 10).
pr_107_proves:
  - the future authorization contract is fully specified
  - lifecycle values are internally consistent
  - historical evidence is protected
  - the package remains non-runnable
  - future consumer requirements are explicit
# Round 8: this list no longer needs a prose-guard exemption region. Each item
# is written in explicitly negative grammar the guard parses directly, so the
# facts are SCANNED rather than exempted. The key is renamed because the items
# are now negative statements -- keeping `does_not_prove` would have made every
# item a double negative.
pr_107_absence_facts:
  - "before PR #109, no authorization consumer exists in the tree"
  - "before PR #109, Gate A is not runtime-enforced"
  - owner approval cannot currently authorize a run
  - "before PR #109, digests are not checked"
  - "before PR #109, model invocation is not blocked by authorization state"
  - Evidence 0016 is not executable
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

## 1a. Gate A runtime consumer status

```text
gate_a_authorization_consumer_status: IMPLEMENTED
```

The Gate A authorization consumer now exists as runtime source at
`scripts/gate_a_authorization.py`, and it is wired into the real Stage 1
invocation path in `scripts/skill_executor.py` ahead of the first model call.

Stated plainly, and without hedging:

```text
A Gate A authorization consumer exists in this repository.
The runtime loads the authorization record.
The runtime loads and validates the owner-approval artifact.
The runtime recomputes the authorization-record SHA-256 over exact bytes.
The runtime verifies owner identity.
The runtime verifies the preparation-package digest.
The runtime verifies the Gate D checklist digest.
The runtime binds a validated authorization result to the Stage 1 model
  invocation, as a typed single-use capability object.
The 15-step sequence in section 5 is current runtime behavior. It executes.
The tests in PR #107 validate CONTRACT CONSISTENCY ONLY.
The tests in PR #107 do NOT prove runtime enforcement, and must never be
  cited as evidence of it.
The invocation-boundary proofs live in
  tests/test_gate_a_invocation_boundary.py, which exercises the real
  executors with a spy provider.
```

### What implementing the consumer did NOT do

The mechanism now exists. Nothing is authorized by it. Every one of these
remains true and blocking:

```text
A DRAFT authorization record exists, and it is NOT operative.
A DRAFT authorization-record digest file exists, and it is NOT authority.
The run-control directory exists, and it holds only draft artifacts.
Authorization requires an owner approval binding the exact current record digest.
No run-control commit is pinned.
The execution framework SHA is still PENDING_POST_MERGE_PIN_FINALIZATION.
execution_authorization_status is still NOT_AUTHORIZED.
package_runnable is still false.
package_status is still PREPARED_NOT_RUN.
Evidence 0016 is still unused.
```

The existence of the draft record and its digest is NOT authority. It means
only that the authorization *proposal* has stable, hashable bytes that an owner
could later approve. Authority arrives solely with an owner-approval artifact,
which does not exist.

An enforcement mechanism with nothing operative to enforce denies every
request. That is the intended state: the consumer returns
`GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING` while the sentinel stands, and with
the record and digest present but no owner approval on disk it denies with
`GATE_A_OWNER_APPROVAL_MISSING`, and mints no capability. Merging the consumer
therefore moves the package *closer* to being auditable, and not one step
closer to being authorized.

### Scope of the prose-honesty guard

The package tests include a deterministic prose guard that scans this document,
the Gate D checklist, and the execution package for sentences asserting that
authorization enforcement happens *now*. It exists because the authorization
contract below was specified while no runtime consumer existed, so any
present-tense enforcement sentence in these files would have been false; now
that the consumer is merged and wired, the status-aware guard in
`tests/support/state_honesty_guard.py` governs instead.

**Declared scope.** This deterministic guard covers the enumerated
active-simple-present, emphatic-do, present-progressive, and affirmative-passive
enforcement forms used by this package, with manner adverbs recognized in four
positions drawn from a closed nine-word set. It is not a general English
semantic analyzer.

Concretely, it matches a closed lexicon of enforcement verbs in four shapes.
The four shapes, in the order the exhibits below appear, are: active simple
present, emphatic `do`, present progressive, and affirmative passive. The label
column that used to sit outside the quotation marks has been removed, because
prose outside the quotes is precisely where half a claim can be hidden. Each
line is now one complete quoted exhibit with no unquoted remainder.

Invalid example:

```text
# BEGIN_PROSE_GUARD_EXEMPTION reason="non-authoritative example"
"Gate A verifies the digest."
"Gate A does verify the digest."
"Gate A is checking the digest."
"The digest is verified by Gate A."
# END_PROSE_GUARD_EXEMPTION
```

**Adverb positions covered.** The passive grammar accepts a bounded manner
adverb in four slots. The guard rejects all four of these when the claim
is affirmative. The four slots, in the order the exhibits below appear, are:
pre-participle, post-participle, pre-agent, and post-agent. Each line is one
complete quoted exhibit with no unquoted remainder.

Invalid example:

```text
# BEGIN_PROSE_GUARD_EXEMPTION reason="non-authoritative example"
"The digest is procedurally verified."
"The digest is verified procedurally."
"The digest is verified procedurally by Gate A."
"The digest is verified by Gate A procedurally."
# END_PROSE_GUARD_EXEMPTION
```

**Supported manner-adverb set (exactly these nine).** `procedurally`,
`automatically`, `currently`, `mechanically`, `deterministically`, `explicitly`,
`directly`, `securely`, `synchronously`. The guard claims support for these
words only, not for arbitrary English adverbs. At most two adverbs are accepted
per slot; the grammar uses explicit bounded quantifiers, never an open span.

**No manner-adverb carve-out exists.** An earlier revision allowed an agentless procedural-block phrasing on the
grounds that such wording asserts the opposite of runtime enforcement. That exception was demonstrably bypassable in the pre-participle
slot, so it was deleted rather than extended. Truthful statements of this kind
are now written in plainly negative form instead --
`The run remains non-runnable until an owner approval binds the exact current record digest.` -- which
contains no enforcement participle and therefore needs no exception.

What it deliberately does **not** do: parse arbitrary English, resolve
coreference, model tense beyond the auxiliaries `is/are/was/were` and
`do/does/did`, or detect paraphrase. Modal and future forms (`must verify`,
`will recompute`, `would be verified`) are legal by design, because those are
the truthful ways to describe a contract requirement as a requirement, rather
than as a claim that some particular run has already been authorized.

Negation counts only in the auxiliary slot of the matched construction
(`is not verified`, `does not verify`, `is not checking`) or bound to the
subject (`no current runner verifies`). Proximity to `not`, `prohibited`,
`must not`, `example`, `old wording`, `future` or `required` exempts nothing.

**Exemption-marker semantics.** The only exemption is an exactly paired
`BEGIN_PROSE_GUARD_EXEMPTION` / `END_PROSE_GUARD_EXEMPTION` region. The opening
marker requires a non-empty reason from a closed set: `quoted obsolete wording`
or `non-authoritative example`. Enclosing text excludes
it from lexical matching and does **not** make it authoritative; authoritative
contract requirements must never be placed inside a region. The mechanism fails
closed: a missing, blank or unknown reason, a nested region, an unmatched
marker, a region longer than twelve lines, a region covering more than half a
document, a marker inside inline code, and a near-miss spelling all exempt
nothing. Text after a closing marker is scanned normally.

These markers previously carried a name implying they enclosed only historical
quotations. They were renamed because they also enclosed current truthful denial
lists, so that name misdescribed their own function -- unacceptable in a package
whose subject is documentation honesty.

**Reason-content contracts (round 8).** Marker reasons are **not merely
vocabulary labels**. The seventh review demonstrated that validating only the
marker structure and the reason vocabulary bought nothing: a structurally
perfect region labelled `reason="truthful denial list"` containing one
affirmative simple-present sentence naming Gate A, the authorization digest and
every invocation was accepted, hiding a real enforcement overclaim. (The exact
string is not reproduced here, because reproducing it would itself be an
overclaim; it is held only as a test fixture, `DEMONSTRATED_BYPASS_CLAIM`, in
`tests/test_stage1_auteur_prep_package.py`.) A reason must constrain what
its region may contain; it may never be a label that switches inspection off.

Each remaining reason carries its own **mechanically validated content
contract**, checked *before* the region is exempted from ordinary scanning:

| Reason | Content contract the guard enforces |
|---|---|
| `quoted obsolete wording` | Immediately introduced by text identifying the content as old, obsolete, superseded or quoted historical wording; every line is quoted or blockquoted; bounded to six content lines; no current authoritative statement may sit beside the quotation. |
| `non-authoritative example` | The whole immediately preceding line must be one of a small closed set of approved, non-negated introducers; the region is bounded to six content lines; every line must be an explicit quotation; and everything outside the quotation marks is scanned with the shared enforcement lexicon. Illustrative shape alone exempts nothing, and the permissive label-column heuristic was deleted in round 9. |

The architecture is no longer "parse markers, delete exempt content, scan the
remainder". It is: parse markers, validate marker structure and reason
vocabulary, validate each region's content against its declared reason, then
scan all non-exempt governing prose. Region validation reuses the **same**
enforcement lexicon and the same active/emphatic/progressive/passive matchers as
ordinary prose; there are deliberately not two lexicons that could drift apart.
A region that fails its contract exempts nothing at all.

Consequently a valid reason **cannot hide an affirmative current-enforcement
claim**. Reason *accuracy* still receives manual review -- the guard does not
decide whether a well-formed negative denial list is factually true, or whether
a quotation is genuinely historical -- but an **obvious semantic mismatch
mechanically fails its reason contract**. (Phrased without an enforcement
participle on purpose: the guard applies its own lexicon to this document, and
no carve-out exists for prose describing the guard itself.)

This remains a **deterministic lexical/structural guard**, not a general
semantic analyzer, and it claims no natural-language understanding.

**Preferred remedy is elimination, not a cleverer exemption.** Both real
`truthful denial list` regions were removed in round 8 by rewriting their items
into explicitly negative grammar the guard parses directly, taking the real
region count in **checked-in files only** from six to four. In round 9 the live
PR body's surviving denial region was rewritten the same way, and the reason
was retired from the allowed set entirely. Fewer exemption regions is safer
than more sophisticated exemption validation. The four remaining checked-in
regions are all `non-authoritative example` regions holding
deliberately-rejected illustrative strings, each an explicit quotation, and `tests/test_stage1_auteur_prep_package.py` builds a deterministic
inventory of every one of them (file, opening line, closing line, reason,
introducer, size, and reason-specific validator result) so they can be audited
in one place.

**The quoted-example contract is deliberately narrow (round 10).** Round 9
validated example regions by deleting every quoted span and scanning the
leftovers. That is compositionally bypassable: a single sentence can be split
across the quote boundary so neither leftover fragment is a complete clause and
the scanner sees nothing. Two demonstrated shapes -- one that quotes only the
predicate and object, and one that quotes only the subject and verb -- both
slipped through, even though the very same sentence with no quotation marks at
all does not. That asymmetry pins the defect on quote segmentation rather than
on lexicon coverage. The full attack matrix lives in
`tests/test_stage1_auteur_prep_package.py`, which is where such strings belong.

The remedy is not a smarter remainder scanner. Inferring whether fragments
outside the quotes happen to reconstitute a claim is the guess-the-grammar
approach that failed repeatedly. Instead the contract is now fail-closed:

> one line, one balanced quoted exhibit, no meaningful unquoted remainder.

A content line may contain only an optional blockquote prefix, optional list
indentation or bullet, exactly one complete balanced quoted exhibit, optional
terminal punctuation, and whitespace. Any other non-whitespace token outside
the exhibit rejects the region. Partial-span bypasses are then impossible by
construction: there is nowhere outside the quotation marks to put the other
half of the sentence. Supported quote styles are exactly two -- straight double
and smart double. Nested quotation, escaped quotation marks, multi-line quote
spans, inline-code backticks, mixed straight/smart pairs, multiple independent
spans, and every other Unicode quotation mark all fail closed with a named
reason (`UNQUOTED_LEADING_TEXT`, `MULTIPLE_QUOTED_SPANS`,
`MULTILINE_QUOTE_UNSUPPORTED`, `INLINE_CODE_NOT_QUOTATION`, and so on) rather
than being silently misparsed. The label column that previously sat outside the
quotation marks in the checked-in regions was removed for exactly this reason;
the labels now live in ordinary scanned prose above each region.

Because the guard's scope is bounded and enumerated, it is a regression fence
for the wordings reviewers have actually demonstrated -- not proof that no
dishonest sentence can ever be written. Reviewer judgement remains required.

### Measured results (round 10)

Recorded here, in the versioned package, so the numbers are not held only in a
PR description. All figures below were observed, not carried forward.

Canonical environment: Python 3.12.8 (`pyproject` requires >=3.11 and classifies
3.11/3.12; CI pins 3.11, which is not installed on this machine, so the other
classified version was used -- recorded, not assumed), `pip install -e .`,
`pytest` 9.1.1, PyYAML 6.0.3, click 8.4.2, `claude-agent-sdk==0.2.82`, and
`--basetemp` on Windows.

```text
package tests   python -m pytest tests/test_stage1_auteur_prep_package.py -q
                322 passed, 439 subtests passed, exit 0
                (historical: 301 / 353 in round 9; 272 / 338 in round 8;
                 239 / 286 in round 7)

focused suite   clean main (1761e42f) : 236 passed, 5 skipped,   7 subtests, exit 0 (11 files)
                proposed merge        : 558 passed, 5 skipped, 446 subtests, exit 0 (12 files)
                delta +322 passing, +439 subtests; 236+322=558, 7+439=446

broader suite   python -m pytest tests -q --continue-on-collection-errors
                clean main (1761e42f) : 23 failed, 587 passed, 6 skipped, 3 errors,
                                        25 warnings,  74 subtests, exit 1
                proposed merge        : 23 failed, 909 passed, 6 skipped, 3 errors,
                                        25 warnings, 513 subtests, exit 1
                delta +322 passing, +439 subtests; 587+322=909, 74+439=513
```

Failure and collection-error node IDs were captured and diffed: the two sets are
byte-identical (26 lines -- 23 `FAILED` plus 3 `ERROR`, identical MD5). No
existing pass became a failure, and the entire passing delta corresponds exactly
to the new preparation-package tests, which do not exist on `main`.

**Correction to the previously published focused-suite absolutes.** The figures
carried in the PR description before round 8 (`249 passed / 10 subtests` on
`main`) were overstated by 13 passed and 3 subtests. The observed clean-`main`
figures are `236 passed / 7 subtests`. The published *delta* was never wrong;
only the absolute totals were. They are corrected here and in the PR body.

**The three collection errors have three independent causes, not two.** They are
enumerated separately in the PR description; the two `ImportError` modules are
not one duplicated fault -- `test_auto_invocation_target_repo.py` imports one
name that the package does not export, while `test_integration_external_repo.py`
imports two (`SkillsOrchestrator` *and* `ConfigManager`). All three reproduce
identically on clean `main` and are unrelated to this PR.

### What cannot make this package runnable

This is the point of the section. Three plausible-looking paths to a "runnable"
state are each explicitly insufficient:

| Attempted path | Result |
|---|---|
| Fill in all three pending sentinels with real SHAs and digests | **Still not runnable.** By hand they are unapproved; Gate A denies. |
| Create the run-control directory, the authorization record, and the digest file | **Still not runnable.** Done: they exist as drafts, and Gate A denies for missing owner approval. |
| Obtain a genuine repository-owner approval of the exact digest | **Still not runnable** until the execution pin is also finalized. |

Existence is not authority. Drafting a record and hashing it produces stable
bytes an owner *could* approve; it produces no approval. An approval is a
decision *about* an enforcement mechanism, and the mechanism now exists and
evaluates it — but no approval has been given.

The consumer requirement has been satisfied. The consumer was:

1. **implemented** as real source code;
2. **tested**, with the positive and negative categories of section 2j;
3. **reviewed** independently;
4. **merged**;
5. **wired into the real Stage 1 invocation path**, ahead of the first model
   call, and proven so by integration test.

All five are true, so `GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED`
(hard stop 24, section 2h) is retired and no longer fires. Authorization state
is therefore effective — and it currently evaluates to DENY.

### Where the consumer lives

```yaml
gate_a_authorization_consumer_path: scripts/gate_a_authorization.py
gate_a_consumer_integration_point: scripts/skill_executor.py::ClaudeAgentSdkSkillExecutor
```

The contract requires that the consumer gate the real Stage 1 execution
path — which enters through `scripts/workflow-runtime.py` — before the
first model call. It does **not** claim that `scripts/workflow-runtime.py`
performs, or has ever performed, any authorization preflight. It does not; the
preflight happens at the executor integration point named above.
`scripts/workflow-runtime.py` is named in this package solely as
`stage1_entrypoint`
(`stage1_entrypoint_performs_authorization_preflight: false`).

Selecting the exact module, and the exact call site ahead of the first model
invocation, is a decision for the separately scoped consumer-implementation
task, which must justify it against the repository's actual runtime
architecture rather than against a location guessed here in advance.

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
  it cannot be known until PR #107 merges. The run remains non-runnable while it
  holds the sentinel value. See section 2a.

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
The run remains non-runnable while execution_framework_sha is unset.
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
3. That exact full 40-character SHA — never abbreviated, never a branch ref —
   is *selected* at this point, but it is **not written into this package**.
   No PR writes an execution pin into this document. The selected SHA is
   recorded only later, inside the future immutable `authorization-record.yaml`
   described in section 2b, in that record's own `execution_framework_sha`
   field.
4. Selecting the SHA is a prerequisite for authoring the authorization record;
   it is not itself an edit to any governing artifact.
5. Only then may a separate owner-level task decide whether to authorize the
   live attempt and create that authorization record.
   Pin finalization is not authorization.

The framework SHA selected under this procedure is
`cad8ef227d6c20a28e786e90c0401f776f4b7b51` (the canonical merge commit of
PR #109 on `main`). Recording it here as prose is descriptive history, not an
execution pin: it is inert until an owner-approved authorization record carries
it, and the machine-readable contract above still reads
`PENDING_POST_MERGE_PIN_FINALIZATION`.

### Chosen mechanism: owner-approved external immutable authorization record

A document cannot contain its own future merge SHA, and this package does
**not** attempt to. It also does not delegate that job to a later PR against
itself. Instead:

- This package's machine-readable contract keeps
  `execution_framework_sha: PENDING_POST_MERGE_PIN_FINALIZATION` permanently.
  The preparation package remains the **governing contract**, not the pin
  carrier. The sentinel is permanent and is never replaced: it means "no
  operative authorization record currently supplies the execution pin", not
  "a value is owed to this field". Any future PR that proposes to write a SHA
  into this field, or to add a second finalized-pin field beside it, is
  out of contract and must be rejected.
- A separate immutable **authorization record**, created only after this
  preparation PR merges, carries the **execution pin**.
- The Gate A consumer must consume the authorization record as the
  authoritative execution pin, while continuing to obey this package as the
  governing contract; the consumer merged in PR #109 implements this
  requirement.

This avoids the circular requirement that a commit contain its own SHA: the
record is authored *after* the revision it pins is already immutable, and the
governing contract never mutates to carry a pin at all.

That record does **not** exist yet. It must not be created by this PR.
Authorization cannot succeed without an owner approval binding the exact
current record digest. The package remains non-runnable.

---

## 2b. The single mandatory authorization mechanism

An earlier revision of this package offered the authorization record two
possible homes: it could "exist at the pinned framework revision, **or** be
copied into an immutable run-control location whose SHA-256 digest is
recorded". **That fork is deleted.** It was unsafe in both branches:

- The first branch is **logically impossible** under this package's own
  ordering. The authorization record is authored *after* the execution
  framework revision it pins already exists and is immutable. A commit cannot
  retroactively contain a file written after it. Offering that branch invited
  an operator to satisfy it by amending, rewriting, or re-pinning history.
- The second branch was offered as **optional**, named **no approving
  authority**, and let the operator record the digest of whatever bytes they
  happened to be holding. Self-recording a digest of your own file proves
  only that the file hashes to its own hash. It authenticates nothing.

Exactly one mechanism is permitted, with no alternative:

```text
MECHANISM (mandatory, sole, non-optional):
  Owner-approved external immutable authorization record.

The future authorization record MUST:
  1. be created only after PR #107 has merged;
  2. pin an already-existing immutable execution framework SHA;
  3. live OUTSIDE the pinned framework commit;
  4. be stored in the explicit immutable run-control location named below;
  5. have its exact bytes hashed with SHA-256;
  6. have that SHA-256 digest approved by the repository owner, in a
     DISTINCT approval artifact, before any invocation;
  7. be verified by the Gate A consumer before any model invocation
     (that consumer now exists and enforces; see section 1a);
  8. remain immutable for the life of Evidence 0016.

There is no second mechanism. There is no fallback. There is no
operator-chosen variant. The authorization record must NOT exist at the
pinned framework revision, and no copy-with-self-recorded-digest is
acceptable as authority.
```

The contract field `authorization_mechanism_alternatives_allowed` is `false`
and `authorization_mechanism_count` is `1`. Any document, script, or operator
procedure that presents a choice of authorization provenance is in violation
of this package and is a Gate A hard stop.

---

## 2c. Immutable run-control location

The authorization artifacts live in a dedicated run-control directory that is
unique to Evidence 0016, outside all historical evidence directories, and
clearly distinguishable from generated evidence output:

```text
experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/
```

The authorization record and its digest are drafted by this PR at the first two
paths below; the third path must remain absent until the repository owner
creates it:

```text
experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/authorization-record.yaml
experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/authorization-record.sha256
experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/owner-approval.md
```

Properties this location must satisfy:

- **explicit** — the exact paths are named here, in advance, not chosen at
  run time;
- **unique to Evidence 0016** — no other attempt shares the directory;
- **outside historical evidence directories** — it is not under
  `experiments/evidence/`, and in particular never under
  `experiments/evidence/0015-...`;
- **distinguishable from generated evidence** — run-control artifacts are
  authored governance inputs, never model output;
- **immutable after owner approval** — see section 2f;
- **populated only with draft, non-operative artifacts before owner
  approval** — the directory now exists
  (`run_control_directory_exists: true`) and holds the draft authorization
  record and its digest, but it does not and must not contain
  `owner-approval.md` (`owner_approval_present_at_preparation_time: false`,
  a historical observation about preparation time, not a claim about the
  present). Stable bytes for a proposal are not an approval of it.

---

## 2d. Owner-approved digest chain

The approval chain is deterministic and ordered. No step may be reordered,
merged, or skipped.

```text
 1. PR #107 merges as PREPARATION ONLY.
 2. A later task selects an immutable execution framework SHA that contains:
      - this preparation package;
      - the Gate D checklist;
      - the package-validation tests;
      - the runtime validator;
      - model enforcement;
      - target-safety controls.
 3. A DRAFT authorization record is created OUTSIDE that pinned revision,
    in the run-control location of section 2c.
 4. Its exact bytes are finalized. No further edit is permitted after this
    point without restarting the chain from step 3.
 5. SHA-256 is computed over the exact finalized record bytes.
 6. The repository owner approves THAT EXACT DIGEST in a DISTINCT approval
    artifact (owner-approval.md).
 7. The approval artifact records: authorization-record digest; execution
    framework SHA; Auteur target SHA; evidence number; exact model; and an
    explicit authorization decision.
 8. Before invocation, the required Gate A consumer must RECOMPUTE the
    authorization-record SHA-256 from the bytes on disk.
 9. That consumer must COMPARE the recomputed digest to the OWNER-APPROVED
    digest from the approval artifact.
10. Any mismatch, absence, malformed record, or conflicting field must be a
    HARD STOP before model invocation.
```

**Steps 8-10 describe required behavior of the Gate A consumer, which now
exists and performs them.** See section 1a. Their being performed authorizes
nothing: with the sentinels standing and no owner approval, they deny. The full ordered lifecycle,
including the consumer-implementation steps that must precede step 3 above, is
restated in `authorization_lifecycle_order` and immediately below.

### Ordered lifecycle including consumer implementation

The chain above cannot begin at "create a draft authorization record". The
consumer must exist first, or the record it is written for governs nothing:

```text
 1. PR #107 merges as a PREPARATION CONTRACT ONLY.
 2. Select the immutable execution framework revision containing that contract.
 3. IMPLEMENT the real Gate A authorization consumer.
 4. Add positive and negative consumer tests.
 5. WIRE the consumer into the actual Stage 1 invocation path, ahead of any
    model invocation.
 6. Independently review and merge the consumer.
 7. Select a NEW immutable execution framework SHA that contains the consumer.
 8. Create the external authorization record against THAT SHA.
 9. Finalize its bytes and compute SHA-256.
10. Create the separate owner-approval artifact.
11. The owner approves that exact digest.
12. Pin the immutable run-control commit.
13. Perform a DRY PREFLIGHT with no model invocation.
14. Only after preflight passes may a separate owner decision authorize
    exactly one live invocation.
```

Creating effective authorization before steps 3-7 are complete is
**prohibited** (`effective_authorization_before_consumer_steps_complete_allowed:
false`). An owner approval created before the consumer is implemented and
merged is **invalid and non-operative**
(`owner_approval_created_before_consumer_implementation_is_valid: false`) — it
approves an enforcement step that nothing performs, and it must not be
carried forward or reused once the consumer later exists. The framework SHA
used for authorization must be selected *after* consumer merge
(`execution_framework_sha_selected_after_consumer_merge: true`), because a
revision predating the consumer cannot enforce the contract it carries.

**The authorization record must not approve itself.** If the record contains a
digest field describing itself, that value is **informational only** and must
never be treated as authoritative — a record can trivially be edited to carry
a digest matching its own edited bytes. The authoritative digest comes solely
from the distinct owner-approval artifact
(`authoritative_digest_source: owner_approval_artifact`).

---

## 2e. Approving authority and identity verification

The approving authority is the **repository owner**, or an **explicitly
delegated campaign owner** named by the owner.

The owner-approval artifact must include:

```text
approver_github_identity        (the approving GitHub account)
approval_timestamp              (ISO-8601, UTC)
authorization_record_sha256     (exact 64 lowercase hex characters)
execution_framework_sha         (exact full 40-character SHA)
target_sha                      (exact full 40-character SHA)
evidence_number                 ("0016")
evidence_slug                   (0016-stage1-auteur-post-remediation-controlled-attempt)
exact_model                     (claude-sonnet-5)
authorization_decision          AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION
no_retry_statement              (explicit: no retry, no rerun, no repair)
owner_decision_reference        (the owner decision authorizing the run)
```

**The operator executing the run must not self-approve.** An operator may
supply the approval only if that operator is also the recorded owner or the
recorded delegate *and* the approval identity must be explicitly verified
(`operator_self_approval_allowed: false`).

Approval identity must be verified by, at minimum, all of:

1. the approval artifact is committed to (or otherwise stored immutably in)
   the run-control location of section 2c;
2. Git history or platform identity shows **who** authored/approved it —
   commit author/committer identity, or the merging reviewer identity on the
   run-control PR;
3. that identity matches the owner/delegate named in this authorization
   contract.

If any of the three cannot be demonstrated, approval identity is
**unauthorized** and Gate A fails.

---

## 2f. Immutability of the run-control artifacts

"Immutable run-control location" is **not** a filesystem convention. A
directory path is not an immutability guarantee — files at a path can be
rewritten silently.

The approved artifacts must be fixed by at least one **immutable content
identity**:

- a committed Git blob/commit SHA **plus** the owner-approved SHA-256 digest;
  or
- an immutable artifact-store object ID **plus** the owner-approved SHA-256
  digest.

For this repository, the preferred form is a **dedicated Git commit or merged
PR containing the run-control artifacts**, combined with the owner-approved
SHA-256 digest of the authorization record.

No circular self-reference is created, because the two commits are distinct:

```text
- the authorization record pins an EARLIER framework execution SHA;
- the LATER run-control commit contains the authorization and approval
  artifacts;
- the consumer verifies BOTH the framework SHA and the
  authorization digest;
- the run-control commit does NOT need to equal the framework execution SHA,
  and must not be assumed to.
```

The future execution package therefore distinguishes three separate values:

```yaml
execution_framework_sha: PENDING_POST_MERGE_PIN_FINALIZATION
run_control_commit_sha: PENDING_AUTHORIZATION_RECORD_CREATION
authorization_record_sha256: PENDING_OWNER_APPROVAL
```

All three are unset in PR #107 and hold sentinels. **Every pending sentinel
blocks execution** (`pending_sentinels_block_execution: true`). A sentinel is
not a SHA, not a digest, and must never be replaced by a guessed,
abbreviated, anticipated, or branch-derived value.

---

## 2g. Required contents of the future authorization record

The future authorization record must contain at least the following fields.
This is the complete required contract; a record missing any of them
must be rejected.

```yaml
schema_version:                  # e.g. "1"
authorization_status:            # exactly AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION
authorization_scope:             # single controlled Stage 1 invocation, Evidence 0016
evidence_number:                 # "0016"
evidence_slug:                   # 0016-stage1-auteur-post-remediation-controlled-attempt
execution_framework_sha:         # full 40-char SHA, already immutable
target_repository:               # https://github.com/ThorStarlord/auteur.git
target_sha:                      # 0653defb05625f2fcde0ac32eac6e59ccf7eeb90
exact_model:                     # claude-sonnet-5
artifact_type:                   # repository_sensemaking_brief
preparation_package_path:        # canonical path, see below
preparation_package_sha256:      # 64 lowercase hex
gate_d_checklist_path:           # canonical path, see below
gate_d_checklist_sha256:         # 64 lowercase hex
authorization_record_created_at: # ISO-8601 UTC
authorization_record_created_by: # authoring identity (NOT the approver)
owner_approval_reference:        # pointer to the distinct approval artifact
one_invocation_only:             true
no_retry:                        true
no_fallback:                     true
no_model_substitution:           true
no_artifact_repair:              true
no_target_mutation:              true
stop_on_first_failed_gate:       true
```

The record binds together, in one signed-off object: the framework revision;
the target revision; the evidence identity; the model identity; the governing
package; the Gate D checklist; the authorization scope; the
one-invocation/no-retry constraints; and the owner approval.

The record must be **rejected** if any required field is absent, blank, malformed,
or inconsistent with this preparation package. `authorization_record_created_by`
is the *author*, never the *approver*; approval lives only in the separate
artifact.

### Package and checklist provenance

The record carries SHA-256 digests for the two governing documents, and the
Gate A consumer verifies them before any model invocation:

```text
SHA-256(preparation package bytes) == authorization record preparation_package_sha256
SHA-256(Gate D checklist bytes)    == authorization record gate_d_checklist_sha256
```

Both files must be loaded from `framework_root` at the finalized
`execution_framework_sha`. External or copied package/checklist files are
prohibited (`external_package_or_checklist_copy_allowed: false`). The declared
paths must match the canonical paths declared in PR #107:

```text
docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md
docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md
```

Any digest mismatch is a hard stop before model invocation.

---

## 2h. Authorization-record failure modes (all hard stops)

Every condition below **stops the run before model invocation**. None permits
retry, repair, substitution, or "proceeding with a note".

| # | Hard-stop condition |
|---|---|
| 1 | authorization record absent |
| 2 | approval artifact absent |
| 3 | owner-approved digest absent |
| 4 | digest malformed (not 64 lowercase hex) |
| 5 | digest mismatch (recomputed != owner-approved) |
| 6 | approval identity unauthorized |
| 7 | record changed after approval |
| 8 | execution framework SHA mismatch |
| 9 | target SHA mismatch |
| 10 | evidence number mismatch |
| 11 | evidence slug mismatch |
| 12 | model mismatch |
| 13 | package path mismatch |
| 14 | package digest mismatch |
| 15 | checklist path mismatch |
| 16 | checklist digest mismatch |
| 17 | authorization status not exactly `AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION` |
| 18 | one-invocation flag false or absent |
| 19 | no-retry flag false or absent |
| 20 | conflicting duplicate records |
| 21 | more than one approval artifact |
| 22 | pre-existing Evidence 0016 output |
| 23 | mutable or floating path used as authority |
| 24 | `GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED` |

Each classifies **Gate A as failed**, stops before model invocation, produces
**no retry**, and preserves the failed preflight record.

### Hard stop 24 — `GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED` (RETIRED)

This hard stop **no longer fires**, because its condition was fixed rather than
waived: a reviewed Gate A consumer now exists and is wired into the real
invocation path ahead of the first model call. It is deliberately **kept in the
list of 24 and kept non-waivable**, so that deleting or unwiring the consumer
would make it fire again.

Conditions 1-23 are now *reachable* and are evaluated by
`scripts/gate_a_authorization.py`. The first hard stop that still fires is the
pending execution pin (`GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING`). The
authorization record and its digest now exist as drafts, so the next hard stop
that fires once the pin is finalized is the missing owner approval
(`GATE_A_OWNER_APPROVAL_MISSING`).

Semantics:

```text
TRIGGERED whenever no reviewed and merged Gate A authorization consumer exists.
TRIGGERED whenever the consumer is not wired into the real Stage 1 invocation
  path, ahead of the first model call.
TRIGGERED whenever only document-consistency tests exist, and no test exercises
  the actual invocation boundary.

EFFECT:
  - BLOCKS creation of a runnable authorization state;
  - BLOCKS any owner authorization from taking effect;
  - STOPS before model invocation;
  - PERMITS NO RETRY;
  - CANNOT be waived, and specifically cannot be satisfied by filling
    authorization-record fields, digest fields, or sentinel values by hand.
```

Its current value is `gate_a_authorization_consumer_not_implemented_is_active:
false` and it remains not waivable
(`gate_a_authorization_consumer_hard_stop_waivable: false`).

**Current state: a Gate A authorization consumer exists and is enforcing, so
authorization state is now enforceable. A draft authorization record and its
digest file exist, and neither is operative. Authorization requires an owner
approval binding the exact current record digest, and none binds it. No
execution pin is finalized. The package is not runnable.**

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

## 2j. Acceptance criteria for the Gate A authorization consumer

The criteria below were specified while the consumer was still future work;
the implementation PR has since merged `scripts/gate_a_authorization.py`, which
satisfies them, as proven by `tests/test_gate_a_authorization_consumer.py`.
They are restated here as the consumer's contract.

The Gate A authorization consumer must:

1. accept the immutable run-control location, or the exact paths, as input;
2. load exactly one authorization record;
3. load exactly one owner-approval artifact;
4. parse the 24-field authorization-record schema of section 2g;
5. reject missing or duplicate records;
6. reject missing or duplicate approvals;
7. recompute the authorization-record SHA-256 from its exact bytes;
8. compare that recomputed digest to the owner-approved digest;
9. verify approval identity;
10. verify authorization status;
11. verify framework HEAD;
12. verify target HEAD;
13. verify evidence number and slug;
14. verify the exact model;
15. verify the preparation-package path and digest;
16. verify the Gate D checklist path and digest;
17. verify all safety booleans;
18. verify that no pre-existing Evidence 0016 output is present;
19. emit a deterministic structured preflight result;
20. include stable failure codes;
21. stop the execution path before any model call on failure;
22. leave an auditable preflight record;
23. perform no target writes;
24. permit no retry;
25. **be tested through the actual invocation boundary**, not only as an
    isolated helper.

Criterion 25 is load-bearing. A consumer that passes unit tests in isolation but
is never called by the real Stage 1 path enforces nothing, and reproduces
exactly the defect this section exists to prevent: a specification that looks
enforced and is not.

### Required future test categories

The consumer implementation PR must supply at least these categories. **PR #107
implemented none of them**; PR #107 asserts only, at contract level, that they
are mandatory future work. The implementation work has since supplied them
(`tests/test_gate_a_authorization_consumer.py`), and the contract field
`gate_a_consumer_required_test_categories_implemented_in_this_pr` now reads
`true`.

```text
valid authorization accepted
missing record rejected
missing approval rejected
digest mismatch rejected
unauthorized approver rejected
framework mismatch rejected
target mismatch rejected
model mismatch rejected
package digest mismatch rejected
checklist digest mismatch rejected
false safety flag rejected
duplicate record rejected
duplicate approval rejected
pre-existing evidence output rejected
consumer absent blocks execution
consumer not wired into invocation path blocks execution
positive proof that the model invocation cannot occur before preflight success
```

---

## 2k. Proof required before any future authorization

Future authorization must not proceed until a later independent review
demonstrates **all** of the following. Each is an observable fact about merged
code, not a claim in a document:

```text
1. real consumer source code exists;
2. consumer source is merged;
3. consumer tests pass;
4. the actual invocation path calls the consumer;
5. a NEGATIVE integration test proves the model invocation count remains ZERO
   when preflight fails;
6. a POSITIVE integration test proves exactly ONE invocation can occur, and
   only after successful preflight;
7. the selected execution framework SHA contains the consumer;
8. all preparation artifacts remain present at that SHA.
```

Machine-readable form:

```yaml
consumer_merge_required_before_authorization: true
consumer_integration_proof_required: true
negative_zero_invocation_test_required: true
positive_single_invocation_test_required: true
```

Items 5 and 6 are the substantive proof. Everything else can be satisfied by
code that exists but is never reached; only an integration test taken across
the real invocation boundary distinguishes an enforced gate from a decorative
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

#### Required behavior of the Gate A authorization consumer

> **This subsection states the ratified contract requirement** for the Gate A
> consumer, which now exists at `scripts/gate_a_authorization.py` and performs
> the fifteen steps below at the invocation boundary. The requirement is
> normative: it binds the consumer, and it is not a grant of authorization to
> any run. See section 1a.

**Digest verification must occur BEFORE model invocation.** The required Gate A
consumer must recompute the authorization-record SHA-256 and compare it against
the owner-approved digest *before* any model is invoked. Before any live
attempt may be authorized, an implemented consumer must complete all fifteen
steps below successfully, in this order:

```text
 1. Authorization record exists at the EXACT planned run-control path:
    experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/authorization-record.yaml
 2. Owner approval artifact must exist at:
    experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/owner-approval.md
 3. Authorization record SHA-256 must be RECOMPUTED over its exact bytes
    on disk.
 4. The recomputed digest MATCHES the owner-approved digest taken from the
    approval artifact (never from the record itself).
 5. Approval identity is valid: approver is the repository owner or the
    explicitly delegated campaign owner, verified per section 2e.
 6. Approval status is exactly AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION.
 7. Authorization record required fields are complete, non-blank, well-formed.
 8. Authorization record execution_framework_sha == framework checkout HEAD.
 9. Authorization record target_sha == Auteur target checkout HEAD.
10. Evidence number "0016" and slug match the planned attempt exactly.
11. exact_model matches the enforced model (claude-sonnet-5).
12. preparation_package_path matches the canonical path AND
    SHA-256(preparation package bytes at framework_root) == preparation_package_sha256.
13. gate_d_checklist_path matches the canonical path AND
    SHA-256(Gate D checklist bytes at framework_root) == gate_d_checklist_sha256.
14. one_invocation_only, no_retry, no_fallback, no_model_substitution,
    no_artifact_repair, no_target_mutation, stop_on_first_failed_gate are all true.
15. No existing Evidence 0016 output is present anywhere.
```

Any failure of any step:

- classifies **Gate A as failed**;
- **stops before model invocation**;
- produces **no retry**;
- **preserves the failed preflight record**.

The full hard-stop condition list is section 2h. The three pending sentinels
(`PENDING_POST_MERGE_PIN_FINALIZATION`,
`PENDING_AUTHORIZATION_RECORD_CREATION`, `PENDING_OWNER_APPROVAL`) each block
execution on their own. Hard stop 24,
`GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED`, is retired and no longer
fires, because the component that reads the sentinels now exists; it is kept
non-waivable so that deleting or unwiring the consumer would make it fire
again.

- A reviewed, merged Gate A authorization consumer exists, and is wired into
  the real Stage 1 invocation path ahead of the first model call. Absent this,
  Gate A fails at hard stop 24 and none of the fifteen steps above can run.
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
The run remains non-runnable while execution_framework_sha is
  PENDING_POST_MERGE_PIN_FINALIZATION.
The run remains non-runnable while run_control_commit_sha is
  PENDING_AUTHORIZATION_RECORD_CREATION.
The run remains non-runnable while authorization_record_sha256 is
  PENDING_OWNER_APPROVAL.
A Gate A authorization consumer now exists and enforces this contract at the
  invocation boundary. Its existence authorizes nothing; it only makes the
  non-authorized state enforceable rather than merely documented.
A draft authorization record, its digest file, and the run-control directory
  exist. None of them is operative, and their existence is NOT authority.
  Authorization requires an owner approval binding the exact current record
  digest, and none binds it. The package is not runnable.
Authorization requires the sole mandatory mechanism of section 2b: an
  owner-approved external immutable authorization record whose SHA-256 digest
  the repository owner approved in a distinct artifact, verified by Gate A
  before invocation. There is no alternative mechanism.
A separate, explicit owner instruction is required.
At most one invocation could ever be authorized by such an instruction.
No automatic retry, repair, or rerun is permitted even then.
```

### What PR #107 proves, and what it does not

PR #107 **proves**:

```text
- the future authorization contract is fully specified;
- lifecycle values are internally consistent;
- historical evidence is protected;
- the package remains non-runnable;
- future consumer requirements are explicit.
```

PR #107 **does not prove** runtime enforcement. Stated as scanned negative
facts rather than inside a prose-guard exemption region:

- before PR #109, no authorization consumer exists in the tree;
- before PR #109, Gate A is not runtime-enforced;
- owner approval cannot currently authorize a run;
- before PR #109, digests are not checked;
- before PR #109, model invocation is not blocked by authorization state;
- Evidence 0016 is not executable.

PR #107 is a **preparation-contract PR**. It implements no security
enforcement. Its tests are contract-consistency tests
(`pr_107_tests_are_contract_consistency_tests: true`) and must never be cited
as evidence that runtime enforcement exists
(`pr_107_implements_runtime_enforcement: false`).

### Owner authorization (blank — no approval pre-filled, and not yet meaningful)

**An approval entered below would still not make this package runnable**, and
this block must remain blank here regardless. The consumer now exists, so the
condition recorded as
`owner_approval_created_before_consumer_implementation_is_valid: false` is no
longer what blocks an approval. What blocks it now is that the execution pin is
still `PENDING_POST_MERGE_PIN_FINALIZATION`, and that a valid approval is a
separate owner-authored artifact at the run-control path — never prose filled
into this document.

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

**Round 9: every exemption region receives the shared enforcement scan.** The
eighth review found that the `non-authoritative example` contract covered
illustrative *shape* only and never reached the shared clause scanner, and it
executed seven distinct bypasses through that hole. The following now hold for
**every** reason, with no per-reason exception:

- Every exemption region, regardless of reason, is scanned with the **same**
  enforcement lexicon and the same clause scanner as ordinary prose.
- **Illustrative shape alone never exempts content.** A blockquote, a table
  row, or a two-column layout is not evidence that text is an example.
- Introducers are **immediately and structurally bound** to the region: the
  whole preceding non-blank, non-marker, non-fence line must itself be an
  approved introducer.
- A **generic or negated `example` token is insufficient**. `Example:`,
  `Not an example:`, `Example implementation:`, `Current example:`,
  `Production example:`, `Authoritative example:` and `Example requirement:`
  all authorize nothing. An unbound substring search for `example` is gone.
- **Label-column heuristics cannot authorize an exemption.** The permissive
  `<label><two spaces><text>` rule is deleted outright rather than narrowed;
  example content must now be an explicit quotation.
- A **current-enforcement claim cannot hide inside any reason type.** Text
  outside the quotation marks on every region line is scanned as ordinary
  authoritative prose.
- The exemption inventory is reported for **checked-in files and the live PR
  body separately**; no scope-qualified count is stated without saying which
  scope it covers.
- This remains a **deterministic lexical/structural guard**, not semantic
  English understanding.

**`truthful denial list` is retired (round 9).** Round 8 rewrote both real
denial regions as ordinary explicit negative prose, which the guard already
accepts with no exemption at all. The live PR body's surviving instance was
rewritten the same way in round 9. Nothing then needed the reason, so it was
removed from the allowed set together with its validator, its introducer
vocabulary and its positive fixtures, rather than retained for symmetry. The
allowed set is now exactly `quoted obsolete wording` and
`non-authoritative example`.

**Approved example introducers (closed set).** `Invalid example:`,
`Rejected example:`, `Non-authoritative example:`, `Hypothetical invalid
wording:`, `Example of wording that must not be treated as current behavior:`.
Headings, table rows, HTML comments, inline code and link targets are reduced
to nothing before matching, so none of them can introduce a region.
