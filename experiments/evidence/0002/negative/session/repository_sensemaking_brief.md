# Repository Sensemaking Brief: sensemaking-skills

**Repository**: sensemaking-skills  
**Analysis Date**: 2026-07-25  
**Overall Assessment**: Production-ready framework with proven agent-native diagnostics; phase 2+ orchestration routing remains untested in production

---

## 1. Executive Summary

**sensemaking-skills** is an agent-native framework for repository diagnosis and workflow orchestration. It turns project uncertainty ("fog") into clear problem frames, research paths, and actionable next-step prompts. The codebase implements a sophisticated artifact-driven agentic engineering architecture with strong verification discipline.

**Current Status**: Phase 4 complete (production-ready). Phase 1 (agent-native diagnostics with bounded retry and graceful escalation) is proven via Scenario 5 testing. Phase 2-5 (multi-workflow routing and specialized implementation paths) are architecturally complete but lack real-world validation.

**Primary Value**: Enables agents (Claude Code, Cursor, OpenCode) to diagnose repositories autonomously, classify uncertainty types, and recommend targeted workflows — without external API calls or credentials.

---

## 2. Repository Purpose & Scope

**Founding Goal**: Provide a meta-routing layer that transforms vague project problems into structured fog-type classifications and skill recommendations.

**Core Principles**:
1. **Fog First** — Always classify uncertainty type before proposing solutions
2. **Artifacts as API** — Skills communicate via durable, validated outputs, not conversation memory
3. **Boundary Rule** — Do not perform downstream work (building) by default
4. **Local-First Design** — No external API calls, no credentials, works entirely offline
5. **Agent-Native** — Skills defined in SKILL.md; agents orchestrate via artifact handoffs

**Architecture Philosophy**: Artifact-Driven Agentic Engineering (documented in CONTEXT.md, ADRs 0001-0013).

---

## 3. Current Capabilities (Proven)

### Phase 1: Agent-Native Diagnostic Framework ✅ COMPLETE & PROVEN
- **Repository diagnosis** produces accurate 14-section briefs identifying weakest boundaries
- **Fog classification** assigns input to one of four types: product_fog, ui_fog, docs_fog, architecture_fog
- **Skill routing** selects appropriate next workflow (problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner)
- **Bounded retry logic** recovers from errors with max 3 attempts per stage
- **Graceful escalation** recommends deeper analysis when budget exhausted (Scenario 5 proven)
- **SessionStart hook** injects bootstrap skill teaching agents fog classification and error parsing

**Evidence**: 
- PHASE-4-1-COMPLETE.md documents happy-path + Scenario 5 (failure path, budget exhaustion) passing all tests
- PHASE-4-1-SCENARIO-5-NO-ATTEMPT-4-CONFIRMATION.md proves escalation correctly halts at 3 attempts without attempting a 4th

### Phase 2-3: Multi-Workflow Orchestration Framework ✅ ARCHITECTURALLY COMPLETE
- **Fog-type-aware routing** — workflow-planner reads fog_type and recommends correct implementation workflow
- **Four implementation workflows** — ui-implementation, product-implementation, docs-implementation, implementation (default)
- **Workflow registry** (workflow-registry.yaml) — 10+ workflows defined with step sequences
- **Auto-invocation mechanism** — workflow-runtime.py chains workflows based on recommended_workflow_id
- **Skill registry** (skill-registry.yaml) — 20+ skills catalogued with artifact contracts
- **Validation stack** — Three-level hierarchy (structural, generic, specialized validators)

**Evidence**: 
- Files exist and are registered: workflow-registry.yaml, skill-registry.yaml, artifact-contracts.yaml
- PHASE-3-TESTING-PLAN.md and PHASE-3-FRAMEWORK-DELIVERED.md confirm architecture complete
- Test fixtures in examples/skill-tests/ include behavioral proof fixtures

---

## 4. Not Yet Proven (Gaps)

### Production Execution Gaps
1. **No value-production runs** — All runs to date are system-proving (proving infrastructure works), not solving real stakeholder problems
   - Phase 1-3 focus: "Does the orchestration engine work?"
   - Phase 4+: "Does it produce value for real repositories?"
   - Precondition: Clean git worktree + external stakeholder problem + human gate approval

2. **Multi-workflow routing untested on real codebases** — Architecture for ui/product/docs/architecture fog-type routing exists but has not been exercised against actual repositories
   - workflow-planner.py determines fog_type and recommends workflow
   - workflow-runtime.py validates fog-type alignment and invokes workflow
   - Structural tests pass; end-to-end behavioral validation pending

