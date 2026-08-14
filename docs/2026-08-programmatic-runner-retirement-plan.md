# Programmatic Runner — Staged Retirement Plan

**Date**: 2026-08-13
**Status**: Step 3 (deprecate model executors) EXECUTED 2026-08-13; steps 4-8 pending.
**Authority**: ADR 0013 (Accepted 2026-08-13): the primary execution model is
agent-native — the active coding agent reads and executes Skills directly.
The programmatic second-model runner (`workflow-runtime.py` /
`skill_executor.py` model executors) is a separate automation/compatibility
path, not part of the semantic definition of Skill execution.

**Decision**: begin STAGED RETIREMENT of the programmatic model-invocation
responsibility. Do not delete anything during discovery. Do not fund the
credential-backed assurance run unless a concrete headless/second-model
product use case later demands it.

Retire because the responsibility is no longer needed by the ratified
architecture — NOT because the runner failed. It never failed behaviorally;
its product role was superseded.

## Discovery — consumers of the model-invocation path

- **Tests (30+)**: `tests/integration/test_yolo_execution_with_skills.py`,
  `test_autonomous_execution_integration.py`, `test_executor_environment.py`,
  `test_executor_path_handoff.py`, `test_artifact_permission_gate.py`,
  `test_gate_a_*`, `tests/support/deterministic_executor.py`, and many
  contract/path tests that exercise the runtime + executor machinery.
- **CI** (`.github/workflows/validation.yml`): installs
  `claude-agent-sdk==0.2.82` (3 places) and exercises `skill_executor.py`.
- **Docs (~40 files)**: operational (PHASE5_SKILL_INVOCATION,
  orchestration-patterns, workflow-output-system, TROUBLESHOOTING,
  DEPLOYMENT_GUIDE, orchestrator-skill-example) and historical (PHASE-*).
- **Scripts**: `brief_skeleton.py` (runtime-owned-skeleton prompt, built by
  the executor), `gate_a_authorization.py` (Gate A consumer).

## Responsibility classification

### workflow-runtime.py

| Responsibility | Classification | Note |
|---|---|---|
| Artifact resolution (session-scoped paths, ADR 0010) | **KEEP** | needed under agent-native; the deterministic layer still resolves paths |
| Validation dispatch | **KEEP** | deterministic validators are core |
| Gates / execution modes | **KEEP** | useful control points; may simplify under agent-native |
| Workflow planning (plan generation) | **KEEP** | the plan is a durable contract |
| Session handling / run ledger | **KEEP** | the evidence trail |
| Second-model invocation (executor selection + invoke_skill) | **RETIRE** | the model-spawning responsibility |

### skill_executor.py

| Responsibility | Classification | Note |
|---|---|---|
| `SkillExecutor` ABC + `DryRunSkillExecutor` + `PromptChainSkillExecutor` | **KEEP** | deterministic, agent-agnostic; prompt-chain is a useful handoff |
| `ClaudeAgentSdkSkillExecutor` (claude-code) | **RETIRE** | model invocation, Claude-specific |
| `api` executor | **RETIRE** | model invocation, Claude-specific |
| Permission-gate hooks / tool-call tracing tied to the SDK | **RETIRE WITH SDK EXECUTOR** | exist to confine the SDK's tool calls; the concepts (write confinement, trace) may be MOVE'd to a lighter agent-native form |
| `resolve_output_path` / `canonicalize_path` / `is_within_root` | **KEEP** | deterministic infra used by tests |
| `build_skeleton_prompt` (brief skeleton) | **MOVE** | to a standalone helper consumed by the agent-native path, not the SDK executor |

### Supporting consumers

| Consumer | Classification |
|---|---|
| CI `claude-agent-sdk` installs + SDK-invocation tests | **RETIRE** (with the SDK executor) |
| Deterministic runtime/executor tests | **KEEP** |
| Operational docs (PHASE5_SKILL_INVOCATION, orchestration-patterns, TROUBLESHOOTING, DEPLOYMENT_GUIDE, etc.) | **MOVE** (re-scope to agent-native; archive historical PHASE-* as-is) |

