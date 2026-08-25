candidate_id: T2H-W4L
family: T2
complexity_level: HIGH
task_text: |
  This repository's runtime (`scripts/workflow-runtime.py`) defines a hardcoded tuple, `OrchestrationRunner._CONTEXT_ARTIFACT_IDS`, listing exactly which artifacts compose the aggregate `context_artifacts` input that implementation workflows (the `ui-*`, `product-*`, `docs-*` families) receive as one bundle. Read the tuple and its surrounding comment yourself. Two of its members are `problem_frame` and `unknowns_map` -- the two early-pipeline diagnostic artifacts that, per each one's own `consumed_by` list in `skills/workflow-planner/references/artifact-contracts.yaml`, both feed into `repo-sensemaker` on the way to the eventual sensemaking brief.

  Separately, the runtime also contains a method, invoked automatically after every skill produces an artifact, that guarantees a specific deterministic machine field -- one that always points back to the run's single immutable user-intent artifact -- is present in a produced artifact's YAML block, inserting it itself if the producing skill omitted it. Read this method's docstring and body too. Its guard clause is narrow: it only acts when the artifact's own contract entry lists this field under `required_machine_fields` specifically -- listing it under `recommended_machine_fields` instead does not trigger the guarantee at all.

  Four artifacts later in the pipeline already carry this field as required, each because their own contract entry says so: `prd`, `issue_list`, `agent_brief`, and `session_summary`. `problem_frame` and `unknowns_map` -- despite being bundled together as the SAME aggregate `context_artifacts` input by the runtime's own hardcoded tuple, and despite both feeding the same downstream diagnostic consumer -- currently have NEITHER of them declared with this field at all. Fixing only one of the two would leave the bundle internally inconsistent: an implementation workflow consuming `context_artifacts` would get the provenance guarantee on one bundled member but not the other, for no principled reason, since the runtime treats them as equal members of the same group feeding the same downstream consumer.

  Give BOTH `problem_frame` and `unknowns_map` the same guarantee their four downstream siblings already have: add this one field as a REQUIRED machine field on EACH of their own contract entries. It must be required, not recommended, on both -- only a required declaration actually activates the runtime's injection method for a given artifact, and this task requires the guarantee to be real for both bundled artifacts, not merely aspirational for one of them.

  Do not add this field to any other artifact's contract entry -- including `discovery_findings`, which also appears in the same runtime tuple but, unlike `problem_frame` and `unknowns_map`, is not consumed by `repo-sensemaker` at all (it belongs to a separate product-discovery track) and is out of scope. Do not change the requiredness of the field on `repository_sensemaking_brief` or `workflow_orchestration_plan`, which already carry it as recommended -- leave those two exactly as they are. Do not modify `scripts/workflow-runtime.py` or any file other than `skills/workflow-planner/references/artifact-contracts.yaml` -- the runtime's injection method is already written generically against the contract and needs no code change to pick up this edit; only the hardcoded bundle membership itself (which this task does not ask you to change) lives in the runtime file.