3. **Dynamic chaining heuristics provisional** — Routing decisions based on unknowns_count >= 5 and clarity_assessment == "low" are initial estimates
   - Empirical validation deferred to first value-production runs
   - Thresholds will be refined using repeatable failure analysis

### Orphan Skills (Not Integrated)
- **data-access-layer-auditor** — Registered but zero workflow step references
- **project-classifier** — Defined but not in skill-registry active use paths
- **usage-researcher** — Registered but no workflow references (despite usage-research-scenarios.yaml existing)
- **workflow-presenter** — No workflow references

These skills were built or documented but not wired into execution paths; they remain available for future expansion.

---

## 5. Architecture Strengths

### Verification Discipline
**Founding Principle**: "Artifacts are the API between skills"

1. **Field-name contracts** (artifact-contracts.yaml) — Producers and consumers must agree on machine field names before writing code
   - test_field_contract_agreement.py enforces this at compile time
   - Prevents silent mismatches like the flat-path-vs-session-path regression

2. **Artifact-path resolution** — OrchestrationRunner._resolve_artifact_path owns path computation
   - Producers write to context["expected_output_path"] (passed by runtime)
   - Prevents "artifact not found" bugs from path recomputation drift

3. **Validator-consumer traceability** — Before a validator rule exists, confirm something downstream reads it
   - Example: Evidence-line format was too strict until we confirmed what actually parses it
   - Prevents false failures fighting the producer's valid output

4. **Three-level validation hierarchy**
   - Level 1 (Structural): Repository-wide consistency (validate-repo.py)
   - Level 2 (Generic): Universal contracts — sections, machine fields, no absolute paths (validate-artifact.py)
   - Level 3 (Specialized): Semantic checks per artifact type (validate-brief.py, validate-plan.py, etc.)

### Orchestration Patterns (ADR-Backed)
- **ADR 0001**: Strict vs. Lenient validation (planning vs. execution modes)
- **ADR 0002**: Workflow separation of concerns (one purpose per workflow)
- **ADR 0003**: Artifact composition (meaningful transformation per step)
- **ADR 0004**: Evidence tracking (validators + run logs = audit trail)
- **ADR 0005**: Three-stage automation (diagnostic → orchestration → implementation)
- **ADR 0006**: User intent as durable artifact (immutable raw intent, append-only amendments)
- **ADR 0011**: Canonical vocabulary enforcement (single source of truth for enums)
- **ADR 0012**: Manual vs. automation invocation paths (dual strategy, same workflows)

### Documentation & Teachability
- **CONTEXT.md** — 400+ lines defining domain language, core principles, orchestration rules
- **ADR directory** — 13 documented architectural decisions with rationale
- **SKILL.md files** — Each skill self-documents inputs, outputs, error modes
- **Bootstrap skill** (using-sensemaking) — Teaches agents fog classification without introspecting the repo
- **GETTING_STARTED.md** — Dual-path execution guide (manual + automation)

### Production Hardening Evidence
- **PHASE-4-3-EDGE-CASE-PLAN.md & PHASE-4-3-RESULTS.md** — Edge case testing identified and fixed critical bug
  - workflow-planner.py lines 88-116 now check escalation_recommended flag before choosing workflow
  - Routing accuracy improved from 50% to 100%
- **PHASE-4-4-OPERATOR-RUNBOOKS.md** — Operational procedures documented
- **PHASE-4-5-PRODUCTION-GATE.md** — Gate approval signed off

---

## 6. Weakest Boundary: Fog-Type-Aware Routing in Production

**Identified Weakness**: The transition from **Phase 1 proven framework to Phase 2+ multi-workflow orchestration** is architecturally complete but not yet validated against real-world fog classification.

**Specific Concern**: workflow-planner.py classifies fog_type in the orchestration plan, and workflow-runtime.py routes to the appropriate implementation workflow. However:

1. **Fog-type classification never exercised against diverse real codebases** — repo-sensemaker.py has logic to detect product_fog, ui_fog, docs_fog, architecture_fog signals, but the signal detection has not been empirically validated. False positives in fog classification could misroute to the wrong workflow.

2. **ui-fog detection signals not in production** — docs/ui-fog-signals.md defines Tier 1/2/3 indicators for UI-heavy projects, but the sensemaker skill has not been tested on UI-intensive codebases to confirm signal accuracy.

3. **Dynamic routing heuristics untested** — The rule "insert discovery skill if unknowns_count >= 5 OR clarity_assessment == 'low'" is a provisional heuristic. No empirical data on whether these thresholds optimize the right objective (time-to-actionable-brief vs. research quality vs. cost).

