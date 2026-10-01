# Strategic State Mechanical Reassessment v1

**Status:** `BUILD_BOUNDED_MECHANICS`  
**Milestone:** Strategic Outer Loop Precision v1 — Package 6  
**Scope:** mechanically decidable representation changes only  
**Semantic authority added:** none

## Question

After Product Boundary Reconciliation, Level-3 Strategic Decision Model v1, durable-state refinement, thesis-transition semantics, and semantic Reasoning Model integration, did any newly stable concept become mechanically necessary for fresh-context reconstruction?

## Findings

Two representation gaps are now both stable and mechanically decidable.

### M1 — Strategic Decision to Support is a required current-state anchor

The refined Level-3 contract makes the strategic decision being supported necessary to reconstruct why a boundary/uncertainty/responsibility exists.

Mechanical rule:

```text
STATUS.md contains exactly one
### Current strategic decision to support
```

The validator does not judge the text under that heading.

```text
section present != decision strategically important
```

The read-only `campaign strategy inspect/diff` projection should expose that section, and an explicit strategy handoff may transport the already-authored text with the source STATUS digest. It must report that the tool did not select the decision.

### M2 — ADR 0029 is now current product-boundary authority

Product Boundary Reconciliation v1 owner-ratified ADR 0029 and superseded ADR 0014. A Level-3 state that silently points at no current product boundary would now be mechanically incomplete.

Mechanical rules:

```text
docs/adr/0029-current-product-boundary.md exists

### Current product strategy
contains exactly one canonical pointer:
Current product-boundary authority
-> docs/adr/0029-current-product-boundary.md
```

The validator does not judge whether ADR 0029 is a good boundary.

## Not mechanized

The reassessment explicitly rejects mechanical checks for:

```text
strategic decision importance
frontier comparison quality
highest-leverage ranking
smallest-intervention correctness
Thesis Tension materiality
whether Level-4 review is semantically required
whether active work depends on a challenged thesis
post-review STILL_RELEVANT / STALE / SUSPECT / CONTRADICTORY classification
```

Those remain agent/human semantic judgment.

## Implementation

Bounded changes:

- `scripts/validate-strategic-state.py`
  - require ADR 0029 surface and canonical STATUS pointer;
  - require the Strategic Decision to Support heading;
- `tests/test_strategic_state_validation.py`
  - positive/negative coverage for both new anchors;
  - preserve proof that semantically questionable prose is not scored;
- `src/sensemaking_skills/campaign_strategy_cli.py`
  - project/diff Strategic Decision to Support;
  - transport already-authored decision text into explicit Level-3-to-Campaign handoff metadata;
  - preserve `strategic_decision_selected_by_tool: false`;
- `tests/campaign_validation/test_campaign_strategy_ergonomics.py`
  - inspect/diff/handoff coverage plus missing-section rejection.

## Claim ceiling

```text
representation valid
!= strategic decision correct
!= boundary highest leverage
!= responsibility warranted
!= semantic truth
```

No new strategic-state schema, Campaign schema, scoring model, planner, router, automatic escalation, or experiment is introduced.