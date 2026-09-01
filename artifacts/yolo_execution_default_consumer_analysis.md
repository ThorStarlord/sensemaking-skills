# `yolo_execution` Default Consumer Analysis

## 1. Scope

- **Repository**: `ThorStarlord/sensemaking-skills`
- **Pinned revision**: `bc9b429c12a60722ec8c1d66a0ce2440ce512082`
- **Source finding**: Run 2 T4 in `artifacts/domain_alignment_report_run2.md`
- **Question**: Before changing `SkillsOrchestrator.run_workflow(... execution_mode="yolo_execution")`, determine who relies on the omitted-argument default, whether changing it is a compatibility break, and what migration boundary is warranted.
- **Non-goal**: This analysis does not authorize a runtime default change.

## 2. Current Authority and Runtime State

### 2.1 Canonical execution-mode vocabulary

`docs/canonical-vocabulary.yaml` marks:

- `guided_execution` as the canonical default execution mode;
- `yolo_execution` as `compatibility_only: true`, with a status note that it is legacy compatibility behavior after programmatic-runner retirement.

This is evidence that `yolo_execution` must not be treated as newly ratified product behavior merely because a compatibility wrapper still contains that default.

### 2.2 Deterministic runtime default is already `plan_only`

`docs/2026-08-programmatic-runner-retirement-plan.md` records the post-retirement default-pair repair:

- `workflow-runtime.py --mode` changed from `yolo_execution` to `plan_only`;
- `plan_only` was selected because it is allowed for every retained workflow, requires no model executor, and matches ADR 0013's CLI-as-planning/compatibility role;
- the programmatic runner retirement project is recorded as closed.

`scripts/workflow-runtime.py` currently exposes `--mode` with `default="plan_only"`.

Therefore the stale Python-wrapper default is not the default of the retained deterministic runtime itself.

### 2.3 Other active entrypoints do not default to yolo

Repository search shows:

- `scripts/workflow-runner-agent.py`: `--mode` defaults to `guided_execution`;
- `scripts/portfolio-orchestrator.py`: `--mode` defaults to `guided_execution`;
- `scripts/run-ledger.py`: mode is required for run creation;
- the installed `sensemaking-skills` CLI in `src/sensemaking_skills/cli.py` does not expose a command that calls `SkillsOrchestrator.run_workflow` at all; its current user-facing role is validation/setup support for the agent-native architecture.

## 3. `SkillsOrchestrator` Consumer Inventory

### 3.1 Implementation

`src/sensemaking_skills/runner.py` currently declares:

```python
def run_workflow(
    self,
    workflow_id: str,
    execution_mode: str = "yolo_execution",
    ...
) -> int:
```

The method always forwards the resolved mode explicitly to `workflow-runtime.py` as `--mode <execution_mode>`.

The same module has one internal execution call in `_run_workflow_with_parent_session(...)`, and that call passes `execution_mode="yolo_execution"` **explicitly**. Changing the public method's omitted-argument default would therefore not change this internal manual parent-session path.

### 3.2 In-repository call sites

A repository-wide search for `run_workflow(` / `orchestrator.run_workflow` finds no active production call site that executes `SkillsOrchestrator.run_workflow` while omitting `execution_mode`.

The visible call surfaces are:

- `API.md` examples, which pass `guided_execution` or `autonomous_execution` explicitly;
- `tests/test_auto_invocation_target_repo.py`, which replaces `run_workflow` with a test double to prove no unauthorized child workflow is spawned; it does not establish reliance on the implementation default;
- the explicit internal parent-session invocation described above.

**Repository conclusion**: no in-repository behavioral dependency on the omitted-argument `yolo_execution` default was found.

### 3.3 Public API documentation disagrees with implementation

`API.md` presents `SkillsOrchestrator` as a programmatic Python API and documents its signature as:

```python
execution_mode: str = "guided_execution"
```

All runnable examples in that API reference pass an execution mode explicitly.

Thus the repository currently has three distinct statements:

1. canonical vocabulary: `guided_execution` is the default; `yolo_execution` is compatibility-only;
2. retained deterministic runtime: no-argument CLI default is `plan_only` after ADR 0013 retirement;
3. Python compatibility wrapper implementation: omitted argument becomes `yolo_execution`.

The third statement is the outlier.

## 4. External Consumer Boundary

