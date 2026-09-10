# Customer Discovery bounded workflow

**Status:** current agent-native PM workflow contract for the first vertical slice.  
**Execution model:** active-agent controlled; not a registered Wayfinder workflow and not a deterministic semantic router.

## Goal

Allow a user to authorize a bounded Customer Discovery sequence without requiring ceremonial approval between every useful analytical step while preserving evidence, responsibility, authority, and stop boundaries.

## Canonical responsibility sequence

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

Candidate capabilities currently declared for those responsibilities are respectively `persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, and `hypothesis`.

The responsibility sequence is canonical; the capability selection is agent-authored. A later implementation may add another capability for the same responsibility without changing the workflow contract.

## Authorization envelope

An instruction such as "run Customer Discovery end-to-end" authorizes the active agent to continue across the sequence while each next responsibility is warranted and the required evidence/authority is available.

The envelope does not authorize unrelated scope expansion, target-repository mutation, customer contact, experiment execution, publishing, price changes, or other external mutation.

## Step semantics

For each responsibility:

1. reconstruct current Campaign state and relevant admitted evidence;
2. decide whether the responsibility is already satisfied, warranted, blocked, or unnecessary;
3. if work is needed, inspect the current capability catalog using the explicit responsibility type;
4. select a capability semantically; do not treat catalog order as ranking;
5. execute the canonical Skill through the available harness representation;
6. run canonical artifact validation immediately;
7. admit useful valid artifact bytes into the Campaign;
8. author the Campaign advance/defer/close decision with exact evidence refs;
9. continue only if the next responsibility remains warranted inside the envelope.

A step may be skipped when durable evidence already satisfies the responsibility. Skipping a capability is not skipping the responsibility judgment.

## Mandatory stops

Stop or defer on missing decision-critical evidence, decision-blocking owner intent, validation failure, Campaign integrity failure, scope expansion, external action, insufficient authority, material contradiction, unwarranted next responsibility, or a harness failure that makes native invocation untrustworthy.

## Completion

The bounded workflow is complete when the Campaign has a defensible `product_hypothesis` result or explicitly records why that terminal responsibility was deferred/closed, and the durable handoff contains enough state for a fresh agent to reconstruct the decision path.

`workflow authorized != every step mandatory != external mutation authorized`.
