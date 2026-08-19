# Path 4 — Frozen AI-Research Transfer Cases

**Status:** frozen synthetic input set / not yet evaluated  
**Authority:** research input only; not an ADR, product contract, schema, Skill, workflow, runtime specification, or product-positioning change  
**Tracker:** Issue #214  
**Protocol:** `docs/research/domain-general-control-transfer.md`  
**Freeze baseline:** `main@0c8536ca1f3d7c71b65c7d762c9b81baea2671ac`  
**Transfer domain:** AI research  
**Case count:** exactly 8

## 1. Freeze declaration

This file contains the complete Path 4 case inputs that must be frozen before evaluation.

The cases are **synthetic AI-research situations**. They are intended to test conceptual transfer of the control relation under materially different domain semantics. They are not records of real AI-research projects, and they do not establish real-world effectiveness.

The input set deliberately contains:

- no preferred responsibility;
- no preferred evidence-gathering order;
- no transfer disposition;
- no evaluator rationale;
- no numeric control score or ranking;
- no software-engineering analogy;
- no claim that any candidate control concept is domain-general.

Evaluation must use the canonical Path 4 protocol without editing these frozen inputs.

## 2. Anti-analogy stress designation

At least two cases must deliberately resist a clean software-engineering analogy.

The designated anti-analogy stress cases are:

- **P4-C05**, where scientific support is stochastic, seed-distributed, and claim-specific rather than a deterministic pass/fail state;
- **P4-C07**, where technical feasibility is separated from data-use, privacy, ethics, and collaborator authority that cannot be reduced to a technical validation event.

This designation supplies no preferred answer. It only identifies cases whose domain facts must be reasoned about on their own terms.

---

## P4-C01 — Conflicting literature before hypothesis commitment

**Family:** literature-to-hypothesis responsibility

### Research goal

Determine whether a proposed retrieval-aware calibration method is worth a focused empirical study for a biomedical question-answering benchmark.

### Current state

The team has a draft hypothesis that retrieval-aware calibration improves uncertainty estimates when supporting passages are partially missing.

Two recent papers appear relevant:

- Paper A reports a sizable calibration improvement from a closely related method on two biomedical QA datasets.
- Paper B reports that most of the apparent improvement disappears after constructing contamination-controlled splits and separating retrieval quality from calibration quality.

The draft hypothesis was written before Paper B was found.

### Contemplated consequential decision

Choose the next research responsibility before committing substantial effort to the proposed empirical study.

### Known evidence

- Paper A reports gains on datasets that overlap with widely used pretraining corpora.
- Paper B uses a smaller but explicitly contamination-controlled evaluation and reports mixed effects.
- The team has access to one public biomedical QA dataset and a separate retrieval corpus.
- No team experiment has yet been run for the proposed method.
- A small literature or dataset-provenance investigation would consume little compute.

### Live unresolved uncertainties

- Whether the mechanism claimed by Paper A remains plausible once contamination and retrieval-quality confounds are separated.
- Whether the available local dataset can support a contamination-aware evaluation without constructing a new benchmark.
- Whether the proposed hypothesis is materially distinct from the negative result in Paper B.

### Plausible next responsibilities

- reconcile the conflicting literature and dataset assumptions;
- design and execute a small empirical pilot;
- reformulate or narrow the hypothesis before experimentation;
- stop pursuing this hypothesis and redirect attention elsewhere.

### Resource / authority facts

The project lead has delegated authority for literature review and up to 50 GPU-hours of exploratory work. Larger compute use or external release requires separate approval.

### Verification target

No scientific claim has yet been authorized. Any later claim would need to distinguish calibration effects from retrieval quality and contamination.

### Explicit domain constraint

Published empirical findings are evidence with differing experimental assumptions; neither paper is treated as canonical state merely because it is newer or more positive.

---

## P4-C02 — Published baseline cannot be reproduced

**Family:** baseline reproduction boundary

### Research goal

Evaluate a proposed architectural change against a published sequence-model baseline before claiming an improvement.

### Current state

The published paper reports a validation score of 71.4. The team reimplemented the baseline from the paper and public code but obtains a mean near 66.8 across five seeds.

The public code omits the exact preprocessing cache used for the paper, and the released checkpoint was trained under an older library stack.

### Contemplated consequential decision

Decide whether to begin testing the novel architectural change, continue diagnosing the baseline reproduction gap, or redefine the comparison target.

