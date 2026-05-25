# Phase 1: Agent-Native Implementation Checklist

**Status**: Planning  
**Target**: Weeks 1-3 (May 24 - June 7, 2026)  
**Goal**: Complete agent-native orchestration with skill-led architecture, platform-agnostic skills, and structured validator output

---

## Overview

Phase 1 delivers a working agent-native system where:
- Agents in Claude Code/Cursor read bootstrap skill and make decisions
- Agents invoke `repo-sensemaker` and understand fog classification
- Validators output JSON (agents parse reliably)
- Skills self-document in SKILL.md (agents reference during execution)
- Run logs created by helper scripts (not agent memory)
- CLI invokes same skills (compatibility layer, not orchestrator)

---

## Task Dependencies

```
Week 1 (Foundation):
  ├─ Task 1.1: Create bootstrap skill template
  ├─ Task 1.2: Create SessionStart hook
  ├─ Task 1.3: Validator JSON refactoring guide
  └─ Task 1.4: Artifact contract updates

Week 2 (Implementation):
  ├─ Task 2.1: Implement validator JSON output (brief, plan, artifact)
  ├─ Task 2.2: Helper script: validate-and-report.py
  ├─ Task 2.3: Helper script: record-validation.py
  ├─ Task 2.4: Update skill SKILL.md files (repo-sensemaker, workflow-planner, handoff)
  └─ Task 2.5: Update artifact-contracts.yaml

Week 3 (Testing & Integration):
  ├─ Task 3.1: End-to-end test (agent diagnoses repo)
  ├─ Task 3.2: Validate validator JSON output
  ├─ Task 3.3: Verify run log creation
  └─ Task 3.4: CLI compatibility check (scripts can still invoke skills)
```

---

## Detailed Tasks

### **Week 1: Foundation**

---

#### **Task 1.1: Create Bootstrap Skill Template**
**Assigned to**: You  
**Depends on**: None  
**Effort**: 6-8 hours  
**File**: `skills/using-sensemaking/SKILL.md.template` (create from template)

**What it includes**:
- [ ] Skill frontmatter (name, description, how to invoke)
- [ ] 7 main sections (see SKILL.md.template)
- [ ] Fog classification teaching (~2000-2500 words)
- [ ] Decision tree diagrams (text-based, ASCII)
- [ ] Structured error interpretation examples
- [ ] Retry logic + escalation flowchart
- [ ] Links to external docs (CONTEXT.md, ADRs, ui-fog-signals.md)

**Success criteria**:
- [ ] Template is complete (all 7 sections have content/placeholders)
- [ ] Examples are concrete (not abstract)
- [ ] A new agent reading this skill understands when to invoke workflows
- [ ] References to external docs are correct URLs
- [ ] Bootstrap skill file can be moved to `skills/using-sensemaking/SKILL.md` with no changes

**Acceptance**: Bootstrap skill teaches fog classification, agents can act on it autonomously

---

#### **Task 1.2: Create SessionStart Hook**
**Assigned to**: You  
**Depends on**: Task 1.1 (bootstrap skill exists)  
**Effort**: 3-4 hours  
**Files**: 
- `hooks/hooks.json` (update)
- `hooks/session-start` (create/update)

**What it does**:
- [ ] Register SessionStart hook in hooks.json
- [ ] Implement `session-start` script that reads bootstrap skill
- [ ] Inject bootstrap skill into system context
- [ ] Support platforms: Claude Code (primary), Cursor (secondary), OpenCode (optional)

**Success criteria**:
- [ ] Hook fires at session start in Claude Code
- [ ] Bootstrap skill appears in agent's context
- [ ] Agent can reference bootstrap skill in reasoning
- [ ] No errors in hook execution

**Acceptance**: Agent can read bootstrap skill from first message in Claude Code session

---

#### **Task 1.3: Validator JSON Refactoring Guide**
**Assigned to**: You  
**Depends on**: None  
**Effort**: 4-6 hours  
**File**: `docs/validator-json-refactor-guide.md`

