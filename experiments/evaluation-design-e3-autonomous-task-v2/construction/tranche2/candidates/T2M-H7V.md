candidate_id: T2M-H7V
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's specialized validator for the `architectural_review_recommendation` artifact (`scripts/validate-architectural-review-recommendation.py`) enforces a check unrelated to the "success measurement" concern this artifact type is already known for: whenever a recommendation's `confidence` value is `low` or `medium`, the validator requires an accompanying list of the specific risks that were identified, and reports a logic error when that list is missing or empty. Read the validator's source yourself to confirm this.

  This artifact's own producer-facing template (`skills/architectural-review/references/architectural-review-template.md`) already includes this exact list in its example machine-readable block, under a comment marking it as something every outcome -- not only low/medium-confidence ones -- should carry. Despite both of these real, verifiable facts, `architectural_review_recommendation`'s own entry in `skills/workflow-planner/references/artifact-contracts.yaml` never declares this field at all -- neither as required nor recommended.

  Close this gap: declare the field that captures this enumerated list of identified risks as a RECOMMENDED (not required) machine field on `architectural_review_recommendation`'s own contract entry. Recommended, not required, because the validator's check is conditional on `confidence`; declaring it required would make every existing high-confidence recommendation artifact -- which the validator never demands this field for -- non-compliant with the contract overnight.

  Do not declare this field on any other artifact's contract entry -- including the diagnostic artifact elsewhere in this pipeline whose own required content section is literally named "Risks" (a structurally similar-sounding but unrelated signal on a different artifact). Do not add, remove, or change the requiredness of any other field on `architectural_review_recommendation`. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: 2ecf33a80aee6ee3f5a893680a735f582112de52dcd7de1a97a6bbc07a9ab395
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `architectural_review_recommendation`'s contract block declares `required_machine_fields: [artifact_id, decision, confidence, created_at, created_by]` and has no `recommended_machine_fields` key at all. `scripts/validate-architectural-review-recommendation.py`, read in full, contains (immediately after its `confidence` enum check): `confidence = artifact_data.get("confidence"); risks = artifact_data.get("risks_identified", []); if confidence in ("low", "medium"): if not risks or (isinstance(risks, list) and len(risks) == 0): errors.append({"error_id": "architectural_review_recommendation.risks_identified.logic_error", ...})`. This is a real, currently-enforced, conditional check; the specialized validator hardcodes its own field name and never reads `artifact-contracts.yaml`, so its pass/fail behavior is unaffected by this task's edit either way. The artifact's own template (`skills/architectural-review/references/architectural-review-template.md`), in its "Machine-readable Decision" YAML example, lists `risks_identified:` under the comment `# Recommended for all outcomes` -- confirming both the field's real name and that "recommended" (not "required") is the template author's own stated intent.

  Expected field name: `risks_identified` (the only name the validator's source and the template both use).

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  arr = by_id["architectural_review_recommendation"]
  rec = set(arr.get("recommended_machine_fields") or [])
  req = set(arr.get("required_machine_fields") or [])
  assert "risks_identified" in rec, "FAIL: risks_identified not declared as a recommended machine field on architectural_review_recommendation"
  assert rec == {"risks_identified"}, f"FAIL: architectural_review_recommendation's recommended_machine_fields is not exactly {{'risks_identified'}}, got {rec}"
  assert "risks_identified" not in req, "FAIL: risks_identified declared as required -- the validator's check is conditional on confidence"
  assert req == {"artifact_id", "decision", "confidence", "created_at", "created_by"}, \
      "FAIL: an existing required field on architectural_review_recommendation was changed"

  um = by_id["unknowns_map"]
  um_fields = set(um.get("required_machine_fields") or []) | set(um.get("recommended_machine_fields") or [])
  assert "risks_identified" not in um_fields, \
      "FAIL: risks_identified declared on unknowns_map -- wrong artifact (confused with its own 'Risks' required section)"

  for other_id, other in by_id.items():
      if other_id == "architectural_review_recommendation":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert "risks_identified" not in other_fields, \
          f"FAIL: risks_identified also/instead declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"architectural_review_recommendation"}, \
      f"FAIL: diff touches artifact block header(s) other than architectural_review_recommendation: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator's warning appears only post-edit
  FIXTURE = CLONE / "artifacts" / "architectural_review_recommendation.md"
  FIXTURE.write_text(
      "# Architectural Review Recommendation (fixture)\n\n"
      "## Summary\nShort.\n\n"
      "## Analysis\nShort.\n\n"
      "## Recommendation\nShort.\n\n"
      "## Machine Readable Decision\n\n"
      "```yaml\n"
      "artifact_id: architectural_review_recommendation\n"
      "decision: defer\n"
      "confidence: low\n"
      "reversal_conditions:\n"
      "  - \"Condition one\"\n"
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
      f"FAIL: generic validator should still exit 0 (risks_identified is recommended, not required):\n{result.stdout}"
  assert "risks_identified" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field risks_identified:\n{result.stdout}"

  # 3b. Corroborating (not decisive) evidence: the specialized validator independently
  # confirms risks_identified is a real, enforced field for low/medium-confidence
  # recommendations -- unaffected by the contract edit either way, run only to establish
  # the field is not fabricated.
  spec_result = subprocess.run(
      [sys.executable, "scripts/validate-architectural-review-recommendation.py", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert spec_result.returncode == 1 and "risks_identified" in spec_result.stdout, \
      f"FAIL: specialized validator no longer independently confirms risks_identified matters (environment assumption broken):\n{spec_result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised. (Verified by hand: running this exact fixture and generic-validator invocation against the frozen-SHA scripts confirms `[WARN] MISSING_RECOMMENDED_FIELD: Recommended field missing: risks_identified` with exit 0 once the field is declared recommended, and the specialized validator independently reports `Field: risks_identified` with exit 1 on the same fixture, both unaffected by the contract edit.)

  Negative cases (must be rejected):
  - **Declared as required instead of recommended**: fails the required-field assertion; would make every existing high-confidence `architectural_review_recommendation` artifact (which the validator never demands this field for) non-compliant with the contract.
  - **Declared on `unknowns_map` instead of (or as well as) `architectural_review_recommendation`**: fails the `unknowns_map`-disjointness assertion -- the deliberate trap is that artifact's own required section literally named "Risks", which is a different signal about a different artifact.
  - **Declared on multiple artifacts (hedging)**: fails the per-artifact attribution loop, which rejects any artifact other than `architectural_review_recommendation` carrying the field.
  - **Wrong field name** (e.g. `risks`, `identified_risks`, `risk_list`): fails both the attribution assertion and the fixture warning-text assertion, since the fixture check greps for the literal string `risks_identified`.
  - **Editing the specialized validator or the template instead of the contract**: leaves `artifact-contracts.yaml` unchanged, so assertion 1 fails outright; the task is specifically about the contract file.
oracle_spec_sha256: efe3c2164a52739977eafd87be53873dff61c38a7f3e513969b00f3317bec053
complexity_breakdown: |
  Two reasoning hops: (1) read the specialized validator's source to find a conditional (confidence-dependent) check that names a field never declared anywhere in the contract, and cross-reference the artifact's own template to confirm the field's real name and its author's stated scope ("recommended for all outcomes"); (2) resist two plausible near-misses the task text deliberately leaves for the agent to resolve -- declaring the field required (since the validator's check reads as a hard failure for low/medium confidence) instead of recommended, and placing it on `unknowns_map` (whose own required section is literally named "Risks") instead of `architectural_review_recommendation` (where the check and the template both actually live).

  Not HIGH: exactly one artifact's validator enforces this field, and exactly one correct requiredness once the validator's conditional nature is understood -- no cross-file runtime tuple or multi-artifact coordinated edit is required. Not trivial: the field is named in neither the task text nor the contract, the validator's check is nested inside a confidence branch unrelated to the artifact's other, better-known conditional fields, and a real required section on a different, real diagnostic artifact ("Risks" on `unknowns_map`) sits right there as a plausible wrong home.
complexity_breakdown_sha256: 9cc4ee577ae904611194194279a9a71774c406155f88de4153488601f17f54f1
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `architectural_review_recommendation` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/architectural_review_recommendation.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: e00ead817c03091fcfdca7d3866a794d3b0b48abea671961d2414104122c176b
qualification: |
  ADMISSIBLE
