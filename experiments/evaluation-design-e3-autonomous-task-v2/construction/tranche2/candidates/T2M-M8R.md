candidate_id: T2M-M8R
family: T2
complexity_level: MEDIUM
task_text: |
  This repository's `issue_list` artifact (produced by `to-issues`) already has its own producer-facing template (`skills/to-issues/references/issue-list-template.md`), whose "Machine-Readable Handoff" section lays out the full YAML block a producer should emit -- including several fields this artifact's own entry in `skills/workflow-planner/references/artifact-contracts.yaml` does not currently declare at all.

  Most of those undeclared fields are out of scope for this task. Exactly one of them, however, sits in the same "divergence escalation" cluster as three fields the contract already protects as recommended machine fields: a flag for whether escalation is required, the reason for it, and the list of resolution options offered to the user. The template's own comment for this fourth, still-undeclared field describes it as recording who must act next when a divergence is flagged -- the user, or nobody.

  Declare only that fourth field as a new RECOMMENDED (not required) machine field on `issue_list`'s own contract entry, matching how its three siblings in the same escalation cluster are already declared recommended rather than required.

  Do not add any of the template's other undeclared fields (the ones covering issue counts, a schema-version marker, or the structured list of issues itself) -- they are unrelated to the escalation cluster and out of scope. Do not declare this field on any other artifact's contract entry -- in particular, do not add it to `agent_brief` (the artifact `issue_list` feeds into downstream, via `triage`): this signal belongs to `issue_list`'s own scope, and propagating it onto a downstream consumer is not part of this task. Do not add, remove, or change the requiredness of any of `issue_list`'s four existing required machine fields, or of its three existing recommended machine fields. Do not touch any file other than `skills/workflow-planner/references/artifact-contracts.yaml`.