**What it includes**:
- [ ] JSON schema definition (structured error format)
- [ ] Step-by-step refactoring instructions
- [ ] Examples for each validator type:
  - Syntactic errors (missing field, wrong type)
  - Semantic errors (conflict between fields)
  - Logic errors (evidence contradicts conclusion)
- [ ] How to write `suggested_fixes` field
- [ ] How to link to reference documentation
- [ ] Backwards compatibility notes

**Success criteria**:
- [ ] Guide is clear enough to refactor any validator
- [ ] Examples cover all error types in Phase 1
- [ ] Developers can follow guide without asking questions

**Acceptance**: A developer can pick any Phase 1 validator and refactor to JSON using this guide

---

#### **Task 1.4: Artifact Contract Updates**
**Assigned to**: You  
**Depends on**: None  
**Effort**: 2-3 hours  
**File**: `skills/workflow-planner/references/artifact-contracts.yaml`

**What changes**:
- [ ] Add `primary_fog_type` to repository_sensemaking_brief
- [ ] Add `recommended_workflow_id` to repository_sensemaking_brief
- [ ] Add `evidence` to repository_sensemaking_brief
- [ ] Add `primary_fog_type` to workflow_orchestration_plan
- [ ] Add `chosen_workflow_id` to workflow_orchestration_plan
- [ ] Add `routing_decision_method` to workflow_orchestration_plan
- [ ] Add `workflow_steps` to workflow_orchestration_plan
- [ ] DO NOT add `validation_status` to any artifact (validation is transient, not artifact data)
- [ ] Document field meanings (what agents use)
- [ ] Add examples

**Success criteria**:
- [ ] All Phase 1 artifacts have required fields per artifact-contracts.yaml
- [ ] NO `validation_status` field in any artifact (validation is separate)
- [ ] Field types are correct (enum, string, array, object)
- [ ] `primary_fog_type` enum includes all 4 values: product_fog, ui_fog, docs_fog, architecture_fog
- [ ] `workflow_steps` is array of step objects with: step_id, skill, input_artifact, output_artifact, gate, description

**Acceptance**: artifact-contracts.yaml validates all Phase 1 artifacts; test_field_contract_agreement.py passes

---

### **Week 2: Implementation**

---

#### **Task 2.1: Implement Validator JSON Output**
**Assigned to**: You  
**Depends on**: Task 1.3 (refactoring guide), Task 1.4 (contract updates)  
**Effort**: 8-10 hours  
**Files**:
- `scripts/validate-brief.py` (refactor)
- `scripts/validate-plan.py` (refactor)
- `scripts/validate-artifact.py` (refactor)

**What it does**:
- [ ] Refactor validate-brief.py to output JSON (use guide from 1.3)
- [ ] Refactor validate-plan.py to output JSON
- [ ] Refactor validate-artifact.py to output JSON (generic checks)
- [ ] Keep human-readable output as `message` field (agents can explain to users)
- [ ] Add timestamp field to all JSON output
- [ ] Preserve existing validation logic (only change output format)

**Success criteria**:
- [ ] All Phase 1 validators output JSON to stdout
- [ ] JSON includes: valid, error_type, field, current_value, message, suggested_fixes, reference
- [ ] Human tests still pass (validate existing fixtures)
- [ ] JSON is valid (can be parsed by `json.loads()`)
- [ ] Backwards compatibility: validators still return exit code 0 on pass, 1 on fail

**Acceptance**: Phase 1 validators output JSON; agents can parse and understand errors

---

#### **Task 2.2: Helper Script: validate-and-report.py**
**Assigned to**: You  
**Depends on**: Task 2.1 (validators output JSON)  
**Effort**: 4-6 hours  
**File**: `scripts/validate-and-report.py` (create)

**What it does**:
- [ ] Accepts artifact path as argument
- [ ] Calls appropriate validator (dispatches based on artifact_id)
- [ ] Captures JSON output from validator
- [ ] Returns JSON to caller (skill or CLI)
- [ ] Calls record-validation.py to log the validation attempt

