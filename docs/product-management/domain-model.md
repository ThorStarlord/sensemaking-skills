# Product Management domain model

## Core model

A PM Campaign reuses the canonical Sensemaking distinction among goal, uncertainty, responsibility, capability, authority, evidence, artifacts, transitions, and terminal/continuation state.

The PM domain adds a vocabulary for **responsibilities**; it does not create a second Campaign runtime.

## Responsibility taxonomy v1

The smallest current vocabulary that covers the 27-source migration candidates without making every Skill its own type is:

| Responsibility type | Meaning | Candidate capabilities |
|---|---|---|
| `customer_understanding` | Represent who experiences the problem and relevant behavior/context. | persona, customer-journey, ideal-customer-profile |
| `problem_discovery` | Frame consequential customer/product problems and identify what must be learned. | discovery |
| `research_synthesis` | Turn supplied primary/secondary research into traceable patterns and findings. | interview-synthesis |
| `opportunity_mapping` | Relate desired outcomes to evidence-backed opportunities, assumptions, candidate solutions, and tests. | opportunity-tree |
| `product_hypothesis` | Express a falsifiable product bet with measures, risks, and kill criteria. | hypothesis |
| `market_understanding` | Analyze alternatives, competitive context, and positioning evidence. | competitive-analysis |
| `product_specification` | Convert a warranted product direction into bounded requirements. | prd / current `to-prd` adjacency |
| `delivery_specification` | Decompose product intent into user-centered slices and verifiable done states. | user-stories, acceptance-criteria |
| `prioritization` | Compare candidate work using declared evidence, trade-offs, and chosen framework. | prioritize |
| `product_strategy` | Define strategic choices, goals, metrics, sequencing, and business assumptions. | strategy, north-star, okr, roadmap, lean-canvas |
| `experimentation` | Design or analyze tests of product hypotheses using actual supplied observations where required. | experiment-design, ab-test-analysis |
| `product_measurement` | Assess product signals such as PMF using supplied empirical evidence. | measure-pmf |
| `commercial_strategy` | Reason about monetization, positioning, sales enablement, and GTM. | pricing, gtm, battlecard |
| `risk_and_readiness` | Surface failure modes and readiness evidence before consequential release/launch decisions. | pre-mortem, launch-checklist |
| `communication` | Transform established state into stakeholder/user-facing communication. | release-notes, stakeholder-update |

This vocabulary may change only through an explicit domain-contract revision. It is not inferred automatically from user prose by deterministic code.

## Capability selection

The required control flow is:

```text
agent identifies warranted responsibility
-> deterministic catalog returns declared candidates
-> agent inspects evidence/authority/availability
-> agent selects or declines a capability
-> execution returns control to the agent
```

Catalog membership must never be interpreted as recommendation, ranking, or authorization.

## First workflow envelope

The first bounded semantic workflow is `customer-discovery`:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

This is a responsibility sequence, not a native command chain. The active agent may skip a capability when the responsibility is already satisfied by durable evidence, and must stop when a later responsibility is not warranted.

## State and continuation

PM artifacts become useful Campaign evidence only after the canonical admission boundary succeeds. A later transition may cite those exact admitted bytes. Handoff/resume behavior remains the existing Campaign responsibility; PM does not create a separate memory system.
