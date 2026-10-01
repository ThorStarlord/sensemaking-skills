> **HISTORICAL (pre-ADR-0013, 2026-08)**: runner-led orchestration record,
> preserved as historical evidence. The ratified execution model is agent-native
> (ADR 0013); the programmatic second-model runner was retired.

# Phase 1 Candidate Expanded Product Architecture

**Status**: Candidate Architecture (Not Proven End-to-End)  
**Created**: 2026-07-23  
**Version**: 1.0 — DRAFT  
**Note**: This document describes a broader multi-stage architecture. It is NOT the first production milestone. See issue #28 for the narrow first proven path.

---

## Executive Summary

This document proposes a **candidate two-stage agent-native architecture** for future expansion. This is NOT the first production milestone.

The actual first production golden path is defined in issue #28:

1. **Diagnostic Phase** — Agent invokes skills to classify fog type and recommend an implementation workflow
2. **Implementation Phase** — System automatically invokes the recommended implementation workflow, which executes to completion

This golden path is **skill-driven, not script-driven**. Agents (in Claude Code, Cursor, OpenCode) own the control loop by invoking skills via the Skill tool. Artifacts are the contract; validators provide proof.

---

## Phase 1 Scope Definition

### What Phase 1 Includes

✅ **Core Entry Points** (Both routed automatically to implementation workflows):
- Fast path: `repo-sensemaker` → `workflow-planner` (for clear repository state)
- Full fog path: `problem-framer` → `unknowns-mapper` → `repo-sensemaker` → `workflow-planner` (for ambiguous problems)
- Default path (CLI): `full-local-sensemaking` workflow with conditional `discovery` step

✅ **Auto-Invocation Pipeline**:
- Diagnostic phase produces `workflow_orchestration_plan` with `primary_fog_type` and `recommended_workflow_id`
- Runtime automatically invokes implementation workflow matching the fog type
- No manual step selection required

✅ **Four Implementation Workflows** (Auto-Invoked Based on Fog Type):
- `product-implementation-workflow` (product_fog) → discovery → opportunity-tree → prd → issues → triage → tdd → handoff
- `ui-implementation-workflow` (ui_fog) → domain alignment → ui flows → screen specs → issues → triage → tdd → handoff
- `docs-implementation-workflow` (docs_fog) → domain alignment → prd → handoff
- `implementation-workflow` or `architecture-implementation-workflow` (architecture_fog) → domain alignment → prd → issues → triage → tdd → handoff

✅ **Artifact Validation**:
- Generic validators (`validate-artifact.py`) check structure and required fields for all artifacts
- Specialized validators enforce domain-specific rules
- Validators produce structured JSON output for agent parsing
- Validation results recorded in `run_log.md`, not in artifacts themselves (ADR 0004)

✅ **Human Gates**:
- Approval gates exist between steps (configurable per execution mode)
- In `yolo_execution`, gates are bypassed; validators act as safety mechanism
- In `guided_execution`, gates pause for human review before proceeding
- In `autonomous_execution`, gates are skipped but validators are non-negotiable

✅ **Agent-Native Bootstrap**:
- SessionStart hook injects `using-sensemaking` skill
- Agents learn fog classification, workflow routing, error parsing, retry logic
- Agents invoke skills conversationally and read artifacts to drive decisions

### What Phase 1 Excludes

❌ **Script-Driven Orchestration**:
- Legacy `workflow-runtime.py` invocations become compatibility layer only
- No direct Python script control over skill sequencing
- Agent reasoning + Skill tool is the primary path

❌ **Multi-Stage Manual Routing**:
- Agents don't manually select between implementation workflows
- `workflow-planner` automatically determines workflow based on fog type
- Auto-invocation is the default behavior (no approval gate before implementation workflow start)

❌ **External Routing in Phase 1**:
- Skills with `step_type: external_routing` (discovery, interview-synthesis, etc.) are not invoked directly by agents in diagnostic phase
- They are invoked BY the implementation workflows based on fog type
- Exception: `product-implementation-workflow` invokes discovery as part of its sequence

