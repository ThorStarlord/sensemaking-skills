# Example: YOLO Hallucination Failure (Negative Fixture)

This example demonstrates a `repository_sensemaking_brief` that contains hallucinated evidence. In YOLO mode, the `validate-brief.py` script would detect this and halt the execution.

## 1. Repository Goal
Stabilize the sensemaking-skills repository.

## 2. Current Shape
The repository is a collection of skills and registries.

## 3. Strong Signals
- Registries are present.
- Validators are in place.

## 4. Missing Pieces
- Automated rollback tests.

## 5. Improvement Opportunities
- Add more negative fixtures.

## 6. Weakest Boundary
The boundary between autonomous execution and safety verification.

## 7. Evidence
The system currently lacks a dedicated `scripts/fake-validator-99.py` file to handle automated recovery.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: "scripts/validate-repo.py"
    lines: "L1-L10"
    quote: "import os"
    supports_claim: "Validators are present."
  - file: "scripts/hallucinated-file.py"
    lines: "L1-L5"
    quote: "print('this file does not exist')"
    supports_claim: "A fake file that should trigger a YOLO halt."
```

## 9. Why This Boundary Matters
It prevents the orchestrator from making decisions based on files that don't exist.

## 10. Candidate Next Steps
- Implement rollback.

## 11. Recommended Next Step
Implement the rollback test.

## 12. Recommended Workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: yolo_execution
weakest_boundary: safety_verification
required_inputs:
  - id: repository_state
    value: current
```

## 14. Ready-to-copy prompt
N/A
