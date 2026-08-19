# Path 4 — Domain-General Control Transfer Results

**Status:** completed bounded synthetic transfer synthesis / proposed research disposition  
**Authority:** research evidence only; not an ADR, product contract, schema, Skill, workflow, runtime specification, generic-core proposal, domain-pack proposal, or product-positioning change  
**Tracker:** Issue #214  
**Protocol:** `docs/research/domain-general-control-transfer.md`  
**Frozen inputs:** `docs/research/path-4-ai-research-transfer-cases.md`  
**Analysis baseline:** `main@b43823449fb488d1208abc3cf7b8ddecb196cdb1`  
**Case count:** 8 / 8  
**Proposed bounded disposition:** `TRANSFER_COHERENT`

## 1. Research question

> **Within a bounded AI-research transfer exercise, can the current Sensemaking control policy remain internally coherent when software-engineering-specific responsibilities, evidence types, verification semantics, and authority boundaries are replaced by AI-research equivalents, without importing repository-specific assumptions into the control layer or inventing generic framework machinery?**

The eight synthetic case inputs were frozen and integrated before these worked records were written.

The transfer exercise held the following candidate control relation under test:

`goal/current state -> live decision-changing uncertainty -> evidence responsibility -> updated warrant -> responsibility/action/stop -> outcome evidence -> verification/claim/continuation`

It did not assume that this relation was already domain-general.

## 2. Summary result

Across all eight frozen cases, the control relation remained intelligible and decision-constraining after the surrounding software-engineering semantics were replaced with AI-research semantics.

Four observations did most of the explanatory work:

1. **Decision-changing uncertainty transferred without repository vocabulary.** Literature conflict, baseline comparability, measurement validity, stochastic variation, data-use authority, and publication authority could each be identified by whether a credible alternative answer would change the next research responsibility, claim scope, resource commitment, stop/continue decision, or authority boundary.
2. **Evidence-bounded claims survived stochastic evidence.** The cases did not require deterministic pass/fail closure. A claim could be narrowed to what current multi-run, replication, provenance, or targeted-analysis evidence actually supported while preserving unresolved uncertainty.
3. **Evidence sufficiency and authority remained separate.** Compute access, data possession, empirical support, and internal replication did not automatically authorize resource consumption, data use, derivative artifacts, external publication, or model release.
4. **Decision and orchestration remained separable.** Once a research responsibility and authority envelope were selected, run scheduling, seed execution, artifact capture, analysis scripts, and other stable mechanics could be coordinated deterministically. Their completion or failure did not by itself choose a materially different scientific responsibility.

No case required a repository, canonical branch, issue, pull request, merge operation, deterministic CI result, or generic domain/runtime framework in order for the reasoning to remain coherent.

The strongest bounded conclusion is therefore:

> **Across the eight frozen synthetic AI-research transfer cases studied, the current control concepts can be applied coherently after replacing software-engineering-specific responsibility, evidence, verification, and authority semantics, providing limited evidence that the control principle may transfer beyond software engineering.**

This is conceptual transfer evidence only. It does not establish a domain-general product or justify generic/domain-pack machinery.

---

## 3. Case records

## P4-C01 — Conflicting literature before hypothesis commitment

### 1. AI-research goal/current state

The team wants to decide whether retrieval-aware calibration merits a focused biomedical-QA study. The draft hypothesis predates conflicting contamination-controlled evidence.

### 2. Contemplated consequential decision

Whether to commit to a pilot, first reconcile the literature/data assumptions, narrow the hypothesis, or stop pursuing it.

### 3. Live decision-changing uncertainties

- whether Paper A's proposed mechanism remains plausible after contamination and retrieval-quality confounds are separated;
- whether the available dataset can support a contamination-aware test;
- whether the local hypothesis is materially distinct from Paper B's negative result.

### 4. Gating / non-gating reasoning

The literature/mechanism question is gating because a credible negative answer can eliminate or materially narrow the proposed empirical responsibility before meaningful compute is spent. The precise final publication form is non-gating at this stage because no external claim is yet being made.

