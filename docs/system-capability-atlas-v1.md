# System Capability Atlas v1

**Status:** descriptive product/documentation map  
**Authority:** subordinate to `docs/product-strategy.md`, ADR 0029, the Four-Level Control Model, Policy Hierarchy v0, and the canonical Skill/runtime contracts  
**Runtime effect:** none; this document introduces no router, planner, schema, state machine, or authority

## 1. Purpose

Sensemaking Skills now contains several layers that solve different problems:
strategic reasoning, bounded responsibility selection, optional durable state,
execution interfaces, evidence return, reconciliation, semantic representation,
and deterministic validation.

This atlas answers a narrower product question:

> **What major systems exist, what question does each own, and which systems
> should an ordinary user normally see?**

It is an observability and orientation surface. It does not redefine the
systems it summarizes.

## 2. Product-facing compression

The ordinary product experience should expose the smallest useful surface:

```text
human first use
-> GETTING_STARTED.md

coding-agent control discipline
-> using-sensemaking

one-prompt strategic start / resume
-> strategic-sensemaking-loop

specialized analysis or packet explicitly needed
-> invoke that specialized Skill directly

durable continuation complexity warrants persistence
-> Campaign

maintenance / qualification
-> operations-runbook + deterministic tooling
```

The existence of a deeper subsystem does not imply that the owner must invoke
or understand it directly.

```text
one front door
!= one semantic responsibility

progressive disclosure
!= hidden authority

internal substrate
!= deprecated surface
```

## 3. Major system map

| System | Primary question owned | Control scope | Primary surface | Typical visibility |
| --- | --- | --- | --- | --- |
| Product Thesis / Strategy Revision | What should the product be, for whom, and why? | Level 4 | `docs/product-strategy.md`, thesis-review contract | Reserved / advanced |
| Strategic Repository Sensemaking | What should change in the repository/product next, if anything? | Level 3 | `strategic-repository-analysis` | Specialized; often reached through strategic loop |
| Strategic Exploration Funnel | Have we covered the repository broadly enough before converging? | Level 3 | system map -> breadth -> candidates -> depth -> paths | Internal reasoning made owner-visible through summary |
| Strategic Frontier | Which materially real repository futures remain decision-relevant? | Level 3 | strategic analysis artifact | Specialized concept |
| Goal Fitness & Frontier Integrity | Are we optimizing a terminal outcome or merely a milestone/proxy? | Level 3 | strategic analysis guidance | Internal guardrail |
| Strategic Hypothesis Admission | May a grounded unbuilt future enter the strategic option set? | Level 3 | strategic analysis guidance | Internal guardrail |
| Strategic Continuity | Is authored strategy mechanically current/reconstructible? | Level 3 support | `strategy inspect|compare|drift|history|graph` | Advanced / diagnostic |
| Strategic Reconciliation | What changes after consequential evidence returns? | Level 3 | `strategic-repository-reconciliation` | Specialized; loop-managed by default |
| Owner Decision | Is the decisive premise genuinely owner-reserved? | Reserved boundary | `owner-decision-capsule` | Specialized / owner-facing |
| Thesis Review | Does evidence challenge a Level-4 commitment? | Level 4 boundary | `thesis-review-packet` | Reserved / owner-facing |
| Using Sensemaking | What bounded responsibility is warranted next? | Primarily Level 2, cross-cutting | `using-sensemaking` | Primary agent-facing |
| Policy Hierarchy | Which reasoning question is decision-relevant now? | Cross-cutting semantic control | Inquiry, Metareasoning, Exploration, Warrant/Choice, Learning/Reconciliation guidance | Internal by default |
| Campaign | What decision state must survive contexts/agents/machines? | Durable Level 2 | `campaign` CLI/state | Conditional; only when continuation warrants |
| Execution Interface | How is already-selected work handed to an executor and evidence returned? | Level 1 support | handoff/result companions, external projections | Internal/integration |
| Handoff | Does a registered Skill transition need durable/copyable context? | Responsibility boundary | `handoff` | Conditional internal |
| Capability & Organization Tracer | Would read-only role/capability topology improve coordination legibility? | Execution support | `organization inspect|role|skill-profile` | Advanced / optional |
| Decision Journey | How did authored strategy, execution, evidence, and reconciliation compose? | Read-only cross-level projection | `journey` family | Advanced / observability |
| Change-Impact Sensemaking | What consequential surfaces does a bounded change affect? | Specialized semantic analysis | `change-impact-analysis` | Specialized |
| Multi-Repository Strategic Sensemaking | How should capabilities/boundaries be understood across an explicit repository set? | Level 3 | `multi-repository-strategic-analysis` | Specialized |
| Repo Sensemaker | What repository uncertainty/fog/weak boundary is materially present? | Diagnostic support | `repo-sensemaker` | Specialized diagnostic |
| Semantic Architecture | How are evidence, semantic profiles, capabilities, references, and conformance represented? | Orthogonal substrate | semantic architecture docs/runtime | Substrate |
| Validator Ecosystem | Is an artifact/repository representation mechanically valid? | Deterministic assurance | validators, fixtures, release checks | Substrate / maintainer |
| Release / Qualification | Which exact bytes satisfy the declared mechanical release contract? | Assurance / release | release manifests, audit, workflows | Maintainer/operator |
| Compatibility Workflow Runtime | Can historical prompt/workflow integrations continue to function? | Compatibility | runner/workflow registries | Compatibility-only |

