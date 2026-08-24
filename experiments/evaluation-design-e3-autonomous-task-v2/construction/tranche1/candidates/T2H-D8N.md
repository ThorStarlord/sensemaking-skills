candidate_id: T2H-D8N
family: T2
complexity_level: HIGH
task_text: |
  This repository's specialized validator for the `user_intent` artifact (`scripts/validate-user-intent.py`) contains a check, applied only when a field is actually present in the artifact's YAML block, that a specific small group of optional machine fields must each be a list, not a scalar or mapping, whenever a producer includes them. Read the validator's source yourself to find this check and the exact set of field names it names together, in one place, as a group.

  None of these fields appears anywhere in `user_intent`'s own contract entry in `skills/workflow-planner/references/artifact-contracts.yaml` -- not as required, not as recommended. Two of the fields in the group correspond to prose sections the contract already requires `user_intent` to have (so the underlying content already has to exist somewhere in the artifact); the third corresponds to no required section at all. All of them nonetheless receive this same type-checking treatment from the validator, as a single group, whenever a producer happens to include them in the machine-readable block.

  Declare the exact set of fields the validator's type check names -- no more, no fewer -- as RECOMMENDED (not required) machine fields on `user_intent`'s own contract entry. Recommended, because the validator's check is conditional on presence: it never demands these fields exist, only that they have the right shape when a producer chooses to include them, and declaring them required would make every existing `user_intent` artifact that lacks them non-compliant overnight.

  Do not add any of these fields to any other artifact's contract entry -- including the artifact that records amendments to `user_intent`, which has a similarly-named field of its own describing the *type* of a single clarification (not a list of them); that is a different concept and is not one of the fields this task is about. Do not change the requiredness of any of `user_intent`'s six existing required machine fields. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: 7715205324620c5c5518b082f08979a8a4ad3def102351229074d021d5f7d55b
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `scripts/validate-user-intent.py`'s `validate_user_intent()` has a block (step 8) reading `for list_field in ['constraints', 'non_goals', 'clarifications']: if list_field in artifact and not isinstance(artifact.get(list_field), list): errors.append(...)`. This is the one place these three field names are named together. `user_intent`'s contract block (`required_sections: [raw_intent, scope_mode, intent_source, constraints, non_goals, machine_readable_intent]`, `required_machine_fields: [artifact_id, intent_source, scope_mode, raw_problem_statement, created_at, immutable]`) has `constraints` and `non_goals` as required *sections* but declares no `recommended_machine_fields` key at all; `clarifications` is not a required section either. `user_intent_amendment` has a required field `clarification_type` (singular, an enum of change-type strings) -- textually adjacent but a different concept from the plural `clarifications` list this task is about.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  EXPECTED = {"constraints", "non_goals", "clarifications"}

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  ui = by_id["user_intent"]
  rec = set(ui.get("recommended_machine_fields") or [])
  req = set(ui.get("required_machine_fields") or [])
  assert EXPECTED <= rec, f"FAIL: not all three fields declared recommended on user_intent; missing {EXPECTED - rec}"
  assert rec == EXPECTED, f"FAIL: user_intent's recommended_machine_fields is not exactly {EXPECTED}, got {rec}"
  assert req == {"artifact_id", "intent_source", "scope_mode", "raw_problem_statement", "created_at", "immutable"}, \
      "FAIL: an existing required field on user_intent was changed"
  assert EXPECTED.isdisjoint(req), "FAIL: one or more of the three fields declared required instead of recommended"

  uia = by_id["user_intent_amendment"]
  uia_fields = set(uia.get("required_machine_fields") or []) | set(uia.get("recommended_machine_fields") or [])
  assert EXPECTED.isdisjoint(uia_fields), \
      f"FAIL: one or more of the three fields also declared on user_intent_amendment (confused with its own clarification_type field): {EXPECTED & uia_fields}"
  assert "clarification_type" in (uia.get("required_machine_fields") or []), \
      "FAIL: sanity check -- user_intent_amendment's own unrelated field was unexpectedly removed"

  for other_id, other in by_id.items():
      if other_id == "user_intent":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert EXPECTED.isdisjoint(other_fields), \
          f"FAIL: one or more of the three fields declared on unrelated artifact {other_id!r}: {EXPECTED & other_fields}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"user_intent"}, f"FAIL: diff touches artifact block header(s) other than user_intent: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator warns on all three, still exits 0
  FIXTURE = CLONE / "artifacts" / "user_intent.md"
  FIXTURE.write_text(
      "# User Intent (fixture)\n\n"
      "## Raw Intent\nShort.\n\n"
      "## Scope Mode\nsoft\n\n"
      "## Intent Source\nuser_problem_statement\n\n"
      "## Constraints\nShort.\n\n"
      "## Non Goals\nShort.\n\n"
      "## Machine Readable Intent\n\n"
      "```yaml\n"
      "artifact_id: user_intent\n"
      "intent_source: user_problem_statement\n"
      "scope_mode: soft\n"
      "raw_problem_statement: Short problem statement.\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "immutable: true\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "user_intent", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (all three fields recommended, not required):\n{result.stdout}"
  for f in EXPECTED:
      assert f in result.stdout, f"FAIL: generic validator does not warn about missing recommended field {f!r}:\n{result.stdout}"
  assert result.stdout.count("MISSING_RECOMMENDED_FIELD") >= 3, \
      f"FAIL: expected at least 3 MISSING_RECOMMENDED_FIELD warnings, got:\n{result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Only 2 of the 3 fields declared** (most plausibly omitting `clarifications`, since unlike `constraints`/`non_goals` it has no matching required section to anchor it): fails the `rec == EXPECTED` exact-set assertion.
  - **Declared as required instead of recommended**: fails the disjointness assertion against `req`; would also make every existing minimal `user_intent` artifact non-compliant, since the validator itself never demands these fields' presence.
  - **Declared on `user_intent_amendment` instead of (or as well as) `user_intent`**: fails the `uia_fields` disjointness assertion -- the deliberate trap is `clarification_type` (singular, an enum) being mistaken for the plural `clarifications` (a list) this task is about.
  - **A fourth, invented field added alongside the correct three** (or one of the three replaced with a near-synonym, e.g. `non_goal` singular): fails the `rec == EXPECTED` exact-set assertion.
oracle_spec_sha256: 86da4731f5f478f92cdf2641e4a296ce6c190fcde2f8d968e4b0e2434122cbd0
complexity_breakdown: |
  Beyond a MEDIUM single-field candidate, this task requires: (1) deriving an exact SET of three fields (not one) from a single Python list literal buried in a specialized validator's optional/conditional branch, rather than pattern-matching one obvious sibling field by naming convention; (2) a genuinely richer near-miss space -- at least four independently-checked wrong answers (partial set, wrong requiredness, wrong artifact via a deceptively similar field name on a related artifact, extra/substituted field) versus a MEDIUM candidate's single near-miss; (3) resolving an internal asymmetry within the evidence itself -- two of the three fields have textual precedent via existing required sections, the third does not -- forcing the agent to trust the validator's source code as ground truth over the more visible section-based convention, rather than simply extending an existing pattern.

  Not manufactured-obscure: every fact cited (the validator's exact Python list, the contract's total absence of `recommended_machine_fields`, the section-precedent asymmetry, `user_intent_amendment`'s adjacent-but-distinct field) is directly verifiable by reading two files at fixed, named locations.
complexity_breakdown_sha256: 375a1228ce3dcc94c36488efc128957244ee9b8ddaa6b73db41d5937756dec09
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `user_intent` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/user_intent.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: eec63b5db8c575cbdb58cb96330285bfc2186624a455d074a6fc9368cf8afe07
qualification: |
  ADMISSIBLE
