# Semantic Architecture Implementation Plan

**Status:** Active architecture program; Phase 10 complete; first bounded Phase 15 conformance pilot qualified  
**Completed milestones:** semantic foundation; Phase 9 Reasoning Model operationalization; Phase 10 common-envelope experiment  
**Qualified incremental checks:** Phase 15 Skill-registry liveness conformance  
**Current frontier:** evidence-derived only — no later or additional phase package is automatically authorized  
**Implementation principle:** Formalize from demonstrated reasoning or maintenance pressure; do not manufacture runtime machinery to make the ontology look complete.

## Objective

Create a shared semantic foundation that lets Sensemaking Skills reason consistently about unfamiliar repositories while preserving evidence lineage, currentness, uncertainty, semantic authority, and the existing agent/deterministic control boundary.

The plan separates:

```text
documented vocabulary
-> ontology semantics
-> observed cross-Skill reuse or maintenance defect
-> bounded executable representation/check
-> possible later control-plane promotion
```

A later phase does not retroactively turn earlier documentation into runtime authority. Phase numbers are organizational labels, not automatic sequencing authority.

## Permanent promotion ladder

```text
observed vocabulary / maintenance need
        |
        v
Level 1: shared term
        |
        | repeated useful distinction
        v
Level 2: ontology entity/relation
        |
        | repeated cross-Skill burden or bounded consistency defect
        | stable semantics
        | mechanically expressible subset
        v
Level 3: executable semantic contract / conformance rule
```

### Level 1 -> Level 2 gate

Require:

- at least one competency question;
- repeated semantic use or critical boundary value;
- clear definition;
- no canonical duplicate;
- useful relations to existing concepts.

### Level 2 -> Level 3 gate

Require:

- evidence from at least two contrasting real workflow/Skill situations unless safety/integrity or a repeated repository-maintenance defect warrants a narrower earlier check;
- stable semantic meaning;
- identified mechanical subset;
- explicit validator scope;
- migration/backward-compatibility consideration when durable state is affected;
- negative/rejection cases;
- no transfer of semantic authority to deterministic machinery.

---

# Phase status map

| Phase | Name | Status |
|---:|---|---|
| 0 | Preserve architecture boundary | COMPLETE |
| 1 | Problem definition | COMPLETE |
| 2 | Competency questions | COMPLETE |
| 3 | Existing concept inventory/reconciliation | BASELINE COMPLETE; incremental |
| 4 | Layered ontology | COMPLETE at Level 2 |
| 5 | Relationship and epistemic model | COMPLETE at Level 2 |
| 6 | Reasoning architecture | COMPLETE at design level |
| 7 | Integration architecture | COMPLETE at design level |
| 8 | Reference scenarios | COMPLETE |
| 9 | Reasoning Model operationalization / Skill semantic-alignment pilots | COMPLETE for first three contrasting pilots |
| 10 | Common artifact-semantic envelope experiment | COMPLETE — Outcome A: optional companion profile |
| 11 | Mechanical semantic probes | DEFERRED pending repeated demand |
| 12 | Repository Semantic Map experiment | DEFERRED |
| 13 | Campaign/control-plane promotion | DEFERRED |
| 14 | Domain-pack extraction | DEFERRED |
| 15 | Ontology conformance/drift checks | INCREMENTAL — first bounded registry-liveness rule qualified; further rules evidence-gated |

---

# Phases 0–8 — Foundation

The foundation milestone established:

- `constitution.md` and the semantic-control boundary;
- `problem-statement.md`;
- 78 initial competency questions;
- `concept-inventory.md` reconciled with existing Campaign semantics;
- the six-layer Intent / Repository-System / Evidence / Knowledge / Work / Product ontology;
- `SoftwareCapability`, `SensemakingCapability`, and `ProductCapability` namespace separation;
- relationship/epistemic rules and prohibited inferences;
- the canonical staged Reasoning Model;
- execution-integration boundaries;
- 12 reference scenarios.

