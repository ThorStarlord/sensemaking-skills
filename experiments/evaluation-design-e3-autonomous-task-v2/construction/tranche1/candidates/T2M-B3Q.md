candidate_id: T2M-B3Q
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's specialized validator for the `architectural_review_recommendation` artifact (`scripts/validate-architectural-review-recommendation.py`) already hard-fails an artifact whose `decision` field starts with "pursue" (i.e. `pursue` or `pursue_narrowed`) if it lacks a structured field defining how success will be measured -- a metric, a baseline, a target, and a measurement method. Read the validator's source to confirm this yourself; it is a real, currently-enforced requirement on the artifact's producer, not a hypothetical one.

  Despite this, the artifact's own entry in `skills/workflow-planner/references/artifact-contracts.yaml` never declares this field at all -- neither as required nor recommended -- so nothing in the contract documents this real validator behavior, and a producer relying only on the contract (not the validator's source code) would never learn this field exists.

  Close this documentation gap: declare the field the validator already checks for as a RECOMMENDED (not required) machine field on the `architectural_review_recommendation` artifact's own contract entry. Not required, because the validator only demands it conditionally -- decisions that don't start with "pursue" never need it -- matching how this repository already documents other conditionally-needed fields elsewhere as recommended rather than required.

  Do not declare the field on any other artifact's contract entry, including one whose required section names sound similar but which is not this field's actual home. Do not change any other field's requiredness on `architectural_review_recommendation`. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: d2e1462c3bb5a18312ddac62831f0e9adc51e33541c3bfdb72591a3be68a4ce0
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `architectural_review_recommendation`'s contract block declares `required_machine_fields: [artifact_id, decision, confidence, created_at, created_by]` and has no `recommended_machine_fields` key at all. `scripts/validate-architectural-review-recommendation.py` (specialized), read in full, hardcodes its own checks independently of the contract file -- including, near the end of `validate_architectural_review_recommendation()`, a check that appends a hard error (`error_id: "architectural_review_recommendation.success_measures.missing_field"`, unconditionally counted in the returned `errors` list, which the CLI's `main()` treats as failure) whenever `decision` starts with `"pursue"` and `success_measures` is absent or not a dict. Because this validator does not read `artifact-contracts.yaml` at all, its own pass/fail behavior is unaffected by this task's edit either way -- it is cited here only as independent, already-real evidence that `success_measures` is a genuine, currently-enforced field and not a fabricated one, per the field-contract-agreement principle in this repo's `CLAUDE.md` ("if you add a new field-read alias to the runtime, declare it in a contract too").

  `scripts/validate-artifact.py` (generic), by contrast, IS contract-driven: it dynamically loads `recommended_machine_fields` and emits a `MISSING_RECOMMENDED_FIELD` warning (not a hard error) for each declared-but-absent one. This is the check whose output changes as a live, observable consequence of this task's contract edit.

  A plausible, textually motivated near-miss exists: `proposed_direction`'s contract block has a required section literally named `success_criteria`, and `proposed_direction` is architectural-review's own upstream input -- an agent could mistakenly attach the new field there instead.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  arr = by_id["architectural_review_recommendation"]
  assert "success_measures" in (arr.get("recommended_machine_fields") or []), \
      "FAIL: success_measures not declared as a recommended machine field on architectural_review_recommendation"
  assert "success_measures" not in (arr.get("required_machine_fields") or []), \
      "FAIL: success_measures declared as required -- the validator only demands it conditionally"
  assert set(arr.get("required_machine_fields") or []) == {"artifact_id", "decision", "confidence", "created_at", "created_by"}, \
      "FAIL: an existing required field on architectural_review_recommendation was changed"

  pd = by_id["proposed_direction"]
  assert "success_measures" not in (pd.get("required_machine_fields") or []) + (pd.get("recommended_machine_fields") or []), \
      "FAIL: success_measures declared on proposed_direction -- wrong artifact (confused with its 'success_criteria' section)"

  for other_id, other in by_id.items():
      if other_id == "architectural_review_recommendation":
          continue
      assert "success_measures" not in (other.get("required_machine_fields") or []) + (other.get("recommended_machine_fields") or []), \
          f"FAIL: success_measures also/instead declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5", "--",
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
      "decision: pursue\n"
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
      f"FAIL: generic validator should still exit 0 (success_measures is recommended, not required):\n{result.stdout}"
  assert "success_measures" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field success_measures -- not actually live:\n{result.stdout}"

  # 3b. Corroborating (not decisive) evidence: the specialized validator independently
  # confirms success_measures is a real, enforced field for pursue decisions -- unaffected
  # by the contract edit either way, run only to establish the field is not fabricated.
  spec_result = subprocess.run(
      [sys.executable, "scripts/validate-architectural-review-recommendation.py", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert spec_result.returncode == 1 and "success_measures" in spec_result.stdout, \
      f"FAIL: specialized validator no longer independently confirms success_measures matters (environment assumption broken):\n{spec_result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Declared on `proposed_direction` instead of (or as well as) `architectural_review_recommendation`**: fails the `proposed_direction`-unchanged assertion -- the textually similar `success_criteria` section name is a deliberate trap, not the field's real home.
  - **Declared as required instead of recommended**: fails the required-field assertion; would make every existing `defer`/`reject`/`investigate_first` decision artifact (which the validator never demands this field for) non-compliant with the contract even though the validator itself never requires it for those decisions.
  - **Declared on multiple artifacts (hedging)**: fails the per-artifact attribution loop, which rejects any artifact other than `architectural_review_recommendation` carrying the field.
  - **Editing the specialized validator instead of the contract**: leaves `artifact-contracts.yaml` unchanged, so assertion 1 fails outright; the task is specifically about the contract file.
oracle_spec_sha256: 81c2f9917dd73c05c0c7c86952a0a79d16440aab91b639c54e696c3d07722679
complexity_breakdown: |
  Two reasoning hops: (1) read the specialized validator's source to discover a real, currently-enforced field requirement that has no matching contract declaration at all -- the task text describes the field's semantics (metric/baseline/target/measurement method) rather than naming it, so the agent must connect that description to the validator's actual field name; (2) resist the textually plausible but wrong near-miss of attaching the field to `proposed_direction`, whose required section is literally named `success_criteria` and which is architectural-review's own upstream input artifact -- correctly recognizing that a required *section name* on a different artifact is not evidence for where a *machine field* belongs.

  Not HIGH: once the validator source is read, there is exactly one artifact whose validator actually enforces the field, and exactly one correct requiredness (recommended, mirroring the field's conditional enforcement) -- no cross-file runtime tuple or multi-hop routing chain is involved. Not trivial: the field name is never stated, the contract currently gives zero hints (no existing `recommended_machine_fields` key to extend by analogy, unlike the other two T2M candidates in this set), and a genuinely similar-sounding section name on a different, closely related artifact sits right there as a trap.
complexity_breakdown_sha256: b5f23a2040e82c32196eeb9f047eda3ddac9778ee7a51784e801fe88c31ceddc
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `architectural_review_recommendation` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/architectural_review_recommendation.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: e00ead817c03091fcfdca7d3866a794d3b0b48abea671961d2414104122c176b
qualification: |
  ADMISSIBLE
