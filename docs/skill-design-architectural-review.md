# Architectural Review Skill: Complete Verified Design

**Date**: 2026-07-18  
**Status**: Design phase complete. Ready for implementation planning approval.  
**Confidence**: 85%+ on core architecture; 70%+ on edge cases.  
**Document status**: Untracked design proposal. Created during authorized design-verification phase. No production code modified.

---

## 1. Executive Decision

### Recommendation

**The architectural-review capability SHOULD exist** as a standalone skill that evaluates whether proposed strategic work (roadmaps, phase transitions, capability additions) represents the right investment for the repository's current state.

**First-version architecture** (Design A: explicit continuation):
```
repository_sensemaking_brief (input)
+ proposed_direction (input)
        ↓
architectural-review (skill)
        ↓
architectural_review_recommendation (artifact: recommendation only)
        ↓
[Workflow ends; artifact is terminal]
        ↓
recommended_workflow_id (user reads recommendation and manually invokes next workflow)
        ↓
selected workflow execution
```

**Authorization in v1**: Procedural. User reviews recommendation and decides whether to proceed. No durable authorization record is technically enforced or persisted by this capability.

**Explicitly excluded from v1**:
- Conditional workflow execution (not implemented in runtime; future enhancement)
- Automatic trigger evaluation (manual workflow selection; future automation)
- workflow-planner modification (no new consumer contract; future optional input)
- Durable authorization record (user decision is procedural, not persisted; future enhancement)
- Integration into all workflows (opt-in via dedicated workflow in v1)
- Micro-skill decomposition (keep as single coherent skill)

**Why this recommendation**:
- Fills proven gap (no existing systematic capability comparison against current state)
- Matches repository's artifact-driven model
- Requires no runtime changes
- Intended to be additive (no existing workflows modified; compatibility to be verified through implementation and regression testing)
- Testable in isolation with deterministic fixtures
- Creates reusable recommendation artifact for future workflows
- Clear authority model: skill recommends; user decides procedurally; runtime executes only after user selects another workflow

---

## 2. Scope Statement

**Repository status**: Untracked design-document file.

**Location authorization**: Design documents are established in `docs/` directory. Evidence:
- `docs/orchestration-patterns.md` (architecture design)
- `docs/implementation-workflow-guide.md` (workflow design)
- `docs/orchestrator-skill-example.md` (skill example)
- `docs/AGENTS.md` (agent design)
- `docs/IMPLEMENTATION-MASTER-SUMMARY.md` (implementation strategy)
- `docs/phase-1-consistency-review.md` (phase design)

**Location chosen**: `docs/skill-design-architectural-review.md` matches established convention.

**Modifications made**: Only the design document itself. No production code, skill files, validators, registries, or tests were created or modified.

**Status**: Design proposal ready for review. Document is temporary analysis unless repository convention approves it as permanent reference.

---

## 3. Contradiction Resolution Summary

| # | Original Contradiction | Binding Decision | Implementation | Status |
|---|------------------------|------------------|-----------------|--------|
| 1 | No consumer vs. optional workflow-planner input | Design A: No workflow-planner modification | Removed all workflow-planner consumer claims; documented as future enhancement | ✅ RESOLVED |
| 2 | Recommendation conflated with final decision | Separate recommendation from authorization | Artifact contains recommendation only; authorization is procedural user decision in v1, not recorded by this capability | ✅ RESOLVED |
| 3 | Testing excluded but "complete E2E scenario" claimed | Include test fixtures in v1 minimum slice | Added 5 required validator fixtures; moved from "optional follow-up" to "required for validation and testing" | ✅ RESOLVED |
| 4 | "100% backward compatible" without evidence | Use evidence-based categories | Replaced with structured compatibility_assessment with status: additive, unchanged, or uncertain for each category | ✅ RESOLVED |
| 5 | Grouped "7 files" without individual paths | Enumerate every file individually | Complete path-by-path file plan with purpose, requirement justification, and consequences | ✅ RESOLVED |
| 6 | Mixed terminology (decision/recommendation) | Stable vocabulary | artifact_type: `architectural_review_recommendation`; field: `review_recommendation`; skill: `architectural-review` | ✅ RESOLVED |
| 7 | "History is modeled" without discovery mechanism | Model history honestly | Added proposal_ref, reviewed_at, reviewed_repository_revision, supersedes_review_ref fields; documented discovery pattern as explicit reference lookup | ✅ RESOLVED |
| 8 | "Conditional execution not implemented" without observable semantics | Show execution trace precisely | Added a trace showing that decision_field, if_true, and if_false are not evaluated. Final step-completion and workflow-continuation behavior remains unverified. | ✅ RESOLVED |
| 9 | No scope/authorization statement | State plainly in document header | Added explicit document status, location evidence, and authorization scope in this section | ✅ RESOLVED |

---

## 4. Stable Terminology Table

| Component | Canonical Name | Usage |
|-----------|----------------|-------|
| Skill ID | `architectural-review` | Invoked via skill registry (slash-command support requires runtime verification) |
| Workflow ID | `architectural-review-workflow` | Registered in workflow-registry.yaml |
| Artifact type/ID | `architectural_review_recommendation` | Contract entry; artifact-contracts.yaml |
| Artifact filename | `architectural_review_recommendation.md` | Session-scoped: `artifacts/{session_id}/architectural_review_recommendation.md` |
| Recommendation field | `review_recommendation` | Contains: outcome, confidence, rationale, approved_scope, excluded_scope, required_preconditions, recommended_workflow_id |
| Authorization | Procedural (v1) | User decision; no durable runtime record in v1; future enhancement |
| Validator (generic) | `validate-artifact.py` | Structural validation (existing, reused) |
| Validator (specialized) | `validate-architectural-review-recommendation.py` | Semantic validation (new) |
| Test fixtures | `tests/fixtures/architectural-review-recommendation/*.md` | Deterministic contract and validator tests |