4. **Auto-chaining mechanism proves structurally but not behaviorally** — workflow-runtime.py._validate_workflow_fog_alignment() exists and would catch a misalignment (e.g., routing ui_fog to implementation-workflow). But the test fixtures do not exercise the full chain: **genuine ui_fog input → ui-fog-signals detection → ui-implementation-workflow selection → step 1 execution**. The end-to-end behavioral path has not been run on a real UI-heavy codebase.

**Why This Matters**: A routing error (e.g., missing ui-fog detection, sending a UI problem to architecture-workflow) would silently produce wrong recommendations. The validator stack would not catch this because the brief itself would be valid — just misdiagnosed.

**Mitigation Path** (Phase 5+):
- First value-production run on a deliberately UI-heavy codebase → validate ui-fog detection signals
- Measure fog-type classification accuracy across 10+ real repositories
- Collect metrics: false-positive rate, recommendation quality per fog-type
- Refine thresholds using repeatable failure analysis (Harden Only Where Pressured principle)
- Gate Phase 2+ feature rollout on achieving >95% classification accuracy

---

## 7. System Dependencies & Constraints

### No External Dependencies
- **No API calls** — All logic runs locally
- **No credentials required** — Zero-configuration out of the box
- **No service dependency** — Works fully offline once installed via pip
- **Python 3.11+** — Only runtime requirement (no compiled code)

### Agent Harness Dependency
- **Skill invocation requires Claude Code or equivalent** — Full diagnosis requires agent to read SKILL.md and invoke skills
- **CLI tools work standalone** — `sensemaking-skills validate`, `analyze`, `test` work without an agent
- **Bootstrap skill injected at session start** — Teaches agent fog classification and error parsing

### Git Worktree Requirement
- **Guided execution and higher** require clean git tree
- **YOLO execution** still requires worktree but less strict on cleanliness
- **Isolation mode** uses temporary worktrees for safe experimentation

---

## 8. Integration Points

### Skills Ecosystem
- **Core Pipeline**: problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner → handoff
- **Specialized Workflows**: Four implementation paths, each with own skill sequences
- **Extensibility**: New skills can be registered in skill-registry.yaml; new workflows in workflow-registry.yaml

### Artifact Contracts
- **problem_frame** (input to unknowns-mapper)
- **unknowns_map** (input to repo-sensemaker, includes routing signal research_needed)
- **repository_sensemaking_brief** (input to workflow-planner; 14 required sections)
- **workflow_orchestration_plan** (output; includes fog_type, recommended_workflow_id, execution_strategy)

### Validation Entry Points
- **validate-artifact.py** — Universal checks; entry point for all artifact validation
- **workflow-runtime.py** — Orchestrator that invokes validators post-step
- **validate-output.py** — Dispatcher that routes to per-artifact validators via artifact-contracts.yaml

---

## 9. Code Organization

```
sensemaking-skills/
├── CONTEXT.md                          [Domain language + 13 ADRs]
├── README.md                           [5-minute primer]
├── GETTING_STARTED.md                  [Dual-path execution guide]
├── skills/
│   ├── repo-sensemaker/                [Primary diagnostic skill]
│   ├── workflow-planner/               [Fog classification + routing]
│   ├── problem-framer/                 [Problem frame skill]
│   ├── unknowns-mapper/                [Knowns/unknowns mapping]
│   ├── handoff/                        [Session summary]
│   └── workflow-planner/references/
│       ├── skill-registry.yaml         [20+ skills]
│       ├── workflow-registry.yaml      [10+ workflows]
│       ├── artifact-contracts.yaml     [Field agreements]
│       └── canonical-vocabulary.yaml   [Enum authority]
├── scripts/
│   ├── validate-artifact.py            [Universal validator]
│   ├── validate-brief.py               [Sensemaking-specific checks]
│   ├── validate-plan.py                [Plan-specific checks]
│   └── [more validators...]
├── docs/
│   ├── adr/                            [Architecture decisions]
│   ├── mode-coverage.yaml              [Execution mode proof]
│   └── ui-fog-signals.md               [UI detection indicators]
├── examples/skill-tests/               [Behavioral fixtures]
├── tests/                              [Unit + integration tests]
└── data/samples/                       [Test repositories]
```

---

## 10. Quality Evidence

### Validation Coverage
- **test_field_contract_agreement.py** — Compile-time contract enforcement
- **validate-brief.py** — 14-section structure, weakness-type recognition, logic-trace validation
- **validate-plan.py** — Workflow step validation, gate consistency, artifact reference checking
- **Mode coverage matrix** (docs/mode-coverage.yaml) — Documents which execution modes are proven

