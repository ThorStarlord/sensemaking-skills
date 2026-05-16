# PRD: First Automation Slice — YOLO Execution via Validator Ecosystem

## Problem Statement

The validator ecosystem (4 phases, 7 scripts, 42 passing test cases, full three-level hierarchy) is complete and verified. But it has never been used to gate an actual automated workflow execution. The safety layer exists but is untested in its primary use case: catching failures during a YOLO execution before they reach an external agent.

Without a live run, there are unvalidated assumptions:

- The pre-flight Level 1 validator catches real structural issues before mutation
- The post-step Level 2 + Level 3 sequence actually halts on a broken artifact
- The run log captures sufficient forensic data for rollback
- An end-to-end YOLO execution produces a valid `prompt_handoff` that passes all gates

## Solution

Execute the `fast-local-diagnostic` workflow in YOLO execution mode, using the full three-level validator hierarchy as zero-tolerance safety gates. This is the simplest possible end-to-end path (2 steps) that exercises every validator level and terminates in a `prompt_handoff` artifact.

The orchestrator SKILL.md already defines the YOLO protocol in detail. The validator scripts, artifact contracts, and workflow registry are already deployed on `main`. This PRD covers the first live execution: from clean worktree to validated `prompt_handoff` on a feature branch, with every validator invocation recorded.

## User Stories

1. As a **repository owner**, I want to run the first YOLO execution against the validator ecosystem, so that I can prove the safety gates work before relying on them for higher-risk automation.

2. As a **developer debugging the automation pipeline**, I want every validator invocation and its result recorded in a run log, so that I can trace exactly what passed and what failed.

3. As the **workflow-orchestrator agent**, I want clear pre-flight checks (clean worktree, feature branch, Level 1 structural validation), so that I never mutate a dirty or unprotected state.

4. As an **operator monitoring the execution**, I want zero-tolerance failure handling, so that a single broken artifact never silently propagates to the next step or to an external agent.

5. As the **orchestrator agent**, I want a rollback command emitted automatically on any validator failure, so that the workspace can be restored to its pre-execution state without manual analysis.

6. As a **contributor reviewing the results**, I want the produced `repository_sensemaking_brief` and `prompt_handoff` artifacts to pass all registered validators (Level 2 + Level 3), so that I can trust the automation produced valid output.

7. As a **future developer adding a new YOLO-eligible workflow**, I want the `fast-local-diagnostic` run to serve as a reference execution, so that I can follow the same pattern for other workflows.

8. As a **maintainer assessing system health**, I want the test suite (42 cases) to pass before the YOLO run begins, so that I know the validator layer itself is healthy before testing it in the live chain.

9. As an **operator**, I want the execution to stop immediately if a step produces no output artifact or produces one that doesn't match its contract, so that ghost artifacts never pollute the next step's context.

10. As a **safety reviewer**, I want the pre-flight to verify we are not on `main` or `master` before any mutation, so that YOLO execution never directly commits to a protected branch.

## Implementation Decisions

### Selected Workflow: `fast-local-diagnostic`

| Property | Value |
|---|---|
| Workflow ID | `fast-local-diagnostic` |
| Execution mode | `yolo_execution` |
| Number of steps | 2 |
| Step 1 | repo-sensemaker → `repository_sensemaking_brief` |
| Step 2 | handoff → `prompt_handoff` |
| Branch policy | `yolo/fast-local-diagnostic/{timestamp}` |
| Run log required | Yes |

**Rationale:** Minimal blast radius (2 steps), all-local skills (YOLO-eligible), exercises every validator level, produces the highest-blast-radius artifact (`prompt_handoff`, consumed by `external_agent`).

### Validator Execution Model

The orchestrator follows the chain defined in `validator-stack-policy.md` and `artifact-contracts.yaml`:

**Pre-flight:**
```
1. git status --porcelain must be empty
2. Current branch is NOT main/master
3. python scripts/validate-repo.py (exit 0 or halt)
```

**After Step 1 (repo-sensemaker → repository_sensemaking_brief):**
```
1. python scripts/validate-artifact.py repository_sensemaking_brief {path}  [Level 2]
2. python scripts/validate-brief.py {path}                                   [Level 3]
```
Any non-zero exit → hard stop.

**After Step 2 (handoff → prompt_handoff):**
```
1. python scripts/validate-artifact.py prompt_handoff {path}                 [Level 2]
2. python scripts/validate-prompt-handoff.py {path}                          [Level 3]
```
Any non-zero exit → hard stop.

**On any failure:**
1. Record full failure details in run_log.md
2. Stop execution loop
3. Recommend: `git reset --hard {PRE_YOLO_COMMIT}`

### Deep Modules

**Module 1: YOLO Pre-flight Check (orchestrator protocol step)**

Already defined in orchestrator SKILL.md. Encapsulates:
- Clean worktree verification
- Protected-branch guard
- Level 1 structural validation
- HEAD SHA capture for rollback target

This is a deep module: the interface is a single gate ("can we start YOLO?"), but it encapsulates git safety, structural integrity, and rollback targeting. It can be verified independently by running it against a clean vs. dirty worktree.

