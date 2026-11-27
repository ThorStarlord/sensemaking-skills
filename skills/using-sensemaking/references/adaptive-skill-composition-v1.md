# Adaptive Skill Composition (v1)

**Purpose:** How the active agent applying `using-sensemaking` composes
specialized reasoning: who owns each activity, when it is warranted, how
results feed back, and what a specialist returns. This reference belongs to the
distributed `using-sensemaking` Skill. It is guidance for one semantic
controller, not a router, pipeline, planner or new artifact.

**Load when:** choosing, sequencing or interpreting specialist reasoning, or a
specialist has just returned.
**Skip when:** the next action is a single obvious step.

## 1. Activity owners

| Activity | Owner (procedure) | Durable product |
| --- | --- | --- |
| Semantic foundation, recall, audit, reconciliation | `repository-semantic-steward` (BOOTSTRAP, RECALL, AUDIT, RECONCILE) | `.sensemaking/knowledge/*.json`, query receipts |
| Relational verification of an absence, dependency, relation or runtime-behavior claim | `repository-semantic-steward` (RELATE) | `RELATIONAL_VERDICT` in the report or receipt finding; reconciled knowledge when warranted |
| Repository orientation when boundaries or ownership are unclear | `repo-sensemaker` | `repository_sensemaking_brief` |
| Divergent and convergent possibility exploration | `strategic-repository-analysis` (Strategic Exploration Funnel) | report; `poss:` records when retained |
| Architectural synthesis and consequence depth | `repository-semantic-steward` (architecture exploration) | `architectural_synthesis`; `arch:` and consequence records when retained |
| Strategic construction-path synthesis and comparative selection | `strategic-repository-analysis` (construction-path synthesis) | `strategic_repository_analysis` |
| Adversarial challenge of a provisional direction | `architectural-review`; `pre-mortem` only when the PM domain pack is installed (if absent, state that the second lens was not applied) | review report |
| Reconsideration after strategic evidence | `strategic-repository-reconciliation`; Steward RECONCILE for knowledge | reconciliation; record history |
| Owner-reserved choice | `owner-decision-capsule` | decision capsule |
| Cross-session continuation of a reasoning mission | `strategic-sensemaking-loop` | session receipts |
| Authorized realization of a selected direction | portable construction loop (`portable-construction-loop-v1.md`) | code change, PR, implementation receipt |

The table names owners, not an order. Skills stay directly invokable by
maintainers; ordinary users need only `using-sensemaking`.

## 2. When each activity is warranted

| Activity | Warranted when |
| --- | --- |
| Semantic foundation | No adequate current model exists for the goal's scope (`ontology-first-entry-v1.md`) |
| Divergent exploration | Possibility coverage is inadequate, or the future is materially open |
| Convergent exploration | The landscape is sufficient and candidates need qualification |
| Architectural synthesis | Alternative structures would materially change a future's value or feasibility |
| Construction-path synthesis | A coherent trajectory toward a future capability needs developing |
| Convergent evaluation | Material alternatives are developed enough to compare |
| Consequence depth | A provisional preference may cause downstream effects that change the choice |
| Adversarial challenge | Important assumptions, commitments or consequences need scrutiny |
| Reconsideration | New evidence changes the premises behind an earlier preference |
| Relational verification | A recommendation or owner escalation rests on an absence, or on a relation the reviewed graph does not settle |

Skip an activity whose result could not change the decision. Skipping is a
judgment to state when it is consequential, not a failure.

## 3. Feedback moves

The controller may move:

- from divergent exploration into ontology enrichment, when exploration
  exposes an unmodelled system or distinction;
- from convergence back to divergence, when an important possibility is missing;
- from consequence depth back to architectural synthesis, when a consequence
  defeats or reshapes the preferred option;
- from architectural synthesis into construction-path comparison;
- from evaluation into further evidence gathering;
- from a justified preference into durable knowledge retention;
- from a recommendation or escalation back into relational verification, when
  it rests on a graph miss, an unexercised declaration or an unrecorded
  relation. The verdict then returns to the controller before the choice is
  finalized.

Each move is a fresh controller choice, made because the returned evidence
warrants it.

```text
specialist result      != controller decision
preferred architecture != selected strategic direction
selected direction     != implementation authorization
suggested continuation != next responsibility
```

## 4. Invoking a specialist

1. Identify the warranted specialist responsibility.
2. Resolve the actual installed or repository-local Skill instructions.
3. Invoke that Skill by name through the host's Skill mechanism (for example
   the Skill tool with `repository-semantic-steward`). This loads its
   `SKILL.md`, which carries its contract: how to validate, which CLI to pin,
   which template an artifact follows. Then read the references it points to.
4. Supply the available source context and relevant artifact references.
5. Receive and interpret its result.
6. Validate consequential artifacts when a validator applies. Give an output a
   specialist's artifact identity (for example `strategic_repository_analysis`)
   only when it follows that specialist's template and passes its validator;
   otherwise present it as a report.
7. Choose the next warranted reasoning activity.

When the host cannot invoke a Skill natively, read the specialist's `SKILL.md`
first and then its references, in the same session; this is an acceptable
fallback. Reading only a deep reference (such as `bootstrap.md`) skips the
specialist's contract and is not. Installed Skills are not a host-independent executable
call graph; do not claim one.

