# Semantic Architecture Phase 15 — Registry Liveness Pilot Handoff

**Status:** COMPLETE — first bounded Phase 15 pilot qualified  
**Pilot:** Skill registry liveness drift conformance  
**Implementation PR:** #325  
**Qualified candidate head:** `1ff498b8fd57c85d590db249a43e8c17a13f5bda`  
**Merge commit:** `d24e9bda18225bf7aa338df1decb5c201474a66e`  
**Product Validation:** run `34470534713` — SUCCESS  
**Release Candidate Distribution:** run `34470534631` — SUCCESS

## Why Phase 15 was activated out of sequence

The semantic implementation plan deliberately made later phases trigger-based rather than sequential. After Phase 10 closed, a fresh frontier audit found no warranted trigger for Phases 11–14, but it did find repeated maintenance evidence for one narrow Phase 15 class:

- repository/status drift had previously lagged actual PM implementation state enough to risk duplicate work;
- Wave 5 qualification exposed a missing canonical Skill-registry identity for a live capability;
- the PM handoff had to repair historical registry notes that still claimed several now-live Skills had no current implementation.

Existing Campaign capability tests already protected identity, output-artifact, availability, and shipped-implementation contracts. The remaining gap was narrower: compatibility registry prose could contradict the mechanically observable canonical Skill tree.

That observed defect class—not the phase number—authorized this pilot.

## Delivered contract

`scripts/validate-skill-registry-liveness.py` compares the canonical compatibility registry against `skills/<id>/SKILL.md` existence and rejects only mechanically decidable contradictions:

```text
duplicate Skill IDs
status: proposed while skills/<id>/SKILL.md exists
explicit no-current-implementation note while skills/<id>/SKILL.md exists
"current canonical implementation lives under skills/<x>/" where x != id
"current canonical implementation lives under skills/<id>/" when that SKILL.md is missing
```

The validator explicitly allows:

```text
status: deprecated
+
current canonical Skill implementation exists
```

when `deprecated` describes historical invocation metadata and the note correctly identifies the current canonical Skill tree.

This distinction preserves compatibility history without allowing stale liveness claims.

## Qualification evidence

The PR added positive and rejection fixtures in `tests/test_skill_registry_liveness.py` and wired them into the existing Product Validation `Repository and Skill contracts` lane.

On exact candidate `1ff498b8fd57c85d590db249a43e8c17a13f5bda`:

- current repository registry liveness conformance — PASS;
- stale no-current-implementation note rejection — PASS;
- proposed/live contradiction rejection — PASS;
- mismatched current-path rejection — PASS;
- broken current-path rejection — PASS;
- duplicate-ID rejection — PASS;
- truthful historical absent-Skill compatibility case — PASS;
- deprecated historical invocation metadata plus valid current Skill — PASS;
- Campaign product Python 3.11 — PASS;
- Campaign product Python 3.12 — PASS;
- Repository and Skill contracts — PASS;
- installed core wheel regressions — PASS;
- Linux filesystem security — PASS;
- Windows filesystem security — PASS;
- Release Candidate Distribution — PASS.

No authority lane was bypassed.

## Semantic boundary

The validator returns:

```text
semantic_truth_established: false
```

It establishes repository consistency only. It does not establish:

- Skill semantic correctness;
- repository qualification merely from tree existence;
- native-harness discovery or invocation;
- portability or promotion;
- that historical invocation metadata should be deleted;
- arbitrary documentation truth;
- ontology correctness beyond the inspected liveness relation.

Therefore:

```text
registry liveness valid
!=
Skill semantically correct
```

and:

```text
canonical Skill tree exists
!=
native harness has discovered/invoked it
```

## Phase 15 disposition

Phase 15 is now **incremental / trigger-driven**, with one qualified executable conformance rule. It is not a completed universal conformance system.

Do not add another Phase 15 rule merely because this pilot passed. A later rule requires its own observed maintenance defect, bounded mechanical claim, rejection coverage, and exact-head qualification.

Examples of still-unproven candidate drift classes include canonical-term duplication, relation subject/object misuse, Level-1/2 concepts falsely described as runtime-enforced, or deprecated vocabulary leaking into active contracts. None is automatically authorized by this pilot.

## Other phases remain deferred

The Phase 15 pilot does not change the evidence state for:

```text
Phase 11 — Mechanical Semantic Probes
Phase 12 — Repository Semantic Map
Phase 13 — Campaign/control-plane promotion
Phase 14 — Domain-pack extraction
```

They remain deferred until their own triggers are demonstrated.

## Next frontier

After this handoff, reconcile current repository/product pressure again. If no new mechanically or semantically demonstrated trigger exists, stop semantic formalization rather than manufacturing another phase package.

The strongest remaining explicit evidence debt remains outside this pilot:

- engineering real-harness external golden-path qualification;
- PM native-harness functional qualification;
- PM second-harness portability qualification.

Repository CI and connector-side reasoning cannot manufacture native-harness origin evidence.
