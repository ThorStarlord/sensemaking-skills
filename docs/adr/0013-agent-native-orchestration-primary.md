# ADR 0013: Agent-Native Orchestration as Primary Model

**Status**: Accepted  
**Date**: 2026-05-24  
**Ratified**: 2026-08-13  
**Context**: Phase 1 Architecture Migration  
**Decision**: Shift from runner-led orchestration (CLI owns control loop) to skill-led orchestration (agents own control loop). Skills become platform-agnostic. CLI transitions from orchestrator to execution-only compatibility layer.

---

## Amendment (2026-08-13) — Ratified with explicit scope

This ADR is ACCEPTED as the primary execution-model decision, with the
following explicit scope:

1. **Primary model**: the active coding agent reads and executes Skills
   directly. The agent is the runtime.
2. **Skill contract**: `SKILL.md` + typed artifact contracts + deterministic
   validators are independent of any particular coding-agent harness.
3. **Programmatic runner**: `workflow-runtime.py` / `skill_executor.py` are a
   SEPARATE automation/compatibility path. They are not part of the semantic
   definition of Skill execution.
4. **Existing implementation reality**: the current programmatic model-backed
   runner is Claude-specific (`claude-code` via the Claude Agent SDK, `api` via
   `ANTHROPIC_API_KEY`). Acceptance does not claim that runner is
   agent-agnostic, and does not require adapters for other coding agents.

**Non-claim**: agent-native execution being primary does NOT imply that every
workflow has been behaviorally validated under every coding-agent harness.
`DEMONSTRATED` is not "universally proven".

---

## Context

The system was originally built as **runner-led orchestration**: `workflow-runtime.py` owned the control loop, calling worker skills, managing gates, and recording evidence. This model:

**Strengths:**
- Deterministic, machine-auditable control flow
- Clear responsibility (runner manages orchestration, skills produce artifacts)
- Validators as external arbiter of correctness

**Limitations for AI-native workflows:**
- CLI is the primary interface; agents are secondary
- Agents can't make intelligent routing decisions (CLI owns the routing logic)
- User experience requires CLI flags (`--workflow`, `--mode`), not conversational interaction
- Next-step decisions require human intervention or hardcoded rules, not agent judgment

---

## Decision

Implement **skill-led orchestration as the primary model**:

```
User asks agent in Claude Code/Cursor
  ↓
SessionStart hook injects using-sensemaking bootstrap skill
  ↓
Agent reads skill policy and understands:
  - When to invoke diagnosis vs implementation workflows
  - How to interpret fog_type classification
  - How to parse structured validator errors
  - Retry logic + escalation rules
  ↓
Agent invokes appropriate skill (via Skill tool)
  ↓
Skill creates/reads artifacts
  ↓
Validators run inside skill context (call helper scripts, parse JSON errors)
  ↓
Agent reads artifact + validation results, decides next step
  ↓
CLI becomes optional: can invoke same skills without orchestration responsibilities
```

### Key Principles

1. **Skills are platform-agnostic**
   - Skills do not assume they're called by an agent or a CLI script
   - Skills take inputs, produce outputs, call helper scripts for validation
   - Same skill works when invoked by agent or CLI

2. **Validators output structured JSON** (not human prose)
   - Agents parse JSON errors reliably
   - Errors include: field name, current value, suggested fixes, reference documentation
   - Enables deterministic auto-fix logic with backoff + escalation

3. **Skills self-document** (in SKILL.md)
   - Each skill describes: inputs, outputs, artifact structure, error handling
   - Agents reference SKILL.md to understand artifact fields
   - Bootstrap skill does NOT become a reference encyclopedia

4. **Helper scripts handle validation + logging**
   - `validate-and-report.py` invoked by skills (not by orchestrator)
   - Helper scripts create/update run logs (not agents)
   - Both agents and CLI produce identical evidence trail

5. **Bootstrap skill teaches, doesn't dictate**
   - ~2000-2500 words: fog classification principles, decision trees, retry logic
   - Links to external docs (CONTEXT.md, ADRs, ui-fog-signals.md)
   - Agents become guided researchers, not blind automata

6. **Artifacts remain the API**
   - ADR 0009 (Artifacts as API) remains load-bearing
   - Field contracts in artifact-contracts.yaml are source of truth
   - Validators enforce contracts (unchanged responsibility)

---

## Consequences

### Immediate (Phase 1)

- **Bootstrap skill creation** (~2000-2500 words)
  - Fog classification teaching
  - Decision-making framework
  - Structured error interpretation
  - Retry + escalation logic
  - References to external docs

- **Validator refactoring**
  - All validators output JSON (structured errors)
  - New helper: `validate-and-report.py`
  - Agents can parse + act on errors
  - Human-readable explanations still in JSON `message` field

