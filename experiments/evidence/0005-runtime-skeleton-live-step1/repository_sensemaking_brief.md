# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-25T19:18:57.351934Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

The sensemaking-skills repository implements an **agent-native orchestration framework** that diagnoses repository uncertainty (fog classification) and routes agents to implementation workflows. The system automates the transition from "what's the problem?" (diagnostic phase) to "what do we do?" (implementation phase) through artifact-driven engineering and skill-led agent orchestration.

**Primary Mission**: Enable AI agents to autonomously diagnose complex repositories, classify uncertainty into four fog types (product_fog, ui_fog, docs_fog, architecture_fog), and recommend specialized implementation workflows based on empirical code analysis.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

**Key Components**:
- **4 Canonical Fog Types**: product_fog, ui_fog, docs_fog, architecture_fog (vocabulary defined in docs/canonical-vocabulary.yaml)
- **Skill-Based Orchestration**: 10+ skills in Python (repo-sensemaker, workflow-planner, handoff, problem-framer, usage-researcher, docs-aligner, unknowns-mapper, skill-maintainer, architectural-review, implementation-coordinator)
- **Unified Validation System**: Five validators producing identical JSON structure (error_id, error_type, field, message, suggested_fixes)
- **Artifact-Driven API**: All skills communicate via validated Markdown artifacts (repository_sensemaking_brief, workflow_orchestration_plan, architectural_review_report, implementation_plan)
- **Bootstrap Skill** (using-sensemaking): ~600 lines teaching fog classification, 3-step diagnosis, error handling, bounded retry (max 3 attempts), graceful escalation
- **SessionStart Hook**: Automatically surfaces bootstrap skill to agents
- **13 Architecture Decision Records**: Documenting fog classification, artifact-driven engineering, soft-context routing, validation modes, workflow composition
- **Helper Scripts**: validate-and-report.py, record-validation.py, workflow-runtime.py
- **Test Infrastructure**: Phase 4.1-4.5 test framework; 5 scenarios tested; Scenario 1 (happy path) and Scenario 5 (budget exhaustion) proven
- **PyPI Distribution**: sensemaking-skills v0.2.1, installable via pip
- **Complete Documentation**: README, CONTEXT.md (11 orchestration principles), GETTING_STARTED.md, EXTENDING.md, operator runbooks, deployment checklists

**Project Phase**: Phase 4 complete (diagnostics proven); Phase 2+ implementation workflows defined but not empirically tested end-to-end at scale.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

**What's Working Excellently**:
- ✅ **Phase 4 Complete & Production Approved** (2026-05-25): All testing phases passed; system approved for production deployment
- ✅ **Proven Agent Behavior (Phase 4.1)**: Fresh agents successfully complete end-to-end diagnostic workflow (happy path and failure path tested)
- ✅ **Bounded Retry Logic Verified**: Agents correctly respect 3-attempt budget, escalate gracefully when exhausted (Scenario 5 passed)
- ✅ **Critical Bug Fixed**: workflow-planner.py now honors escalation_recommended flag; routing accuracy improved from 50% to 100%
- ✅ **Edge Cases Handled (6 Scenarios)**: Large repos (500 files), mixed signals (4-way fog tie), weak evidence, performance tests all pass
- ✅ **Performance Exceeds SLOs**: workflow-planner <300ms, brief validation <500ms, full pipeline <10s
- ✅ **Unified Validation Schema**: All validators produce consistent JSON structure
- ✅ **Bootstrap Skill Comprehensive**: ~600 lines covering 4 fog types, 5 error types, 3-step diagnosis, retry logic
- ✅ **Artifact-Driven Contract**: Field names declared in artifact-contracts.yaml; producers and consumers aligned
- ✅ **Durable Audit Trail**: validation_run_log.md records every attempt with timestamps and error metadata
- ✅ **ADRs Document Everything**: 13 ADRs exhaustively explain design decisions
- ✅ **Operator Runbooks Complete**: 10+ sections covering diagnostics, troubleshooting, escalation, performance tuning, disaster recovery
- ✅ **Deployment Ready**: 3-week rollout plan documented (Shadow → Pilot → GA)

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