### 5. Selected responsibility

**Reconcile the conflicting literature and dataset assumptions before committing to the full pilot.**

### 6. Plausible competing responsibility

A small empirical pilot is plausible because up to 50 GPU-hours are already authorized and direct local evidence could be informative.

### 7. First evidence-producing responsibility

Perform a bounded literature-and-dataset-provenance reconciliation focused on contamination controls, retrieval-quality separation, and whether the local hypothesis adds a distinguishable mechanism.

### 8. Expected decision effect

The evidence can warrant proceeding with a targeted pilot, narrowing the hypothesis and verification target, or stopping the line before compute is committed.

### 9. Evidence-bounded claim available now

The literature contains conflicting evidence under materially different contamination and retrieval assumptions; the proposed local mechanism remains unresolved. No empirical improvement claim is warranted.

### 10. Verification / closure evidence

If the hypothesis survives reconciliation, finding-specific verification would require a contamination-aware empirical design that separates retrieval quality from calibration quality.

### 11. Authority

Literature review and a small exploratory pilot are delegated. Larger compute use and external release remain separately authorized.

### 12. Decision / orchestration boundary

Search, paper extraction, provenance checks, and later run mechanics may be coordinated mechanically after the research responsibility is selected. A literature-search pipeline cannot decide by itself that the hypothesis is worth pursuing.

### 13. Software leakage detected

**None material.** The reasoning depends on scientific literature and dataset assumptions, not repository state.

### 14. Forced analogy detected

**None.** No paper is treated as a branch head or canonical state.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

A cheap pilot could be run in parallel with literature work without violating the control relation if its decision value is explicit. The record selects reconciliation first because the conflicting mechanism evidence can invalidate the larger experimental responsibility at low cost.

---

## P4-C02 — Published baseline cannot be reproduced

### 1. AI-research goal/current state

The team wants a defensible comparison for a new architecture, but its baseline reimplementation remains materially below the paper's headline score while the released checkpoint performs closer to it.

### 2. Contemplated consequential decision

Whether to launch novel-model experiments, continue reproduction diagnosis, define a bounded local comparison protocol, contact the authors, or defer the comparison claim.

### 3. Live decision-changing uncertainties

- source of the training-from-scratch reproduction gap;
- validity of using the released checkpoint as the comparison anchor;
- whether the locally reproducible baseline is a fair target for a new improvement claim.

### 4. Gating / non-gating reasoning

Comparison validity is gating for any claim against the published baseline. Exact reconstruction of every missing historical artifact is not necessarily gating if a transparent, reproducible alternative comparison target can be justified.

### 5. Selected responsibility

**Define and verify a bounded reproducible comparison protocol while diagnosing the highest-value baseline mismatch.**

### 6. Plausible competing responsibility

Run the novel architecture immediately against the local 66.8 baseline and state the comparison narrowly.

### 7. First evidence-producing responsibility

Compare the released checkpoint, available preprocessing variants, and local training pipeline under one explicitly documented evaluation surface; contact the authors for the missing preprocessing artifact if that could change the comparison decision.

### 8. Expected decision effect

Evidence can determine whether the study should compare against the released checkpoint, the local reproducible baseline, both with qualification, or defer a published-baseline comparison entirely.

### 9. Evidence-bounded claim available now

The team's available training-from-scratch pipeline does not reproduce the paper's headline score, while the released checkpoint approaches it. This does **not** establish that the paper is irreproducible.

### 10. Verification / closure evidence

A claim about architectural improvement needs matched evaluation against a clearly identified baseline with the unresolved reproduction limitation carried into claim scope.

### 11. Authority

Routine experiments and author contact are allowed. Publicly characterizing the published work as a reproduction failure requires project-lead review.

### 12. Decision / orchestration boundary

Repeated runs, environment setup, and metric collection can be orchestrated. Choosing what counts as a scientifically fair comparison remains an evidence-grounded decision.

