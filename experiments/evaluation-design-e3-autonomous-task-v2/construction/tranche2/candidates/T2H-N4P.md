candidate_id: T2H-N4P
family: T2
complexity_level: HIGH
task_text: |
  This repository's specialized validator for `architectural_review_recommendation` (`scripts/validate-architectural-review-recommendation.py`) enforces additional required fields once a recommendation's `decision` value is `pursue_narrowed`: TWO machine fields, recording respectively what is being approved for pursuit and what is explicitly excluded from it. The validator checks each of the two independently (not either/or) -- both are hard requirements once `decision` is `pursue_narrowed` -- and both are entirely undeclared anywhere in this artifact's own contract entry in `skills/workflow-planner/references/artifact-contracts.yaml`. Read the validator's source to find the exact field names and confirm both checks are real.

  The same validator conditionally requires several OTHER, DIFFERENT undeclared fields for OTHER decision/confidence combinations elsewhere in its source -- for an `investigate_first` decision, for a `defer` or `reject` decision, and for a low/medium `confidence` value regardless of decision. These are NOT what this task is about; leave every one of them alone.

  Declare exactly the pair of fields tied to the `pursue_narrowed` decision as RECOMMENDED (not required) machine fields on `architectural_review_recommendation`'s own contract entry. Recommended, not required: the validator's check is conditional on `decision`, and declaring either field required would make every existing `pursue`, `investigate_first`, `defer`, and `reject` recommendation artifact non-compliant with the contract even though the validator itself never demands the field from them.

  Do not declare either field on any other artifact's contract entry -- including the artifact that supplies this skill's own upstream input, which has a required section whose name sounds related to "what is approved" but is a different concept entirely. Do not add any of the other conditionally-required fields this same validator checks for the other decision/confidence combinations described above. Do not add, remove, or change the requiredness of any of `architectural_review_recommendation`'s five existing required machine fields. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.

