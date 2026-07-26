# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-07-25T21:04:41.674275Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

The sensemaking-skills repository implements an **agent-native orchestration framework** that transforms repository uncertainty (fog classification) into actionable problem frames and implementation workflows. The system enables AI agents to autonomously diagnose repositories, classify uncertainty into four canonical fog types (product_fog, ui_fog, docs_fog, architecture_fog), and route to specialized implementation workflows based on empirical code analysis.

**Primary Mission**: Provide a meta-routing layer that turns diagnostic artifacts into workflow recommendations, with proven agent autonomy, bounded error recovery, and graceful escalation under computational budget constraints.

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

**Key Components**:
- **Canonical Fog Vocabulary**: Four fog types defined with decision criteria in docs/canonical-vocabulary.yaml
- **Skill-Based Architecture**: 10+ skills implemented in Python (repo-sensemaker, workflow-planner, handoff, problem-framer, usage-researcher, docs-aligner, unknowns-mapper, skill-maintainer, architectural-review, implementation-coordinator)
- **Unified Validation System**: Five validators producing identical JSON structure (error_id, error_type, field, message, suggested_fixes)
- **Artifact-Driven Contracts**: All skills communicate via validated Markdown artifacts with field names declared in artifact-contracts.yaml
- **Bootstrap Skill** (using-sensemaking): ~600 lines teaching fog classification, 3-step diagnosis, 5 error types, error handling, bounded retry logic (max 3 attempts), graceful escalation patterns
- **SessionStart Hook**: Automatically surfaces bootstrap skill reference to agents at session start
- **13 Architecture Decision Records**: Comprehensive documentation of fog classification (ADR 0004), artifact-driven engineering (ADR 0002), soft-context routing (ADR 0007), validation modes (ADR 0001), skill-led orchestration (ADR 0013)
- **Workflow Registry**: 22+ workflows defined including fast-path, full-fog, and 4 implementation workflows (product, ui, docs, architecture)
- **Helper Scripts**: validate-and-report.py, record-validation.py, workflow-runtime.py for orchestration and validation
- **Test Infrastructure**: Phase 4.1-4.5 testing framework with 6 scenarios; Scenario 1 (happy path) and Scenario 5 (budget exhaustion) empirically proven with fresh agents
- **PyPI Distribution**: sensemaking-skills v0.2.1 available on PyPI
- **Complete Documentation**: README with quick-start, CONTEXT.md (13 orchestration principles), GETTING_STARTED.md, EXTENDING.md, operator runbooks (PHASE-4-4-OPERATOR-RUNBOOKS.md), deployment checklists (3-week rollout plan)

**Project Phase**: Phase 1 (diagnostics) and Phase 2 (routing) complete and production-approved. Phase 3-4 (implementation workflows) are defined, unit-tested, but lack empirical end-to-end validation with real agents at scale.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

**What's Working Excellently**:
- ✅ **Phase 4 Complete & Production Approved** (2026-05-25): All testing phases (4.1-4.5) passed; production gate approval signed; 3-week rollout plan ready
- ✅ **Phase 1 Agent Behavior Proven** (Phase 4.1): Fresh agents successfully complete diagnostic workflow end-to-end (happy path) without guidance; artifacts valid on first attempt
- ✅ **Bounded Retry + Graceful Escalation** (Phase 4.1 Scenario 5): Agents respect 3-attempt budget, recognize different errors, escalate when exhausted (does NOT infinite-loop)
- ✅ **Critical Bug Fixed**: workflow-planner.py now honors escalation_recommended flag; routing accuracy improved from 50% to 100%
- ✅ **Edge Case Handling** (Phase 4.3, 6/6 scenarios pass): Large repos (500 files), mixed signals (4-way fog tie), weak evidence, performance testing all pass
- ✅ **Performance Exceeds SLOs** (Phase 4.2): workflow-planner <300ms (target 5s), validation <500ms (target 1s), full pipeline <1.1s (target 10s)
- ✅ **Unified Validation Schema**: All 5 validators produce consistent error JSON; agents can parse uniformly
- ✅ **Bootstrap Skill Comprehensive**: ~600 lines covering 4 fog types, 5 error types, 3-step diagnosis, retry/escalation logic, decision heuristics
- ✅ **Artifact Contracts Enforced**: Field names declared in artifact-contracts.yaml; test_field_contract_agreement.py enforces producer/consumer alignment
- ✅ **Durable Audit Trail**: validation_run_log.md records every attempt with timestamps, error metadata, causal chain
- ✅ **13 ADRs Document Everything**: Fog classification, artifact-driven API, soft-context routing, validation modes, agent orchestration—all decisions documented with rationale
- ✅ **Operator Runbooks Complete**: 10+ sections covering diagnostics, troubleshooting, escalation, performance tuning, disaster recovery, deployment procedures
- ✅ **Rollout Plan Documented**: Week 1 shadow mode, Week 2 pilot (10-20 users), Week 3+ general availability with clear go/no-go criteria

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

