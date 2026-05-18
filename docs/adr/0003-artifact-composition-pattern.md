# ADR 0003: Artifact Composition Pattern

**Status**: Accepted  
**Date**: 2026-05-18  
**Context**: Phase 3 Implementation  
**Decision**: Each step in a workflow must meaningfully transform its input artifact; no pass-through or renaming steps

---

## Context

When designing multi-step workflows, there's a temptation to add "convenience" steps that don't actually transform data, just reformat or rename it:

**Problematic Composition Example:**
```
domain_alignment_report (raw document)
         ↓ copy-and-rename
    prd_draft            (exact same content, different filename) ❌
         ↓ format-prettily
    prd                  (same content, just prettier) ❌
         ↓ to-issues
    issue_list
```

**The Problem:**
1. **No Value Added**: Steps 1-2 don't add information; they just shuffle bytes
2. **Validation Confusion**: Validators can't tell if transformation happened (content is same)
3. **Clarity Lost**: Future readers don't understand why those steps exist
4. **Skill Overload**: Skills accumulate trivial transformations (formatting, renaming, copying)
5. **Reusability Broken**: You can't reuse prd_draft or intermediate formats; they're not semantic artifacts

**Real-World Impact:**
- Workflows become bloated with meaningless steps
- Hard to debug which step actually failed (if a step doesn't transform, where did the error come from?)
- Testing becomes expensive (more steps = more test fixtures needed)

---

## Decision

### Core Rule
**Each step must transform its input artifact into a semantically different output.**

### Transformation Criteria

A step is a valid transformation if ALL of these are true:

1. **Different Semantics**: The output artifact represents different information than the input
   - ✓ alignment_report → prd: Overview changes to Specification
   - ✓ prd → issues: Spec changes to Implementation Tasks
   - ✗ prd → prd_formatted: Same spec, just prettier

2. **Information Added**: The step adds information the input didn't have
   - ✓ prd → issues: Breaks spec into specific actionable tasks (new info)
   - ✓ issues → agent_brief: Assigns tasks to agents (new info)
   - ✗ prd → prd_summary: Shorter version of same info (not new info)

3. **Output Consumed**: The next step actually uses the output (not a side-effect)
   - ✓ Step 2 produces `issue_list`; Step 3 consumes `issue_list`
   - ✗ Step 2 produces `log.txt`; Step 3 doesn't use `log.txt` (side-effect)

4. **Not Reversible**: You can't recreate the input from the output (meaning info was added/changed)
   - ✓ prd → issues: Can't recreate prd from issues (issues are derived)
   - ✗ prd → prd.backup: Exact copy; could recreate original

### Implementation

In `product-to-issues` workflow:

```yaml
steps:
  - id: 1
    skill: to-prd
    input_artifact: domain_alignment_report   # What we know about domain
    output_artifact: prd                       # What to build (semantic change)
  
  - id: 2
    skill: to-issues
    input_artifact: prd                        # What to build
    output_artifact: issue_list                # How to build it (semantic change)
  
  - id: 3
    skill: triage
    input_artifact: issue_list                 # How to build it
    output_artifact: agent_brief               # Who builds what (semantic change)
```

Each step's output is semantically different and consumed by the next step.

---

## Consequences

### Positive
1. **Clear Workflow Logic**: Every step has a clear reason to exist (it transforms meaningfully)
2. **Easier Validation**: Validators can check that transformation actually happened
3. **Reusable Artifacts**: Each artifact can be independently validated and reused
4. **Better Testing**: Fewer test fixtures needed (each step is essential)
5. **Clearer Skill Purpose**: Skills focus on meaningful transformation, not busywork
6. **Simpler Debugging**: If a step fails, you know it's the transformation (not formatting)

### Negative
1. **Harder Workflow Design**: Requires thinking about what each step adds (not just convenient steps)
2. **More Skill Development**: Can't use simple formatting/renaming skills; need substantive skills
3. **Fewer Intermediate States**: Can't save intermediate formats for debugging (have to go end-to-end)

### Trade-offs
- We chose **meaningful transformation over convenience** because:
  - Clear workflows are easier to understand and maintain
  - Validation gaps caused by hidden steps is worse than missing intermediate formats
  - Reusability of semantic artifacts is valuable

---

## Alternatives Considered

### Alternative 1: Allow Helper Steps
- Permit "formatting" or "renaming" steps that don't transform
- **Rejected because**: Where do you draw the line? Is "fix indentation" allowed? "Add headers?" Then workflows get bloated with trivial steps
- **Consequence**: Unclear workflows; every step must be audited to see if it "counts"

### Alternative 2: Optional Steps
- Allow steps that are sometimes run, sometimes not
- **Rejected because**: Makes workflows non-deterministic; hard to understand what the workflow actually does
- **Consequence**: Confusing execution; unclear which steps are core

### Alternative 3: Inline Transformations
- Let skills do multiple transformations (prd → format → validate → prd_final)
- **Rejected because**: Skills become complex; can't validate intermediate states; reusability broken
- **Consequence**: Skills grow too large; hard to test

### Alternative 4: Artifact Versioning
- Allow prd v1, prd v2, prd v3 to track transformations
- **Rejected because**: Violates single-semantic-artifact rule; clutters artifact space
- **Consequence**: Version explosion; unclear which version to use when

---

## Evidence

This decision was validated during Phase 3:

### Good Composition (product-to-issues)
- Step 1 (to-prd): alignment_report → prd ✓ (transforms: overview → spec)
- Step 2 (to-issues): prd → issue_list ✓ (transforms: spec → tasks)
- Step 3 (triage): issue_list → agent_brief ✓ (transforms: tasks → assignment)

**Result**: All 7 design validation tests pass; workflow is clear and maintainable

### Bad Composition (docs-architecture with mixed steps)
- Step 1 (grill-with-docs): raw_fog → alignment_report ✓ (transforms: uncertainty → knowledge)
- Step 2 (to-prd): alignment_report → prd ✗ (mixing concerns; not part of alignment purpose)
- Step 3 (handoff): prd → prompt_handoff ✗ (expects alignment_report, not prd)

**Result**: Validation gap; artifact orphaning; unclear workflow purpose

---

## Implications for Future Decisions

1. **Workflow Design**: Every step must meaningfully transform (test: can you explain the transformation?)
2. **Skill Design**: Skills should focus on substantive transformation, not formatting
3. **Artifact Validation**: Each artifact should be semantically distinct (not just copies)

---

## Related

- **Pattern**: See `orchestration-patterns.md` → Pattern 3: Artifact Composition & Chaining
- **Guide**: `workflow-design-guide.md` → Step 5: Verify Each Step Transforms Meaningfully
- **Test**: Phase 3 composition validation tests (7/7 pass)
- **Prior Issue**: Orphaned PRD artifact in docs-architecture (Phase 2 discovery)

---

## For Workflow Designers

**Test each step with these questions:**

1. **Semantic Change**: Does the output represent different information than the input?
   - "Is alignment_report different from prd?" → Yes (overview vs. spec)
   - "Is prd_formatted different from prd?" → No (same content, prettier) ❌

2. **Information Added**: Does the step add something new?
   - "Does to-issues add task specificity?" → Yes (new info)
   - "Does format-pretty add info?" → No (just prettier) ❌

3. **Next Step Uses It**: Is the output consumed by step N+1?
   - "Does step N+1 use issue_list?" → Yes
   - "Does step N+1 use log.txt?" → No (side-effect) ❌

4. **Not Reversible**: Can you recreate the input from the output?
   - "Can you recreate prd from issues?" → No (lost info) ✓
   - "Can you recreate prd from prd.backup?" → Yes (exact copy) ❌

**If any test fails, remove the step.**

---

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Why Bad | Better Way |
|---|---|---|---|
| Formatting step | prd → prd_formatted | No transformation | Let consumer format |
| Copy step | artifact → artifact_backup | No transformation | Skip (use version control) |
| Intermediate state | prd_draft → prd → prd_final | Too many states | Combine to single step |
| Renaming | issue_list → issues_v2 | No semantic change | Use single name |
| Convenience | raw → intermediate1 → intermediate2 → final | Too many levels | Reduce to necessary steps |

---

## Acceptance Criteria

This decision is accepted when:
- ✓ product-to-issues has 3 steps, each meaningfully transforms (prd→issues→briefs)
- ✓ No pass-through or formatting steps in any workflow
- ✓ Each step's output is consumed by next step (artifact continuity)
- ✓ All composition validation tests pass (7/7)
- ✓ New workflows follow this pattern (meaningful transformation per step)

---

## Questions & Answers

**Q: What about helper artifacts (logs, diagnostics)?**  
A: Those aren't part of the workflow artifact chain; they're side-effects. The chain is: input → step1 → artifact1 → step2 → artifact2 → etc. Logs can exist but don't advance the chain.

**Q: What if I need intermediate states for debugging?**  
A: Save them outside the workflow (e.g., in artifacts/debug/). The workflow chain should only include semantic transformations.

**Q: Can one step have multiple outputs?**  
A: The workflow only tracks the primary output (for the chain). Other outputs are side-effects. If you need multiple tracked outputs, you need multiple workflows.

**Q: What's the difference between "information added" and "reformatted"?**  
A: - Information added: New data, analysis, decisions (prd→issues adds specific tasks)
   - Reformatted: Same data, different structure (prd→prd_json is reformatting)
   
**Q: Should I combine prd + issues into one step?**  
A: No. They're meaningfully different transformations (spec-to-tasks is one transformation, tasks-to-assignments is another). Separate steps are correct.
