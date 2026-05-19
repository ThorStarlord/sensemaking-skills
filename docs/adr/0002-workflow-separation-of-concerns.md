# ADR 0002: Workflow Separation of Concerns

**Status**: Accepted  
**Date**: 2026-05-18  
**Context**: Phase 2 Implementation  
**Decision**: Each workflow should have ONE clear purpose; don't mix different concerns in a single workflow

---

## Context

During Phase 2 analysis, we discovered a critical design issue in the docs-architecture workflow:

**Original docs-architecture Workflow** (problematic):
```yaml
steps:
  - id: 1
    skill: docs-aligner          # Purpose: align domain understanding
    output_artifact: domain_alignment_report
  
  - id: 2
    skill: to-prd                   # Purpose: generate PRD specification ← DIFFERENT PURPOSE
    output_artifact: prd
  
  - id: 3
    skill: handoff                  # Purpose: prepare execution prompt
    output_artifact: prompt_handoff
```

**The Problem**:
1. **Confused Purpose**: Is this workflow about domain alignment OR PRD generation? Both!
2. **Artifact Orphaning**: The PRD produced by step 2 wasn't consumed by step 3 (handoff expects domain_alignment_report)
3. **Unclear Ownership**: If prd is needed, which workflow should produce it? docs-architecture or somewhere else?
4. **Skill Confusion**: Should to-prd live here or in a dedicated workflow?
5. **Validation Gap**: We couldn't validate whether the PRD was actually used or just generated as a side-effect

**Real Impact**:
- Users didn't know if the system actually used the PRD artifacts
- New workflow designers copied the anti-pattern (mixing concerns)
- Maintenance became unclear: if to-prd needs improvement, who owns it?

---

## Decision

### Core Rule
**Each workflow has ONE clear, singular purpose.** Every step in the workflow must advance that purpose.

### Implementation

#### 1. Separate docs-architecture (Domain Alignment Focus)
```yaml
- id: docs-architecture
  display_name: Domain Alignment
  purpose: Align implementation with repository documentation through stakeholder interviews
  steps:
    - id: 1
      skill: docs-aligner
      output_artifact: domain_alignment_report
    
    - id: 2
      skill: handoff
      input_artifact: domain_alignment_report
      output_artifact: prompt_handoff
```

#### 2. Create product-to-issues (PRD Generation Focus)
```yaml
- id: product-to-issues
  display_name: Product PRD & Implementation Issues
  purpose: Transform domain alignment into PRD, then into implementation issues and agent briefs
  steps:
    - id: 1
      skill: to-prd
      input_artifact: domain_alignment_report
      output_artifact: prd
    
    - id: 2
      skill: to-issues
      input_artifact: prd
      output_artifact: issue_list
    
    - id: 3
      skill: triage
      input_artifact: issue_list
      output_artifact: agent_brief
```

### Testing for Single Purpose