**Signature**:
```bash
python scripts/validate-and-report.py <artifact_path>
# Returns: JSON with validation result + records to run log
```

**Success criteria**:
- [ ] Script successfully calls validators
- [ ] JSON output is parseable
- [ ] Run log is updated by this script
- [ ] Skills can import and call this function

**Acceptance**: Skills call validate-and-report.py and get back JSON errors + run log recording

---

#### **Task 2.3: Helper Script: record-validation.py**
**Assigned to**: You  
**Depends on**: Task 2.1 (validators output JSON)  
**Effort**: 4-6 hours  
**File**: `scripts/record-validation.py` (create)

**What it does**:
- [ ] Called by validate-and-report.py after validation
- [ ] Accepts: artifact_id, validator_name, validation_result (JSON)
- [ ] Reads/creates run_log.md in current session
- [ ] Appends validation step with:
  - Step number
  - Artifact validated
  - Validator used
  - Result (valid/invalid)
  - Timestamp
  - Error details (if invalid)
- [ ] Run log is always human-readable (supplementary to machine JSON)

**Signature**:
```bash
python scripts/record-validation.py --artifact-id <id> --validator <name> --result <json>
# Updates run_log.md in current session directory
```

**Success criteria**:
- [ ] Run log is created if missing
- [ ] Validation entries are appended (not overwritten)
- [ ] Timestamp is ISO format
- [ ] Run log is readable by humans

**Acceptance**: After each validation, run_log.md is updated with step details

---

#### **Task 2.4: Update Skill SKILL.md Files**
**Assigned to**: You  
**Depends on**: Task 1.4 (artifact contracts updated)  
**Effort**: 6-8 hours  
**Files**:
- `skills/repo-sensemaker/SKILL.md` (update Outputs section)
- `skills/workflow-planner/SKILL.md` (update Outputs section)
- `skills/handoff/SKILL.md` (update Outputs section)

**What each SKILL.md now includes**:

```markdown
## Outputs

### Artifact: repository_sensemaking_brief

**Type**: Diagnostic output  
**Consumer**: Agent (reads fog_type + evidence, decides next workflow)

**Key fields agents read**:
- primary_fog_type: one of [product_fog, ui_fog, docs_fog, architecture_fog]
- evidence: file-level proof supporting classification
- recommended_workflow_id: next workflow to invoke

**If validation fails**:
- Agent reads validation_status.error_type
- Agent reads validation_status.suggested_fixes
- Agent retries with adjustments (up to N times)
- Agent escalates to user if retry fails

**Example artifact structure**:
[show shortened example with field names + types]
```

**Success criteria**:
- [ ] Each skill documents its outputs in SKILL.md
- [ ] Documentation is concrete (shows field names, types, examples)
- [ ] Agents can understand artifact structure by reading SKILL.md
- [ ] No implementation details (just API contract)

**Acceptance**: A new agent can read SKILL.md and understand what artifacts to expect and how to use them

---

#### **Task 2.5: Update artifact-contracts.yaml (Final Pass)**
**Assigned to**: You  
**Depends on**: Task 2.4 (SKILL.md files updated)  
**Effort**: 2-3 hours  
**File**: `skills/workflow-planner/references/artifact-contracts.yaml`

**What it does**:
- [ ] Verify all Phase 1 artifacts are documented
- [ ] Add examples to each artifact
- [ ] Verify field types match what validators enforce
- [ ] Add links to SKILL.md files (where agents learn about outputs)

**Success criteria**:
- [ ] artifact-contracts.yaml matches SKILL.md documentation
- [ ] test_field_contract_agreement.py passes
- [ ] Validators enforce fields listed in contract

**Acceptance**: Artifacts are fully documented in contracts + SKILL.md files

---

### **Week 3: Testing & Integration**

---

#### **Task 3.1: End-to-End Test (Agent Diagnoses Repo)**
**Assigned to**: You  
**Depends on**: Tasks 2.1-2.5 (all implementation complete)  
**Effort**: 6-8 hours  
**Manual test** (not automated)