**What's Not Yet Implemented or Complete**:
- ⚠️ **Phase 3+ Multi-Phase Orchestration Unproven**: Four implementation workflows (product-implementation, ui-implementation, docs-implementation, architecture-implementation) are fully defined and have unit tests, but **end-to-end orchestration with real agents has never been executed**
- ❌ **Very Large Repository Handling (10k+ files)**: System performance assumptions untested at scale; escalation is mitigation but not empirically validated with real large codebases
- ❌ **CI/CD Integration Examples**: Deployment checklists exist but no concrete GitHub Actions / GitLab CI / Jenkins pipeline examples
- ❌ **Custom Workflow Extension Guide**: ADRs explain patterns; cookbook-style "add a new workflow" tutorial missing
- ❌ **Auto-Remediation**: System recommends workflows but doesn't generate fix PRs or automated code changes
- ❌ **Portfolio-Level Analysis**: Single-repository focus; cross-repository issue correlation, portfolio strategy not implemented
- ⚠️ **Soft-Context Routing Edge Cases**: Tie-breaking when multiple fog types equally plausible relies on user intent heuristic; refinement needed for high-ambiguity repos

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

- Add visual decision tree (flowchart) for "which fog type am I looking at?" to bootstrap skill
- Provide concrete runbook for agents receiving "insufficient evidence" error and how to escalate with additional context
- Document manual CLI walkthrough (reproduce Phase 4 scenarios locally without agent harness)
- Create "implementation workflow cookbook" with 3-5 worked examples of real-world repos routed to each workflow type
- Publish deployment playbook for practitioners (Slack post, blog, wiki)
- Add performance dashboards template and monitoring guidance for operations teams
- Expand examples/skill-tests with real-world codebases (currently test-fixture heavy; need 10+ diverse examples)
- Add tracing/debugging guide for agents stuck in validation loops (decision tree for which error type means what)
- Document fail-safe procedures for production if Phase 3+ orchestration fails at scale

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Primary Weakness**: The practical **end-to-end orchestration of all four implementation workflows at scale** has not been empirically proven with real agents in production scenarios.

**Specifically**:
- Phase 1 diagnostics are proven (agents can read skill, classify fog, produce valid brief artifact)
- Phase 2 routing is proven (workflow-planner selects workflow with 100% accuracy after bug fix)
- Individual workflow steps exist and have unit tests
- **But no empirical evidence that an agent can**:
  1. Accept ambiguous user intent
  2. Execute diagnostic workflow to completion without intervention
  3. Get routed to (e.g.) architecture-implementation-workflow
  4. Execute multi-phase implementation workflow (e.g., scan → identify → propose → validate)
  5. Handle validation failures across multiple phases with bounded retry
  6. Escalate gracefully when budget exhausted during implementation
  7. Produce final output artifact that passes downstream validation

**The Gap**: Individual pieces work. Full orchestration chain with real agents is untested. This is the **integration and safety boundary**.

**Weakness Type: Safety Gaps** — The system has proven diagnostic workflows but autonomous multi-phase orchestration at scale lacks real-agent validation, creating uncertainty about production readiness beyond Phase 1.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

**Evidence Summary**:
The repository demonstrates:
- ✅ Complete Phase 1 infrastructure (repo-sensemaker skill, unified validators, bootstrap skill, SessionStart hook)
- ✅ Complete Phase 2 infrastructure (workflow-planner skill, orchestration plan artifact, workflow registry)
- ✅ Complete Phase 3 infrastructure (operator runbooks, deployment checklists, skill maintenance)
- ✅ Complete Phase 4 testing (agent behavior proven for Phase 1-2, documented empirically)
- ✅ Theoretical soundness (13 ADRs document every architectural decision with constraints)
- ✅ Empirical proof of Phase 1-2 (Scenario 1 happy path and Scenario 5 failure path pass with fresh agents)
- ❌ Empirical proof of Phase 3+ multi-phase orchestration with real agents

**Logic Trace**: sensemaking-skills has successfully built and empirically tested a **diagnostic phase** (Phase 1: agent autonomously reads skill, classifies fog, produces valid brief) and **routing phase** (Phase 2: workflow-planner reads brief, selects workflow with 100% accuracy post-fix). The **implementation phases** (Phase 3-4: multi-step orchestration across four fog-type workflows) are completely defined with architecture, unit tests, and runbooks. However, **no production-like end-to-end execution** has been performed where a real agent starts with user intent, runs diagnostics, gets routed, and executes a full implementation workflow to completion.

