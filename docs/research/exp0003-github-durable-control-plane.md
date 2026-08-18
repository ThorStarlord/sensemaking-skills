# EXP-0003 research design: GitHub-durable connector-native control plane

**Issue:** #191  
**Status:** Phase A implementation candidate  
**Classification:** `EXPLORATORY_NOT_CANONICAL_EVIDENCE`

## 1. Why this experiment exists

EXP-0002 established the repository-side two-lane control model and reached a bounded approved state, but its final empirical execution history could not be reconstructed because authoritative reservation/invocation state could have existed only on the Windows executor host before publication to GitHub.

EXP-0003 does not retry EXP-0002. It tests a successor architecture in which **GitHub is the only authoritative durable campaign-state surface**. The current connected coding agent is allowed to be ephemeral: losing the workspace may lose compute, but it must not erase or obscure whether an attempt was reserved, invoked, produced output, or reached a terminal state.

## 2. Hypothesis

A bounded multi-attempt `coding_agent_native` campaign can execute through the connected GitHub workspace while preserving:

- durable pre-invocation reservation;
- fail-closed attempt and concurrency limits;
- exact target/framework/configuration identity;
- complete visibility of failed/interrupted attempts;
- no hidden retry, repair, fallback, target mutation, or automatic merge;
- exact-head deterministic validation;
- independent auditability from GitHub alone.

The hypothesis is falsified if a campaign interruption can leave two materially different execution histories that are indistinguishable from GitHub.

## 3. What changes from EXP-0002

### Removed deployment assumptions

EXP-0003 requires none of the following:

- Windows;
- Task Scheduler;
- a persistent `H:\...` checkout;
- executor-local attempt directories;
- executor-local logs as authoritative evidence;
- process inspection to determine whether a hidden attempt exists.

### Retained governance invariants

- Lane B / Gate A remains unchanged.
- Results remain `EXPLORATORY_NOT_CANONICAL_EVIDENCE`.
- Target mutation is prohibited.
- External provider API use is prohibited for this campaign type.
- Fallback, repair, hidden retry, and automatic merge are prohibited.
- Reservations consume attempt slots according to the existing campaign-accounting semantics.
- Concurrency is one for `github_results_branch_v1`.
- The canonical Phase-4 attempt-state vocabulary is reused unchanged:
  `RESERVED`, `ABORTED_BEFORE_INVOCATION`, `INVOKED`, `PROVIDER_FAILED`,
  `OUTPUT_CAPTURED`, `VALIDATION_FAILED`, `VALIDATION_PASSED`.

`PROVIDER_FAILED` is retained as compatibility vocabulary for the existing two-lane state machine; in a `coding_agent_native`/external-provider-prohibited campaign it means the attempt's execution failed after the invocation boundary, not that an external provider API was called.

## 4. Authority surfaces

### GitHub is authoritative for durable state

The results branch contains one complete state document plus attempt artifacts. Git commit history is the durability mechanism.

The state document is validated by
`src/sensemaking_skills/campaign_validation/github_durable.py`.

### The ChatGPT workspace is an ephemeral executor

The workspace may:

- read the frozen framework/skill revision through the GitHub connector;
- read the exact pinned target SHA through the GitHub connector;
- produce the requested diagnostic artifact;
- write campaign state/artifacts through the GitHub connector.

The workspace is **not** authoritative for whether a reservation or invocation occurred. If a state transition was not durably committed, it does not count as durable campaign state.

### GitHub Actions is the deterministic validator

Artifact validation runs against an exact GitHub head. The validation terminal state records both the exact validated head and the workflow run id.

## 5. Required durable ordering

For every attempt:

```text
commit RESERVED
    -> commit INVOKED
    -> first experiment-scoped target read
    -> commit OUTPUT_CAPTURED + artifact
    -> exact-head GitHub Actions validation
    -> commit VALIDATION_PASSED or VALIDATION_FAILED
```

The invocation boundary is explicitly:

```text
before_first_experiment_scoped_target_read
```

This is an execution-accounting boundary, not a statement about when the ChatGPT session itself started.

## 6. Results branch and PR lifecycle

Before attempt 1:

1. Create an isolated results branch.
2. Create the campaign state document with zero attempts.
3. Open a **draft results PR**.
4. Record the PR number and results branch in the state document.
5. Validate the empty campaign state.

The draft PR therefore exists throughout execution instead of appearing only after the campaign finishes.

No results PR may be merged automatically. Final merge, if ever appropriate, remains a separate human integration decision after independent audit.

## 7. State contract v1

A `github_results_branch_v1` state document is closed-schema and contains:

```yaml
state_schema_version: "1"
campaign_id: "EXP-0003-stage1-auteur-github-connector-pilot"
classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
execution_mode: "coding_agent_native"
execution_surface: "github_connector"
durability_backend: "github_results_branch_v1"
validation_backend: "github_actions_exact_head"
invocation_boundary: "before_first_experiment_scoped_target_read"
results_branch: "experiment/exp-0003-results"
results_pr_number: 123

target_repository: "https://github.com/ThorStarlord/auteur.git"
target_sha: "<40-hex pinned SHA>"
framework_sha: "<40-hex merged framework SHA>"
configuration_id: "<64-hex configuration id>"

max_attempt_slots: 3
concurrency_ceiling: 1
external_provider_api_prohibited: true
target_mutation_prohibited: true
fallback_prohibited: true
repair_prohibited: true
automatic_merge_prohibited: true

attempts: []
```

Unknown fields fail closed in contract v1.

## 8. Attempt contract

Each attempt records the current state plus the exact commit SHA for every durable transition:

```yaml
attempt_id: "attempt-001"
configuration_id: "<campaign configuration id>"
state: "VALIDATION_PASSED"
state_history:
  - state: "RESERVED"
    commit_sha: "<40-hex>"
  - state: "INVOKED"
    commit_sha: "<40-hex>"
  - state: "OUTPUT_CAPTURED"
    commit_sha: "<40-hex>"
  - state: "VALIDATION_PASSED"
    commit_sha: "<40-hex>"
reserved_commit_sha: "<RESERVED commit>"
invoked_commit_sha: "<INVOKED commit>"
output_commit_sha: "<OUTPUT_CAPTURED commit>"
artifact_path: "experiments/results/<campaign>/attempts/attempt-001/repository-sensemaking-brief.md"
validation_head_sha: "<OUTPUT_CAPTURED commit>"
validation_run_id: 123456789
terminal_reason: null
```

The validator requires transition commit SHAs to be unique across campaign history. Validation must be bound to the exact `OUTPUT_CAPTURED` head.

## 9. Crash/interruption semantics

### Before `RESERVED`

Nothing has been consumed. Another workspace may safely begin the attempt protocol.

### After `RESERVED`, before `INVOKED`

The slot exists permanently. Recovery must transition it to
`ABORTED_BEFORE_INVOCATION` or continue that same attempt to `INVOKED`; it may not silently delete the reservation.

### After `INVOKED`, before output preservation

The invocation is permanently known to have occurred. Recovery must not replay it as if it never happened. If no output can be recovered, the attempt terminates through the existing post-invocation failure path and the slot remains consumed.

### After `OUTPUT_CAPTURED`, before validation terminalization

The artifact is already durable. Recovery validates that exact preserved head; it does not rerun the analysis.

## 10. Exact-head validation

The existing `phase2-campaign-validation` GitHub Actions job runs the entire
`tests/campaign_validation` directory on Python 3.11 and 3.12 at the exact PR head. The Phase-A adapter test suite therefore enters the existing validator ecosystem without changing the workflow definition.

During a real EXP-0003 attempt, artifact-specific validation will also run against the exact `OUTPUT_CAPTURED` head. The terminal state records the workflow run id and requires `validation_head_sha == output_commit_sha`.

## 11. Phase A scope

This Phase-A PR may add only:

- this research/design document;
- the pure GitHub-durable state validator;
- tests for that validator.

It must not:

- create an operative EXP-0003 policy/approval;
- reserve or invoke any attempt;
- modify EXP-0002;
- modify Lane B / Gate A behavior;
- add a universal readiness gate;
- add a deterministic workflow router;
- modify the target repository.

## 12. Phase B after Phase A merges

After Phase A is independently reviewed and merged:

1. use the merge commit as the new frozen framework SHA;
2. prepare `EXP-0003-stage1-auteur-github-connector-pilot` against the exact pinned Auteur target SHA;
3. compute/freeze the new configuration id and policy digest using the canonical Two-Lane v1 digest rules;
4. choose a bounded validity window;
5. present the complete envelope in the active conversation;
6. require a **new standalone `approve`** after that presentation.

Agreement to this design or authorization to prepare it is not campaign approval.

## 13. Falsification criteria

EXP-0003 should be reported as unsupported/inconclusive if any of the following occurs:

- GitHub cannot distinguish whether an attempt crossed the invocation boundary;
- a reserved attempt can disappear from durable history;
- a new attempt can be created while another remains non-terminal under concurrency one;
- validation cannot be tied to the exact preserved artifact head;
- an interruption requires machine-local evidence to reconstruct campaign state;
- target identity or framework/configuration identity cannot be proven from GitHub;
- a hidden retry/repair is needed to obtain a reportable result.

Success means the complete campaign can be independently reconstructed and audited from GitHub alone, including its failures.