**What you do**:
- [ ] Open Claude Code with your sensemaking-skills repo
- [ ] SessionStart hook fires, bootstrap skill injected
- [ ] You type: "Diagnose my codebase"
- [ ] Agent reads bootstrap skill and understands fog classification
- [ ] Agent invokes repo-sensemaker via Skill tool
- [ ] repo-sensemaker produces artifact with fog_type
- [ ] Validators output JSON errors (if any)
- [ ] Agent attempts auto-fix (up to 3 retries with backoff)
- [ ] Agent reads final artifact and decides next workflow
- [ ] Agent invokes workflow-planner
- [ ] workflow-planner produces orchestration plan
- [ ] Agent reads plan and understands Phase 1 diagnostic is complete
- [ ] If validation fails after 3 retries, agent escalates with structured error details

**Success criteria**:
- [ ] Agent completes fast-path-workflow autonomously
- [ ] Artifact fog_type is correct (matches your actual codebase)
- [ ] Agent recommends correct next workflow (product-impl, ui-impl, etc.)
- [ ] Validator JSON errors are parsed correctly
- [ ] If validation fails, agent attempts auto-fix (up to 3 times)
- [ ] If escalation occurs: agent shows error + suggested_fixes + reference documentation
- [ ] Agent never gets stuck (bounded retry with graceful escalation)

**Acceptance**: Agent diagnoses repo and completes Phase 1 workflow end-to-end in Claude Code

---

#### **Task 3.2: Validate Validator JSON Output**
**Assigned to**: You  
**Depends on**: Task 2.1 (validators refactored)  
**Effort**: 4-5 hours  
**Automated test**

**What it tests**:
- [ ] All Phase 1 validators output valid JSON
- [ ] JSON includes required fields: valid, error_type, field, message, suggested_fixes, reference
- [ ] JSON parses without errors
- [ ] Exit codes still work (0 on pass, 1 on fail)
- [ ] Human-readable fallback still works (if JSON parsing fails)

**Test approach**:
```bash
# Run validators on valid + invalid fixtures
python scripts/validate-brief.py artifacts/valid-brief.md > output.json
# Verify JSON is valid
python -c "import json; json.load(open('output.json'))"
```

**Success criteria**:
- [ ] All Phase 1 validators pass JSON validation
- [ ] No regressions (existing fixtures still work)

**Acceptance**: Validators reliably output JSON; agents can parse errors

---

#### **Task 3.3: Verify Run Log Creation**
**Assigned to**: You  
**Depends on**: Task 2.3 (record-validation.py created)  
**Effort**: 3-4 hours  
**Automated test**

**What it tests**:
- [ ] After validation, run_log.md is created
- [ ] Each validation step is recorded
- [ ] Timestamps are ISO format
- [ ] Error details are included (if validation fails)
- [ ] Run log is human-readable

**Test approach**:
```bash
# Run a workflow, check run_log.md exists
python scripts/validate-artifact.py artifacts/test-brief.md
python scripts/record-validation.py --artifact-id repository_sensemaking_brief --validator validate-brief.py --result '{"valid": true}'
# Verify run_log.md has new entry
grep "validate-brief.py" run_log.md
```

**Success criteria**:
- [ ] Run logs are created by helper scripts (not agents)
- [ ] All Phase 1 validation steps appear in run log
- [ ] No data loss (validation results are recorded)

**Acceptance**: Run logs are created automatically; provide audit trail of validation

---

#### **Task 3.4: CLI Compatibility Check**
**Assigned to**: You  
**Depends on**: Tasks 2.1-2.3 (validators + helpers complete)  
**Effort**: 3-4 hours  
**Manual test**

**What you do**:
- [ ] CLI still works (can invoke skills via workflow-runtime.py)
- [ ] CLI produces same artifacts as agent
- [ ] CLI uses same validators (JSON output)
- [ ] CLI uses same run log recording
- [ ] **Goal**: Verify that CLI is now a compatibility layer, not the orchestrator

