# Durable Campaign and realization continuity (2026-11-24)

**Status:** durable continuation and evidence-linked realization capability.
**Source baseline:** `0e64430c83ca861b8e9ac2eaf5c842464c6891b3`.
**Assessment implementation:** `5e0fc0c7e2c4022efd01ef3219336a80f5699ecf`.
**Fresh continuation:** `119b2b8d9e88b4a6f116d4d1e40589973e0c752c`.

The bound possibility remains `HYPOTHETICAL` in claim status. Its reviewed
realization is now `PARTIALLY_IMPLEMENTED` with the original `HYPOTHETICAL`
basis preserved in history. The Campaign binding still reports
`realization: not_established`.

## 1. Durable continuation

The prior Campaign lived in `%TEMP%`. It was copied without editing its
history to:

```text
H:\codex\campaigns\smk-bridge-continuity-probe
```

The copy passed `campaign validate`; the original `%TEMP%` workspace was kept
as evidence. The Campaign has no target snapshot, so the copy is portable at
the Campaign-state level; it is not a target-identity claim. The durable
identity is:

| Field | Value |
| --- | --- |
| `campaign_id` | `bridge-continuity-probe` |
| Binding | `poss:goal-family-construction-bridge` |
| Final state | `responsibility_deferred_R-AUTO-0002` |
| Deferred responsibilities | `R-AUTO-0003`, `R-AUTO-0002` |
| Assessments | `RA-AUTO-0001`, `RA-AUTO-0002` |
| Binding realization | `not_established` |

A later context can locate and validate this workspace without private session
memory or the temporary directory.

## 2. Observed limitation

The immutable binding preserved the original commitment, but the Campaign did
not distinguish:

- original conditions;
- current evidence state;
- remaining work.

`working-context` and `resume-profile` projected the five original conditions
verbatim. The six transitions carried about 5.3k characters of prose with
`evidence_refs: []` and `established_facts: []`. The bridge rendered every
component as `implementation_verified: false`, conflating:

- code-backed capability;
- guidance-only capability;
- declared but unverified component.

The bridge also presented the possibility's realization basis from
`1f8a21fb` without flagging that the inspected revision was `0e64430c`.

## 3. Implementation reality

The required-capability audit found:

| Capability | Actual status |
| --- | --- |
| `cap:adaptive-metareasoning` | Guidance-only by design; no runtime selector |
| `cap:breadth-exploration-guidance` | Guidance-only; no code executes the funnel |
| `cap:experience-lesson-recall` | Code-backed: `semantic method context` returned 13 reviewed lessons and 2 candidates; recall conditions remain `NOT_RECORDED` when absent |
| `cap:repository-only-discovery` | Guidance-only with optional `workspace-orient` / `workspace-query` support |

The two code components, `component:knowledge-store` and
`component:semantic-knowledge-plane`, are implemented and exercised by the real
method-context consumer. `implementation_verified: false` was therefore not
evidence that everything was absent. The route is documentary and does not
prove component sufficiency or current behavior.

## 4. Delivered realization continuity

### Assessment writer

`campaign capability-outcome assess` appends an agent-authored assessment of
the binding's original conditions. It:

- requires one status per original condition, with no duplicates or omissions;
- validates every `file:` path as tracked at the exact source revision and
  every `commit:` ref as an exact local commit;
- requires evidence for `EVIDENCE_PRESENT`, `PARTIAL_EVIDENCE` and
  `CONTRADICTING_EVIDENCE`;
- records the condition text, status, evidence refs and basis;
- commits through a same-state lifecycle transition that preserves the active
  responsibility and the binding;
- never changes `binding.realization` or `binding.remaining_conditions`.

### Consumers

`working-context` and `resume-profile` project the latest assessment; `audit`
also projects the append-only history. The bridge compares the assessment
source revision with `indexed_ref` (`REALIZATION_ASSESSMENT_STALE`) and the
possibility's authored `assessed_ref` with `indexed_ref`
(`KNOWLEDGE_REALIZATION_STALE`). It also projects the authored
`claim_ceiling` and `scope` for capabilities and components.

### Source evidence resolution

The fresh continuation added `binding_source_evidence` to the bridge. It
resolves each binding `file:` or `commit:` reference at the queried revision
and reports `RESOLVED`, `MISSING`, `UNRESOLVED`, `UNSAFE`, `UNRECOGNIZED` or
`NOT_ASSESSED`, with an `ALL_RESOLVED` / `INCOMPLETE` / `NOT_ASSESSED` summary
and the `BINDING_SOURCE_EVIDENCE_INCOMPLETE` caveat. This checks presence, not
content, implementation or semantic truth.

## 5. Real assessments

`RA-AUTO-0001` at `5e0fc0c7`:

- conditions 1 and 4: `PARTIAL_EVIDENCE`;
- conditions 2, 3 and 5: `EVIDENCE_PRESENT`;
- binding realization: `not_established`.

`RA-AUTO-0002` at `119b2b8d`, after the fresh increment:

- condition 1: `EVIDENCE_PRESENT` (fresh resume through normal consumers);
- condition 2: `EVIDENCE_PRESENT` (routes ruled out capability duplication and
  shaped an evidence/consumer increment);
- condition 3: `EVIDENCE_PRESENT` (same-state transition preserved the binding
  and recorded the route effect);
- condition 4: `PARTIAL_EVIDENCE` (same-mission uses only; independent use and
  redundancy remain open);
- condition 5: `EVIDENCE_PRESENT` (diff review found no planner, ranker,
  generator or readiness verdict).

The original five conditions are copied verbatim into both assessments. The
binding and `RA-AUTO-0001` were unchanged by `RA-AUTO-0002`.

## 6. Fresh continuation

The fresh agent resumed `R-AUTO-0002` at `5e0fc0c7` without a hint about the
next increment. It recovered the binding, the first assessment, the original
conditions and the stale knowledge caveat. It then:

1. added resolution of the binding's preserved source references;
2. reconciled the stale reviewed realization to `PARTIALLY_IMPLEMENTED`,
   preserving the original `HYPOTHETICAL` basis in history;
3. appended `RA-AUTO-0002`;
4. made no planner, ranker or readiness surface.

Its commit is `119b2b8d`; the parent fast-forwarded to preserve that exact
hash. The reconciled knowledge record remains pinned to `5e0fc0c7`, so the
bridge correctly reports `KNOWLEDGE_REALIZATION_STALE` at later revisions; that
is a currentness prompt, not a claim that the reconciled evidence is wrong.

## 7. Claim ceiling

| Level | Status |
| --- | --- |
| Durable Campaign copy validates and resumes | Observed |
| Binding survives assessments and deferral | Observed |
| Per-condition evidence states project through normal consumers | Observed |
| Source references resolve at the queried revision | Observed; presence only |
| Reviewed realization reflects partial implementation | Observed in the reconciled pack, with history retained |
| Component implementation | NOT ESTABLISHED; `implementation_verified` remains false |
| Independent later-agent use | NOT ESTABLISHED |
| Decision influence or comparative benefit | NOT ESTABLISHED |
| Cognitive or longitudinal qualification | NOT ESTABLISHED |

## 8. Continuation

The Campaign is deferred, not closed. Condition 4 remains `PARTIAL_EVIDENCE`;
independent later-agent use and component implementation evidence remain
separate responsibilities. The durable binding, both assessments and the
original conditions are intact.

The next warranted evidence is an independent continuation that uses the
resolved source evidence and the reconciled realization, chooses a real
increment and records whether the bridge changed the choice or reduced
reconstruction. No further projection, profile flag, ranker, planner or
readiness verdict is warranted without that evidence.
