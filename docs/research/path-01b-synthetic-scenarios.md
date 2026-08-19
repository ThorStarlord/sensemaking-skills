# Path 01b Synthetic Stress Suite — Frozen Inputs

**Status:** frozen candidate scenario inputs; not evaluated  
**Tracker:** Issue #204  
**Protocol:** `docs/research/competing-live-uncertainties.md`  
**Protocol baseline:** `main@57d7d82cbb267c5f1c03b5ff87e7b885a83aee80`  
**Synthetic:** true

## Execution boundary

These scenarios are deliberately constructed research inputs. They are not normal-use evidence and cannot establish real-world prevalence or effectiveness.

For every evaluated pass:

- expose exactly one scenario block below, plus the coding-agent output contract from the canonical Path 01b protocol;
- do not expose another scenario's answer;
- do not expose evaluator notes, transformation relationships, or intended stress properties before the answer;
- require exactly one top-level selection: `A first`, `B first`, or `act now / investigate neither`;
- require prospective qualitative reasoning and an explicit statement that no numeric score, weight, or pseudo-point system was used.

The scenario IDs are opaque execution identifiers. Their ordering does not imply a preferred selection.

---

## SCLU-001

### Goal

Decide whether to authorize a production hotfix for an API request-normalization defect before the next scheduled deployment window.

### Authorized scope and authority boundary

The coding agent may inspect repository evidence and propose the next evidence-producing responsibility. It may not deploy, merge, or change the external API contract. Release authorization belongs to the repository owner.

### Contemplated consequential decision

Whether the current hotfix candidate is sufficiently warranted to move to owner release review.

### Supplied evidence

- A reproducible malformed request reaches a normalization branch that has a recently edited condition.
- A focused unit reproduction can be run or inspected cheaply and would establish whether that condition actually causes the observed malformed request.
- The same normalization branch also affects a billing-relevant request field. Existing tests cover common billing inputs but not the malformed shape in the report.
- A broader billing-semantics investigation would take materially longer but could reveal whether changing the condition would alter accepted billing behavior for another class of callers.
- The proposed hotfix is small, but release is externally visible and rollback would require another deployment.

### Candidate live uncertainties

**A.** Is the recently edited normalization condition actually the cause of the reported malformed request?

Credible alternatives:
- yes — the focused reproduction fails through that exact condition;
- no — another normalization step causes the malformed request.

**B.** Would changing that condition alter billing-relevant behavior for callers not represented by the focused reproduction?

Credible alternatives:
- yes — the hotfix would change accepted billing semantics for another caller class;
- no — the behavior is isolated to the malformed-input defect.

### Why either could reasonably be selected first

A is cheap and could invalidate the hotfix entirely. B has greater wrong-action exposure because an incorrect assumption could ship externally visible billing behavior.

---

## SCLU-002

### Goal

Decide whether a compatibility patch for a shared serialization helper should proceed toward merge review.

### Authorized scope and authority boundary

The coding agent may inspect this repository and its documented ownership boundaries. It may propose a patch or escalation, but it may not change a separately owned upstream contract or merge without owner authorization.

### Contemplated consequential decision

Whether this repository should carry and merge the compatibility change.

### Supplied evidence

- A downstream test failure appears when the shared helper receives a newly introduced upstream field.
- Repository history shows that this helper has historically normalized upstream payload differences.
- A recent architecture note says new semantic fields should normally be handled at the upstream boundary rather than silently normalized downstream.
- The upstream repository lists another team as owner of the semantic contract, but this repository owns backward-compatibility behavior for existing consumers.
- A local compatibility patch would be straightforward if this repository still owns that responsibility.

### Candidate live uncertainties

**A.** Does the failing behavior still fall inside this repository's compatibility responsibility, or did the architecture change move that responsibility upstream?

Credible alternatives:
- this repository still owns backward-compatible normalization;
- the architecture change moved this semantic responsibility upstream.

**B.** Even if a local compatibility change is technically appropriate, does the current maintainer have authority to encode behavior that may redefine an upstream-owned semantic field?

Credible alternatives:
- yes — compatibility ownership includes this bounded interpretation;
- no — upstream owner confirmation is required before encoding the semantic meaning.

### Why either could reasonably be selected first

A sits earlier in the responsibility warrant. B may independently block action because it changes who is entitled to define the behavior.

---

## SCLU-003

### Goal

Decide whether to replace a cache invalidation path that is causing intermittent stale reads.

### Authorized scope and authority boundary

The coding agent may inspect and modify the repository on a review branch, but may not deploy or alter the service-level consistency contract without owner approval.

### Contemplated consequential decision

Whether to proceed with a cache-path rewrite or first narrow the responsibility further.

### Supplied evidence