These remain documentation/ontology authority except where an existing executable product contract or a separately promoted Level-3 contract implements a mechanical subset.

---

# Phase 9 — Reasoning Model Operationalization & Skill Semantic-Alignment Pilots

**Status:** COMPLETE for the first three contrasting pilots.

## Goal

Test the Reasoning Model against real Skill contracts before creating broad common schemas.

## Pilot A — `repo-sensemaker`

Tested target/currentness semantics, observation versus inference, evidence-backed claims, contradiction/currentness handling, consequential uncertainty, absence/completeness, and explicit limits.

Result: the Skill already had strong evidence mechanics; the primary gain was explicit epistemic vocabulary and separation of fog/weakness classification from the specific decision-changing uncertainty.

Evidence: `pilots/pilot-a-repo-sensemaker.md` and `pilots/pilot-a-profile.yaml`.

## Pilot B — `architectural-review`

Tested inherited currentness/evidence, Component/Layer/Boundary/Contract/Dependency semantics, observed dependency versus inferred architectural violation, ratified/documented intent, and current defect versus proposal-contingent risk.

Result: the common warrant/provenance core transferred successfully even though the Skill inherits rather than re-collects repository evidence. Architecture-specific concepts remain local.

Evidence: `pilots/pilot-b-architectural-review.md` and `pilots/pilot-b-profile.yaml`.

## Pilot C — `repair-verifier` + `output-reconciler`

Tested Change versus Outcome versus Repair, fresh post-change currentness, like-for-like validation scope, changed != succeeded, local `closed/remaining` and `verified/disputed/omitted` enums, and explicit verification limits.

Result: the common core transferred into post-change reasoning. Over-broad `prove repair worked` and universal `verified` language was narrowed to the actual verification scope.

Evidence: `pilots/pilot-c-repair-reconciliation.md` and `pilots/pilot-c-profile.yaml`.

## Stable common core found

Across the Phase 9 pilots:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence refs
bounded scope / claim limits
uncertainty
explicit limits / non-claims
```

Not common-core concepts:

```text
fog/weakness taxonomies
Component/Layer/Boundary/Contract
domain verdict enums
repair closed/remaining
reconciliation verified/disputed/omitted
Campaign transition shape
```

## Phase 9 promotion decision

The repeated core warranted one **experimental Level-3 representation contract**: `semantic_reasoning_profile` v1.

The standalone validator may check representation shape, IDs, enums, evidence-ref requirements, currentness evidence presence, and explicit-limit presence. It may not judge semantic truth, evidence sufficiency, uncertainty priority, responsibility warrant, architectural correctness, repair success, or Campaign disposition.

The profile was intentionally not registered for Campaign admission.

---

# Phase 10 — Common Artifact-Semantic Envelope Experiment

**Status:** COMPLETE — repository-qualified Outcome A.

## Hypothesis tested

Several analytical workflows may benefit from a shared semantic envelope containing:

```text
target/currentness
observations
material claims
claim epistemic status
evidence refs
claim limits
uncertainties
explicit limits
```

Phase 10 tested the existing `semantic_reasoning_profile` as a companion artifact without modifying canonical domain artifact schemas.

## Experiment design

The experiment preregistered three contrasting real-repository episodes under `phase-10/`:

1. `repo-sensemaker` reasoning on Chess Mentor Engine — direct diagnosis/currentness.
2. `output-reconciler` reasoning on the React incremental game — exact-SHA handoff evidence plus independently mutable live PR metadata.
3. PM `pre-mortem` reasoning on ViralFactory — a canonical `risk_analysis` artifact compared directly with the companion semantic profile.

The decision rule allowed three outcomes:

```text
A. Keep as companion reasoning/audit profile.
B. Embed a smaller demonstrated subset into multiple analytical artifacts.
C. Narrow or retire it because duplication/overhead exceeds value.
```

Outcome B required at least two contrasting episodes to show the same missing decision-changing semantic field that their canonical domain artifacts did not already represent adequately.

## Phase 10 findings

### Cross-artifact reconstruction

The profile materially improved domain-neutral reconstruction. A fresh reader can recover target/currentness, observed facts, material interpretations, unresolved questions, and non-claims without first learning each domain artifact's local taxonomy.

### Currentness pressure

The React episode produced the strongest value signal. Immutable exact-SHA repository evidence and mutable live PR metadata had to be kept separate before a continuation decision could be trusted:

```text
immutable snapshot evidence
!=
live mutable metadata
```

That distinction was decision-relevant, but `output-reconciler` already models currentness locally.

### Duplication pressure

The ViralFactory episode produced the strongest negative embedding signal. The canonical PM `risk_analysis` already represents evidence status, evidence refs, observed versus hypothetical risk, uncertainty, mitigations, recommendation boundaries, and unresolved questions. Embedding the whole common profile would create a second representation of substantially the same semantics.

Chess Mentor Engine likewise already had strong claim-ceiling/evidence documentation; the profile mainly compressed and normalized it.

### Boilerplate and overhead

Mandatory use could encourage duplicate observations/claims/uncertainties merely to satisfy a second schema. Exact token cost was not instrumented, so Phase 10 makes no fake precision claim. Qualitatively, companion coordination cost is moderate and justified selectively, not universally.

### Validator boundary

No episode required deterministic semantic judgment. The existing validator remained representation-only and continued to emit:

```text
semantic_truth_established: false
```

The PM risk artifact continued to use its existing PM validator rather than a generic semantic replacement.

## Phase 10 decision — Outcome A

Keep `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**.

