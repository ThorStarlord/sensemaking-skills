# Issue List: Sensemaking Skills Infrastructure Stabilization

**Generated from:** PRD-SENSEMAKING-SKILLS-INFRASTRUCTURE-FIX.md  
**Generated Date:** 2026-05-29  
**Status:** Ready for Implementation  
**Total Effort Estimate:** 2.0 days  
**Total Issues:** 4 core features

---

## 1. Scope Status

**PRD Scope Check:** ✅ `exact_match`  
**User Goal Preserved As:** exact_match  
**Scope Expansion:** None  
**Divergence Detected:** No  

This issue list addresses exactly the four infrastructure gaps the user identified. All issues are core (goal-preserving).

---

## 2. Issues Generated

### INFRA-001: Document Evidence Rules Dual-Mode Rendering

**Type:** Documentation + Test  
**Priority:** P0 (foundational for downstream consumers)  
**Effort:** 0.5 days  
**Scope:** Core  

**Description:**  
Add dual-mode documentation to evidence-rules so downstream skills can support both investigative (line numbers, snippets) and durable (grep-verifiable) output modes.

**Acceptance Criteria:**
- [ ] `repo-sensemaker/references/evidence-rules.md` documents two modes: investigative and durable
- [ ] Each mode includes examples (file citations with/without line numbers)
- [ ] `repo-analysis-template.md` Section 7 has YAML frontmatter toggle: `<!-- mode: investigative | durable -->`
- [ ] Template includes note explaining when to use each mode
- [ ] Downstream docs (prompt-handoff, to-prd) explain mode implications
- [ ] Test passes: repo-sensemaker can produce both modes on demand

**Definition of Done:**
- Documentation PR merged
- No skill behavior changes required
- Downstream consumers can read mode flag and act accordingly

**Dependencies:** None (can start immediately)

---

### INFRA-002: Document Execution Decision Criteria (Direct vs. Orchestrator)

**Type:** Documentation  
**Priority:** P0 (needed before Phase 5 autonomous runs)  
**Effort:** 0.25 days  
**Scope:** Core  

**Description:**  
Document criteria for when to invoke workflow-orchestrator vs. call skills directly. Resolves semantic gap where "don't wait" doesn't fit existing execution modes.

**Acceptance Criteria:**
- [ ] `docs/AGENTS.md` has new section "Agent Decision Tree: When to invoke orchestrator"
- [ ] Decision tree includes three heuristics: 1-3 skills, 4+ skills, "don't wait" override
- [ ] Each heuristic has reasoning (why that threshold)
- [ ] Examples provided: TDD on single issue (direct) vs. 6-skill orchestrated flow (orchestrator)
- [ ] Context note added to `workflow-orchestrator/references/execution-modes.md` pointing to decision tree
- [ ] No changes to orchestrator code or modes

**Definition of Done:**
- Documentation PR merged
- Links are correct and cross-file references work
- Future agents can use this to decide orchestration scope

**Dependencies:** None (can start immediately)

---

### INFRA-003: Implement Skill-Hygiene Validator (v1)

**Type:** Feature (automation)  
**Priority:** P0 (unblocks validation, depends on INFRA-004)  
**Effort:** 0.5 days  
**Scope:** Core  

**Description:**  
Build automated validator that catches broken skill references before merge. Three checks: npm scripts exist, skill IDs cross-ref, artifact contracts resolve.

**Acceptance Criteria:**
- [ ] `scripts/validate-skill-hygiene.mts` created and passes linting
- [ ] Check 1: Detects missing npm scripts (reads AGENTS.md, checks package.json)
  - [ ] Test: Add reference to nonexistent `npm run validate:fake`, run validator, confirm detection
  - [ ] Test: Existing codebase validates without errors
- [ ] Check 2: Detects missing skill IDs (reads workflow-registry.yaml, checks skill-registry.yaml)
  - [ ] Test: Add workflow step with fake skill ID, confirm detection
  - [ ] Test: Existing codebase validates without errors
- [ ] Check 3: Detects missing artifact contracts (reads skill registry, checks artifact-contracts.yaml)
  - [ ] Test: Add artifact ref not in contracts.yaml, confirm detection
  - [ ] Test: Existing codebase validates without errors
- [ ] `package.json` has entry `"validate:skills": "tsx scripts/validate-skill-hygiene.mts"`
- [ ] `npm run validate:skills` completes in < 2 seconds
- [ ] Error messages are actionable (point to file + line where ref appears)

**Definition of Done:**
- Script runs in CI/pre-commit
- All existing references pass validation
- Test suite confirms detection of three types of breakage

**Dependencies:** 
- **Blocks:** None
- **Blocked by:** INFRA-004 (needs artifact-contracts.yaml to exist)

---

### INFRA-004: Define Artifact-Contract Schemas for PM/Engineering Pipeline

**Type:** Feature (contracts)  
**Priority:** P0 (unblocks validator, needed before downstream consumers validate)  
**Effort:** 0.75 days  
**Scope:** Core  

**Description:**  
Add four new artifact-contract schemas (prd, issue_list, agent_brief, code_patch) to artifact-contracts.yaml. These contracts enable downstream validators and prevent format drift.