- Stale reads occur only for requests crossing two service boundaries.
- A feature flag can route a small cohort around the suspect cache path without changing persisted data; disabling the flag is immediate.
- A separate design note is ambiguous about whether the cross-service reads require strong consistency or only bounded staleness.
- If strong consistency applies, the rewrite likely expands beyond the local cache into invalidation signals across services.
- If bounded staleness applies, the reversible feature-flag path could provide enough operational evidence to avoid a broad rewrite.

### Candidate live uncertainties

**A.** Can the reversible feature-flag route isolate the suspect cache path closely enough to preserve options while gathering evidence?

Credible alternatives:
- yes — the flag isolates the path and gives a safe discriminating probe;
- no — the flag changes too many request characteristics to isolate the cause.

**B.** Does the consistency requirement for these cross-service reads demand strong consistency rather than bounded staleness?

Credible alternatives:
- strong consistency applies and the responsibility expands materially;
- bounded staleness is acceptable and the local responsibility remains plausible.

### Why either could reasonably be selected first

A strongly preserves options and is reversible. B has larger decision branching because its answer may redirect the entire solution scope.

---

## SCLU-004

### Goal

Decide what evidence to gather first before replacing a flaky integration-test harness.

### Authorized scope and authority boundary

The coding agent may inspect tests, CI configuration, and harness code. It may propose changes on a review branch but may not disable required CI checks.

### Contemplated consequential decision

Whether the harness itself should be replaced or whether the flakiness belongs to the execution environment.

### Supplied evidence

- Failures cluster around parallel test execution but appear on two different operating systems.
- The harness has one known race-prone shared temporary-directory helper.
- CI telemetry also shows occasional filesystem latency spikes during the same jobs.
- A harness-focused probe and an environment-focused probe have similar expected effort and similar reversibility.
- Either answer could redirect the next implementation responsibility; neither path changes external authority.

### Candidate live uncertainties

**A.** Is the harness's shared temporary-directory helper the dominant cause of the flakiness?

Credible alternatives:
- yes — parallel test races explain the observed failures;
- no — the helper is incidental and the failures remain after isolation.

**B.** Are CI filesystem latency spikes sufficient to explain the observed flakiness without replacing the harness?

Credible alternatives:
- yes — environment behavior explains the failures;
- no — latency is correlated but not causal.

### Why either could reasonably be selected first

Both uncertainties have credible evidence, similar evidence cost, similar reversibility, and comparable decision effect. The supplied evidence does not intentionally privilege one as decisive.

---

## SCLU-005

### Goal

Decide how to reconcile a documentation/runtime contradiction before editing either source.

### Authorized scope and authority boundary

The coding agent may inspect canonical documentation and implementation and prepare a reviewable reconciliation. It may not change public API semantics without owner approval.

### Contemplated consequential decision

Whether documentation should change to match implementation, implementation should change to match documentation, or the contradiction should be escalated.

### Supplied evidence

- One canonical guide says a field is optional.
- The current implementation rejects requests without that field.
- A release note from the same release is ambiguous and does not resolve which source is intended authority.
- Checking the exact implementation history for when rejection became active is one short repository read.
- Checking the exact guide history for when optionality was asserted is another short repository read.
- Both reads are cheap, non-mutating, and can be completed before any edit; arguing extensively about which read comes first would cost at least as much as performing both.

### Candidate live uncertainties

**A.** Did implementation intentionally tighten the field requirement in a later canonical change?

Credible alternatives:
- yes — implementation represents an intentional newer contract;
- no — the rejection is accidental or unsupported.

**B.** Did the guide intentionally preserve optionality after the implementation change?

Credible alternatives:
- yes — documentation reflects the intended contract and implementation drifted;
- no — the guide is stale relative to canonical implementation decisions.

### Why either could reasonably be selected first

Either check is cheap and decision-changing, while the metareasoning required to establish a strict ordering may exceed the cost of immediately inspecting both pieces of evidence.

---

## SCLU-006

### Goal

Decide whether to make a small reversible refactor now or investigate two adjacent uncertainties first.

### Authorized scope and authority boundary

The coding agent may make a review-branch refactor that does not alter behavior or public API. Merge remains owner-controlled.

### Contemplated consequential decision

Whether to rename a misleading private local variable and update its directly associated comment now.

### Supplied evidence

- The variable is private to one function and its current name incorrectly suggests milliseconds although the value is seconds.
- The planned edit changes only the local variable name and its adjacent comment; tests and public interfaces are unaffected.
- There is an open design discussion about whether the surrounding helper might be renamed in a future cleanup.
- There is also a minor style question about whether the adjacent comment should eventually be removed in favor of a clearer helper name.
- Neither unresolved discussion changes the correctness of the current seconds-vs-milliseconds naming mismatch.
- The refactor is cheap, reversible, and independently reviewable.

### Candidate live uncertainties