## Smallest migration sequence

1. Ratify ADR 0013 (DONE — `c29094d`).
2. Record this plan (DONE — this document).
3. **Deprecate**: mark the model executors + `--executor claude-code|api` as
   deprecated in code comments and docs; no behavior change.
4. **Move** the genuinely useful deterministic infra out of the executor
   (skeleton prompt, path helpers) so retirement loses nothing.
5. **Retire the SDK surface**: remove CI's `claude-agent-sdk` installs and the
   SDK-invocation tests; keep `DryRun`/`PromptChain` + deterministic infra.
6. **Re-scope docs**: operational docs to agent-native; archive historical
   runner-led docs.
7. **Final removal**: delete the SDK/api executors + the executor-selection
   path, leaving `workflow-runtime.py` as pure deterministic infrastructure
   (paths, validation, gates, planning, sessions) and `skill_executor.py` as
   the deterministic/prompt-chain adapter set.
8. Re-run the layering audit + full suite; verify ADR 0013 alignment.

Each step is an independent, verifiable slice. Nothing is deleted in this
document; the migration begins only on explicit approval of the sequence.

## Step 3 evidence (executed 2026-08-13)

- Deprecated (non-behavioral markers only): ClaudeAgentSdkSkillExecutor and
  ApiSkillExecutor class docstrings; --executor help text notes claude-code and
  api as DEPRECATED (retained for backward compatibility during staged
  retirement, ADR 0013).
- Preserved unmarked: SkillExecutor ABC, DryRunSkillExecutor,
  PromptChainSkillExecutor, path/artifact resolution, planning, gates,
  sessions/ledger, validators. The claude-code default is unchanged.
- Zero execution-semantics change: --executor choices unchanged
  (dry-run,prompt-chain,claude-code,api); no exit-code/gate/artifact/auth/
  selection change; no runtime warnings added outside help output.
- Verification: validate-repo PASS; validator harness 74/74; executor tests
  40 passed / 4 skipped / 8 failed - all 8 failures pre-existing in
  test_executor_environment.py (missing `tempfile` import; ANTHROPIC_BASE_URL
  present in the local contaminated .claude/settings.json), unrelated to this
  slice. Diff inspected: 4 files, +28/-16, no line-ending churn.

## CLI default-pair integrity check (post-Step-5, executed 2026-08-13)

- Check: `python scripts/workflow-runtime.py --workflow fast-path-workflow`
  (no --mode/--executor). Result before fix: INVALID - MODE_NOT_ALLOWED
  (default mode yolo_execution is not allowed for the default workflow) and,
  on workflows that do allow yolo, the yolo+dry-run pair silently skips
  execution (validate_mode is never called in the runtime; the
  supports_real_execution branch at workflow-runtime:915 is skipped).
