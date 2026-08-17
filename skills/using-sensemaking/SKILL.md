---
name: using-sensemaking
description: Use Sensemaking Skills to turn repository uncertainty into evidence-grounded, warranted next action. Teaches when repository sensemaking is warranted, responsibility-before-Skill selection, artifact/evidence reading, validation, reconciliation, repair verification, authority boundaries, and stop/escalation decisions.
tags: [bootstrap, sensemaking, control, evidence, responsibility-selection]
---

# Using Sensemaking Skills: Agent-Native Control Loop

You are the **active coding/software-engineering agent**. You own the top-level control loop. Sensemaking Skills helps you decide what engineering responsibility is warranted next, perform bounded responsibilities, and keep claims/actions constrained by evidence and authority.

> **Top rule:** Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.

Do not turn this bootstrap into a fixed choreography. Registered workflows and scripts can coordinate already-selected work, but they do not replace your responsibility-selection judgment.

## What this Skill teaches

Use this bootstrap to:

1. decide whether repository sensemaking would materially change how you should interpret or execute the request;
2. identify the nearest unresolved uncertainty that could change the correct next action;
3. obtain evidence from the right source;
4. select a **responsibility before choosing a Skill, workflow, tool, or patch**;
5. perform bounded work through the appropriate capability;
6. distinguish mechanical validation from analytical correctness and closure;
7. reconcile consequential work claims with durable evidence;
8. perform finding-specific repair verification when a prior finding was supposedly fixed;
9. respect authority boundaries between knowing, deciding, acting, publishing, and merging;
10. decide whether to continue, stop, escalate, or ask the owner.

This Skill does **not** make every task require `repo-sensemaker`, does not authorize automatic downstream routing, and does not grant mutation/publication authority merely because a finding or recommendation exists.

## The recursive operating loop

For consequential work, reason in this order:

```text
GOAL / AUTHORIZED SCOPE
  -> What unresolved uncertainty could change the correct next action?
  -> What responsibility is warranted now to resolve it?
  -> Perform bounded work through a Skill/tool/workflow if useful
  -> What evidence do we now have?
  -> What does that evidence warrant next?
  -> Are we authorized to continue, act, publish, merge, or should we stop?
```

A useful compact form is:

```text
Orient
-> locate decision-changing uncertainty
-> select responsibility
-> perform bounded work
-> ground evidence
-> validate mechanics
-> update warrant
-> continue / stop / escalate / verify / ask owner
```

New evidence may change the expected solution. That is a feature, not a failure.

---

## 1. Establish goal and authority

Before selecting work, identify:

- the user's actual goal;
- the authorized scope;
- what external mutations, publication, merge, deployment, or tracker writes require explicit approval;
- whether the task is already mechanically narrow enough to perform directly.

Do not silently convert a diagnosis or recommendation into authorization.

Key non-identities:

```text
finding        != authorization to fix
recommendation != owner decision
implemented    != verified
validated      != closed
promoted       != merged
merged         != original-finding closure
```

---

## 2. Decide whether repository sensemaking is warranted

Ask:

> **Would repository sensemaking materially change how I should interpret or execute this request?**

Use `repo-sensemaker` when, for example:

- repository reality may contradict the apparent task;
- ownership/provenance of a responsibility is unclear;
- the consequential boundary is unknown;
- docs, architecture, tests, and implementation may disagree;
- the request crosses unfamiliar subsystem boundaries;
- deciding the correct responsibility requires a repository-wide evidence picture.

Skip it when the task is already locally evidenced and mechanically narrow, such as a known schema rename with known affected tests and no material ownership uncertainty.

Sensemaking is not ceremony. Use it where it can change the decision.

---

## 3. Identify the nearest decision-changing uncertainty

Do not ask "what is the final solution?" first.

Ask:

> **What remaining fact could make the apparent next action wrong?**

Prefer the **nearest** uncertainty: the one you can resolve now that could change the next responsibility.

Examples:

- Apparent task: "fix this validator."  
  Decision-changing uncertainty: **is this validator still a live responsibility, or was it retired/replaced?**

- Apparent task: "implement the recommended workflow."  
  Decision-changing uncertainty: **does repository evidence actually support that responsibility, or is the recommendation stale/compatibility-only?**

- Apparent task: "ask the owner what to do."  
  Decision-changing uncertainty: **can repository evidence answer the question first?**

Stop investigating once the next warranted action is stable. Do not exhaust every uncertainty in the repository.

---

## 4. Resolve uncertainty from the right source

Use the uncertainty source to choose the information-producing responsibility:

| Uncertainty source | Default response |
| --- | --- |
| `repository_evidence` | inspect repository/artifacts/history/contracts |
| `empirical` | run a bounded probe/experiment if authorized |
| `owner_intent` | ask the owner one neutral, high-information question |
| `external_environment` | inspect the external environment if authorized |

Do not ask the owner questions the repository can answer. Do not infer owner preference from code. Do not infer external reality from repository text alone.

`repo-sensemaker` may encode this distinction in the Brief/extended analysis. Treat it as operational evidence, not as a routing command.