**A.** Will the surrounding helper likely be renamed in the future cleanup?

Credible alternatives:
- yes — a later rename may touch the same line again;
- no — the helper name may remain stable.

**B.** Should the adjacent explanatory comment eventually be removed rather than maintained?

Credible alternatives:
- yes — future naming cleanup could make it redundant;
- no — the comment may remain useful even after cleanup.

### Why either could reasonably be selected first

Both are real unresolved questions, but neither obviously gates the cheap reversible correction currently contemplated.

---

## SCLU-007

### Goal

Decide whether a reported regression can be closed as fixed on canonical `main`.

### Authorized scope and authority boundary

The coding agent may inspect repository history, tests, and current validation evidence. It may recommend closure but may not close the tracker without owner authorization.

### Contemplated consequential decision

Whether evidence warrants the claim that the original regression is fixed on canonical `main`.

### Supplied evidence

- A broad audit of the module could inspect dozens of related behaviors and produce substantial additional information.
- The original regression report contains one exact failing input and expected output.
- A merged change claims to address the defect, and generic module CI is green.
- No finding-specific verification of that exact input on canonical `main` is currently recorded.
- The broad audit would be much more expensive than checking the exact original input.

### Candidate live uncertainties

**A.** Are there any other latent defects in the surrounding module that a broad audit would reveal?

Credible alternatives:
- yes — additional defects may exist;
- no — no additional defects are found.

**B.** Does the exact originally failing input now produce the expected output on canonical `main`?

Credible alternatives:
- yes — finding-specific evidence supports the closure claim;
- no — the original regression remains live despite generic green CI.

### Why either could reasonably be selected first

A promises much more information about the module. B is far narrower but directly determines whether the specific closure claim is warranted.

---

## SCLU-008

### Goal

Decide whether a package release candidate may proceed to the externally visible publication step.

### Authorized scope and authority boundary

The coding agent may inspect release metadata and recommend the next evidence-producing step. It may not publish the package or create an external release without owner authorization.

### Contemplated consequential decision

Whether the release candidate is sufficiently warranted to request owner publication approval.

### Supplied evidence

- The package version in the built metadata can be compared cheaply against the release tag and the exact source commit.
- A previous release once published an artifact from the wrong commit and required a corrective release.
- There is also a recently reported moderate performance regression in an optional feature path.
- Investigating the performance report would take substantially longer; current evidence does not show data loss, security impact, or API incompatibility.
- Publication is externally visible and cannot be undone; a later version can supersede it, but the published artifact remains available.

### Candidate live uncertainties

**A.** Does the release artifact's version/provenance exactly match the intended tag and source commit?

Credible alternatives:
- yes — provenance is correct;
- no — the candidate was built from the wrong version or source.

**B.** Is the reported optional-path performance regression severe enough that publication should be delayed?

Credible alternatives:
- yes — the regression crosses the release's acceptable performance boundary;
- no — it is real but does not block this release.

### Why either could reasonably be selected first

A is cheap and sits immediately before an irreversible publication boundary. B could still change the release decision but requires materially more investigation.

---

## SCLU-009

### Goal

Decide whether to authorize a production hotfix for an API request-normalization defect before the next scheduled deployment window.

### Authorized scope and authority boundary

The coding agent may inspect repository evidence and propose the next evidence-producing responsibility. It may not deploy, merge, or change the external API contract. Release authorization belongs to the repository owner.

### Contemplated consequential decision

Whether the current hotfix candidate is sufficiently warranted to move to owner release review.

### Supplied evidence

- A reproducible malformed request reaches a normalization branch that has a recently edited condition.
- A focused unit reproduction can be run or inspected cheaply and would establish whether that condition actually causes the observed malformed request.
- The same normalization branch also affects a billing-relevant request field. Existing tests cover common billing inputs but not the malformed shape in the report.
- A broader billing-semantics investigation would take materially longer but could reveal whether changing the condition would alter accepted billing behavior for another class of callers.
- The proposed hotfix is small, but release is externally visible and rollback would require another deployment.

### Candidate live uncertainties

**A.** Would changing the recently edited normalization condition alter billing-relevant behavior for callers not represented by the focused reproduction?

Credible alternatives:
- yes — the hotfix would change accepted billing semantics for another caller class;
- no — the behavior is isolated to the malformed-input defect.

**B.** Is that recently edited normalization condition actually the cause of the reported malformed request?

Credible alternatives:
- yes — the focused reproduction fails through that exact condition;
- no — another normalization step causes the malformed request.

### Why either could reasonably be selected first

One uncertainty is cheap and could invalidate the hotfix entirely. The other has greater wrong-action exposure because an incorrect assumption could ship externally visible billing behavior.

---

## SCLU-010

### Goal