### 13. Software leakage detected

**No control-layer leakage.** Code and library versions are domain evidence in this AI-research case, but the reasoning does not depend on a repository lifecycle or merge state.

### 14. Forced analogy detected

**None.** Reproduction is not treated as equivalent to a deterministic regression test.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

The case cannot guarantee a unique comparison target because the missing preprocessing artifact may remain unavailable. The control relation handles this by bounding the claim rather than requiring total uncertainty elimination.

---

## P4-C03 — Competing experiment responsibilities after a subgroup failure

### 1. AI-research goal/current state

Aggregate classifier performance improved, but the required low-resource subgroup degraded across all four seeds and the measurement labels show signs of inconsistency.

### 2. Contemplated consequential decision

Whether to audit measurement, ablate synthetic data, collect more data, change the architecture, or abandon the subgroup requirement.

### 3. Live decision-changing uncertainties

- whether subgroup measurement is reliable enough to interpret the observed degradation;
- whether synthetic-data semantics or architecture is the dominant cause;
- whether more data would clarify the mechanism or merely amplify a bad measurement surface.

### 4. Gating / non-gating reasoning

Measurement validity is the nearest gating dependency because causal ablations and architecture changes cannot be interpreted cleanly if the target labels are materially unreliable. The exact eventual architecture is non-gating until that measurement boundary is clearer.

### 5. Selected responsibility

**Audit subgroup measurement and annotation quality before the larger architecture sweep.**

### 6. Plausible competing responsibility

A targeted synthetic-data ablation is also credible because the degradation appears across seeds and directly tests one suspected intervention.

### 7. First evidence-producing responsibility

Conduct a bounded, expert-reviewed annotation audit sufficient to determine whether the subgroup metric is decision-usable; if it is, proceed to the targeted synthetic-data ablation.

### 8. Expected decision effect

The audit can preserve the current subgroup target, redefine its measurement, require new labels, or make causal ablation interpretable. It can also show that the apparent six-point degradation is partly a measurement artifact.

### 9. Evidence-bounded claim available now

The new configuration improves the aggregate metric but does not currently support a claim of improved multilingual robustness because a required subgroup worsens on the existing measurement surface.

### 10. Verification / closure evidence

A robustness claim requires a trusted subgroup evaluation plus evidence that the chosen intervention does not materially sacrifice the subgroup under that evaluation.

### 11. Authority

Additional human annotation requires approval from the language-data owner; the remaining compute allocation is constrained.

### 12. Decision / orchestration boundary

Annotation sampling, experiment launching, and metric aggregation can be orchestrated after responsibilities are selected. A workflow should not automatically launch an architecture sweep merely because the aggregate metric is positive.

### 13. Software leakage detected

**None material.**

### 14. Forced analogy detected

**None.** The measurement surface is treated as a scientific construct, not a test suite whose green/red state is self-interpreting.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

Measurement audit and a cheap ablation could be jointly useful. The qualitative choice is intentionally not represented as a numeric ranking; the audit is selected because it conditions interpretation of several downstream experimental options.

---

## P4-C04 — Expensive compute commitment with incomplete authority

### 1. AI-research goal/current state

Small runs support a scaling trend, but the proposed 8-GPU, 12-day experiment would consume a material share of a jointly owned external allocation.

### 2. Contemplated consequential decision

Whether to launch, run a cheaper diagnostic/intermediate study, request authority, redesign the experiment, or defer.

### 3. Live decision-changing uncertainties

- extrapolation of the scaling trend;
- whether the data-loading bottleneck becomes important at scale;
- whether this project is authorized to consume the shared allocation.

### 4. Gating / non-gating reasoning

Allocation authority is a hard gating dependency for the large run. The scaling and bottleneck uncertainties affect scientific warrant and experiment design but cannot override absent authority.

### 5. Selected responsibility

**Request explicit allocation authority while preserving the scientific decision package; do not launch the large run yet.**

### 6. Plausible competing responsibility