### Testing Approach
1. **Structural tests** — YAML parsing, registry consistency, enum validation
2. **Behavioral fixtures** — Positive (valid artifacts pass) and negative (invalid artifacts fail)
3. **Integration tests** — End-to-end workflow execution with real orchestration runner
4. **System-proving runs** — PHASE-1 through PHASE-4 demonstrate system works
5. **Scenario-based testing** — Scenario 5 specifically tests budget exhaustion + graceful escalation

### Hardening Validation (Harden Only Where Pressured)
- **NO_LOGIC_TRACE** bug — Recurred across 2 independent runs; triggered producer-side hardening (repo-sensemaker skill spec updated)
- **UNKNOWN_WEAKNESS_TYPE** bug — Same; triggered template hardening
- **INVALID_LINE_FORMAT** bug — Validator bug-fix (evidence format too strict for real output)

---

## 11. Known Limitations & Mitigation

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No value-production runs | Unknown real-world performance | Phase 5: Launch with beta cohort |
| Fog-type routing untested | Possible misrouting to wrong workflow | Phase 5: Validate on 10+ real repos |
| Dynamic chaining heuristics provisional | May insert unnecessary discovery skill | Phase 5: Measure and refine thresholds |
| Orphan skills not integrated | Dead code; confuses new contributors | Future: Remove or integrate |
| No repeatable failure ledger yet | Can't identify systemic patterns | Future: Accumulate from production runs |

---

## 12. Recommended Next Steps

### Immediate (Before Production Rollout)
1. **Fog-type classification validation** — Run on 5-10 real codebases with known fog types; measure accuracy
2. **UI-fog signal testing** — Test on UI-heavy projects (React, Vue, design-system repos); validate tier-1 signal detection
3. **Dynamic chaining empirical validation** — Measure impact of discovery skill insertion on brief quality and cost

### Short-Term (Phase 5 Objectives)
1. **Value-production run #1** — Real stakeholder problem, clean git worktree, gate approval at each step
2. **Beta cohort pilot** — 10-20 engineers across different org teams; collect feedback
3. **Repeatable failure tracking** — Build failure ledger from production runs; identify systemic patterns
4. **Orphan skill resolution** — Integrate or deprecate unused skills (data-access-layer-auditor, project-classifier, usage-researcher)

### Medium-Term (Post-GA Roadmap)
1. **Multi-fog disambiguation** — When repo shows signals for multiple fog types, develop tiebreaker rules
2. **Specialized workflow optimization** — Measure real-world performance of product/ui/docs/architecture workflows
3. **Agent-skill feedback loop** — Agents report which recommendations were useful; refine signal detection
4. **Regional performance data** — Collect anonymized metrics on fog-type accuracy, recommendation latency, user satisfaction

---

## 13. Critical Bug Fix (Phase 4.3)

**Issue**: workflow-planner.py ignored escalation_recommended flag when choosing workflow  
**Root Cause**: Lines 88-116 did not check escalation status before routing  
**Fix**: Added conditional check to respect escalation_recommended flag  
**Impact**: Routing accuracy improved from 50% to 100%

**Verification**: PHASE-4-3-EDGE-CASE-PLAN.md and PHASE-4-3-RESULTS.md document the issue, fix, and re-validation proof.

---

## 14. Verdict & Object Under Pressure

**Verdict**: Production-ready framework with proven Phase 1 diagnostics; Phase 2+ orchestration routing architecturally sound but lacking real-world behavioral validation.

**Object Under Pressure**: The **fog-type classification and multi-workflow routing layer** (orchestration-plan generation and auto-chaining logic). This is where silent failures would occur (wrong workflow selected without validator catching it). This is the weakest boundary requiring Phase 5 production validation.

**What's Safe Today**: Agents can use Phase 1 (problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner) to produce accurate diagnostics on any repository. Bounded retry and graceful escalation are proven.

**What Needs Production Proof**: Whether the recommended_workflow_id produced by workflow-planner actually routes to the right implementation path on real codebases with diverse fog types.

---

## References

- **CONTEXT.md** — Full architectural narrative and domain language
- **PHASE-4-COMPLETE-FINAL-UPDATED.md** — Phase 4 completion summary
- **PHASE-4-5-PRODUCTION-GATE.md** — Gate approval documentation
- **DEPLOYMENT-GUIDE-2026-05-25.md** — Deployment procedures
- **PHASE-4-4-OPERATOR-RUNBOOKS.md** — Operational procedures
- **docs/adr/** — All architectural decisions with rationale
- **docs/canonical-vocabulary.yaml** — Authoritative enum definitions
- **skills/workflow-planner/references/artifact-contracts.yaml** — Machine field contracts