❌ **Handoff to Third-Party Systems**:
- Phase 1 stays within local repository context
- No integration with external project management, ticketing, or deployment systems
- Artifacts are local MD/JSON files, not synced to external platforms

❌ **Artifact Storage Outside Local Filesystem**:
- All artifacts are written to `artifacts/` directory
- No cloud storage, database persistence, or external artifact registry
- Run logs stay local in `runs/` directory

❌ **Real-Time Collaborative Editing**:
- Artifacts are created by skills in isolation
- No concurrent editing or real-time sync across agents
- Single-writer model (one skill owns artifact production)

---

## Canonical Golden Path: Step-by-Step

### Stage 1: Diagnostic Phase

**Goal**: Transform user intent + repository state into fog classification and implementation workflow recommendation.

```
┌─────────────────────────────────────────────────────────────────────┐
│ USER INTENT (artifact: user_intent.md)                              │
│ - Raw problem statement                                             │
│ - Scope mode (discovery/validation/delivery)                        │
│ - Constraints, non-goals                                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    [Agent receives intent]
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
   ╔═══════════════════════════════════╗  ╔═══════════════════════════╗
   │ FAST PATH                         │  │ FULL FOG PATH             │
   │ (Clear repo state)                │  │ (Ambiguous problem)       │
   ├═══════════════════════════════════╤══════════════════════════════╣
   │ STEP 1: repo-sensemaker           │  STEP 1: problem-framer      │
   │ Input: repository_state           │  Input: raw_fog              │
   │ Output: repository_sensemaking_   │  Output: problem_frame.md    │
   │         brief.md                  │  Gate: review_problem_frame  │
   │ Gate: review_diagnosis            │                              │
   │                                   │  ▼                           │
   │ ▼                                 │  STEP 2: unknowns-mapper    │
   │ STEP 2: workflow-planner          │  Input: problem_frame.md     │
   │ Input: repository_sensemaking_    │  Output: unknowns_map.md    │
   │         brief.md                  │  Gate: review_unknowns_map   │
   │ Output: workflow_orchestration_   │                              │
   │         plan.md                   │  ▼                           │
   │ Gate: review_orchestration_plan   │  STEP 3: repo-sensemaker    │
   ╚═══════════════════════════════════╤══════════════════════════════╝
                                       │
                                       ▼
                    [Fog Type Classification Determined]
                    [recommended_workflow_id Selected]
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                    ╔════▼════════════════════╗    ╔▼════════════════════╗
                    │ If artifact              │    │ If artifact         │
                    │ research_needed==true:  │    │ research_needed==   │
                    │                         │    │ false: SKIP         │
                    │ STEP 3-conditional:     │    │                     │
                    │ discovery               │    │ Output artifact: go │
                    │ (external_routing)      │    │ directly to STEP 4  │
                    │                         │    │                     │
                    │ Gate: review_discovery  │    └─────────────────────┘
                    ╚════┬────────────────────╝
                         │
                         ▼
                    STEP 4: repo-sensemaker
                    Input: unknowns_map.md (or discovery_findings.md)
                    Input: repository_state
                    Output: repository_sensemaking_brief.md
                    Gate: review_sensemaking_brief
                         │
                         ▼
                    STEP 5: workflow-planner
                    Input: repository_sensemaking_brief.md
                    Output: workflow_orchestration_plan.md
                    Gate: none (or review_orchestration_plan)
                         │
                         ├─ Reads: primary_fog_type
                         ├─ Reads: recommended_workflow_id
                         │
                         ▼
┌───────────────────────────────────────────────────────────────────────┐
│ workflow_orchestration_plan.md (CRITICAL HANDOFF ARTIFACT)           │
│ ├─ primary_fog_type: one of [product_fog, ui_fog, docs_fog,         │
│ │                           architecture_fog]                        │
│ ├─ chosen_workflow_id: the recommended implementation workflow       │
│ ├─ workflow_steps: structured array of skill sequence                │
│ ├─ routing_decision_method: how fog type was determined              │
│ ├─ escalation_recommended: if true, urgency exists (rare in Phase 1) │
│ └─ machine_readable_plan: for agent/runtime parsing                  │
└───────────────────────────────────────────────────────────────────────┘
```

