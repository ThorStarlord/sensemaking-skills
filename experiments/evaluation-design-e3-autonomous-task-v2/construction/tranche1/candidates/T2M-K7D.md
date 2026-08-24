candidate_id: T2M-K7D
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's unknowns-mapper skill produces an `unknowns_map` artifact with a "Machine-readable routing" YAML block (its Section 7) at the end. That block already gives downstream consumers a lightweight numeric signal for two of the artifact's required content sections -- a count of open unknowns and a count of stated assumptions -- both declared as required machine fields in this artifact's entry in `skills/workflow-planner/references/artifact-contracts.yaml`.

  The artifact has a third, structurally parallel required section that enumerates open items the same way (risks), but the contract currently gives a downstream consumer no equivalent numeric field to read for it -- anyone wanting a quick "how many risks were flagged" signal has to parse prose instead of reading a machine field.

  Add one new machine field to the `unknowns_map` artifact's own contract entry that closes this gap, following the exact naming convention already used by its two sibling count fields. The new field must be declared as a RECOMMENDED (optional) machine field, not required -- every `unknowns_map` artifact already produced under the current contract lacks this field, and declaring it required would make all of them non-compliant overnight.

  Do not change the requiredness or presence of any existing field on `unknowns_map` or on any other artifact. Do not add or modify any other artifact's contract entry. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: effe60ba37483bdd4687eee8a800a2b8e57f06914b380621035e47d0476e85bd
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `unknowns_map`'s contract block (`artifact-contracts.yaml`, id `unknowns_map`) declares `required_machine_fields: [clarity_assessment, unknowns_count, assumptions_count, research_needed]` and has no `recommended_machine_fields` key at all. Its two validators are `scripts/validate-unknowns-map.py` (specialized) and `scripts/validate-artifact.py` (generic). Read in full: `validate-unknowns-map.py` hardcodes its own `required_fields = ["clarity_assessment", "unknowns_count", "assumptions_count", "research_needed"]` list independently of the contract file -- it does not load `artifact-contracts.yaml` at all, so it is unaffected by this task's edit either way (correctly: the task never asks anyone to touch that script). `validate-artifact.py`, by contrast, dynamically loads `recommended_machine_fields` from the contract via `_validator_utils.load_artifact_contracts` and emits a `MISSING_RECOMMENDED_FIELD` warning (not a hard error; exit code unaffected) for each declared-but-absent recommended field -- this is the authoritative, live check that this task's contract edit is real and load-bearing, not decorative.

  Expected field name: `risks_count` (the only name consistent with the stated naming convention of the sibling fields `unknowns_count` / `assumptions_count` for the sibling section `risks`).

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
  um = by_id["unknowns_map"]
  assert "risks_count" in (um.get("recommended_machine_fields") or []), \
      "FAIL: risks_count not declared as a recommended machine field on unknowns_map"
  assert "risks_count" not in (um.get("required_machine_fields") or []), \
      "FAIL: risks_count declared as required -- would break every existing unknowns_map artifact lacking it"
  assert set(um.get("required_machine_fields") or []) == {"clarity_assessment", "unknowns_count", "assumptions_count", "research_needed"}, \
      "FAIL: an existing required field on unknowns_map was changed"
  for other_id, other in by_id.items():
      if other_id == "unknowns_map":
          continue
      assert "risks_count" not in (other.get("required_machine_fields") or []) + (other.get("recommended_machine_fields") or []), \
          f"FAIL: risks_count also/instead declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK -- every other artifact block byte-identical to frozen SHA
  diff = subprocess.run(
      ["git", "diff", "--unified=0", "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5", "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"unknowns_map"}, f"FAIL: diff touches artifact block header(s) other than unknowns_map: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- the generic validator is contract-driven; prove
  #    the new field is live by observing its warning appear only post-edit.
  FIXTURE = CLONE / "artifacts" / "unknowns_map.md"
  FIXTURE.write_text(
      "# Unknowns Map (fixture)\n\n"
      "## 1. Knowns\nWhat is already established.\n\n"
      "## 2. Unknowns\nOpen question one. Open question two. Open question three.\n\n"
      "## 3. Assumptions\nAssumption one. Assumption two.\n\n"
      "## 4. Risks\nRisk one.\n\n"
      "## 5. Research Paths\nHow to resolve the unknowns above.\n\n"
      "## 6. Stopping Rule\nWhen to stop researching and proceed.\n\n"
      "## 7. Machine-readable routing\n\n"
      "```yaml\n"
      "clarity_assessment: medium\n"
      "unknowns_count: 3\n"
      "assumptions_count: 2\n"
      "research_needed: true\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "unknowns_map", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, f"FAIL: generic validator should still exit 0 (risks_count is recommended, not required):\n{result.stdout}"
  assert "risks_count" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field risks_count -- field is not actually live:\n{result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions above hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Declared as required instead of recommended**: fails assertion 1 directly (`risks_count` present in `required_machine_fields`); would also make `validate-artifact.py` hard-fail every existing `unknowns_map` artifact that lacks it.
  - **Declared on a different, structurally-similar diagnostic artifact** (e.g. `problem_frame`, which sits at a similar early pipeline stage but has no `risks` section at all): fails the per-artifact attribution loop in assertion 1 and produces no warning-text change in the fixture check for `unknowns_map`.
  - **Wrong field name** (e.g. `risk_count` singular, or `num_risks`): fails both the attribution assertion and the fixture warning-text assertion, since the fixture check greps for the literal string `risks_count`.
  - **Editing `scripts/validate-unknowns-map.py`'s hardcoded field list instead of (or as well as) the contract**: `artifact-contracts.yaml`'s `unknowns_map` block is left without the correctly attributed field, so assertion 1 still fails; this specialized validator is contract-independent by design (verified by reading it) and was never the right place to make this change.
oracle_spec_sha256: 5bfc67a8940f68e8c31bc64a078712cbe437f0bb50db98901e12fe0866e9e161
complexity_breakdown: |
  Two reasoning hops, neither trivial: (1) recognize that `unknowns_map`'s existing `unknowns_count`/`assumptions_count` fields establish a naming and requiredness convention that the `risks` section lacks a counterpart for, and infer the correct new field name (`risks_count`) from that convention rather than being told it; (2) recognize that of the artifact's two validators, only the generic one (`validate-artifact.py`) is contract-driven -- the specialized one hardcodes its own field list and is a plausible-but-wrong place to make this change, since editing it alone would not touch the contract at all and would leave the actual required deliverable (a declared contract field) missing.

  Not HIGH: no cross-file runtime-tuple update is required (unlike a routing-field alias), and there is exactly one artifact block that plausibly owns this field once the `risks` section is noticed -- no genuine multi-artifact ambiguity to resolve, just a single naming/placement/requiredness decision. Not trivial: the task never names the field or the file to avoid touching, and the "recommended vs required" distinction is a real trap given that both sibling fields are required.
complexity_breakdown_sha256: 3e2c06cf4d360ef6194023a95bbeff54195b19265e4407ff32262c56a338f56f
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `unknowns_map` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/unknowns_map.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: 0007d4bfed4f6006aaf2a417aad26a34a68636e94492a5e688a3746a5df9fea6
qualification: |
  ADMISSIBLE
