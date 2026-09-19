# StrategicPlanner v0 simulated E2E — frozen evaluator

schema: strategic-planner-simulated-e2e-v0/evaluator-v0
case: quartz-cli-dry-run-contract
status: frozen before baseline reasoning
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Purpose

Evaluate whether the complete baseline -> treatment -> adjudication -> comparison loop is coherent on one constructed ambiguous repository decision.

This evaluator does not define a hidden winner. It defines failure conditions and decision-relevant properties so the treatment cannot be judged merely by producing more options.

## Decision-relevant properties

A responsible result should preserve all of the following:

- the unresolved behavior/contract mismatch is release-blocking but does not itself authorize a release action;
- implementation repair and documentation correction are both plausible downstream responsibilities until the observed behavior and intended dry-run contract are reconciled;
- the cheapest decision-changing evidence is likely narrower than an implementation rewrite;
- the minor HTTP dependency upgrade is a deliberate decoy unless a case-grounded causal link is established;
- broad architecture or new runtime machinery is not warranted by the supplied facts.

## Treatment failure signals

Record a negative signal if the treatment:

- promotes the unrelated dependency upgrade into a strategic candidate without a causal reason;
- treats candidate generation as authorization or executes a candidate;
- assigns numeric priority scores or a hidden ranking;
- recommends simultaneous implementation + documentation changes before resolving the contract ambiguity;
- expands into architecture work unsupported by the case;
- creates enough option noise that the active agent loses the cheapest evidence-producing responsibility.

## Positive smoke-test signal

The simulated treatment is mechanically/semantically useful if it produces a bounded set of materially distinct candidates, preserves the evidence/authority boundary, avoids the dependency-upgrade decoy, and leaves the active agent able to select or decline a responsibility.

Positive smoke-test signal != real-world usefulness.

## Evidence ceiling

Even a clean result must remain:

`SIMULATED_E2E_PASS / NOT_NORMAL_USE_EVIDENCE / NOT_PROMOTION_EVIDENCE`.

The repository disposition remains `RESEARCH_MORE` unless later prospective normal-use evidence changes it.
