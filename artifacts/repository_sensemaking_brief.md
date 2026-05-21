# Repository Sensemaking Brief

## 1. Repository goal

Establish a production-ready **Artifact-Driven Agentic Engineering** platform that converts unstructured user intent ("Fog") into verified, executable orchestration workflows. The system treats agentic automation as a systems engineering discipline, enforcing strict artifact contracts, durable audit trails, and explicit approval gates at every handoff.

The core mission: **Discipline over Magic** — replace ephemeral conversation memory with validated artifacts that serve as the API between autonomous skills.

---

## 2. Current shape

**Core Structure**:
- `skills/`: 14 atomic diagnostic and implementation skills (repo-sensemaker, problem-framer, unknowns-mapper, workflow-planner, docs-aligner, to-prd, to-issues, usage-researcher, skill-maintainer, and others)
- `scripts/`: Python orchestration runtime (workflow-runtime.py), 20+ validators, and execution dispatchers
- `docs/`: Philosophy (artifact-driven engineering, agentic failure modes, ADRs), implementation phases, PRDs, and troubleshooting guides
- `workflows/`: Composite skill chains (fast-path-workflow, full-fog-workflow, docs-architecture, skill-maintenance-loop, experimental-autonomous-sprint)
- `examples/`: Test fixtures, negative validation cases, usage research scenarios, and skill test suites
- `references/`: YAML registries (workflow-registry.yaml, skill-registry.yaml, artifact-contracts.yaml)

**Execution Framework**:
- Multi-mode orchestration: plan_only, prompt_chain, guided_execution, autonomous_execution, yolo_execution
- Approval gates between workflow steps
- Level-1/Level-2/Level-3 validators for structural, semantic, and evidence-based validation
- Intent propagation system: Every artifact references source_intent_ref to user's original problem statement
- Auto-invocation of downstream workflows based on orchestration plans

**Recent Completions** (Phase 0–5, as of 2026-05-19):
- User Intent Artifact Contract with immutability enforcement
- Workflow registry updated to require user_intent as first-class input
- All 5 Level-3 validators proven in live workflows
- Skill invocation framework complete (enables yolo_execution mode)
- Parallel execution working across 2–5 concurrent workers
- Intent propagation validation proven across 21+ independent runs with zero repeatable failures

---

## 3. Strong signals

1. **Artifact-Driven Philosophy Proven**: Durable YAML/Markdown contracts replace ephemeral chat memory. Every skill output validated before handoff.
   - Evidence: docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md + 21 live runs with zero repeatable failures

2. **Comprehensive Validator Stack**: 20+ validators covering structural, semantic, and evidence-based validation.
   - Evidence: validate-brief.py, validate-plan.py, validate-prompt-handoff.py, validate-run-log.py, validate-skill-improvement-plan.py, validate-usage-research-report.py
   - All 5 Level-3 validators proven in Phase 5 (May 2026)

3. **Multi-Mode Execution**: All 5 execution modes implemented and proven production-ready.
   - 4 of 5 modes (plan_only, prompt_chain, guided_execution, autonomous_execution) verified with zero repeatable failures
   - yolo_execution proven on skill-maintenance-loop workflow (Phase 5)

4. **Registry-Based Routing**: Machine-readable workflow and skill registries enable deterministic, auditable workflow selection.
   - Evidence: workflow-registry.yaml (14 workflows), skill-registry.yaml (40+ skills), artifact-contracts.yaml (25+ contracts)
   - 100% classification accuracy for project routing (per VERDICT-SUMMARY.md)

5. **Intent-Aware System**: User intent captured at entry, propagated through all artifacts, auditable at every step.
   - Evidence: User intent artifact contract with source_intent_ref required in all downstream artifacts
   - Immutability enforcement prevents intent drift

6. **Safety & Audit Trails**: Every skill execution recorded in TEST-RUN-LOG.md with reasoning, evidence, and gate decisions.
   - Evidence: examples/skill-tests/quarantine/ + VERDICT-SUMMARY.md validation runs

