---
name: workflow-orchestrator
description: select and stage a workflow from a repository sensemaking brief. use when the user has a diagnostic brief and wants a workflow plan, prompt chain, guided execution plan, or guarded orchestration with approval gates.
---

# workflow-orchestrator

## Workflow
1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Select Workflow**: Match the recommended path to an available workflow in the `workflow-registry.yaml`.
3. **Plan**: Produce a Workflow Orchestration Plan with ordered steps and approval gates.
4. **Mode Selection**: Determine the execution mode (Default: `plan_only`).
5. **Execute/Generate**:
   - `plan_only`: produce the plan artifact and stop. No workflow steps are executed, and no repository files are modified (except the plan itself if explicitly requested).
   - `prompt_chain`: produce copy/paste prompts and stop.
   - `guided_execution`: execute one eligible step, validate its output artifact, write/update the run log, then stop for approval.
   - `autonomous_execution`: execute eligible steps until the next approval gate, failed validation, non-executable skill, or stop condition.
    - `yolo_execution`: [STABLE] execute only eligible steps with no intermediate approval. **MANDATORY**: Run `Post-Step Verification` after each skill execution. Stop immediately on missing artifact, invalid handoff, failed verification (script or LLM), non-executable skill, dirty git state, or run-log failure.

## Output Format
Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure. 

**CRITICAL**: Every plan MUST include the **Section 11: Machine-readable plan** YAML block. Plans without this block are invalid and violate the artifact contract.

Use [Run Log Template](references/run-log-template.md) only when recording an actual guided or autonomous run.

## Execution Modes
Use [Execution Modes](references/execution-modes.md) as the source of truth. The inline behavior summary in the workflow above is only a control-plane shortcut.

## Boundary Rules
- **Safety First**: Default to `plan_only` mode. 
- **Contract Enforcement**: If a brief does not contain a valid machine-readable handoff, or the requested execution mode is not allowed by [Execution Modes](references/execution-modes.md), the orchestrator MUST refuse the request or downgrade to `plan_only` or `guided_execution`.
- **Validator Stack Compliance**: The orchestrator MUST follow the [Validator Stack Policy](references/validator-stack-policy.md) for every step. ALL registered validators (Generic and Specialized) MUST pass before a step is considered complete.
- **Machine Verifiability**: The orchestrator MUST generate Section 11 (Machine-readable plan) in every orchestration plan. Failure to do so renders the artifact non-verifiable.
- **Handoff Compliance**: Transitions between skills in a workflow MUST comply with the [Artifact Contracts](references/artifact-contracts.yaml).
- **Plan-only Hygiene**: In `plan_only` mode, the orchestrator MUST NOT populate `Section 9: Prompt Chain` with copy-pasteable prompts. Section 9 should explicitly state: `N/A - mode is plan_only. No prompt chain generated.`
- **Path Normalization**: Generated artifacts, plans, and run logs MUST use relative paths (e.g., `artifacts/name.md` or `./runs/...`) and NEVER use absolute `file:///` links.
- **Execution Authority**: The orchestrator may execute only registry-approved steps where `availability.executable_by_orchestrator: true` and `availability.type` is either `local` or `local_command`.
  - `local` means the skill is bundled in this repository.
  - `local_command` means the skill is installed in the local working environment and MUST define an `invocation` block with `runtime`, `command`, `input_artifact`, and `output_artifact`.
  - `external`, `external_required`, and `prompt_only` steps must be treated as routing targets, not executable steps.