### Known evidence

- Five local baseline runs cluster between 65.9 and 67.5.
- The paper reports one headline score plus a small standard deviation but does not publish per-seed outputs.
- A released checkpoint evaluated locally scores 70.8 after minor compatibility fixes.
- Reproducing the paper's preprocessing exactly is currently impossible because an intermediate data artifact was not released.
- The novel architecture code is ready to run.

### Live unresolved uncertainties

- How much of the reproduction gap comes from preprocessing rather than model implementation.
- Whether the released checkpoint is a valid substitute for reproducing training from scratch.
- Whether a fair comparison can be made using the locally reproducible baseline instead of the paper's headline number.

### Plausible next responsibilities

- diagnose the baseline/environment mismatch;
- define a bounded reproducible comparison protocol using available artifacts;
- run the novel architecture against the local baseline;
- contact the original authors for missing preprocessing details;
- defer the comparison claim.

### Resource / authority facts

The team can run ordinary experiments within its existing compute allocation. Contacting external authors is allowed. Publicly claiming reproduction failure requires project-lead review.

### Verification target

Any future improvement claim must identify the comparison baseline and uncertainty induced by the unresolved reproduction gap.

### Explicit domain constraint

A successfully completed training run does not by itself establish that the published baseline was reproduced.

---

## P4-C03 — Competing experiment responsibilities after a subgroup failure

**Family:** competing experiment responsibilities

### Research goal

Improve a multilingual classifier while preserving performance on a low-resource language subgroup.

### Current state

A new model trained with additional synthetic data improves the aggregate validation score but degrades the low-resource subgroup by roughly six points.

Three observations are simultaneously plausible explanations:

- the synthetic-data generator may shift label semantics for the subgroup;
- the subgroup validation labels may contain annotation inconsistencies;
- the new architecture may trade subgroup robustness for aggregate performance.

### Contemplated consequential decision

Choose the next research responsibility before spending the remaining experiment budget.

### Known evidence

- Aggregate performance improves across four seeds.
- The subgroup degradation appears in all four seeds but varies in magnitude.
- A manual inspection of 20 subgroup examples found several questionable labels but is too small to estimate prevalence.
- Training without synthetic data has not yet been repeated under the new architecture.
- Additional human annotation is possible but requires coordination with a language expert.

### Live unresolved uncertainties

- Whether the measurement surface is reliable enough to interpret the subgroup degradation.
- Whether the synthetic-data intervention or the architecture is the dominant cause.
- Whether collecting more subgroup data would clarify the mechanism or merely increase sample size around a mismeasured target.

### Plausible next responsibilities

- audit subgroup measurement and annotation quality;
- perform a targeted synthetic-data ablation;
- collect additional subgroup examples;
- modify the architecture;
- narrow the research goal to aggregate performance and explicitly abandon the subgroup requirement.

### Resource / authority facts

The remaining compute budget allows either several small ablations or one substantial architecture sweep. New human annotation requires approval from the language-data owner.

### Verification target

Any claim of improved multilingual robustness must account for the subgroup effect rather than relying only on the aggregate score.

### Explicit domain constraint

Several live uncertainties may remain simultaneously decision-changing; the case does not assume that one must always be resolved in isolation.

---

## P4-C04 — Expensive compute commitment with incomplete authority

**Family:** resource / irreversibility authority

### Research goal

Test whether scaling a sparse multimodal model produces a predicted capability transition at a substantially larger training budget.

### Current state

Small-scale runs match the predicted scaling trend. The proposed next run would use 8 H100-class GPUs for approximately 12 days through a shared external allocation.

The lab has technical access credentials for the cluster, but the allocation is jointly owned by two projects.

### Contemplated consequential decision

Decide whether the large run should be launched now, preceded by additional evidence work, reduced in scope, or escalated for authority.

### Known evidence

- Three smaller runs lie close to the predicted scaling curve.
- The largest existing run is still more than an order of magnitude smaller than the proposed run.
- A cheap diagnostic run could test one suspected data-loading bottleneck but would not validate the scaling hypothesis.
- The shared allocation has enough remaining capacity for the proposed run, but consuming it would materially reduce the other project's options.
- No explicit approval for this specific large run is recorded.

### Live unresolved uncertainties

