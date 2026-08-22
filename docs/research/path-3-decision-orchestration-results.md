# Path 3 — Decision Versus Orchestration Results

**Status:** completed bounded repository-grounded synthesis / proposed research disposition  
**Authority:** research evidence only; not an ADR, product contract, schema, Skill, routing rule, workflow-registry change, or runtime specification  
**Tracker:** Issue #210  
**Protocol:** `docs/research/decision-versus-orchestration.md`  
**Frozen episode set:** `docs/research/path-3-episode-set.md`  
**Analysis baseline:** `main@dbeeac92d868d65afe3334ad393dac6d3b5f021e`  
**Episode count:** 8  
**Proposed bounded disposition:** `BOUNDARY_COHERENT`

## 1. Research question

> **Across concrete repository-grounded episodes, can the current decision/orchestration boundary distinguish responsibility-selection decisions from execution-control decisions without either orchestration swallowing decision or Sensemaking swallowing orchestration?**

The governing architectural sentence tested here is:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

The eight episode identities were frozen before these records and this synthesis were written. P3-E03 and P3-E05 intentionally inspect different transitions from the same EXP-0005 campaign and are not treated as independent replications.

## 2. Summary result

Across the frozen episode set, the boundary remained coherent without requiring a new exception or contradictory ownership rule.

Three recurring distinctions did the explanatory work:

1. **Responsibility selection versus step selection.** The decision layer determines which engineering responsibility should become active at all; orchestration may deterministically select the next already-declared step only after that responsibility is selected.
2. **Execution gating versus responsibility redirection.** A deterministic validator, authorization guard, timeout/failure rule, or review gate may refuse or pause an execution transition. Interpreting that observation into a different engineering responsibility remains a decision-layer transition.
3. **Owning decision-critical evidence versus owning the runtime that produced it.** Scheduler state, attempt ledgers, validation results, logs, and other execution state may materially constrain the next decision. Sensemaking therefore needs truthful access to the relevant evidence, but it does not follow that Sensemaking should own generic scheduler, worker, queue, persistence, or DAG machinery.

No episode required deterministic orchestration to choose among materially different engineering responsibilities in order to remain correct. No episode showed that the decision loop itself must own generic execution infrastructure in order to reason correctly.

The strongest bounded conclusion is therefore:

> **Across the eight frozen repository-grounded episodes studied, the current decision/orchestration distinction provides a coherent explanatory boundary: evidence-grounded responsibility selection remains agent-owned, while deterministic coordination may proceed after responsibility selection without acquiring authority to change the engineering responsibility.**

This does **not** establish universal architectural adequacy, optimal workflow design, runtime completeness, real-world prevalence of either failure mode, or that every future transition has a unique classification.

## 3. Episode records

### P3-E01 — superseded ADR 0018 deterministic fog routing

**Repository evidence:** `docs/adr/0018-workflow-routing-policy.md`, blob `a6ff0bb294875c38778a8114bb0dcd166bd2aca5`.

**Contemplated decision:** which downstream engineering responsibility should follow a repository-sensemaking brief.

**Responsibility selected / under consideration:** architectural review versus escalation or some other responsibility.

**Decision-changing evidence or uncertainty:** the current repository goal, live weakest boundary, current uncertainty, later canonical decisions, and whether architectural review is actually the warranted next responsibility. `primary_fog_type` is diagnostic evidence but does not by itself settle those questions.

**Authority boundary:** responsibility selection belongs to the active coding agent under the later agent-native architecture. Diagnostic metadata does not grant routing authority.

**Orchestration mechanism:** the historical static `primary_fog_type -> workflow` routing table.

**Decision owner:** active coding agent.

**Orchestration owner:** workflow planner/runtime after a responsibility has already been selected.

**Why the behavior belongs on that side:** deterministic selection of a subflow is legitimate when it coordinates a responsibility already chosen for evidence-grounded reasons. The historical ADR instead proposed making `primary_fog_type` itself the authority that selected downstream work.

**Counterfactual if orchestration owned the decision:** a diagnostic label could silently commit the repository to architectural review even when later evidence, authority, or a live uncertainty made reconciliation, stopping, escalation, verification, or another responsibility more warranted.

