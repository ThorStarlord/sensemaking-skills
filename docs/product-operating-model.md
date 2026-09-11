# Sensemaking Skills Product Operating Model

**Status:** current operating model  
**Authority:** product strategy plus ADRs 0013/0014  
**Scope:** how value is delivered and who owns each reasoning/control boundary

This is a compact value-stream and responsibility map. The more detailed
operating guide remains [agent-native-operating-workflow.md](agent-native-operating-workflow.md).
The canonical higher-scope control model is
[strategic-outer-loop.md](strategic-outer-loop.md).

## Four-level control architecture

Sensemaking distinguishes four scopes of reasoning and durable state:

```text
LEVEL 4 — PRODUCT THESIS / STRATEGY REVISION
What product should this be, for whom, and why?
                    |
                    v
LEVEL 3 — STRATEGIC REPOSITORY EVOLUTION
What should change in the product/repository next?
                    |
                    v
LEVEL 2 — RESPONSIBILITY / CAMPAIGN
What bounded responsibility resolves the selected decision?
                    |
                    v
LEVEL 1 — EXECUTION
What concrete steps correctly perform the bounded work?
```

These are not four runtime engines. The active coding agent owns semantic
judgment across the scopes permitted by its authority.

The core control law is:

> Lower levels may execute decisions delegated from higher levels, but they may
> not silently redefine commitments owned by the higher level.

Therefore Level 1 does not silently redefine the responsibility, Level 2 does
not silently redefine the Strategic Frontier, and Level 3 does not silently
rewrite the product thesis. Level 4 does not manufacture action authority.

## Core bounded value process — Levels 1 and 2

```text
Repository goal / problem
        ↓
Establish current repository state
        ↓
Identify consequential uncertainty
        ↓
Gather bounded evidence
        ↓
Determine warranted responsibility
        ↓
Check authority
        ↓
Select an appropriate capability
        ↓
Perform bounded work
        ↓
Validate mechanically
        ↓
Record durable result
        ↓
Reassess
        ↓
continue / owner decision / defer / stop
```

This is a recursive loop, not a fixed lifecycle. New evidence may warrant a
responsibility conventionally considered earlier, later, or sideways.

## Strategic Repository Evolution — Level 3

Level 3 operates above a bounded Campaign. It asks what repository-level change
is warranted next given the product mission and current capability state.

```text
product mission / current strategy
        ↓
current product + repository capability state
        ↓
material gaps / contradictions / opportunities
        ↓
Strategic Frontier
        ↓
select or decline one current strategic boundary
        ↓
identify decision-changing strategic uncertainty
        ↓
select one warranted repository-level responsibility
        ↓
delegate bounded Campaign / work package
        ↓
receive qualified result + evidence
        ↓
update strategic state
        ↓
reassess mission / frontier
        ↓
continue / defer / owner decision / thesis review / stop
```

The Strategic Frontier is not a backlog. A frontier item is a decision-relevant
possibility, not automatic work or authorization.

`STATUS.md` is the current operational projection of Level-3 state. Its
conceptual contract is
[strategic-state-contract.md](strategic-state-contract.md).

## Product Thesis / Strategy Revision — Level 4

Level 4 asks whether the product thesis itself remains the right commitment.
The canonical authority surface is [product-strategy.md](product-strategy.md).

It reasons over slower-changing commitments such as product purpose, primary
user, problem, JTBD, value proposition, product boundary, strategic principles,
non-goals, success measures, strategic bets, and evidence ceilings.

Level 3 may detect a thesis-level contradiction, but it must escalate rather
than silently rewrite those commitments. The revision process is defined in
[product-thesis-revision.md](product-thesis-revision.md).

Typical Level-4 dispositions are:

```text
REAFFIRM
REINTERPRET
REVISE
RETIRE
SUPERSEDE
```

Major owner-reserved strategic changes require explicit owner ratification.

## Responsibility ownership

| Boundary | Owns |
| --- | --- |
| Human owner | Mission, strategic intent, major product decisions, authority grants, claim-ceiling expansion, reserved merge/release decisions |
| Active coding agent | Semantic interpretation, evidence-informed responsibility selection, strategic-frontier selection within authority, capability selection, bounded implementation reasoning, continuation/stopping |
| Skills | Specialized reasoning protocols, artifact contracts, bounded capabilities |
| Artifacts | Durable state, evidence transfer, handoff, traceability |
| Deterministic machinery | Hashes, schemas, identities, invariants, mechanical validation, tests, qualification checks |
| Runtime substrate | Agent lifecycle, tool execution, process orchestration, and persistence mechanics external to Sensemaking |

The active agent owns the recursive semantic loop. Execution/orchestration
coordinates an already-selected responsibility and must not silently replace it
with a materially different one.

## Governance loop

The governance loop is the product-change/reconciliation view of Levels 3 and 4:

```text
Observe real repository / product behavior
        ↓
Identify a consequential problem, gap, contradiction, or opportunity
        ↓
Classify evidence and evidence ceilings
        ↓
Form or revise a bounded product/repository hypothesis when needed
        ↓
Choose the smallest warranted intervention, analysis, or validation
        ↓
Execute / build / reconcile
        ↓
Adjudicate the result
        ↓
build / repair / defer / reject / remove / no change
        ↓
qualify mechanically where applicable
        ↓
update Level-3 state
        ↓
update Level-4 strategy only when warranted and authorized
```

This loop is intentionally lightweight. It does **not** require a new empirical
experiment before every construction step. Experiments are one possible source
of evidence when a decision genuinely depends on behavior that repository facts
cannot answer; they are not the default controller.

## Upward evidence and downward delegation

Information can travel upward without granting authority upward or downward.

```text
Level 4 commitment
    ↓
Level 3 repository responsibility
    ↓
Level 2 bounded Campaign responsibility
    ↓
Level 1 action

Level 1/2 result + evidence
    ↑
Level 3 capability-state reconciliation
    ↑
Level 4 thesis review only when material
```

When a lower-level result contradicts the higher-level rationale, return the
contradiction to the owning level rather than expanding scope silently.

## Authority transitions

Keep these distinct:

```text
finding         != authorization to fix
recommendation  != owner decision
implemented     != validated
validated       != reconciled
reconciled      != repair-verified
repair-verified != merged or published
```

Valid terminal outcomes include a recommendation, owner handoff, deferment,
repair verification, no repository change, thesis-review escalation, or
stopping at an authority boundary. Stopping is successful when further work is
not warranted or is not authorized.

## Support and external boundaries

The core package is local-first. The user's coding-agent harness supplies model
reasoning; local scripts and validators supply mechanical evidence. Optional
experimental GitHub integration is not a requirement of the core product.

Do not invent persistence, scheduling, worker-management, strategic planning,
or merge authority in Sensemaking when those responsibilities belong to the
runtime substrate, active agent, or human owner.

## Product-management guardrail

Every proposed feature or strategic change should connect strategy to a
consequential decision and sufficient evidence:

```text
strategic fit → decision value → evidence → smallest warranted intervention
```

If the chain is missing, the work remains a hypothesis, deferred direction, or
non-strategic backlog item rather than a current product commitment.

Repository-grounded construction may proceed without product-value
experimentation when the missing capability/integrity boundary and its
mechanical contract are already clear. When the decisive question becomes
behavioral value rather than architecture or integrity, record that boundary
honestly instead of manufacturing semantic machinery.
