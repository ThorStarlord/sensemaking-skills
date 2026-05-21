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
The **skill execution boundary** between workflow orchestration and skill invocation is the primary blocker preventing end-to-end workflow completion. The orchestration system is production-ready for planning, but cannot generate intermediate artifacts because skills have no execution mechanism.

### Why This Boundary Matters
Without skill execution, workflows halt after Step 2, preventing:
- Full end-to-end testing of the orchestration system
- Real-world usage where artifacts must be generated
- Validation of artifact contract enforcement across all steps
- Discovery of integration issues between skills

## Evidence
The orchestration system was tested with the full-local-sensemaking workflow in yolo_execution mode:
- ✅ Pre-flight checks: PASSED (git validation, repository structure)
- ✅ Plan generation: PASSED (5-step plan created successfully)
- ✅ Step 1 (problem-framer): PASSED (fixture artifact validated)
- ✅ Step 2 (unknowns-mapper): PASSED (fixture artifact validated)
- ❌ Step 4 (repo-sensemaker): FAILED (no skill execution, no fixture)

This pattern demonstrates that the orchestration logic is correct but blocked by lack of artifact generation.

## Evidence Excerpts
```yaml
evidence_excerpts:
  - file: "scripts/workflow-runtime.py"
    lines: "190-210"
    quote: "Modified execute_step() to use fixture artifacts when --use-fixtures flag is set"
    supports_claim: "Fixture infrastructure enables partial workflow testing"
  
  - file: "examples/problem-framer/problem_frame-fixture.md"
    lines: "1-50"
    quote: "Complete fixture artifact with all required sections validated against contract"
    supports_claim: "Fixture artifacts can satisfy validator requirements"
  
  - file: "EXECUTION_IMPROVEMENTS.md"
    lines: "30-45"
    quote: "Step 2: unknowns-mapper | FAILED (missing artifact sections) | Root Cause: The unknowns-mapper skill is not being invoked/executed"
    supports_claim: "Lack of skill execution is the primary blocker"
```

## Candidate Next Steps
1. **Create repo-sensemaker fixture**: Would allow workflow to progress to Step 5
2. **Implement skill_executor.py**: Design invocation mechanism for skills
3. **Add parametrized tests**: Cover all 5 execution modes with fixtures
4. **Complete remaining fixtures**: workflow-planner, prompt-handoff outputs
5. **Profile execution time**: Measure orchestration overhead
6. **Document skill contract**: Specify how skills should be invoked and validated

## Recommended Next Step
**Create skill_executor.py with support for fixture artifacts and Claude API invocation**

This addresses the critical blocker while maintaining testability. The architecture should:
1. Accept skill name, input artifacts, and execution mode (fixture/live)
2. Return output artifact or error with clear diagnostics
3. Support both fixture mode (for testing) and Claude API mode (for production)
4. Integrate seamlessly with execute_step() in workflow-runtime.py

## Recommended Workflow
For iterative development of the skill execution infrastructure:
1. Use **fixture mode** with --use-fixtures flag for rapid orchestration testing
2. Implement Claude API integration in skill_executor.py
3. Gradually migrate from fixtures to live skill execution
4. Add parametrized tests as new skills are executable

## Machine-readable Handoff
```yaml
source_intent_ref: "user_intent"
recommended_workflow_id: "implementation-workflow"
recommended_execution_mode: "guided_execution"
weakest_boundary: "skill_execution"
required_inputs:
  - problem_frame
  - unknowns_map
  - user_intent
user_implied_fog_type: "unknown_unknowns"
primary_fog_type: "architecture_fog"
diagnosis_conflict: false
escalation_recommended: false
```

## Ready to Copy Prompt
Use the identified weak boundary (skill execution) as the starting point for implementation:

**Problem Statement**: Skills exist as SKILL.md prompts but have no invocation mechanism, blocking end-to-end workflow execution.

**Artifact Context**: This brief is based on analysis of the sensemaking-skills repository and validated with fixture-based orchestration testing.

**Next Action**: Design and implement skill_executor.py to invoke skills via Claude API or subprocess, starting with support for fixture artifacts in testing mode.
