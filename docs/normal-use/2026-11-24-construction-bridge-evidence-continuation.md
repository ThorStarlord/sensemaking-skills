# Construction bridge: resolved source evidence and reconciled realization (2026-11-24)

**Status:** normal-use capability increment and third fresh continuation of the
`bridge-continuity-probe` Campaign. **Source baseline:** `5e0fc0c7e2c4022efd01ef3219336a80f5699ecf`.
**Bound outcome:** `poss:goal-family-construction-bridge`. **Capability:** the
joined bridge can now mechanically resolve the binding's preserved source
references at the revision being inspected, and the reviewed possibility record
reflects the observed partial implementation instead of the stale
"no bridge implementation" basis.

This is one continuation, not independent later-agent qualification,
component-implementation verification, readiness or comparative benefit.

## 1. Resumed Campaign state

The Campaign resumed at `responsibility_active_R-AUTO-0002` with the immutable
capability-outcome binding and the first realization assessment intact:

- possibility `poss:goal-family-construction-bridge`, `realization:
  not_established`, `epistemic_status: selected_hypothesis`;
- four required capabilities and five original realization conditions;
- assessment `RA-AUTO-0001` at `5e0fc0c7`, with three `EVIDENCE_PRESENT`
  conditions and two `PARTIAL_EVIDENCE` conditions;
- no bound Campaign target.

The normal consumers (`campaign working-context`, `campaign resume-profile
--profile working` and `campaign capability-outcome bridge`) returned the
binding and the assessment without re-running opportunity discovery. The
bridge also returned `KNOWLEDGE_REALIZATION_STALE`: the possibility's authored
realization basis was assessed at `1f8a21fb`, not the indexed revision.

## 2. What source inspection showed

The bridge's own source check exposed a real asymmetry:

- the binding's six `source_refs` are authored pointers, not admitted Campaign
  evidence;
- the bridge compared those pointers with the possibility's references for a
  documentary overlap (`source_alignment: MATCH`), but it never checked whether
  any cited path or commit still resolved at the queried revision;
- the realization assessment validated its own evidence refs at the assessment
  revision, so the current evidence was checked while the original commitment
  was not.

All six binding references did resolve at `5e0fc0c7`; the gap was the absence
of the check, not a broken reference. The check is also a prerequisite for a
later agent to distinguish preserved evidence from a stale or mistyped pointer.

Two independent source checks agreed that the reviewed possibility record was
stale:

- `.sensemaking/knowledge/possibility-synthesis.json` still said
  `realization: HYPOTHETICAL` with the basis "No construction-bridge
  implementation, independent later-agent use or benefit is observed", and its
  `claim_ceiling` said "no implemented bridge";
- `semantic workspace-query --operation workspace-impact --ref
  32925b69c460c245699b6657945c374eeb96d7cd` listed
  `poss:goal-family-construction-bridge` among 87 affected reviewed records
  because its cited evidence sources had changed.

The repository did contain real partial construction: the required-capability
route join (`4fe5a2aa`), the Campaign capability-outcome binding (`7df3a7d0`),
the joined bridge consumer (`5e3a783a`) and the evidence-linked realization
assessment (`5e0fc0c7`). The reviewed record no longer described that state.
Every route component still carried `implementation_verified: false`.

## 3. Increment

### 3.1 Binding source-evidence resolution

`campaign capability-outcome bridge` now adds `binding_source_evidence`. For
each binding source reference at the exact indexed revision it reports:

- `RESOLVED` when a `file:` path is tracked at that revision or a `commit:`
  value is an exact local commit;
- `MISSING` when the path is not tracked or the commit is unavailable;
- `UNSAFE` for a malformed file path or commit value;
- `UNRECOGNIZED` for another reference prefix;
- `NOT_ASSESSED` when no exact indexed revision is available.