## 5. Return convention

A specialist returns control without deciding the next specialist. Its return,
expressed through its existing artifact and task report rather than a new
master artifact, states:

- the responsibility it completed (or why it stopped);
- the actual source revision and artifact references;
- consequential findings;
- remaining uncertainties and contradictions;
- a suggested continuation, as evidence for the controller;
- the limits of its claim and of the authority it used.

The controller reads the return, decides what changed, and reconciles before
continuing.

## 5a. Cognitive integration: preserve the decision-relevant effect

When composing consequential intellectual work, distinguish availability and
connectivity from actual influence. A result is integrated when its supported
contribution is interpreted against the governing question and changes a
material premise, possibility, comparison, method, action, or justified
reaffirmation. Calling several Skills or producing compatible artifacts does
not establish better judgment.

Consider the relevant kind of influence, not a required sequence:

- **Enabling:** understanding exposes constraints, affordances or an
  unrepresented distinction that makes exploration or evaluation useful.
- **Corrective:** challenge or verification defeats an assumption or
  unsupported conclusion; reopen the affected question rather than defend
  the old result.
- **Transformative:** a new route, affordable reversible probe or revised
  objective changes what deserves commitment.
- **Generative:** recombine grounded relationships, capabilities and future
  states to discover a genuinely different possibility. Check enabling
  conditions, contrary evidence and downstream costs; novelty is not value.

Carry forward the governing intent, actual decision/question, exact source
identity and authority, affected claims and their epistemic limits, relevant
alternatives, live assumptions, counterevidence, and reconsideration
conditions. Preserve only what the next decision or later consumer needs
through existing evidence, knowledge, decision and receipt surfaces. Do not
preserve private reasoning traces or build a second knowledge store.
When using several projections, pin their source revisions; a shared
snapshot is not proof of current applicability or semantic compatibility.

When results seem incompatible, first distinguish factual contradictions
from different premises, objectives, time horizons, contemplated
commitments or tradeoffs. Resolve genuine contradictions using source
evidence. A valid risk finding and a valuable opportunity can both hold:
compare a reversible build, staged inquiry, another design, deferral or no
change before committing. No synthesis may silently waive an invariant,
qualification requirement or authority boundary.

For decisions that turn on both future possibilities and intellectual
approach, use [developmental trajectory reasoning](developmental-trajectory-reasoning-v1.md)
and the existing [method precedent and trial guidance](method-trial-v1.md)
when warranted. The CLI supports `workspace-query --operation product-outline`
or `--operation possibility-ecology` with `--method-question QUESTION`;
add `--include-method-trials` when earlier trial decisions and observations
could inform the present composition. Question-led discovery is lexical,
not applicability. A trial without a prior lesson link can be recovered;
a trial is not a promoted lesson. Inspect actual conditions and results.
Do not assume a prior method or composition applies just because it matches.

## 5b. Develop the composition itself when actual experience warrants it

The active agent can adapt how it combines existing methods rather than
only improving their individual outputs. For example, insufficient option
coverage may warrant backcasting from a desired capability state before
divergence and comparison. A conflict between consequence depth and
architecture may warrant a reversible feasibility probe before selection.
These are possibilities, not prescriptions.

If a consequential real episode exposes an integration barrier, identify
whether it concerns method quality, activation, context delivery, semantic
compatibility, interpretation, selection influence, cross-session retention,
or unnecessary cost. Compare alternative explanations and source evidence;
do not infer an intrinsic agent trait or diagnose failure from absent traces.
Use SCL and Method Adaptation for a conditional procedural change only when
the actual method before/after, scope, evidence, outcome and limitations
support it. Optional method trials can preserve an attributable predecision
commitment; later observation remains separate from effect or causality.

Use the least costly composition that preserves a strong warranted decision,
not the least ambitious product responsibility. Account for the value of
discovered options, avoided rework, information, omitted opportunities,
retained complexity and future context burden. Direct work, a brief source
check, a focused specialist, a parallel independent review, or a richer
composition can each be preferable. Return to direct action when further
cooperation would not materially change the decision. There is no mandatory
integration artifact, stage, score, controller or qualification gate.

## 6. Anti-patterns

- A fixed pipeline that runs every activity for every request.
- Numeric scores or a selector that picks the next Skill.
- A specialist that hands work directly to another specialist.
- Treating a strategic selection as a request to implement.
- Treating a graph miss, `NOT_ASSESSED` or an unexercised declaration as
  product absence, or escalating such a gap to the owner without relational
  verification.
- Recording a relation or runtime behavior stronger than its governing and
  implementing sources show, for example a constraint on an implementation that
  the governing source constrains only as a support claim.
- A second controller: continuation procedures resume and preserve reasoning;
  they do not redefine responsibility selection.

## 7. Optional decision observability

When the user requests maximum decision transparency, apply
`decision-observability-v1.md` at consequential selection and return boundaries.
Record the rationale before acting, separate actual host events from self-report,
and classify skips, failures and undocumented omissions accurately. This does
not change the activity owners, introduce a fixed sequence or require an audit
in ordinary use.
