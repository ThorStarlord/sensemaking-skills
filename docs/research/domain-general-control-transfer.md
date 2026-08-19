# Path 4 — Domain-General Control Versus Domain-Specific Semantics

**Status:** proposed bounded transfer protocol  
**Authority:** research protocol only; not an ADR, product contract, schema, Skill, workflow, runtime specification, or product-positioning change  
**Tracker:** Issue #214  
**Protocol baseline:** `main@6bfa1c2b42ca64bf6c8fa1fc349b9306f1c10e64`  
**Transfer domain:** AI research  
**Case target:** 8 frozen cases before evaluation

## 1. Research question

> **Within a bounded AI-research transfer exercise, can the current Sensemaking control policy remain internally coherent when software-engineering-specific responsibilities, evidence types, verification semantics, and authority boundaries are replaced by AI-research equivalents, without importing repository-specific assumptions into the control layer or inventing generic framework machinery?**

This protocol operationalizes Research Path 4 from `docs/research/control-model-research-agenda.md`.

The purpose is not to prove that Sensemaking is domain-general. The purpose is to test whether the current control concepts still explain decisions naturally after the surrounding domain semantics change materially.

## 2. Current product boundary

Sensemaking Skills remains a software-engineering product.

The current product baseline is not changed by this study:

- the active coding agent owns the top-level engineering control loop;
- bounded Skills perform software-engineering responsibilities;
- evidence, validation, verification, reconciliation, and authority constrain claims and actions;
- Path 3 preserves the distinction that decision selects the work while orchestration coordinates already-selected work.

No result from this protocol changes that positioning automatically.

## 3. Strongest permitted claim

A positive result may establish only:

> **Across the bounded AI-research transfer cases studied, the current control concepts can be applied coherently after replacing software-engineering-specific responsibility, evidence, verification, and authority semantics, providing limited evidence that the control principle may transfer beyond software engineering.**

A positive result does **not** establish:

- a domain-general product;
- universal applicability;
- production readiness outside software engineering;
- real-world AI-research effectiveness;
- cross-model or cross-organization reproducibility;
- a warranted generic core or domain-pack architecture;
- a warranted AI-research Skill suite;
- that all candidate control concepts are domain-general primitives.

## 4. Candidate control concepts under test

The exercise provisionally holds these concepts stable enough to test:

1. goal and current state;
2. decision-changing uncertainty;
3. warranted responsibility selection;
4. evidence-bounded claims;
5. distinction among knowing, deciding, acting, and publishing;
6. continuation, stopping, and escalation;
7. outcome-specific verification;
8. decision versus orchestration separation.

These are hypotheses, not ratified abstractions.

If a concept has to change meaning materially to survive the transfer, record that as transfer limitation rather than silently redefining it.

## 5. Semantics that must change

A legitimate transfer exercise must replace the surrounding domain model rather than relabel software artifacts.

### Software-engineering examples not assumed by the transfer

- repository, source tree, branch, commit, issue, pull request;
- tests and CI as the default verification surface;
- repair, refactor, retirement, reconciliation, merge;
- canonical branch state;
- merge/publication evidence as the default authority model.

### AI-research semantics to use instead

Cases should naturally involve combinations of:

- literature evidence and prior empirical findings;
- hypotheses and scientific claims;
- datasets, checkpoints, experiment configurations, seeds, metrics, and experiment artifacts;
- baseline reproduction;
- experiment design and execution;
- ablation and replication;
- claim-specific empirical verification;
- stochastic or distributional evidence;
- compute/resource commitments;
- dataset provenance, license, privacy, or ethics constraints;
- collaborator or project-owner authority;
- publication, preprint, benchmark, model, or artifact release authority.

The mapping must follow the research decision, not a desire to produce neat analogies.

## 6. Transfer invariants and semantic substitution

For each case, separate four layers explicitly.

### A. Control relation

Describe the proposed domain-independent relation among:

`goal/current state -> live decision-changing uncertainty -> evidence responsibility -> updated warrant -> responsibility/action/stop -> outcome evidence -> verification/claim/continuation`

Do not encode this as a machine state model. It is a reasoning relation under test.

### B. Domain semantics

Describe the AI-research objects and responsibilities that give the relation meaning in this case.

### C. Software leakage

Record any point where the reasoning appears to depend on software-specific assumptions such as:

- deterministic tests;
- one canonical branch;
- merge as the natural publication boundary;
- issue/PR ownership;
- source-code mutation as the primary action;
- repository history as the primary authority record.

### D. Forced analogy

Record any mapping that is formally tidy but distorts the actual AI-research decision.

Examples of insufficient reasoning include:

- assuming every metric is equivalent to a test;
- assuming every experiment artifact has a single canonical state equivalent to `main`;
- assuming publication authority is equivalent to merge authority;
- assuming replication is simply regression testing;
- assuming scientific uncertainty closes deterministically when a run is green.

## 7. Case-freeze protocol

Before evaluation, create exactly **8 transfer cases** in a separate frozen input artifact.

The inputs must be frozen before worked answers or evaluator notes are written.

The case set should cover these families:

1. **Literature-to-hypothesis responsibility** — an unresolved literature or prior-evidence question changes whether a hypothesis should be pursued.
2. **Baseline reproduction boundary** — reproduction failure can redirect responsibility from novel experimentation to understanding the baseline/environment mismatch.
3. **Competing experiment responsibilities** — ablation, more data, model change, or measurement repair are simultaneously plausible next responsibilities.
4. **Resource/irreversibility authority** — an expensive compute run, external service, or scarce resource commitment requires authority distinct from technical plausibility.
5. **Positive-result claim verification** — a surprising improvement requires finding-specific verification rather than generic information gain or execution success.
6. **Replication / negative-result stopping** — replication evidence changes whether to continue, narrow, stop, or reformulate the claim.
7. **Data/ethics/provenance authority** — technically plausible work is blocked or redirected by dataset provenance, license, privacy, ethics, or collaborator ownership.
8. **Publication/release authority** — technical evidence may be sufficient for a bounded claim while publication or external release still requires separate authority.

At least two cases must deliberately resist a clean software analogy.

A case may include multiple live uncertainties. Do not force every case into a single-question form if that changes its meaning.

## 8. Case construction rules

Each frozen case must specify only the situation needed for evaluation:

- research goal;
- current state;
- contemplated consequential decision;
- known evidence;
- live unresolved uncertainties;
- plausible next responsibilities;
- relevant resource or publication authority facts;
- verification target, if already defined;
- any explicit domain constraint.

Do **not** embed:

- a preferred answer;
- a hidden score;
- a software analogy;
- a Path 4 disposition;
- evaluator rationale;
- a statement that a concept is domain-general.

If synthetic cases are used, say so explicitly in the frozen artifact.

## 9. Per-case worked record

Every evaluated case must record:

1. **AI-research goal/current state**
2. **Contemplated consequential decision**
3. **Live decision-changing uncertainty or uncertainties**
4. **Why each uncertainty is gating or non-gating**
5. **Selected responsibility**
6. **Plausible competing responsibility**
7. **First evidence-producing responsibility, if further evidence is warranted**
8. **Expected decision effect of that evidence**
9. **Evidence-bounded claim that could be made now**
10. **Verification/closure evidence appropriate to that claim**
11. **Authority needed to act, spend resources, access data, or publish**
12. **Decision/orchestration boundary**
13. **Software leakage detected**
14. **Forced analogy detected**
15. **Control-concept outcome:** `survives naturally`, `survives with qualification`, or `fails in this case`
16. **Ambiguity/caveats**

The record must explain the decision qualitatively. Do not introduce numeric control scores or aggregate rankings.

## 10. Decision-changing uncertainty transfer check

The case should demonstrate that an uncertainty matters because a credible alternative answer could materially change one or more of:

- hypothesis pursued;
- experiment responsibility;
- scope of claim;
- evidence responsibility;
- resource commitment;
- continuation or stopping;
- escalation;
- action/publication authority.

Interesting uncertainty is not automatically decision-changing uncertainty.

This criterion intentionally mirrors the control relation while replacing the software-engineering decision surface.

## 11. Evidence and claim transfer check

Scientific evidence may be stochastic, noisy, aggregate, or replication-dependent.

Therefore evaluation must test whether `evidence-bounded claims` works without treating deterministic pass/fail evidence as the default.

A case supports transfer when the reasoning can state:

- what exact claim is under consideration;
- what evidence supports or weakens that claim;
- what uncertainty remains;
- what finding-specific verification would change the claim status;
- why execution success alone is insufficient.

Do not require all uncertainty to disappear before a bounded claim can be warranted.

## 12. Authority transfer check

Keep evidence sufficiency and authority separate.

Examples include:

- enough evidence to justify an experiment, but no authority to consume the required compute budget;
- technically usable data, but unresolved license/privacy/ethics authority;
- a supported internal claim, but no collaborator or project-owner authority to publish it externally;
- a result worth preserving, but no authority to release model artifacts or checkpoints.

A case fails this check if the reasoning treats technical plausibility or empirical support as automatic permission to act or publish.

## 13. Decision versus orchestration transfer check

Path 3's bounded result is carried forward as a hypothesis to test, not as guaranteed truth in the new domain.

For each case ask:

- which responsibility must be selected through evidence-grounded judgment;
- which experiment/run/validation steps can be mechanically coordinated after that responsibility is selected;
- what execution evidence must return to the decision layer;
- whether a deterministic failure, timeout, or completed run is being allowed to choose a materially different research responsibility by itself.

A scheduler may coordinate an already-authorized run. Its existence does not by itself warrant the experiment or the next scientific responsibility.

## 14. Cross-case support signals

Transfer is supported when the frozen cases repeatedly show that:

- decision-changing uncertainty can be expressed naturally without repository-specific vocabulary;
- responsibility selection remains evidence- and authority-dependent;
- evidence-bounded claims remain meaningful with stochastic evidence;
- verification remains claim-specific rather than synonymous with successful execution;
- stopping and escalation remain meaningful controls;
- action/publication authority stays separate from evidence sufficiency;
- decision and orchestration remain separable;
- software objects are unnecessary to preserve the control relation.

## 15. Weakening and falsification signals

Record limitations or falsification when cases repeatedly show that:

- software-specific lifecycle assumptions must be reintroduced for the reasoning to work;
- a candidate control concept changes meaning so materially that continuity is only verbal;
- AI-research decisions require a different top-level relation among evidence, uncertainty, action, and verification;
- stochastic evidence cannot be handled without rewriting the control model rather than only changing domain verification semantics;
- authority cannot remain separate from evidence sufficiency;
- responsibility boundaries are forced or arbitrary;
- decision/orchestration separation becomes incoherent under experiment execution;
- the evaluator relies on analogy rather than the actual research decision;
- expressing the cases requires new generic/domain-pack/runtime machinery.

## 16. Bounded dispositions

Conclude exactly one:

- `TRANSFER_COHERENT`
- `TRANSFER_LIMITED`
- `TRANSFER_INCOHERENT`

### `TRANSFER_COHERENT`

The candidate control concepts survive the bounded case set without material contradiction after domain semantics are replaced. This is limited evidence of conceptual transfer only.

### `TRANSFER_LIMITED`

The control relation remains useful across much of the case set, but one or more candidate concepts require material qualification, become ambiguous, or depend on domain structure more strongly than the current domain-general framing suggests.

### `TRANSFER_INCOHERENT`

The supposed shared control relation repeatedly depends on software semantics, requires contradictory reinterpretation, or fails to explain consequential AI-research decisions without being materially rewritten.

## 17. Mandatory limitations for any synthesis

Every final synthesis must state explicitly whether the cases were synthetic.

If synthetic, include this exact disclosure:

> **This was a bounded synthetic AI-research transfer exercise. Real-world AI-research effectiveness, prevalence, cross-agent reproducibility, organizational fit, and production readiness outside software engineering were not tested.**

Even a positive result remains research evidence only.

## 18. Non-goals and machinery boundary

This protocol does **not** authorize:

- a generic Sensemaking Core package;
- domain-pack/plugin infrastructure;
- an AI-research Skill suite;
- automatic domain detection or routing;
- a generic responsibility/evidence/authority schema;
- changing the current software-engineering product positioning;
- Workflow-v0 or workflow-registry behavior changes;
- a scheduler, queue, worker manager, persistence service, DAG runtime, or retry framework;
- an experiment campaign merely to exercise existing infrastructure;
- treating a transfer result as canonical proof of domain generality.

The machinery-promotion rule remains:

`repeated useful responsibility + stable semantics + repeated manual burden/error + mechanically expressible boundary -> candidate formalization`

A coherent conceptual transfer result alone satisfies none of those promotion requirements.

## 19. Execution order

1. Integrate this protocol before case construction.
2. Construct exactly 8 transfer cases without answers.
3. Freeze the case-input artifact on a dedicated branch/PR.
4. Integrate the frozen case set before evaluation.
5. Evaluate all 8 cases against this protocol without changing the inputs.
6. Perform cross-case comparison.
7. Record exactly one bounded disposition.
8. Validate the exact results head.
9. Stop at an unmerged results PR for owner integration.
10. Close Issue #214 only after the final synthesis is separately integrated.

No campaign approval is required for this research-only conceptual transfer exercise.

## 20. Definition of done

Path 4 is complete only when:

- this protocol is canonical on `main`;
- exactly 8 AI-research transfer cases are frozen before evaluation;
- at least two frozen cases resist clean software analogy;
- every case receives the full worked record;
- software leakage and forced analogy are explicitly audited;
- stochastic evidence and claim-specific verification are exercised;
- authority separation and decision/orchestration transfer are exercised;
- exactly one bounded disposition is recorded;
- synthetic-vs-real-world limitations are explicit;
- no generic/domain-pack machinery is promoted from the study alone;
- the final results PR is separately integrated by owner decision.
