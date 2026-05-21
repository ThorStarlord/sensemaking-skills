# Session-Scoped Artifact Isolation

**Date**: 2026-05-21
**Status**: Approved

## Problem

`_resolve_artifact_path()` resolves step artifacts to flat paths like `artifacts/repository_sensemaking_brief.md`. When a prior workflow run fails partway through, these files linger with stale content. The next run reads the stale file and fails validation (e.g., the `MISSING_EVIDENCE_EXCERPTS` error we hit).

## Solution

Route all step artifacts into the session's numbered run directory, mirroring what `_create_user_intent_artifact` already does.

### Current behavior

```
artifacts/
├── plan_full-local-sensemaking.md
├── repository_sensemaking_brief.md
├── run_log_full-local-sensemaking_yolo_execution.md
└── ...
```

### Desired behavior

```
artifacts/
├── 05-orchestration-run/
│   ├── 00-user-intent.md
│   ├── plan_full-local-sensemaking.md
│   ├── repository_sensemaking_brief.md
│   ├── run_log_full-local-sensemaking_yolo_execution.md
│   └── ...
├── 06-orchestration-run/
│   └── ...
└── ...
```

## Change

Single method: `_resolve_artifact_path()`. When a numbered run directory exists (set by `_create_user_intent_artifact`), all artifact paths are prefixed with it.

**Algorithm**:
1. `_create_user_intent_artifact` already creates `artifacts/NN-orchestration-run/` and stores the path in `self.intent_path`
2. Extract the session directory from `self.intent_path` (its parent directory)
3. In `_resolve_artifact_path`, instead of returning `artifacts/<artifact-id>.md`, return `artifacts/NN-orchestration-run/<artifact-id>.md`
4. Contract-based paths (from `artifact-contracts.yaml`) that use `{session_id}` already work; for those without `{session_id}`, prepend the session directory

### Methods affected

| Method | Change |
|--------|--------|
| `_resolve_artifact_path()` | Prepend session run dir to all non-template paths |
| `_create_user_intent_artifact()` | Already correct — no change |
| `generate_plan()` | Uses `self.plan_out` which defaults to `artifacts/plan_*.md` — update default to session dir |
| `write_run_log()` | Uses `self.log_dir` — update default to session dir |
| All other artifact readers/writers | Use `_resolve_artifact_path()` — no direct change needed |

### No contract changes

`artifact-contracts.yaml` paths remain unchanged. The session-scoping happens in the resolver, not the contract. Downstream consumers (validators, auto-invocation) receive the correct session-scoped path.

## Edge cases

| Case | Handling |
|--------|----------|
| No session dir yet (pre-intent) | `_resolve_artifact_path` falls back to flat `artifacts/<id>.md` |
| Chained workflows | Child workflow creates its own session dir — isolated from parent |
| Resume mode | Resume log is written to the same session dir as the original run |

## Risks

- **Run logs still go to `self.log_dir`** — must be updated to use session dir, so the run log is co-located with its artifacts
- **Diagnostic/implementation reports** are also written to `self.log_dir` — same treatment
- **Existing flat files in `artifacts/`** are orphaned but harmless; they will be ignored in favor of session-scoped copies
