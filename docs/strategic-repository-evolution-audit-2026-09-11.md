# Strategic Repository Evolution Audit — 2026-09-11

**Status:** current Level-3 strategic audit for repository evolution  
**Target:** `main@1d86c65ff10d29dfd23d3a44ffe8a1053f664845`  
**Control level:** Level 3 — Strategic Repository Evolution  
**Product-thesis authority:** `docs/product-strategy.md`  
**Control-model authority:** `docs/strategic-outer-loop.md`  
**Experiments:** not required or performed

## 1. Outer Loop v0 baseline decision

The Strategic Outer Loop architecture is now treated as the **frozen v0 operational baseline**.

`OUTER_LOOP_V0 = FROZEN_OPERATIONAL_BASELINE`

This means the repository currently considers the following control model sufficient for normal use:

```text
Level 4 — Product Thesis / Strategy Revision
Level 3 — Strategic Repository Evolution
Level 2 — Responsibility / Campaign
Level 1 — Execution
```

The freeze is not a claim that the product is finished forever. It is a construction boundary:

- do not extend the outer-loop model merely because another abstraction can be imagined;
- do not build `strategy inspect/diff`, an `OuterLoopEngine`, a `StrategicPlanner`, a new strategic-state schema, automatic Campaign creation, or Level-4 automation without new concrete pressure;
- use the existing Level-3/Level-4 architecture during ordinary repository development;
- reopen outer-loop construction only from a concrete repeated integrity/reconstruction burden, a mechanically explicit product requirement, or explicit owner direction.

The frozen baseline includes Strategic State Contract Validation v0. Mechanical validation remains narrower than semantic strategy judgment.

## 2. Audit question

> Given the current product thesis, repository capability state, evidence ceilings, and the frozen Outer Loop v0 baseline, what is the single highest-leverage repository-level responsibility currently warranted?

The audit does not assume Semantic Architecture, Campaign runtime, PM capabilities, or outer-loop machinery remain the active frontier.

## 3. Current product/repository state

### Product thesis

`docs/product-strategy.md` remains coherent with the current repository direction:

- primary user: AI-native repository owner / maintainer;
- job: help a capable coding agent establish the warranted repository-level responsibility for consequential ambiguous work;
- deterministic machinery owns mechanical representation/integrity, not semantic truth or strategic selection;
- repository qualification remains distinct from native-harness/product-value proof;
- new experiments are not a current prerequisite.

No thesis-level contradiction was found in this audit.

`THESIS_REVIEW_REQUIRED = NO`

### Capability state

The repository already contains substantial structure:

- Campaign/Responsibility/Authority semantics and durable Campaign state;
- target snapshots, reconciliation, handoff, provenance, artifact admission and narrative/qualification receipts;
- Semantic Architecture Phase 9/10 contracts;
- B1–B7 build-first semantic substrate;
- Skill manifests and Domain Packs;
- Campaign observability/portability and B7 reference audit;
- 27 repository-qualified PM capabilities;
- four-level Strategic Outer Loop documentation contracts;
- Strategic State Contract Validation v0.

The dominant repository problem is therefore no longer simply "missing structure." Simplification, current-authority clarity, and maintenance burden must now compete with new feature construction.

## 4. Repository-wide audit lenses

The audit reviewed the current repository through these Level-3 lenses:

1. product-definition and product-strategy coherence;
2. outer-loop/inner-loop control architecture;
3. Campaign and semantic-substrate capability gaps;
4. repository qualification and evidence ceilings;
5. operator/coding-agent navigation and reconstruction;
6. documentation authority and historical/current-state separation;
7. duplicated operational procedures and synchronization burden;
8. opportunities for simplification/removal rather than new abstraction;
9. previously deferred outer-loop candidates;
10. empirical/native-harness work explicitly deferred by owner direction.

## 5. Findings

### F1 — Product thesis and current strategic-state model are sufficiently coherent

The current Level-4 and Level-3 authority surfaces are explicitly separated and mechanically validated. No current evidence warrants a thesis revision or a new strategic-state schema.