Run a smaller diagnostic or intermediate-scale experiment within existing delegated resources before escalating.

### 7. First evidence-producing responsibility

Produce the bounded approval package: current scaling evidence, resource cost, opportunity cost to the other project, and any cheap diagnostic evidence that materially changes the requested run.

### 8. Expected decision effect

The allocation owners can authorize the run, authorize a reduced envelope, defer it, or reject the commitment. Scientific evidence can separately change the requested design.

### 9. Evidence-bounded claim available now

The observed small-scale runs are consistent with the predicted trend over the tested range. They do not establish the proposed large-scale transition.

### 10. Verification / closure evidence

The scaling claim requires outcome evidence from appropriately scaled experiments; authorization evidence is separate and must precede the resource commitment.

### 11. Authority

Technical cluster access exists. Shared-allocation authority for this specific run does not.

### 12. Decision / orchestration boundary

A scheduler may coordinate an approved job and capture its artifacts. It cannot convert credentials or idle capacity into authority to consume jointly owned resources.

### 13. Software leakage detected

**None.**

### 14. Forced analogy detected

**None.** Resource authorization is treated directly as project governance, not as a merge or deployment permission analogy.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

A small diagnostic may be warranted independently and could occur before approval if it lies within delegated authority. It does not remove the large-run authority boundary.

---

## P4-C05 — Surprising positive result with stochastic evidence

### 1. AI-research goal/current state

Three matched seeds show a surprising four-point mean improvement, but the effect is uneven, possible duplicate-template/contamination concerns remain, and the intervention changes more than one causal factor.

### 2. Contemplated consequential decision

What verification responsibility should occur before making or circulating a strong improvement or causal claim.

### 3. Live decision-changing uncertainties

- seed robustness of the observed gain;
- contribution of duplicate-template structure or contamination;
- causal attribution between optimization and data ordering;
- defensible scope of the claim if the mechanism remains unresolved.

### 4. Gating / non-gating reasoning

Robustness and contamination are gating for a strong general improvement claim. Mechanism isolation is additionally gating for a causal claim but not necessarily for a narrow descriptive claim about the tested configuration.

### 5. Selected responsibility

**Perform claim-specific verification rather than treating the completed runs as closure.**

The bounded verification responsibility includes additional matched seeds plus a targeted contamination/duplicate-template analysis. A mechanism ablation is required only if the intended claim is causal.

### 6. Plausible competing responsibility

Preserve and circulate only a narrow descriptive internal result now, explicitly withholding a general or causal claim.

### 7. First evidence-producing responsibility

Run the preregistered verification package: additional matched seeds and targeted duplicate-template/contamination analysis on the headline benchmark.

### 8. Expected decision effect

The resulting distribution can strengthen the bounded improvement claim, narrow it to specific subsets/configurations, or make the apparent gain unpersuasive. A later ablation can separately govern causal attribution.

### 9. Evidence-bounded claim available now

Across the initial three matched seeds, the tested intervention configuration has a higher observed mean on the prespecified headline benchmark. The current evidence does not yet warrant a robust general improvement claim or a causal mechanism claim.

### 10. Verification / closure evidence

Verification is distributional and claim-specific: additional matched runs, contamination-sensitive subset analysis, and—only for causal language—an intervention-isolating ablation.

### 11. Authority

Additional verification runs are within budget. External publication of a strong claim requires senior-researcher approval after verification.

### 12. Decision / orchestration boundary

Seed scheduling, run execution, artifact capture, and prespecified analyses can be orchestrated. The number or completion state of runs does not by itself determine claim scope or the next research responsibility.

### 13. Software leakage detected

**None.** This anti-analogy case remains coherent without deterministic test or canonical-artifact semantics.

### 14. Forced analogy detected

**A tempting analogy was explicitly rejected:** treating the metric threshold or a completed run as a green test would distort stochastic scientific evidence.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

No finite seed count creates universal certainty. The control model does not require that; it requires claim scope to track the evidence and remaining uncertainty.

