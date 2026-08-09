# Repository Sensemaking Brief (vNext) — composition test

*(Condensed for the composition test — follows the vNext template's
structure and Section 15 schema; Sections 1-5, 9-14 abbreviated since this
artifact's purpose is testing composition, not exercising every section.)*

## 1. Repository goal
A pre-implementation intelligence/orchestration system that diagnoses
repositories and produces validated handoff artifacts (ADR 0014).

## 6. Weakest boundary / consequential boundary

Four independent, previously-undocumented-as-a-group findings share one
root cause: `docs/canonical-vocabulary.yaml` and the contract-agreement
guard rails built to protect it have drifted from the real registries/
runtime surface, and none of the tests that would catch this are wired
into any CI job.

**Weakness type:** Other — explanation: the closest of the seven
registered types is Zero Validation, but that's not quite accurate: real
tests exist for every one of the four items below (`test_field_contract_agreement.py`,
`test_path_drift.py::test_gate_names_are_canonical`,
`::test_vocabulary_covers_all_artifacts`, `::test_vocabulary_covers_all_workflows`).
The defect is that none of them run in `.github/workflows/validation.yml`
— validation exists in the repo but has zero enforcement in practice,
which doesn't cleanly fit "no automated check exists."

## 7. Evidence

- `scripts/workflow-runtime.py` (`OrchestrationRunner._FOG_TYPE_FIELDS`)
  still includes a bare `fog_type` candidate that's declared in no
  artifact contract — `tests/test_field_contract_agreement.py:82` fails on
  this today, on `main`.
- `docs/canonical-vocabulary.yaml`'s `gates` section is missing
  `review_findings` and `review_recommendation`, which
  `skills/workflow-planner/references/workflow-registry.yaml` references —
  `tests/test_path_drift.py:194` (`test_gate_names_are_canonical`) fails.
- `docs/canonical-vocabulary.yaml`'s `artifact_ids` section is missing
  `architectural_review_recommendation` and `proposed_direction`, both
  declared in `skills/workflow-planner/references/artifact-contracts.yaml`
  — `tests/test_path_drift.py:398` fails.
- `docs/canonical-vocabulary.yaml`'s `workflow_ids` section is missing
  `architectural-review-planning-workflow`, `architecture-implementation-workflow`,
  and `skill-evaluation-workflow`, all present in the real
  `workflow-registry.yaml` — `tests/test_path_drift.py:374` fails.
- None of `test_field_contract_agreement.py` or `test_path_drift.py` are
  invoked by any job in `.github/workflows/validation.yml` (confirmed by
  reading the workflow file in full — the `validate` job runs exactly
  `validate-repo.py`, `test-validators.py`, run-log validation, and
  `validate-mode-coverage.py`; no other job names these files either).

**Logic trace:** the fog_type alias failure was already diagnosed and
classified as "leading candidate for next repair" in a prior session. This
investigation found three more instances of the identical drift class
(canonical-vocabulary.yaml lagging the real registries) while checking
whether that classification still held, plus confirmed all four share the
same second property — a real, already-written test exists, but nothing
runs it. That combination (same defect class, same enforcement gap,
independently discovered four times) is what elevates this from "one small
repair" to "the consequential boundary" — fixing `fog_type` alone would
leave the same class of drift free to recur undetected in the same way it
already has three more times.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: tests/test_field_contract_agreement.py
    lines: L82
    quote: "see file/lines"
    supports_claim: "fog_type is read by the runtime but declared in no artifact contract"
  - file: tests/test_path_drift.py
    lines: L194
    quote: "see file/lines"
    supports_claim: "workflow-registry.yaml gates not present in canonical-vocabulary.yaml"
  - file: tests/test_path_drift.py
    lines: L374-L398
    quote: "see file/lines"
    supports_claim: "workflow-registry.yaml/artifact-contracts.yaml ids missing from canonical-vocabulary.yaml"
```

## 15. Analysis vNext

```yaml
analysis_vnext:
  schema_version: prototype-1
  domain:
    - architecture
    - docs
    # "docs" because canonical-vocabulary.yaml is itself documentation-as-
    # registry; the runtime code half (fog_type alias) is architecture.
  discovery_confidence:
    level: high
    why_bounded: >
      All four findings are directly observed (test failures with exact
      line numbers, cross-checked against the real registry files and the
      real CI workflow file). Nothing here rests on inference. The only
      thing NOT independently re-verified in this pass is whether more
      than these four instances of the same drift class exist elsewhere in
      the repo -- this brief claims four confirmed instances, not
      exhaustiveness.
  consequential_boundary:
    description: >
      canonical-vocabulary.yaml + its guard tests have drifted from the
      real registries in (at least) four ways, none of which are CI-
      enforced.
    rationale: >
      Same defect class recurring four times, independently discovered,
      is stronger evidence of a systemic gap than any single instance --
      and it directly matches this repo's own CLAUDE.md warning (the
      fog_type incident is the one it's named after).
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: >
      Should all four drift items be fixed together as one canonical
      contract-hygiene pass, should only the already-classified fog_type
      alias be fixed now with the other three deferred, and should any of
      the four guard tests be added to a required CI gate as part of
      whichever scope is chosen?
  owner_intent_state:
    known: >
      In a prior session on this same repository, the owner classified the
      fog_type alias specifically as "the leading candidate for the next
      small contract-correctness repair" and separately said, of the
      broader canonical-vocabulary/CI-enforcement question: "record -- not
      automatically fix -- the newly exposed hygiene/vocabulary/CI debt."
    unresolved: >
      Whether that prior "record, don't fix" guidance still holds now that
      three MORE instances of the same drift class are confirmed (not just
      one), and whether CI-wiring should be bundled with any of these
      fixes or remains a fully separate decision.
    status: thin
```
