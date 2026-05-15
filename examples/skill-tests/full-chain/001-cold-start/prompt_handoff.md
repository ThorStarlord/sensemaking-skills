# Prompt Handoff

## 1. Target Skill
`workflow-orchestrator` (or User/External Agent)

## 2. Context to Preserve
- **Repository Goal**: Framework for transforming "messy ideas" into "useful AI workflows."
- **Diagnosis**: The repository is in Wave 3 hardening; the `full-local-sensemaking` workflow has been validated as the primary entry point for unformed concepts.
- **Decision**: The `full-local-sensemaking` workflow was successfully planned and validated in `plan_only` mode.

## 3. Task
Proceed with the execution of the `full-local-sensemaking` workflow as staged in the orchestration plan.

## 4. Constraints
- Do not mutate protected files (`skills/**/SKILL.md`, `scripts/**`, etc.).
- Maintain strict artifact contracts.
- No absolute file links in repository artifacts.

## 5. Inputs
- `examples/skill-tests/full-chain/001-cold-start/repo_sensemaking_brief.md`
- `examples/skill-tests/full-chain/001-cold-start/workflow_orchestration_plan.md`

## 6. Expected Output
Execution logs for the first active step of the chosen workflow.

## 7. Stop Condition
Stop after the first step of execution or upon any validation failure.

---

## 8. Ready-to-copy Prompt
```markdown
/workflow-orchestrator
You are the next execution agent. Starting from the staged orchestration plan in examples/skill-tests/full-chain/001-cold-start/workflow_orchestration_plan.md, execute the `full-local-sensemaking` workflow only within the permissions and stop conditions specified.
Ensure all artifact contracts are validated and git status is checked before each step.
```