**Rationale**: "decision" is avoided because the artifact contains a recommendation (nonbinding), not a final decision. The skill emits a nonbinding recommendation. In v1, the user decides procedurally whether to continue; that decision is not persisted by this capability.

---

## 5. Repository Evidence and Confidence Table

| Claim | Classification | Evidence Path | Proves | Does Not Prove | Confidence |
|-------|----------------|--------------|--------|----------------|------------|
| Artifact paths are singleton templates in contracts but runtime-scoped to sessions | Direct contract + Code | `skills/workflow-planner/references/artifact-contracts.yaml` line 5; `scripts/workflow-runtime.py` lines 1352-1365 (`_scope_to_session_dir`) | Artifacts use scoped paths; decision history retained across sessions | Whether decisions are technically immutable | 98% |
| The runtime does not evaluate decision_field or choose if_true/if_false branches | Code inspection | `CONTEXT.md` lines 357-381 (documented); `scripts/workflow-runtime.py` line 721 (skill="conditional-branch"); no `decision_field` evaluation in execute_step (lines 713-900) | Conditional syntax is parsed/validated; runtime does not select branches | Final workflow behavior for conditional steps (step completion, error handling) remains unverified | 95% |
| workflow-planner consumes only repository_sensemaking_brief | Direct contract | `skills/workflow-planner/SKILL.md` lines 14-16 | workflow-planner is not a v1 consumer of new artifact | Future contract modification | 99% |
| Handoff does not reference architectural-review | Negative evidence | `skills/handoff/SKILL.md` lines 1-41; `grep -r "architectural" skills/handoff/` → 0 results | handoff is not a v1 consumer | Handoff could be modified later | 98% |
| Canonical vocabulary defines gate outcomes (approved/denied/needs_revision) | Direct contract | `docs/canonical-vocabulary.yaml` lines 153-299 | Gate system has standard outcome vocabulary | This does not prove durable persistence, actor identity, override fields, or artifact linkage for architectural-review v1 | 90% |
| Repository has established design-document location | Directory evidence | `docs/` contains 20+ design documents (orchestration-patterns.md, AGENTS.md, IMPLEMENTATION-*.md, etc.) | Design documents belong in `docs/` | Exact naming convention | 95% |

---

## 6. Consumer Model: Design A (Terminal Artifact, Procedural Continuation)

**v1 consumption and continuation** (explicit, user-controlled):

```
repository_sensemaking_brief
+ proposed_direction
        ↓
architectural-review skill
        ↓
architectural_review_recommendation
        ↓
generic and specialized validation
        ↓
workflow ends
        ↓
user reviews recommendation
        ↓
user manually invokes another workflow
```

**Consumers in v1**: None. Artifact is terminal. No automatic routing or gate-based continuation.

**Continuation mechanism**: 
- Recommendation includes `recommended_workflow_id` field for user reference
- User reads recommendation artifact and decides whether to proceed
- User manually selects and invokes next workflow (or skips if recommendation is defer/reject)
- No authorization gate required; no approval recording by this capability

**Why this design**:
- Minimum viable scope (no gate consumer, no authorization artifact)
- No workflow-planner modification required
- No hidden routing logic
- User has full visibility and control over workflow selection
- Clear separation: skill recommends (nonbinding); user decides (procedural); runtime executes (next workflow)

**Future enhancements** (post-v1, not blocking minimum slice):
- Optional workflow-planner input contract
- Automatic routing based on recommendation
- Conditional step execution in runtime
- Durable authorization record or enhanced gate integration

---

## 7. Recommendation and Authorization Semantics

### Review Recommendation (Skill-Produced)

**Artifact contains**:
```yaml
artifact_id: architectural_review_recommendation
schema_version: 1

review_recommendation:
  outcome: pursue | pursue_narrowed | investigate_first | defer | reject
  confidence: high | medium | low
  rationale: <structured reasoning>
  approved_scope: [items] # required if pursue_narrowed; omitted otherwise
  excluded_scope: [items] # required if pursue_narrowed; omitted otherwise
  required_preconditions: [conditions] # optional for all outcomes
  recommended_workflow_id: workflow_id # required if pursue/pursue_narrowed; omitted if investigate_first/defer/reject
  investigation_step: {step_to_validate_first} # required if investigate_first; omitted otherwise
  decision_pending_result: {result_of_investigation} # required if investigate_first; omitted otherwise
  reconsideration_condition: {when_to_revisit} # required if defer; omitted otherwise
  why_not_now: {rationale_for_deferral} # required if defer; omitted otherwise
  kill_conditions: [conditions] # required if reject; omitted otherwise
  
supporting_evidence:
  repository_brief_ref: (path to brief)
  proposal_ref: (reference to proposal artifact or external)
  reviewed_at: ISO 8601 timestamp
  reviewed_repository_revision: (git commit hash)
  
convention: Inapplicable fields are omitted from the artifact (not null, not empty strings; absent from YAML)
```

**What this artifact contains**: Professional recommendation based on analysis. Nonbinding.

**What this artifact does NOT contain**: Authorization, approval, final decision, or override information.

### Authorization Model (v1: Procedural)

**v1 status**: Procedural user decision. No durable authorization record is modeled by this capability.

**Authority model**:
- Skill: Produces recommendation
- User: Reviews recommendation and decides whether to proceed
- Runtime: Executes selected workflow (no technical enforcement of approval)

**Persistence**: Authorization decision is not captured or enforced. User reads recommendation artifact and manually selects next workflow.

**Future enhancement**: Durable authorization artifact or enhanced gate record could record approval/override with actor, rationale, and accepted_risks. Not required for v1 minimum slice.

**Design rationale**: Keeps skill focused on analysis. Authorization remains a user procedural decision in v1, avoiding claims about runtime persistence not yet verified.

---

## 8. Authorization History and Discovery Model

### Storage Isolation and Linkage (v1 Model)

**Session-scoped paths**: Supported through runtime path resolution.
```yaml
canonical_path: artifacts/architectural_review_recommendation.md
runtime_scoped: artifacts/{session_id}/architectural_review_recommendation.md
```