task_text_sha256: 13cd2a526ee590bf59db3472b07082ca0a16007eb626445bbaff4db96c1f7dc7
oracle_spec: |
  Verified mechanism (read at frozen SHA `0ffb564b`): `scripts/workflow-runtime.py`'s `OrchestrationRunner._CONTEXT_ARTIFACT_IDS = ("user_intent", "problem_frame", "unknowns_map", "discovery_findings", "repository_sensemaking_brief", "workflow_orchestration_plan")` is the hardcoded bundle the `context_artifacts` aggregate input expands to. `problem_frame`'s own `consumed_by` list is `[unknowns-mapper, repo-sensemaker]`; `unknowns_map`'s is `[repo-sensemaker, prompt-handoff]` -- both real, shared consumption by `repo-sensemaker`. `discovery_findings`'s `consumed_by` is `[opportunity-tree, prompt-handoff]` -- no `repo-sensemaker`, confirming it is a different track despite sharing the same runtime tuple.

  `OrchestrationRunner._ensure_intent_ref(artifact_id, artifact_path)` (called unconditionally for every step's `output_artifact`, right before validation) guarantees `source_intent_ref` on a produced artifact only when `"source_intent_ref" in contract.get("required_machine_fields", [])` for that artifact's contract entry; it never consults `recommended_machine_fields`. `prd`, `issue_list`, `agent_brief`, `session_summary` already declare it required (frozen baseline, unaffected by this task). `repository_sensemaking_brief` and `workflow_orchestration_plan` already declare it *recommended* (frozen baseline) -- deliberately out of scope; the task does not ask for their requiredness to change. `problem_frame` had zero required or recommended machine fields in the frozen baseline; `unknowns_map` had four required fields, none of them `source_intent_ref`.

  Oracle procedure (run against the agent's final repository state, a patched clone at frozen SHA, CLONE_DIR):

  ```python
  import subprocess, sys, importlib.util
  from pathlib import Path
  import yaml

  FROZEN_SHA = "0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5"
  CLONE = Path(CLONE_DIR)
  CONTRACTS = CLONE / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
  RUNTIME_PATH = CLONE / "scripts" / "workflow-runtime.py"
  TARGETS = ("problem_frame", "unknowns_map")

  # 1. STRUCTURAL / ATTRIBUTION CHECK
  contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
  by_id = {a["id"]: a for a in contracts["artifacts"]}

  for tid in TARGETS:
      art = by_id[tid]
      req = set(art.get("required_machine_fields") or [])
      rec = set(art.get("recommended_machine_fields") or [])
      assert "source_intent_ref" in req, f"FAIL: source_intent_ref not declared required on {tid}"
      assert "source_intent_ref" not in rec, f"FAIL: source_intent_ref declared recommended (not required) on {tid}"

  pf = by_id["problem_frame"]
  assert set(pf.get("required_machine_fields") or []) == {"source_intent_ref"}, \
      "FAIL: problem_frame's required_machine_fields contains more than just source_intent_ref"
  um = by_id["unknowns_map"]
  assert set(um.get("required_machine_fields") or []) == {
      "clarity_assessment", "unknowns_count", "assumptions_count", "research_needed", "source_intent_ref",
  }, "FAIL: unknowns_map's required_machine_fields changed unexpectedly"

  df = by_id["discovery_findings"]
  df_fields = set(df.get("required_machine_fields") or []) | set(df.get("recommended_machine_fields") or [])
  assert "source_intent_ref" not in df_fields, \
      "FAIL: source_intent_ref also declared on discovery_findings -- same runtime tuple, but not consumed by repo-sensemaker, out of scope"

  # prd, issue_list, agent_brief, session_summary already require source_intent_ref in the
  # frozen baseline -- verify their state is unchanged rather than asserting disjointness.
  ALREADY_HAD_IT_REQUIRED = ("prd", "issue_list", "agent_brief", "session_summary")
  EXPECTED_REQUIRED = {
      "prd": {"source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_requires_approval"},
      "issue_list": {"source_intent_ref", "user_goal_preserved_as", "scope_expansion_proposed", "scope_expansion_status"},
      "agent_brief": {"source_intent_ref"},
      "session_summary": {"source_intent_ref"},
  }
  for sib in ALREADY_HAD_IT_REQUIRED:
      assert set(by_id[sib].get("required_machine_fields") or []) == EXPECTED_REQUIRED[sib], \
          f"FAIL: {sib}'s required_machine_fields was changed -- out of scope for this task"

  for other_id, other in by_id.items():
      if other_id in TARGETS or other_id in ("repository_sensemaking_brief", "workflow_orchestration_plan") or other_id in ALREADY_HAD_IT_REQUIRED:
          continue
      other_fields = set(other.get("required_machine_fields") or []) | set(other.get("recommended_machine_fields") or [])
      assert "source_intent_ref" not in other_fields, \
          f"FAIL: source_intent_ref also declared on unrelated artifact {other_id!r}"

  rsb = by_id["repository_sensemaking_brief"]
  assert "source_intent_ref" in (rsb.get("recommended_machine_fields") or []), \
      "FAIL: repository_sensemaking_brief's pre-existing recommended source_intent_ref was removed"
  assert "source_intent_ref" not in (rsb.get("required_machine_fields") or []), \
      "FAIL: repository_sensemaking_brief's requiredness for source_intent_ref was changed -- out of scope"
  wop = by_id["workflow_orchestration_plan"]
  assert "source_intent_ref" in (wop.get("recommended_machine_fields") or []), \
      "FAIL: workflow_orchestration_plan's pre-existing recommended source_intent_ref was removed"
  assert "source_intent_ref" not in (wop.get("required_machine_fields") or []), \
      "FAIL: workflow_orchestration_plan's requiredness for source_intent_ref was changed -- out of scope"

  # 2. PROTECTED-STATE CHECK
  diff = subprocess.run(
      ["git", "diff", "--unified=0", FROZEN_SHA, "--",
       "skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  touched = {line.split("id:", 1)[1].strip() for line in diff.splitlines() if line.startswith(("+  - id:", "-  - id:"))}
  assert touched <= set(TARGETS), f"FAIL: diff touches artifact block header(s) other than {TARGETS}: {touched}"

  runtime_diff = subprocess.run(
      ["git", "diff", "--stat", FROZEN_SHA, "--", "scripts/workflow-runtime.py"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout.strip()
  assert runtime_diff == "", f"FAIL: scripts/workflow-runtime.py was modified; this mechanism is already generic and needs no code change:\n{runtime_diff}"

  # 3. AUTHORITATIVE RUNTIME CHECK -- exercise the real _ensure_intent_ref method for BOTH targets
  sys.path.insert(0, str(CLONE / "scripts"))
  spec = importlib.util.spec_from_file_location("workflow_runtime", str(RUNTIME_PATH))
  workflow_runtime = importlib.util.module_from_spec(spec)
  sys.modules["workflow_runtime"] = workflow_runtime
  spec.loader.exec_module(workflow_runtime)
  OrchestrationRunner = workflow_runtime.OrchestrationRunner

  # Sanity: confirm both targets are indeed members of the runtime's own hardcoded bundle
  # tuple, the fact this task's scoping argument depends on.
  assert "problem_frame" in OrchestrationRunner._CONTEXT_ARTIFACT_IDS
  assert "unknowns_map" in OrchestrationRunner._CONTEXT_ARTIFACT_IDS

  FIXTURES = {
      "problem_frame": (
          "# Problem Frame (fixture)\n\n"
          "## 1. Raw Fog\nShort.\n\n"
          "## 2. Problem Under the Problem\nShort.\n\n"
          "## 3. Object Under Pressure\nShort.\n\n"
          "## 4. Failure Mode\nShort.\n\n"
          "## 5. Success Condition\nShort.\n\n"
          "## 6. What Must Be True\nShort.\n\n"
          "## 7. Next Artifact\nUnknowns Map.\n"
      ),
      "unknowns_map": (
          "# Unknowns Map (fixture)\n\n"
          "## Knowns\nShort.\n\n## Unknowns\nShort.\n\n## Assumptions\nShort.\n\n"
          "## Risks\nShort.\n\n## Research Paths\nShort.\n\n## Stopping Rule\nShort.\n\n"
          "```yaml\n"
          "clarity_assessment: medium\n"
          "unknowns_count: 2\n"
          "assumptions_count: 1\n"
          "research_needed: false\n"
          "```\n"
      ),
  }

  frozen_contracts_text = subprocess.run(
      ["git", "show", f"{FROZEN_SHA}:skills/workflow-planner/references/artifact-contracts.yaml"],
      cwd=CLONE, capture_output=True, text=True,
  ).stdout
  frozen_contracts = yaml.safe_load(frozen_contracts_text)

  for artifact_id, content in FIXTURES.items():
      fixture_path = CLONE / "artifacts" / f"{artifact_id}.md"
      fixture_path.write_text(content, encoding="utf-8")
      runner = object.__new__(OrchestrationRunner)
      runner.contracts = contracts  # the agent's edited (post-task) contract, already loaded above
      runner._ensure_intent_ref(artifact_id, str(fixture_path))
      post_edit = fixture_path.read_text(encoding="utf-8")
      assert "source_intent_ref: 00-user-intent.md" in post_edit, \
          f"FAIL: _ensure_intent_ref did not inject source_intent_ref into {artifact_id} given the edited contract"

      # Reference re-run against the UNMODIFIED frozen contract -- must be a no-op for BOTH,
      # proving the injection is caused by this task's contract edit, not pre-existing behavior.
      fixture_path.write_text(content, encoding="utf-8")
      runner_frozen = object.__new__(OrchestrationRunner)
      runner_frozen.contracts = frozen_contracts
      runner_frozen._ensure_intent_ref(artifact_id, str(fixture_path))
      frozen_behavior = fixture_path.read_text(encoding="utf-8")
      assert frozen_behavior == content, \
          f"FAIL: with the unmodified frozen contract, _ensure_intent_ref should have been a no-op for {artifact_id}"

  print("PASS")
  ```

  PASS iff all assertions hold with no `FAIL:` raised.

  Negative cases (must be rejected):
  - **Only one of the two artifacts edited** (most plausibly `problem_frame` alone, since it is the more obviously "empty" contract block): fails the per-target structural loop for whichever artifact was skipped, and independently fails the runtime check in step 3 for that artifact (no injection occurs).
  - **Declared as recommended instead of required on either artifact**: fails the required-field assertion for that artifact, and independently fails the runtime check -- `_ensure_intent_ref`'s guard clause reads only `required_machine_fields`.
  - **Declared on `discovery_findings` instead of, or in addition to, the correct pair**: fails the dedicated `discovery_findings` disjointness assertion; `discovery_findings` shares the same runtime tuple but is not consumed by `repo-sensemaker`, making it a genuinely plausible but wrong third candidate.
  - **"Helpfully" promoting `repository_sensemaking_brief` or `workflow_orchestration_plan`'s existing recommended `source_intent_ref` to required**, reasoning that "the whole tuple should be consistent": fails the dedicated equality assertions for those two artifacts; the task explicitly scopes the requiredness change to the two named artifacts only.
  - **Editing `scripts/workflow-runtime.py`** (e.g., hardcoding a hint or adding a comment) instead of, or in addition to, editing the contract: fails the `runtime_diff == ""` assertion.
oracle_spec_sha256: b2d0369c24123e0b45d1a9650e6c6ecbed1eb0d39dddde3e0d827a15b915df86
complexity_breakdown: |
  This is a genuine two-block coordinated edit, not a single-block promotion dressed up as HIGH: (1) `problem_frame` and `unknowns_map` are a real, verifiable pair -- both members of the same hardcoded runtime bundle (`OrchestrationRunner._CONTEXT_ARTIFACT_IDS`) AND both genuinely consumed by the same downstream skill (`repo-sensemaker`, per each artifact's own `consumed_by` list) -- not merely two blocks that "also happen to need the same field" by loose analogy. Getting the task right requires editing BOTH contract blocks in the same way; editing only one leaves the bundle's internal consistency claim in the task text unsatisfied, and the oracle's structural loop independently fails for whichever artifact was skipped. This mirrors the shape of this same set's `T2H-Q5X` (a producer-chain coupling between two real blocks) rather than the earlier single-block, convention-inferred design this candidate started from. (2) The correct scope is bounded by a real, checkable distinguishing fact -- `discovery_findings` sits in the identical runtime tuple but is not consumed by `repo-sensemaker` -- giving a textually tempting third-artifact near-miss that a shallow "add it everywhere in the tuple" reading would fail on. (3) `repository_sensemaking_brief` and `workflow_orchestration_plan` (the tuple's other two non-`user_intent` members) already carry the field as *recommended*, creating a further plausible-but-wrong "make the whole tuple consistent by promoting these too" temptation that the task text and oracle both explicitly guard against. (4) As before, the requiredness decision on each of the two target artifacts is independently, mechanically verified by executing the real runtime method (`OrchestrationRunner._ensure_intent_ref`) against fixtures, not just asserted via static YAML shape.

  Not manufactured-obscure: every fact cited (the runtime tuple's exact membership, each artifact's `consumed_by` list, the four already-required siblings, the two already-recommended siblings) is directly readable in two files at fixed locations. Not MEDIUM: correctness requires two coordinated block edits plus reasoning about a five-artifact scope boundary (2 in scope, 1 same-tuple decoy out of scope, 2 already-correct-as-recommended decoys out of scope) -- a genuinely richer relationship-and-near-miss space than a single-field promotion.
complexity_breakdown_sha256: 10da2e6458c03291ae650e1b2cc75ce536f3a606e409846227df4775e990fb75
initial_state_or_fixture_spec: |
  Frozen SHA repo state, no fixture changes required by the agent. The oracle writes its own throwaway `problem_frame` and `unknowns_map` fixture artifacts at verification time (see `oracle_spec`, step 3), directly into the patched clone at `artifacts/problem_frame.md` and `artifacts/unknowns_map.md`, and reuses them for the frozen-contract reference re-run; the agent never needs to see or create these files.
initial_state_or_fixture_spec_sha256: 98b56fc8c80174470717c89bb8632f81c332d9b2d3bace067490d9ff67333768
qualification: |
  ADMISSIBLE
