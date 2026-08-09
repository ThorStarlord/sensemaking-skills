# Repository Sensemaking Brief: State-Currency Discipline Fixture

This fixture demonstrates one good representation of the state-currency and
claim-provenance discipline codified in `skills/repo-sensemaker/SKILL.md` and
`skills/repo-sensemaker/references/repo-analysis-template.md` (Section 7 and
Section 11 guidance). It mirrors the structure of
`tests/fixtures/repo-sensemaker-template-canonical.md` so it passes the real
`scripts/validate-brief.py` unchanged.

The repository described here is synthetic; the point of this fixture is the
*wording* of the discipline, not a real diagnosis of this repository. Note the
two required shapes:

- a decision-changing current-state claim that IS verified, with the probe
  cited (git history, in this example);
- a decision-changing current-state claim that is NOT verified, clearly
  identified as documented but not independently verified.

No literal label tokens are required — the distinction is semantic and carried
in prose, per the codified guidance.

## 1. Repository goal
Example repository goal text.

## 6. Weakest boundary
**Weakness type:** Contract Mismatch

## 7. Evidence
- README.md (lines 5-12): feature requirements are vague, no user context
- docs/ARCHITECTURE.md: does not exist

State-currency note: the roadmap document claims the proposal-apply CLI is
incomplete, but current git history (HEAD e790f30, `git log --oneline -5`)
shows that CLI merged into main; the roadmap claim is therefore stale
documented state, treated as historical context rather than current fact. The
release checklist's "publishing formats not shipped" entry could not be
confirmed from repository evidence — no branch, commit, or artifact references
it — so it remains documented but not independently verified.

Claim provenance: the diagnosis above keeps observed evidence (the README.md
citations), documented claims (the roadmap and checklist entries), inference
(the stale-roadmap conclusion drawn from git history), and owner-supplied
context (the Stage 1 intent) distinguishable.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L5-L12
    quote: "An agent-native framework for repository diagnosis and workflow orchestration."
    supports_claim: "Feature requirements are vague"
```

## 11. Recommended next step
The smallest concrete action with highest leverage: proceed with the
proposal-apply follow-up work. This depends on the verified current state that
the proposal-apply CLI exists in main (probe: git history at HEAD e790f30); the
checklist's publishing-formats claim is documented but not independently
verified and is not sequenced on.

## 12. Recommended workflow
Logic trace: the evidence shows feature requirements are vague and no
architecture documentation exists, so the fog is centered on undefined
product scope rather than UI, docs, or architecture concerns; this points
to product_fog and the product-implementation-workflow.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (lines 5-12): feature requirements are vague, no user context"
  - "docs/ARCHITECTURE.md: does not exist"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: analytics_feedback_gap
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