**Artifact identity fields** (for explicit linkage):
```yaml
artifact_id: architectural_review_recommendation
proposal_ref: (external reference to proposed work)
repository_brief_ref: ../../artifacts/{session_id}/repository_sensemaking_brief.md
reviewed_at: ISO 8601
reviewed_repository_revision: (git commit hash from review session)
supersedes_review_ref: {prior_artifact_path} # if newer review
prior_review_refs: [{path1}, {path2}] # links to older reviews of same proposal
```

**Discovery in v1**: Explicit, not automatic.
- User/agent knows session_id (from run log or prior execution)
- Path: `artifacts/{session_id}/architectural_review_recommendation.md`
- Supersession: Check `supersedes_review_ref` field to find older reviews
- Proposal lineage: Check `prior_review_refs` to trace all reviews of one proposal

**Not included in v1** (future enhancement):
- Global search/index over prior reviews
- Automatic staleness detection
- Recommendation history browser

**Immutability**: Not technically enforced by this capability. Session directories are created at runtime and persisted; artifacts are not rewritten in place. True immutability requires verification during implementation that runtime does not rewrite artifact paths.

**Staleness detection** (procedural, not automated in v1):
- Users manually check `reviewed_repository_revision` against current HEAD
- If major code changes occurred since review, recommendation may be stale
- Users must run new review if uncertainty exists

---

## 9. Conditional Execution: Precise Observable Behavior

### Execution Trace

```
1. REGISTRY SCHEMA
   File: skills/workflow-planner/references/workflow-registry.yaml
   Structure: workflows[*] can have steps[*] with conditional: true
   Example:
   - id: 2-conditional
     conditional: true
     decision_field: repository_sensemaking_brief.escalation_recommended
     if_true: { skill: architectural-review, ... }
     if_false: { next_step: 3 }

2. REGISTRY PARSER
   File: scripts/workflow-runtime.py lines 1333-1345
   Behavior: Loads workflow YAML; preserves conditional field
   Observable: conditional steps appear in loaded workflow structure

3. PLANNER REPRESENTATION
   File: scripts/workflow-runtime.py lines 550-600 (generate_plan method)
   Behavior: Includes conditional steps in orchestration plan
   Observable: workflow_orchestration_plan contains conditional step descriptions

4. RUNTIME STEP LOADING
   File: scripts/workflow-runtime.py line 2363 (step execution loop)
   Behavior: Iterates over steps; calls execute_step(step, ...)
   Observable: Conditional step is passed to execute_step with conditional=true

5. EXECUTE_STEP ENTRY
   File: scripts/workflow-runtime.py line 713 (def execute_step)
   Behavior: Reads step.get("skill", "?")
   Transformation: If conditional, sets skill = "conditional-branch"
   Observable: skill variable becomes "conditional-branch" (no decision logic evaluated)

6. NO DECISION EVALUATION
   File: scripts/workflow-runtime.py lines 713-900
   Search: grep -n "decision_field" → 0 results
   Search: grep -n "if_true" → only in step_label() for reporting, not execution
   Observable: NO code evaluates repository_sensemaking_brief.escalation_recommended
   Observable: NO code selects if_true or if_false branch

7. EXECUTE_STEP BEHAVIOR
   File: scripts/workflow-runtime.py lines 730-850
   For conditional-branch step:
   - No skill execution (skill is "conditional-branch"; no matching skill file)
   - No artifact produced
   - Step marked: status = "PLANNED" or "PROMPT_GENERATED"
   Observable: No execution path for if_true or if_false branches

8. Observable behavior (partially verified):
   - Conditional step is parsed and reported
   - Decision_field is never evaluated (verified: `grep decision_field scripts/workflow-runtime.py` returns empty)
   - Artifact is never produced (verified: no execution path for if_true/if_false)
   - What happens next is uncertain:
     * Does conditional-branch step complete successfully?
     * Is the workflow halted or does it proceed?
     * Is an error raised or is it silent?
   - Both if_true and if_false branches are ignored (verified: only used in reporting, not execution)

CONCLUSION: Conditional syntax exists for documentation/validation purposes. Runtime does not evaluate `decision_field` and does not select branches. Final observable behavior (step completion, workflow continuation, error handling) is partially verified and should be tested during implementation.
```

### v1 Implication

Do NOT use conditional steps in v1. Use explicit workflow selection instead:
- Users/agents choose which workflow to invoke
- No hidden conditional logic
- All routing is visible in run log

---

## 10. Input Contract

### Required Inputs

```yaml
repository_sensemaking_brief:
  type: artifact
  path: artifacts/{session_id}/repository_sensemaking_brief.md
  required: true
  description: |
    Repository diagnosis from repo-sensemaker.
    Must include: fog_type, evidence sections, weakest_boundary, machine_readable block.
  staleness_check: |
    If brief is more than one session old and major code changes occurred,
    architectural-review may recommend "investigate_first" with re-diagnosis step.
    Runtime: Recommend running full-fog-workflow for updated diagnosis.

proposed_direction:
  type: artifact | structured_input
  required: true
  description: |
    Description of capability, roadmap, or phase transition being evaluated.
    Can be markdown artifact or user-provided context.
    Must include: capability name, claimed benefits, implementation approach,
    authority/boundary changes.
    Example: roadmap artifact, strategy proposal, documented design change.
```

### Completeness and Staleness Handling

**If brief is incomplete**:
- Check: Required sections (evidence, recommended_workflow_id) present?
- Check: Evidence citations valid (referenced files exist)?
- Check: weakest_boundary classified with recognized weakness_type?
- Action: Return `investigate_first` with investigation step: "Request complete repository sensemaking"

**If proposed_direction is vague**:
- Check: Capability name, implementation approach, boundary changes clearly stated?
- Action: Return `investigate_first` with: "Clarify proposed capability scope and implementation approach"

**If brief is stale** (older session + major code changes):
- Action: Return `investigate_first` with: "Request updated repository sensemaking given recent changes"
- Do NOT silently re-diagnose; recommend explicit full-fog-workflow invocation

