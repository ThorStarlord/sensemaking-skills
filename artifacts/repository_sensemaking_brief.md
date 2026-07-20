# Repository Sensemaking Brief: sensemaking-skills

## 1. Repository Goal

The sensemaking-skills repository implements an **agent-native orchestration system** that diagnoses repository uncertainty (fog classification) and routes agents to implementation workflows. Phase 1 focuses on diagnostic workflows (repo-sensemaker, workflow-planner) with graceful agent autonomy and bounded retry logic.

---

## 2. Current Shape

**Key Components**:
- **14 skills** defined: repo-sensemaker, workflow-planner, handoff, problem-framer, usage-researcher, docs-aligner, unknowns-mapper, skill-maintainer, and others
- **13 ADRs** documenting core design patterns (artifact-driven engineering, soft-context routing, agent-native orchestration, validation modes)
- **5 unified validators** (validate-brief.py, validate-plan.py, validate-artifact.py, plus integrate/helper scripts)
- **Bootstrap skill** (using-sensemaking/SKILL.md) — comprehensive ~600-line teaching guide
- **SessionStart hook** — surfaces bootstrap reminder to agents
- **Helper scripts** — validate-and-report.py (unified dispatcher), record-validation.py (durable logging)
- **Test infrastructure** — Phase 1 test orchestrator, 5 test scenarios, execution guides
- **CONTEXT.md** — Domain language and orchestration principles

**Documentation**:
- README with philosophy and quick-start
- CONTEXT.md with core principles and design patterns
- 13 ADRs explaining every major design decision
- Skill-specific SKILL.md files with concrete examples

---

## 3. Strong Signals

**What's Working Well**:
- ✅ **Architectural clarity**: 13 ADRs exhaustively document fog classification, artifact-driven engineering, validation modes, and routing logic
- ✅ **Unified validator schema**: All 5 validators produce identical JSON structure (error_id, error_type, field, message, suggested_fixes) enabling consistent agent parsing
- ✅ **Bootstrap skill teaching**: 600+ lines covering 4 fog types, 5 error types, 3-step diagnosis, retry logic, escalation rules with concrete examples
- ✅ **Bounded retry with escalation**: Explicit 3-attempt limit with escalation conditions (same error, logic_error, insufficient evidence)
- ✅ **Evidence-driven design**: Agents ground decisions in artifacts, not conversation memory; every skill produces validated outputs
- ✅ **SessionStart integration**: Hook surfaces bootstrap reminder; agents don't need to hunt for documentation
- ✅ **Durable audit trail**: validation_run_log.md records every attempt with timestamps, error metadata, references for reproducibility
- ✅ **Graceful error handling**: validate-and-report.py wraps subprocess failures in same JSON schema, no special-case parsing needed

---

## 4. Missing Pieces

**What's Not Yet Implemented or Incomplete**:
- ❌ **Phase 2 implementation workflows**: System is diagnostic-only; product-implementation-workflow, ui-implementation-workflow, etc. are not yet implemented
- ❌ **Real-agent behavior proof**: Code is complete, unit tests pass, but no empirical evidence that actual agents follow the expected pattern
- ❌ **Skill registration**: repo-sensemaker exists as a skill definition but is not registered in the Skill tool (agents must follow the framework manually, not invoke a callable)
- ❌ **Agent integration testing**: No test showing end-to-end agent → bootstrap skill → repo-sensemaker artifact → validate → log
- ⚠️ **Practice vs. theory gap**: Documentation is dense; unclear if agents will intuitively understand how to apply it without explicit walkthrough

---

## 5. Improvement Opportunities

- Clear presentation of "agent vs. skill" distinction (skill = definition/pattern; agent = does the work per the pattern)
- Concrete worked example of Scenario 1 happy path in agent's words
- Reference list of "if agent gets stuck, check X" in bootstrap skill
- More visual examples of error JSON in error handling section

---

## 6. Weakest Boundary

**Primary Weakness**: The practical integration of agent + bootstrap skill + artifact validation pipeline **is unproven in real agent behavior**.