The project is a distributable Python package (`pyproject.toml`, package version 0.2.2 in source) and `API.md` explicitly advertises programmatic use through `sensemaking_skills.runner.SkillsOrchestrator`.

Current public package evidence checked on **2026-09-01**:

- PyPI project: `https://pypi.org/project/sensemaking-skills/`
- latest published release visible there: **0.2.1** (2026-05-26)
- the repository's source version 0.2.2 is therefore not the only relevant compatibility boundary; already-installed 0.2.1/source users may exist outside this repository.

The repository cannot enumerate those external callers. Consequently:

> `no in-repo omitted-mode caller found` does **not** prove `no omitted-mode caller exists`.

Changing the wrapper default silently would alter observable behavior for any external caller that currently invokes `run_workflow(workflow_id)` without `execution_mode`.

## 5. Breaking-Change Analysis

### Option A — silently change wrapper default to `guided_execution`

**Not warranted now.**

It would align with `API.md` and canonical vocabulary, but it changes actual behavior for any omitted-mode caller and may select an execution mode whose operational role differs from the deterministic runtime's post-retirement `plan_only` default.

### Option B — silently change wrapper default to `plan_only`

**Not warranted now.**

This best matches the retained deterministic runtime and ADR 0013 retirement mechanics, but it is still an observable behavior change for external omitted-mode callers.

### Option C — remove the default and require `execution_mode`

**Architecturally clean but immediately breaking.**

It would eliminate ambiguous implicit authority, but existing omitted-mode calls would fail instead of preserving compatibility.

### Option D — staged deprecation while preserving current fallback

**Smallest plausible migration path if the wrapper remains public.**

A future owner-authorized change could:

1. detect omission separately from explicit `yolo_execution`;
2. preserve the current compatibility fallback during the deprecation window;
3. emit an explicit deprecation warning requiring callers to choose a mode;
4. update `API.md` so examples and signature no longer imply that an implicit execution choice is stable product behavior;
5. in a separately versioned breaking change, either require an explicit mode or adopt the then-ratified safe default.

This preserves behavior while making the compatibility debt observable.

### Option E — retire the Python workflow-execution wrapper

**Also plausible, but broader than C4.**

ADR 0013 and the retirement plan make the active coding agent the primary execution model. If `SkillsOrchestrator.run_workflow` has no continuing product use case, retiring rather than modernizing this compatibility wrapper may be preferable. That requires an explicit product/release decision and is not implied by this consumer scan alone.

## 6. Disposition

```text
C4_CONSUMER_ANALYSIS = COMPLETE
IN_REPO_OMITTED_MODE_DEPENDENCY = NONE_FOUND
INTERNAL_PARENT_SESSION_DEPENDENCY = EXPLICIT_YOLO_ONLY
ACTIVE_RUNTIME_DEFAULT = PLAN_ONLY
OTHER_ACTIVE_ENTRYPOINT_DEFAULTS = GUIDED_OR_REQUIRED
PUBLIC_API_DOCUMENTED_DEFAULT = GUIDED_EXECUTION
PYTHON_WRAPPER_IMPLEMENTED_DEFAULT = YOLO_EXECUTION_COMPATIBILITY_ONLY
EXTERNAL_OMITTED_MODE_DEPENDENCY = UNKNOWN_AND_NOT_ENUMERABLE_FROM_REPO
SILENT_DEFAULT_CHANGE_NOW = NOT_WARRANTED
OWNER_RELEASE_DECISION_REQUIRED = YES
```

C4 is no longer blocked on **consumer discovery**. The remaining uncertainty is a **product/release compatibility decision**:

> Is `SkillsOrchestrator.run_workflow` still a supported public execution surface worth migrating, or should it remain/retire as compatibility infrastructure?

Until that decision is made, preserving the current behavior is safer than silently changing what omitted arguments do.

## 7. Recommended Next Responsibility

Do **not** patch `runner.py` merely because `yolo_execution` looks stale.

The next C4 responsibility, if pursued, is an owner/release-policy decision choosing between:

- **retain + staged deprecation** of implicit mode selection; or
- **retire** the compatibility wrapper as part of a separately scoped public-API change.

A direct `yolo_execution -> guided_execution` or `yolo_execution -> plan_only` default flip should not be merged as an ordinary mechanical repair.