Disposition: `NO_CHANGE_WARRANTED`.

### F2 — Previously deferred outer-loop machinery still lacks a concrete construction warrant

The repository does not currently demonstrate a repeated consumed burden that requires:

```text
strategy inspect/diff
Level-3 -> Campaign automation
Level-4 reconciliation automation
StrategicPlanner / OuterLoopEngine
```

These remain ideas, not pending work.

Disposition: `DEFERRED`.

### F3 — Native-harness/product-value evidence remains incomplete but is owner-deferred

The evidence ceiling is explicit and honest. The absence of more experiments is not a repository-integrity defect and does not authorize speculative infrastructure.

Disposition: `DEFERRED_BY_OWNER_DIRECTION`.

### F4 — Documentation volume contains substantial historical material

The `docs/` tree contains many phase-, milestone-, closure-, hardening-, and implementation-era documents. Historical documentation is not itself a defect; Git history and dated records are useful evidence.

The actionable question is whether a historical document still presents itself as a current authority or whether current operators must compose several historical surfaces to reconstruct normal procedures.

Disposition: `MONITOR / DO_NOT_MASS_DELETE`.

### F5 — Operational runbook authority is fragmented and mechanically stale relative to current CI

This is the strongest current reconstruction/integrity issue.

Current evidence:

1. `README.md` directs operators to `docs/milestone-runbook.md` as the operating and qualification runbook and as the source for locally reproducible Product Validation/Lab/Release commands.
2. `docs/milestone-runbook.md` still declares itself a **post-milestone operational source of truth** tied to Features #298–#300.
3. Its repository-contract reproduction predates later current gates. In particular, the current `.github/workflows/validation.yml` runs:
   - `scripts/validate-strategic-state.py --repo-root .`;
   - `tests/test_semantic_reasoning_profile.py`;
   - `tests/test_skill_registry_liveness.py`;
   - `tests/test_strategic_state_validation.py`;
   - `tests/test_semantic_substrate.py`;
   - `tests/test_semantic_reference_audit.py`;
   - `tests/test_semantic_conformance.py`;
   - `tests/test_semantic_cli.py`;
   while the older runbook's copied repository-contract list stops at the earlier probe/path/CLI tests.
4. `docs/post-milestone-handoff-runbook.md` layers Packages #302–#304 procedures on top of the earlier milestone runbook and explicitly tells operators to continue using the older runbook for the full qualification flow.
5. Therefore current operational knowledge is split across a current CI workflow, an older document claiming source-of-truth status, and a later milestone companion.

This produces a concrete failure mode:

```text
operator follows README
-> opens milestone-era runbook
-> runs an incomplete historical reproduction of repository-contract validation
-> may believe current repository qualification was reproduced
```

The problem is mechanical/documentary current-authority drift. It does not require an experiment to establish.

Disposition: `ACTIVE_CANDIDATE`.

## 6. Candidate strategic boundaries

### Candidate A — Operational Runbook Authority Consolidation v0

Goal:

> Make one current document the canonical operator-facing local qualification/runbook surface, while preserving historical milestone records without letting them compete for current authority.

Concrete consumer:

- repository owners;
- maintainers;
- coding agents following `README.md` / `CONTEXT.md`;
- future sessions reproducing Product Validation and release qualification.

Mechanically decidable completion:

- one current operations/qualification runbook exists;
- README and CONTEXT point to it;
- old milestone runbooks explicitly identify themselves as historical and point to the current runbook;
- the current runbook reflects current checked-in workflow categories, including Strategic State Contract Validation v0 and B7-era repository tests;
- CI workflows remain executable authority;
- no current runbook claims semantic truth or independent authority over CI.

### Candidate B — Broad documentation archival / deletion

Potential value exists, but a mass archive/removal would require subjective judgments about historical usefulness and could destroy useful reconstruction context.

Disposition: `REJECT_FOR_NOW`.