**What's Not Yet Implemented or Complete**:
- ⚠️ **Phase 2+ Multi-Phase Orchestration Unproven**: Four specialty workflows (product-implementation, ui-implementation, docs-implementation, architecture-implementation) are defined and theoretically sound, but end-to-end orchestration with real agents has not been tested
- ❌ **Very Large Repository Handling (10k+ files)**: System may fill context window; escalation is mitigation but not empirically tested
- ❌ **CI/CD Integration Examples**: Deployment checklists exist but no step-by-step GitHub Actions / GitLab CI / Jenkins examples
- ❌ **Custom Workflow Extension Guide**: ADR explains patterns; step-by-step "add a new workflow" guide missing
- ❌ **Auto-Remediation**: System recommends workflows but doesn't generate fix PRs automatically
- ❌ **Portfolio-Level Analysis**: Single-repository focus; cross-repository issue correlation not implemented
- ⚠️ **Soft-Context Routing Edge Cases**: Tie-breaking when multiple fog types equally plausible relies on user intent; heuristic refinement needed

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Add visual decision tree for "which fog type am I looking at?" to bootstrap skill
- Document concrete runbook for agents receiving "insufficient evidence" error
- Provide CLI examples for running Phase 4 test scenarios manually (reproducibility)
- Create "skill extension cookbook" with worked examples (e.g., adding new validation rules)
- Publish deployment playbook for practitioners (wiki / blog post)
- Add performance dashboards template for operations teams
- Expand examples/skill-tests with real-world codebases (currently test-fixture heavy)
- Add tracing/debugging guide for agents stuck in error loops

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Primary Weakness**: The practical end-to-end orchestration of **all 4 implementation workflows at scale** has not been empirically proven with real agents.

**Specifically**:
- Phase 1 diagnostics are proven (agents can read skill, classify fog, produce valid brief)
- workflow-planner routing is proven (100% accuracy after bug fix)
- Individual workflow steps exist and have unit tests
- **But**: No empirical evidence that an agent can:
  1. Accept vague user intent
  2. Execute diagnostic workflow to completion
  3. Get routed (e.g.) to architecture-implementation-workflow
  4. Execute multi-phase implementation (scan → identify → propose → validate)
  5. Handle validation failures across phases with bounded retry
  6. Escalate gracefully when budget exhausted
  7. Produce final artifact (e.g., ARCHITECTURE_REVIEW.md)

**The gap**: Individual pieces work. Full chain at scale is untested. This is the **integration boundary**.

**Weakness Type: Architecture Fog** — System design is sound and well-documented, but the practical end-to-end execution path (multi-phase orchestration) is theoretically proven but empirically unvalidated.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

**Evidence Summary**:
The repository demonstrates:
- ✅ Complete Phase 1 infrastructure (diagnostic skills, unified validators, bootstrap, hook)
- ✅ Complete Phase 2 infrastructure (CLI, PyPI distribution)
- ✅ Complete Phase 3 framework (operator runbooks, deployment checklists)
- ✅ Complete Phase 4 testing (agent behavior proven for diagnostics only)
- ✅ Theoretical soundness (13 ADRs document architecture)
- ✅ Empirical proof of Phase 1 (Scenario 1 happy path passes)
- ❌ Empirical proof of Phase 2-4 multi-phase orchestration

**Logic Trace**: sensemaking-skills has successfully built and tested a **diagnostic phase** (Phase 1: agent reads skill, classifies fog, produces valid brief) and **routing layer** (Phase 2: workflow-planner reads brief, selects workflow with 100% accuracy). However, **implementation phases** (Phase 3-4: multi-step orchestration across four fog-type workflows) are defined with unit tests, but have NOT been executed end-to-end with real agents.

Phase 4.1 testing proves diagnostic workflows work: agents autonomously complete repo-sensemaker → brief → validation → workflow-planner → plan → validation without intervention. The phase also proves error handling works (bounded retry, graceful escalation).

**The Gap**: No end-to-end test demonstrates that an agent can start with user intent, run diagnostics, get routed to (say) architecture-implementation-workflow, then successfully execute a multi-phase implementation sequence and produce a final artifact.

This is not a documentation gap or missing feature—it's an **architectural integration question**: Does the orchestration design work when real agents attempt it? The design is sound (13 ADRs prove this). Individual pieces work (Phase 4.1 proves this). But the full chain at scale is untested.