## 4. Product-role classification

This classification is **orthogonal** to the release manifest's
`supported/internal/experimental` classification.

### 4.1 Front-door surfaces

Use these when the user should not need to understand subsystem choreography.

- `GETTING_STARTED.md` — human first-use entry point.
- `using-sensemaking` — coding-agent operating discipline.
- `strategic-sensemaking-loop` — one-prompt strategic start/resume.

### 4.2 Specialized direct surfaces

Invoke these when their bounded responsibility is explicitly the task:

- `repo-sensemaker`;
- `strategic-repository-analysis`;
- `strategic-repository-reconciliation`;
- `owner-decision-capsule`;
- `thesis-review-packet`;
- `external-evidence-packet`;
- `multi-repository-strategic-analysis`;
- `change-impact-analysis`;
- `architectural-review`;
- `output-reconciler`;
- `repair-verifier`.

These remain first-class capabilities even when a front door normally invokes
or recommends them.

### 4.3 Internal substrate / composition surfaces

Ordinary users should not need to sequence these manually:

- Policy Hierarchy contracts;
- Strategic Exploration Funnel internals;
- Strategic Continuity projections;
- Campaign provenance/identity/reference machinery;
- Execution handoff/result interchange;
- Decision Journey projections;
- Capability & Organization Tracer;
- validator/runtime conformance machinery;
- semantic architecture substrate;
- `handoff` when a Skill-to-Skill transition is actually useful.

### 4.4 Compatibility / historical surfaces

These exist to preserve earlier integrations or repository history and should
not be mistaken for current semantic-control authority:

- compatibility workflow runtime and legacy registries;
- deprecated Skill invocations retained in registries;
- historical research/experiment packages;
- superseded ADR/product-boundary material retained as provenance.

## 5. System relationships

```text
PRODUCT THESIS (L4)
        |
        v
STRATEGIC REPOSITORY SENSEMAKING (L3)
  system map -> breadth -> frontier -> depth -> paths
        |
        v
USING-SENSEMAKING / WARRANTED RESPONSIBILITY (L2)
        |
        +---- optional CAMPAIGN durability
        |
        v
EXECUTION (L1)
        |
        v
EVIDENCE + MECHANICAL VALIDATION
        |
        v
LEARNING / RECONCILIATION
        |
        +---- continue bounded responsibility
        +---- revise/reopen Level 3
        +---- owner decision
        +---- thesis review
        +---- stop

STRATEGIC-SENSEMAKING-LOOP
= product-facing composition over the existing boundaries
!= new source of truth
```

## 6. Common non-equivalences

```text
capability available != responsibility warranted
responsibility warranted != action authorized
validator PASS != semantic truth
repository drift != strategy invalid
returned evidence != automatic model change
milestone != terminal outcome
frontier candidate != construction path
strategic path selected != implementation authorized
large task != Campaign required
organization visible != organization runtime warranted
front-door orchestration != monolithic planner
```

## 7. Maintenance rule

Update this atlas only when a **material system boundary or product-facing role**
changes. Do not turn it into a complete file inventory, duplicate the Skill
registry, or add every helper command.

The authoritative contracts remain the linked canonical documents and Skills.