**Diagnostic Phase Output Artifacts** (Must Validate Successfully):
1. `repository_sensemaking_brief.md` (Primary)
   - Sections: evidence (file-level, with excerpts), recommended_workflow
   - Machine fields: artifact_id, primary_fog_type, evidence, recommended_workflow_id, created_at, immutable
   - Validator: `validate-artifact.py repository_sensemaking_brief` + `validate-brief.py`
   - Key field for routing: `primary_fog_type`

2. `workflow_orchestration_plan.md` (Critical Handoff)
   - Sections: brief_consumed, chosen_workflow, why_this_workflow, workflow_steps_definition, machine_readable_plan
   - Machine fields: artifact_id, primary_fog_type, chosen_workflow_id, routing_decision_method, workflow_steps, created_at
   - Validator: `validate-artifact.py workflow_orchestration_plan` + `validate-plan.py`
   - Key field for auto-invocation: `chosen_workflow_id` (reads from `recommended_workflow_id` in plan or brief)

**Validation Results**: Stored in `run_log.md`, NOT in artifacts (ADR 0004).

---

### Stage 2: Implementation Phase (Auto-Invoked)

**Goal**: Execute the recommended implementation workflow based on fog type, producing implementation-ready artifacts (prd, issues, code_patch, or documentation).

**Auto-Invocation Mechanism**:
- Runtime reads `workflow_orchestration_plan.chosen_workflow_id` (or `recommended_workflow_id`)
- Validates fog type alignment with selected workflow (ADR 0005)
- Automatically invokes the workflow without manual step selection
- Execution mode (guided_execution, autonomous_execution, yolo_execution) is inherited from diagnostic phase

#### Product Fog Path → `product-implementation-workflow`

```
Triggered when: primary_fog_type == 'product_fog'
Required input: repository_sensemaking_brief.md

Step 1: docs-aligner
  Input: context_artifacts (sensemaking brief + orchestration plan)
  Output: domain_alignment_report.md
  Gate: review
  ↓
Step 2: discovery (external_routing)
  Input: domain_alignment_report.md
  Output: discovery_findings.md
  Gate: review
  ↓
Step 3: opportunity-tree
  Input: discovery_findings.md
  Output: opportunity_map.md
  Gate: review
  ↓
Step 4: to-prd
  Input: opportunity_map.md
  Output: prd.md
  Gate: review
  ↓
Step 5: to-issues
  Input: prd.md
  Output: issue_list.md
  Gate: review
  ↓
Step 6: triage
  Input: issue_list.md
  Output: agent_brief.md
  Gate: review
  ↓
Step 7: tdd (implementation)
  Input: agent_brief.md
  Output: code_patch.md
  Gate: review
  ↓
Step 8: handoff
  Input: code_patch.md
  Output: session_summary.md
  Gate: session_close
```

#### UI Fog Path → `ui-implementation-workflow`

```
Triggered when: primary_fog_type == 'ui_fog'
Required input: repository_sensemaking_brief.md

Step 1: docs-aligner
  Input: context_artifacts
  Output: domain_alignment_report.md
  Gate: review
  ↓
Step 2: ui-flow
  Input: domain_alignment_report.md
  Output: ui_flows.md
  Gate: review
  ↓
Step 3: ui-screen-spec
  Input: ui_flows.md
  Output: screen_specs.md
  Gate: review
  ↓
Step 4: to-issues
  Input: screen_specs.md
  Output: issue_list.md
  Gate: review
  ↓
Step 5: triage
  Input: issue_list.md
  Output: agent_brief.md
  Gate: review
  ↓
Step 6: tdd (implementation)
  Input: agent_brief.md
  Output: code_patch.md
  Gate: review
  ↓
Step 7: handoff
  Input: code_patch.md
  Output: session_summary.md
  Gate: session_close
```