<!-- MODEL_SECTION:evidence_prose:END -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
```yaml
evidence_excerpts:
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 1-20
    quote: "System has completed all Phase 4 testing and verification. Phase 4.1 Fresh-agent behavior test PASS. Critical bug fixed: workflow-planner.py now honors escalation_recommended flag. Routing accuracy improved from 50% to 100%."
    supports_claim: "Phase 1 diagnostics proven; routing accuracy fixed"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 40-65
    quote: "Agent reads bootstrap skill, follows diagnostic skill, diagnoses repository autonomously, produces valid brief, brief validation passes first attempt, agent creates orchestration plan, plan validation passes first attempt, end-to-end diagnostic + planning completes without intervention."
    supports_claim: "Happy path workflow proven with fresh agent"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 42-56
    quote: "Scenario 5 Budget Exhaustion: Agent encounters validation failure, reads error message, applies fix, retries, recognizes different error on attempt 3, respects 3-attempt budget, does not attempt 4th retry, escalates gracefully. Bounded retry logic proven working."
    supports_claim: "Failure path and escalation logic proven"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 69-84
    quote: "Performance baselines: workflow-planner execution 0.287s (target <5s), brief validation 0.412s (target <1s), plan validation 0.398s (target <1s), total automation ~1.1s (target <10s). All metrics EXCELLENT."
    supports_claim: "Performance exceeds SLOs"
  
  - file: CONTEXT.md
    lines: 99-117
    quote: "Skill-led orchestration: Agents own control loop, read bootstrap skill, understand fog classification, invoke skills via Skill tool, read artifacts, parse validator errors, decide next step. Evidence model: durable artifacts prove outputs, validators prove contracts, run ledgers prove causal chain."
    supports_claim: "Architecture is sound and well-specified"
  
  - file: README.md
    lines: 8-11
    quote: "Status: Beta (Scenario 5 tested and proven). Production-ready for agent-based use. Proven diagnostic framework."
    supports_claim: "Phase 1 production-ready; Phase 2+ unproven"
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

If full-chain orchestration remains unproven:

1. **Unknown whether Phase 2+ is agent-usable** — Implementation workflows are defined but agents may not naturally follow multi-phase sequences
2. **Silent failures in production deployment** — Agents might succeed at diagnosis but fail at implementation phases, producing partial artifacts downstream
3. **Deployment risk underestimated** — Production rollout assumes full chain works; if it doesn't, rollout must pause or rollback
4. **Maintenance burden on operators** — If agents get stuck in implementation phases, escalation procedures will be exercised frequently and runbooks may be insufficient
5. **Wasted effort on Phase 5+ features** — Portfolio analysis, CI/CD integration, auto-remediation all assume Phase 2-4 are robust; testing would validate this
6. **No evidence of real-world complexity** — Test fixtures are clean; real codebases have conflicting signals, insufficient evidence, ambiguous architecture. End-to-end testing would surface these edge cases

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. **Execute Phase 4.2: Full-Chain Agent Test** — Run fresh agent on real codebase with clear architecture_fog signals, routing to architecture-implementation-workflow, completing multi-phase orchestration
2. **Capture full transcript and artifacts** — Record every step including validation results, error handling, escalation if triggered
3. **Test multi-phase error handling** — Use Scenario 5 (budget exhaustion) to verify bounded retry works across workflows and phases
4. **If Phase 4.2 passes, test all 4 implementation workflows** — Execute agents on product_fog, ui_fog, docs_fog, architecture_fog repositories
5. **If any workflow fails, identify root cause** — Skill issue? Validation? Orchestration? Fix at lowest scope
6. **Establish CI/CD automation** — Once proven, automate Phase 4.2 so regressions are caught immediately

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

**Execute Phase 4.2: Full-Chain Agent Test (Multi-Phase Orchestration)**

**Why**: Infrastructure is ready. Individual components are proven. What's needed is empirical execution of the full orchestration chain.

**Test Setup**:
- Pick a real repository (not test fixture) with clear architecture_fog signals
- Run diagnostic workflow → get routed to architecture-implementation-workflow
- Execute multi-phase implementation sequence
- Capture artifacts and validation results

**Success Criteria**:
- ✅ All phases complete without manual intervention
- ✅ All artifacts pass validation on first attempt
- ✅ workflow-planner correctly routes to architecture-implementation-workflow
- ✅ Implementation workflow produces valid final artifact (e.g., ARCHITECTURE_REVIEW.md)
- ✅ Performance remains within SLOs (<10s total automation, <30min full pipeline)

**Expected Outcome**: Empirical proof that full orchestration chain works, enabling confident production deployment and Phase 5 (portfolio analysis).

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

**Prompt for Architecture Implementation Workflow Testing**:

```
You are testing the sensemaking-skills orchestration framework. Your task:

1. Read the bootstrap skill at skills/using-sensemaking/SKILL.md
2. Execute the repo-sensemaker skill to analyze this repository
3. Create repository_sensemaking_brief.md with your analysis
4. Validate the brief using scripts/validate-and-report.py
5. Run workflow-planner to determine recommended implementation workflow
6. Create workflow_orchestration_plan.md
7. Validate the plan
8. If recommended workflow is architecture-implementation-workflow, execute it end-to-end
9. Capture all artifacts and validation results

Success means: All artifacts valid on first attempt, workflow-planner recommends architecture-implementation-workflow, implementation workflow completes without manual intervention, final artifact (ARCHITECTURE_REVIEW.md) is valid.

Budget: Max 3 attempts per phase. Escalate gracefully if budget exhausted.
```

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: architecture_fog
primary_fog_type: architecture_fog
diagnosis_conflict: False
escalation_recommended: True
evidence:
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 1-20): Phase 4 complete and approved; diagnostics proven"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 40-65): Fresh agent happy path passes end-to-end"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 42-56): Budget exhaustion and escalation logic proven"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 69-84): Performance exceeds all SLOs"
  - "CONTEXT.md (lines 99-117): Skill-led orchestration architecture sound"
  - "README.md (lines 8-11): Phase 1 production-ready; Phase 2+ unproven"
  - "src/sensemaking_skills/skills/workflow_planner.py: Critical escalation bug fixed; routing accuracy 50% -> 100%"
recommended_workflow_id: architecture-orchestration-validation
recommended_execution_mode: autonomous_execution
weakest_boundary: unproven_multi_phase_orchestration
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-25T19:18:57.351934Z"
immutable: true
```
