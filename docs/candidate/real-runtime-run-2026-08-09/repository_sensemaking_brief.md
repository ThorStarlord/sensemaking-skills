# Repository Sensemaking Brief

<!-- artifact_id: repository_sensemaking_brief | schema_version: 1 -->
<!-- runtime-generated skeleton created_at: 2026-08-10T02:01:25.000254Z -->

## 1. Repository goal

<!-- MODEL_SECTION:repository_goal:BEGIN -->

This repository is a meta-routing framework: it turns repository/project uncertainty ("fog") into problem frames, evidence-backed diagnoses, and routed next steps for AI agents, via Markdown-defined skills communicating through durable artifacts rather than conversation memory ("artifacts are the API," CONTEXT.md).

<!-- MODEL_SECTION:repository_goal:END -->

## 2. Current shape

<!-- MODEL_SECTION:current_shape:BEGIN -->

`skills/` holds the product surface (repo-sensemaker, architectural-review, workflow-planner, and others). `scripts/` holds the validator stack (`validate-brief.py`, `validate-artifact.py`, `brief_skeleton.py`) plus the runtime (`workflow-runtime.py`, `skill_executor.py`). `docs/canonical-vocabulary.yaml` and `skills/workflow-planner/references/workflow-registry.yaml` both declare workflow-id vocabularies, separately maintained.

<!-- MODEL_SECTION:current_shape:END -->

## 3. Strong signals

<!-- MODEL_SECTION:strong_signals:BEGIN -->

`scripts/validate-brief.py` and `scripts/validate-artifact.py` are both real, exercised validators with their own test suites. `docs/canonical-vocabulary.yaml`'s `fog_types` list (5 entries) is the single source both `validate-brief.py` (as of PR #163) and `validate-artifact.py` use for fog-type enums, showing this kind of registry unification has already been done once, successfully, for a sibling field.

<!-- MODEL_SECTION:strong_signals:END -->

## 4. Missing pieces

<!-- MODEL_SECTION:missing_pieces:BEGIN -->

The same unification was not done for `recommended_workflow_id`. `validate-artifact.py`'s `_validate_enum_fields` (scripts/validate-artifact.py:39-84) checks `recommended_workflow_id` against `docs/canonical-vocabulary.yaml`'s `routing_fields` enum, while `validate-brief.py` checks the same field against `skills/workflow-planner/references/workflow-registry.yaml` (a separate, larger file). `docs/canonical-vocabulary.yaml`'s `workflow_ids` list (docs/canonical-vocabulary.yaml:609) has 19 entries; `workflow-registry.yaml` has more, including `architecture-implementation-workflow` (skills/workflow-planner/references/workflow-registry.yaml:848), `skill-evaluation-workflow` (skills/workflow-planner/references/workflow-registry.yaml:905), and `architectural-review-planning-workflow` (skills/workflow-planner/references/workflow-registry.yaml:942) -- none of which appear in canonical-vocabulary.yaml's list.

<!-- MODEL_SECTION:missing_pieces:END -->

## 5. Improvement opportunities

<!-- MODEL_SECTION:improvement_opportunities:BEGIN -->

Regenerate `docs/canonical-vocabulary.yaml`'s `workflow_ids` / `routing_fields.recommended_workflow_id.values` from `workflow-registry.yaml` (the fuller, more-authoritative-seeming list), mirroring the fog-type unification already done in PR #163.

<!-- MODEL_SECTION:improvement_opportunities:END -->

## 6. Weakest boundary

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->

**Weakness type:** Contract Mismatch

