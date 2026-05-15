# Repository Sensemaking Brief

## 1. Repository goal
Establish a robust, contract-enforced "Sensemaking Skills" ecosystem for turning raw repository "fog" into executable, registry-compliant AI workflows.

## 2. Current shape
- `skills/`: Modular sensemaking logic (framer, mapper, sensemaker).
- `scripts/`: Validation stack for artifacts and repository state.
- `examples/skill-tests/`: New, hardened verification suite for Wave 1/2 compliance.
- `workflow-registry.yaml`: Orchestration metadata.

## 3. Strong signals
- **Artifact Rigor**: Every skill has a corresponding template and validation script (e.g., `scripts/validate-artifact.py`).
- **Hardened Testing**: The `ALL-SKILLS-TEST-PLAN.md` provides a clear, multi-phase roadmap for repository stability.

## 4. Missing pieces
- **Semantic Continuity Validation**: While structural validation is strong, automated checks for "semantic alignment" between piped skills (e.g., Mapper addressing the Framer's OUP) are missing.
- **Wave 2 Automation**: Multi-skill handoff tests are planned but not yet institutionalized as a single-command suite.

## 5. Improvement opportunities
- **Unified Compliance Reporting**: Consolidating per-task logs into a centralized dashboard or report.
- **Registry Schema Docs**: Explicit documentation for the `workflow-registry.yaml` schema to prevent "OUP" ambiguity.

## 6. Weakest boundary
The **Semantic Thread Handoff**: The risk that an upstream skill (Problem Framer) produces a structurally valid but semantically disconnected artifact for the downstream skill (Unknowns Mapper).

## 7. Evidence
- `examples/skill-tests/ALL-SKILLS-TEST-PLAN.md`: Defines Phase 2 (Isolated) and Phase 3 (Handoff) as distinct steps, separated by manual/audit review.
- `scripts/validate-artifact.py`: Focuses on field presence and template adherence rather than cross-artifact semantic verification.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: examples/skill-tests/ALL-SKILLS-TEST-PLAN.md
    lines: 38-42
    quote: "1. Phase 1: Read-only Audits... 2. Phase 2: Isolated Output Artifacts... 3. Phase 3: Handoff & Full-chain Tests"
    supports_claim: "Verification of isolated units precedes verification of semantic chains."
  - file: scripts/validate-artifact.py
    lines: 10-20
    quote: "def validate_structure(artifact_type, file_path):"
    supports_claim: "Current validation is primarily structural/contractual."
```

## 9. Why this boundary matters
If the semantic thread is broken, the `workflow-orchestrator` will generate valid-looking plans that solve the wrong problem or fail to address the actual "Object Under Pressure."

## 10. Candidate next steps
- Run Handoff tests (`framer-to-mapper`) to verify thread integrity.
- Implement a `validate-thread.py` script to check OUP consistency across artifacts.
- Update `ALL-SKILLS-TEST-PLAN.md` to include semantic success criteria.

## 11. Recommended next step
Execute Task 2 (`iso-mapper-001`) using the output of Task 1 (`iso-framer-001`) as a direct input to test the Handoff boundary.

## 12. Recommended workflow
`handoff-verification`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: handoff-verification
recommended_execution_mode: plan_only
weakest_boundary: semantic_thread_handoff
required_inputs:
  - repository_sensemaking_brief
  - problem_frame
  - unknowns_map
```

## 14. Ready-to-copy prompt
Execute the handoff verification workflow using `examples/skill-tests/problem-framer/problem_frame.md` as the producer and `unknowns-mapper` as the consumer. Focus on OUP alignment.
