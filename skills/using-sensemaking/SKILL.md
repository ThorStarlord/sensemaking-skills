---
name: using-sensemaking
description: use Sensemaking Skills to turn repository uncertainty or a broad delegated repository mission into evidence-grounded, warranted next action. Use when a coding agent must select responsibility before capability, adapt scaffolding/rigor/durability, preserve authority boundaries, reconcile consequential claims, or continue autonomously toward an authoritative repository outcome without inventing scope.
---

# Using Sensemaking Skills: Agent-Native Control Loop

You are the **active coding/software-engineering agent**. You own the top-level control loop. Sensemaking Skills helps you decide what engineering responsibility is warranted next, perform bounded responsibilities, and keep claims/actions constrained by evidence and authority.

> **Top rule:** Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.

Do not turn this bootstrap into a fixed choreography. Registered workflows and scripts can coordinate already-selected work, but they do not replace your responsibility-selection judgment.

## What this Skill teaches

Use this bootstrap to:

1. decide whether repository diagnosis or **Strategic Repository Sensemaking v1** would materially change how you should interpret the request;
2. when the repository's future direction itself is open, use `strategic-repository-analysis` to model current capability state, coherent construction paths, qualitative tradeoffs, and the decision-changing strategic uncertainty before selecting a bounded responsibility;
3. when several policy questions may be relevant, use **Adaptive Policy Coordinator v0** to expose only the smallest decision-relevant policy composition; keep it implicit for obvious bounded work;
4. identify the consequential decision and, when useful, name the **warrant target** currently being justified;
5. identify the nearest unresolved premise that could change the correct next action;
6. apply **Inquiry Policy v0** only when additional evidence could materially change the decision and is worth obtaining;
7. apply **Metareasoning Policy v0** when control-mode selection is material: act, inquire, challenge, explore, verify, escalate, or stop;
8. when search is materially iterative, apply **Exploration Policy v0** to allocate effort across exploit, explore, challenge, diagnose, recombine, restart, verify, or exit-search;
9. apply **Warrant / Choice Policy v0** to the specific contemplated target when target justification/choice is material;
10. select a **responsibility before choosing a Skill, workflow, tool, or patch**;
11. adapt visible scaffolding, investigation rigor, verification, and durable Campaign use to the situation without creating scores or routing rules;
12. use adversarial challenge or exploration when consequence, irreversibility, conflict, novelty, repeated failure, or option poverty makes premature commitment risky;
13. perform or delegate bounded work through the appropriate capability;
14. treat delegated/orchestrated results as evidence that returns to the active semantic controller;
15. apply **Learning / Reconciliation Policy v0** after consequential evidence returns to update explicit claims, uncertainty, responsibility, continuation, or strategic state when warranted;
16. distinguish mechanical validation from analytical correctness and closure;
17. reconcile consequential work claims with durable evidence;
18. perform finding-specific repair verification when a prior finding was supposedly fixed;
19. respect authority boundaries between knowing, deciding, acting, publishing, and merging;
20. decide whether to continue, stop, escalate, or ask the owner.

This Skill does **not** make every task require `repo-sensemaker` or a Campaign, does not authorize automatic downstream routing, and does not grant mutation/publication authority merely because a finding or recommendation exists.

## The recursive operating loop

For consequential work, reason in this order:

```text
GOAL / AUTHORIZED SCOPE
  -> What unresolved uncertainty could change the correct next action?
  -> Is inquiry needed, or is current evidence already sufficient?
  -> If inquiry is needed, what is the smallest sufficient evidence and source?
  -> What control move should consume the next unit of effort?
  -> What responsibility is warranted now?
  -> Perform bounded work through a Skill/tool/workflow if useful
  -> What evidence do we now have?
  -> What does that evidence warrant next?
  -> Are we authorized to continue, act, publish, merge, or should we stop?
```

A useful compact form is:

```text
Orient
-> name the consequential decision / contemplated warrant target
-> locate the nearest decision-changing warrant gap
-> apply Inquiry Policy: no inquiry, or smallest sufficient evidence
-> apply Metareasoning Policy when control-mode choice is material
-> if search is materially iterative, apply Exploration Policy
-> apply Warrant / Choice Policy to the specific target
-> select responsibility
-> perform or delegate bounded work
-> ground returned evidence
-> apply Learning / Reconciliation Policy when the result is consequential
-> validate mechanics
-> update warrant
-> continue / stop / escalate / verify / ask owner
```

This is reasoning guidance, not a mandatory runtime phase machine.

New evidence may change the expected solution. That is a feature, not a failure.