task_text_sha256: a206b22d4e6613d8a40c23fc280d7979d9da04d3be3a344ee6585ef202ee4813
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `architectural_review_recommendation`'s contract block declares `required_machine_fields: [artifact_id, decision, confidence, created_at, created_by]` and has no `recommended_machine_fields` key at all. `scripts/validate-architectural-review-recommendation.py`'s `validate_architectural_review_recommendation()`, read in full, branches on `decision` (after validating it against the allowed-values list) and, specifically `if decision == "pursue_narrowed":`, independently checks:
  - `if "approved_scope" not in artifact_data or not artifact_data["approved_scope"]:` -> error `architectural_review_recommendation.approved_scope.missing_field`
  - `if "excluded_scope" not in artifact_data or not artifact_data["excluded_scope"]:` -> error `architectural_review_recommendation.excluded_scope.missing_field`

  Neither `approved_scope` nor `excluded_scope` is declared in the contract. The SAME validator also independently checks, for OTHER decision/confidence values, three further undeclared fields that are deliberate decoys for this task: `investigation_steps` OR `validation_step` (either satisfies, for `decision == "investigate_first"`), `reversal_conditions` (for `decision in ("defer", "reject")`), and `risks_identified` (for `confidence in ("low", "medium")`, independent of `decision`) -- none of these belong to the `pursue_narrowed` pair this task asks for.

  `proposed_direction` (`consumed_by: [architectural-review]`, this skill's own upstream input) has a required section literally named `success_criteria` -- textually adjacent to "what is approved to pursue" but not the same concept, and not where these fields belong.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  EXPECTED = {"approved_scope", "excluded_scope"}
  DECOYS = {"investigation_steps", "validation_step", "reversal_conditions", "risks_identified", "success_measures"}

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  arr = by_id["architectural_review_recommendation"]
  rec = set(arr.get("recommended_machine_fields") or [])
  req = set(arr.get("required_machine_fields") or [])

  assert EXPECTED <= rec, f"FAIL: not both approved_scope and excluded_scope declared recommended; missing {EXPECTED - rec}"
  assert rec == EXPECTED, f"FAIL: architectural_review_recommendation's recommended_machine_fields is not exactly {EXPECTED}, got {rec}"
  assert EXPECTED.isdisjoint(req), "FAIL: one or both of approved_scope/excluded_scope declared required instead of recommended"
  assert req == {"artifact_id", "decision", "confidence", "created_at", "created_by"}, \
      "FAIL: an existing required field on architectural_review_recommendation was changed"
  assert DECOYS.isdisjoint(rec | req), f"FAIL: one or more out-of-scope decoy fields also declared: {DECOYS & (rec | req)}"

  pd = by_id["proposed_direction"]
  pd_fields = set(pd.get("required_machine_fields") or []) | set(pd.get("recommended_machine_fields") or [])
  assert EXPECTED.isdisjoint(pd_fields), \
      f"FAIL: one or both of approved_scope/excluded_scope declared on proposed_direction -- wrong artifact (confused with its 'success_criteria' section): {EXPECTED & pd_fields}"

  for other_id, other in by_id.items():
      if other_id == "architectural_review_recommendation":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert EXPECTED.isdisjoint(other_fields), \
          f"FAIL: one or both of approved_scope/excluded_scope also declared on unrelated artifact {other_id!r}: {EXPECTED & other_fields}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--", "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"architectural_review_recommendation"}, \
      f"FAIL: diff touches artifact block header(s) other than architectural_review_recommendation: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator's warnings appear only post-edit
  FIXTURE = CLONE / "artifacts" / "architectural_review_recommendation.md"
  FIXTURE.write_text(
      "# Architectural Review Recommendation (fixture)\n\n"
      "## Summary\nShort.\n\n"
      "## Analysis\nShort.\n\n"
      "## Recommendation\nShort.\n\n"
      "## Machine Readable Decision\n\n"
      "```yaml\n"
      "artifact_id: architectural_review_recommendation\n"
      "decision: pursue_narrowed\n"
      "confidence: high\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "created_by: oracle-fixture\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "architectural_review_recommendation", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (approved_scope/excluded_scope recommended, not required):\n{result.stdout}"
  for f in EXPECTED:
      assert f in result.stdout, f"FAIL: generic validator does not warn about missing recommended field {f!r}:\n{result.stdout}"
  assert result.stdout.count("MISSING_RECOMMENDED_FIELD") >= 2, \
      f"FAIL: expected at least 2 MISSING_RECOMMENDED_FIELD warnings, got:\n{result.stdout}"

  # 3b. Corroborating (not decisive) evidence: the specialized validator independently
  # confirms BOTH fields are real, hard requirements for this exact decision value --
  # unaffected by the contract edit either way, run only to establish the pair is not
  # fabricated.
  spec_result = subprocess.run(
      [sys.executable, "scripts/validate-architectural-review-recommendation.py", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert spec_result.returncode == 1, "FAIL: specialized validator should still hard-fail this pursue_narrowed fixture lacking both fields"
  for f in EXPECTED:
      assert f in spec_result.stdout, f"FAIL: specialized validator no longer independently confirms {f!r} matters: {spec_result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Only one of {approved_scope, excluded_scope} declared** (most plausibly `approved_scope` alone, since it reads as the more "primary" of the pair): fails the `rec == EXPECTED` exact-pair assertion.
  - **Declared as required instead of recommended**: fails the disjointness-against-`req` assertion; would make every non-`pursue_narrowed` recommendation artifact non-compliant.
  - **Declared on `proposed_direction` instead of (or as well as) `architectural_review_recommendation`**: fails the dedicated `proposed_direction`-disjointness assertion -- the deliberate trap is that artifact's own required `success_criteria` section, a different concept.
  - **One or more of the other branches' undeclared fields also added** (`investigation_steps`, `validation_step`, `reversal_conditions`, `risks_identified`, `success_measures`): fails the `DECOYS.isdisjoint(...)` assertion.
  - **Editing the specialized validator instead of the contract**: leaves `artifact-contracts.yaml` unchanged, so assertion 1 fails outright.

oracle_spec_sha256: 7afa77e8c6345b5cfd4698d383cd53d25898a4f3354981a131b3d1294665828d
complexity_breakdown: |
  Beyond a MEDIUM single-field candidate on this same artifact (this pool's own T2M-B3Q and T2M-H7V each declare ONE optional field for a different, single condition), this task requires: (1) deriving an exact PAIR of fields, both independently and unconditionally required by the validator once a specific decision value holds, rather than a single field with a single trigger; (2) navigating a genuinely richer near-miss space -- FIVE distinct, real, validator-checked-but-undeclared fields sit in the same source file across three different decision/confidence branches (`investigation_steps`/`validation_step` for `investigate_first`, `reversal_conditions` for `defer`/`reject`, `risks_identified` for low/medium confidence), and the task requires picking exactly the two that belong to `pursue_narrowed` while leaving all five decoys untouched; (3) resisting a wrong-artifact trap grounded in a real, textually adjacent required section (`proposed_direction`'s `success_criteria`) on this skill's own upstream input artifact.

  Not manufactured-obscure: every fact cited (the validator's exact conditional branches, the five decoy fields' own trigger conditions, `proposed_direction`'s required section) is directly verifiable by reading two files at fixed, named locations. Not MEDIUM: this pool's own two MEDIUM candidates on this same artifact each resolve a single field under a single condition with a single wrong-artifact decoy; this task requires resolving a coupled PAIR under one condition while independently rejecting a five-field decoy set spanning three unrelated conditions in the same source function.

complexity_breakdown_sha256: 2bd2e6097f55266f4825d4ec689207c6bcac453388aa804655355d702cd7527c
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `architectural_review_recommendation` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/architectural_review_recommendation.md`; the agent never needs to see or create this file.

initial_state_or_fixture_spec_sha256: e00ead817c03091fcfdca7d3866a794d3b0b48abea671961d2414104122c176b
qualification: |
  ADMISSIBLE