**Acceptance Criteria:**
- [ ] Schema `prd` added to artifact-contracts.yaml with required_sections and required_machine_fields
  - Includes: executive_summary, user_goal, features, out_of_scope, acceptance_criteria
  - Machine fields: prd_id, date, status, source_intent_ref, user_goal_preserved_as
- [ ] Schema `issue_list` added with per-issue structure
  - Per-issue fields: issue_id, title, effort_estimate, acceptance_criteria, parallelizable
  - Machine fields: parent_prd_id, total_effort_estimate, created_date
- [ ] Schema `agent_brief` added with required sections
  - Sections: agent_brief_id, task, context, instructions, acceptance_criteria, expected_output
  - Machine fields: parent_issue_id, effort_estimate, required_skills, created_date
- [ ] Schema `code_patch` added with file tracking
  - Sections: files_created, files_modified, test_summary
  - Machine fields: parent_brief_id, test_count, test_pass_count, test_fail_count, created_date
- [ ] All schemas are valid YAML (no parsing errors)
- [ ] Cross-references validated: consumed_by/produced_by are real artifacts
- [ ] Documentation added: explain each field's purpose and validation rules

**Derivation:**
- Schemas derived from intersection of Phase 4 artifacts
- Legacy artifacts marked "pre-schema" (not validated against new contracts)
- Forward validation applies to new runs only

**Definition of Done:**
- All four schemas merged into artifact-contracts.yaml
- No errors when parsed by validation tooling
- Downstream consumers (to-issues, tdd) can read and validate against these schemas

**Dependencies:** None (can start immediately, INFRA-003 depends on completion)

---

## 3. Parallelization Plan

**Phase 1 (Days 1-1.5, Parallel):**
- INFRA-001: Document evidence modes (0.5d) — can run in parallel
- INFRA-002: Document decision criteria (0.25d) — can run in parallel
- INFRA-004: Define artifact contracts (0.75d) — can run in parallel

**Phase 2 (Day 2, Sequential):**
- INFRA-003: Implement validator (0.5d) — must run after INFRA-004

**Total Timeline:** 2.0 days (1.5d parallel + 0.5d sequential)

---

## 4. Release Scope

| Metric | Value |
|--------|-------|
| **Total Issues** | 4 |
| **Core Issues** | 4 |
| **Expansion Issues** | 0 |
| **Total Effort** | 2.0 days |
| **Critical Path** | INFRA-004 → INFRA-003 (1.25 days) |
| **Timeline** | 2 calendar days (with parallelization) |
| **Blockers to Deployment** | None (all issues must complete before rollout) |

---

## 5. Out of Scope

- **Skill behavior changes:** Issues only add contracts, documentation, and validators — no algorithm changes
- **Orchestrator code refactoring:** Execution-mode decision lives in docs only
- **Retroactive validation:** Legacy artifacts (Phase 4) not re-validated; forward validation starts with next runs
- **File-path glob validation:** Deferred to Phase 5
- **Slash-command validation:** Deferred indefinitely (requires runtime context)
- **Env var validation:** Deferred to Phase 5

---

## 6. Success Criteria

**All issues resolved when:**
1. ✅ Evidence-rules dual-mode is documented and testable
2. ✅ Execution decision criteria are in AGENTS.md with examples
3. ✅ Skill-hygiene validator runs and detects all three types of breakage
4. ✅ Artifact contracts are defined and validate against new artifacts
5. ✅ No deployment blockers remain
6. ✅ Framework ready for 3-week rollout plan

---

## 7. Machine-Readable Handoff

```yaml
# Artifact Contract: Issue List
artifact_id: ISSUE-LIST-SENSEMAKING-INFRASTRUCTURE-FIX
artifact_type: issue_list
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: exact_match
scope_expansion_proposed: false
scope_expansion_status: exact_match
parent_prd_id: PRD-SENSEMAKING-SKILLS-INFRASTRUCTURE-FIX
created_date: 2026-05-29
total_issues: 4
total_effort_estimate_days: 2.0
issues:
  - issue_id: INFRA-001
    title: Document Evidence Rules Dual-Mode Rendering
    effort_days: 0.5
    priority: P0
    scope_type: core
    dependencies: []
    parallelizable: true
  - issue_id: INFRA-002
    title: Document Execution Decision Criteria
    effort_days: 0.25
    priority: P0
    scope_type: core
    dependencies: []
    parallelizable: true
  - issue_id: INFRA-003
    title: Implement Skill-Hygiene Validator (v1)
    effort_days: 0.5
    priority: P0
    scope_type: core
    dependencies: [INFRA-004]
    parallelizable: false
  - issue_id: INFRA-004
    title: Define Artifact-Contract Schemas
    effort_days: 0.75
    priority: P0
    scope_type: core
    dependencies: []
    parallelizable: true
critical_path:
  - INFRA-004 (0.75d)
  - INFRA-003 (0.5d)
  - total_critical_path_days: 1.25
total_parallel_timeline_days: 2.0
release_ready: false
escalation_required: false
downstream_consumer: tdd
next_step: Implement issues via TDD (test-first)
```

---

**Next Steps:** TDD skill will implement these four issues with test-first approach, starting with INFRA-004 (highest-priority blocker).