7. **Parallel Execution Framework**: Skills can run concurrently with isolated path enforcement.
   - Evidence: Phase 5 skill invocation framework + portfolio-orchestrator.py for multi-project management

---

## 4. Missing pieces

1. **Product Manager Skills Integration**: The repo assumes optional external skill packs (Product Manager Skills, Matt Pocock Skills, Interface Skills). When not installed:
   - plan_only mode: Produces copy-paste prompts (works)
   - execution modes: Fails with clear error (acceptable but not automated)
   - Evidence: README.md lines 203–213, scripts/skill_executor.py error handling

2. **PRD Artifact Validation in Full Workflow**: docs-architecture workflow claims to produce prd.md but doesn't validate it.
   - Evidence: VERDICT-SUMMARY.md "One Known Gap" section
   - Impact: LOW immediate (PRD not yet needed), MEDIUM future (when product workflows scale)
   - Fix documented in implementation-checklist.md phases 1–4

3. **Semantic Cross-Artifact Validation**: Validators check structure and evidence within artifacts, but not semantic alignment across artifact boundaries.
   - Example: Does problem_frame's "object under pressure" align with repo-sensemaker's weakest boundary?
   - Current state: Manual gate review at each step
   - Future: Automated semantic drift detection

4. **Failure Recovery Automation**: When orchestration gates fail or skills produce invalid artifacts:
   - Current: Workflow halts, user must retry
   - Missing: Auto-remediation suggestions or graceful degradation paths

