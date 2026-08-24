candidate_id: T2H-Q5X
family: T2
complexity_level: HIGH
task_text: |
  This repository's ticketing pipeline runs `issue_list` (produced by `to-issues`) through `triage`, whose own output artifact is `agent_brief` -- the brief the TDD implementation agent actually works from. Read `issue_list`'s and `agent_brief`'s own entries in `skills/workflow-planner/references/artifact-contracts.yaml`.

  `issue_list` already requires two machine fields together, as a pair: one recording whether a scope expansion beyond the original ask was proposed for an item, and a second, separate one recording its current approval status (a small state -- exact match to the original ask, still awaiting approval, approved, or diverged). Once `triage` turns an approved (or still-pending) scope-expansion issue into an `agent_brief`, this signal is silently dropped: `agent_brief`'s own contract entry currently requires only a single field, unrelated to scope expansion, and the implementing agent reading the brief has no contractual guarantee it will learn whether the ticket in front of it carries an unresolved or approved scope change.

  Close this gap: add BOTH of `issue_list`'s scope-expansion fields -- the proposed-flag and the status field, exactly that pair, no more -- to `agent_brief`'s own contract entry as RECOMMENDED (not required) machine fields. Recommended, because every `agent_brief` already produced under the current contract lacks them, and because not every ticket involves a scope expansion in the first place -- making them required would force every ordinary, non-expansion ticket's brief to carry meaningless placeholder values.

  Do not add `issue_list`'s other required fields (the ones about matching the original user goal, or the source-intent reference) to `agent_brief` -- this task is specifically about the scope-expansion signal, not general provenance tracking. Do not modify `issue_list`'s own contract entry -- it is already correct as-is. Do not add these fields to `code_patch` (the artifact `tdd` itself produces one step later) or to any other artifact. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: 86a8764cf97b95eef37124cf6e06932d4f3acf08116f0591e290b9e27bae9e13
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `issue_list`'s contract block declares `required_machine_fields: [source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_status]`. `agent_brief`'s contract block (`produced_by: triage`, `consumed_by: [tdd]`) currently declares only `required_machine_fields: [source_intent_ref]` and has no `recommended_machine_fields` key at all. `code_patch` (produced by `tdd`, one further hop downstream of `agent_brief`) has no machine fields declared either. This is a real relationship between two contract blocks connected by the `to-issues` -> `triage` producer chain, not a fabricated one -- both field lists are read directly from the frozen-SHA file. Note: `prd` (upstream of `issue_list`) also already carries both field *names* in the frozen baseline (`scope_expansion_proposed` required, `scope_expansion_status` recommended) -- this is pre-existing and unrelated to this task; the oracle accounts for it explicitly rather than treating `prd` as "yet another unrelated artifact that must stay disjoint from these field names."

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  EXPECTED = {"scope_expansion_proposed", "scope_expansion_status"}

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}

  ab = by_id["agent_brief"]
  rec = set(ab.get("recommended_machine_fields") or [])
  req = set(ab.get("required_machine_fields") or [])
  assert EXPECTED <= rec, f"FAIL: not both scope-expansion fields declared recommended on agent_brief; missing {EXPECTED - rec}"
  assert rec == EXPECTED, f"FAIL: agent_brief's recommended_machine_fields is not exactly {EXPECTED}, got {rec}"
  assert req == {"source_intent_ref"}, "FAIL: agent_brief's required_machine_fields was changed"
  assert EXPECTED.isdisjoint(req), "FAIL: one or both scope-expansion fields declared required instead of recommended"
  assert "user_goal_preserved_as" not in (rec | req), \
      "FAIL: user_goal_preserved_as (explicitly out of scope for this task) was also added to agent_brief"

  il = by_id["issue_list"]
  assert set(il.get("required_machine_fields") or []) == {
      "source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_status",
  }, "FAIL: issue_list's contract entry was modified -- it was already correct"

  # prd (upstream of issue_list) already legitimately carries both scope-expansion field
  # names in the frozen baseline (scope_expansion_proposed required, scope_expansion_status
  # recommended) -- verified directly in the frozen-SHA contract file. That pre-existing,
  # unrelated fact must not be disturbed, and prd is excluded from the "no other artifact
  # carries these fields" sweep below for that reason -- it is not evidence the agent
  # touched prd, only that the fields were already there before this task.
  prd = by_id["prd"]
  assert set(prd.get("required_machine_fields") or []) == {
      "source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_requires_approval",
  }, "FAIL: prd's required_machine_fields was changed -- prd is out of scope for this task"
  assert set(prd.get("recommended_machine_fields") or []) == {
      "scope_expansion_status", "scope_expansion_details", "scope_expansion_approvals",
  }, "FAIL: prd's recommended_machine_fields was changed -- prd is out of scope for this task"

  cp = by_id["code_patch"]
  cp_fields = set(cp.get("required_machine_fields") or []) | set(cp.get("recommended_machine_fields") or [])
  assert EXPECTED.isdisjoint(cp_fields), \
      f"FAIL: scope-expansion field(s) also declared on code_patch (one hop too far downstream): {EXPECTED & cp_fields}"

  for other_id, other in by_id.items():
      if other_id in ("agent_brief", "issue_list", "prd"):
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert EXPECTED.isdisjoint(other_fields), \
          f"FAIL: scope-expansion field(s) also declared on unrelated artifact {other_id!r}: {EXPECTED & other_fields}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"agent_brief"}, f"FAIL: diff touches artifact block header(s) other than agent_brief: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator warns on both, still exits 0
  FIXTURE = CLONE / "artifacts" / "agent_brief.md"
  FIXTURE.write_text(
      "# Agent Brief (fixture)\n\n"
      "## Summary\nShort.\n\n"
      "```yaml\n"
      "artifact_id: agent_brief\n"
      "source_intent_ref: 00-user-intent.md\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "agent_brief", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (both fields recommended, not required):\n{result.stdout}"
  for f in EXPECTED:
      assert f in result.stdout, f"FAIL: generic validator does not warn about missing recommended field {f!r}:\n{result.stdout}"
  assert result.stdout.count("MISSING_RECOMMENDED_FIELD") >= 2, \
      f"FAIL: expected at least 2 MISSING_RECOMMENDED_FIELD warnings, got:\n{result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Only one of the two fields added** (most plausibly just `scope_expansion_status`, since it alone is more directly actionable than the boolean flag): fails the `rec == EXPECTED` exact-pair assertion.
  - **Declared as required instead of recommended**: fails the disjointness-against-`req` assertion; would force every ordinary non-expansion ticket's `agent_brief` to carry a meaningless value.
  - **`user_goal_preserved_as` also copied over** (a plausible over-broad "just mirror issue_list's provenance fields" reading): fails the dedicated `user_goal_preserved_as not in (rec | req)` assertion.
  - **Added to `code_patch` instead of (or as well as) `agent_brief`** (propagating one hop too far downstream): fails the `code_patch`-disjointness assertion.
  - **`issue_list` itself also edited** (e.g. to "tidy" the pair there too): fails the `issue_list`-unchanged assertion; it was already correct and the task explicitly says not to touch it.
  - **Declared on an unrelated artifact instead of agent_brief**: fails the per-artifact attribution loop.
oracle_spec_sha256: 4ef09871e78e6ab5b9aa0f4a1e48081029a44f9030366457912c2d170edce050
complexity_breakdown: |
  Beyond a MEDIUM single-block candidate, this task requires: (1) correctness that genuinely depends on a relationship between TWO different contract blocks (`issue_list` and `agent_brief`) connected by a real producer/consumer chain (`to-issues` -> `triage` -> `agent_brief`), not a single block read in isolation; (2) adding a matched PAIR of fields together while explicitly resisting a plausible third field from the very same source block (`user_goal_preserved_as`) that the task text names and rules out -- a richer near-miss space than a single-field MEDIUM edit; (3) reasoning about the correct stopping point in a three-artifact pipeline chain (`issue_list` -> `agent_brief` -> `code_patch`), since the same over-broad "propagate everything downstream" instinct that produces the `user_goal_preserved_as` near-miss could equally produce a `code_patch` near-miss one hop further along.

  Not manufactured-obscure: every fact cited (`issue_list`'s four required fields, `agent_brief`'s current single-field contract, the `triage` producer relationship, `code_patch`'s position one hop further downstream) is directly readable in one file. Not MEDIUM: T2M-R9W in this same set already demonstrates the "compare two blocks, edit one, verify the other" MEDIUM shape on a different field (`scope_expansion_status` alone, promoted on `prd`); this task requires a two-field coordinated addition to a different, previously-untouched block, with a wider and more textually-tempting negative-case set spanning three artifacts instead of two.
complexity_breakdown_sha256: 947c1178bdcaa0590bf2d0b3d95a870198f4cf436e2581e03251cce84868e482
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `agent_brief` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/agent_brief.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: aeb96fc220a91918a32f3e5c447baa0e35d4354f0bb9bb8f7c439bbf39bd2fc7
qualification: |
  ADMISSIBLE
