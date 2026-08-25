candidate_id: T2M-J4K
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's orchestration runtime (`scripts/workflow-runtime.py`) contains the only code path that actually produces `user_intent_amendment` artifacts -- `OrchestrationRunner.create_intent_amendment()` -- matching this artifact's own `produced_by: orchestration-runner` entry in `skills/workflow-planner/references/artifact-contracts.yaml`. Read that method's source yourself.

  Every time this method runs, it writes a machine-readable field that mirrors the amendment's free-text clarification content into the artifact's YAML block -- the same pattern this repo already uses on `user_intent` itself, where the analogous prose is mirrored into a machine field carrying a `raw_` prefix. Despite this method being the artifact type's sole real producer and always writing this field, `user_intent_amendment`'s own contract entry never declares it -- neither as required nor recommended.

  The same method also writes a second field, an internal schema-version marker, that is likewise undeclared in the contract. That second field is OUT OF SCOPE for this task -- do not add it.

  Declare only the field that mirrors the clarification's prose content as a RECOMMENDED (not required) machine field on `user_intent_amendment`'s own contract entry. Recommended, not required, because this artifact type's specialized validator (`scripts/validate-user-intent-amendment.py`) never checks for this field's presence at all -- only the runtime's own current implementation happens to always include it, which is a property of today's code, not a validated contract guarantee.

  Do not declare this field on any other artifact's contract entry -- including `user_intent` itself, which already has its own, differently-named prose-mirroring field for a different section. Do not add the schema-version field mentioned above, and do not add, remove, or change the requiredness of any of `user_intent_amendment`'s six existing required machine fields. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: 4c5940ba9971d11c90fc7d89c5285043481202e6c6b0b4a4bccb330d00cfe986
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `user_intent_amendment`'s contract block declares `produced_by: orchestration-runner` and `required_machine_fields: [artifact_id, amends_intent_ref, clarification_type, requires_reroute, created_at, created_by]`, with no `recommended_machine_fields` key at all. `scripts/workflow-runtime.py`'s `OrchestrationRunner.create_intent_amendment(artifact_dir, clarification, clarification_type=...)` builds an `amendment_yaml` dict containing (verbatim from the source): `"artifact_id": "user_intent_amendment"`, `"schema_version": 1`, `"amends_intent_ref": "00-user-intent.md"`, `"raw_clarification": clarification`, `"clarification_type": clarification_type`, `"requires_reroute": True`, `"created_at": ...`, `"created_by": "user"`, and writes it verbatim (via `yaml.dump`) between `---`/`---` fences -- the exact frontmatter format `scripts/validate-user-intent-amendment.py`'s own YAML extraction regex (`re.search(r"---\s+(.*?)\s+---", ...)`) expects. `raw_clarification` and `schema_version` are both written on every call but neither is declared in the contract. `scripts/validate-user-intent-amendment.py`, read in full, hardcodes its own `required_fields` list identical to the contract's current six required fields and never inspects `raw_clarification` or `schema_version` at all -- its pass/fail behavior is unaffected by this task's edit either way.

  Expected field name: `raw_clarification` (the literal dict key the runtime writes; `schema_version` is the second, deliberately out-of-scope field the same method also writes).

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
  uia = by_id["user_intent_amendment"]
  rec = set(uia.get("recommended_machine_fields") or [])
  req = set(uia.get("required_machine_fields") or [])
  assert "raw_clarification" in rec, "FAIL: raw_clarification not declared as a recommended machine field on user_intent_amendment"
  assert rec == {"raw_clarification"}, f"FAIL: user_intent_amendment's recommended_machine_fields is not exactly {{'raw_clarification'}}, got {rec}"
  assert "raw_clarification" not in req, "FAIL: raw_clarification declared as required"
  assert "schema_version" not in (rec | req), "FAIL: schema_version (deliberately out of scope) was also added"
  assert req == {"artifact_id", "amends_intent_ref", "clarification_type", "requires_reroute", "created_at", "created_by"}, \
      "FAIL: an existing required field on user_intent_amendment was changed"

  ui = by_id["user_intent"]
  ui_fields = set(ui.get("required_machine_fields") or []) | set(ui.get("recommended_machine_fields") or [])
  assert "raw_clarification" not in ui_fields, \
      "FAIL: raw_clarification declared on user_intent -- wrong artifact (it has its own raw_problem_statement field for a different section)"

  for other_id, other in by_id.items():
      if other_id == "user_intent_amendment":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert "raw_clarification" not in other_fields, \
          f"FAIL: raw_clarification also/instead declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"user_intent_amendment"}, f"FAIL: diff touches artifact block header(s) other than user_intent_amendment: {touched}"

  runtime_diff = subprocess.run(
      ["git", "diff", "--stat", FROZEN_SHA, "--", "scripts/workflow-runtime.py"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout.strip()
  assert runtime_diff == "", f"FAIL: scripts/workflow-runtime.py was modified; this task only asks for a contract edit:\n{runtime_diff}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator warns only post-edit
  FIXTURE = CLONE / "artifacts" / "user_intent_amendment.md"
  FIXTURE.write_text(
      "# User Intent Amendment (fixture)\n\n"
      "---\n"
      "artifact_id: user_intent_amendment\n"
      "amends_intent_ref: 00-user-intent.md\n"
      "clarification_type: scope_refinement\n"
      "requires_reroute: true\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "created_by: oracle-fixture\n"
      "---\n\n"
      "## Clarification\n\nShort clarification text.\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "user_intent_amendment", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (raw_clarification is recommended, not required):\n{result.stdout}"
  assert "raw_clarification" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field raw_clarification:\n{result.stdout}"

  # 3b. Corroborating (not decisive) evidence: the runtime's own producer source still
  # writes raw_clarification literally -- unaffected by the contract edit either way, run
  # only to establish the field is not fabricated. (Deliberately a static source check,
  # not an executed call to create_intent_amendment: that method's own success-path print
  # statement contains a non-ASCII character that crashes on some platform stdout codecs,
  # an unrelated, pre-existing environment quirk this oracle must not depend on.)
  runtime_src = (CLONE / "scripts" / "workflow-runtime.py").read_text(encoding="utf-8")
  assert '"raw_clarification": clarification' in runtime_src, \
      "FAIL: runtime's create_intent_amendment no longer writes raw_clarification (environment assumption broken)"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised. (Verified by hand against the frozen-SHA scripts: declaring `raw_clarification` as recommended on `user_intent_amendment` produces `[WARN] MISSING_RECOMMENDED_FIELD: Recommended field missing: raw_clarification` with exit 0 from the generic validator on the fixture above, and the runtime source literally contains `"raw_clarification": clarification,` inside `create_intent_amendment`.)

  Negative cases (must be rejected):
  - **Declared as required instead of recommended**: fails the required-field assertion; the specialized validator never demands this field, so requiring it overstates a guarantee the contract doesn't actually enforce.
  - **`schema_version` also added** (a plausible over-broad "document everything the runtime writes" reading): fails the dedicated `schema_version not in (rec | req)` assertion.
  - **Declared on `user_intent` instead of (or as well as) `user_intent_amendment`**: fails the `user_intent`-disjointness assertion -- the deliberate trap is that `user_intent` already has its own, differently-named `raw_` field (`raw_problem_statement`) for a structurally similar but distinct purpose.
  - **Wrong field name** (e.g. `clarification_text`, `raw_intent`, or the section name `clarification` alone): fails both the attribution assertion and the fixture warning-text assertion.
  - **Editing `scripts/workflow-runtime.py`** (e.g. adding a comment or hint) instead of, or in addition to, editing the contract: fails the `runtime_diff == ""` assertion.
oracle_spec_sha256: 0111a6e586bc7cf11c665bd947df8cbff26382ec70ecb8958974a3b3a352f865
complexity_breakdown: |
  Two reasoning hops: (1) recognize that `user_intent_amendment`'s sole real producer is deterministic Python code (not an LLM-authored skill), read that code, and identify which of the two undeclared fields it writes is the one meant by "mirrors the clarification's prose content" (as opposed to the unrelated schema-version marker also present) -- inferring the field's exact name (`raw_clarification`) from both the source and its structural parallel to `user_intent`'s own `raw_problem_statement`; (2) resist two plausible near-misses -- also adding the out-of-scope `schema_version` field, and placing the new field on `user_intent` instead of `user_intent_amendment` since that is where the analogous `raw_` field already lives.

  Not HIGH: exactly one artifact's producer writes this field, and exactly one correct requiredness once the specialized validator's silence on it is understood -- no cross-file runtime tuple or multi-artifact coordinated edit is required. Not trivial: the field is named in neither the task text nor the contract, the runtime writes two undeclared fields at once (only one of which is in scope), and a real, differently-named sibling field on a different, closely related artifact (`user_intent`'s `raw_problem_statement`) sits right there as a plausible source of confusion about which artifact the new field belongs to.
complexity_breakdown_sha256: 162b491718abd50e85ccf5b8b57647b905b3b97031eaa3e9aa9212d0f46b97bf
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `user_intent_amendment` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/user_intent_amendment.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: 0322234c5bba23142ac5000c6aac3fc514163737b9a1d4de4c8e82a6826111e4
qualification: |
  ADMISSIBLE