**Counterfactual if decision owned the orchestration:** requiring the active agent to manually choose every stable step inside an already-selected architectural-review subflow would add judgment where a static sequence is sufficient and would reduce repeatability without improving responsibility selection.

**Ambiguity / caveat:** the same table lookup is not inherently unsafe. If the agent has already selected architectural review, a deterministic lookup or subflow invocation can be ordinary orchestration. The failure shape is granting the table authority to make the product-level responsibility decision.

**Failure-mode signal:** `F1` — historical orchestration-swallowing-decision design, later superseded.

### P3-E02 — PR #164 stale-vs-live responsibility redirection

**Repository evidence:** PR #164 head `b51822e7da941cf5a5d42d31017d6c9e186c36e4` and `docs/research/uncertainty-selection-pr164-falsification.md`, blob `102e03a74a98c9cc84f8418aa700fc4f81ab35b2`.

**Contemplated decision:** whether to refresh/rebase the old prototype and run another vNext experiment.

**Responsibility selected / under consideration:** further prototype execution versus inspecting current canonical decision state and stopping work on the stale surface.

**Decision-changing evidence or uncertainty:** whether PR #164 was still a live decision surface at all. Later canonical evidence had already harvested and adjudicated the material packaging questions.

**Authority boundary:** current canonical decisions and owner-accepted product state outrank unresolved questions preserved in an old exploratory artifact.

**Orchestration mechanism:** a plausible fixed `rebase -> rerun checks -> run another experiment` path.

**Decision owner:** active coding agent using current canonical evidence and live-warrant reasoning.

**Orchestration owner:** deterministic rebase/test/experiment mechanics only if further prototype work is first warranted.

**Why the behavior belongs on that side:** liveness of the responsibility is semantic and evidence-dependent. A workflow can reliably execute a rebase and rerun, but it cannot infer from the existence of an old unresolved question that the old responsibility is still live.

**Counterfactual if orchestration owned the decision:** the system would perform disciplined but globally stale work, consuming evidence-gathering effort against a superseded product question simply because the historical artifact still contained unresolved text.

**Counterfactual if decision owned the orchestration:** once a new experiment were actually selected, forcing the agent to manually manage every deterministic rebase/check step would not improve the liveness decision and would weaken repeatability.

**Ambiguity / caveat:** old artifacts can still carry live findings. The decision rule is not “old means stale”; it is “check whether the finding or uncertainty remains live in the current warrant.”

**Failure-mode signal:** `F1` — counterfactual fixed-path hazard; avoided in the observed handling.

### P3-E03 — EXP-0005 durable attempt lifecycle

**Repository evidence:** `experiments/results/EXP-0005-stage1-auteur-github-connector-pilot/report.md`, blob `93bb74fa17d46a2566932342b3645b5663ba2620`.

**Contemplated decision:** how to perform the already-approved bounded campaign attempts without losing accounting, target identity, or exact-head validation guarantees.

**Responsibility selected / under consideration:** execute the frozen connector-native campaign responsibility against the pinned target within the approved envelope.

**Decision-changing evidence or uncertainty:** campaign approval, frozen target/configuration/policy, remaining attempt budget, and later produced target evidence. Those inputs were selected before the deterministic lifecycle transitions ran.

**Authority boundary:** the campaign envelope bounded what could execute; target mutation, fallback, hidden retry/repair, and automatic merge were prohibited. The lifecycle could not expand its own authority.

**Orchestration mechanism:** `RESERVED -> INVOKED -> OUTPUT_CAPTURED -> exact-head validation -> terminal state`, concurrency one, durable attempt accounting, and fail-closed budget constraints.

**Decision owner:** active agent/human governance for campaign authorization and later research interpretation.

**Orchestration owner:** durable campaign state transitions, serialized attempt control, artifact preservation, and exact-head validation.

**Why the behavior belongs on that side:** after the target, responsibility, authorization envelope, and budget were already fixed, the lifecycle transitions were mechanically expressible and gained no authority to choose a different engineering responsibility.

**Counterfactual if orchestration owned the decision:** a failed attempt, exhausted slot, or validation result could silently trigger a different target, fallback model, repair, hidden retry, or altered analysis responsibility. That would turn execution policy into unauthorized responsibility selection.

