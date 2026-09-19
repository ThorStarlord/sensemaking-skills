# StrategicPlanner v0 simulated E2E — first-pass active-agent adjudication

schema: strategic-planner-simulated-e2e-v0/adjudication-v0
case: quartz-cli-dry-run-contract
treatment_commit: 7ac691db3ba808fc09b890bb08baa12e51c84193
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Adjudication

Select **Candidate A — bounded contract diagnosis**.

It best preserves the evidence boundary and discriminates between the two materially different downstream repairs (implementation versus documentation/test reconciliation) without prematurely mutating either.

Candidate B and Candidate C remain plausible downstream responsibilities, but neither is currently warranted because the behavior and intended contract are unresolved.

Candidate D is **not materially distinct enough** from Candidate A. Its CI/test-environment reproduction is a contingent diagnostic branch already contained inside Candidate A's evidence-producing responsibility. Treating it as a separate repository-level candidate adds option noise.

## Final responsibility after treatment

`BOUNDED_CONTRACT_DIAGNOSIS`

This is the same final responsibility as the frozen baseline.

## Treatment contribution

The treatment makes the implementation-repair versus documentation-reconciliation fork more explicit, but the baseline already identified that fork. The treatment therefore improves representation/auditability more than decision selection in this case.

## Defect exposed

`CANDIDATE_SUBSUMPTION_NOISE`

StrategicPlanner v0 asks for materially distinct candidates but does not explicitly tell the semantic reasoner to collapse a contingent substep when one candidate subsumes another.

This is a prompt/contract precision issue, not evidence for a new runtime or ranking mechanism.