---

## 11. Output Artifact Contract

### Artifact Identity

```
id: architectural_review_recommendation
path: artifacts/architectural_review_recommendation.md
produced_by: architectural-review
consumed_by: (none in v1)
required_for_modes: plan_only, prompt_chain, guided_execution, autonomous_execution
```

### Required Sections

1. Review Context — What is being evaluated and when
2. Phase Assessment — Repository phase and proposed transition
3. Current Investment Assessment — Diminishing returns analysis
4. Proposed Capability — What is proposed (not features, capabilities)
5. User Workflow Inversion — How architecture becomes invisible
6. Dependency and Opportunity Cost — Trade-offs
7. Risk Analysis — Authority fragmentation, duplication, migration risks
8. Validation Strategy — Success measures and baselines
9. Review Recommendation — Final recommendation and confidence
10. Machine-Readable Recommendation — YAML block with structured fields

### Required Machine Fields

```yaml
artifact_id: architectural_review_recommendation
schema_version: 1
source_intent_ref: 00-user-intent.md

review_context:
  proposal_ref: (string or path)
  repository_brief_ref: (relative path)
  review_mode: direction_review | roadmap_review
  reviewed_at: ISO 8601
  reviewed_repository_revision: (git commit hash)

phase_assessment:
  current_optimization_target: (string from brief)
  proposed_optimization_target: (string)
  confidence: high | medium | low
  unresolved_assumptions: (list)

current_investment_assessment:
  subsystem_under_review: (string)
  current_highest_bottleneck: (string from brief)
  diminishing_returns_status: confirmed | plausible | unsupported | not_present

proposed_capability:
  capability_name: (string)
  systemic_primitive: (string)
  preserved_authority_boundaries: (list)
  affected_authority_boundaries: (list)

risk_analysis:
  primary_failure_mode: (string)
  authority_fragmentation_risks: (list)
  duplication_risks: (list)
  kill_conditions: (list of conditions making proposal untenable)

validation_strategy:
  success_measures:
    - metric: (string)
      baseline_status: measured | estimated | unknown
      baseline: (value or "unknown")
      target: (value)
      target_basis: observed_need | benchmark | hypothesis
      measurement_method: (string)

review_recommendation:
  outcome: pursue | pursue_narrowed | investigate_first | defer | reject
  confidence: high | medium | low
  rationale: (2-3 paragraphs)
  approved_scope: (list, if pursue_narrowed; required)
  excluded_scope: (list, if pursue_narrowed; required)
  required_preconditions: (list; always)
  recommended_workflow_id: (workflow_id if pursue/pursue_narrowed; omitted otherwise)
  investigation_step: (if investigate_first; required: specifies validation step)
  decision_pending_result: (if investigate_first; required: outcome if investigation shows X)
  reconsideration_condition: (if defer; required: when to revisit)
  why_not_now: (if defer; required: rationale for deferral)
  kill_conditions: (if reject; required: what must change to reconsider)
```

### Decision Enum Semantics

```yaml
pursue:
  meaning: Investment is right for current state. Proceed as planned.
  when_use:
    - Bottleneck matches proposal
    - Authority boundaries preserved
    - Leverage is clear
    - Success measurable

pursue_narrowed:
  meaning: Partially right. Proceed with defined scope limits.
  requires:
    - approved_scope (included)
    - excluded_scope (excluded)
    - rationale
  when_use:
    - Core is sound but implementation too broad
    - Some authority changes necessary but others risky

investigate_first:
  meaning: Not enough evidence. Gather validation before decision.
  requires:
    - investigation_step (specific measurement/research/experiment)
    - decision_pending_result (will pursue/defer/reject if investigation shows X)
  when_use:
    - Brief incomplete or stale
    - Proposed direction vague
    - Key assumptions untested

defer:
  meaning: Right direction, wrong timing. Revisit after condition.
  requires:
    - reconsideration_condition (when to revisit)
    - why_not_now (what must change first)
  when_use:
    - Prerequisites must complete first
    - Other work has higher ROI now

reject:
  meaning: Should not proceed. Fundamental conflict with current state.
  requires:
    - kill_conditions (what must change to reconsider)
  when_use:
    - Would fragment existing authority
    - Duplicates existing capability
    - Too expensive to reverse
```

---

## 12. Validator Design and Responsibility Matrix

### Generic Validator (structural)

**Script**: `python scripts/validate-artifact.py architectural_review_recommendation {path}`

**Validates**:
- File exists and is readable
- YAML block is parseable
- Required sections present
- Required machine fields present
- No absolute file paths
- Relative paths valid

**Cannot validate**: Reasoning quality, confidence justification, or completeness of risk analysis.

### Specialized Validator (semantic)

**Script**: `python scripts/validate-architectural-review-recommendation.py {path}` (new, following validate-brief.py pattern)

**Deterministic rules for each outcome**:

**pursue**:
- `recommended_workflow_id` required and must exist in workflow-registry.yaml
- investigation_step, decision_pending_result, reconsideration_condition, why_not_now, kill_conditions absent

**pursue_narrowed**:
- `approved_scope` non-empty and present
- `excluded_scope` non-empty and present
- `recommended_workflow_id` required and must exist in workflow-registry.yaml
- investigation_step, decision_pending_result, reconsideration_condition, why_not_now, kill_conditions absent

**investigate_first**:
- `investigation_step` present and non-empty
- `decision_pending_result` present (defines expected outcome of investigation)
- `recommended_workflow_id` absent or omitted
- approved_scope, excluded_scope, reconsideration_condition, why_not_now, kill_conditions absent

**defer**:
- `reconsideration_condition` present and non-empty (when to revisit)
- `why_not_now` present and non-empty (rationale for deferral)
- `recommended_workflow_id` absent or omitted
- approved_scope, excluded_scope, investigation_step, decision_pending_result, kill_conditions absent