- Repair (smallest coherent contract): default --mode yolo_execution ->
  plan_only (allowed for every retained workflow, requires no executor, matches
  ADR 0013's CLI-as-planning/compat role). --executor default dry-run (the
  runtime's normative __init__ default) retained.
- Result after fix: VALID - no-arg default invocation generates the plan
  (plan_only + dry-run). Retained tests 32 passed.

## Documentation reconciliation (post-retirement, executed 2026-08-13)

Three buckets, classified individually:
- CURRENT OPERATIONAL (agent-native banner added, runner content marked
  superseded): PHASE5_SKILL_INVOCATION, orchestration-patterns,
  orchestrator-skill-example, DEPLOYMENT_GUIDE, TROUBLESHOOTING,
  workflow-output-system, workflow-design-guide, validation-workflow.
- SUPERSEDED BUT HISTORICALLY USEFUL (HISTORICAL marker added, preserved):
  PHASE-1-ACCEPTANCE-VERIFIED, PHASE-1-GOLDEN-PATH,
  PHASE-1-IMPLEMENTATION-COMPLETE, PHASE-1-STATUS-SUMMARY, PHASE-80-81-CLOSURE,
  implementation-checklist, candidate/architecture-decision.
- ADRs: unchanged (historical decision records; ADR 0013 is current).
- Deferred to a follow-up pass: ROUTING_GUIDE, run-ledger-guide,
  PORTFOLIO_OPERATIONS, PRODUCT-CONTRACT-REVIEW (retained mechanics with
  incidental runner mentions - verify incidental references individually).

## Step 5 evidence (atomic removal, executed 2026-08-13)

- SDK dependency classified COUPLED_TO_RETAINED_RUNTIME (eager module-level
  `from claude_agent_sdk import ...` in skill_executor.py): removing the SDK
  without the executors would break imports of retained DryRun/PromptChain and
  workflow-runtime. So Steps 5-7 collapsed into one atomic cut.
- Removed: ClaudeAgentSdkSkillExecutor, ApiSkillExecutor, --executor
  claude-code|api, EXECUTOR_REGISTRY entries, the eager SDK import, the SDK
  permission-gate/PreToolUse machinery, tool-call trace hooks, model-runner
  prompt builders, duplicate path helpers, 14 SDK/API-specific test files, and
  3 CI claude-agent-sdk installs.
- Default-executor guardrail: --executor default changed claude-code ->
  dry-run (the runtime's normative __init__ default; no retained executor can
  run the default yolo mode, so a model default would be misleading). Choices
  now [dry-run, prompt-chain].
- Preserved: SkillExecutor ABC, DryRun, PromptChain, resolve_output_path,
  brief_skeleton (canonical-structure authority), runtime/gates/sessions/
  validators/artifact resolution.
- Proof: import skill_executor + workflow-runtime OK; DryRun/PromptChain +
  run-log + gate_a + path tests pass with the SDK reference removed (harness
  74/74; retained sweeps 98 + 309 passed; only pre-existing env failures
  remain - untracked 0016 file). --executor --help shows {dry-run,
  prompt-chain} default dry-run. grep: zero claude_agent_sdk references in
  scripts/, tests/, CI (the sole remaining reference is execution_infra/
  README.md documenting the separate exploratory_execution.ClaudeProvider,
  out of scope).

## Step 4 evidence (discovery-and-extraction, executed 2026-08-13)

Finding: NO MOVE is earned. Existing module boundaries already disentangle
retained deterministic infrastructure from the retiring surface.

| candidate responsibility | existing consumers | classification | rationale |
|---|---|---|---|
| resolve_output_path | DryRun/PromptChain (retained executors) + SDK/Api | KEEP_IN_PLACE | retained deterministic executor infra |
| canonicalize_path / is_within_root (skill_executor copies) | SDK permission gate + test_artifact_permission_gate only | RETIRE_WITH_RUNNER | canonical primitive already lives in sensemaking_skills.path_containment (retained via gate_a_authorization, ADR 0023); the skill_executor copies are duplicates |
| build_artifact_permission_gate + PreToolUse hooks | SDK executor + tests | RETIRE_WITH_RUNNER | exists to confine the SDK's tool calls |
| prompt builders (build_semantic_authorities_block, build_evidence_discipline_block, build_yaml_fence_contract_block, build_skeleton_prompt) | SDK executor prompt-building + tests | RETIRE_WITH_RUNNER | classification B: prompt scaffolding whose only purpose is preparing the deprecated second-model executor |
| brief_skeleton.py (standalone module) | deprecated executor (functional) + validate-brief/weakness_type_safeguard (canonical-structure references) | KEEP_IN_PLACE | already its own module; referenced as the canonical brief-structure authority; revisit at Step 7 |

Criterion applied: does a non-deprecated responsibility or consumer need this
capability independently of launching a second model? (No relocations made;
no new abstraction created; no behavior change.)

## Non-goals

- No deletion during discovery.
- No funding of the credential-backed runner assurance run unless a concrete
  headless/second-model use case appears.
- No Codex/Pi/Hermes adapters; no generalization of the runner to "look
  symmetric."