**Module 2: Post-Step Validator Chain (orchestrator protocol step)**

Already defined in orchestrator SKILL.md and artifact-contracts.yaml. Encapsulates:
- Level 2 generic validation per artifact contract
- Level 3 specialized validation per artifact contract
- Aggregate pass/fail across all registered validators

This is the deepest module: the orchestrator doesn't need to know which validators apply to which artifact — it looks up `artifact-contracts.yaml` and runs whatever is registered. The contract file is the interface.

**Module 3: Run Log Writer (orchestrator protocol step)**

Already templated in `references/run-log-template.md`. Encapsulates:
- Pre-flight block (commit SHA, branch, validator result)
- Per-step block (skill, artifact, validator results)
- Failure block (error details, rollback command)
- Success block (final state, artifact list)

### No New Code Required

All components are already on `main`:
- 7 validator scripts (Level 1 + Level 2 + 5 Level 3)
- Shared utility module (`_validator_utils.py`)
- Test suite (42/42 passing)
- Workflow registry (11 workflows, `fast-local-diagnostic` YOLO-eligible)
- Artifact contracts (22 types, `prompt_handoff` wired to both Level 2 and Level 3)
- REGRESSIONS.yaml (2 required regression cases)
- Orchestrator SKILL.md (defines YOLO protocol including pre-flight, post-step verification, rollback)

The "implementation" is execution of the existing protocol, not code changes.

### Scenarios: Go-Live and Rollback

**Happy path:**
Clean worktree → pre-flight passes → Step 1 produces brief → both validators pass → Step 2 produces handoff → both validators pass → feature branch exists with artifacts and run log → offered for PR review.

**Failure scenario (Step 1):**
Clean worktree → pre-flight passes → Step 1 produces brief → Level 2 validators pass → Level 3 validator fails (e.g., hallucinated workflow ID) → hard stop → rollback advised → forensic artifacts preserved on feature branch for analysis.

**Failure scenario (Step 2):**
...Step 1 succeeds → Step 2 produces handoff → Level 2 passes → Level 3 fails (e.g., unknown target skill) → hard stop → rollback advised.

## Testing Decisions

### What Makes a Good Test

The test suite (42 cases) already validates each validator in isolation using positive and negative fixtures. The YOLO execution does not need new validator tests — it needs a **live integration test** that proves the chain works end-to-end.

### What Gets Tested Live

The live run validates what fixture tests cannot:
- **Orchestrator compliance**: Does the orchestrator actually invoke validators between steps, or does it skip them?
- **Cross-step artifact flow**: Does the handoff step receive the brief in a format the validators accept?
- **Real registry lookups**: Registry data is real (not fixture data) — does `validate-brief.py` correctly find the workflow ID in the production registry?
- **File I/O under YOLO**: Do artifacts written by skills on a feature branch pass path-based checks?
- **Run log integrity**: Does the run log capture all validator invocations with correct exit codes?

### What Is NOT Tested

- **Validator unit behavior**: Already covered by 42 fixture tests. The live run does not re-test individual error codes.
- **Edge cases in failure handling**: The live run tests the happy path. Failure scenarios (rollback) are tested only if a validator actually fails.
- **External agent handoff**: The `prompt_handoff` artifact is validated but not actually passed to an `external_agent` — that's out of scope for this slice.

## Out of Scope

- **Building a new YOLO runner script.** The orchestrator SKILL.md is the execution engine. No separate CLI tool or script is needed.
- **Adding validators for other artifact types.** `prompt_handoff` is the only Level 3 addition. The other 17 artifact types remain at Level 2 only.
- **CI/CD integration.** No GitHub Actions or other CI changes. The YOLO run is agent-driven, not pipeline-driven.
- **External agent handoff.** The run produces a validated `prompt_handoff` but does not deliver it to an `external_agent`.
- **Merging the feature branch to `main`.** The branch is produced for review. Merging requires human approval outside this scope.
- **Modifying any validator behavior.** The run uses validators as-is. No behavioral changes, error code additions, or output format changes.
- **LLM self-review step.** The orchestrator SKILL.md mentions LLM-based post-step verification. This run uses only script-based validators (Level 2 + Level 3). The LLM review is advisory and out of scope for the first automation slice.

## Further Notes

- Pre-run prerequisite: `python scripts/test-validators.py` must pass (42/42) and `python scripts/validate-repo.py` must pass before starting. Both are verified as of 2026-05-16.
- The `fast-local-diagnostic` workflow does not declare `requires_clean_worktree: true` in the registry (unlike `full-local-sensemaking`). The orchestrator must enforce this manually per the SKILL.md YOLO protocol.
- The `handoff` skill in Step 2 produces `prompt_handoff` — this is the "handoff" skill (not "prompt-handoff"), but both produce the same artifact type. The contract captures both as producers.
- After successful execution: feature branch `yolo/fast-local-diagnostic/{timestamp}` exists with `run_log.md`, `repository_sensemaking_brief.md`, and `prompt_handoff.md`. All three artifacts are validated. The branch is available for PR.
- The term **automation slice** refers to a minimal end-to-end YOLO execution that exercises the full validator safety chain. It is not a persistent domain term — it describes this specific go-live event.