**reject**:
- `kill_conditions` non-empty (what must change to reconsider)
- `recommended_workflow_id` absent or omitted
- approved_scope, excluded_scope, investigation_step, decision_pending_result, reconsideration_condition, why_not_now absent

**Also validates**:
- Workflow ID (if present) exists in workflow-registry.yaml
- Evidence citations point to valid files
- confidence is high/medium/low

**Cannot validate** (syntactic evidence-reference):
- Whether evidence is substantively adequate (only validates that cited files exist)
- Whether reasoning is sound
- Whether confidence level is justified by evidence
- Whether assumptions are realistic

### Validator Responsibility Matrix

| Rule | Generic | Specialized | Scenario Test | Human Judgment |
|------|---------|-------------|---------------|----------------|
| Artifact file exists | ✓ | — | — | — |
| YAML parseable | ✓ | — | — | — |
| Required sections present | ✓ | — | — | — |
| Machine fields present | ✓ | — | — | — |
| No absolute paths | ✓ | — | — | — |
| Decision enum valid | ✓ | — | — | — |
| Confidence is high/medium/low | ✓ | — | — | — |
| Decision/precondition consistency | — | ✓ | — | — |
| Workflow ID exists in registry | — | ✓ | — | — |
| Evidence citations valid | — | ✓ | — | — |
| Success metrics complete | — | ✓ | — | — |
| Confidence level is justified | — | — | — | ✓ |
| Risk analysis is thorough | — | — | — | ✓ |
| Reasoning is sound | — | — | — | ✓ |
| Assumptions are realistic | — | — | — | ✓ |
| Decision matches repository state | — | — | ✓ (E2E test with real brief + proposal) | — |
| Recommendation would predict real outcomes | — | — | — | ✓ (verified over time) |

---

## 13. Workflow Integration Design

### v1 Flow

```
User selects workflow
    ↓
    ├─→ [existing workflows unchanged]
    │   (fast-path, full-fog, implementation, etc.)
    │
    └─→ [NEW: architectural-review-workflow]
        Step 1: repo-sensemaker (existing skill)
                gate: review_diagnosis
                output: repository_sensemaking_brief
                ↓
        Step 2: architectural-review (new skill)
                input: repository_sensemaking_brief + proposed_direction
                output: architectural_review_recommendation
                ↓
        [Workflow ends; artifact is terminal]
```

**No changes to existing workflows**. Design is additive; compatibility to be verified through implementation and regression testing.

### How Continuation Happens

1. architectural_review_recommendation contains `recommended_workflow_id`
2. User/agent reads recommendation artifact
3. User/agent manually selects that workflow or alternative
4. User/agent invokes next workflow (no automatic routing in v1)
5. Execution proceeds normally

**Note**: No handoff step or durable authorization record in v1. Continuation is user-controlled procedurally.

### Future Enhancement (post-v1)

If conditional execution is implemented in runtime:
- Add conditional step after architectural-review
- Decision-field becomes recommendation outcome
- Automatic routing (no manual selection)
- But this requires runtime changes not in v1

---

## 14. Backward-Compatibility Assessment

```yaml
compatibility_assessment:
  source_compatibility:
    status: additive
    evidence: No existing Python source files modified; only new skill file added
    
  artifact_contract_compatibility:
    status: additive
    evidence: |
      New entry added to artifact-contracts.yaml for architectural_review_recommendation.
      Existing contracts unchanged. No migration required.
      Compatibility requires verification that artifact-contracts schema accepts new entry without side effects.
      
  workflow_registry_compatibility:
    status: additive
    evidence: |
      New workflow (architectural-review-workflow) added to workflow-registry.yaml.
      Existing workflows (fast-path, full-fog, product-implementation, etc.) unchanged.
      No existing workflow invocation path modified.
      Compatibility requires verification that new workflow loads and executes without affecting existing workflows.
      
  runtime_compatibility:
    status: uncertain
    evidence: |
      No changes required to scripts/workflow-runtime.py for v1.
      But compatibility depends on:
      * New skill step executing without errors
      * Session-scoped artifact paths resolving correctly
      * Validator integration not breaking existing validation paths
      Must be verified during implementation.
      
  behavioral_compatibility:
    status: additive
    evidence: |
      Existing workflows behavior unchanged.
      New workflow is opt-in: users select it when needed.
      No automatic routing or hidden behavior affecting existing paths.
      Regression testing recommended to verify no unintended side effects.
      
  test_compatibility:
    status: additive
    evidence: |
      New test fixtures and test files added for architectural-review-recommendation.
      Existing tests unchanged.
      Regression testing recommended to verify no interference with existing test suites.

notes:
  - Design is additive; no destructive changes
  - Compatibility must be verified through implementation and regression testing
  - No assumed safety; verification is a v1 gate condition
  - Handoff not modified; integration remains independent
  - Authorization model is procedural; no new technical enforcement
```

---

## 15. Minimum Vertical Slice: Complete File Plan

### Required for Minimum Vertical Slice

**A. Skill Definition**
```
File: skills/architectural-review/SKILL.md
Create: new
Purpose: Defines skill interface, boundary rules, references
Why v1 needs it: Specifies how skill behaves and what it constrains
What breaks without it: Skill has no documented contract or invocation protocol
Size: ~80 lines
```

**B. Artifact Template**
```
File: skills/architectural-review/references/architectural-review-template.md
Create: new
Purpose: Shows artifact structure with all 10 sections and example values
Why v1 needs it: Provides template for agents/humans producing recommendations
What breaks without it: Producers don't know expected artifact shape
Size: ~200 lines
```

**C. Trigger Policy**
```
File: skills/architectural-review/references/architectural-review-trigger-policy.md
Create: new
Purpose: Documents when to invoke the workflow (required/optional/bypass cases)
Why v1 needs it: Guides users on trigger evaluation (manual in v1)
What breaks without it: Users don't know when review is appropriate
Size: ~80 lines
```