- **YOLO Safety Heuristics (Pre-flight)**:
    - **Context Check**: Before starting a YOLO chain, estimate the total repository context + task description. If it exceeds 100k tokens (or 80% of the model's comfortable limit), the orchestrator MUST automatically downgrade to `guided_execution` or `autonomous_execution` with mandatory gates.
    - **Clean State**: Verify `git status` is clean. Record the current `HEAD` SHA in the Run Log as `PRE_YOLO_COMMIT`.
    - **Explicit Pre-flight Log**: Every YOLO run log MUST include a `Preflight` block documenting the Level 1 structural validation (`python scripts/validate-repo.py`), current branch safety, and dry-run status.
- **YOLO Post-Step Verification**:
    - After every skill execution in YOLO mode, the orchestrator MUST perform the full validator stack defined in `artifact-contracts.yaml`:
        1. **Level 2 (Generic)**: Execute the `verification.generic_validator` for the produced artifact.
        2. **Level 3 (Specialized)**: Execute all scripts listed in `verification.specialized_validators`.
        3. **LLM Self-Review**: Perform a 1-shot internal review of the artifact against the `verification.llm_criteria` if present. 
    - **Failure Protocol**: If ANY check fails, the orchestrator MUST:
        - Stop the execution loop immediately.
        - Report the failure details in the Run Log.
        - Recommend the specific rollback command: `git reset --hard {PRE_YOLO_COMMIT}`. For no-mutation dry-runs, use `rollback_recommendation: "No mutation occurred; no reset required."`
- **YOLO Step Completion**:
    - A YOLO step is not complete when a command is merely named.
    - A YOLO step is complete only when the declared `output_artifact` exists, satisfies `artifact-contracts.yaml`, and is recorded in the run log.
    - For `local_command` steps, the orchestrator MUST use the exact `invocation.command`; it must not invent command names.
    - After each step, preserve only the declared output artifact, compact run-log entry, and fields required by the next step.
    - Stop immediately if the command output cannot be mapped to the declared `output_artifact`.
- **Approval Gates**: 
    - Do not bypass approval gates in `guided_execution` or `autonomous_execution` mode. 
    - In `guided_execution`, the orchestrator MUST record an explicit `gate_result: approved_by_user` (including `approved_at` and `approved_by`) in the run log before proceeding. Implicit approval is forbidden.
    - In `yolo_execution`, approval gates are operationally bypassed only after eligibility checks, but they MUST remain present in the machine-readable plan and run log with `gate_behavior: bypassed_by_yolo`.
- **Research & Subset Runs**:
    - Research-mode or subset workflow runs (e.g., executing only Steps 1 & 2) MUST still produce contract-valid `workflow_orchestration_plan` and `run_log` artifacts. 
    - Research mode may limit steps, but it MUST NOT relax Section 11 (must use `artifact_id` and `chosen_workflow_id`), `validator_stack`, path normalization, or approval-gate logging requirements.
    - **Formal Subset Semantics**: When executing a subset of a registry workflow, the plan MUST set `subset_run: true` and define `included_steps` (contiguous from step 1), `excluded_steps` (with reasons), and matching `steps` entries. This allows `validate-plan.py` to verify the subset against the full registry definition.
- **Strict Path Hygiene**:
    - Generated artifacts, plans, run logs, and user-facing summaries MUST use relative paths and NEVER use absolute `file:///` links. This applies to both the file content and the final response text.

## Local Command Execution

When executing a `local_command` step, the orchestrator MUST:

1. Read the skill's `invocation` block from `skill-registry.yaml`.
2. **Environment Pre-flight**: Verify the `invocation.runtime` is available in the local environment. If the runtime is missing, stop and report the environment mismatch.
3. Pass only the declared `input_artifact` plus the minimal necessary context.
4. Invoke the declared `command`; do not invent command names.
5. Treat the declared `output_artifact` as the only valid result of the step.
6. Append a compact run-log entry before continuing.
7. Summarize prior full artifacts once more than one artifact exists in context.
8. **Ghost Artifact Handling**: If a skill produces files or artifacts not declared in the `output_artifact` contract, the orchestrator MUST NOT pass them forward as context. Record undeclared outputs in the run log and require user approval before proceeding if they contaminate the workspace.
9. Stop if the command, input artifact, output artifact, or runtime is missing.

A `local_command` step is not complete until its declared `output_artifact` exists and satisfies the next handoff contract.

## Hard Stop Conditions
The orchestrator MUST stop and report instead of continuing when any of these occur:
- The skill is `external`, `external_required`, or `prompt_only`.
- The next step is `workflow-orchestrator` itself, unless the mode is `plan_only`.
- The expected output artifact is missing, malformed, or does not satisfy `artifact-contracts.yaml`.
- The selected workflow does not explicitly allow the requested execution mode.
- The run log cannot be created or updated.
- The working tree is dirty before `autonomous_execution` or `yolo_execution`.
- The current branch is `main` or `master` during a mode that can mutate files.
- **Interrupt Protocol**: If execution is interrupted, the orchestrator MUST attempt to save a partial Run Log to preserve the state of completed steps.
- More than one retry would be required for the same step.
- The current context contains more than one full artifact from prior steps; summarize earlier artifacts before continuing.

## References
- [Validator Stack Policy](references/validator-stack-policy.md)
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Artifact Contracts](references/artifact-contracts.yaml)
- [Execution Modes](references/execution-modes.md)
- [Git Safety Policy](references/git-safety-policy.md)
- [Recovery Policy](references/recovery-policy.md)
- [Approval Gates](references/approval-gates.md)
- [Run Log Template](references/run-log-template.md)
- [Usage Research Scenarios](references/usage-research-scenarios.yaml)
- [Usage Research Rubric](../../docs/usage-research-rubric.md)

