---
name: discovery
description: Frame an uncertain product problem into evidence-aware problem hypotheses, learning questions, validation approaches, and decision criteria. Use when the active agent has a problem-discovery responsibility, the problem is vague or contested, or investment should be preceded by bounded learning. Produce discovery_findings without treating a research plan as proof that a hypothesis was validated.
---

# Discovery

Satisfy a `problem_discovery` responsibility by producing `discovery_findings`.

## Inputs

Require a problem statement, relevant product/customer context, and known constraints. Consume supplied persona, customer, repository, market, operational, or experiment evidence when available.

## Procedure

1. Read [references/methodology.md](references/methodology.md).
2. Reframe the problem in user/job/outcome terms without smuggling a solution into the problem statement.
3. Separate established observations from candidate root-cause hypotheses.
4. Identify decision-relevant hypotheses; use 3-5 only when that breadth is warranted.
5. For each hypothesis, identify evidence already available, missing evidence, a bounded test/observation, and a result that would change the decision.
6. Sequence learning by uncertainty reduction and cost, not by presentation convenience.
7. Render [references/output-contract.md](references/output-contract.md) and return control.

## Stop or downgrade

- A proposed experiment is not validation evidence.
- If the requested conclusion requires customer or operational evidence that is unavailable, leave the hypothesis unresolved and name the missing evidence.
- Do not launch experiments, contact users, or mutate external systems without separate authority.

## Boundary

`validation plan != validated hypothesis` and `well-structured discovery artifact != correct product direction`.