task_text_sha256: fb7296567b1ca8ab3376ca46f6a3f3891e4baf961cc7e41ee56ac105fb955a89
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `issue_list`'s contract block declares `required_machine_fields: [source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_status]` and `recommended_machine_fields: [escalation_required, escalation_reason, escalation_options]`. `skills/to-issues/references/issue-list-template.md`, Section 9 "Machine-Readable Handoff", lists (verbatim, as commented placeholders) a larger YAML block: `artifact_id, schema_version, source_intent_ref, user_goal_preserved_as, scope_expansion_proposed, scope_expansion_status, issues_generated, core_issues_count, expansion_issues_count, escalation_required, escalation_reason, escalation_options, decision_required_from, issues, created_at`. Of these, `schema_version`, `issues_generated`, `core_issues_count`, `expansion_issues_count`, and `issues` are undeclared in the contract and are NOT part of the escalation cluster (they are deliberately out of scope for this task). `decision_required_from` is the one undeclared field that IS part of the escalation cluster: the template comments it as `# user (if divergence) | none`, immediately following `escalation_options` in the same block, in the same "If Divergence" narrative section (Section 8) of the template. `issue_list` has no specialized validator (only the generic, contract-driven one), so the authoritative live check is `scripts/validate-artifact.py`'s `MISSING_RECOMMENDED_FIELD` warning, exactly as for `issue_list`'s three existing recommended fields.

  The downstream artifact named in the task text as an explicit trap is `agent_brief`: its own contract entry already carries `scope_expansion_proposed` and `scope_expansion_status` (a *different* pair, for goal-preservation tracking, not escalation) as recommended fields, per this same experiment's separate T2H-Q5X candidate design -- an agent that over-generalizes "propagate `issue_list` signals downstream" could plausibly add `decision_required_from` there too. This oracle treats that as a genuine near-miss to reject, independent of whether `agent_brief`'s own contract entry has actually been edited to add that unrelated pair in any given run.

  Expected field name: `decision_required_from` (the literal key the template uses).

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  OUT_OF_SCOPE = {"schema_version", "issues_generated", "core_issues_count", "expansion_issues_count", "issues"}

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}
  il = by_id["issue_list"]
  rec = set(il.get("recommended_machine_fields") or [])
  req = set(il.get("required_machine_fields") or [])
  assert "decision_required_from" in rec, "FAIL: decision_required_from not declared as a recommended machine field on issue_list"
  assert rec == {"escalation_required", "escalation_reason", "escalation_options", "decision_required_from"}, \
      f"FAIL: issue_list's recommended_machine_fields is not exactly the escalation cluster plus decision_required_from, got {rec}"
  assert "decision_required_from" not in req, "FAIL: decision_required_from declared as required"
  assert req == {"source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_status"}, \
      "FAIL: an existing required field on issue_list was changed"
  assert rec.isdisjoint(OUT_OF_SCOPE), f"FAIL: one or more out-of-scope template fields were also added: {rec & OUT_OF_SCOPE}"

  ab = by_id["agent_brief"]
  ab_fields = set(ab.get("required_machine_fields") or []) | set(ab.get("recommended_machine_fields") or [])
  assert "decision_required_from" not in ab_fields, \
      "FAIL: decision_required_from declared on agent_brief -- wrong artifact (over-generalized from its own unrelated scope_expansion_proposed/status pair)"

  for other_id, other in by_id.items():
      if other_id == "issue_list":
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert "decision_required_from" not in other_fields, \
          f"FAIL: decision_required_from also/instead declared on unrelated artifact {other_id!r}"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= {"issue_list"}, f"FAIL: diff touches artifact block header(s) other than issue_list: {touched}"

  # 3. AUTHORITATIVE VALIDATOR CHECK -- generic validator warns only post-edit
  FIXTURE = CLONE / "artifacts" / "issue_list.md"
  FIXTURE.write_text(
      "# Issue List (fixture)\n\n"
      "## 1. PRD Consumed\n\nShort.\n\n"
      "```yaml\n"
      "artifact_id: issue_list\n"
      "source_intent_ref: 00-user-intent.md\n"
      "user_goal_preserved_as: exact_match\n"
      "scope_expansion_proposed: false\n"
      "scope_expansion_status: exact_match\n"
      "created_at: '2026-08-19T00:00:00Z'\n"
      "```\n",
      encoding="utf-8",
  )
  result = subprocess.run(
      [sys.executable, "scripts/validate-artifact.py", "issue_list", str(FIXTURE), "--repo-root", "."],
      cwd=CLONE, capture_output=True, text=True,
  )
  assert result.returncode == 0, \
      f"FAIL: generic validator should still exit 0 (decision_required_from is recommended, not required):\n{result.stdout}"
  assert "decision_required_from" in result.stdout and "MISSING_RECOMMENDED_FIELD" in result.stdout, \
      f"FAIL: generic validator does not warn about the missing recommended field decision_required_from:\n{result.stdout}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised. (Verified by hand against the frozen-SHA scripts: declaring `decision_required_from` as recommended on `issue_list` produces a `[WARN] MISSING_RECOMMENDED_FIELD: Recommended field missing: decision_required_from` line, among the other pre-existing escalation-cluster warnings, with exit 0 from the generic validator on the fixture above.)

  Negative cases (must be rejected):
  - **Declared as required instead of recommended**: fails the required-field assertion; breaks the established convention that this whole escalation cluster (its three existing siblings) is recommended, not required.
  - **One or more of the template's other undeclared fields also added** (`schema_version`, `issues_generated`, `core_issues_count`, `expansion_issues_count`, or `issues`): fails the `OUT_OF_SCOPE` disjointness assertion.
  - **Declared on `agent_brief` instead of (or as well as) `issue_list`**: fails the `agent_brief`-disjointness assertion -- the deliberate trap is that `agent_brief` already carries a different, unrelated pair of fields sourced from `issue_list`, inviting an over-generalized "propagate everything downstream" reading.
  - **Wrong field name** (e.g. `decision_required`, `escalation_decision_from`, or `action_required_from`): fails both the attribution assertion and the fixture warning-text assertion.
  - **Editing the template instead of the contract**: leaves `artifact-contracts.yaml` unchanged, so assertion 1 fails outright; the task is specifically about the contract file.
oracle_spec_sha256: 8ee6ab856218b5b09d07d8362a26d6bb68a484953ac532fe92d624f539290925
complexity_breakdown: |
  Two reasoning hops: (1) scan the artifact's own template for undeclared fields, then narrow a list of six candidates down to exactly one by recognizing which single field belongs to the already-partially-contracted "escalation cluster" (three siblings already recommended) rather than to the several unrelated undeclared fields (issue counts, schema version, the issues list itself) that share the same YAML block but not the same semantic cluster; (2) resist placing the field on `agent_brief` instead -- a plausible over-generalization of "propagate `issue_list`'s escalation signal downstream to the artifact that consumes it via `triage`" that the task text explicitly forecloses.

  Not HIGH: exactly one artifact's template motivates this field, and exactly one correct requiredness (matching its three already-recommended siblings) -- no cross-file runtime tuple or coordinated multi-block edit is required. Not trivial: the field is named in neither the task text nor the contract, five other undeclared template fields sit in the same YAML block as decoys, and the task text's explicit prohibition on adding the field to `agent_brief` only earns its place as a real distractor -- rather than an arbitrary unrelated artifact -- because `agent_brief` is a genuine downstream consumer of `issue_list` via `triage`.
complexity_breakdown_sha256: 6a64352bb33b65270c0df83bf9698ea5380faac19ab7e3f016a91c56112f6f93
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `issue_list` fixture artifact at verification time (see `oracle_spec`, step 3) directly into the patched clone at `artifacts/issue_list.md`; the agent never needs to see or create this file.
initial_state_or_fixture_spec_sha256: f7c3ea10eff765cff76cb6d5447c7eba4903c8ee5c37d0d2055b531fc3578fba
qualification: |
  ADMISSIBLE