---

## P4-C06 — Negative replication evidence and continuation pressure

### 1. AI-research goal/current state

Three preregistered replications in a newer model family fail to reproduce an earlier positive effect; a broad ten-variant sweep is proposed despite limited remaining compute.

### 2. Contemplated consequential decision

Whether to stop, narrow the claim, test a specific model-family interaction, run the broad sweep, or revisit the theory.

### 3. Live decision-changing uncertainties

- whether the original effect is model-family-specific;
- whether more variants would discriminate a real interaction from noise;
- whether the current negative evidence is already sufficient to narrow the broad claim.

### 4. Gating / non-gating reasoning

The broad claim is already materially weakened by preregistered negative replication. The model-family interaction remains live only if a focused test could change whether the original result should be preserved as a narrower family-specific claim. Generic desire for more information is non-gating.

### 5. Selected responsibility

**Narrow the current claim and, only if the interaction hypothesis is sufficiently specific, design a focused model-family interaction test rather than the broad ten-variant sweep.**

### 6. Plausible competing responsibility

Stop additional experiments and report the bounded negative replication immediately.

### 7. First evidence-producing responsibility

Before further compute, specify what observable model-family interaction would distinguish a real moderator from ordinary noise. If no focused discriminating test can be stated, stop.

### 8. Expected decision effect

A focused interaction result can preserve a narrower model-family-specific hypothesis or support stopping. Failure to define such a test prevents broad information gathering from masquerading as decision value.

### 9. Evidence-bounded claim available now

The earlier effect did not replicate in three preregistered runs on the newer model family under the tested protocol. This does not establish a universal negative across all model families.

### 10. Verification / closure evidence

Closure of the broad claim can rely on the bounded negative replication plus explicit scope. A narrower interaction claim would require a prespecified moderator test and appropriate replication.

### 11. Authority

Small follow-up work is delegated; consuming most of the remaining project compute requires project-lead approval.

### 12. Decision / orchestration boundary

A run manager can execute an authorized focused experiment. It must not infer from a negative result that ten new variants are automatically warranted.

### 13. Software leakage detected

**None material.** Independent code review is evidence of implementation fidelity, not the authority that interprets the scientific result.

### 14. Forced analogy detected

**None.** Failed replication is not treated as a failed regression test proving impossibility.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

The evidence supports either stopping or one focused moderator test depending on theoretical specificity. The control relation preserves this ambiguity rather than converting uncertainty into an automatic retry policy.

---

## P4-C07 — Technically usable dataset with unresolved provenance and ethics authority

### 1. AI-research goal/current state

The team technically possesses de-identified clinical notes sufficient for training, but derivative-model permission, old-consent coverage, and privacy/ethics review remain unresolved.

### 2. Contemplated consequential decision

Whether to train now, obtain data-use/privacy/ethics clarification, exclude a subset, redesign around a public dataset, or stop.

### 3. Live decision-changing uncertainties

- authorization for derivative model training/checkpoints;
- status of the older-consent subset;
- sufficiency of de-identification for the intended risk profile;
- whether an alternative dataset preserves the research question.

### 4. Gating / non-gating reasoning

Data-use/ethics authority is gating for training on the transferred corpus. A sample de-identification check is relevant risk evidence but is not a substitute for permission. The exact final model architecture is non-gating until lawful/authorized data use is established.

### 5. Selected responsibility

**Request explicit data-use, privacy, ethics, and collaborator-scope clarification before training on the ambiguous corpus.**

### 6. Plausible competing responsibility

Exclude the ambiguous older-consent subset and continue on the remainder if an authorized reviewer confirms that the reduced corpus is covered.

### 7. First evidence-producing responsibility

Assemble the data-use facts for the responsible authority: agreement text, intended derivative artifacts, provenance of the older subset, de-identification evidence, retention plan, and publication/release intent.

### 8. Expected decision effect

