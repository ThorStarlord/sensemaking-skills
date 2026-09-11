# Sensemaking Skills Product Operating Model

**Status:** current operating model  
**Authority:** product strategy plus ADRs 0013/0014  
**Scope:** how value is delivered and who owns each reasoning/control boundary

This is a compact value-stream and responsibility map. The more detailed
operating guide remains [agent-native-operating-workflow.md](agent-native-operating-workflow.md).
The canonical higher-scope control model is
[strategic-outer-loop.md](strategic-outer-loop.md).
The Level-4 Persona & Adaptive Guidance Model v0 interpretation is frozen in
[persona-adaptive-guidance-design-preflight.md](persona-adaptive-guidance-design-preflight.md).

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

## Adaptive guidance and rigor

Sensemaking uses one stable doctrine while allowing the active coding agent to
adapt how much scaffolding, process rigor, and durability are warranted by the
situation. This is semantic agent judgment, not a routing algorithm.

The primary design persona is a **high-delegation agent-assisted builder /
repository owner**, beginner-first and expert-capable. The same person may have
different effective expertise in different decisions, and an expert may still
choose high delegation because they want leverage rather than instruction.

Five situational factors clarify the adaptation:

| Factor | Meaning | Primarily influences |
| --- | --- | --- |
| **User supervision capability** | The user's contextual ability to spot omissions, understand repository constraints, and evaluate agent judgment | Scaffolding and explanation |
| **Desired delegation** | How much engineering judgment the user wants the agent to exercise independently | Agent decision ownership within granted authority |
| **Decision complexity** | How difficult it is to determine the warranted repository responsibility | Sensemaking and investigation rigor |
| **Consequentiality** | Cost, irreversibility, authority sensitivity, or damage potential of a wrong responsibility/action | Caution, evidence, validation, reconciliation |
| **Continuation complexity** | How much repository-specific decision state must survive time, sessions, agents, machines, or handoffs | Campaign durability, provenance, handoff, resume |

Conceptually:

```text
user supervision capability
        -> scaffolding

desired delegation
        -> agent decision ownership within authority

decision complexity + consequentiality
        -> process rigor

continuation complexity
        -> durability / Campaign value
```

These factors are independent enough that one must not stand in for another.
For example, a technically difficult implementation may have low decision
complexity, a one-line change may be highly consequential, and a beginner-facing
task may need more guidance without needing Campaign state.

### Opinionated principles, adaptive ceremony

Sensemaking is intentionally opinionated about engineering invariants:
repository reality over stale planning, evidence before unsupported commitment,
responsibility before capability, explicit authority, bounded claims, and
correct stopping. Those principles do not become optional because a task is
small or the user is experienced.

The ceremony used to express them is adaptive. A narrow locally evidenced task
may need only direct work and tests. An ambiguous repository responsibility may
need repository sensemaking. Higher consequentiality may justify stronger
validation/reconciliation. High continuation complexity may justify Campaign
state and provenance.

```text
stable doctrine
!= mandatory full pipeline
```

### Progressive disclosure

More user guidance does not require more visible machinery. A beginner may need
the agent to proactively surface a missing dependency or authority boundary in
plain language while Campaign/provenance details remain internal unless useful.
An expert may prefer concise evidence and direct access to the mechanical
surfaces.

```text
more scaffolding
!= more visible machinery
```

No beginner/expert runtime mode, competence score, task-complexity score,
consequentiality score, or automatic Campaign threshold is authorized by this
model.

### Desired delegation is not authority

The user may want the coding agent to make many engineering decisions without
manual routing. That desired delegation does not create authority to merge,
release, deploy, publish, perform destructive external mutations, or cross any
other reserved boundary.

```text
desired delegation
!= granted authority
```

The active agent should resolve repository-answerable questions itself when
that judgment is delegated, while still escalating owner intent and reserved
actions at the appropriate boundary.

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

The adaptive guidance model changes neither this ownership table nor the
semantic/mechanical boundary. It helps the active agent decide how much
scaffolding and durable support is useful; it does not transfer judgment to
runtime machinery.

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