**Counterfactual if decision owned the orchestration:** asking the active agent to improvise reservation order, invocation accounting, concurrency, artifact preservation, and exact-head validation each time would add no useful judgment and would make hidden replay/accounting errors more likely.

**Ambiguity / caveat:** the attempt itself contains model judgment while producing the brief. This episode classifies the durable attempt lifecycle, not the semantic content of the brief, as orchestration.

**Failure-mode signal:** `none` — positive deterministic-orchestration control.

### P3-E04 — EXP-0004 approval-audit fail-closed boundary

**Repository evidence:** Issue #197 and disposition comment `#issuecomment-5331288456`.

**Contemplated decision:** whether the approved EXP-0004 envelope could truthfully enter operative execution on the active surface.

**Responsibility selected / under consideration:** execute the frozen campaign versus stop before operative receipt and conclude the envelope was not executable as specified.

**Decision-changing evidence or uncertainty:** the frozen approval contract required a concrete `session-id#message-id`; the active surface did not expose truthful identifiers.

**Authority boundary:** the human standalone approval authorized only the exact frozen envelope. Neither the executor nor the agent could fabricate an identifier, reinterpret the approval contract, or silently repair the campaign in place.

**Orchestration mechanism:** receipt validation and pre-invocation fail-closed lifecycle checks.

**Decision owner:** human for approval; active agent for interpreting the invariant failure, concluding the research disposition, and deciding that any repair belonged in successor framework work.

**Orchestration owner:** verifier/lifecycle logic that refused to cross the operative execution boundary when the required receipt could not validate.

**Why the behavior belongs on that side:** this episode is a sequential handoff. The mechanical guard owns “this transition is invalid under the frozen contract.” The agent owns “therefore this campaign is falsified at this boundary, do not repair it in place, and any successor must be newly designed and approved.”

**Counterfactual if orchestration owned the decision:** execution machinery could invent a plausible identifier, select a replacement approval interpretation, or mutate the envelope to keep running, crossing a human-authority boundary.

**Counterfactual if decision owned the orchestration:** the agent could treat the verifier as advisory and manually bypass a failed prerequisite, making the fail-closed contract rhetorical rather than executable.

**Ambiguity / caveat:** “stop” appears in both layers, but at different semantic levels. Orchestration refuses an invalid state transition; decision interprets that refusal into campaign disposition and next responsibility. This is sequential participation, not contradictory ownership.

**Failure-mode signal:** `none` — positive authority/gating boundary control.

### P3-E05 — EXP-0005 exact-head validation, disposition, and integration separation

**Repository evidence:** PR #203 head `c206f212011924deae045f03303fec40eb344ef6`, aggregate Validator #503 (`32177211469`), later owner-authorized merge `65c2be1b430e7bc8d1400ca99d80c6ff6256a051`, and the EXP-0005 report blob `93bb74fa17d46a2566932342b3645b5663ba2620`.

**Contemplated decision:** whether the preserved campaign results were technically valid, what bounded research disposition they supported, and whether the exploratory evidence should be integrated.

**Responsibility selected / under consideration:** validate the exact results head; interpret the campaign evidence; optionally integrate the historical evidence after owner authorization.

**Decision-changing evidence or uncertainty:** exact-head validator result, full durable attempt history, result classification, and explicit owner authority for integration.

**Authority boundary:** technical validation did not grant publication/merge authority. Exploratory classification did not automatically become canonical evidence.

**Orchestration mechanism:** exact-head GitHub Actions validation and durable report/artifact accounting.

**Decision owner:** active agent for bounded research interpretation; human owner for integration authorization.

**Orchestration owner:** deterministic validator and evidence-preservation machinery.

**Why the behavior belongs on that side:** the validator can establish that a specific head satisfies deterministic repository checks. It cannot decide what scientific claim is warranted from that evidence or whether the owner wants the evidence integrated.

**Counterfactual if orchestration owned the decision:** green validation could automatically imply `SUPPORTED`, promote exploratory evidence, or merge the PR, conflating technical success, research inference, and authority.

**Counterfactual if decision owned the orchestration:** replacing exact-head validation with free-form agent confidence would weaken evidence identity and make the research interpretation harder to audit.

