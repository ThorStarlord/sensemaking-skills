candidate_id: T2H-V6C
family: T2
complexity_level: HIGH
task_text: |
  This repository's canonical vocabulary registry (`docs/canonical-vocabulary.yaml`, `routing_fields` section) declares a field recording OTHER fog types present in a repository besides the single dominant one -- a list, explicitly marked `required: false` in that registry entry, reusing the same five canonical fog-type values `primary_fog_type` uses. TWO independent validators already enforce this field's value validity whenever it is present in an artifact: the generic artifact validator (`scripts/validate-artifact.py`, via its enum-checking helper, which reads this exact field name out of the canonical vocabulary registry) AND a separate, fully implemented specialized validator (`scripts/validate-fog-type-normalization.py`) written specifically for fog-type fields, complete with its own dedicated test suite. Despite this, the field appears in NO artifact's contract entry in `skills/workflow-planner/references/artifact-contracts.yaml` -- not required, not recommended, anywhere.

  Read `repository_sensemaking_brief`'s own contract entry, where this artifact's other two fog-type fields already live: the single dominant type (required), and a separate, optional field for what the user themselves implied (recommended). Declare the missing field as a RECOMMENDED (not required) machine field there too -- matching both the canonical vocabulary registry's own stated requiredness for it, and this artifact's already-established pattern of treating its non-dominant fog-type signal as optional.

  Do not declare this field on `workflow_orchestration_plan`. That artifact's contract entry already mirrors `repository_sensemaking_brief`'s single dominant fog-type field, per an explicit ADR-driven design comment you can read directly in its own contract block -- but it does NOT mirror the brief's optional user-implied fog-type field, and the field this task is about belongs to that same non-mirrored category, not the mirrored one; check both blocks yourself before deciding.

  Do not confuse this field with `repository_sensemaking_brief`'s own Section 15 `extended_analysis.domain` field -- a structurally similar-looking list of fog dimensions on the SAME artifact, whose own contract note explicitly states it must not be wired into routing without a separate, new owner decision. That note is describing a different, already-settled field; it does not apply to the field this task asks you to add.

  Do not wire the specialized fog-type-normalization validator into any artifact's `verification` block -- the generic validator already independently enforces this field's value validity once it is declared; wiring in the specialized validator is a separate decision this task does not ask for. Do not add, remove, or change the requiredness of any other field on `repository_sensemaking_brief`. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.