- **Skill self-documentation**
  - Each SKILL.md documents output artifacts
  - Field descriptions, error conditions, examples
  - Agents reference during execution

- **SessionStart hook**
  - Platform-specific implementations (Claude Code, Cursor, OpenCode)
  - Injects bootstrap skill at session start
  - No additional setup needed

- **Artifact structure updates**
  - `repository_sensemaking_brief`: add `primary_fog_type`, `recommended_workflow_id`
  - All artifacts: add `validation_status` field (valid | invalid + reason)
  - Update `artifact-contracts.yaml`

### Medium-term (Phase 2)

- **CLI execution layer** (optional)
  - CLI can invoke skills (Python imports)
  - CLI uses same helper scripts as agents
  - Produces identical run logs
  - No orchestration logic (that's agents' job)

- **Test suite alignment**
  - Tests validate structured error output (JSON)
  - Tests validate skill platform-agnosticism
  - Tests validate run log creation by helper scripts

### Long-term

- **CLI deprecation becomes optional**
  - If agents work reliably, CLI can be deprecated
  - If CLI support is needed, it's a thin compatibility layer
  - No code duplication between paths

- **Multi-platform support**
  - Agents in Claude Code, Cursor, OpenCode, others
  - All invoke the same skill-led orchestration
  - Hooks platform-specific; skills platform-agnostic

---

## Rationale

### Why skill-led instead of runner-led?

1. **Agents make better decisions in context**
   - Agents can read artifact content and reason about it
   - CLI can only follow hardcoded rules
   - Example: Agent reads evidence, decides fog_type; CLI can't reason about evidence quality

2. **Conversational UX requires agent agency**
   - User: "Diagnose my codebase"
   - Agent: "I found product fog. Invoking product-implementation-workflow"
   - User: "Actually, it's more of a UI problem"
   - Agent: "I'll switch to ui-implementation-workflow"
   - This requires agent judgment, not CLI flags

3. **Evidence guarantees still hold**
   - CONTEXT.md section 9 states: "Artifacts prove outputs. Validators prove outputs satisfy contracts. Run ledgers prove the causal chain."
   - Helper scripts (not agents) create run ledgers
   - Validators remain deterministic and external
   - Evidence model unchanged — only orchestrator changes

4. **Platform-agnostic skills enable ecosystem**
   - Skills can be reused in CLI, agents, future orchestrators
   - No duplication of skill logic
   - Easy to add new platforms without rewriting skills

### Why structured validator errors?

Agents need to:
1. Understand WHAT went wrong (field name, error type)
2. Understand WHY it matters (which consumer needs this, why)
3. Know HOW to fix it (suggested values, references)

JSON structure enables deterministic parsing. Human prose requires agent reasoning (hallucination risk).

### Why Phase 1, not Phase 2?

Scenario A (simple interactive agent) requires manual workflow selection, which defeats the purpose of agent-native.

Scenario B (smart autonomous agent) requires:
- Fog classification teaching (bootstrap skill)
- Artifact structure understanding (SKILL.md references)
- Validator error parsing (JSON format)
- Retry logic (backoff + escalation)

All are necessary for Phase 1 credibility. Better to build all at once than stagger them.

---

## Alternatives Considered

### 1. Hybrid: Keep both runner-led and skill-led
- **Pro**: Backward compatible with existing CLI workflows
- **Con**: Two orchestration models = maintenance burden, validator drift, unclear source of truth
- **Rejected**: Single source of truth (skills) is cleaner

### 2. Embedded validation (agents validate, no external scripts)
- **Pro**: Fast, no subprocess calls
- **Con**: Validator logic in skill code, no canonical validators, easy to diverge
- **Rejected**: Validators as external scripts is load-bearing (test suite, CI/CD, auditability)

### 3. Simple agent (Scenario A: agent asks user to pick workflow)
- **Pro**: Easier to implement, less agent reasoning required
- **Con**: Defeats purpose of agent-native ("want agent to make decisions")
- **Rejected**: User explicitly stated "I want the agent to decide"

---

## Success Criteria

Phase 1 succeeds when:
- [ ] Agent diagnoses repo WITHOUT asking user questions
- [ ] Agent reads fog_type and picks correct workflow first try
- [ ] Agent auto-fixes artifact conflicts (with retry + backoff)
- [ ] Agent completes fast-path-workflow end-to-end in Claude Code
- [ ] Validator errors are JSON (parseable)
- [ ] Each skill documents its outputs in SKILL.md
- [ ] Run logs created by helper scripts (not agents)
- [ ] CLI can invoke skills (but doesn't orchestrate)

---

## Related ADRs

- **ADR 0005**: Three-stage automation (auto-invocation)
- **ADR 0009**: Handoff skill and naming conventions
- **ADR 0010**: Runtime owns artifact path resolution
- **ADR 0012**: Manual vs. automation invocation paths (now superceded by skill-led model)
