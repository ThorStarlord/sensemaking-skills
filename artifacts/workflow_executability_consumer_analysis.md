# Workflow Executability / Compatibility-Liveness Analysis

## 1. Scope

- **Repository**: `ThorStarlord/sensemaking-skills`
- **Pinned revision**: `d72d23454f9b21eb0db6f9176a387ce3dee4bb05`
- **Source finding**: Run 2 T3 in `artifacts/domain_alignment_report_run2.md`
- **Prior reconciliation**: `artifacts/reconciliation_report.md` correctly disputes the original `CONTEXT.md` taxonomy framing and reframes the remaining question as workflow executability / compatibility-liveness.
- **Question**: Are workflows that reference proposed/deprecated Skills merely preserved historical records, or are current planning/validation surfaces presenting them as executable workflow definitions?
- **Non-goal**: This analysis does not choose whether to retire workflows, replace steps, restore old capabilities, or add a workflow lifecycle schema.

## 2. Definitions Used in This Analysis

This report distinguishes four different claims:

1. **registered** — an ID exists in `workflow-registry.yaml` or `skill-registry.yaml`;
2. **selectable/plannable** — current planner/runtime machinery accepts the workflow ID and can materialize its steps into a plan;
3. **locally implementable Skill** — a `local_execution` step names a current installed Skill implementation rather than a proposed/deprecated historical registry entry;
4. **execution authorized** — a user/agent has separately selected and authorized execution under the agent-native control model.

These are not interchangeable. In particular:

```text
registered != locally implementable
selectable != executable end-to-end
plan-valid != capability-live
recommendation != execution authorization
```

## 3. Skill-Lifecycle Evidence

`skills/workflow-planner/references/skill-registry.yaml` explicitly records:

- `triage`: `status: proposed`; status note says it is referenced by the current operating workflow but **not yet implemented**;
- `tdd`: `status: deprecated`; status note says there is **no implementation under `skills/`** and it is retained so historical registry/workflow/validator references keep reconciling;
- `ui-brief`, `ui-flow`, `ui-screen-spec`: `status: deprecated`, no implementation under `skills/`;
- multiple product-management Skills (`persona`, `discovery`, `opportunity-tree`, `hypothesis`, `prd`, `user-stories`, `acceptance-criteria`, and others) are also explicitly `deprecated` with the same no-current-implementation note.

For these entries, availability metadata still says:

```yaml
availability:
  type: local_command
  executable_by_orchestrator: true
  requires_installed_skill: true
```

Thus the registry itself distinguishes lifecycle state from availability metadata, but the fields currently disagree about present liveness for proposed/deprecated entries.

Direct path checks at the pinned revision confirm that `skills/triage/SKILL.md` and `skills/tdd/SKILL.md` do not exist, consistent with their lifecycle notes.

## 4. Current Workflow Blast Radius

The canonical `skills/workflow-planner/references/workflow-registry.yaml` contains **eight current workflow definitions with at least one `local_execution` step whose Skill is proposed or deprecated**.

| Workflow | Locally-declared non-live dependency evidence |
| --- | --- |
| `product-to-issues` | `triage` (`proposed`) |
| `product-autonomous-sprint` | `persona`, `discovery`, `opportunity-tree`, `hypothesis`, `prd`, `user-stories`, `acceptance-criteria` (`deprecated`) |
| `experimental-autonomous-sprint` | `triage` (`proposed`), `tdd` (`deprecated`) |
| `implementation-workflow` | `triage` (`proposed`), `tdd` (`deprecated`) |
| `product-implementation-workflow` | `discovery`, `opportunity-tree`, `tdd` (`deprecated`) plus `triage` (`proposed`) |
| `ui-diagnostic-workflow` | `ui-brief` (`deprecated`) |
| `ui-implementation-workflow` | `ui-flow`, `ui-screen-spec`, `tdd` (`deprecated`) plus `triage` (`proposed`) |
| `architecture-implementation-workflow` | `triage` (`proposed`), `tdd` (`deprecated`) |

This is not the same issue as `external_routing` steps in `product-discovery-sprint` / `product-strategy-sprint`: those steps explicitly delegate outward and therefore do not make the same claim of local executability. They remain separate compatibility/product questions.

The installed-package registry at `src/sensemaking_skills/defaults/workflow-registry.yaml` also contains affected implementation definitions (including `implementation-workflow`, `product-implementation-workflow`, `ui-diagnostic-workflow`, and `ui-implementation-workflow`), so the liveness ambiguity is not confined to self-dogfood documentation.

## 5. Why Current Validation Does Not Catch This

### 5.1 Repository validator

`scripts/validate-repo.py` validates Skill availability structurally:

- availability type must be one of `local`, `local_command`, `external`, `prompt_only`;
- `local_command` must have an invocation command;
- a workflow step marked `local_execution` must point at a Skill whose availability type is `local` or `local_command`.

It does **not** enforce:

- `status != proposed`;
- `status != deprecated`;
- `requires_installed_skill: true` implies a current Skill implementation exists;
- a `skills/<skill-id>/SKILL.md` implementation exists before `local_execution` is accepted.

Consequently a deprecated/no-implementation Skill can remain mechanically acceptable as `local_execution` because its stale availability block still says `local_command`.

### 5.2 Plan validator

`scripts/validate-plan.py`:

- accepts `chosen_workflow_id` when it exists in the workflow registry;
- checks that plan steps match registry steps;
- checks that the referenced Skill exists in the Skill registry and is contracted to the output artifact.