#### Docs Fog Path → `docs-implementation-workflow`

```
Triggered when: primary_fog_type == 'docs_fog'
Required input: repository_sensemaking_brief.md

Step 1: docs-aligner
  Input: context_artifacts
  Output: domain_alignment_report.md
  Gate: review
  ↓
Step 2: to-prd
  Input: domain_alignment_report.md
  Output: prd.md (documentation specification)
  Gate: review
  ↓
Step 3: handoff
  Input: prd.md
  Output: session_summary.md
  Gate: session_close
```

#### Architecture Fog Path → `implementation-workflow` or `architecture-implementation-workflow`

```
Triggered when: primary_fog_type == 'architecture_fog'
Required input: repository_sensemaking_brief.md

Step 1: docs-aligner
  Input: context_artifacts
  Output: domain_alignment_report.md
  Gate: review
  ↓
Step 2: to-prd
  Input: domain_alignment_report.md
  Output: prd.md (architecture specification)
  Gate: review
  ↓
Step 3: to-issues
  Input: prd.md
  Output: issue_list.md
  Gate: review
  ↓
Step 4: triage
  Input: issue_list.md
  Output: agent_brief.md
  Gate: review
  ↓
Step 5: tdd (implementation)
  Input: agent_brief.md
  Output: code_patch.md
  Gate: review
  ↓
Step 6: handoff
  Input: code_patch.md
  Output: session_summary.md
  Gate: session_close
```

**Implementation Phase Output Artifacts** (Must Validate Successfully):
- `prd.md` — Product/specification artifact
- `issue_list.md` — Decomposed implementation tasks
- `agent_brief.md` — Ready-for-implementation task brief
- `code_patch.md` — Implementation output (TDD cycles)
- `session_summary.md` — Completion summary

**Final Artifact**: `session_summary.md` (proof of execution completion)

---

## Human Gates and Approval Points

### Gates in Diagnostic Phase

| Gate Location | Execution Mode | Behavior |
|---|---|---|
| `review_problem_frame` (if full-fog-workflow) | guided_execution | ✋ PAUSE — User reviews problem frame |
| | autonomous_execution | ➡️ SKIP — Auto-proceed if validator passes |
| | yolo_execution | ➡️ SKIP — Auto-proceed, validator is safety |
| `review_unknowns_map` (if full-fog-workflow) | guided_execution | ✋ PAUSE — User reviews unknowns and assumptions |
| | autonomous_execution | ➡️ SKIP — Auto-proceed if validator passes |
| | yolo_execution | ➡️ SKIP — Auto-proceed, validator is safety |
| `review_discovery` (conditional) | guided_execution | ✋ PAUSE — User reviews discovery findings |
| | autonomous_execution | ➡️ SKIP — Auto-proceed if validator passes |
| | yolo_execution | ➡️ SKIP — Auto-proceed, validator is safety |
| `review_diagnosis` / `review_sensemaking_brief` | guided_execution | ✋ PAUSE — User reviews fog diagnosis and weakest boundary |
| | autonomous_execution | ➡️ SKIP — Auto-proceed if validator passes |
| | yolo_execution | ➡️ SKIP — Auto-proceed, validator is safety |
| `review_orchestration_plan` (if required) | guided_execution | ✋ PAUSE — User reviews selected workflow and routing logic |
| | autonomous_execution | ➡️ SKIP — Auto-proceed if validator passes |
| | yolo_execution | ➡️ SKIP — Auto-proceed, validator is safety |
| **Auto-Invocation of Implementation Workflow** | all modes | ➡️ AUTOMATIC — No approval gate before implementation workflow starts |