The authority review can permit the intended study, impose subset/artifact restrictions, require additional safeguards, redirect the study to public data, or stop the use entirely.

### 9. Evidence-bounded claim available now

Automated sampling found no obvious direct identifiers in the inspected subset, and the collaborator intentionally transferred the data. Neither fact establishes permission for derivative model training or publication.

### 10. Verification / closure evidence

Technical privacy evidence remains relevant to risk assessment, while authorization closure requires the applicable data-use/privacy/ethics decision. These evidence classes are complementary rather than interchangeable.

### 11. Authority

Compute access and physical possession do not grant data-use, derivative-model, retention, or publication authority. Multiple governance actors may legitimately constrain the action.

### 12. Decision / orchestration boundary

Automated de-identification scans, access controls, and later training can be orchestrated. A data pipeline cannot transform technical readability or successful privacy scanning into legal/ethical authority.

### 13. Software leakage detected

**None.** This anti-analogy case remains coherent with plural, non-technical authority and without a single canonical technical status.

### 14. Forced analogy detected

**A tempting analogy was explicitly rejected:** treating a de-identification check as equivalent to a green validation gate that authorizes use would collapse distinct authority semantics.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

The responsible authority may be plural and organization-specific. The transfer claim does not require a universal authority schema; it requires evidence sufficiency and permission to remain distinguishable.

---

## P4-C08 — Supported internal result without publication authority

### 1. AI-research goal/current state

A preregistered primary result has replicated internally, but partner prepublication review is pending and the underlying checkpoint cannot be publicly redistributed.

### 2. Contemplated consequential decision

What can be claimed, archived, prepared, published, or released now.

### 3. Live decision-changing uncertainties

- partner approval of public wording;
- whether a methods-only artifact avoids restricted disclosure;
- whether mixed exploratory analyses belong in the bounded public claim.

### 4. Gating / non-gating reasoning

The partner review is gating for external publication under the collaboration agreement. It is not gating for preserving the supported internal result. Checkpoint-license restrictions independently gate artifact release.

### 5. Selected responsibility

**Preserve the supported bounded internal claim and prepare a constrained publication package for required partner review; do not release the checkpoint.**

### 6. Plausible competing responsibility

Prepare a methods-only public artifact that excludes restricted material, but only if the agreement permits that disclosure without bypassing review.

### 7. First evidence-producing responsibility

Submit a bounded draft and release plan to the partner review process, explicitly separating primary replicated findings, mixed exploratory analyses, and restricted checkpoint material.

### 8. Expected decision effect

Review can authorize publication as drafted, require narrower wording, allow methods-only disclosure, delay release, or prohibit particular artifacts.

### 9. Evidence-bounded claim available now

The preregistered primary descriptive result is supported for internal use by the original study plus an independent internal replication. Mixed exploratory analyses do not inherit that support.

### 10. Verification / closure evidence

The primary claim is scientifically verified to the bounded internal standard by preregistration and internal replication. Publication/release closure additionally requires partner and license authority.

### 11. Authority

The team may archive evidence and prepare drafts. External publication and checkpoint redistribution are separately governed.

### 12. Decision / orchestration boundary

Draft assembly, artifact redaction, and submission workflows may be orchestrated. A completed scientific analysis or successful internal replication cannot automatically trigger external publication.

### 13. Software leakage detected

**None.**

### 14. Forced analogy detected

**A merge/publication analogy is unnecessary and would be misleading.** Publication is governed by collaboration and license terms, not by a canonical code-integration state.

### 15. Control-concept outcome

**`survives naturally`**

### 16. Ambiguity / caveats

A methods-only disclosure may be independently permissible, but the supplied facts do not establish that. The bounded decision is therefore to preserve the internal claim and use the actual publication authority process.

---

## 4. Cross-case comparison