**Test approach**:
```bash
# Run diagnostic workflow via CLI (legacy path)
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Verify artifacts are produced
ls artifacts/*/repository_sensemaking_brief.md

# Verify run_log.md exists
ls artifacts/*/run_log.md

# Verify validators output JSON
python scripts/validate-brief.py artifacts/*/repository_sensemaking_brief.md
```

**Success criteria**:
- [ ] CLI still works (no regressions)
- [ ] Artifacts from CLI match artifacts from agent
- [ ] Validators output JSON in both paths
- [ ] Run logs are identical format (agent + CLI)

**Acceptance**: CLI is a compatibility layer; agents are primary orchestrator

---

## Phase 1 Success Criteria (Overall)

All of the following must be true:

- [ ] **Bootstrap skill**: Agent reads it and understands fog classification autonomously
- [ ] **SessionStart hook**: Injects bootstrap skill at session start in Claude Code
- [ ] **Agent autonomy**: Agent diagnoses repo WITHOUT asking you questions
- [ ] **Fog classification**: Agent reads fog_type and picks correct workflow
- [ ] **Validator JSON**: All Phase 1 validators output structured JSON
- [ ] **Artifact self-docs**: Each skill documents outputs in SKILL.md
- [ ] **Artifact contracts**: artifact-contracts.yaml has all Phase 1 artifacts + fields
- [ ] **Run logs**: Created by helper scripts (not agent memory)
- [ ] **Retry + escalation**: Agent retries on validation failure; escalates if stuck
- [ ] **CLI compatibility**: CLI still works; produces same artifacts as agent
- [ ] **Platform-agnostic skills**: Same skill works whether called by agent or CLI
- [ ] **End-to-end test**: Agent completes fast-path-workflow autonomously in Claude Code

---

## Known Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Bootstrap skill is too large; agents don't read it | Keep it focused: teach fog classification + decision rules, not encyclopedic details. Link to external docs for depth. |
| Agents hallucinate fog type classification | Agents reference evidence in artifact. If classification is wrong, validator catches it. Retry + escalation is safety valve. |
| Validator JSON refactoring is tedious | Use refactoring guide (Task 1.3). Template each validator output once, then copy pattern. |
| Run log recording is unreliable | Helper scripts own recording (not agents). Logs are append-only (no overwrites). Timestamped. |
| CLI breaks during Phase 1 | CLI is compatibility layer: skills don't know if called by agent or CLI. Test both paths in Task 3.4. |

---

## How to Use This Checklist

1. **Week 1**: Complete Tasks 1.1 - 1.4 (planning + contracts)
2. **Week 2**: Complete Tasks 2.1 - 2.5 (implementation)
3. **Week 3**: Complete Tasks 3.1 - 3.4 (testing)
4. **After Phase 1**: Move to Phase 2 (implementation workflows, more fog types, etc.)

**Track progress**:
- Mark tasks as in_progress when you start
- Mark as completed when success criteria are met
- If a task is blocked, create a note (don't skip it)

---

## Phase 1 Completion Criteria

Phase 1 is DONE when:
- ✅ All tasks 1.1 - 3.4 are completed
- ✅ Agent autonomously diagnoses repo in Claude Code (Task 3.1)
- ✅ Validators reliably output JSON (Task 3.2)
- ✅ Run logs are created automatically (Task 3.3)
- ✅ CLI still works (Task 3.4)
- ✅ CONTEXT.md and ADR 0013 are updated (already done)

**Success**: You have a working agent-native system where agents make orchestration decisions, skills are platform-agnostic, and evidence layer is preserved.

---

## Next: Phase 2 Planning

After Phase 1 succeeds, Phase 2 will:
- Refactor all diagnostic workflows (not just fast-path)
- Refactor implementation workflows
- Add more fog types (if needed)
- Expand bootstrap skill to teach advanced scenarios
- Add more platforms (Cursor, OpenCode, others)

But first: **complete Phase 1 to baseline**.
