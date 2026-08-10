# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-08-10T10:55:08.779484Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness type:** Contract Mismatch

The recommended_workflow_id registry drift between validate-artifact.py and validate-brief.py.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

scripts/validate-artifact.py:39 shows the drift.

Logic trace: this is the chain from evidence to conclusion.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
evidence_excerpts:
- file: scripts/validate-artifact.py
  lines: L39
  quote: "def _validate_enum_fields(yaml_data, artifact_id, vocab, errors):"
  supports_claim: registry drift source
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: docs/candidate/stress-test-2026-08-10/00-user-intent.md
user_implied_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog | unknown
primary_fog_type: architecture_fog
diagnosis_conflict:  # model fills: true | false
escalation_recommended: False
evidence:
- "scripts/validate-artifact.py (lines L39): registry drift"
recommended_workflow_id: implementation-workflow
recommended_execution_mode:  # model fills: plan_only | guided_execution
weakest_boundary:  # model fills: short slug
weakness_type: Contract Mismatch
weakness_type_explanation: null  # model fills with a non-empty string ONLY if weakness_type is 'Other'; otherwise leave null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-10T10:55:08.779484Z"
immutable: true
```

## 15. Extended analysis (candidate)

<!-- OPTIONAL, non-blocking, candidate (not yet ratified -- see docs/candidate/architecture-decision.md and docs/candidate/draft-adr-extended-analysis.md). Leave this block absent entirely if you have nothing here; validate-brief.py never requires it. If present, it must be a single `extended_analysis:` YAML mapping with any of: domain (list, reuses canonical fog vocabulary), discovery_confidence ({level, why_bounded}), consequential_boundary ({description, rationale, is_demonstrated_weakness}), uncertainty ({source, question}), owner_intent_state ({known, status}). -->

<!-- MODEL_SECTION:extended_analysis:BEGIN -->

```yaml
extended_analysis:
  schema_version: candidate-1
  consequential_boundary:
    description: brief_skeleton.reconcile stringifies harvested None as literal text None instead of YAML null
    rationale: confirmed directly against a real reconciled artifact; unrelated to the registry drift
    is_demonstrated_weakness: true
```

<!-- MODEL_SECTION:extended_analysis:END -->
