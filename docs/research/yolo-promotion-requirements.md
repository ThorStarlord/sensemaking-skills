# YOLO Mode Promotion Requirements

## 1. Current State Analysis
YOLO execution mode (`yolo_execution`) is currently defined as the maximum automation mode for local sensemaking and implementation skills.
Its current boundaries include:
- All approval gates are bypassed.
- Requires explicit opt-in via an exact opt-in string: `"I choose yolo_execution and accept automated repository changes, feature-branch commits, bypassed gates, and recovery risk."`
- Operates exclusively on a feature branch (direct commits to `main` or `master` are prohibited).
- Demands a `Run Log` before and after mutations.
- Adheres to `Git Safety Policy` and `Recovery Policy`.
- Allowed skills are strictly `local` or `local_command`. External or prompt-only skills cause a hard stop.

While the git-level boundaries are well-defined, the mode is currently considered "draft" because of the inherent risks of autonomous execution without intermediate human review.

## 2. Core Risk: Compounding Errors
The primary danger of YOLO mode is the compounding of errors. Without intermediate approval gates, an error or hallucination in Step 1 (e.g., misinterpreting the problem frame) becomes the factual foundation for Step 2. Step 2's output, now deeply flawed, is passed to Step 3, leading to an exponential degradation of quality and potentially destructive or nonsensical repository modifications.

## 3. Proposed Mitigations for Promotion
To safely graduate YOLO mode from "draft" to a fully supported production feature, the following mitigations must be implemented to act as automated circuit breakers:

### A. Task Scoping Constraints
- **Context Window Fitness:** YOLO mode should only be permitted for small, tightly-scoped tasks that fit comfortably within the LLM's context window. If the task is too broad, the orchestrator should automatically downgrade the execution mode to `guided_execution` or reject the request.
- **Complexity Thresholds:** Establish metrics to reject YOLO mode if the repository state or the requested change exceeds a predefined complexity threshold.

### B. Intermediate Validations
- **Script Validators:** Introduce programmatic validators (e.g., syntax checks, unit test execution, artifact schema validation) that run automatically after each step.
- **LLM Validators:** Implement a lightweight, parallel LLM review step that evaluates the output of a given step against the original problem frame. If the LLM validator detects drift or hallucination, YOLO execution halts.
- **Final Validation:** A comprehensive final validation (both script and LLM) must pass before the YOLO chain is considered successful.

### C. Negative Testing / Fixtures
- **Fail-Fast Mechanisms:** If any intermediate validation fails, YOLO mode must immediately halt, preventing the error from passing to the next step.
- **Rollback Integration:** Upon validation failure, the orchestrator should optionally trigger the `Recovery Policy` to reset the feature branch to its pre-YOLO state, leaving a detailed error log.

## 4. Promotion Checklist
Before YOLO mode can be officially promoted, the following tasks must be completed and merged:

- [ ] **Artifact Schema Enhancements:** Define specific script/LLM validation contracts in `../../skills/workflow-orchestrator/references/artifact-contracts.yaml` for YOLO steps.
- [ ] **Task Scoping Logic:** Implement heuristic checks in `../../skills/workflow-orchestrator/` to evaluate task size and context fit before allowing YOLO mode.
- [ ] **Validation Runner:** Build or integrate a mechanism to execute intermediate script and LLM validators during the YOLO loop.
- [ ] **Negative Fixtures:** Add test cases in `examples/` that prove YOLO mode successfully halts and rolls back when a step produces an invalid output or fails validation.
- [ ] **Documentation Update:** Remove "draft" references and explicitly document the automated validation safety nets in `../../skills/workflow-orchestrator/references/execution-modes.md` and `../../skills/workflow-orchestrator/SKILL.md`.
