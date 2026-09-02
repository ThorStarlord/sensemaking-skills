# ADR 0028: Implicit `SkillsOrchestrator` execution-mode selection is deprecated

**Status:** Accepted  
**Date:** 2026-09-01  
**Decision source:** issue #264, Option A explicitly owner-ratified  
**Evidence:** `artifacts/yolo_execution_default_consumer_analysis.md`

## Context

`SkillsOrchestrator.run_workflow` is a public Python compatibility surface. Its implemented omitted-argument behavior has historically selected `yolo_execution`, while the current architecture no longer treats that implicit choice as a stable product default. Repository analysis found no active in-repository production caller that depends on omission, but unknown external callers cannot be ruled out at a public package boundary.

A silent default change would therefore be a compatibility break without a release boundary.

## Decision

Retain the public wrapper for compatibility and deprecate **implicit execution-mode selection** before any future breaking change.

During this deprecation stage:

- callers may continue to call `run_workflow` without `execution_mode`;
- omission preserves the current observable fallback to `yolo_execution`;
- omission emits a clear `FutureWarning` requiring callers to choose a mode explicitly;
- explicit `yolo_execution` remains available and does not emit the omission warning;
- other explicit execution modes remain unchanged;
- public API documentation must require explicit mode selection and must not present any implicit mode as a stable current-product default.

This is a compatibility-preserving migration step, not a new default-selection policy.

## Non-decisions

This ADR does **not**:

- change the omitted-mode fallback to `guided_execution`;
- change it to `plan_only`;
- remove `SkillsOrchestrator.run_workflow`;
- remove `yolo_execution`;
- require explicit mode immediately;
- change the package version;
- define the later breaking-release version or the eventual replacement/default behavior.

Those decisions require a separate release decision after an appropriate deprecation window.

## Verification

The implementation must prove that:

1. omission emits exactly the deprecation signal and still passes `yolo_execution` to the retained runtime;
2. explicit `yolo_execution` emits no omission warning;
3. another explicit mode emits no omission warning and is forwarded unchanged;
4. the internal parent-session path remains explicit about `yolo_execution` and therefore does not rely on omission;
5. public API documentation no longer teaches an implicit execution-mode default.