- Whether the small-scale trend extrapolates to the proposed scale.
- Whether a known data-loading bottleneck will become significant at the larger scale.
- Whether the project has authority to consume the shared allocation for this experiment.

### Plausible next responsibilities

- run the large experiment;
- execute a smaller diagnostic or intermediate-scale experiment;
- request explicit allocation approval;
- redesign the experiment to reduce resource commitment;
- stop or defer the scale-up.

### Resource / authority facts

Technical capability to submit the job exists. Budget/allocation authority for this use does not automatically follow from technical access.

### Verification target

A completed large run could produce evidence about scaling behavior, but it would not retroactively establish that the resource commitment was authorized.

### Explicit domain constraint

Resource authority is a live constraint even when the scientific rationale for an experiment is technically plausible.

---

## P4-C05 — Surprising positive result with stochastic evidence

**Family:** positive-result claim verification  
**Anti-analogy stress case:** yes

### Research goal

Assess whether a new training intervention genuinely improves reasoning accuracy on a held-out benchmark.

### Current state

An initial experiment reports a four-point mean improvement over the baseline across three seeds. The result is larger than expected from prior pilot work.

Per-seed differences are uneven: one seed shows a very large gain, while the other two show smaller gains. A separate diagnostic metric also improved, but it was chosen after viewing the headline result.

### Contemplated consequential decision

Decide what research responsibility should follow before making or circulating a strong improvement claim.

### Known evidence

- Three intervention runs and three matched baseline runs are complete.
- The headline benchmark was specified before the runs.
- One benchmark subset is known to contain near-duplicate problem templates.
- No data contamination audit has been performed for this intervention.
- The intervention changes both optimization and data ordering, so the causal mechanism is not isolated.
- Additional matched seeds and targeted subset analyses are affordable.

### Live unresolved uncertainties

- Whether the observed mean improvement is robust across seed variation.
- Whether duplicate-template structure or contamination contributes materially to the gain.
- Whether the gain is attributable to the intended intervention mechanism or to correlated training changes.
- How narrow the claim must remain if the mechanism is not isolated.

### Plausible next responsibilities

- run additional matched seeds;
- perform a targeted contamination / duplicate-template analysis;
- isolate the intervention through an ablation;
- preserve a narrow descriptive result without a causal claim;
- stop investigating and circulate the current result internally.

### Resource / authority facts

The team may run additional experiments within budget. External publication of a strong claim requires senior-researcher approval after claim verification.

### Verification target

Verification is claim-specific and may require a distribution of evidence across runs and targeted analyses rather than a single binary acceptance event.

### Explicit domain constraint

There is no single canonical run whose success deterministically closes the scientific uncertainty. Evidence remains stochastic and claim-scoped.

---

## P4-C06 — Negative replication evidence and continuation pressure

**Family:** replication / negative-result stopping

### Research goal

Determine whether a previously reported interpretability intervention reliably changes a model behavior under the team's current experimental conditions.

### Current state

The original internal study reported a positive effect in one model family. Three new replications on a newer model family show effects near zero, with confidence intervals spanning small positive and negative values.

A researcher proposes running ten more variants because the original effect was theoretically compelling.

### Contemplated consequential decision

Decide whether to continue replication, narrow or reformulate the claim, investigate a model-family interaction, or stop the line of work.

### Known evidence

- The original positive study used one model family and two seeds.
- Three new preregistered replications on a newer family do not reproduce the effect.
- The implementation has passed independent code review for fidelity to the preregistered protocol.
- A small architecture difference between the model families could plausibly moderate the effect.
- Ten additional variants would consume most of the remaining project compute budget.

### Live unresolved uncertainties

- Whether the original effect was model-family-specific.
- Whether additional variants are likely to discriminate a real interaction from ordinary noise.
- Whether the existing negative evidence is already sufficient to narrow or stop the broader claim.

### Plausible next responsibilities

- stop and report the bounded negative replication;
- design a focused model-family interaction test;
- run the proposed broad variant sweep;
- re-examine the theoretical claim before more computation;
- preserve the original result only as model-specific evidence.

### Resource / authority facts

The researcher may spend a small remaining allocation without approval. Consuming most of the project budget requires the project lead's authorization.

### Verification target

A closure claim must distinguish failure to replicate the broad effect from evidence that the effect is impossible under every model family.

### Explicit domain constraint

Absence of a replicated effect may justify stopping or narrowing without proving a universal negative.