**Ambiguity / caveat:** P3-E05 and P3-E03 share one campaign. They test different semantic transitions and are not independent empirical replications.

**Failure-mode signal:** `none` — clean execution-evidence-to-decision handoff.

### P3-E06 — Path 01b `act_now` / stop-investigating control

**Repository evidence:** `docs/research/path-01b-synthetic-coherence-results.md`, blob `02db3672294fe09774f8e917b482bed9231105ec`, scenario `SCLU-006`.

**Contemplated decision:** whether to make a cheap reversible behavior-preserving refactor now or investigate two adjacent unresolved questions first.

**Responsibility selected / under consideration:** perform the private rename/comment correction without additional evidence gathering.

**Decision-changing evidence or uncertainty:** neither adjacent unresolved question changed correctness, public behavior, authority, or reversibility of the current refactor. They were not live warrant dependencies for the contemplated action.

**Authority boundary:** the agent may stop investigating when unresolved questions are non-gating; unresolvedness alone does not authorize orchestration to launch more investigation.

**Orchestration mechanism:** perform the selected bounded edit and its validation after the decision to `act now`.

**Decision owner:** active agent applying the qualitative warrant/liveness reasoning.

**Orchestration owner:** edit/test mechanics after the bounded action is selected.

**Why the behavior belongs on that side:** whether more evidence is worth gathering is a target-specific decision-value judgment. Once the action is selected, the edit/validation sequence can be deterministic.

**Counterfactual if orchestration owned the decision:** a generic workflow could see unresolved adjacent questions and automatically launch investigation, making “unresolved” equivalent to “blocking” and recreating stale/information-gain work.

**Counterfactual if decision owned the orchestration:** manually choosing every edit/validation micro-step would not improve the decision about whether evidence is needed.

**Ambiguity / caveat:** this is evaluator-aware synthetic evidence, not a normal-use empirical engineering episode. It therefore checks conceptual consistency more than real-world prevalence.

**Failure-mode signal:** `none` — conceptual stopping control consistent with the boundary.

### P3-E07 — registered `docs-contract-reconciliation` subflow

**Repository evidence:** `skills/workflow-planner/references/workflow-registry.yaml`, blob `31aa4550bed57e13a4fbae66b6528c512ca056a5`, plus `scripts/workflow-runtime.py` at analysis baseline, blob `a48f3c1d8635c1dbd11a10b42c0daa050542da3c`.

**Contemplated decision:** after docs/contract reconciliation has been selected as the responsibility, how should diagnosis, reconciliation, verification, and handoff be sequenced.

**Responsibility selected / under consideration:** reconcile drift among documentation, registries, artifact contracts, templates, and validator rules.

**Decision-changing evidence or uncertainty:** the initial repository diagnosis and later verification may show that the presumed reconciliation responsibility is wrong, complete, incomplete, or needs escalation.

**Authority boundary:** the workflow declaration does not itself prove the reconciliation responsibility is warranted. In `guided_execution`, runtime gate behavior is mandatory, giving explicit review boundaries where evidence can be reassessed rather than assuming every later step is always warranted.

**Orchestration mechanism:** declared four-step sequence: `repo-sensemaker -> sensemaking-docs-reconciler -> repair-verifier -> handoff`, with review gates and declared artifacts.

**Decision owner:** active agent/human at entry and at any material reassessment/redirection boundary.

**Orchestration owner:** registry/runtime sequencing, artifact passing, deterministic validation, and gate coordination inside the selected reconciliation responsibility.

**Why the behavior belongs on that side:** once reconciliation is selected, the declared sequence is a bounded mechanically stable subgraph. The review gates prevent the sequence from needing product authority merely to remain useful; evidence can be surfaced back to the decision layer before continuing.

**Counterfactual if orchestration owned the decision:** a runner could treat the workflow id as permanent authority and continue reconcile/verify/handoff even if diagnosis showed that the real responsibility had shifted to product clarification, retirement, escalation, or some non-reconciliation concern.

**Counterfactual if decision owned the orchestration:** requiring the agent to reconstruct step order, artifact plumbing, validator dispatch, and gate bookkeeping on every run would duplicate stable execution mechanics and make the workflow registry largely pointless.