Phase 4.1 testing proves diagnostic workflows work: agents autonomously complete repo-sensemaker → brief → validation → workflow-planner → plan → validation without manual intervention. Scenario 5 proves error handling (bounded retry, graceful escalation) works.

**The Production Gap**: No end-to-end test demonstrates that an agent can start with user intent (from 00-user-intent.md), run fast-path-workflow diagnostic phase, get routed to (e.g.) architecture-implementation-workflow, successfully execute multi-phase implementation sequence, produce final artifact (ARCHITECTURE_REVIEW.md) that passes validation, and handle multi-phase errors gracefully.

This is not a documentation gap or missing feature—it's a **production safety validation question**. The design is theoretically sound (13 ADRs prove this). Individual components work (Phase 4.1-4.2 prove this). But the full chain at real scale with messy input is untested.

See PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 40-65) for happy path proof, lines 42-56 for failure path proof, and lines 69-84 for performance metrics.

<!-- MODEL_SECTION:evidence_prose:END -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
```yaml
evidence_excerpts:
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 1-20
    quote: "System has completed all Phase 4 testing and verification. Phase 4.1 Fresh-agent behavior test PASS (happy path + failure path). Critical bug fixed: workflow-planner.py now honors escalation_recommended flag. Routing accuracy improved from 50% to 100%."
    supports_claim: "Phase 1-2 diagnostics and routing proven; critical safety bug fixed"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 40-65
    quote: "Agent reads bootstrap skill (using-sensemaking), follows diagnostic skill (repo-sensemaker), diagnoses repository autonomously, produces valid diagnostic brief, brief validation passes first attempt, agent creates orchestration plan, plan validation passes first attempt, end-to-end diagnostic + planning completes without intervention. Result: PASS"
    supports_claim: "Happy path workflow (Phase 1-2) proven with fresh agent; artifacts valid on first attempt"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 42-56
    quote: "Scenario 5 Budget Exhaustion: Agent encounters validation failure (missing required field), reads error message, applies suggested fix, retries, recognizes different error on 3rd attempt, respects 3-attempt budget (does NOT attempt 4th retry), escalates gracefully with clear reasoning. Result: Bounded retry logic PROVEN WORKING"
    supports_claim: "Failure path and escalation logic proven; agents correctly handle error recovery within budget"
  
  - file: PHASE-4-COMPLETE-FINAL-UPDATED.md
    lines: 69-84
    quote: "Performance baselines: workflow-planner 0.287s (target <5s), brief validation 0.412s (target <1s), plan validation 0.398s (target <1s), total automation ~1.1s (target <10s). All metrics EXCELLENT. Linear O(n) scaling verified."
    supports_claim: "Automation performance exceeds all SLOs; ready for scale"
  
  - file: DEPLOYMENT-GUIDE-2026-05-25.md
    lines: 8-19
    quote: "Component verification matrix: Infrastructure WORKING (Phase 4.2-4.3), Happy path agent behavior PROVEN (Phase 4.1), Failure path agent behavior PROVEN (Phase 4.1 Scenario 5), Edge cases HANDLED (Phase 4.3 6/6 scenarios), Performance ACCEPTABLE (Phase 4.2 baselines set), Documentation COMPLETE (Phase 4.4 runbooks), Gate approval PASSED (Phase 4.5)"
    supports_claim: "All Phase 1-2 components verified; Phase 3+ not yet empirically tested"
  
  - file: CONTEXT.md
    lines: 99-117
    quote: "Skill-led orchestration: Agents own control loop, read bootstrap skill, understand fog classification, invoke skills via Skill tool, read artifacts, parse validator errors, decide next step. Evidence model: durable artifacts prove outputs, validators prove contracts, run ledgers prove causal chain."
    supports_claim: "Architecture is well-specified and documented"
  
  - file: src/sensemaking_skills/skills/workflow_planner.py
    lines: 88-116
    quote: "Check escalation_recommended flag before choosing workflow. If escalation_recommended is True, route to full-fog-workflow regardless of confidence. This ensures safety-critical escalation is honored."
    supports_claim: "Critical safety fix: routing logic now correctly escalates when recommended"
```
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

If full-chain multi-phase orchestration remains unproven:

1. **Unknown production readiness** — Phase 1-2 is proven; Phase 3+ is not. Production rollout assumes all phases work; if Phase 3 fails, rollout must pause or rollback mid-stream
2. **Silent failures risk** — Agents might successfully diagnose and route but fail during implementation phases, producing partial/invalid artifacts downstream that go unnoticed
3. **Escalation procedures undertested** — Runbooks assume escalation works; if agents get stuck in multi-phase loops, runbook procedures haven't been validated with real agent behavior
4. **Deployment timing risk** — 3-week rollout plan assumes Phase 3+ is safe; if unproven, timeline must extend or deployment must remain Phase 1-2 only
5. **Maintenance burden underestimated** — If agents frequently fail in Phase 3+ orchestration, operator load will be higher than anticipated; runbooks may be insufficient
6. **Wasted effort on Phase 5 features** — Portfolio analysis, CI/CD integration, auto-remediation all assume Phase 3-4 are production-grade; testing would validate this prerequisite

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. **Execute Phase 4.3 Extension: Full-Chain Multi-Phase Agent Test** — Run fresh agent on real codebase with clear architecture_fog signals, routing to architecture-implementation-workflow, executing full multi-phase sequence end-to-end
2. **Capture full transcript, artifacts, and validation results** — Record every step including multi-phase error handling, retry decisions, escalation if triggered
3. **Test 4-way routing accuracy** — Execute agents on repos with product_fog, ui_fog, docs_fog, architecture_fog characteristics; verify each routes to correct workflow
4. **Test multi-phase error handling** — Use Scenario 5 pattern (introduce validation errors) to verify bounded retry works across multiple phases, not just first phase
5. **If Phase 4.3 passes, establish continuous validation** — Automate Phase 4.3 so regressions in multi-phase orchestration are caught in CI/CD before production
6. **If any phase fails, trace root cause to lowest scope** — Skill issue? Validation? Orchestration logic? Fix only what's broken
7. **Document findings in Phase-4-6 report** — Publish results of multi-phase orchestration testing; update deployment readiness matrix

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

**Execute Phase 4.3 Extension: Full-Chain Multi-Phase Orchestration Test (All Four Implementation Workflows)**

**Why**: Infrastructure is ready. Phase 1-2 is proven. What's needed is empirical execution of Phase 3-4 orchestration with real agents to validate production readiness before rolling out to general availability.

**Test Setup**:
- Select 4 real repositories (not test fixtures) with clear fog-type signals (one per type: product_fog, ui_fog, docs_fog, architecture_fog)
- For each repo:
  1. Run diagnostic workflow → get routed to implementation workflow
  2. Execute full multi-phase implementation sequence
  3. Capture all artifacts, validation results, performance metrics
  4. Record error handling and escalation if triggered

**Success Criteria**:
- ✅ All 4 workflows complete without manual intervention
- ✅ All artifacts pass validation on first attempt
- ✅ workflow-planner correctly routes to expected implementation workflow for each fog type
- ✅ Each workflow produces valid final artifact (e.g., ARCHITECTURE_REVIEW.md)
- ✅ Performance remains within SLOs (<10s total automation, <30min full pipeline)
- ✅ No infinite error loops; agents escalate gracefully when needed

**Expected Outcome**: Empirical proof that full orchestration chain works across all fog types, validating production readiness and enabling confident general-availability rollout.

**Estimated Effort**: 2-4 hours total (test setup, agent execution, analysis, documentation)

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

**Prompt for Full-Chain Multi-Phase Orchestration Test**:

```
You are validating the sensemaking-skills orchestration framework for production readiness. Your task:

1. Read the bootstrap skill at skills/using-sensemaking/SKILL.md
2. Select a repository with clear architecture_fog signals (mixed design patterns, architectural debt, etc.)
3. Execute the diagnostic workflow (repo-sensemaker → brief → workflow-planner → plan)
4. Verify routing to architecture-implementation-workflow
5. Execute the implementation workflow end-to-end
6. Capture all artifacts and validation results
7. Document any errors, escalations, or unexpected behavior

Success means: All phases complete without manual intervention, all artifacts valid on first attempt, workflow-planner routes to architecture-implementation-workflow, implementation workflow produces final valid artifact.

Budget: Max 3 attempts per phase. Escalate gracefully if budget exhausted.

Expected duration: 2-4 hours.
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
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 1-20): Phase 4 complete and approved; Phase 1-2 diagnostics and routing proven; critical bug fixed"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 40-65): Fresh agent happy path passes end-to-end; artifacts valid on first attempt"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 42-56): Budget exhaustion and escalation logic proven working; agents respect retry limits"
  - "PHASE-4-COMPLETE-FINAL-UPDATED.md (lines 69-84): Performance exceeds all SLOs; system ready for scale"
  - "DEPLOYMENT-GUIDE-2026-05-25.md (lines 8-19): All Phase 1-2 components verified; Phase 3+ not yet empirically tested"
  - "CONTEXT.md (lines 99-117): Architecture is sound and well-specified"
  - "src/sensemaking_skills/skills/workflow_planner.py (lines 88-116): Critical escalation bug fixed; routing accuracy 50% -> 100%"
recommended_workflow_id: skill-maintenance-loop
recommended_execution_mode: autonomous_execution
weakest_boundary: unproven_multi_phase_orchestration
required_inputs:
  - repository_state
created_at: "2026-07-25T21:04:41.674275Z"
immutable: true
```