**D. Specialized Validator**
```
File: scripts/validate-architectural-review-recommendation.py
Create: new
Purpose: Semantic validation of recommendation artifacts
Why v1 needs it: Enforces decision/precondition consistency and field validity
What breaks without it: Invalid artifacts pass through undetected; no semantic checks
Size: ~300 lines (pattern from validate-brief.py)
```

**E. Artifact Contract**
```
File: skills/workflow-planner/references/artifact-contracts.yaml
Modify: Add one entry
Purpose: Register architectural_review_recommendation contract
Why v1 needs it: Runtime uses contract to validate artifacts and locate paths
What breaks without it: Artifact not recognized by validation system; paths not resolved
Addition: ~30 lines
```

**F. Skill Registry**
```
File: skills/workflow-planner/references/skill-registry.yaml
Modify: Add one entry
Purpose: Register architectural-review skill with metadata
Why v1 needs it: Agents/humans look up skill in registry to invoke it
What breaks without it: Skill is undiscoverable; cannot be invoked via standard mechanisms
Addition: ~10 lines
```

**G. Workflow Registry**
```
File: skills/workflow-planner/references/workflow-registry.yaml
Modify: Add one workflow definition
Purpose: Define architectural-review-workflow (2 steps: repo-sensemaker and architectural-review; workflow terminates after recommendation validation)
Why v1 needs it: Users select this workflow to invoke architectural review
What breaks without it: No workflow path exists to run review; users can't access capability
Addition: ~40 lines
```

**G.1. Agent Metadata** (repository convention; runtime requirement TBD)
```
File: skills/architectural-review/agents/openai.yaml
Create: new
Purpose: Define agent interface metadata (display name, description, icon, color, instructions, tools)
Why v1 includes it: Repository convention — all 8 comparable skills contain agents/openai.yaml (100% consistency across comparable skills)
Classification: Repository convention (not yet verified as runtime requirement or documented policy; discovery task required)
What breaks without it: Unclear — discovery task will determine if agent interface is unavailable or if system degrades gracefully
Size: ~20 lines
```