5. **Local Skill Testing Framework**: Skills are validated in live workflows, but isolated unit test suite is minimal.
   - Evidence: examples/skill-tests/quarantine/ is dense with integration tests, but skills/*/test/ is sparse
   - Current workaround: Usage research scenarios (examples/usage-research/)

---

## 5. Improvement opportunities

1. **Unified Execution Dashboard**: Consolidate run logs, artifact navigation, and gate status into a web UI.
   - Current: Run logs are Markdown files in examples/ or artifacts/
   - Opportunity: Real-time orchestration status, artifact diff viewer, gate decision interface

2. **Skill Performance Metrics**: Track usage research findings (usage-researcher skill output) over time.
   - Current: Each run is isolated; no trending or performance heatmap
   - Opportunity: Identify consistently weak skills, prioritize maintenance, measure improvement ROI

3. **Automatic Workflow Recommendation**: When user intent conflicts with repository diagnosis, suggest escalation to full-fog-workflow automatically.
   - Current: repo-sensemaker produces diagnosis_conflict flag, but orchestrator doesn't auto-escalate
   - Opportunity: Reduce false-positive skill routing

4. **Multi-Language Skill Support**: All skills are currently Claude-prompts-in-Python-runners.
   - Opportunity: Support other model providers (Anthropic batch API, external LLMs) via plugin architecture

5. **Exhaustive Negative Test Suite**: Add more fixture examples for skills to refuse/fail gracefully (examples/negative/).
   - Current: 8 negative fixtures exist; opportunity to expand to cover all fog types and boundary violations

6. **Automated Skill Evolution**: skill-maintainer skill produces improvement plans, but patches are manual.
   - Opportunity: Auto-apply non-breaking improvements, version skill patches, track evolution history

---

## 6. Weakest boundary

**Weakness Type**: Contract Mismatch

**The "Intent-Execution Mismatch Boundary"**: What happens when user intent (expressed at entry) diverges from what the system detects in the repository?

**Specific vulnerability**: 
- User says: "We need a UI redesign" (ui_fog)
- Repository signals: "State management is broken" (architecture_fog)
- System routes to: docs-architecture workflow (architecture focus)
- Result: User sees recommendations for code refactoring, not UI mockups
- Risk: User frustration, context-switching costs, recommendation ignored

**Why this boundary exists**:
- repo-sensemaker detects fog type from code structure, not from user words
- workflow-planner routes based on codebase diagnosis, not user expectation
- No automated escalation to full-fog-path when conflict is detected
- Gate review (human approval) is the only safeguard

**Evidence**: 
- Stage 1 Intent-Aware Analysis in repo-sensemaker SKILL.md (lines 10–36) describes the conflict detection but implementation is incomplete
- VERDICT-SUMMARY.md shows workflows executing as planned; no evidence of conflict detection rejection
- workflow-planner SKILL.md has no explicit handling for diagnosis_conflict=true

**Why it matters**:
If a user's mental model of the problem doesn't match the repository's actual problem, recommendations will miss the mark. In autonomous workflows, this could silently route work to the wrong team.

### Logic Trace

The diagnostic reasoning for identifying this weakest boundary follows a chain of observations about the artifact-driven engineering system:
1. **Observation**: User intent is captured at entry (raw_problem_statement) but downstream skills only see the repository state, not the user's original framing.
2. **Inference**: When intent and codebase diagnosis diverge, no automated mechanism reconciles them — the conflict flag (diagnosis_conflict) exists but is never consumed.
3. **Connection**: The workflow-planner routes solely on codebase diagnosis (fog type from repo-sensemaker) and never compares it against user intent.
4. **Conclusion**: The system has a **Contract Mismatch** between what user intent promises (personalized routing) and what the routing logic delivers (codebase-only routing).

---

## 6.5. Problem classification (fog type)

**Primary fog type**: **architecture_fog** (with **product_fog** secondary concern)

**Classification reasoning**:
1. The repository itself is about orchestrating agentic workflows, not about any specific product's architecture
2. Core "weakest boundaries" relate to:
   - Intent-execution mismatch (design flaw in routing logic)
   - Cross-artifact semantic validation (missing architectural layer)
   - Skill invocation automation (orchestration architecture gap, now closed in Phase 5)
   - PRD artifact lifecycle (workflow architecture gap, identified in VERDICT-SUMMARY)

3. However, there's a secondary **product_fog** signal:
   - Unclear which downstream skill packs (PM, Interface, Matt Pocock) are "first-class" vs. "optional"
   - Undocumented product decision about when to route to product-implementation-workflow vs. docs-architecture
   - Missing user research on skill ecosystem adoption

**Conclusion**: Treat as **architecture_fog** (repo structure/boundaries) with advisory note to consider product clarity as a near-term refinement.

---

## 7. Evidence

**File-level evidence supporting diagnosis**:

| Finding | File(s) | Lines | Strength |
|---------|---------|-------|----------|
| Intent-execution mismatch is a detected but unhandled gap | skills/repo-sensemaker/SKILL.md | 10–36, 42–49 | High |
| All validators proven and working in Phase 5 | docs/PHASE5_SKILL_INVOCATION.md | 44–79 | High |
| PRD artifact not being validated in full workflows | docs/VERDICT-SUMMARY.md | 67–78 | High |
| Semantic cross-artifact validation missing | docs/philosophy/AGENTIC_FAILURE_MODES.md | (Handoff Failure class) | Medium |
| Parallel execution framework complete | scripts/portfolio-orchestrator.py, Phase 5 summary | – | High |
| Intent propagation proven | docs/IMPLEMENTATION-COMPLETE-phases-0-5.md | 50–78 | High |
| Multi-mode execution all proven | docs/VERDICT-SUMMARY.md | 89–99 | High |
| Skill routing 100% accurate on test set | docs/VERDICT-SUMMARY.md | 13 | Medium |
| Usage research scenarios capture real edge cases | examples/usage-research/scenarios/ | – | Medium |

---

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/SKILL.md
    lines: L26-L35
    quote: "Detect Conflicts: If user intent != codebase diagnosis, flag it"
    supports_claim: "Conflict detection defined but not handled in workflow-planner"

  - file: docs/PHASE5_SKILL_INVOCATION.md
    lines: L53-L79
    quote: "All 5 Level-3 validators triggered and validated successfully in Phase 5"
    supports_claim: "Validators are proven working across the stack"

  - file: docs/VERDICT-SUMMARY.md
    lines: L67-L78
    quote: "docs-architecture produces prd.md claim but doesn't validate it"
    supports_claim: "PRD lifecycle gap exists in the artifact pipeline"

  - file: docs/IMPLEMENTATION-COMPLETE-phases-0-5.md
    lines: L133-L149
    quote: "Artifact contracts updated to require source_intent_ref across all major artifacts"
    supports_claim: "Intent propagation system is working correctly"
```

---

## 9. Why this boundary matters

**Short-term (Next 2-4 weeks)**:
If intent-execution mismatch boundary isn't addressed, user-initiated workflows may route to incorrect downstream skills. Example: User problem "Improve dashboard UX" gets routed to docs-architecture (architecture fog) instead of ui-implementation-workflow. User receives code refactoring recommendations instead of UI mockups.

**Medium-term (Months 2-3)**:
As skill ecosystem scales and more workflows auto-invoke:
- Systems that silently mis-diagnose fog type accumulate broken recommendations
- Users lose trust in routing logic
- Manual gate reviews become necessity, defeating automation value

**Long-term (Operational risk)**:
In fully autonomous mode (yolo_execution):
- No human gate at conflict detection
- Misrouted work escalates in parallel workflows
- Portfolio orchestrator can amplify bad routing decisions across multiple projects

**Mitigation status**:
- Conflict detection logic is defined in repo-sensemaker SKILL.md but not enforced upstream
- workflow-planner has no explicit rejection rule for diagnosis_conflict=true
- No evidence of conflict escalation in any live workflow run

---

## 10. Candidate next steps

1. **Implement Intent-Conflict Escalation** (Highest Priority)
   - Update workflow-planner to detect diagnosis_conflict=true
   - Auto-escalate to full-fog-workflow if conflict is high-confidence
   - Add gate override allowing user to acknowledge conflict and proceed anyway
   - Estimated effort: 2–3 hours

2. **Fix PRD Artifact Lifecycle** (High Priority)
   - Move to-prd skill out of docs-architecture workflow
   - Create product-to-issues workflow that consumes PRD as input
   - Update workflow-registry.yaml and artifact-contracts.yaml
   - Estimated effort: 4–6 hours

3. **Implement Semantic Cross-Artifact Validator** (Medium Priority)
   - Check alignment between problem_frame and repo-sensemaker outputs
   - Flag if language suggests different system boundaries
   - Add as Level-2 validator
   - Estimated effort: 6–8 hours

4. **Expand Negative Test Suite** (Medium Priority)
   - Add fixtures for intent-conflict scenarios, semantic misalignment, skill refusing work
   - Create documented refusal-to-act examples
   - Estimated effort: 4–5 hours

5. **Measure Skill Adoption & Performance** (Lower Priority)
   - Build trending dashboard from usage-researcher output
   - Track fog types, routing accuracy, skill failure rates
   - Estimated effort: 8–10 hours

---

## 11. Recommended next step

**Implement Intent-Conflict Escalation** — the highest-leverage, lowest-risk action that directly addresses the weakest boundary.

**Why**:
- Directly fixes the intent-execution mismatch vulnerability
- Minimal code changes (update 1 skill definition + 1 validator check)
- Zero breaking changes to existing workflows
- Enables safe auto-invocation of downstream workflows
- Builds confidence in yolo_execution mode for future autonomous sprints

**Concrete action**:
1. Update `skills/workflow-planner/SKILL.md` to add gate logic: "If diagnosis_conflict=true, recommend full-fog-workflow instead of fast-path recommendation"
2. Add check in workflow-planner validation: Flag as escalation_recommended if conflict detected
3. Add test fixture: `examples/negative/workflow-planner-conflict-escalation.md`
4. Run through guided_execution mode to verify gate behavior

**Expected time**: 2–3 hours (including tests)

---

## 12. Recommended workflow

`skill-maintenance-loop` (if treating repo itself as the project)

OR

`fast-path-workflow` (if user is running diagnostics on another repository)

**For this repository's self-improvement**:
- Use: skill-maintenance-loop (chains usage-researcher → skill-maintainer)
- Input: Repository state + improvement opportunity
- Output: skill_improvement_plan.md with concrete patches
- Execution mode: guided_execution (review improvements before applying)

**For downstream projects**:
- Recommend: fast-path-workflow (chains repo-sensemaker → workflow-planner → auto-invoke)
- Or: full-fog-workflow (if problem statement is vague)

---

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1.0
created_at: "2026-05-20T00:00:00Z"
created_by: repository_analysis
immutable: true

source_intent_ref: "repository_root"
user_implied_fog_type: architecture_fog
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false

recommended_workflow_id: skill-maintenance-loop
recommended_execution_mode: guided_execution
weakest_boundary: intent_execution_mismatch
required_inputs:
  - repository_state
  - user_intent (optional for self-analysis)

evidence_basis: "21+ live runs (Phase 0-5), VERDICT-SUMMARY analysis, validator coverage matrix"
high_confidence_areas:
  - "All validator infrastructure proven in Phase 5"
  - "Multi-mode execution all operational"
  - "Intent propagation system working across 21 runs"
  - "Zero repeatable failures in 18 analyzed run logs"

low_confidence_areas:
  - "Intent-conflict escalation logic defined but not enforced"
  - "Semantic cross-artifact validation not yet implemented"
  - "Product ecosystem clarity (which external skills are canonical)"

issues_identified:
  - id: intent_execution_mismatch
    severity: high
    status: detected_but_unhandled
    fix_priority: 1
  
  - id: prd_artifact_lifecycle
    severity: high
    status: documented_in_verdict
    fix_priority: 2
  
  - id: semantic_validation_gap
    severity: medium
    status: identified
    fix_priority: 3
```

---

## 14. Ready-to-copy prompt

Use this prompt to invoke `skill-maintenance-loop` or `problem-framer` for follow-up work:

```
# Repository Improvement Task: Intent-Conflict Escalation

Context: The sensemaking-skills repository has proven all validator infrastructure (Phase 5 complete as of 2026-05-19). However, a critical gap exists in the orchestration logic.

Problem: When user intent diverges from repository diagnosis, the system detects the conflict (sets diagnosis_conflict=true in repo-sensemaker output) but does NOT escalate to full-fog-workflow. This risks mis-routing autonomous work.

Example failure scenario:
- User: "We need a UI redesign" (ui_fog)
- System detects: "State management is broken" (architecture_fog)
- Current behavior: Routes to docs-architecture workflow anyway
- Desired behavior: Escalates to full-fog-workflow with user override option

Tasks:
1. Update `skills/workflow-planner/SKILL.md` to add escalation logic for diagnosis_conflict=true
2. Add validator check: `validate-plan.py` flags plans with unescalated conflicts
3. Create test fixture: `examples/negative/workflow-planner-conflict-escalation.md`
4. Test in guided_execution mode and verify gate allows user override
5. Document the escalation rule in `docs/orchestration-patterns.md`

Success criteria:
- Conflicts detected → Recommend full-fog-workflow as primary option
- User can override and proceed with fast-path → Gate explicitly documents trade-off
- Test fixture demonstrates both escalation and override paths
- Zero impact to existing fast-path or full-fog workflows

Estimated effort: 2-3 hours

Next artifact: skill_improvement_plan.md (from skill-maintainer) with patches to workflow-planner and validator stacks
```

---

## Appendix: Key Documents for Reference

- **Philosophy**: docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md
- **Failure Taxonomy**: docs/philosophy/AGENTIC_FAILURE_MODES.md
- **Phase Completions**: docs/IMPLEMENTATION-COMPLETE-phases-0-5.md, docs/PHASE5_SKILL_INVOCATION.md
- **Validation Evidence**: docs/VERDICT-SUMMARY.md
- **Execution Modes**: docs/orchestration-patterns.md
- **Skill Registry**: skills/workflow-planner/references/skill-registry.yaml
- **Workflow Registry**: skills/workflow-planner/references/workflow-registry.yaml
- **Artifact Contracts**: skills/workflow-planner/references/artifact-contracts.yaml
