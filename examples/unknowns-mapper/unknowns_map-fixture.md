# Unknowns Map: Sensemaking Skills Repository

## 1. Knowns
- The repository uses a five-skill sensemaking pipeline: problem-framer, unknowns-mapper, repo-sensemaker, workflow-planner, and prompt-handoff.
- Artifacts are validated against contracts in `artifact-contracts.yaml`.
- The workflow-runtime.py orchestrator manages execution across 5 modes: plan_only, prompt_chain, guided_execution, autonomous_execution, and yolo_execution.
- Pre-flight checks validate git state and repository structure before execution.
- Validators enforce zero-tolerance validation in yolo_execution mode (gates are bypassed, validation is strict).

## 2. Unknowns
- How should skills be invoked to produce artifacts (Claude API, local subprocess, mock execution)?
- What is the complete skill execution infrastructure architecture?
- How should fixture artifacts integrate with the testing framework?
- What is the expected timeline for full skill execution support?

## 3. Assumptions
- Skills exist as SKILL.md files with clear templates and examples.
- The artifact contract system is sufficient to validate all skill outputs.
- Fixture artifacts can be used to test orchestration without actual skill execution.
- The workflow-runtime orchestration logic is independent of skill execution mechanism.

## 4. Risks
- **Skill execution blocker**: Without a skill executor, the workflow halts at Step 2 (unknowns-mapper), preventing full end-to-end testing.
- **Artifact format drift**: Skills might produce artifacts that don't match the expected template structure.
- **Testing gap**: Hard to test orchestration logic without being able to progress through all workflow steps.
- **User confusion**: Error messages about missing artifact sections might not make sense without clear fixture examples.

## 5. Research Paths
1. **Design skill execution**: Define API for invoking skills (Claude API, subprocess, or mock).
   - Check existing `skill_executor.py` implementation
   - Evaluate integration points with `execute_step()` in workflow-runtime.py
   - Research fixture vs. live execution trade-offs

2. **Create fixture artifacts**: Generate complete, valid examples for all workflow steps.
   - Problem frame fixture
   - Unknowns map fixture (this artifact)
   - Repository sensemaking brief fixture
   - Orchestration plan fixture (already auto-generated)
   - Run log fixture

3. **Add testing modes**: Implement `--use-fixtures` or `--skip-execution` flag.
   - Allow orchestration testing without skill execution
   - Enable integration tests for all 5 execution modes

4. **Improve error messaging**: Link validator errors to fixture examples.
   - Already done: validator now shows template path
   - Next: embed example artifacts in error messages

## 6. Stopping Rule
Research is complete when:
- At least one valid fixture artifact exists for unknowns_map
- Workflow-runtime can progress through Step 2 using fixtures
- Integration tests pass for plan_only, prompt_chain, and guided_execution modes
- Error messages clearly reference available fixture examples

## 7. Machine-readable routing

```yaml
clarity_assessment: "high"
unknowns_count: 4
assumptions_count: 3
research_needed: true
```
