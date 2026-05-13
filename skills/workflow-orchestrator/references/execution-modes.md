# Execution Mode Contract

This contract defines the strict permissions and boundaries for each orchestration mode in `workflow-orchestrator`.

| Mode | May create files? | May call downstream skills? | May commit? | Requires approval? |
| :--- | :---: | :---: | :---: | :---: |
| **`plan_only`** | No | No | No | No |
| **`prompt_chain`** | No | No | No | No |
| **`guided_execution`** | Maybe | Yes, one step at a time | No, unless approved | **Yes** |
| **`autonomous_execution`** | Maybe | Yes | Only in feature branch, if explicitly allowed | **High-risk opt-in** |

## Mode Descriptions

### 1. `plan_only` (Default)
The orchestrator selects a workflow and lists the sequence of skills and gates. No actual tools are called beyond reading the repository state.

### 2. `prompt_chain`
The orchestrator generates a sequence of copy-pasteable prompts for the user to run in other agents or sessions. No execution occurs.

### 3. `guided_execution`
The orchestrator runs the workflow one step at a time. After each step (e.g., after `grill-with-docs` produces a report), it MUST stop and wait for explicit user approval before proceeding to the next skill.

### 4. `autonomous_execution`
The orchestrator executes the full skill chain without stopping for intermediate approvals. 
- **Prohibited**: Direct commits to `main` or `master`.
- **Prohibited**: Deleting core architectural files.
- **Requirement**: Must log every step to a `run-log.md`.
- **Requirement**: User must provide an explicit high-risk opt-in string: *"I choose autonomous_execution and accept high-risk bypassed gates."*