Use it when at least one of these conditions exists:

- reasoning spans multiple artifacts/surfaces with different currentness semantics;
- a fresh context needs a compact warrant/provenance index;
- an experiment/review compares reasoning across Skills or domains;
- local domain vocabulary makes cross-domain audit unnecessarily expensive.

Do not require it when a strong domain artifact already represents the decision-changing evidence/currentness/uncertainty/limits and no cross-artifact reconstruction need exists.

### Not promoted

Phase 10 does not authorize:

- Campaign admission of the profile;
- Campaign schema changes;
- a mandatory universal artifact envelope;
- Repository Semantic Map work;
- a central reasoning engine;
- automatic semantic routing/capability ranking.

See `phase-10/results.md` and `phase-10-handoff.md` for experiment and qualification evidence.

---

# Phase 11 — Mechanical Semantic Probes

**Status:** Deferred pending stable demand.

Potential mechanical relations include:

```text
TargetSnapshot identity
file containment
language-level imports/exports
manifest dependencies
artifact digests
known-membership boundary crossing
complete-scope exact search
```

Every probe must declare source/scope, completeness guarantee, currentness, blind spots, and the exact mechanical claim established. Do not name a mechanical output as if it established semantic architectural judgment.

**Current disposition:** remain deferred. The Phase 10 episodes and subsequent Phase 15 liveness defect did not demonstrate repeated demand for a new repository relation family. The liveness checker is a conformance rule over existing Skill identity/tree semantics, not a new repository semantic probe family.

---

# Phase 12 — Repository Semantic Map Experiment

**Status:** Deferred.

Trigger only if multiple Skills repeatedly reconstruct the same repository entities/relations and durable sharing would materially reduce inconsistency or duplicated work.

Candidate bounded artifact:

```text
RepositorySemanticMap
- target_snapshot
- scope
- entities
- relations
- claims
- contradictions
- unresolved_uncertainties
- evidence_refs
```

It must never become a complete repository source of truth.

Phase 9, Phase 10, and the bounded Phase 15 liveness pilot do **not** provide sufficient evidence for this experiment.

---

# Phase 13 — Campaign / Control-Plane Promotion

**Status:** Deferred.

A semantic concept should enter Campaign schema only when:

1. it must survive across sessions to preserve consequential decision state;
2. at least two real workflows demonstrate the need;
3. semantics are stable;
4. migration can avoid semantic invention;
5. mechanical validation boundaries are clear.

