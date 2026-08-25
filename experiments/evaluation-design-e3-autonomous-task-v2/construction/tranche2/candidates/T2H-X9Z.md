candidate_id: T2H-X9Z
family: T2
complexity_level: HIGH
task_text: |
  This repository's orchestration runtime (`scripts/workflow-runtime.py`) is the sole real producer of `workflow_orchestration_plan` artifacts: `OrchestrationRunner.generate_plan()` authors the plan directly rather than leaving execution-state fields to an LLM's guess, because (per the method's own docstring) only the runtime knows them precisely. Read this method's source and find the dict of machine-readable fields it writes into every plan it generates.

  Compare the exact set of keys that dict writes against `workflow_orchestration_plan`'s own contract entry in `skills/workflow-planner/references/artifact-contracts.yaml`. Two of the keys the method writes -- unconditionally, on every single plan it produces, no branching involved -- are declared in that contract entry NEITHER as required NOR as recommended:

  - One of them is checked by this artifact's specialized validator (`scripts/validate-plan.py`): read that validator's source and find the check that hard-errors, unconditionally, whenever this field is absent from a plan's machine-readable block.
  - The other's exact field NAME is already used elsewhere in this same contract file -- declared as a REQUIRED machine field on a different artifact, one with no producer/consumer relationship to `workflow_orchestration_plan`. Do not assume that existing declaration already covers this gap: this repository's own field-contract-agreement guardrail (`tests/test_field_contract_agreement.py`, enforcing the rule in this repo's CLAUDE.md) unions declared machine-field names across ALL artifacts, so it cannot tell "declared on the right artifact" from "declared on any artifact" -- the field must be declared on `workflow_orchestration_plan`'s own contract entry specifically, matching what its own producer actually writes into IT.

  A third key the same method writes is checked only conditionally, by a different part of the same specialized validator -- one that cross-references the plan's own declared initial inputs against the chosen workflow's entry in the workflow registry, only once a real, registered workflow with declared inputs has been chosen.

  The method also writes at least two further keys that are OUT OF SCOPE for this task: one is pure execution-tracking bookkeeping the runtime uses for its own internal ledger, read by no validator and no downstream consumer as a machine field; the other is a dict key whose underlying concept is already fully covered by one of `workflow_orchestration_plan`'s existing REQUIRED machine fields, just under a different, already-established name -- it is not a new field, and must not be declared as one.

  Declare exactly the two unconditionally-written fields as REQUIRED machine fields, and the one conditionally-checked field as a RECOMMENDED (not required) machine field, all three on `workflow_orchestration_plan`'s own contract entry. Do not add, remove, or change the requiredness of any of `workflow_orchestration_plan`'s existing machine fields. Do not declare any of these three fields on any other artifact's contract entry -- including the one that already, coincidentally, requires a same-named field for an entirely unrelated concern. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.

task_text_sha256: 5a03accf653e94519e00c8cfbdd4238398cb23ad4bd38ebfb4b4f4c8a2865d13
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `OrchestrationRunner.generate_plan()` in `scripts/workflow-runtime.py` builds an `OrderedDict` (local variable `machine`) written verbatim into every plan's Section 13 YAML block. Its keys, compared against `workflow_orchestration_plan`'s contract block (`required_machine_fields: [artifact_id, primary_fog_type, chosen_workflow_id, routing_decision_method, workflow_steps, created_at]`, `recommended_machine_fields: [source_intent_ref, execution_mode, system_recommended_workflow, selected_workflow, routing_divergence, escalation_recommended, auto_escalation_allowed, approval_gates, gate_behavior, stop_conditions, subset_run, subset_reason, included_steps, excluded_steps]`):

  - `status` -- written unconditionally (`("status", "created")`). `scripts/validate-plan.py`'s `validate_plan()` contains, unconditionally near the top: `if "status" not in plan_data: errors.append(_code_error(SECTION_11_MALFORMED, "Missing 'status' in machine-readable block", field="status"))`. Undeclared in the contract. Expected requiredness: REQUIRED.
  - `scope_expansion_requires_approval` -- written unconditionally (`("scope_expansion_requires_approval", True)`). This exact field name is already a REQUIRED machine field on `prd`'s contract entry (a `to-prd`-produced artifact with no producer/consumer relationship to `workflow_orchestration_plan`) -- real, verified, and a deliberate trap: the field-contract-agreement guardrail unions field names across all artifacts, so it would treat `prd`'s existing declaration as "coverage" even though `workflow_orchestration_plan` itself declares nothing. Undeclared on `workflow_orchestration_plan`. Expected requiredness: REQUIRED.
  - `initial_inputs` -- written unconditionally as a value (`("initial_inputs", initial_inputs)`), but only meaningfully checked conditionally: `_validate_plan_against_registries()` in `validate-plan.py` reads `plan_inputs = plan_data.get("initial_inputs", [])` and `reg_inputs = workflow.get("initial_inputs", [])` from the chosen workflow's registry entry, and only compares/errors (`INPUT_MISMATCH`) `if plan_inputs or reg_inputs`. Undeclared in the contract. Expected requiredness: RECOMMENDED (the check is conditional on the chosen workflow's own registry entry declaring inputs).
  - `session_id` -- written unconditionally but read by no validator anywhere in the codebase as a machine field; pure internal ledger bookkeeping. OUT OF SCOPE.
  - `steps` -- the dict's own internal key for the machine-readable step list (`m_step` list), a different name for the SAME concept `workflow_steps` already covers as an existing REQUIRED field. Not a new field. OUT OF SCOPE.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  BASELINE_REQUIRED = {"artifact_id", "primary_fog_type", "chosen_workflow_id", "routing_decision_method", "workflow_steps", "created_at"}
  BASELINE_RECOMMENDED = {
      "source_intent_ref", "execution_mode", "system_recommended_workflow", "selected_workflow",
      "routing_divergence", "escalation_recommended", "auto_escalation_allowed", "approval_gates",
      "gate_behavior", "stop_conditions", "subset_run", "subset_reason", "included_steps", "excluded_steps",
  }
  NEW_REQUIRED = {"status", "scope_expansion_requires_approval"}
  NEW_RECOMMENDED = {"initial_inputs"}
  OUT_OF_SCOPE = {"session_id", "steps"}

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  wop = by_id["workflow_orchestration_plan"]
  req = set(wop.get("required_machine_fields") or [])
  rec = set(wop.get("recommended_machine_fields") or [])

  assert NEW_REQUIRED <= req, f"FAIL: not both status and scope_expansion_requires_approval declared required; missing {NEW_REQUIRED - req}"
  assert req == BASELINE_REQUIRED | NEW_REQUIRED, f"FAIL: required_machine_fields is not exactly baseline + {NEW_REQUIRED}, got {req}"
  assert "initial_inputs" in rec, "FAIL: initial_inputs not declared as a recommended machine field"
  assert rec == BASELINE_RECOMMENDED | NEW_RECOMMENDED, f"FAIL: recommended_machine_fields is not exactly baseline + {NEW_RECOMMENDED}, got {rec}"
  assert OUT_OF_SCOPE.isdisjoint(req | rec), f"FAIL: out-of-scope field(s) also declared: {OUT_OF_SCOPE & (req | rec)}"

  prd = by_id["prd"]
  assert set(prd.get("required_machine_fields") or []) == {
      "source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_requires_approval",
  }, "FAIL: prd's required_machine_fields was changed -- prd is out of scope for this task (its existing field is a same-name coincidence, not evidence to edit it)"

  ALL_NEW = NEW_REQUIRED | NEW_RECOMMENDED
  for other_id, other in by_id.items():
      if other_id in ("workflow_orchestration_plan", "prd"):
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert ALL_NEW.isdisjoint(other_fields), f"FAIL: one of {ALL_NEW} also declared on unrelated artifact {other_id!r}: {ALL_NEW & other_fields}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--", "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"workflow_orchestration_plan"}, f"FAIL: diff touches artifact block header(s) other than workflow_orchestration_plan: {touched}"

  runtime_diff = subprocess.run(
      ["git", "diff", "--stat", FROZEN_SHA, "--", "scripts/workflow-runtime.py"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout.strip()
  assert runtime_diff == "", f"FAIL: scripts/workflow-runtime.py was modified; this task only asks for a contract edit:\n{runtime_diff}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator, two fixtures
  def make_fixture(extra_yaml_lines):
      body = (
          "# Workflow Orchestration Plan (fixture)\n\n"
          "## 1. Brief Consumed\nShort.\n\n"
          "## 2. Chosen Workflow\nShort.\n\n"
          "## 3. Why This Workflow\nShort.\n\n"
          "## 4. Workflow Steps Definition\nShort.\n\n"
          "## 5. Machine Readable Plan\n\n"
          "```yaml\n"
          "artifact_id: workflow_orchestration_plan\n"
          "source_intent_ref: 00-user-intent.md\n"
          "primary_fog_type: ui_fog\n"
          "chosen_workflow_id: ui-implementation-workflow\n"
          "routing_decision_method: diagnosis_primary_soft_context\n"
          "workflow_steps:\n"
          "  - step_id: 1\n"
          "created_at: '2026-08-19T00:00:00Z'\n"
          + extra_yaml_lines +
          "```\n"
      )
      return body

  FIXTURE = CLONE / "artifacts" / "plan_ui-implementation-workflow.md"

  # 3a. Fixture missing BOTH new required fields -> generic validator must now FAIL, citing both.
  FIXTURE.write_text(make_fixture(""), encoding="utf-8")
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "workflow_orchestration_plan", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 1, f"FAIL: generic validator should now fail (status, scope_expansion_requires_approval required and absent):\n{result.stdout}"
  assert "MISSING_MACHINE_FIELDS" in result.stdout, f"FAIL: failure not attributed to missing machine fields:\n{result.stdout}"
  assert "status" in result.stdout, f"FAIL: 'status' not cited as missing:\n{result.stdout}"
  assert "scope_expansion_requires_approval" in result.stdout, f"FAIL: 'scope_expansion_requires_approval' not cited as missing:\n{result.stdout}"

  # 3b. Fixture with both new required fields present but initial_inputs absent -> exit 0, warns.
  FIXTURE.write_text(make_fixture("status: created\nscope_expansion_requires_approval: true\n"), encoding="utf-8")
  result2 = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "workflow_orchestration_plan", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result2.returncode == 0, f"FAIL: generic validator should pass once status and scope_expansion_requires_approval are present:\n{result2.stdout}"
  assert "initial_inputs" in result2.stdout and "MISSING_RECOMMENDED_FIELD" in result2.stdout, \
      f"FAIL: generic validator does not warn about missing recommended field initial_inputs:\n{result2.stdout}"

  # 3c. Corroborating (not decisive) evidence: validate-plan.py's own unconditional status
  # check still fires on the same fixture, independent of the contract edit either way.
  spec_result = subprocess.run(
      [sys.executable, "scripts/validate-plan.py", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert "status" not in [] , "sanity"  # no-op guard; real assertion below
  assert "Missing 'status'" not in spec_result.stdout, \
      "FAIL: fixture in 3b already includes status, so validate-plan.py must not still report it missing"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Only one of {status, scope_expansion_requires_approval} declared required** (most plausibly `status` alone, since it has the more directly readable unconditional validator check; `scope_expansion_requires_approval` is easy to skip on the mistaken belief that `prd`'s existing required declaration already "counts"): fails the `NEW_REQUIRED <= req` or exact-set assertion, and independently fails fixture 3a's `scope_expansion_requires_approval in result.stdout` check when omitted.
  - **`scope_expansion_requires_approval` treated as already covered and NOT added, reasoning "it's already required on `prd`"**: this is the central trap this task is designed to catch -- fails the exact-set assertion on `workflow_orchestration_plan` even though `prd`'s own entry (verified unchanged) does carry the field.
  - **Either field declared recommended instead of required**: fails the exact required-set assertion, and fixture 3a would incorrectly pass (exit 0) instead of failing.
  - **`initial_inputs` declared required instead of recommended, or omitted entirely**: fails the exact recommended-set assertion.
  - **`session_id` and/or `steps` also declared**: fails the `OUT_OF_SCOPE.isdisjoint(...)` assertion.
  - **Any of the three fields declared on a different artifact instead of (or in addition to) `workflow_orchestration_plan`**: fails the per-artifact attribution loop.
  - **`prd`'s contract entry also edited** (e.g. "cleaning up" the coincidental name match): fails the `prd`-unchanged assertion.
  - **Editing `scripts/workflow-runtime.py`** instead of, or in addition to, the contract: fails the `runtime_diff == ""` assertion.

oracle_spec_sha256: 124536e3ae42b26dd539008d9a4026afc55bf1bb781b0bc2881d82866fb191dc
complexity_breakdown: |
  Beyond a MEDIUM single-field candidate, this task requires: (1) deriving an exact SET of three fields, not one, by reading a runtime producer method's actual field-writing code end to end and cross-referencing every key it writes against BOTH the contract AND a specialized validator's source -- not pattern-matching a single sibling field by naming convention; (2) resolving genuinely mixed requiredness within that one set (two REQUIRED, one RECOMMENDED), each independently justified by a different piece of evidence (an unconditional validator check vs. a conditional registry cross-check), rather than one uniform answer; (3) correctly rejecting a real, specific instance of this repository's own documented field-contract-agreement guardrail gap -- `scope_expansion_requires_approval` already exists as a required field on an entirely unrelated artifact (`prd`), which a careless reading of "is this field already declared somewhere in the contract file" would wrongly treat as sufficient, when the guardrail itself (and CLAUDE.md's rule) requires it be declared on THIS artifact specifically; (4) resisting two further plausible-but-wrong same-source decoys (`session_id`, pure bookkeeping; `steps`, an internal alias for the already-required `workflow_steps`) drawn from the exact same dict as the three correct fields, not from an unrelated part of the file.

  Not manufactured-obscure: every fact cited (the runtime method's literal dict, the two validator checks, `prd`'s pre-existing field, the field-contract-agreement guardrail's real union behavior) is directly verifiable by reading two files at fixed, named locations. Not MEDIUM: no MEDIUM candidate in this pool derives a mixed-requiredness SET from a deterministic producer's own source while also requiring the agent to recognize and reject a same-name-elsewhere false-coverage trap grounded in this repository's own documented guardrail limitation.

complexity_breakdown_sha256: 47c2ca0d2b9e00db297e303e6ed29c5b86f13150a7225d2c2f6aaabc40958ce5
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `workflow_orchestration_plan` fixture artifacts at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/plan_ui-implementation-workflow.md`, reusing the same path across two fixture variants; the agent never needs to see or create this file.

initial_state_or_fixture_spec_sha256: f01f5a1b1f9f9c120febb9247d2ab55638a18a4728e71e1e9bfe12eb19102290
qualification: |
  ADMISSIBLE