| Case | Primary transfer pressure | Selected responsibility | Claim/evidence behavior | Authority separation | Decision/orchestration | Outcome |
|---|---|---|---|---|---|---|
| P4-C01 | conflicting literature / hypothesis liveness | literature + dataset reconciliation | no premature empirical claim | small work delegated; release separate | searches/runs coordinate after selection | survives naturally |
| P4-C02 | incomplete reproduction / comparability | bounded comparison protocol + diagnosis | local non-reproduction != universal irreproducibility | public reproduction claim reviewed | runs coordinate; comparison target is judgment | survives naturally |
| P4-C03 | competing causal + measurement uncertainty | measurement audit first | aggregate gain cannot support robustness claim | annotation authority separate | experiments coordinate after target validity | survives naturally |
| P4-C04 | expensive irreversible resource use | obtain allocation authority | small-scale trend remains bounded | credentials != budget authority | scheduler executes only authorized run | survives naturally |
| P4-C05 | stochastic surprising positive result | claim-specific verification | distributional, contamination-sensitive claim scope | publication authority separate | run completion != scientific closure | survives naturally |
| P4-C06 | negative replication / stopping | narrow + focused moderator test or stop | bounded negative != universal negative | major compute requires lead | no automatic retry/sweep | survives naturally |
| P4-C07 | data provenance / privacy / ethics | obtain data-use authority | technical privacy evidence != permission | plural governance authority | pipeline cannot authorize use | survives naturally |
| P4-C08 | publication / release boundary | preserve internal claim + seek review | internal scientific support != external release | partner/license authority separate | analysis completion != publish trigger | survives naturally |

### 4.1 Decision-changing uncertainty

All eight cases identified uncertainties by their effect on a consequential decision rather than by whether they were merely interesting:

- pursue / narrow / stop a hypothesis;
- choose a comparison target;
- repair measurement before causal experimentation;
- spend scarce compute;
- strengthen or narrow a scientific claim;
- continue or stop replication;
- use restricted data;
- publish or release evidence/artifacts.

This required no repository-specific object.

### 4.2 Evidence-bounded claims under stochastic evidence

P4-C05 and P4-C06 are the strongest anti-deterministic controls. Neither needs a binary pass/fail interpretation:

- a positive three-seed result can warrant a narrow descriptive observation while leaving robustness and causal attribution unresolved;
- a failed replication can warrant narrowing or stopping a broad claim without proving a universal negative.

The control concept therefore survived by changing **domain verification semantics**, not by changing the top-level relation between evidence, uncertainty, warrant, and claim scope.

### 4.3 Authority

Authority remained separable from technical evidence in materially different forms:

- shared compute allocation (P4-C04);
- data-use/privacy/ethics and collaborator scope (P4-C07);
- partner publication review and artifact license (P4-C08).

The concept did not require authority to reduce to a single owner, token, branch permission, or publication state.

### 4.4 Decision versus orchestration

Across all cases, stable mechanics could be coordinated after responsibility selection:

- paper/data extraction;
- repeated experiment execution;
- seed scheduling;
- metric aggregation;
- artifact capture;
- privacy scanning;
- draft assembly and submission.

But deterministic completion/failure of those mechanics did not gain authority to select a materially different research responsibility.

This is consistent with the bounded Path 3 distinction while using AI-research semantics rather than software-engineering workflow semantics.

### 4.5 Software leakage and forced analogy

No case required repository, branch, PR, merge, or CI semantics to preserve the control relation.

Some cases naturally contained software artifacts—code, library stacks, automation, checkpoints—but those were **evidence or execution tools inside AI research**, not control primitives.

The strongest rejected forced analogies were:

- P4-C05: metric/run success is not a deterministic green test;
- P4-C07: de-identification scanning is not an authority-granting validation gate;
- P4-C08: publication is not a merge operation.

The reasoning was clearer when those analogies were avoided.

## 5. Falsification / weakening review

### Software-specific lifecycle assumptions required?

**No material instance observed.**

### Candidate concepts materially changed meaning?

**No material rewrite observed.** `verification` became stochastic/replication-aware and `authority` became plural/governance-specific, but those are domain semantics already permitted by the candidate concepts rather than contradictory redefinitions.