Specifically:
- Agents have not yet demonstrated they can:
  1. Read bootstrap skill without explicit navigation help
  2. Understand fog classification conceptually from the skill alone
  3. Perform repo-sensemaker analysis without automated tooling
  4. Produce a valid repository_sensemaking_brief artifact on first try
  5. Correctly invoke validate-and-report.py and interpret JSON output
  6. Call record-validation.py and understand the run log entry
  7. Handle validation errors with bounded retry (max 3 attempts)
  8. Escalate gracefully when stuck

- The validators themselves are complete and tested
- The skill documentation is comprehensive
- The architecture is sound
- **But the glue—actual agent behavior—has never been exercised**

**Weakness type: Zero Validation** (The system has structural tests, but no behavioral proof with real agents)

---

## 6.5. Problem Classification (Fog Type)

**Primary fog type: docs_fog**

**Reasoning**:
- **Product clarity**: The repository's goal is very clear (create agent-native orchestration)
- **Architecture clarity**: ADRs explain every design decision; structure is well-documented
- **User need clarity**: Agent orchestration is an explicit, validated design goal
- **Unclear practical usage**: The **specification** is comprehensive, but the **practical integration path** for agents is untested
- The documentation teaches "what" (4 fog types, 3-step diagnosis) but the real test is whether agents naturally follow "how"
- **This is a docs_fog issue**: The knowledge exists but hasn't been validated as actionable by its end users (agents)

---

## 7. Evidence

### Evidence Summary

The repository demonstrates:
- ✅ Complete infrastructure (validators, skill, bootstrap, hook, logger, test harness)
- ✅ Comprehensive documentation (CONTEXT.md, 13 ADRs, skill SKILL.md files)
- ✅ Theoretical soundness (architecture decisions are well-reasoned, constraints are explicit)
- ❌ Empirical proof of agent behavior (no transcript showing an agent actually completing Phase 1 end-to-end)

### Evidence Excerpts

```yaml
evidence_excerpts:
  - file: PHASE-1-EXECUTION-STATUS.md
    lines: 32-38
    quote: "Phase 1 is transitioning from planning to execution. All planning, architecture, infrastructure, and unit-testing is complete. The next step is the empirical test: Can a fresh agent actually use Phase 1 as designed?"
    supports_claim: "Repository is theoretically complete but empirically unproven"
  
  - file: skills/using-sensemaking/SKILL.md
    lines: 1-50
    quote: "This skill teaches you how to diagnose repositories and make autonomous orchestration decisions... Do not run any code or create files. Do make you an expert in software architecture (that's for domain skills). Do make you understand how artifacts flow between skills."
    supports_claim: "Bootstrap skill documentation is comprehensive but depends on agent comprehension"
  
  - file: test-results/phase1/EXECUTION-GUIDE.md
    lines: 50-80
    quote: "Agent should: 1. Read skills/using-sensemaking/SKILL.md 2. Invoke repo-sensemaker skill 3. Produce repository_sensemaking_brief 4. Call validate-and-report.py 5. Parse JSON response"
    supports_claim: "Happy path is well-defined but untested with real agent"
  
  - file: CONTEXT.md
    lines: 84-100
    quote: "Agents read bootstrap skill (using-sensemaking), understand fog classification and workflow routing... Agents invoke skills (via Skill tool), read artifacts, parse structured validator errors, decide next step"
    supports_claim: "Agent behavior is specified but behavioral proof is pending"
```

### Logic Trace (Required)

Logic trace: The repository has successfully implemented all structural components needed for agent-native Phase 1 orchestration: validators with unified JSON schema, a comprehensive bootstrap skill teaching fog classification and error handling, SessionStart hook integration, and a complete test harness documenting 5 scenarios. However, **no real agent has yet completed a full Phase 1 diagnostic cycle**. The skill documentation is written theoretically ("when you read this, you will understand...") but hasn't been validated through actual agent execution. The **documentation is complete but its practical effect on agent behavior is untested**. This is a docs_fog issue: the knowledge exists, the specification is clear, but the real question—do agents naturally follow the teaching?—remains unanswered. The weakest boundary is the gap between "skill exists and is thorough" and "agents actually use it as designed." Testing this requires empirical proof: a fresh agent given only the bootstrap skill and the three-step pattern, completing Phase 1 end-to-end without guidance.

