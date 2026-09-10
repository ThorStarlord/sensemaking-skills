# Sensemaking Skills Product Operating Model

**Status:** current operating model  
**Authority:** product strategy plus ADRs 0013/0014  
**Scope:** how value is delivered and who owns each boundary

This is a compact value-stream and responsibility map. The more detailed
operating guide remains [agent-native-operating-workflow.md](agent-native-operating-workflow.md).

## Core value process

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

## Responsibility ownership

| Boundary | Owns |
| --- | --- |
| Human owner | Mission, strategic intent, major product decisions, authority grants, claim-ceiling expansion, reserved merge/release decisions |
| Active coding agent | Semantic interpretation, evidence-informed responsibility selection, capability selection, bounded implementation reasoning, continuation/stopping within authorized policy |
| Skills | Specialized reasoning protocols, artifact contracts, bounded capabilities |
| Artifacts | Durable state, evidence transfer, handoff, traceability |
| Deterministic machinery | Hashes, schemas, identities, invariants, mechanical validation, tests, qualification checks |
| Runtime substrate | Agent lifecycle, tool execution, process orchestration, and persistence mechanics external to Sensemaking |

The active agent owns the product-level recursive loop. Execution/orchestration
coordinates an already-selected responsibility and must not silently replace it
with a materially different one.

## Governance loop

```text
Observe real repository behavior
        ↓
Identify a consequential problem
        ↓
Classify evidence
        ↓
Form a product hypothesis
        ↓
Design the smallest intervention or experiment
        ↓
Execute / dogfood
        ↓
Adjudicate the result
        ↓
build / repair / defer / reject / remove / no change
        ↓
qualify
        ↓
update durable strategy when warranted
```

This loop is intentionally lightweight. A new mechanism needs a concrete
failure boundary and evidence that the smallest intervention does not suffice.

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
repair verification, no repository change, or stopping at an authority
boundary. Stopping is successful when further work is not warranted or is not
authorized.

## Support and external boundaries

The core package is local-first. The user's coding-agent harness supplies model
reasoning; local scripts and validators supply mechanical evidence. Optional
experimental GitHub integration is not a requirement of the core product.

Do not invent persistence, scheduling, worker-management, or merge authority in
Sensemaking when those responsibilities belong to the runtime substrate or the
human owner.

## Product-management guardrail

Every proposed feature must connect strategy to a decision and an experiment:

```text
strategic fit → decision value → observed evidence → smallest test
```

If the chain is missing, the work is a hypothesis to investigate or defer, not
a current product commitment.