task_text_sha256: f48dd5f7bffd6668a5f22c3e66cef430e38efe7e065c24832000ec9b8ec552fe
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `docs/canonical-vocabulary.yaml`'s `routing_fields` section declares `- field: secondary_fog_types, type: list(enum), values: [product_fog, ui_fog, architecture_fog, docs_fog, integration_fog], required: false, description: "Other fog types present but less critical"`. `scripts/validate-artifact.py`'s `_validate_enum_fields()` (called unconditionally from `validate_artifact()` whenever a YAML block is found, independent of the contract) contains a dedicated block: `if "secondary_fog_types" in yaml_data: ... for i, fog_type in enumerate(secondary): if fog_type not in fog_type_normalizer: errors.append(INVALID_ENUM_VALUE, ...)`. `scripts/validate-fog-type-normalization.py`, read in full, independently checks and normalizes the same field (`if "secondary_fog_types" in machine_data: ...`), backed by its own tests (`tests/test_fog_type_normalization.py`) and fixtures (`tests/fixtures/validate-fog-type-normalization/`) -- but is NOT referenced anywhere in `artifact-contracts.yaml`'s `specialized_validators` lists for any artifact (verified: no match for "fog-type-normalization" anywhere in the contract file), nor invoked by `validate-and-report.py` or `validate-repo.py`.

  `repository_sensemaking_brief`'s contract block: `required_machine_fields: [artifact_id, primary_fog_type, evidence, recommended_workflow_id, created_at, immutable]`; `recommended_machine_fields: [source_intent_ref, user_implied_fog_type, diagnosis_conflict, escalation_recommended, escalation_target, escalation_reason, auto_escalation_allowed, weakness_type, weakness_type_explanation, extended_analysis.domain, extended_analysis.consequential_boundary, extended_analysis.uncertainty, extended_analysis.owner_intent_state]`, with an explicit note: "extended_analysis (Section 15, ADR 0024 ACCEPTED): optional, non-blocking, model-constrained... Not read by workflow-runtime.py's routing (_WORKFLOW_ID_FIELDS / _FOG_TYPE_FIELDS)... Any future promotion to drive real routing requires a new owner decision per field." `secondary_fog_types` is a wholly separate field from `extended_analysis.domain` and is not mentioned in that note.

  `workflow_orchestration_plan`'s contract block has `primary_fog_type` as required (mirroring the brief, per its own comment: "The plan may carry the diagnosed fog type... (ADR 0005)") but its `recommended_machine_fields` list does NOT include `user_implied_fog_type` -- confirming only the single forced-choice field is mirrored, not the brief's optional non-dominant fog-type signal(s).

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  BASELINE_REQUIRED = {"artifact_id", "primary_fog_type", "evidence", "recommended_workflow_id", "created_at", "immutable"}
  BASELINE_RECOMMENDED = {
      "source_intent_ref", "user_implied_fog_type", "diagnosis_conflict", "escalation_recommended",
      "escalation_target", "escalation_reason", "auto_escalation_allowed", "weakness_type",
      "weakness_type_explanation", "extended_analysis.domain", "extended_analysis.consequential_boundary",
      "extended_analysis.uncertainty", "extended_analysis.owner_intent_state",
  }

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  brief = by_id["repository_sensemaking_brief"]
  rec = set(brief.get("recommended_machine_fields") or [])
  req = set(brief.get("required_machine_fields") or [])

  assert "secondary_fog_types" in rec, "FAIL: secondary_fog_types not declared as a recommended machine field on repository_sensemaking_brief"
  assert rec == BASELINE_RECOMMENDED | {"secondary_fog_types"}, \
      f"FAIL: repository_sensemaking_brief's recommended_machine_fields is not exactly baseline + secondary_fog_types, got {rec}"
  assert "secondary_fog_types" not in req, "FAIL: secondary_fog_types declared required instead of recommended"
  assert req == BASELINE_REQUIRED, "FAIL: an existing required field on repository_sensemaking_brief was changed"

  wop = by_id["workflow_orchestration_plan"]
  wop_fields = set(wop.get("required_machine_fields") or []) | set(wop.get("recommended_machine_fields") or [])
  assert "secondary_fog_types" not in wop_fields, \
      "FAIL: secondary_fog_types declared on workflow_orchestration_plan -- only primary_fog_type is mirrored there, not the brief's non-dominant fog-type signals"
  assert "user_implied_fog_type" not in (wop.get("recommended_machine_fields") or []), \
      "FAIL: sanity check -- workflow_orchestration_plan unexpectedly gained user_implied_fog_type; baseline assumption broken"

  for other_id, other in by_id.items():
      if other_id == "repository_sensemaking_brief":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert "secondary_fog_types" not in other_fields, \
          f"FAIL: secondary_fog_types also declared on unrelated artifact {other_id!r}"

  specialized = brief.get("verification", {}).get("specialized_validators", []) or []
  assert not any("fog-type-normalization" in v for v in specialized), \
      "FAIL: validate-fog-type-normalization.py was wired into repository_sensemaking_brief's specialized_validators -- out of scope for this task"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--", "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"repository_sensemaking_brief"}, \
      f"FAIL: diff touches artifact block header(s) other than repository_sensemaking_brief: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator warns only post-edit
  FIXTURE = CLONE / "artifacts" / "repository_sensemaking_brief.md"
  FIXTURE.write_text(
      "# Repository Sensemaking Brief (fixture)\n\n"
      "## Evidence\nShort.\n\n"
      "## Recommended Workflow\nShort.\n\n"
      "```yaml\n"
      "evidence_excerpts:\n"
      "  - file: CONTEXT.md\n"
      "    lines: '1-2'\n"
      "    quote: 'Short excerpt.'\n"
      "    supports_claim: 'Sanity fixture claim.'\n"
      "```\n\n"
      "```yaml\n"
      "artifact_id: repository_sensemaking_brief\n"
      "primary_fog_type: ui_fog\n"
      "evidence: present\n"
      "recommended_workflow_id: ui-implementation-workflow\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "immutable: true\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "repository_sensemaking_brief", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (secondary_fog_types is recommended, not required):\n{result.stdout}"
  assert "secondary_fog_types" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field secondary_fog_types:\n{result.stdout}"

  # 3b. Corroborating (not decisive) evidence: with an INVALID secondary_fog_types value in
  # the YAML block, the generic validator's enum check independently rejects it -- proving
  # the field is genuinely live-enforced today, regardless of this task's contract edit.
  FIXTURE.write_text(
      "# Repository Sensemaking Brief (fixture)\n\n"
      "## Evidence\nShort.\n\n"
      "## Recommended Workflow\nShort.\n\n"
      "```yaml\n"
      "evidence_excerpts:\n"
      "  - file: CONTEXT.md\n"
      "    lines: '1-2'\n"
      "    quote: 'Short excerpt.'\n"
      "    supports_claim: 'Sanity fixture claim.'\n"
      "```\n\n"
      "```yaml\n"
      "artifact_id: repository_sensemaking_brief\n"
      "primary_fog_type: ui_fog\n"
      "evidence: present\n"
      "recommended_workflow_id: ui-implementation-workflow\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "immutable: true\n"
      "secondary_fog_types: [not_a_real_fog_type]\n"
      "```\n",
      encoding="utf-8",
  )
  result2 = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "repository_sensemaking_brief", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result2.returncode == 1 and "INVALID_ENUM_VALUE" in result2.stdout, \
      f"FAIL: generic validator no longer independently rejects an invalid secondary_fog_types value (environment assumption broken):\n{result2.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Declared as required instead of recommended**: fails the required-field assertion; contradicts the canonical vocabulary registry's own `required: false` and would make every existing single-fog-type brief non-compliant.
  - **Declared on `workflow_orchestration_plan` instead of (or as well as) `repository_sensemaking_brief`**: fails the dedicated `workflow_orchestration_plan`-disjointness assertion -- the deliberate trap is that `primary_fog_type` IS mirrored there (real, per ADR 0005) while `user_implied_fog_type` is NOT, and this field belongs to the non-mirrored category.
  - **Declared as (or confused with) `extended_analysis.domain`, or that field's requiredness/wording changed**: fails the exact-recommended-set assertion, since `BASELINE_RECOMMENDED` requires `extended_analysis.domain` to remain present, unchanged, and distinct from the new field.
  - **`validate-fog-type-normalization.py` wired into `repository_sensemaking_brief`'s `specialized_validators`**: fails the dedicated specialized-validators assertion.
  - **Declared on any other artifact instead of `repository_sensemaking_brief`**: fails the per-artifact attribution loop.
  - **Wrong field name** (e.g. `secondary_fog_type` singular, `other_fog_types`): fails both the attribution assertion and the fixture warning-text assertion, since the fixture check greps for the literal string `secondary_fog_types`.

oracle_spec_sha256: 7f4f89a8c31f4484a21a168391aa7bf1174b3635cd1f83acd540fba997a21514
complexity_breakdown: |
  Beyond a MEDIUM single-field candidate, this task requires: (1) recognizing that TWO fully independent, already-implemented validators (one generic and contract-driven for requiredness but hardcoded for enum values, one specialized and entirely orphaned -- never wired into any artifact's `specialized_validators` list, verified by its absence from the whole contract file) both already enforce this field's value validity, and correctly treating only the generic validator's behavior as the decisive, contract-driven signal while explicitly NOT wiring in the orphaned one (a plausible-but-wrong "complete the validator's job" over-reach the task text explicitly rules out); (2) resolving a genuine cross-block placement question that requires reading TWO different contract entries side by side -- `primary_fog_type` IS mirrored from the brief onto `workflow_orchestration_plan` (real, ADR-documented), but the brief's OTHER fog-type field (`user_implied_fog_type`) is verifiably NOT mirrored there, and only by checking both blocks can the agent correctly place this field on the brief alone; (3) resisting a same-artifact, textually similar decoy (`extended_analysis.domain`, also a list of fog dimensions) that this repository's own contract notes explicitly and pre-emptively warn must not be wired into routing without a separate owner decision -- a real, documented trap on the very same contract entry being edited.

  Not manufactured-obscure: every fact cited (the canonical vocabulary registry entry, both validators' source, the brief's and plan's exact field lists, the extended_analysis note's exact wording) is directly verifiable by reading three files at fixed, named locations. Not MEDIUM: no MEDIUM candidate in this pool requires checking a second artifact's contract block to correctly REJECT placement there (as opposed to comparing two blocks to decide where to promote an already-recommended field, which this pool's own T2M-R9W does), nor requires distinguishing between two independently real validators and choosing not to complete the wiring of one of them.

complexity_breakdown_sha256: f84bcf28c44403cf81322244cfe491195a968aff24bee11127e89c69d10269fb
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `repository_sensemaking_brief` fixture artifacts at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/repository_sensemaking_brief.md`, reusing the same path across two fixture variants; the agent never needs to see or create this file.

initial_state_or_fixture_spec_sha256: 815420ab8bf22d3303a3998ad85cf9e13905e921eeeab3953be5e348036cd781
qualification: |
  ADMISSIBLE