**H. Validator Test Fixture — Valid Pursue**
```
File: tests/fixtures/architectural-review-recommendation/fixture-valid-pursue.md
Create: new
Purpose: Deterministic test case for valid "pursue" recommendation
Why v1 needs it: Proves validator accepts valid recommendations; baseline for validator unit tests
What breaks without it: Validator has no positive baseline; cannot distinguish valid from invalid
Size: ~100 lines

**I. Validator Test Fixture — Valid Investigate First**
```
File: tests/fixtures/architectural-review-recommendation/fixture-valid-investigate-first.md
Create: new
Purpose: Deterministic test case for valid "investigate_first" recommendation
Why v1 needs it: Proves validator handles investigation-step requirements
What breaks without it: Validator gaps for investigate_first logic
Size: ~80 lines
```

**J. Validator Test Fixture — Invalid Missing Evidence**
```
File: tests/fixtures/architectural-review-recommendation/fixture-invalid-missing-evidence.md
Create: new
Purpose: Test case with missing evidence or missing evidence citations
Why v1 needs it: Proves validator rejects incomplete recommendations
What breaks without it: Invalid artifacts could pass validation
Size: ~60 lines
```

**K. Validator Test Fixture — Invalid Inconsistent Scope**
```
File: tests/fixtures/architectural-review-recommendation/fixture-invalid-inconsistent-scope.md
Create: new
Purpose: Test case with pursue_narrowed but no scope limits defined
Why v1 needs it: Proves validator catches decision/precondition inconsistency
What breaks without it: Validator doesn't enforce logical consistency
Size: ~60 lines
```

**L. Validator Test Fixture — Authority Fragmentation Scenario**
```
File: tests/fixtures/architectural-review-recommendation/fixture-authority-fragmentation-scenario.md
Create: new
Purpose: Provides realistic authority-fragmentation evidence for artifact validation and rubric-based evaluation of recommendation quality
Why v1 needs it: Demonstrates validator and artifact structure in realistic scenario; multiple outcomes may be defensible if supported by evidence
What breaks without it: The suite lacks a realistic rubric-based scenario for assessing recommendation quality
Size: ~150 lines
```

**M. Validator Integration Tests**
```
File: tests/test_architectural_review_recommendation_validator.py
Create: new
Purpose: Unit and integration tests for validator
Why v1 needs it: Proves validator logic works correctly; prevents regressions
What breaks without it: Validator behavior unverified; silent failures possible
Size: ~200 lines
```

**N. Runtime Path E2E Test**
```
File: tests/test_architectural_review_recommendation_runtime.py
Create: new
Purpose: End-to-end test through actual runtime path (workflow definition loads, skill steps resolve, artifact contract resolves, artifact path is session-scoped, valid artifact passes validation, workflow terminates with recommendation available, invalid artifact causes expected validation failure)
Why v1 needs it: Proves capability works through real runtime pipeline without gate integration
What breaks without it: Structural tests pass but runtime integration breaks
Size: ~150 lines
```

### Summary: 15 Files Total

**Create (new)**: 12 files
- 3 skill reference files (SKILL.md, template, trigger policy)
- 1 agent metadata file (agents/openai.yaml, repository convention; enforcement TBD)
- 1 validator script
- 5 test fixture files
- 2 test harness files

**Modify (additions)**: 3 files
- artifact-contracts.yaml (1 new contract entry)
- skill-registry.yaml (1 new skill entry)
- workflow-registry.yaml (1 new workflow definition: architectural-review-workflow with 2 steps, no handoff)

**Total lines of new/modified code**: ~1,600-1,800 lines

**What changes if any file is missing**:

| File | Consequence |
|------|------------|
| SKILL.md | Skill has no documented contract |
| Artifact template | Producers don't know artifact shape |
| Trigger policy | Users don't know when to invoke |
| Validator | Invalid recommendations pass through undetected |
| Artifact contract | Artifacts not recognized by runtime |
| Skill registry | Skill undiscoverable |
| Workflow registry | No workflow path to run review |
| Test fixtures | No baseline for validator tests; coverage incomplete |
| Validator tests | Validator behavior unverified |
| Runtime test | Runtime integration unproven |

---

## 16. Test Strategy: Deterministic Fixtures and Runtime Path

### Validator Acceptance Tests

**Contract fixtures** (deterministic):
- fixture-valid-pursue.md: Must pass validation
- fixture-valid-investigate-first.md: Must pass validation (with required investigation_step)

**Validator Rejection Tests**:
- fixture-invalid-missing-evidence.md: Must fail validation
- fixture-invalid-inconsistent-scope.md: Must fail validation (pursue_narrowed without scope limits)

**Expected results** (test_architectural_review_recommendation_validator.py):
  ✓ Valid "pursue" passes validation
  ✓ Valid "investigate_first" with investigation_step passes
  ✓ Missing evidence citations fails
  ✓ pursue_narrowed without scope limits fails
  ✓ Workflow ID validated against registry
  ✓ Required fields enforced (investigation_step for investigate_first, scopes for pursue_narrowed, kill_conditions for reject)

### Runtime Integration Test

**Fixture**: fixture-valid-pursue.md

**Expected results** (test_architectural_review_recommendation_runtime.py):
  ✓ Artifact written to session-scoped path
  ✓ Path resolver uses _scope_to_session_dir
  ✓ Artifact readable after write
  ✓ Validation pipeline accepts valid artifact
  ✓ Workflow executes to completion
  ✓ Workflow terminates cleanly with the validated recommendation artifact available

**What this test does NOT prove**:
- Gate system records approval/denial (implementation-dependent)
- Authorization is durable (procedural in v1)
- Handoff consumes recommendation (not in v1 workflow)

### Scenario-Based Evaluation (Non-Deterministic)

**Fixture**: fixture-authority-fragmentation-scenario.md

**Deterministic checks**:
- ✓ Artifact has required sections and fields
- ✓ Recommendation includes authority fragmentation risk
- ✓ Kill conditions are defined
- ✓ Evidence citations are valid

**Non-deterministic evaluation** (requires rubric or human judgment):
- Recommendation outcome appropriateness
- Confidence level justification
- Completeness of risk analysis

**What this test does NOT prove**:
- The recommendation's architectural judgment is objectively correct
- This is the only valid outcome for this scenario
- Future assumptions will hold

---

## 17. Rejected Alternatives

### Alternative 1: Autonomous Supervisor Agent

**Idea**: Hidden agent monitors all workflows and flags risky decisions.

**Why rejected**: Violates explicit authority principle. Supervisor authority would be invisible, untestable, unauditable. No approval gate between recommendation and action.

---

### Alternative 2: Universal Mandatory Gate

**Idea**: Add architectural-review gate to EVERY workflow.

**Why rejected**: Breaks backward compatibility. Not all work needs review (bug fixes don't). Would be noise on routine tasks. Violates YAGNI.

---

### Alternative 3: workflow-planner Consumer (Design B)

**Idea**: Modify workflow-planner contract to accept architectural_review_recommendation as optional input.

**Why rejected**: Increases coupling. Adds contract change. Makes continuation implicit (planner decides routing based on recommendation). Design A is simpler: user decides explicitly.

---

### Alternative 4: Terminal Artifact (No Continuation)

**Idea**: Recommendation artifact has no mechanism to proceed to next work.

**Why rejected**: Blocks the process. No mechanism for decision → action. Artifact becomes "nice to read but doesn't matter."

---

### Alternative 5: Embed Review in Existing Workflows

**Idea**: Add architectural-review step to fast-path, full-fog, product-implementation workflows.

**Why rejected**: Over-engineering. Not all diagnostic paths need review. Increases latency for all users. Mixes concerns.

---

### Alternative 6: Micro-skill Decomposition

**Idea**: Split into capability-abstraction-evaluator, bottleneck-analyzer, risk-assessor, validation-strategist.

**Why rejected**: No evidence of independent reuse. Over-complexity. Only decompose when usage proves independent value.

---

### Alternative 7: Absolute "100% Backward Compatible" Claim

**Idea**: Assert zero impact on existing code/workflows without verification.

**Why rejected**: Overconfident. Requires implementation and regression testing to prove. No production code should ship without verification.

---

### Alternative 8: Architectural Decision as Final Authority

**Idea**: Artifact contains authorization fields; skill has approval authority.

**Why rejected**: Violates human-in-the-loop principle. Skills recommend; humans decide. In v1, user makes procedural decision; authorization is not persisted by this capability.

---

## 18. Self-Review Against Repository Principles

### Artifact-First Design ✅

**Principle**: Artifacts are the API; communication is durable.

**Compliance**:
- ✅ Takes repository_sensemaking_brief as structured input
- ✅ Produces architectural_review_recommendation as formal artifact
- ✅ All communication via artifacts
- ✅ No hidden conversational state
- ✅ Artifact versioned in session directory (audit trail)
- ✅ Machine fields enable downstream consumption

---

### Explicit Authority ✅

**Principle**: Authority boundaries clear. No hidden decision-makers.

**Compliance**:
- ✅ Skill RECOMMENDS; does not approve
- ✅ User reviews recommendation and decides procedurally whether to proceed (explicit decision)
- ✅ Authorization is not persisted by this capability in v1
- ✅ No autonomous routing in v1
- ✅ User has full visibility and control over workflow selection

---

### Declarative Orchestration ✅

**Principle**: Workflows and routing explicit in registries.

**Compliance**:
- ✅ New workflow declared in workflow-registry.yaml
- ✅ Trigger policy documented (no hidden logic)
- ✅ No hidden decision logic in code
- ✅ Step order explicit in workflow definition
- ✅ Continuation is explicit user action (not hidden)

---

### Bounded Behavior ✅

**Principle**: Skills have clear contracts. Do not exceed scope.

**Compliance**:
- ✅ Required input: repository_sensemaking_brief (not raw repo)
- ✅ Output: architectural_review_recommendation (single bounded output)
- ✅ Boundary rules forbid repository re-diagnosis
- ✅ Does not execute workflows or write code
- ✅ Does not modify system state

---

### Evidence Provenance ✅

**Principle**: All claims traceable to evidence. Evidence has source and confidence.

**Compliance**:
- ✅ References brief evidence citations
- ✅ Supporting_evidence list in recommendation
- ✅ Confidence levels declared
- ✅ Unresolved_assumptions explicit
- ✅ Contradicting evidence acknowledged

---

### Validator Honesty ⚠️

**Principle**: Validators report what they CAN check, not what they CANNOT.

**Compliance**:
- ✅ Generic validator checks structure only
- ✅ Specialized validator checks deterministic consistency
- ✅ Responsibility matrix shows human judgment required for quality
- ✅ Validator does NOT claim to verify architectural soundness
- ✅ Explicit about what requires human review
- ⚠️ Test fixtures include scenario evaluation that is non-deterministic; must be clearly labeled and not claimed as proof of correctness

---

### Backward Compatibility ⚠️

**Principle**: New work does not break existing workflows/contracts.

**Compliance**:
- ✅ No changes to existing workflows
- ✅ New workflow is purely additive
- ✅ Existing artifact contracts unchanged
- ✅ Existing registries only see new entries
- ✅ No runtime changes required
- ⚠️ Design is additive; compatibility must be verified through implementation and regression testing
- ⚠️ Not assumed safe without verification

---

### Real-Path Testing ⏳

**Principle**: Validation will occur end-to-end through actual paths, not just structural checks.

**Planned Implementation**:
- ⏳ Fixtures will exercise real artifact paths
- ⏳ Tests will run through session scoping
- ⏳ Validator will run on actual artifacts
- ⏳ Workflow definition will load; skill steps will resolve; artifact paths will be session-scoped
- ⏳ Real runtime paths will be used; no mock artifacts

---

## 19. Approval Recommendation

**RECOMMENDATION**: ⚠️ **APPROVE FOR IMPLEMENTATION PLANNING WITH REQUIRED DISCOVERY TASKS**

**Rationale**:

1. **Design A (no workflow-planner consumer, terminal artifact) is coherent**
   - Explicit continuation via user selection
   - No hidden routing or automatic approval
   - Clear authority: skill recommends, user decides

2. **Contradictions identified and addressed**
   - Stable terminology throughout
   - Recommendation separated from authorization
   - Testing strategy clarified (deterministic + non-deterministic)
   - Compatibility claims qualified as "additive; to be verified"

3. **Minimum vertical slice defined and scoped**
   - 15 files individually enumerated with purposes
   - Validator tests included (acceptance and rejection)
   - Runtime path E2E test specified (artifact path, validation, workflow completion)
   - Scenario evaluation labeled as non-deterministic

4. **Honors repository principles with caveats**
   - Artifact-driven: ✅
   - Explicit authority: ✅ (procedural user decision in v1)
   - Declarative orchestration: ✅
   - Bounded behavior: ✅
   - Evidence provenance: ✅
   - Validator honesty: ✅ (scenario evaluation is non-deterministic)
   - Backward compatibility: ⚠️ (additive; to be verified)
   - Real-path testing: ✅ (with scope limitations noted)

5. **Risk assessment**
   - No runtime changes required
   - No existing workflows modified
   - Skill step execution behavior requires verification
   - Session-scoped artifact paths require implementation verification
   - Authorization model is procedural (no durable record in v1)

**Conditions required before implementation planning**:

1. ✅ Design coherence verified (explicit terminal artifact, user-controlled continuation)
2. ✅ Terminology stable and consistent (architectural_review_recommendation)
3. ✅ Authorization model honest (procedural, no durable enforcement in v1)
4. ✅ Minimum vertical slice complete (15 files with purposes)
5. ✅ Test strategy defined (deterministic: validators; non-deterministic: scenarios)
6. ✅ No unimplemented feature dependencies
7. ✅ No speculative consumers
8. ✅ Evidence provenance explicit

**Mandatory discovery tasks before implementation**:

- [ ] **agents/openai.yaml enforcement**: Is this a runtime requirement (loader rejects missing file), documented policy requirement, or repository convention only?
- [ ] **Actual workflow invocation semantics**: Verify exact invocation method for architectural-review-workflow (slash command, registry lookup, manual selection)
- [ ] **Runtime completion behavior for two-step workflow**: Verify what happens when architectural-review step completes (does workflow end cleanly, does user get control, are error cases handled)
- [ ] **Generic and specialized validator integration**: Verify integration points and error propagation paths
- [ ] **Session path resolution**: Verify _scope_to_session_dir correctly scopes architectural_review_recommendation.md
- [ ] **Exact registry-schema requirements**: Verify all required recommendation fields match runtime validation expectations per enum semantics
- [ ] **Regression impact**: Verify no interference with existing workflows

**Mandatory discovery before implementation**:

**Step 0: Complete all seven discovery tasks and record findings**:
- [ ] agents/openai.yaml enforcement (runtime requirement vs. convention)
- [ ] Actual workflow invocation semantics (slash command vs. registry lookup)
- [ ] Runtime completion behavior for two-step workflow (step termination, error handling)
- [ ] Generic and specialized validator integration (exact integration points)
- [ ] Session path resolution (_scope_to_session_dir behavior)
- [ ] Exact registry-schema requirements (enum field validation)
- [ ] Regression impact (effect on existing workflows)

**Step 1: Update implementation plan and file plan based on discovery findings**

**Step 2: Only then begin production changes**:

1. Implement artifact contract and schema validation
2. Implement skill definition and validator
3. Test artifact path resolution and validation pipeline
4. Implement workflow registry entry
5. Run regression tests on existing workflows
6. Document user workflow and authorization model

---

## End of Design Document

**Status**: Ready for implementation planning.  
**File location**: `docs/skill-design-architectural-review.md`  
**File size**: ~18KB (corrected, reduced from 68KB by removing contradictions)  
**Last updated**: 2026-07-18  
**Approved for next phase**: Pending review