**Ambiguity / caveat:** this study inspected the canonical declaration and runtime gate semantics; it did not execute a fresh normal-use `docs-contract-reconciliation` run. Coherence therefore depends on review gates remaining genuine reassessment/exit boundaries rather than decorative acknowledgements. This is a runtime-behavior caveat, not a contradiction in the ownership rule.

**Failure-mode signal:** `none` — positive bounded-subflow control with an execution-evidence limitation.

### P3-E08 — EXP-0002 executor-host recovery / generic execution-continuity pressure

**Repository evidence:** Issue #187 and reclassification comment `#issuecomment-5327362061`.

**Contemplated decision:** whether another EXP-0002 attempt could safely proceed and what empirical conclusion was warranted when GitHub lacked authoritative executor-host state.

**Responsibility selected / under consideration:** recover scheduler/host-local evidence before any replay, versus preserve the ambiguity and conclude the research path without inventing machine state.

**Decision-changing evidence or uncertainty:** Task Scheduler `LastRunTime` / `LastTaskResult`, execution log, machine-local ledger, attempt directories, reservation/output/result files, and whether any attempt had already consumed authority.

**Authority boundary:** absence of GitHub output did not authorize a retry. The agent could not claim `zero attempts`, `never executed`, or complete accounting without the missing executor evidence.

**Orchestration mechanism:** Windows scheduling, process execution, local persistence, attempt ledger/output files, and host recovery state.

**Decision owner:** active agent using whatever truthful execution evidence is available to classify the research state and determine whether replay would be safe.

**Orchestration owner:** scheduler/worker/persistence infrastructure and its durable execution records.

**Why the behavior belongs on that side:** the scheduler and host-local state are execution infrastructure. Their facts are decision-critical evidence, but owning the Task Scheduler, worker process, log transport, or generic persistence service would not itself improve responsibility selection. The correct product obligation is to consume or require truthful evidence from those systems, not to absorb them into Sensemaking by default.

**Counterfactual if orchestration owned the decision:** “no GitHub result” or “task appears absent” could be turned automatically into permission to replay, risking a hidden retry after authority may already have been consumed.

**Counterfactual if decision owned the orchestration:** Sensemaking would need to become the scheduler, worker manager, persistence layer, and recovery system merely so the agent could reason about campaign state, expanding the product thesis around generic runtime continuity instead of decision semantics.

**Ambiguity / caveat:** this episode shows an important interface requirement: execution infrastructure can contain facts without which the decision layer cannot safely proceed. Keeping the runtime outside Sensemaking therefore does not mean its state is irrelevant or optional. The historical machine-local ambiguity remains unresolved.

**Failure-mode signal:** `F2` — concrete pressure toward absorbing generic orchestration, avoided by preserving the external-evidence limitation instead.

## 4. Cross-episode comparison

### 4.1 F1 — orchestration swallows decision

P3-E01 is the clearest historical F1 instance: diagnostic metadata was proposed as direct routing authority. P3-E02 demonstrates the same shape from another angle: a fixed execution path could have continued a stale prototype responsibility after later evidence had removed its decision relevance.

The positive controls identify the safer boundary:

- P3-E03 allows deterministic state transitions only inside an already-frozen campaign responsibility and envelope.
- P3-E04 permits a validator to refuse an invalid transition but not to reinterpret approval, repair the campaign, or choose a successor responsibility.
- P3-E05 lets validation establish facts about an exact head while keeping scientific disposition and integration authority outside the validator.
- P3-E06 makes evidence-gathering itself a selected responsibility rather than an automatic consequence of unresolved questions.
- P3-E07 allows a fixed subflow only after docs/contract reconciliation is selected and relies on review gates as evidence-return boundaries.

The consistent rule across these cases is:

> **Orchestration may deterministically choose the next step only inside the semantic boundary of already-selected work. When new evidence would change the responsibility itself, control returns to decision.**

### 4.2 F2 — decision swallows orchestration

P3-E08 supplies concrete F2 pressure. Safe campaign reasoning needed scheduler/log/ledger facts, but that does not imply that Sensemaking should become a Task Scheduler, worker manager, persistence service, queue, or generic recovery runtime.