---

## 8. Why This Boundary Matters

If this remains weak:
1. **Unknown whether Phase 1 is agent-usable** — Engineers will continue building Phase 2, but agents might not actually use Phase 1 as intended
2. **Silent failures in production** — Agents might misunderstand fog classification or skip validation steps, producing invalid artifacts downstream
3. **Wasted effort on Phase 2** — If Phase 1 agent behavior is broken, Phase 2 implementation will inherit the problem
4. **False confidence from unit tests** — Validators pass tests, skill docs exist, but real agent behavior was never proven
5. **No audit trail of actual behavior** — The validation_run_log.md will be empty until an agent actually uses the system

---

## 9. Candidate Next Steps

1. **Run Scenario 1 (Happy Path) with a fresh agent** — Test the happy path: agent reads skill, diagnoses repo, produces valid brief, validates successfully, logs result
2. **Capture agent transcript and artifacts** — Record what the agent actually did, not what we expected it to do
3. **If Scenario 1 passes, run Scenario 2-5** — Test error handling, bounded retry, escalation, semantic conflict detection
4. **If any scenario fails, identify the specific gap** — Did agent skip skill reading? Misunderstand fog types? Fail to invoke validator?
5. **Fix only the identified gap, not architectural assumptions** — If agent misunderstands validation JSON, fix that specific instruction; don't redesign the whole system

---

## 10. Recommended Next Step

**Execute Scenario 1 (Happy Path) with a fresh agent.**

The test is already designed and documented in `test-results/phase1/EXECUTION-GUIDE.md`. What's needed is the empirical execution: open a fresh Claude Code/Cursor session and give the agent the test prompt:

```
Diagnose this repository using sensemaking-skills. 
Read the bootstrap skill if you haven't seen it yet. 
Follow the three-step diagnosis pattern.
```

Capture:
- Agent's actual behavior (did it read the skill?)
- Artifacts produced (is repository_sensemaking_brief valid?)
- Validator JSON output (what did validate-and-report.py say?)
- Run-log entry (did record-validation.py create the entry?)
- Final result (PASS or FAIL, and if FAIL, at which exact step?)

---

## 11. Recommended Workflow

**phase1-agent-behavior-test** (not yet in workflow-registry.yaml, but should be)

Mode: `plan_only` initially (run Scenario 1, collect results, report findings without committing fixes)

Steps:
1. Execute Scenario 1 with fresh agent
2. Analyze behavior against expected pattern
3. If PASS: Proceed to Scenario 2
4. If FAIL: Identify root cause, recommend targeted fix

---

## 12. Machine-Readable Handoff

### Stage 1: Intent-Aware Fields & Standard Fields

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: docs_fog
evidence:
  - "PHASE-1-EXECUTION-STATUS.md (lines 32-38): Repository is theoretically complete but empirically unproven; Phase 1 is transitioning from planning to execution"
  - "skills/using-sensemaking/SKILL.md (lines 24-44): Bootstrap skill documentation is comprehensive but depends on agent comprehension and practical integration"
  - "test-results/phase1/EXECUTION-GUIDE.md (lines 50-80): Happy path is well-defined but untested with real agent behavior"
  - "CONTEXT.md (lines 84-100): Agent behavior is specified in principle but behavioral proof is pending"
recommended_workflow_id: fast-path-workflow
recommended_execution_mode: plan_only
created_at: 2026-05-25T00:15:00Z
immutable: true
source_intent_ref: null
user_implied_fog_type: unknown
diagnosis_conflict: false
escalation_recommended: false
weakest_boundary: unproven_agent_behavior
evidence_level: theoretical_high_empirical_zero
```

---

## 13. Created At

**Timestamp**: 2026-05-25T00:15:00Z  
**Session**: Phase 1 Real-Agent Orchestration Test — Scenario 1 Execution  
**Status**: Ready for validation
