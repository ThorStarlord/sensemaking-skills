# Phase 9 Pilot C — repair-verifier + output-reconciler

**Pilot status:** Completed on pinned repository/Skill evidence  
**Source Skills:** `skills/repair-verifier/`, `skills/output-reconciler/`  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Pinned target ref:** `8109b0a7133abb8363f808d01292f5f7375d766f`  
**Purpose:** Test the Reasoning Model after work has occurred, where the central question is whether evidence warrants a claim about outcome/repair rather than what should be done next.

## Question under test

Do the common semantic fields from Pilots A/B remain useful for post-change verification and reconciliation, and what is the smallest mechanical contract that can be extracted without letting validators decide semantic success?

## Before alignment

Both Skills already had strong evidence habits:

- `repair-verifier` re-runs the deterministic probe and distinguishes `closed` from `remaining` findings;
- `output-reconciler` treats a work summary as an auditable artifact rather than trusted prose;
- `output-reconciler` compares like-for-like before attributing a failure to the claimed change;
- both preserve explicit dispositions instead of silently discarding unresolved findings.

Two semantic overreach risks remained:

1. `repair-verifier` said structural and direction-evidence closure together **prove the reconciliation worked**, which could be read more broadly than the checks' actual coverage.
2. `output-reconciler` used `verified` in a way that could be mistaken for universal truth rather than support for a bounded claim under a specific baseline/currentness/scope.

## Competency questions exercised

- CQ-CUR-3 — What exact post-change state is being verified?
- CQ-EVI-3 — Does the evidence support the same baseline/check/scope as the claim?
- CQ-EPI-2 — What does `verified` or `closed` establish, and what remains a semantic inference?
- CQ-CHG-1 — Did the repository change?
- CQ-CHG-2 — Did the original finding stop reproducing?
- CQ-CHG-3 — Did the intended outcome actually occur?
- CQ-CHG-4 — What evidence would justify calling the work a repair?
- CQ-UNC-3 — Which outcome remains unresolved because the verification scope is narrower than the success condition?
- CQ-HOF-2 — Can a later agent see what was checked versus merely claimed?

## Observed reasoning seams

### Seam A — Change versus Outcome versus Repair

The shared model makes the post-change ladder explicit:

```text
OBSERVED: repository state changed
OBSERVED: fresh probe produced result R
DERIVED: original finding F no longer reproduces under check C
INFERRED: bounded structural condition addressed by F is resolved
UNRESOLVED: broader runtime/user success condition was not exercised
```

This prevents `changed` or `PASS` from collapsing into `repair succeeded`.

### Seam B — Domain classifications versus epistemic status

The existing artifact enums remain useful and should not be replaced:

```text
repair-verifier: closed | remaining
output-reconciler: verified | disputed | omitted
```

The general epistemic vocabulary answers a different question: how is the underlying claim warranted?

For example:

```text
classification: verified
epistemic basis: OBSERVED + DERIVED under pinned scope
limit: external integration not checked
```

### Seam C — Like-for-like is part of claim warrant

A comparison is meaningful only when baseline, method, scope/configuration, claimed change, and post-change target are aligned. A narrower PASS cannot support a broader claim merely because both use the word `validation`.

## Alignment applied

`repair-verifier` now:

- removes the over-broad `prove the reconciliation worked` language;
- distinguishes non-reproduction from semantic repair success;
- requires post-change currentness and like-for-like checks;
- requires explicit verification limits where the success condition is broader than the probe.

`output-reconciler` now:

- defines `verified` as support within the audited claim/baseline/scope;
- makes currentness explicit;
- treats over-broad claims as disputable even when a narrower check passes;
- preserves uncertainty and untested surfaces;
- keeps the existing artifact enum while mapping its evidentiary basis to shared epistemic concepts.

Both Skills gain bounded semantic-alignment references. Their canonical artifact schemas remain unchanged.

## Invalid inference jumps prevented

1. `repository changed -> repair succeeded`.
2. `fresh structural check passes -> all intended outcomes achieved`.
3. `finding no longer reproduces under one probe -> every manifestation of the problem is resolved`.
4. `claim classified verified -> claim is universally true`.
5. `validator accepts reconciliation report -> work claim is semantically correct`.
6. `candidate fails check X -> candidate introduced failure X` without a like-for-like baseline.

## Cross-pilot comparison

Stable across all three pilots:

```text
1. target/currentness boundary
2. observations or inherited observations
3. material claims
4. epistemic status
5. evidence references
6. bounded scope / claim limits
7. decision-relevant uncertainty
8. explicit limits / non-claims
```

Not stable enough for the common core:

```text
fog type
weakness type
Component / Layer / Boundary / Contract
decision enum
repair closed/remaining enum
reconciliation verified/disputed/omitted enum
specific capability selection
Campaign transition shape
```

Those remain domain/Skill contracts.

## Coordination overhead

Low-to-moderate. The post-change Skills already had explicit claims/evidence and dispositions. Most alignment consists of narrowing over-broad language and preserving verification scope rather than adding new output fields.

## Level-3 extraction decision

**WARRANTED, but only as an experimental comparison/validation contract.**

Three contrasting pilots reuse a stable mechanical representation for:

```text
target/currentness
observations
claims + epistemic-status enum + evidence-ref shape
uncertainties
explicit limits
```

The repository may therefore add a standalone `semantic_reasoning_profile` validator that checks representation only. It must not:

- validate semantic truth;
- rank uncertainties;
- select responsibilities/capabilities;
- decide architectural violations;
- decide repair success;
- enter Campaign admission routing automatically.

This is the smallest useful Level-3 extraction supported by Phase 9 evidence.

## Phase 10 decision

Phase 10 begins as a **bounded experiment**, not a universal artifact migration. The common profile remains a companion to canonical Skill artifacts. Future evidence must show whether shared artifact-semantic fields should be embedded in domain artifacts or remain an external reasoning/audit profile.

## Result

**Phase 9's three-pilot gate is satisfied for the experimental common profile.** The Reasoning Model is now operationalized in pre-diagnosis, architecture-decision, and post-change verification/reconciliation contexts without centralizing semantic control.

## Explicit limits

- No native external coding-agent harness was used for these semantic-alignment pilots.
- The pilots establish cross-Skill representation utility, not improved benchmark/task success.
- No Campaign schema change is warranted by this evidence alone.
- No Repository Semantic Map is warranted yet; the pilots did not demonstrate repeated expensive reconstruction of the same full entity graph.