### Gates in Implementation Phase

- **`review` gates** (between steps): Behavioral varies by execution mode (see above)
- **`session_close` gate** (at handoff): Final approval for completion
- **No gate before starting implementation workflow** — Auto-invocation is unconditional in Phase 1

---

## Artifact Chain: Validation and Dependencies

```
DIAGNOSTIC PHASE ARTIFACTS:
user_intent.md
  ↓ (input to)
problem_frame.md (if full-fog)
  ↓ (input to)
unknowns_map.md (if full-fog)
  ├─ decision point: if unknowns_map.research_needed == true
  │  ↓
  │  discovery_findings.md (external_routing)
  │  ↓ (input to)
  │
repository_sensemaking_brief.md ✅ [MUST VALIDATE]
  ├─ critical_field: primary_fog_type
  ├─ critical_field: recommended_workflow_id
  ↓ (input to)
workflow_orchestration_plan.md ✅ [MUST VALIDATE]
  ├─ critical_field: primary_fog_type
  ├─ critical_field: chosen_workflow_id
  ├─ routing_decision: fog type → implementation workflow
  ↓ (triggers auto-invocation)

IMPLEMENTATION PHASE ARTIFACTS (based on fog_type):
context_artifacts (brief + plan from diagnostic)
  ↓ (input to)
domain_alignment_report.md ✅ [MUST VALIDATE]
  ↓ (input to)
[workflow-specific artifacts]
  (discovery_findings, opportunity_map, ui_flows, screen_specs, etc.)
  ↓ (input to)
prd.md ✅ [MUST VALIDATE]
  ├─ critical_field: source_intent_ref
  ├─ critical_field: user_goal_preserved_as
  ├─ critical_field: scope_expansion_proposed
  ↓ (input to)
issue_list.md ✅ [MUST VALIDATE]
  ├─ critical_field: source_intent_ref
  ├─ critical_field: scope_expansion_status
  ↓ (input to)
agent_brief.md ✅ [MUST VALIDATE]
  ├─ critical_field: source_intent_ref
  ↓ (input to)
code_patch.md ✅ [MUST VALIDATE]
  ↓ (input to)
session_summary.md ✅ [MUST VALIDATE]
  └─ critical_field: source_intent_ref
```

---

## What Must Validate Successfully

### Diagnostic Phase (Non-Negotiable)

1. **`user_intent.md`**
   - Validator: `validate-artifact.py user_intent` + `validate-user-intent.py`
   - Failure mode: Workflow halts, error reported to user
   - Retry: User clarifies intent, provides amended artifact

2. **`repository_sensemaking_brief.md`**
   - Validator: `validate-artifact.py repository_sensemaking_brief` + `validate-brief.py`
   - Failure mode: Diagnostic incomplete, workflow halts
   - Must have: primary_fog_type, evidence with file references, recommended_workflow
   - Retry: repo-sensemaker re-invoked with additional context

3. **`workflow_orchestration_plan.md`**
   - Validator: `validate-artifact.py workflow_orchestration_plan` + `validate-plan.py`
   - Failure mode: Auto-invocation blocked, workflow halts
   - Must have: primary_fog_type, chosen_workflow_id, workflow_steps array
   - Retry: workflow-planner re-invoked with corrected diagnostic brief

### Implementation Phase (Execution Mode Dependent)

| Artifact | Validator | guided_execution | autonomous_execution | yolo_execution |
|---|---|---|---|---|
| domain_alignment_report.md | validate-artifact.py | ✅ Required | ✅ Required | ✅ Required |
| prd.md | validate-prd.py | ✅ Required | ✅ Required | ✅ Required |
| issue_list.md | validate-artifact.py | ✅ Required | ✅ Required | ✅ Required |
| agent_brief.md | validate-artifact.py | ✅ Required | ✅ Required | ✅ Required |
| code_patch.md | validate-artifact.py | ✅ Required | ✅ Required | ✅ Required |
| session_summary.md | validate-artifact.py | ✅ Required | ✅ Required | ✅ Required |