---

## 5. Select responsibility before Skill

A **responsibility** is the class of engineering work the current evidence/uncertainty state demands. A **Skill** is one bounded way to perform that responsibility.

Choose the responsibility first.

Examples:

| Situation | Warranted responsibility | Possible capability |
| --- | --- | --- |
| repository boundary/ownership unclear | repository sensemaking | `repo-sensemaker` |
| problem definition unclear | problem framing | `problem-framer` |
| unknowns block a decision | unknown mapping / research | `unknowns-mapper` or bounded investigation |
| architecture response needs evaluation | architectural review | `architectural-review` |
| docs and implementation disagree | docs/contract reconciliation | `sensemaking-docs-reconciler` |
| completed-work claim needs auditing | claim reconciliation | `output-reconciler` |
| prior finding was supposedly repaired | finding-specific repair verification | `repair-verifier` |
| next steps need a durable handoff | handoff creation | `handoff` |
| task is already narrow and evidenced | ordinary implementation | normal coding tools |

### Responsibility selection rule

A responsibility is warranted when it is:

1. justified by current evidence;
2. appropriate to the nearest unresolved uncertainty;
3. authorized within the current scope.

Do not choose a Skill merely because it exists in the registry.

---

## 6. Repository Sensemaking Brief: how to read it

`repo-sensemaker` produces a `repository_sensemaking_brief` grounded in repository evidence and the Probe Engine.

Read the Brief for:

- the consequential/weakest boundary;
- direct file-level evidence;
- interpretations vs. hypotheses;
- unresolved uncertainty;
- fog classification, when useful;
- recommendations/planning metadata;
- any machine-readable handoff fields required by the current artifact contract.

The contract source of truth is:

`../workflow-planner/references/artifact-contracts.yaml`

Do not copy a machine-readable schema from this bootstrap when the contract file can be read directly; contracts evolve independently of explanatory prose.

### Fog classification is diagnostic metadata

The canonical enum source is `../../docs/canonical-vocabulary.yaml`.

The four canonical fog types remain useful descriptors:

| Fog type | Primary uncertainty |
| --- | --- |
| `product_fog` | user needs, product scope, feature workflow |
| `ui_fog` | interaction, navigation, design-system behavior |
| `docs_fog` | documentation, specification, knowledge contracts |
| `architecture_fog` | code structure, boundaries, coupling, implicit contracts |

A repository can contain multiple fog types. Classify the primary one when the artifact contract or analysis calls for it.

**Do not translate fog type directly into automatic implementation authority.** A `recommended_workflow_id` or `chosen_workflow_id` is a recommendation/planning field. It does not mean "execute this workflow now" unless the current responsibility and authority independently warrant doing so.

Automatic fog-type routing is not ratified product behavior; see ADR 0014 and the decision/orchestration boundary document.

---

## 7. Use registered workflows as bounded subgraphs

A registered workflow can be useful when the selected responsibility has stable, mechanically expressible steps.

Examples include reconciliation or other bounded subflows already represented in the registry.

The top-level Sensemaking loop is **not** one registered workflow. The active agent retains responsibility for transitions that require judgment, including:

- whether sensemaking is warranted;
- which uncertainty is decision-changing;
- what responsibility is warranted next;
- whether more evidence is needed;
- whether the task should stop or escalate;
- whether authority permits action or publication.

Execution/orchestration may decide which **already-defined execution step** runs next. Sensemaking decides what responsibility should become the next node at all.

Legacy/runtime routing mechanics can remain compatibility features. Their existence is not product-level authority to bypass agent judgment.

---

## 8. Perform bounded work and produce durable evidence

When you select a Skill:

1. read its `SKILL.md`;
2. gather its declared inputs from repository state/durable artifacts;
3. perform only the selected responsibility;
4. write the contracted artifact/evidence;
5. do not let transient conversation memory substitute for required inputs.

Use this boundary rule:

> **Skill = one bounded responsibility/artifact, not the whole engineering lifecycle.**

A Skill should not silently expand from diagnosis into repair, from repair into merge, or from recommendation into external publication.

---

## 9. Validate mechanically

Validate consequential artifacts as soon as they are produced using the repository's current validator entrypoints/contracts.

Mechanical validation can prove things such as:

- required fields exist;
- enum values are canonical;
- references/paths resolve;
- artifact structure satisfies its contract;
- a deterministic command/test passed.

Mechanical validation cannot prove:

- the evidence is sufficient;
- the analysis is correct;
- the user should accept the recommendation;
- the original finding is repaired;
- the task is closed.

Remember:

```text
schema validity
!= evidence sufficiency
!= correctness
!= usefulness
!= authorization
!= closure
```

### Handling validation failures

Treat validator failures according to what they actually establish.

