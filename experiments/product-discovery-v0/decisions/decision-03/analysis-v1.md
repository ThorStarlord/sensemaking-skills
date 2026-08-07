# Decision 03 — proportional authorization and governance

## 1. Decision
What minimum control set is proportionate for exploratory agent-native workflows with different consequences?

## 2. Known
- **OBSERVED:** ADR 0023 proposes two lanes rather than a single universal authorization regime (`docs/adr/0023-two-lane-experiment-authorization.md:39`).
- **OBSERVED:** EXP-0002 requires an exact frozen envelope and standalone conversational approval, but calls the approval file an audit receipt rather than identity proof (`README.md:50-67`).
- **OBSERVED:** the package also prohibits target mutation, hidden retry, fallback, external-provider calls, repair, and merge; attempts are capped at three.
- **DERIVED:** the repo can express strong controls. It has not compared those controls with lighter ones on user friction or incident prevention.

## 3–4. Uncertainty and type
Dominant: **assurance/governance**. Unknowns: consequence tiers, threat model, which controls prevent plausible harm, approval fatigue, and minimum traceability. Real target mutation or spend changes the risk; a local read-only analysis does not.

## 5. Alternatives
1. Ordinary conversational consent plus platform sandbox for read-only, zero-spend work.
2. Proportional frozen envelope: explicit target, write boundary, spend, attempt limit, and prohibited actions; one approval.
3. Full campaign policy, durable ledger, digests, reservation/finalization for every exploration.
4. Do nothing beyond existing coding-agent permissions.

## 6. Highest-value uncertainty
Which plausible harms survive platform controls, and which additional control actually prevents each one? This can reverse the decision more than convenience measurements alone.

## 7–9. Cheapest credible experiment
**Hypothesis:** a short consequence-based checklist plus one explicit approval is enough for read-only/no-spend exploration; durable campaign controls become worthwhile only for mutation, external spend, unattended repetition, or canonical-evidence claims.

Tabletop 8 real proposed sessions. For each, list assets/actions, worst credible harm, existing sandbox control, additional control, burden, and residual risk. Run only the read-only cases using the light envelope; do not simulate harmful mutations.

- **Observations:** prevented action mapped to control, approval steps/time, misunderstandings, uncontained risks.
- **Success:** each retained control maps to a credible harm and operators correctly understand the boundary.
- **Failure:** material actions can occur outside the envelope or users approve without understanding it.
- **Kill:** reject the light lane if it permits target mutation/spend/unattended execution without a reliable boundary.
- **Ambiguous:** no incidents occur but the sample never exercises a boundary.

**Available probe:** mapping current EXP-0002 controls shows several protect consequences absent from this documentation-only task; thus copying all controls here would be ceremonial. Actual comprehension and incident rates **REQUIRE_REAL_WORLD_EVIDENCE**.

## 10. Synthesis
- **Original hypothesis:** exploratory work needs lightweight governance.
- **Observations:** strong machinery exists; proportionality evidence does not.
- **Surprise:** conversation can be authority while the file is only receipt, separating consent from accounting.
- **Contradiction:** extensive controls coexist with a zero-provider, read-only intended run.
- **Changed understanding:** governance should be selected from consequences, not the label “experiment.”
- **Current preferred:** proportional frozen envelope; ordinary consent for strictly read-only/no-spend/manual work, stronger accounting when consequences increase.
- **Confidence:** medium as principle, low on exact tier boundaries.
- **Next experiment:** consequence-control tabletop plus observed consent comprehension.
- **Disposition:** **REVISE** universal campaign governance into consequence-based controls.