P3-E03 and P3-E07 reinforce the positive side: reservation ordering, artifact plumbing, validation dispatch, gate bookkeeping, and stable subflow sequencing are useful precisely because they are mechanized rather than repeatedly re-decided.

The consistent rule is:

> **Decision may require truthful execution evidence without owning the generic machinery that produces and persists that evidence.**

That rule prevents “runtime state matters to judgment” from being misread as “the decision product must own the runtime.”

### 4.3 Execution gates are not product decisions

P3-E04 is the important edge case. A deterministic guard can correctly return “this transition may not proceed” without thereby selecting the next engineering responsibility. The later judgment—falsify this envelope, stop, design successor framework work, or escalate—is separate.

This same separation appears in P3-E05 and P3-E07. A validator or review gate can define an execution boundary; it does not acquire authority to interpret evidence into a materially different engineering responsibility.

### 4.4 Authority remains a separate axis

P3-E04 and P3-E05 show that neither decision nor orchestration can manufacture external authority. Human approval, publication, and merge authority remain distinct from technical capability and technical validity.

The boundary therefore does not collapse to two total system layers. It is a control-ownership distinction operating alongside authority constraints.

## 5. Bounded disposition

**`BOUNDARY_COHERENT`**

The current decision/orchestration distinction explains the eight frozen repository-grounded episodes without material contradiction. The required counterfactuals also show that moving responsibility selection into orchestration or generic runtime ownership into Sensemaking would predict concrete correctness failures or product-boundary expansion.

This disposition is intentionally bounded. It means only that the current distinction is a coherent explanatory and design-constraining rule across this selected repository evidence set.

It does **not** establish:

- universal architectural adequacy;
- that every future transition is easy to classify;
- runtime completeness or correctness of every registered workflow;
- optimal workflow design;
- prevalence of F1 or F2 in ordinary engineering;
- independent replication across repositories, agents, teams, or domains;
- that the protocol itself should become executable schema or routing machinery.

## 6. Limitations

1. **Single repository / retrospective analysis.** The episode set comes from one repository history and was interpreted in one research context.
2. **Selection was frozen, not independent.** Freezing prevents post-result substitution but does not provide blind or independent evaluation.
3. **Shared evidence dependence.** P3-E03 and P3-E05 are different transitions from EXP-0005, not independent replications.
4. **One synthetic control.** P3-E06 comes from evaluator-aware Path 01b synthetic research and should not be counted as real-world prevalence evidence.
5. **Declared workflow versus fresh execution.** P3-E07 inspected canonical registry and runtime gate semantics but did not perform a new normal-use workflow run in this study.
6. **Unresolved executor history remains unresolved.** P3-E08 does not recover the missing Windows host state; it analyzes the control boundary exposed by that limitation.
7. **Classification still requires semantic judgment.** The result supports a reasoning boundary, not a machine classifier for `decision` versus `orchestration`.

## 7. Design implications without machinery promotion

The study supports several design constraints, not new runtime features:

- diagnostic metadata may inform responsibility selection but must not silently become responsibility-routing authority;
- fixed subflows should begin only after the responsibility they coordinate is selected;
- execution failure/gating may stop or pause a transition, but responsibility redirection returns to decision;
- validators should establish bounded facts and return evidence rather than infer scientific disposition or merge authority;
- execution infrastructure should expose enough provenance/state for safe reassessment when its history is decision-critical;
- decision-critical execution state does not by itself justify moving generic scheduler/worker/persistence machinery into Sensemaking;
- review gates inside bounded workflows must remain real reassessment/exit boundaries when new evidence can invalidate the workflow's assumed responsibility.

No evidence in this cycle satisfies the repository's machinery-promotion rule for a new decision/orchestration schema, routing engine, Skill, scheduler, queue, worker manager, persistence service, DAG runtime, retry/fallback system, or Workflow-v0/registry behavior change.

## 8. Handoff

Path 3 can close at this bounded research level if this result is reviewed and integrated.

The next research candidate is **Path 4 — domain-general control versus domain-specific semantics**:

> Which parts of the control model are genuinely domain-general, and which only work because software-engineering semantics supply domain-specific evidence, authority, responsibility, and closure concepts?

Path 4 should treat this Path 3 result as bounded source evidence, not as proof that the control model transfers unchanged to another domain.
