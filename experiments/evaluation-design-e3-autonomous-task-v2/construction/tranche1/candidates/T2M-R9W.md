candidate_id: T2M-R9W
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's pipeline routes a `prd` artifact (produced by the `to-prd` skill) downstream into an `issue_list` artifact (produced by `to-issues`). Read both artifacts' entries in `skills/workflow-planner/references/artifact-contracts.yaml`: `issue_list` already treats the field recording the current handling status of a proposed scope expansion -- whether it exactly matches the original ask, is still awaiting approval, has been approved, or has diverged from it -- as a REQUIRED machine field it cannot function without. But `prd`, the upstream artifact where this same status is first recorded, only lists the equivalent field as recommended (optional).

  Fix this asymmetry at its source: in the `prd` artifact's own contract entry, promote this specific field from recommended to required, so the guarantee a downstream consumer already depends on originates where the value is first decided, rather than being merely hoped for.

  Do not add, remove, or change the requiredness of any other field on `prd`. Do not modify `issue_list`'s contract entry -- it is already correct as-is. Do not modify any other artifact's contract entry. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: 59e2d018c1d5333990039eb95c53d4cd6bd06ee00eb52cc5821fe913ce9565b9
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `prd`'s contract block declares `required_machine_fields: [source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_requires_approval]` and `recommended_machine_fields: [scope_expansion_status, scope_expansion_details, scope_expansion_approvals]`. `issue_list`'s contract block declares `required_machine_fields: [source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_status]` -- `scope_expansion_status` is already required there. This asymmetry is real, not fabricated (both lists read directly from the frozen-SHA file).

  `scripts/validate-prd.py` (specialized) only validates `scope_expansion_status`'s *value* against `VALID_EXPANSION_STATUSES` when the field happens to be present in the YAML block (`status = meta.get("scope_expansion_status"); if status is not None and status not in VALID_EXPANSION_STATUSES: ...`) -- it never requires the field's presence itself, so its pass/fail behavior is unaffected by this task's edit either way. `scripts/validate-artifact.py` (generic), by contrast, dynamically loads `required_machine_fields` from the contract and hard-fails (`MISSING_MACHINE_FIELDS`, non-zero exit) an artifact missing any of them when the artifact is short (`line_count < 100`, so the large-artifact relaxation does not apply) -- this is the authoritative, live check that promoting the field to required actually changes enforced behavior.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"

  # 1. STRUCTURAL CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  prd = by_id["prd"]
  assert "scope_expansion_status" in (prd.get("required_machine_fields") or []), \
      "FAIL: scope_expansion_status not promoted to required on prd"
  assert "scope_expansion_status" not in (prd.get("recommended_machine_fields") or []), \
      "FAIL: scope_expansion_status still (also) listed as recommended on prd"
  assert set(prd.get("required_machine_fields") or []) == {
      "source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed",
      "scope_expansion_requires_approval", "scope_expansion_status",
  }, "FAIL: prd's required_machine_fields changed in an unexpected way"
  assert set(prd.get("recommended_machine_fields") or []) == {"scope_expansion_details", "scope_expansion_approvals"}, \
      "FAIL: prd's recommended_machine_fields changed in an unexpected way"

  il = by_id["issue_list"]
  assert set(il.get("required_machine_fields") or []) == {
      "source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_status",
  }, "FAIL: issue_list's contract entry was modified -- it was already correct"

  for other_id, other in by_id.items():
      if other_id in ("prd", "issue_list"):
          continue
      assert "scope_expansion_status" not in (other.get("required_machine_fields") or []) + (other.get("recommended_machine_fields") or []), \
          f"FAIL: scope_expansion_status also declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5", "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"prd"}, f"FAIL: diff touches artifact block header(s) other than prd: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator flips PASS/FAIL on a short fixture
  FIXTURE = CLONE / "artifacts" / "prd.md"
  FIXTURE.write_text(
      "# PRD (fixture)\n\n"
      "## Executive Summary\nShort.\n\n"
      "## User Goal\nShort.\n\n"
      "## Goal Preservation And Expansion\nShort.\n\n"
      "## Features\nShort.\n\n"
      "## Out Of Scope\nShort.\n\n"
      "## Acceptance Criteria\nShort.\n\n"
      "## Non Functional Requirements\nShort.\n\n"
      "## Machine Readable Handoff\n\n"
      "```yaml\n"
      "source_intent_ref: artifacts/user_intent.md\n"
      "user_goal_preserved_as: exact_match\n"
      "scope_expansion_proposed: false\n"
      "scope_expansion_requires_approval: false\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "prd", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 1, (
      f"FAIL: generic validator should now hard-fail this fixture (scope_expansion_status is "
      f"required and absent from its YAML block), got exit {result.returncode}:\n{result.stdout}"
  )
  assert "scope_expansion_status" in result.stdout and "MISSING_MACHINE_FIELDS" in result.stdout, \
      f"FAIL: failure is not attributed to the promoted field:\n{result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised. (A reference re-run of step 3 against the unmodified frozen-SHA contract on the same fixture exits 0 with only recommended-field warnings, confirming the flip is caused by this task's edit and not the fixture.)

  Negative cases (must be rejected):
  - **Promoting a neighboring field instead** (`scope_expansion_details` or `scope_expansion_approvals`, both plausible since they sit right next to the correct field in the same list): fails the structural assertions (wrong field promoted; `scope_expansion_status` stays recommended) and the fixture stays exit 0, since the field set that governs this fixture's omission never gains the required entry that matters.
  - **Also editing `issue_list`'s contract entry** (e.g. adding the field there again, or changing its requiredness): fails the `issue_list`-unchanged assertion; that artifact's contract was already correct and the task explicitly says not to touch it.
  - **Declaring the field required on an unrelated artifact instead of prd**: fails the per-artifact attribution loop.
  - **Removing the field from `prd` entirely instead of promoting it**: fails the required-field-presence assertion outright.
oracle_spec_sha256: be46653fbad974723ac193ae80486f3ade3d59dfd13051a75e3ea7f4c31fe486
complexity_breakdown: |
  Two reasoning hops: (1) locate the real requiredness asymmetry between `prd` and its downstream consumer `issue_list` by comparing two separate contract blocks rather than reading one in isolation -- the task text never names the field, only its meaning, so the agent must map that meaning to `scope_expansion_status` specifically and not one of its two textually adjacent siblings (`scope_expansion_details`, `scope_expansion_approvals`); (2) recognize the promotion must land only on `prd` (the producer where the value originates) and not be duplicated onto the already-correct `issue_list` entry.

  Not HIGH: a single, well-defined promotion within one contract block, with only one plausible correct field once its meaning is identified -- no runtime code path or cross-file tuple needs updating. Not trivial: two textually similar recommended-field siblings sit right next to the correct one, and the reasoning must cross two artifact blocks (prd and issue_list) to notice the asymmetry exists at all before making the edit in the right place.
complexity_breakdown_sha256: 631b1b953e3758f75911e4d2ee008eb059705041c61dda3f0abda268bfcc2af7
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `prd` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/prd.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: fa01c3b5636ac6ef0db2b8833def444d6ed75de62f26be67ed548a271fc63c60
qualification: |
  ADMISSIBLE