The section reports counts, the indexed revision and an assessment of
`ALL_RESOLVED`, `INCOMPLETE` or `NOT_ASSESSED`. An incomplete result adds the
`BINDING_SOURCE_EVIDENCE_INCOMPLETE` caveat. This is presence checking, not
content inspection, implementation verification or semantic truth;
`semantic_truth_established` and `implementation_verified` remain false.

### 3.2 Reconciled reviewed realization

The authored possibility record now reports `PARTIALLY_IMPLEMENTED` with
`establishment: observed`. Its basis names the four implemented surfaces and
the new source-evidence check, while keeping the unresolved limits explicit:
documentary routes, unverified component implementation, no strategy-context
join, and no independent later-agent use, decision influence or benefit. The
original `HYPOTHETICAL` basis is preserved in the realization `history`; the
`claim_ceiling` and `horizon` bases are corrected to match the observed state.
The record keeps its `hypothetical` claim status: partial implementation does
not make the value hypothesis true.

### 3.3 Consumer behavior

The non-JSON bridge output prints the binding source-evidence assessment and
lists any non-resolved reference. The existing consumers still project the
binding and the latest assessment unchanged.

## 4. Real CLI observations

At `5e0fc0c7`, with the reconciled record still uncommitted, the modified bridge
returned:

```text
Binding source evidence: ALL_RESOLVED
  counts: RESOLVED=6
  indexed_ref: 5e0fc0c7e2c4022efd01ef3219336a80f5699ecf
Knowledge realization: STALE
  assessed_ref: 1f8a21fb8b053fef607422027f15394f18351fa9
  indexed_ref: 5e0fc0c7e2c4022efd01ef3219336a80f5699ecf
Caveats: TARGET_NOT_BOUND, UNINDEXED_WORKTREE_CHANGES,
  KNOWLEDGE_REALIZATION_STALE, DOCUMENTARY_ROUTES, INSPECT_ORIGINAL_SOURCE
```

The six resolved references are the two knowledge/authority artifacts, the two
prior normal-use records, the semantic architecture module and the persistent
knowledge CLI documentation. The worktree caveat was expected while the
increment was uncommitted.

After the increment is committed, the reconciled record's `assessed_ref`
remains `5e0fc0c7`. The bridge therefore continues to report
`KNOWLEDGE_REALIZATION_STALE` when queried at a later revision: this is the
existing revision-currentness prompt, not an assertion that the reconciled
basis is wrong. A later agent should re-read the cited sources; the new record
and the reconciled pack are the sources that describe the partial state.

`semantic knowledge-proposal-check` validated the reconciled pack before the
commit. The check is schema/path validation, not semantic truth.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Binding source references resolve at the inspected revision | Observed through the real bridge |
| Missing/unsafe/unrecognized reference reporting | Observed through the real bridge and a control Campaign |
| Reviewed possibility basis reflects the observed partial implementation | Observed in the reconciled pack |
| Original `HYPOTHETICAL` basis preserved | Observed in the realization history |
| Component implementation | NOT ESTABLISHED; `implementation_verified` remains false |
| Capability sufficiency, readiness or completion | NOT ESTABLISHED |
| Independent later-agent use | NOT ESTABLISHED; this continuation is within the same mission |
| Decision influence or comparative benefit | NOT ESTABLISHED |
| Comparative or longitudinal cognitive benefit | NOT ESTABLISHED |

The increment adds a mechanical presence check and corrects a stale reviewed
basis. It does not prove that the bridge is valuable, that a component works,
that the remaining conditions are satisfied or that the Campaign outcome is
realized.

## 6. Continuation

The binding and prior assessment are unchanged. The original five conditions
still govern continuation. The next useful evidence is independent later-agent
use, not another projection: a later agent should resume from the bound state,
use the resolved source evidence and reconciled realization, choose a real
increment and record whether the bridge changed the choice or reduced
reconstruction. The unresolved limits remain the absence of a
strategy-context join, component implementation evidence and independent
qualification. No planner, ranker, generator or readiness verdict is
warranted.