Phase 10 showed that the common profile can help fresh-context reconstruction, but did not show that Campaign correctness depends on persisting this profile as control-plane state. The Phase 15 liveness gate is repository conformance, not Campaign state. Both remain outside Campaign artifact admission.

---

# Phase 14 — Domain-Pack Extraction

**Status:** Deferred.

Trigger only after at least two independently implemented domain systems demonstrate a stable pattern such as:

```text
foundation semantics
+ responsibility vocabulary
+ capability manifests
+ artifact contracts
+ validators
+ domain Skills
```

The PM domain is one clear implementation. Core engineering Skills are not automatically a second domain pack merely because they share the repository. A separate reconciliation must establish that at least two domain implementations genuinely expose the same reusable package boundary before extraction is authorized.

---

# Phase 15 — Ontology Conformance and Drift Checks

**Status:** INCREMENTAL — first bounded rule qualified; further expansion evidence-gated.

## Trigger observed

After Phase 10, a fresh frontier audit found repeated maintenance drift around Skill liveness/status metadata:

- status/hand-off state had lagged actual PM implementation state;
- Wave 5 qualification exposed a missing canonical registry identity for a live Skill;
- the PM domain handoff had to repair historical registry notes that still said several now-live Skills had no current implementation.

Existing capability tests already covered identity/output and availability contracts. The uncovered mechanically decidable class was narrower: **compatibility Skill-registry liveness prose could contradict the canonical `skills/<id>/SKILL.md` tree**.

## Qualified first rule

PR #325 introduced `scripts/validate-skill-registry-liveness.py` and `tests/test_skill_registry_liveness.py`, wired into Product Validation's `Repository and Skill contracts` lane.

The rule checks only:

```text
duplicate registry Skill IDs
status: proposed while canonical skills/<id>/SKILL.md exists
explicit no-current-implementation note while that SKILL.md exists
wrong current-canonical skills/<id>/ path
broken current-canonical skills/<id>/ path
```

It explicitly permits `status: deprecated` to describe historical invocation metadata while a current canonical Skill exists, provided the note identifies that current implementation correctly.

The structured validator result preserves:

```text
semantic_truth_established: false
```

Exact candidate `1ff498b8fd57c85d590db249a43e8c17a13f5bda` passed Product Validation run `34470534713` and Release Candidate Distribution run `34470534631` before merging as PR #325 / `d24e9bda18225bf7aa338df1decb5c201474a66e`.

## Expansion boundary

Phase 15 is **not globally complete** and is not automatically the next broad workstream.

Potential later checks such as canonical-term duplication, Skill-local redefinition, relation subject/object misuse, Level-1/2 terms falsely described as runtime-enforced, or deprecated vocabulary leaking into active contracts remain unimplemented and unauthorized until a real maintenance defect demonstrates their value.

Every later rule needs its own bounded mechanical claim, negative/rejection cases, and qualification evidence.

See `phase-15/README.md` and `phase-15-handoff.md`.

---

# Metrics

Continue tracking when future real work provides evidence:

```text
ambiguous terms encountered
cross-Skill concept mismatches
unsupported inference jumps
claims missing currentness
claims missing evidence
repeated semantic reconstruction
fresh-context rework
artifact boilerplate introduced
validator overreach caught
new concepts requested by real tasks
ontology concepts never used
contract/liveness drift incidents
token / coordination overhead
```

The goal is not maximum ontology coverage. The goal is **more consistent warranted reasoning per unit of coordination overhead**.

# Current next step

Do **not** advance automatically to another Phase 15 rule or to Phase 11, 12, 13, or 14.

Reconcile current repository/product pressure and authorize the smallest next package only when a deferred-phase trigger is demonstrated. Preserving the architecture unchanged is a valid result when no trigger is present.

Preserve the development loop:

```text
observe
-> hypothesize
-> bounded experiment/check
-> evidence
-> smallest warranted formalization
```
