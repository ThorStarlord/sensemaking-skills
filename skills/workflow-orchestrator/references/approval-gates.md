# Approval Gates for Workflow Orchestration

To ensure safety, every workflow step must pass an approval gate:

1. **Alignment Gate**: User confirms that the extracted goals and mental models are correct.
2. **Design Gate**: User approves the PRD or Architecture spec before issues are generated.
3. **Task Gate**: User reviews the issue list and individual Agent Briefs for scope and safety.
4. **Execution Gate**: User approves the code changes and commit summaries generated during TDD.
5. **Handoff Gate**: User confirms the final state of the repository after the run.

## Enforcement
In `guided_execution` mode, the orchestrator MUST stop and wait for a "Go/No-Go" signal after every gate.
In `autonomous_execution` mode, these gates are logged but bypassed (requires explicit high-risk opt-in).
