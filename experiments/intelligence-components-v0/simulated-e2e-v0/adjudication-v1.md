# StrategicPlanner v0 simulated E2E — repaired active-agent adjudication

schema: strategic-planner-simulated-e2e-v0/adjudication-v1
case: quartz-cli-dry-run-contract
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Adjudication

Select **Candidate A — bounded contract diagnosis**.

Candidates B and C are materially distinct downstream repairs, but both depend on evidence Candidate A is designed to obtain. The candidate set now keeps the CI-specific reproduction path inside Candidate A rather than presenting it as a separate strategic responsibility.

## Final responsibility after treatment

`BOUNDED_CONTRACT_DIAGNOSIS`

This remains the same final responsibility as the frozen baseline.

## Treatment contribution

The repaired treatment produces a cleaner explicit option set without changing the decision. It makes the downstream implementation-versus-contract fork auditable, avoids the dependency-upgrade decoy, and preserves the active agent's authority to select the responsibility.

## Residual limitation

The simulated case does not show that StrategicPlanner improves decision quality over baseline. It shows only that the full loop can operate coherently after a small candidate-deduplication prompt repair.