## Adaptive Policy Coordinator: activate only decision-relevant policy questions

When multiple policy layers seem potentially relevant, ask which ones can actually
change the current decision. Use the smallest sufficient composition and collapse back
to direct work as soon as the decision stabilizes.

```text
policy available
!= policy must activate

clear + local + reversible + sufficiently evidenced
-> direct bounded work + relevant verification

iterative search only
-> Exploration Policy may become explicit

consequential returned evidence only
-> Learning / Reconciliation may become explicit
```

The coordinator does not select a Skill/workflow/Campaign automatically and does not
grant authority. Read `references/adaptive-policy-coordinator-v0.md` when policy
composition itself is material.

## Adaptive guidance: use the lightest process that preserves the invariants

Before deciding how much Sensemaking structure to use, make a qualitative judgment about five contextual factors:

```text
user supervision capability
-> how much scaffolding/explanation is useful?

desired delegation
-> how much repository-answerable judgment should I exercise
   within granted authority?

decision complexity
-> how much repository sensemaking/investigation is warranted?

consequentiality
-> how much evidence, validation, reconciliation, or caution is warranted?

continuation complexity
-> does repository-specific decision state need durable Campaign support?
```

Keep the doctrine stable while adapting the ceremony:

```text
clear + local + low consequence + one context
-> direct bounded work + relevant tests

responsibility uncertain / repository-wide evidence matters
-> repository sensemaking

consequential claim or repair
-> stronger evidence / reconciliation / finding-specific verification when warranted

state must survive fresh contexts
-> durable Campaign state
```

Important non-identities:

```text
user supervision capability != permanent expertise class
desired delegation != granted authority
decision complexity != technical difficulty
decision complexity != consequentiality
continuation complexity != task size
more scaffolding != more visible machinery
```

Do not score these factors, infer a permanent beginner/expert class, create a Campaign merely because a task is large, or translate them into automatic Skill/workflow routing. For examples and anti-patterns, read `references/adaptive-guidance-v0.md` when this decision is material.

### Broad delegated repository missions

A user may delegate an **outcome** rather than a preselected implementation task, for example completing the current authoritative product scope or advancing the repository until no further warranted change remains.

Treat such a prompt as a delegation contract:

```text
authoritative desired state
+ evidence-driven responsibility selection
+ granted authority
+ explicit terminal conditions
```

Exercise repository-answerable intermediate judgment, but do not translate broad delegation into unlimited scope, automatic backlog execution, permanent Campaign creation, product-thesis revision, or protected external-action authority.

For concrete terminal-mission patterns and anti-patterns, read `references/delegated-goal-patterns.md` when the mission's scope, authority, or stopping boundary is material.

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

### When the repository's future is the problem

Use `strategic-repository-analysis` when the user is not primarily asking for a
diagnosis or a preselected task, but for a high-level repository evolution
decision such as:

- what could this repository become from here?
- what are the coherent ways to construct/develop it?
- which major capability directions are plausible?
- what do those paths build on, require, unlock, or risk?
- what strategic uncertainty would change the choice?

Its output is a `strategic_repository_analysis`:

```text
current system model
-> capability / limitation map
-> Strategic Frontier
-> 0–5 coherent construction paths when materially real
-> qualitative path comparison
-> decision-changing uncertainty
-> strategic synthesis
-> BUILD / INVESTIGATE / DEFER / NO_CHANGE / OWNER_DECISION / THESIS_REVIEW
```

A current `repository_sensemaking_brief` may be used as evidence, but it is not
a mandatory prerequisite when the strategic analysis can establish current
repository state directly.

Zero construction paths is valid when current evidence/authority does not support even
one coherent construction trajectory yet. Do not manufacture an alternative merely to
make the analysis look complete. A `BUILD` disposition still requires a selected real
path.

```text
repo-sensemaker = diagnostic repository understanding
strategic-repository-analysis = Level-3 repository evolution synthesis

strategic disposition
!= implementation authorization
```

If the strategic disposition is `BUILD`, only then nominate the smallest
bounded repository responsibility and check execution authority independently.
Do not translate construction paths into an automatic backlog.

Sensemaking is not ceremony. Use the lightest surface that can change the
decision.

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

### Make warrant explicit when useful

For consequential work, ask:

1. **What exactly am I trying to justify now?**
2. **What must be true for that target to be warranted?**
3. **Which unresolved premise could change responsibility, scope, authority, continuation, or closure?**
4. **Is more reasoning worth more than acting now?**