Two validators in the same verification chain (`artifact-contracts.yaml`'s `verification.generic_validator` and `verification.specialized_validators` for `repository_sensemaking_brief`) check the same field, `recommended_workflow_id`, against two different, independently-maintained enumerations that have already drifted apart.

<!-- MODEL_SECTION:weakest_boundary_prose:END -->

## 6.5. Problem classification (fog type)

Fog type is recorded in the machine-readable handoff block (Section 13), not here.

## 7. Evidence

<!-- MODEL_SECTION:evidence_prose:BEGIN -->

<!-- mode: investigative -->
`scripts/validate-artifact.py:39-84` shows `_validate_enum_fields` sourcing its `recommended_workflow_id` allow-list from `vocab.get("routing_fields", [])`, itself loaded from `docs/canonical-vocabulary.yaml`. `scripts/validate-brief.py` (the specialized validator run immediately after it in the same chain) sources the same field's allow-list from `skills/workflow-planner/references/workflow-registry.yaml` via `load_workflow_registry()`. `docs/canonical-vocabulary.yaml:609` begins a 19-entry `workflow_ids` list that does not include `architecture-implementation-workflow` (skills/workflow-planner/references/workflow-registry.yaml:848), `skill-evaluation-workflow` (skills/workflow-planner/references/workflow-registry.yaml:905), or `architectural-review-planning-workflow` (skills/workflow-planner/references/workflow-registry.yaml:942), all three of which are real, valid ids in the registry `validate-brief.py` actually checks.

Logic trace: a brief whose `recommended_workflow_id` is one of these three ids passes the specialized validator (`validate-brief.py`) but fails the generic validator (`validate-artifact.py`) with `INVALID_ENUM_VALUE` -- reproduced directly today while building `tests/test_extended_analysis_end_to_end.py` on this same branch, which is why that fixture was written to deliberately use `product-implementation-workflow` (present in both lists) instead. Since both validators are declared as required verification steps for the same artifact in `artifact-contracts.yaml`, this is a live, currently-reproducible Contract Mismatch, not a hypothetical one.

<!-- MODEL_SECTION:evidence_prose:END -->

<!-- REQUIRED: this section's prose must include a paragraph giving the diagnostic reasoning chain that connects the cited evidence to the weakest-boundary conclusion, starting with the exact two-word marker phrase specified in your execution instructions followed by a colon. validate-brief.py fails the whole artifact (error code NO_LOGIC_TRACE) if that reasoning paragraph is absent. -->

## 8. Evidence excerpts

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->

```yaml
evidence_excerpts:
- file: scripts/validate-artifact.py
  lines: L39-L84
  quote: "def _validate_enum_fields(yaml_data, artifact_id, vocab, errors):\n    \"\"\"Validate routing field enum values against canonical vocabulary.\n\n    Args:\n        yaml_data: Parsed YAML machine-readable section\n        artifact_id: The artifact ID\n        vocab: Loaded canonical vocabulary\n        errors: List to append errors to (modified in-place)\n    \"\"\"\n    if not vocab or not yaml_data:\n        return\n\n    # Build enum validators from vocabulary routing_fields\n    routing_fields = {f[\"field\"]: f for f in vocab.get(\"routing_fields\", [])}\n\n    # Validate enum fields that exist in YAML\n    for field_name, field_spec in routing_fields.items():\n        if field_name not in yaml_data:\n            continue\n\n        value = yaml_data[field_name]\n        if value is None:\n            continue\n\n        allowed_values = field_spec.get(\"values\", [])\n        if not allowed_values:\n            continue\n\n        # Handle list fields (e.g., secondary_fog_types)\n        if field_spec.get(\"type\") == \"list(enum)\":\n            if isinstance(value, list):\n                for i, item in enumerate(value):\n                    if item not in allowed_values:\n                        errors.append(\n                            format_error(\n                                INVALID_ENUM_VALUE,\n                                f\"Field '{field_name}[{i}]' has invalid value '{item}'. \"\n                                f\"Allowed: {', '.join(str(v) for v in allowed_values)}\"\n                            )\n                        )\n        # Handle single enum fields\n        else:\n            if value not in allowed_values:\n                errors.append(\n                    format_error(\n                        INVALID_ENUM_VALUE,"
  supports_claim: generic validator sources recommended_workflow_id's allow-list from canonical-vocabulary.yaml's routing_fields
- file: docs/canonical-vocabulary.yaml
  lines: L609
  quote: "workflow_ids:"
  supports_claim: canonical-vocabulary.yaml's workflow_ids list starts here, 19 entries, missing the three ids below
- file: skills/workflow-planner/references/workflow-registry.yaml
  lines: L848
  quote: "- id: architecture-implementation-workflow"
  supports_claim: architecture-implementation-workflow exists in the registry validate-brief.py checks, absent from canonical-vocabulary.yaml
```

<!-- MODEL_SECTION:evidence_excerpts:END -->

## 9. Why this boundary matters

<!-- MODEL_SECTION:why_boundary_matters:BEGIN -->

Any brief recommending one of the drifted-out ids passes the specialized validator but fails the generic one -- an inconsistent pass/fail outcome for the same artifact depending only on which validator runs, or in what order. This is a narrow, mechanical fix, not a design question.

<!-- MODEL_SECTION:why_boundary_matters:END -->

## 10. Candidate next steps

<!-- MODEL_SECTION:candidate_next_steps:BEGIN -->

1. Regenerate canonical-vocabulary.yaml's workflow_ids/routing_fields from workflow-registry.yaml.
2. Add a regression test asserting the two lists agree (mirroring how fog-type agreement is likely already tested after PR #163).
3. Leave workflow-registry.yaml as-is; it's the fuller, more current-seeming list.

<!-- MODEL_SECTION:candidate_next_steps:END -->

## 11. Recommended next step

<!-- MODEL_SECTION:recommended_next_step:BEGIN -->

Regenerate canonical-vocabulary.yaml's workflow-id lists from workflow-registry.yaml and add a regression test for agreement -- small, bounded, mirrors an already-successful precedent (PR #163's fog-type unification).

<!-- MODEL_SECTION:recommended_next_step:END -->

## 14. Ready-to-copy prompt

<!-- MODEL_SECTION:ready_to_copy_prompt:BEGIN -->

Regenerate docs/canonical-vocabulary.yaml's workflow_ids and routing_fields.recommended_workflow_id.values from skills/workflow-planner/references/workflow-registry.yaml's full id list, and add a test asserting the two never drift apart again.

<!-- MODEL_SECTION:ready_to_copy_prompt:END -->

## 12. Recommended workflow

See `recommended_workflow_id` in Section 13. Must match an id in workflow-registry.yaml. Do not invent workflow ids.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: docs/candidate/real-runtime-run-2026-08-09/00-user-intent.md
user_implied_fog_type: architecture_fog
primary_fog_type: architecture_fog
diagnosis_conflict: False
escalation_recommended: False
evidence:
- "scripts/validate-artifact.py (lines L39-L84): sources recommended_workflow_id allow-list from canonical-vocabulary.yaml"
- "docs/canonical-vocabulary.yaml (lines L609): workflow_ids list, 19 entries, missing 3 real registry ids"
- "skills/workflow-planner/references/workflow-registry.yaml (lines L848): architecture-implementation-workflow, absent from canonical-vocabulary.yaml"
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: recommended_workflow_id enum source drift between validate-artifact.py and validate-brief.py
weakness_type: Contract Mismatch
weakness_type_explanation: None
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-10T02:01:25.000254Z"
immutable: true
```

## 15. Extended analysis (candidate)

<!-- OPTIONAL, non-blocking, candidate (not yet ratified -- see docs/candidate/architecture-decision.md and docs/candidate/draft-adr-extended-analysis.md). Leave this block absent entirely if you have nothing here; validate-brief.py never requires it. If present, it must be a single `extended_analysis:` YAML mapping with any of: domain (list, reuses canonical fog vocabulary), discovery_confidence ({level, why_bounded}), consequential_boundary ({description, rationale, is_demonstrated_weakness}), uncertainty ({source, question}), owner_intent_state ({known, status}). -->

<!-- MODEL_SECTION:extended_analysis:BEGIN -->

```yaml
extended_analysis:
  schema_version: candidate-1
  domain:
    - architecture
  discovery_confidence:
    level: high
    why_bounded: >
      Directly reproduced today (not merely inferred): built a real,
      passing end-to-end test on this branch that had to work around this
      exact drift. Bounded because whether this affects any currently
      *running* production workflow (as opposed to being reproducible)
      was not separately checked.
  consequential_boundary:
    description: >
      Two validators required by the same artifact contract check the
      same field against two independently-maintained, already-diverged
      enumerations.
    rationale: >
      scripts/validate-artifact.py:39-84 and scripts/validate-brief.py
      source recommended_workflow_id's allow-list from two different
      files; docs/canonical-vocabulary.yaml is missing at least 3 ids
      real in workflow-registry.yaml.
    is_demonstrated_weakness: true
  uncertainty:
    source: owner_intent
    question: >
      Should docs/canonical-vocabulary.yaml become a generated view of
      workflow-registry.yaml (registry as sole source of truth), or
      should workflow-registry.yaml be pruned to match
      canonical-vocabulary.yaml's smaller, curated list? Both close the
      mismatch; they imply different long-term ownership of "the" list
      of valid workflow ids.
  owner_intent_state:
    known: >
      PR #163 already resolved the analogous fog-type version of this
      exact drift by making canonical-vocabulary.yaml authoritative and
      regenerating validate-brief.py's fog-type check from it -- a real,
      already-decided precedent for which direction this kind of fix
      goes, though not a direct statement about workflow ids specifically.
    status: thin
```

<!-- MODEL_SECTION:extended_analysis:END -->