Ask yourself for each workflow:
1. "What is this workflow's purpose in one sentence?" (If you need "and", it's mixing concerns)
2. "Could I remove any step and the workflow still make sense?" (If yes, it's not core to the purpose)
3. "Does every step contribute to the stated purpose?" (If not, move that step elsewhere)

---

## Consequences

### Positive
1. **Clear Intent**: Anyone reading docs-architecture knows its purpose is domain alignment, not PRD generation
2. **Proper Artifact Flows**: domain_alignment_report flows from docs-architecture → product-to-issues (clear dependency)
3. **Reusability**: product-to-issues can consume alignment reports from OTHER workflows too (not just docs-architecture)
4. **Validation Clarity**: Each artifact has a clear reason to exist (it's consumed by the next step)
5. **Skill Ownership**: to-prd belongs in product-to-issues, not scattered across workflows
6. **Testing Simplicity**: Test each workflow independently without worrying about orphaned artifacts

### Negative
1. **More Workflows**: System has more workflows to manage (simple to understand, but more entries in registry)
2. **Explicit Composition**: Users must explicitly run docs-architecture THEN product-to-issues (not automatic)
3. **Longer Chains**: To go from raw_fog → agent_brief now requires 2+ workflows instead of 1

### Trade-offs
- We chose **separation over consolidation** because:
  - Clear purpose makes future design decisions easier
  - Proper artifact flow prevents validation gaps
  - Reusability (product-to-issues can consume from anywhere) is worth the extra workflow definition

---

## Alternatives Considered

### Alternative 1: Mixed Workflows with Conditional Steps
- Keep all transformations in one workflow, use `if` conditions to skip non-relevant steps
- **Rejected because**: Violates single-responsibility; unclear which steps are "core" vs. "conditional"
- **Consequence**: Users don't know what the workflow is actually for

### Alternative 2: Monolithic "Full Pipeline" Workflow
- Create one mega-workflow that does everything (alignment → PRD → issues → briefs → code)
- **Rejected because**: Can't reuse parts; every workflow must be a full pipeline; impossible to debug
- **Consequence**: Inflexible system; one broken step breaks the entire pipeline

### Alternative 3: Nested Workflows
- Allow workflows to call other workflows as steps
- **Rejected because**: Adds complexity to orchestrator; unclear error handling; late binding makes validation hard
- **Consequence**: Harder to test and validate; more debugging needed

### Alternative 4: Plugin Skills for Different Concerns
- Instead of multiple workflows, create multiple versions of skills (to-prd-v1, to-prd-v2, etc.)
- **Rejected because**: Skill proliferation; hard to maintain; doesn't solve the composition problem
- **Consequence**: Skill registry becomes unmaintainable; unclear which skill to use when

---

## Evidence

This decision was validated during Phase 2:

### Before Refactoring
- docs-architecture had 3 steps mixing two concerns (domain alignment + PRD generation)
- PRD artifact was produced but not consumed (validation gap)
- Tests couldn't verify the PRD was actually validated

### After Refactoring
- docs-architecture has 2 steps, clear purpose: domain alignment
- product-to-issues has 3 steps, clear purpose: PRD → issues → briefs
- Each artifact is consumed by the next step (proper flow)
- Validation tests pass for both workflows (✓ 7/7 tests)

### Real-World Validation
- Orchestrator can plan both workflows successfully
- No artifact orphaning (every output is consumed)
- New workflow designers understand the pattern

---

## Implications for Future Decisions

1. **Workflow Design**: Every new workflow must have a ONE-SENTENCE purpose
2. **Step Addition**: Steps can only be added if they advance the stated purpose
3. **Composition**: Workflows should compose by artifact flow (output of one → input of another)
4. **Artifact Validation**: Easier because artifacts have clear reasons to exist

---

## Related

- **Pattern**: See `orchestration-patterns.md` → Pattern 2: Workflow Separation of Concerns
- **Guide**: `workflow-design-guide.md` → Step 1: Define Your Purpose
- **Test**: All 7 Phase 2 design verification tests pass
- **Prior Issue**: docs-architecture mixing domain alignment with PRD generation (Phase 2 discovery)

---

## For Workflow Designers

When designing a new workflow:

1. **Write your purpose** (one sentence)
2. **For each step**, ask: "Does this advance my stated purpose?"
3. **If no**, move that step to a different workflow
4. **If unclear**, your purpose is too broad; split the workflow

**Good purposes:**
- "Transform domain alignment into PRD" ← Single transformation
- "Diagnose repository architecture" ← Single investigation
- "Assign implementation work to agents" ← Single decision

**Bad purposes:**
- "Do analysis and PRD" ← Two things (AND = red flag)
- "Improve the system" ← Too vague, unclear what work happens
- "Everything from raw_fog to deployed code" ← Way too many concerns

---

## Acceptance Criteria

This decision is accepted when:
- ✓ docs-architecture has 2 steps (docs-aligner, handoff) with clear domain alignment purpose
- ✓ product-to-issues has 3 steps (to-prd, to-issues, triage) with clear PRD generation purpose
- ✓ Each step's output is consumed by next step (no orphaned artifacts)
- ✓ No other workflows mix multiple concerns
- ✓ All workflow design validation tests pass (7/7)
- ✓ New workflows following this pattern have single, clear purposes

---

## Questions & Answers

**Q: What if two concerns naturally go together (like PRD + issues)?**  
A: That's fine! The test is: "Is there ONE clear purpose?" If PRD → issues is your purpose, that's one purpose. The anti-pattern is PRD + ALIGNMENT (two different purposes).

**Q: Why not use flags to turn steps on/off?**  
A: Because then the workflow's "real" purpose is hidden. You can't tell if the workflow is primarily for PRD or alignment; it depends on how you run it. Better to split.

**Q: What about shared setup steps (authentication, data loading)?**  
A: If they're truly shared, they should be in a separate workflow that feeds into others. If they're specific to one purpose, they belong in that workflow.

**Q: Can I have sub-workflows?**  
A: Not yet (would require nested workflow support in orchestrator). For now, decompose into separate workflows and compose by artifact flow.