Useful warrant targets include a claim, inquiry, responsibility, action, continue/stop/escalate decision, closure claim, or protected transition such as merge/publication.

Keep these distinctions explicit:

```text
warrant != confidence score
warrant != authorization
warrant for target A != warrant for target B
```

Use the lightest amount of explicit structure that preserves the decision boundary.

### Warrant / Choice Policy v0

For a consequential contemplated target, ask:

> **What does the current evidence, state, constraints, and authority warrant for this specific target?**

Name the target first. Useful targets include claims, inquiries, responsibilities, actions, continue/stop/escalate choices, closure claims, protected transitions, and strategic directions.

```text
warrant for target A
!= warrant for target B

WARRANTED
!= authorized
!= executed
!= successful

candidate set exists
!= one candidate must be selected
```

When several materially credible targets exist, compare only what matters to the current decision: target-specific support, nearest warrant gap, smallest sufficient intervention, reversibility, currentness, and authority. Select one when commitment is actually needed; otherwise preserve alternatives or return `NO_SELECTION`.

Read `references/warrant-choice-policy-v0.md` when explicit target adjudication or choice is material.

### Learning / Reconciliation Policy v0

After consequential evidence returns, ask:

> **What explicit claims, uncertainties, responsibility, continuation state, or strategic frame should change—if anything?**

`NO_MODEL_CHANGE` is valid. Other useful dispositions include confirming or revising claims, resolving/opening uncertainty, changing responsibility, continuing, stopping, escalating, reopening strategy, or requiring Level-4 thesis review.

```text
result returned
!= state update automatic

learning
!= model-weight update

authority need discovered
!= authority granted
```

Persist only the explicit decision-relevant update another context must reconstruct, using existing Campaign / STATUS / ADR / handoff / evidence surfaces.

Read `references/learning-reconciliation-policy-v0.md` when returned evidence can materially change the decision model.

### Inquiry Policy v0

Before turning an unresolved uncertainty into investigation, ask:

> **Given the current decision and epistemic state, what should I learn next, if anything?**

Inquiry is warranted only when additional evidence could materially change responsibility, scope, authority path, continuation, verification, or closure **and** obtaining that evidence is worth its cost.

```text
uncertainty exists
!= inquiry required

more evidence possible
!= more evidence worth obtaining

NO_INQUIRY_NEEDED
= valid successful policy result
```

When inquiry is warranted, identify the smallest sufficient evidence, its source, the bounded evidence-producing responsibility (if one is needed), authority, and a stop condition.

If the missing premise is owner intent, ask the owner rather than searching the repository. If the needed evidence is external and unavailable or unauthorized, record the external dependency rather than fabricating a local substitute.

Inquiry selection is not action authorization. Returned evidence comes back to the active semantic controller for adjudication.

Read `references/inquiry-policy-v0.md` when explicit inquiry selection is material. Policy Hierarchy v0 is defined in `../../docs/policy-hierarchy-v0.md`.

### Metareasoning Policy v0

When the real question is **how to spend the next unit of reasoning/action effort**, select the smallest useful control move:

```text
ACT
INQUIRE
CHALLENGE
EXPLORE
VERIFY
ESCALATE
STOP
```

Use `ACT` when an already-selected authorized bounded responsibility is sufficiently warranted and more thinking is not worth its cost.

Use `INQUIRE` when Inquiry Policy has identified decision-changing evidence worth obtaining.

Use `CHALLENGE` for consequential, low-reversibility, conflicting, or weakly supported commitments.

Use `EXPLORE` when the frame or option set may be too narrow.

Use `VERIFY` when a consequential result, repair, or closure claim still needs direct confirmation.

Use `ESCALATE` when the real gap is owner intent, higher-scope commitment, protected authority, or external control.

Use `STOP` when no additional effort is warranted.

```text
control move selected
!= responsibility authorized

cheap + reversible + low consequence + information-producing
-> acting can dominate thinking longer
```

Keep this implicit for obvious local work. Read `references/metareasoning-policy-v0.md` when control-mode selection is consequential or ambiguous.

### Challenge and exploration when commitment risk is material

```text
high consequence / low reversibility / conflicting evidence /
novelty / repeated failure / weakly-supported confidence
-> consider adversarial challenge

narrow or repeatedly failing option set / unstable frame
-> consider exploration

otherwise
-> do not add critique ceremony by default
```

**Challenge** asks why the current frame, claim, forecast, option, or closure decision might be wrong.

**Exploration** asks what plausible frame, option, explanation, or intervention is not yet represented.

### Exploration Policy v0

When iterative search has multiple meaningful attempts, use the material search history to allocate the next search move:

```text
EXPLOIT
EXPLORE
CHALLENGE
DIAGNOSE
RECOMBINE
RESTART
VERIFY
EXIT_SEARCH
```

`EXIT_SEARCH` is valid when additional search is unlikely to improve the decision enough to justify its cost.

Search history is a decision-relevant projection of existing evidence/provenance. Keep it transient for small work and reuse existing Campaign/handoff/STATUS/repository-history surfaces when continuation makes it durable.

```text
search history exists
!= SearchState schema required

Exploration Policy
!= Strategic Frontier ranking
```

Keep this implicit for one-shot/local work; do not turn the modes into a score or routing table.

Critic or explorer output is evidence for the active agent; it is not automatic veto, approval, or authority.

Read `references/exploration-policy-v0.md` when iterative search allocation is material. For explicit inquiry selection, read `references/inquiry-policy-v0.md`. For challenge/exploration triggers, delegation evidence return, and persistence guidance, read `references/practical-agent-architecture-v0.md`.

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

When work is delegated to a Skill, subagent, workflow, or external execution system, preserve the evidence-return boundary:

```text
delegated result
-> evidence for the active agent
-> semantic reassessment

worker recommendation != parent decision
worker success != global closure
retry/fallback policy != permission to change responsibility
```

Delegation does not transfer responsibility-selection, closure, or protected-action authority unless that authority was explicitly delegated.

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

Durability and transferability are not identical. Externalize selected rationale, evidence, decisions, or material search history when another actor/context must continue, rediscovery would be costly, or governance/operations/user transfer requires an intelligible artifact. A reasoning result does not automatically require a durable document, and hidden chain-of-thought is never a persistence requirement.

---

## References

Read these when the task needs deeper detail:

- `references/adaptive-guidance-v0.md` — contextual scaffolding, rigor, consequentiality, delegation, and Campaign-use examples
- `references/adaptive-policy-coordinator-v0.md` — compose only decision-relevant semantic policy questions and collapse unnecessary ceremony
- `references/inquiry-policy-v0.md` — decide what to learn next, if anything; smallest sufficient evidence and source boundaries
- `references/metareasoning-policy-v0.md` — choose the next qualitative control move: act, inquire, challenge, explore, verify, escalate, or stop
- `references/exploration-policy-v0.md` — allocate iterative search effort across exploit, explore, challenge, diagnose, recombine, restart, verify, or exit-search
- `references/warrant-choice-policy-v0.md` — adjudicate what a specific target is warranted now and select one warranted target or decline selection
- `references/learning-reconciliation-policy-v0.md` — reconcile returned evidence into explicit claims, uncertainty, responsibility, continuation, or strategic state
- `references/practical-agent-architecture-v0.md` — warrant targets/dependencies, challenge vs. exploration, resource-aware stopping, delegation evidence return, and persistence guidance
- `../../CONTEXT.md` — current product/system context and terminology
- `../../docs/agent-native-operating-workflow.md` — canonical v0 operating map
- `../../docs/decision-orchestration-boundary.md` — decision vs. execution/orchestration ownership
- `../../docs/adr/0013-agent-native-orchestration-primary.md` — active-agent control ownership
- `../../docs/adr/0029-current-product-boundary.md` — current product boundary and deferred automatic routing
- `../workflow-planner/references/artifact-contracts.yaml` — artifact/machine-field contracts
- `../workflow-planner/references/workflow-registry.yaml` — registered bounded workflows/subgraphs
- `../repo-sensemaker/references/evidence-rules.md` — evidence discipline
- `../repo-sensemaker/references/ui-fog-signals.md` — detailed UI-fog signals when UI classification matters
- `../../docs/research/control-model-research-agenda.md` — research hypotheses that must not be treated as ratified product architecture

## Summary: your job as the active agent

1. Establish the goal and authority boundary.
2. Decide how much scaffolding, investigation rigor, verification, and durable state the situation warrants.
3. Ask what uncertainty could change the correct next action.
4. Resolve that uncertainty from the right evidence source.
5. Select the responsibility before the Skill or solution.
6. Perform bounded work through the appropriate capability.
7. Validate mechanics without confusing PASS with truth or closure.
8. Reconcile consequential work claims.
9. Repair-verify original findings when relevant.
10. Update the warrant from new evidence.
11. Continue, stop, escalate, or ask the owner deliberately.

**Most importantly:** the goal is not to follow a predetermined workflow. The goal is to move from uncertainty to warranted engineering action while keeping evidence, claims, authority, and continuation proportional to the situation.