---

## P4-C07 — Technically usable dataset with unresolved provenance and ethics authority

**Family:** data / ethics / provenance authority  
**Anti-analogy stress case:** yes

### Research goal

Train a clinical-language model for an internal study of de-identification robustness.

### Current state

A collaborator has shared a large corpus of de-identified clinical notes. The files are technically readable and sufficient for the planned training run.

The accompanying documentation says the corpus may be used for the collaborator's approved research program, but it does not clearly state whether derivative model training by the receiving team is covered. A subset was originally collected under an older consent process.

### Contemplated consequential decision

Decide whether model training may proceed, whether the data-use scope must first be clarified, whether a restricted subset should be used, or whether the study should be redesigned around another dataset.

### Known evidence

- Automated checks find no obvious direct identifiers in a sample.
- The collaborator confirms the transfer was intentional.
- The data-use agreement available to the receiving team is ambiguous about derivative model artifacts.
- The institutional privacy contact has not reviewed the planned training use.
- An alternative public dataset exists but differs substantially in clinical distribution.

### Live unresolved uncertainties

- Whether the existing authorization covers model training and derivative checkpoints.
- Whether the older-consent subset requires additional review or exclusion.
- Whether de-identification quality is sufficient for the intended risk profile.
- Whether switching datasets would invalidate the research question or only change its scope.

### Plausible next responsibilities

- proceed with model training;
- request data-use/privacy/ethics clarification;
- exclude the ambiguous subset and continue on a reduced corpus;
- redesign the study around the public dataset;
- stop the planned study.

### Resource / authority facts

The team has compute access and technical possession of the data. Technical access does not itself establish permission to use the data, train derivative models, retain checkpoints, or publish findings.

### Verification target

Technical validation of de-identification is relevant evidence but is not the sole authority condition for data use or derivative artifact creation.

### Explicit domain constraint

The controlling boundary includes provenance, consent, privacy, ethics, and collaborator authority; no single technical status is defined as authoritative for all of them.

---

## P4-C08 — Supported internal result without publication authority

**Family:** publication / release authority

### Research goal

Decide how to communicate a completed internal study of a new model-evaluation method.

### Current state

The study has a preregistered primary analysis, a successful internal replication by a second researcher, and a bounded result supporting the primary descriptive claim.

The work was conducted under a collaboration agreement that gives an external partner 30 days to review public disclosures. The partner has not yet completed review. The evaluated model checkpoint is also licensed for internal research only.

### Contemplated consequential decision

Decide what can be claimed or released now and what must wait for additional authority.

### Known evidence

- The primary descriptive result replicated internally.
- Secondary exploratory analyses are mixed.
- The methods and aggregate metrics can be described without distributing the checkpoint.
- The collaboration agreement requires prepublication review.
- The checkpoint license prohibits public redistribution.
- Internal archival of the result is permitted.

### Live unresolved uncertainties

- Whether the external partner will approve the planned public wording.
- Whether a public methods-only report can avoid disclosing restricted information.
- Whether secondary exploratory analyses should be included in the bounded claim.

### Plausible next responsibilities

- archive the supported internal claim and wait for review;
- request publication approval with a bounded draft;
- prepare a methods-only public artifact that excludes restricted materials;
- publish the full result immediately;
- narrow the claim before seeking approval.

### Resource / authority facts

The research team has authority to preserve internal evidence and prepare drafts. External publication and checkpoint release are separately governed.

### Verification target

Scientific support for the bounded descriptive claim and authority to publish or release artifacts are distinct questions.

### Explicit domain constraint

A result can be technically and scientifically supportable for internal use while external publication or artifact release remains unauthorized.

---

## 3. Freeze integrity requirements

Evaluation must treat P4-C01 through P4-C08 as immutable inputs.

The evaluator may use the canonical Path 4 protocol and the relationships explicitly stated in these cases, but must not revise the case facts to make the control model fit.

For every case, the worked record must separately identify:

- control relation;
- AI-research domain semantics;
- software leakage, if any;
- forced analogy, if any;
- claim-specific verification;
- authority boundary;
- decision versus orchestration boundary;
- control-concept outcome.

The final synthesis must use exactly one bounded disposition:

- `TRANSFER_COHERENT`
- `TRANSFER_LIMITED`
- `TRANSFER_INCOHERENT`

No disposition is encoded in this frozen input artifact.