It does **not** interpret Skill lifecycle status or verify installed implementation presence. A plan can therefore be structurally valid while faithfully reproducing a workflow whose local step has no live Skill implementation.

### 5.3 No demonstrated workflow-lifecycle filter

The affected workflow definitions expose execution modes and steps, but no currently enforced workflow-level lifecycle field analogous to the Skill registry's `status: proposed|deprecated` was found in the planning/validation path. Current `WorkflowRegistry`/planner behavior treats registry membership as sufficient for discovery/selection.

Adding workflow lifecycle metadata plus planner/validator filtering would therefore be a **new contract behavior**, not a mechanical use of an already-ratified field.

## 6. Current Selection / Planning Surfaces

This liveness mismatch is operationally relevant even though recommendation is not execution authority.

### 6.1 `workflow-planner` Skill

`skills/workflow-planner/SKILL.md` explicitly presents registered implementation workflows as planning choices:

- product fog -> consider `product-implementation-workflow`;
- UI fog -> consider `ui-implementation-workflow`;
- docs fog -> consider `docs-implementation-workflow`;
- architecture fog -> consider `implementation-workflow` with architecture focus;
- unclassified -> default recommendation `implementation-workflow`.

The Skill correctly states that the active agent/user makes the final selection and that recommendation does not authorize execution. But that authority separation does not answer whether the selected workflow definition is capability-live.

### 6.2 Deterministic planner/runtime

`scripts/workflow-planner.py` and `scripts/workflow-runtime.py` contain fog-to-workflow mappings that point to implementation workflows. Runtime planning/finalization accepts registry membership and mirrors selected registry steps into the orchestration plan; it does not perform a lifecycle/liveness filter first.

Therefore a current agent can receive a registry-grounded, validator-conformant plan containing `local_execution` steps for proposed/deprecated/no-implementation Skills.

### 6.3 Runtime-retirement nuance

ADR 0013's programmatic-runner retirement removed the model-spawning execution responsibility from the retained Python runtime. The retained executors are primarily dry-run/prompt-chain compatibility machinery; the active coding agent owns actual top-level execution.

That reduces the claim that Python itself can autonomously run these steps, but it does **not** make the workflow definition harmless historical prose. The workflow is still a current planning subgraph offered to the active agent, and `local_execution` still communicates that the selected responsibility has a local Skill implementation.

## 7. Candidate Repair Strategies

The evidence establishes the mismatch but does not select a product policy.

### Option A — retire/prune affected workflows

Remove them from current recommendation/selection surfaces or preserve them only in historical documentation.

**Tradeoff**: smallest conceptual model if the workflows are no longer product capabilities, but removes previously advertised workflow IDs and can affect compatibility/artifact history.

### Option B — replace non-live steps with current capabilities

Redesign each affected workflow around currently implemented Skills / direct ordinary coding responsibilities.

**Tradeoff**: preserves workflow purposes, but this is product/workflow redesign; a one-for-one replacement is not established by current evidence.

### Option C — implement/revive missing Skills

Implement `triage` and/or other missing capabilities.

**Tradeoff**: `triage` is still only proposed and `tdd` is explicitly deprecated. Reintroducing `tdd` as current capability would reverse an existing lifecycle disposition and cannot be inferred from registry references alone.

### Option D — introduce workflow lifecycle/liveness semantics

Add an explicit workflow state such as active / compatibility-only / retired and make planners/validators exclude non-active workflows from current recommendation while preserving historical IDs.

**Tradeoff**: cleanly separates provenance from current liveness, but introduces a new registry contract and filtering behavior that is not presently ratified.

### Option E — narrow validator repair only

Teach validators to reject `local_execution` steps when the Skill is proposed/deprecated or when `requires_installed_skill: true` cannot be satisfied.

**Tradeoff**: exposes the problem earlier but would immediately make several currently registered workflows invalid without deciding their intended replacement/retirement. It is therefore not a complete safe repair by itself.

## 8. Disposition

```text
C3_EXECUTABILITY_ANALYSIS = COMPLETE
REGISTERED_WORKFLOW_LIVENESS_MISMATCH = CONFIRMED
AFFECTED_LOCAL_EXECUTION_WORKFLOWS = 8
SKILL_LIFECYCLE_METADATA_EXISTS = YES
WORKFLOW_LIFECYCLE_FILTER_EXISTS = NO_DEMONSTRATED_CURRENT_FILTER
VALIDATE_REPO_LIVENESS_BLIND_SPOT = CONFIRMED
VALIDATE_PLAN_LIVENESS_BLIND_SPOT = CONFIRMED
PACKAGED_WORKFLOW_SURFACE_AFFECTED = YES
MECHANICAL_REPAIR_FROM_CURRENT_AUTHORITY = NO
OWNER_PRODUCT_DECISION_REQUIRED = YES
```

The original Run 1 label "ghost/deprecated consumers" was directionally useful but imprecise. The durable problem is:

> Current workflow-selection and validation surfaces can present a workflow as a valid `local_execution` subgraph even when one or more of its required Skills are explicitly proposed/deprecated and have no current installed implementation.

## 9. Recommended Next Responsibility

Do **not** restore `tdd`, implement `triage`, delete implementation workflows, or invent workflow lifecycle fields as an incidental cleanup.

The next responsibility is an explicit product/architecture decision choosing what **registered workflow** is supposed to mean after ADR 0013:

1. **current selectable capability only**, in which case non-live workflows must leave current selection surfaces; or
2. **current + compatibility/historical catalog**, in which case the registry needs an explicit lifecycle/liveness distinction that planners and validators honor.

Only after that decision is ratified can the smallest safe implementation repair be selected.