**Validation Failure Handling**:
- **guided_execution**: Pause at gate, user reviews error, decides to retry or escalate
- **autonomous_execution**: Automatic retry (max 3 attempts, per ADR 0005); escalate on exhaustion
- **yolo_execution**: Zero-tolerance — validation failure aborts step, records error, halts workflow

---

## Human Gates: Placement and Behavior

### Where Humans Approve / Intervene

1. **After diagnostic phase completion** (workflow_orchestration_plan produced)
   - Execution mode `guided_execution`: Manual review of fog classification and recommended workflow
   - Decision point: Approve routing, request re-diagnosis, or override with explicit workflow selection

2. **Between implementation steps** (each `gate: review` checkpoint)
   - Execution mode `guided_execution`: Manual approval before proceeding
   - Decision point: Accept step output, request revision, or escalate

3. **At workflow completion** (handoff step with `gate: session_close`)
   - All execution modes: Final approval or request for additional work

### Where Humans Do NOT Intervene (Phase 1)

- ❌ Before auto-invocation of implementation workflow
- ❌ Within validator error handling (validators decide pass/fail, not humans)
- ❌ In skill parameter selection (skills read from context artifacts, not from human input)
- ❌ In execution mode selection (set at workflow invocation time, not mid-flow)

---

## Phase 1 Success Criteria

### The golden path succeeds when:

✅ **Diagnostic phase completes**:
- User intent artifact exists and validates
- Repository sensemaking brief exists and identifies fog type
- Workflow orchestration plan exists with correct fog type + workflow routing

✅ **Fog type classification is accurate**:
- Diagnosed fog type matches actual project need
- Implementation workflow selected aligns with fog type
- Evidence in brief supports fog classification (file references + excerpts)

✅ **Auto-invocation succeeds**:
- Implementation workflow invokes automatically (no manual step)
- Workflow runs in same execution mode as diagnostic phase
- No approval gate blocks auto-invocation in Phase 1

✅ **Implementation phase completes**:
- All workflow steps execute (gates either auto-skip or user approves)
- All artifacts validate successfully
- session_summary.md produced and contains source_intent_ref

✅ **Proof is auditable**:
- run_log.md documents every skill invocation, validator result, gate decision
- Artifacts are immutable (created once, never modified)
- source_intent_ref traces from session_summary back to user_intent

---

## Comparison to Informal Understanding

**Original Informal Path** (from ticket):
```
intent → repo-sensemaker → validated brief → architectural-review → recommendation → run log → exit 0
```

**Actual Canonical Phase 1 Path**:
```
intent 
  ↓
[problem-framer → unknowns-mapper] (if full-fog; optional for fast-path)
  ↓
repo-sensemaker (produces repository_sensemaking_brief with fog_type classification)
  ├─ INPUT: repository_state
  ├─ OUTPUT: repository_sensemaking_brief ✅ [validates with validate-brief.py]
  ↓
workflow-planner (produces orchestration_plan with recommended_workflow_id)
  ├─ INPUT: repository_sensemaking_brief
  ├─ OUTPUT: workflow_orchestration_plan ✅ [validates with validate-plan.py]
  ├─ [reads: primary_fog_type]
  ├─ [reads: recommended_workflow_id]
  ↓
[AUTO-INVOCATION TRIGGER]
  ↓
implementation-workflow (product/ui/docs/architecture, selected by fog_type)
  ├─ STEPS: domain-aligner → [research/spec] → to-prd → to-issues → triage → tdd → handoff
  ├─ OUTPUT ARTIFACTS: prd ✅, issue_list ✅, agent_brief ✅, code_patch ✅, session_summary ✅
  ↓
exit 0 with session_summary.md proof
```

