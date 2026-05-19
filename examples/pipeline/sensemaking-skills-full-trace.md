# Example: Full Sensemaking Pipeline Trace (sensemaking-skills)

This example demonstrates the complete V1 pipeline run on the `sensemaking-skills` repository itself.

## Stage 1: Problem Frame (`problem-framer`)
- **Raw Fog**: "How do we make sensemaking skills safe and reliable for autonomous agents?"
- **Problem Under the Problem**: Unreliable handoffs between diagnostic judgment and execution coordination.
- **Object Under Pressure**: The artifact-contract between `repo-sensemaker` and `workflow-planner`.
- **Next Artifact**: Unknowns Map

## Stage 2: Unknowns Map (`unknowns-mapper`)
- **Knowns**: We have a validator, registries, and templates.
- **Unknowns**: How to deterministically validate machine-readable handoffs in Markdown.
- **Assumed**: A machine-readable YAML block is sufficient for safe routing.
- **Next Artifact**: Repository Sensemaking Brief

## Stage 3: Repository Sensemaking Brief (`repo-sensemaker`)
- **Weakest Boundary**: The manual linkage between a prose brief and a workflow ID.
- **Evidence**: `skills/workflow-orchestrator/references/workflow-registry.yaml` contains IDs that aren't yet enforced by a hard schema check in the brief.
- **Machine-readable handoff**:
  ```yaml
  recommended_workflow_id: validator-tdd
  recommended_execution_mode: guided_execution
  weakest_boundary: artifact-contract
  ```
- **Next Artifact**: Workflow Orchestration Plan

## Stage 4: Workflow Orchestration Plan (`workflow-planner`)
- **Chosen Workflow**: `validator-tdd`
- **Execution Mode**: `guided_execution`
- **Approval Gates**: 
  - [ ] Approve `artifact-contracts.yaml` schema.
  - [ ] Approve validator extension for contract check.
- **Next Step**: Run `validator-tdd` to implement the contract.

## Stage 5: Prompt Handoff (`prompt-handoff`)
- **Target Skill**: `validator-tdd`
- **Context Summary**: Fog resolved from "safety vibes" to "contract enforcement." We are hardening the artifact-contract through automated TDD.
- **Ready-to-copy Prompt**:
  ```markdown
  /validator-tdd
  
  Target: Harden the artifact-contract between repo-sensemaker and workflow-orchestrator.
  Input: [Link to Brief]
  Mode: guided_execution
  ```

## Expected Behavior Checklist
- [x] Demonstrates the transition through all five core skills.
- [x] Moves from "Raw Fog" to a "Ready-to-copy Prompt."
- [x] Includes a machine-readable handoff in Stage 3.
- [x] Recommends a relevant execution mode in Stage 4.
