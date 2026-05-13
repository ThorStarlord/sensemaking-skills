# Example: Repository Sensemaking Brief (sensemaking-skills)

## 1. Repository goal
Turn vague project uncertainty into clear problem frames, research paths, and next-step prompts.

## 2. Current shape
- `skills/`: Flagship skills (`repo-sensemaker`, `workflow-orchestrator`).
- `workflows/`: Experimental high-velocity chains.
- `examples/`: Validation fixtures for diagnosis and orchestration.
- `docs/`: PRDs and Issue lists.

## 3. Strong signals
The 11-section `repo-sensemaker` template provides a high-leverage diagnostic frame. The separation of "diagnosis" from "action" protects the repo's core intent.

## 4. Missing pieces
- Automated parity tests for the new two-skill architecture.
- More diverse "Weakness Types" examples (e.g., Vocabulary Drift).

## 5. Improvement opportunities
Consolidate shared references (like `skill-registry.yaml`) into a root `references/` directory to avoid duplication.

## 6. Weakest boundary
The linkage between `repo-sensemaker` output and `workflow-orchestrator` input. It is currently manual and "vibe-based" rather than contract-enforced.

## 7. Why this boundary matters
If the brief doesn't explicitly name a workflow ID, the orchestrator might guess the wrong path, leading to unsafe or irrelevant execution.

## 8. Candidate next steps
1. Create a `shared-vocabulary.md` reference.
2. Add a `validator-tdd` run to implement a brief-to-plan contract.

## 9. Recommended next step
Implement the `validator-tdd` workflow to harden the contract between the two skills.

## 10. Recommended workflow
`validator-tdd` (from `workflow-orchestrator`).

## 11. Ready-to-copy prompt
```markdown
/workflow-orchestrator

Brief Consumed: [Link to this brief]
Target: Harden the contract between repo-sensemaker and workflow-orchestrator.
Workflow: validator-tdd
Mode: guided_execution
```

## Expected Behavior Checklist
- [ ] Identifies the "Weakest Boundary" as the manual handoff between skills.
- [ ] Recommends a specific workflow from the registry.
- [ ] Provides a ready-to-copy prompt for the orchestrator.