Choose the next evidence step before deciding whether this repository should accept a patch that adapts to a new field emitted by a shared upstream serializer.

### Authorized scope and authority boundary

The coding agent may inspect this repository's ownership records and prepare a local review branch. It cannot redefine another team's upstream semantic contract or merge changes without owner approval.

### Contemplated consequential decision

Whether a local compatibility adaptation belongs in this repository and may proceed toward review.

### Supplied evidence

- Existing consumers fail after the upstream serializer starts emitting an additional semantic field.
- Historically, this repository has absorbed representational differences from upstream to protect existing consumers.
- A newer architecture decision says newly introduced semantic meaning should normally be resolved at the producer boundary rather than silently interpreted downstream.
- The producer repository is owned by another team; this repository still explicitly owns backward compatibility for its existing consumers.
- If local ownership remains valid, the compatibility code is simple.

### Candidate live uncertainties

**A.** Has the newer architecture decision shifted this specific semantic responsibility to the producer, despite this repository's legacy compatibility role?

Credible alternatives:
- yes — the responsibility moved upstream;
- no — bounded consumer compatibility remains local responsibility.

**B.** If a downstream compatibility adaptation is otherwise appropriate, is local maintainer authority sufficient to encode an interpretation of a field whose semantic contract belongs to the producer team?

Credible alternatives:
- yes — the compatibility mandate authorizes the bounded interpretation;
- no — producer-owner confirmation is required first.

### Why either could reasonably be selected first

One question determines whether the responsibility belongs here at all. The other can stop the work at an authority boundary even if the technical responsibility remains plausible.

---

## SCLU-011

### Goal

Decide whether to replace a cache invalidation path that is causing intermittent stale reads.

### Authorized scope and authority boundary

The coding agent may inspect and modify the repository on a review branch, but may not deploy or alter the service-level consistency contract without owner approval.

### Contemplated consequential decision

Whether to proceed with a cache-path rewrite or first narrow the responsibility further.

### Supplied evidence

- Stale reads occur only for requests crossing two service boundaries.
- A feature flag can route a small cohort around the suspect cache path without changing persisted data; disabling the flag is immediate.
- A separate design note is ambiguous about whether the cross-service reads require strong consistency or only bounded staleness.
- If strong consistency applies, the rewrite likely expands beyond the local cache into invalidation signals across services.
- If bounded staleness applies, the reversible feature-flag path could provide enough operational evidence to avoid a broad rewrite.
- Separately, the repository has an unresolved question about whether cache metric names should use singular or plural nouns. That naming question does not affect consistency semantics, stale-read causality, deployment authority, or the contemplated rewrite decision.

### Candidate live uncertainties

**A.** Can the reversible feature-flag route isolate the suspect cache path closely enough to preserve options while gathering evidence?

Credible alternatives:
- yes — the flag isolates the path and gives a safe discriminating probe;
- no — the flag changes too many request characteristics to isolate the cause.

**B.** Does the consistency requirement for these cross-service reads demand strong consistency rather than bounded staleness?

Credible alternatives:
- strong consistency applies and the responsibility expands materially;
- bounded staleness is acceptable and the local responsibility remains plausible.

### Additional unresolved context

**C.** Should cache metric names use singular or plural nouns?

Credible alternatives:
- singular naming is preferred;
- plural naming is preferred.

### Why either candidate could reasonably be selected first

A strongly preserves options and is reversible. B has larger decision branching because its answer may redirect the entire solution scope. The supplied context also contains another genuine unresolved repository question.

---

## SCLU-012

### Goal

Determine whether there is enough evidence to recommend closing a previously reported defect on the current canonical branch.

### Authorized scope and authority boundary

The coding agent may review history and validation evidence and recommend a tracker action. It cannot itself make the owner-level closure decision.

### Contemplated consequential decision

Whether the evidence supports saying that the specific reported defect is fixed on canonical `main`.

### Supplied evidence

- A comprehensive examination of the whole subsystem could surface many unrelated weaknesses and would generate much more information than a narrow check.
- The defect report preserves one precise input/output pair that previously failed.
- A merged patch says it fixes the defect, and the ordinary subsystem test suite currently passes.
- There is no durable record that the exact reported input/output pair was checked after the merge on canonical `main`.
- Replaying or inspecting that exact case is far cheaper than a subsystem-wide examination.

### Candidate live uncertainties

**A.** Does the wider subsystem contain additional defects that a comprehensive examination would uncover?

Credible alternatives:
- yes — additional problems exist;
- no — the examination finds none.

**B.** On canonical `main`, does the exact input from the original report now produce the expected result?

Credible alternatives:
- yes — the original finding has direct closure-relevant support;
- no — the original defect remains reproducible.

### Why either could reasonably be selected first

One path promises broad information about the subsystem. The other is narrowly tied to the specific claim being contemplated.