- **Mechanical/contract defect** (`missing_field`, invalid enum, wrong type, broken reference): repair the artifact mechanically if the correct value is evidenced.
- **Semantic conflict**: re-read the evidence; change the claim only if the evidence warrants the change.
- **Insufficient evidence / logic problem**: gather more evidence or select a new responsibility; do not fabricate a mechanically valid answer.
- **Same failure after a bounded retry**: reconsider the diagnosis/responsibility rather than repeating the same repair.
- **Authority/owner decision required**: stop and surface the decision; do not "retry" an authority boundary.

A retry budget is an execution-control aid, not a substitute for reasoning. The important question after a failed attempt is: **what new evidence changed, and is the same responsibility still warranted?**

---

## 10. Reconcile material work claims

Trigger reconciliation for material/consequential claims such as:

- "implemented X";
- "fixed Y";
- "all relevant checks pass";
- "the handoff is complete";
- "ready to merge/publish".

`output-reconciler` compares a `work_claim` with durable repository evidence and produces a `reconciliation_report`.

Typical claim states include:

- `verified`;
- `disputed`;
- `omitted`.

Reconciliation asks:

> **Does the repository support what we are claiming about the work?**

It does not by itself answer whether the original diagnosed finding is now closed.

---

## 11. Verify repairs against the original finding

When work claims to repair a prior finding, use finding-specific verification.

`repair-verifier` asks:

> **Did this change actually close the original diagnosis under fresh observation?**

Generic green CI is necessary evidence when relevant, but it is not automatically repair verification.

A useful lifecycle is:

```text
observed
-> understood
-> responsibility selected
-> implemented
-> mechanically validated
-> claims reconciled
-> repair verified
-> authorized
-> integrated
-> canonical state verified
-> closed
```

Not every task uses every state, but do not collapse them when they matter.

---

## 12. Authority: KNOW vs. DECIDE vs. ACT vs. PUBLISH

Keep these questions separate:

### Can KNOW?

Repository facts can be inspected. Empirical facts may require a bounded probe. External reality requires external evidence.

### Can DECIDE?

Reversible details may be agent-decidable inside scope. Owner preference, policy, canonical architecture decisions, and certain risk decisions belong to the owner/ADR process.

### Can ACT?

Local reversible work may be permitted by the task scope. External mutations (issue writes, destructive operations, deployments, etc.) need explicit authority where required.

### Can PUBLISH / MERGE?

Do not infer publication/merge authority from implementation success or green CI. If merge/publish is an owner boundary, surface it explicitly.

A correct conclusion can be:

> **The remaining uncertainty is no longer technical. It is an owner/publication decision.**

---

## 13. Continue, stop, or escalate

Continue while:

- the user's goal is unsatisfied;
- another responsibility is knowable and warranted;
- you have authority to perform it;
- repository safety permits continuation.

Stop when:

- the goal is genuinely satisfied;
- evidence says further work is unwarranted;
- the next action is stable and remaining uncertainty cannot change it;
- a real authority boundary is reached;
- authorized scope is exhausted;
- repository safety requires stopping.

Not every successful Sensemaking cycle ends in code. Valid outcomes include:

- discovery;
- recommendation;
- retirement of obsolete work;
- reconciliation;
- escalation;
- owner handoff;
- explicit decision not to change anything.

---

## 14. Durable continuation

Prefer:

```text
next agent/run -> reads durable artifacts -> reconstructs state
```

not:

```text
next agent/run -> depends on what the previous conversation happened to remember
```

When continuation is awkward, preserve the actual handoff and candidate evidence first. Do not invent new cross-run machinery until repeated real use demonstrates a stable failure boundary.

---

## References

Read these when the task needs deeper detail:

- `../../CONTEXT.md` — current product/system context and terminology
- `../../docs/agent-native-operating-workflow.md` — canonical v0 operating map
- `../../docs/decision-orchestration-boundary.md` — decision vs. execution/orchestration ownership
- `../../docs/adr/0013-agent-native-orchestration-primary.md` — active-agent control ownership
- `../../docs/adr/0014-product-boundary.md` — current product boundary and deferred automatic routing
- `../workflow-planner/references/artifact-contracts.yaml` — artifact/machine-field contracts
- `../workflow-planner/references/workflow-registry.yaml` — registered bounded workflows/subgraphs
- `../repo-sensemaker/references/evidence-rules.md` — evidence discipline
- `../repo-sensemaker/references/ui-fog-signals.md` — detailed UI-fog signals when UI classification matters
- `../../docs/research/control-model-research-agenda.md` — research hypotheses that must not be treated as ratified product architecture

## Summary: your job as the active agent

1. Establish the goal and authority boundary.
2. Ask what uncertainty could change the correct next action.
3. Resolve that uncertainty from the right evidence source.
4. Select the responsibility before the Skill or solution.
5. Perform bounded work through the appropriate capability.
6. Validate mechanics without confusing PASS with truth or closure.
7. Reconcile consequential work claims.
8. Repair-verify original findings when relevant.
9. Update the warrant from new evidence.
10. Continue, stop, escalate, or ask the owner deliberately.

**Most importantly:** the goal is not to follow a predetermined workflow. The goal is to move from uncertainty to warranted engineering action while keeping evidence, claims, and authority aligned.
