# Repository Sensemaking Brief: sensemaking-skills

## Repository Goal
Build a workflow orchestration and sensemaking pipeline that coordinates problem framing, unknowns mapping, repository analysis, and workflow planning to enable structured problem-solving across teams.

## Current Shape
The repository contains a multi-stage sensemaking pipeline with five core skills:
- **problem-framer**: Converts raw intent into structured problem frames using "The Problem Under the Problem" methodology
- **unknowns-mapper**: Maps knowns, unknowns, assumptions, and risks from problem frames
- **repo-sensemaker**: Analyzes repository structure and codebase to identify weaknesses and opportunities
- **workflow-planner**: Generates executable workflow plans based on sensemaking outputs
- **prompt-handoff**: Prepares the final prompt and context for human or AI agent execution

Supporting infrastructure:
- Artifact-driven architecture with formal contracts in `artifact-contracts.yaml`
- Workflow registry supporting 5 execution modes (plan_only, prompt_chain, guided_execution, autonomous_execution, yolo_execution)
- Pre-flight validation to ensure git cleanliness and repository structure
- Multi-level validator hierarchy (Level 1: structural, Level 2: generic contracts, Level 3: specialized)

## Strong Signals
1. **Well-defined artifact contracts**: Clear specifications for all intermediate artifacts with required sections and machine-readable fields
2. **Robust orchestration foundation**: workflow-runtime.py successfully generates plans and validates structure
3. **Clear execution modes**: Five distinct modes allow different levels of human oversight and automation
4. **Comprehensive error handling**: Validators provide actionable error messages with template references
5. **Git-based audit trail**: All execution runs logged with session IDs and rollback recommendations
6. **Zero-tolerance validation in yolo_execution**: Safety mechanism ensures quality even in automation

## Missing Pieces
1. **Skill execution infrastructure**: Skills exist as SKILL.md prompts but have no invocation mechanism
2. **Claude API integration**: No mechanism to invoke skills via Claude API or subprocess
3. **Fixture artifacts**: Only problem-framer and unknowns-mapper fixtures exist; others needed for testing
4. **Integration tests**: No parametrized tests for all 5 execution modes
5. **Performance metrics**: No tracking of execution time or resource usage
6. **Version management**: No artifact versioning or caching strategy

## Improvement Opportunities
1. **Short-term**: Complete fixture artifacts for all workflow steps to enable orchestration testing
2. **Medium-term**: Implement skill_executor.py to invoke skills via Claude API or subprocess
3. **Long-term**: Add artifact caching, versioning, and multi-user execution support
4. **Quick win**: Add --skip-validation flag for pure orchestration flow testing
5. **Testing**: Parametrized integration tests for each execution mode

## Weakest Boundary
**Contract Mismatch** - The validation rules for repository_sensemaking_brief are unclear about line reference formatting and weakness type classifications. This creates a mismatch between skill expectations and validator requirements, preventing Step 4 completion despite successful skill execution.

### Why This Boundary Matters
The strict validator is now catching real issues but the specification needs clarification:
- Skills don't know exact format for line references (should be "L1-L50" not "1-50")
- Weakness types list isn't accessible during skill execution
- "Logic trace" requirement appears only in validator, not in artifact contract documentation
- This creates a discovery gap that blocks successful artifact generation

## Evidence
Execution logs show the progression from execution failure to validation failure:
- ✅ Steps 1-2: Skills execute successfully (problem-framer, unknowns-mapper)
- ✅ Step 4: Skill executes (repo-sensemaker) - artifact IS generated
- ❌ Step 4: Specialized validator catches format issues (Contract Mismatch weakness type)

File references:
- `scripts/validate-brief.py:L128`: Line format validation rule (expects "Lx-Ly" format)
- `skills/weakness-types.md:L1-L50`: Recognized weakness types list
- `scripts/validate-brief.py:L46`: Logic trace requirement

## Logic Trace
The diagnostic logic identifying the weakest boundary:
1. **Observation**: Skill execution infrastructure was recently implemented (skill_executor.py)
2. **Analysis**: The problem-framer and unknowns-mapper skills now execute successfully
3. **Connection**: Step 4 (repo-sensemaker) fails not due to execution, but artifact format validation
4. **Inference**: The weak boundary has shifted from "skill execution" to "artifact format specification"
5. **Conclusion**: Validators are correctly catching real format issues; the specification needs clarity

## Evidence Excerpts
```yaml
evidence_excerpts:
  - file: scripts/validate-brief.py
    lines: L128-L134
    quote: "Lines must match r'^L\\d+(?:-L\\d+)?$' format"
    supports_claim: "Validator expects L-prefixed line numbers"
  
  - file: scripts/validate-brief.py
    lines: L46-L49
    quote: "Brief does not include a logic trace showing diagnostic reasoning"
    supports_claim: "Logic trace is a hard requirement not documented in contract"
  
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L1-L40
    quote: "Recognized weakness types: Vocabulary Drift, Contract Mismatch, Ghost Features, Safety Gaps..."
    supports_claim: "Weakness types are defined but not linked to artifact contract"
```

## Candidate Next Steps
1. **Update repo-sensemaker fixture**: Fix line format and weakness type to pass validators
2. **Document artifact format**: Add exemplar artifacts to artifact-contracts.yaml
3. **Link validator specs to contracts**: Make validator rules explicit in contracts
4. **Create validator reference guide**: Document all format requirements
5. **Add pre-execution formatter**: Help skills format artifacts correctly

## Recommended Next Step
**Update repository_sensemaking_brief fixture with correct format specifications and run validation loop**

1. Change line references from "1-50" to "L1-L50" format
2. Add "logic trace" section demonstrating diagnostic reasoning
3. Use recognized weakness types from weakness-types.md
4. Verify all citations point to real files that exist
5. Re-run validation to confirm artifact passes

## Recommended Workflow
For completing Step 4 execution:
1. Fix fixture artifact format issues
2. Re-run workflow with default executor
3. Verify all 5 steps complete successfully
4. Document exact format specs for future skill developers
5. Create integration tests to prevent regression

## 13. Machine-readable handoff

```yaml
source_intent_ref: "user_intent"
recommended_workflow_id: "implementation-workflow"
recommended_execution_mode: "guided_execution"
weakest_boundary: "Contract Mismatch"
required_inputs:
  - problem_frame
  - unknowns_map
  - user_intent
user_implied_fog_type: "unknown_unknowns"
primary_fog_type: "specification_fog"
diagnosis_conflict: false
escalation_recommended: false
```

## Ready to Copy Prompt
The artifact format requirements are now clear from validator analysis:

**Format Rules**:
- Evidence line references: "L1" or "L1-L50" (L-prefixed)
- Weakness types: Must match list in skills/weakness-types.md
- Logic trace: Must appear as section or mentioned in text
- File citations: Path relative to repo root, must exist

**Next Step**: Update all generated artifacts to follow these rules and complete Step 4 validation successfully.