### Different top-level control relation required?

**No.** The cases remained explainable as evidence changing uncertainty/warrant, which changes responsibility/action/stop/claim within authority boundaries.

### Stochastic evidence incompatible with evidence-bounded claims?

**No.** P4-C05 and P4-C06 explicitly exercised non-binary evidence.

### Evidence sufficiency conflated with authority?

**No.** P4-C04, P4-C07, and P4-C08 made the separation especially consequential.

### Responsibility boundaries forced or arbitrary?

**No material contradiction observed.** P4-C03 and P4-C06 retained genuine competing options and caveats rather than claiming objective unique rankings.

### Decision/orchestration separation incoherent?

**No.** Mechanically stable execution remained useful after responsibility selection without gaining scientific decision authority.

### Generic/domain-pack/runtime machinery required?

**No.** The entire study was expressed as research records using existing repository evidence mechanics.

## 6. Bounded disposition

**`TRANSFER_COHERENT`**

Reason:

> Across the eight frozen synthetic AI-research transfer cases, the candidate control concepts remained internally coherent after software-engineering-specific responsibility, evidence, verification, and authority semantics were replaced. The cases could identify decision-changing uncertainty, select bounded research responsibilities, scope scientific claims to stochastic evidence, preserve stopping/escalation, separate evidence from action/publication authority, and preserve the decision/orchestration boundary without importing repository lifecycle concepts or inventing generic framework machinery.

This is a **bounded conceptual result**, not proof that the product or control model is universally domain-general.

## 7. Limitations

1. **Synthetic construction.** The cases were deliberately designed to exercise the protocol and may be more legible than ordinary research work.
2. **Same-context evaluator/design bias.** The cases were frozen before evaluation, preventing answer-driven input edits, but case construction and evaluation occurred within the same broader agent context rather than independent evaluators.
3. **One transfer domain.** AI research is materially different from repository-centered engineering but remains technically adjacent to software engineering; more distant domains were not tested.
4. **No real organizational dynamics.** Budget, ethics, collaborator, and publication authority were represented as case facts rather than observed institutional processes.
5. **No empirical scientific execution.** No literature review, model training, replication, statistical analysis, privacy review, or publication process was actually performed for these synthetic cases.
6. **No cross-agent reproducibility.** Another agent/model/context was not tested on the frozen cases.
7. **No prevalence evidence.** The exercise does not show how often these control pressures occur in real AI-research practice.
8. **No machinery evidence.** Conceptual coherence does not establish stable schemas, recurring manual burden, or a mechanically expressible cross-domain interface.

> **This was a bounded synthetic AI-research transfer exercise. Real-world AI-research effectiveness, prevalence, cross-agent reproducibility, organizational fit, and production readiness outside software engineering were not tested.**

## 8. Product and machinery boundary

This result does **not** warrant:

- a generic Sensemaking Core package;
- domain-pack/plugin infrastructure;
- an AI-research Skill suite;
- a generic responsibility/evidence/authority schema;
- automatic domain detection or routing;
- workflow-registry or runtime changes;
- a scheduler, queue, worker manager, persistence service, DAG runtime, or retry framework;
- changing current product positioning away from software engineering.

The machinery-promotion rule remains unchanged:

`repeated useful responsibility + stable semantics + repeated manual burden/error + mechanically expressible boundary -> candidate formalization`

The present study supplies conceptual transfer evidence, not the repeated real-use evidence required by that rule.

## 9. Research handoff

Path 4 can close at the bounded `TRANSFER_COHERENT` level if this result is integrated.

The productive next move is **not** to genericize the architecture. Instead:

- retain the domain-general control interpretation as a research hypothesis;
- continue dogfooding the software-engineering product in normal use;
- preserve future cross-domain episodes when they arise naturally;
- revisit domain specialization or a generic core only if repeated real use demonstrates stable semantics and concrete manual burden/error.

No new experiment campaign is required merely to exercise existing campaign infrastructure.