**Key Differences**:
1. No separate "architectural-review" step in Phase 1 (repo-sensemaker produces the diagnosis)
2. Auto-invocation is the default (no separate recommendation decision point)
3. Implementation workflows are four distinct paths (product/ui/docs/architecture), not one generic
4. Validation is ongoing (not retroactive); validators block invalid artifacts

---

## Excluded from Phase 1

### Features Ruled Out of Scope (Not Roadmap Items)

These are explicitly NOT part of Phase 1 golden path:

| Feature | Why Excluded | Future Phase |
|---|---|---|
| Manual implementation workflow selection | Auto-invocation is the design; manual override is out-of-scope | Phase 2+ if needed |
| External artifact storage (cloud, DB) | Local-first design; artifacts stay on filesystem | Phase 3+ if needed |
| Real-time collaborative editing | Single-writer model; no concurrent edit conflicts | Phase 4+ if needed |
| Third-party system integration (Jira, Linear, etc.) | Handoff artifact is the integration point; actual sync is downstream | Phase 2+ if needed |
| Skill parameter customization via UI | Skills read from context artifacts, not user forms | Phase 3+ if needed |
| Automated deployment from code_patch | code_patch is a review artifact; deployment is user responsibility | Phase 2+ if needed |
| Multi-repo orchestration | Single repository context per session | Phase 5+ if needed |
| Agent-to-agent messaging | No inter-agent communication; agents read shared artifacts | Phase 4+ if needed |

---

## Execution Modes and Golden Path

All execution modes follow the same canonical path; the difference is gate behavior:

| Mode | Diagnostic Gates | Implementation Gates | Safety Mechanism | Use Case |
|---|---|---|---|---|
| **plan_only** | ➡️ SKIP | ➡️ SKIP | Validators only | Preview workflow without execution |
| **prompt_chain** | ➡️ SKIP | ➡️ SKIP | Validators only | Chain prompts for agent coordination |
| **guided_execution** | ✋ PAUSE | ✋ PAUSE | Human approval | Learning, exploration, high-stakes decisions |
| **autonomous_execution** | ➡️ SKIP | ➡️ SKIP | Validators + retry logic (max 3 attempts) | Production CI/CD with automatic recovery |
| **yolo_execution** (default) | ➡️ SKIP | ➡️ SKIP | Validators (zero-tolerance) | High-velocity local development |

---

## Summary: Is This the Canonical Phase 1 Path?

**Yes**, with clarifications:

1. ✅ **Diagnostic phase is correct**: problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner
2. ✅ **Fog classification is the key routing decision**: primary_fog_type determines implementation workflow
3. ✅ **Auto-invocation is the design**: No separate "architectural review" gate; workflow-planner → auto-invoke
4. ✅ **Four implementation workflows**: product/ui/docs/architecture, not one generic path
5. ✅ **Validation is the safety mechanism**: Artifacts must validate; validators block invalid progress
6. ✅ **Agents own the control loop**: Skill tool invocations, conversational decision-making
7. ✅ **Artifacts are immutable and traced**: source_intent_ref links all outputs back to user intent

The golden path is **skill-led, artifact-driven, and auto-invoked**. It's production-ready for Phase 1.

---

## Implementation Evidence

**This golden path has been validated through**:
- Phase 4.1: Fresh-agent behavior testing (happy path + failure scenarios)
- Phase 4.2: Performance measurement
- Phase 4.3: Edge case testing (critical bug in workflow-planner escalation logic fixed)
- Phase 4.4: Operator runbooks documented
- Phase 4.5: Production gate approval

**See**: PHASE-4-COMPLETE-FINAL-UPDATED.md, PHASE-4-5-PRODUCTION-GATE.md for detailed proof.

---

## References

- **CONTEXT.md** § Orchestration Principles (ADRs 0001-0013)
- **workflow-registry.yaml** — Authoritative workflow definitions
- **artifact-contracts.yaml** — Machine field contracts and validator specs
- **docs/mode-coverage.yaml** — Execution mode proving status
- **GETTING_STARTED.md** — Usage guide with examples