### Candidate C — `strategy inspect/diff`

No new consumer failure was found beyond what existing Markdown + validator already covers.

Disposition: `DEFERRED`.

### Candidate D — Level-3 -> Campaign bridge

No repeated manual handoff failure currently establishes that an automated bridge is necessary. The current handoff contract remains sufficient.

Disposition: `DEFERRED`.

### Candidate E — Level-4 reconciliation machinery

No thesis review is active and no repeated reconciliation failure warrants machinery.

Disposition: `DEFERRED`.

### Candidate F — New semantic/capability feature

No repository-wide evidence in this audit establishes a stronger missing mechanical capability than the current operational-authority drift.

Disposition: `NO_SELECTION`.

## 7. Decision

`BUILD OPERATIONAL RUNBOOK AUTHORITY CONSOLIDATION v0`

This is the single highest-leverage repository-level responsibility selected by the audit.

Why:

- it addresses a concrete current consumer path (`README.md` -> runbook);
- the stale/fragmented authority is directly observable from current repository bytes;
- success is mechanically/documentarily decidable;
- it reduces synchronization burden rather than adding a new abstraction;
- it exercises the frozen Outer Loop v0 on normal repository evolution;
- it does not depend on experiments or unmeasured agent-benefit claims.

## 8. Authorized implementation scope

Create one current canonical operator-facing runbook, recommended path:

```text
docs/operations-runbook.md
```

It should cover:

- current authority hierarchy;
- development setup;
- Product Validation reproduction categories;
- Strategic State Contract Validation command;
- repository probe/conformance/repository assertion categories;
- Campaign product tests;
- installed-wheel checks;
- filesystem-security checks;
- Lab Validation boundary;
- Release Candidate Distribution boundary;
- exact-head qualification rule;
- human/owner gates;
- empirical/native-harness claim ceilings;
- where milestone-specific historical records now live.

Reconcile navigation:

- `README.md` -> current operations runbook;
- `CONTEXT.md` -> current operations runbook;
- historical runbooks -> explicit historical status + pointer to current runbook.

Historical documents may retain concise milestone ledgers and Git/PR evidence, but must not claim current operational authority.

## 9. Explicit non-goals

Do not:

- delete historical evidence wholesale;
- create a new workflow/orchestration runtime;
- create an `OuterLoopEngine` or `StrategicPlanner`;
- add strategy ranking;
- change Campaign schema;
- change product thesis;
- create a new strategic-state schema;
- change native-harness qualification claims;
- perform experiments;
- make the runbook authoritative over checked-in CI workflows;
- claim local command reproduction is identical to hosted cross-platform CI when it is not.

## 10. Qualification plan

Repository qualification should establish:

1. all changed current-document pointers resolve;
2. `scripts/validate-strategic-state.py --repo-root .` still passes;
3. `scripts/validate-repo.py` still passes;
4. Product Validation passes on the exact PR head;
5. Release Candidate Distribution passes on the exact PR head;
6. the diff contains no runtime/schema/semantic-routing changes;
7. historical runbooks no longer claim current operational source-of-truth status.

## 11. Natural-use evidence captured

This audit itself is normal-use evidence for Outer Loop v0, not an experiment.

Observed natural-use incident:

```text
current README navigation
+ milestone-era runbook authority claim
+ later companion runbook
+ newer CI gates
-> operator reconstruction/maintenance mismatch
```

No separate usage-evidence datastore is created. Future natural-use incidents should be recorded in the relevant Level-3 audit, issue, ADR, or status reconciliation when they materially affect a decision.

## 12. Stopping rule

After Operational Runbook Authority Consolidation v0 is integrated:

- close the responsibility in `STATUS.md`;
- reassess Level 3 from the new repository state;
- do not automatically begin broad documentation cleanup, `strategy inspect/diff`, an L3->Campaign bridge, Level-4 machinery, or another outer-loop package;
- if no comparably concrete current boundary remains, stop construction and continue normal repository use under the frozen Outer Loop v0 baseline.
